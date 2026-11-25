#!/usr/bin/env python3
"""REST API for AutoFlow, backed by PostgreSQL through psycopg 3."""
import json
import os
import sys
from datetime import date
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parent

def load_local_env():
    """Read simple KEY=VALUE settings without requiring a dotenv package."""
    env_file = ROOT / ".env"
    if not env_file.exists():
        return
    for line in env_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip("\"'"))

load_local_env()
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/autoflow_db")

try:
    import psycopg
    from psycopg.rows import dict_row
except ImportError:
    print("PostgreSQL driver missing. Install it with: python -m pip install -r requirements.txt", file=sys.stderr)
    raise SystemExit(1)

COLLECTIONS = {
    "vehicles": ("vehicles", "vehicle_id", {"make", "model", "year", "license_plate", "category", "daily_rate", "mileage", "status", "image_color"}),
    "customers": ("customers", "customer_id", {"full_name", "email", "phone", "license_number", "joined_on"}),
    "bookings": ("bookings", "booking_id", {"customer_id", "vehicle_id", "pickup_date", "return_date", "status", "estimated_total"}),
    "rentals": ("rentals", "rental_id", {"customer_id", "vehicle_id", "booking_id", "start_date", "end_date", "actual_return_date", "status", "total_amount"}),
    "payments": ("payments", "payment_id", {"rental_id", "amount", "payment_date", "method", "status", "reference"}),
    "maintenance": ("maintenance", "maintenance_id", {"vehicle_id", "service_type", "description", "service_date", "cost", "status"}),
}

def connect():
    return psycopg.connect(DATABASE_URL, row_factory=dict_row, connect_timeout=5)

def initialize():
    """Apply idempotent schema and seed demo rows to the configured database."""
    db = connect()
    try:
        db.execute((ROOT / "sql" / "schema.sql").read_text(encoding="utf-8"), prepare=False)
        if db.execute("SELECT 1 FROM customers LIMIT 1").fetchone() is None:
            db.execute((ROOT / "sql" / "seed.sql").read_text(encoding="utf-8"), prepare=False)
        batch_key = "india_demo_batch_50_v1"
        if db.execute("SELECT 1 FROM app_migrations WHERE migration_key=%s", (batch_key,)).fetchone() is None:
            db.execute((ROOT / "sql" / "additional_demo_data.sql").read_text(encoding="utf-8"), prepare=False)
            db.execute("INSERT INTO app_migrations(migration_key) VALUES (%s)", (batch_key,))
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

def as_dicts(rows):
    return [dict(row) for row in rows]

def database_metadata(db):
    table_rows = as_dicts(db.execute("""
        SELECT table_name AS name, 'table' AS type
        FROM information_schema.tables
        WHERE table_schema = current_schema() AND table_type = 'BASE TABLE' AND table_name <> 'app_migrations'
        UNION ALL
        SELECT table_name AS name, 'view' AS type
        FROM information_schema.views WHERE table_schema = current_schema()
        ORDER BY type, name
    """))
    base_tables = [row["name"] for row in table_rows if row["type"] == "table"]
    schema, foreign_keys, indexes = {}, {}, {}
    for table in base_tables:
        schema[table] = as_dicts(db.execute("""
            SELECT c.column_name AS name, c.data_type AS type,
                   (c.is_nullable = 'NO') AS notnull,
                   (pk.column_name IS NOT NULL) AS pk
            FROM information_schema.columns c
            LEFT JOIN (
                SELECT kcu.table_name, kcu.column_name
                FROM information_schema.table_constraints tc
                JOIN information_schema.key_column_usage kcu
                  ON tc.constraint_name=kcu.constraint_name AND tc.table_schema=kcu.table_schema
                WHERE tc.constraint_type='PRIMARY KEY' AND tc.table_schema=current_schema()
            ) pk ON pk.table_name=c.table_name AND pk.column_name=c.column_name
            WHERE c.table_schema=current_schema() AND c.table_name=%s
            ORDER BY c.ordinal_position
        """, (table,)))
        foreign_keys[table] = as_dicts(db.execute("""
            SELECT kcu.column_name AS "from", ccu.table_name AS "table", ccu.column_name AS "to"
            FROM information_schema.table_constraints tc
            JOIN information_schema.key_column_usage kcu
              ON tc.constraint_name=kcu.constraint_name AND tc.table_schema=kcu.table_schema
            JOIN information_schema.constraint_column_usage ccu
              ON ccu.constraint_name=tc.constraint_name AND ccu.constraint_schema=tc.constraint_schema
            WHERE tc.constraint_type='FOREIGN KEY' AND tc.table_schema=current_schema() AND tc.table_name=%s
        """, (table,)))
        indexes[table] = as_dicts(db.execute("""
            SELECT indexname AS name, indexdef AS definition
            FROM pg_indexes WHERE schemaname=current_schema() AND tablename=%s
        """, (table,)))
    view_row = db.execute("SELECT definition FROM pg_views WHERE schemaname=current_schema() AND viewname='rental_details'").fetchone()
    return {"tables": table_rows, "schema": schema, "foreignKeys": foreign_keys,
            "indexes": indexes, "viewSql": view_row["definition"] if view_row else ""}

class Api(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        print("%s - %s" % (self.address_string(), fmt % args))

    def send_json(self, payload, status=200):
        body = json.dumps(payload, default=str).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PATCH, DELETE, OPTIONS")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_json({"ok": True})

    def read_body(self):
        size = int(self.headers.get("Content-Length", 0))
        return json.loads(self.rfile.read(size) or b"{}")

    def do_GET(self):
        path = urlparse(self.path).path.strip("/").split("/")
        if path[0] != "api":
            return self.send_json({"error": "Not found"}, 404)
        db = None
        try:
            db = connect()
            if len(path) == 2 and path[1] == "dashboard":
                today = date.today()
                stats = {
                    "vehicles": db.execute("SELECT COUNT(*) FROM vehicles").fetchone()["count"],
                    "available": db.execute("SELECT COUNT(*) FROM vehicles WHERE status='Available'").fetchone()["count"],
                    "activeRentals": db.execute("SELECT COUNT(*) FROM rentals WHERE status IN ('Active','Overdue')").fetchone()["count"],
                    "customers": db.execute("SELECT COUNT(*) FROM customers").fetchone()["count"],
                    "revenue": db.execute("SELECT COALESCE(SUM(amount),0) AS value FROM payments WHERE status='Paid'").fetchone()["value"],
                    "maintenance": db.execute("SELECT COUNT(*) FROM maintenance WHERE status IN ('Scheduled','In progress')").fetchone()["count"],
                    "upcomingBookings": db.execute("SELECT COUNT(*) FROM bookings WHERE status IN ('Pending','Confirmed') AND pickup_date >= %s", (today,)).fetchone()["count"],
                }
                recent = as_dicts(db.execute("SELECT * FROM rental_details ORDER BY rental_id DESC LIMIT 6"))
                fleet = as_dicts(db.execute("SELECT * FROM vehicles ORDER BY vehicle_id"))
                return self.send_json({"stats": stats, "recent": recent, "fleet": fleet})
            if len(path) == 2 and path[1] == "database":
                return self.send_json(database_metadata(db))
            if len(path) == 2 and path[1] == "query":
                query_id = parse_qs(urlparse(self.path).query).get("id", [""])[0]
                queries = {
                    "fleet-status": ("Fleet status", "SELECT status, COUNT(*) AS vehicles FROM vehicles GROUP BY status ORDER BY vehicles DESC", "GROUP BY · Aggregate fleet availability by status"),
                    "revenue-month": ("Revenue by month", "SELECT TO_CHAR(payment_date, 'YYYY-MM') AS month, SUM(amount) AS revenue, COUNT(*) AS transactions FROM payments WHERE status='Paid' GROUP BY month ORDER BY month DESC", "SUM · Monthly revenue from paid transactions"),
                    "customer-lifetime": ("Customer lifetime value", "SELECT c.full_name, COUNT(r.rental_id) AS rentals, COALESCE(SUM(r.total_amount),0) AS lifetime_value FROM customers c LEFT JOIN rentals r ON r.customer_id=c.customer_id GROUP BY c.customer_id ORDER BY lifetime_value DESC LIMIT 8", "LEFT JOIN · Keep customers with no rentals in the result"),
                    "rental-ledger": ("Rental payment ledger", "SELECT * FROM rental_details ORDER BY rental_id DESC", "VIEW · Join rentals, customers, vehicles, and payments"),
                    "service-cost": ("Maintenance costs by vehicle", "SELECT v.make || ' ' || v.model AS vehicle, COUNT(m.maintenance_id) AS services, COALESCE(SUM(m.cost),0) AS total_service_cost FROM vehicles v LEFT JOIN maintenance m ON m.vehicle_id=v.vehicle_id GROUP BY v.vehicle_id ORDER BY total_service_cost DESC", "LEFT JOIN · Aggregate service costs without dropping untouched vehicles"),
                }
                if query_id not in queries:
                    return self.send_json({"error": "Unknown saved query"}, 404)
                title, sql, note = queries[query_id]
                return self.send_json({"title": title, "sql": sql, "note": note, "rows": as_dicts(db.execute(sql))})
            if len(path) < 2 or path[1] not in COLLECTIONS:
                return self.send_json({"error": "Unknown resource"}, 404)
            table, key, _ = COLLECTIONS[path[1]]
            if table == "rentals":
                query = "SELECT r.*, c.full_name AS customer_name, v.make || ' ' || v.model AS vehicle_name, v.license_plate FROM rentals r JOIN customers c USING(customer_id) JOIN vehicles v USING(vehicle_id) ORDER BY r.rental_id DESC"
            elif table == "bookings":
                query = "SELECT b.*, c.full_name AS customer_name, v.make || ' ' || v.model AS vehicle_name, v.license_plate FROM bookings b JOIN customers c USING(customer_id) JOIN vehicles v USING(vehicle_id) ORDER BY b.booking_id DESC"
            elif table == "payments":
                query = "SELECT p.*, c.full_name AS customer_name, v.make || ' ' || v.model AS vehicle_name FROM payments p JOIN rentals r USING(rental_id) JOIN customers c USING(customer_id) JOIN vehicles v USING(vehicle_id) ORDER BY p.payment_id DESC"
            elif table == "maintenance":
                query = "SELECT m.*, v.make || ' ' || v.model AS vehicle_name, v.license_plate FROM maintenance m JOIN vehicles v USING(vehicle_id) ORDER BY m.maintenance_id DESC"
            else:
                query = f"SELECT * FROM {table} ORDER BY {key} DESC"
            return self.send_json(as_dicts(db.execute(query)))
        except psycopg.Error as e:
            return self.send_json({"error": str(e).strip()}, 500)
        finally:
            if db:
                db.close()

    def do_POST(self):
        p = urlparse(self.path).path.strip("/").split("/")
        if len(p) != 2 or p[0] != "api" or p[1] not in COLLECTIONS:
            return self.send_json({"error": "Unknown resource"}, 404)
        table, key, allowed = COLLECTIONS[p[1]]
        values = {k: v for k, v in self.read_body().items() if k in allowed}
        if not values:
            return self.send_json({"error": "Provide fields to create this record."}, 400)
        db = connect()
        try:
            if table == "rentals":
                vehicle = db.execute("SELECT status FROM vehicles WHERE vehicle_id=%s FOR UPDATE", (values.get("vehicle_id"),)).fetchone()
                if not vehicle or vehicle["status"] != "Available":
                    raise ValueError("This vehicle is not available for a new rental.")
            if table == "bookings":
                if values.get("pickup_date", "") < date.today().isoformat():
                    raise ValueError("Pickup date must be today or later.")
                values.setdefault("status", "Confirmed")
            if table == "customers" and values.get("email"):
                values["email"] = values["email"].strip().lower()
            cols = list(values)
            placeholders = ",".join(["%s"] * len(cols))
            cur = db.execute(f"INSERT INTO {table} ({','.join(cols)}) VALUES ({placeholders}) RETURNING {key}", [values[c] for c in cols])
            row_id = cur.fetchone()[key]
            row = db.execute(f"SELECT * FROM {table} WHERE {key}=%s", (row_id,)).fetchone()
            db.commit()
            return self.send_json(dict(row), 201)
        except ValueError as e:
            db.rollback()
            return self.send_json({"error": str(e)}, 409)
        except psycopg.IntegrityError as e:
            db.rollback()
            return self.send_json({"error": str(e).strip()}, 400)
        except psycopg.Error as e:
            db.rollback()
            return self.send_json({"error": str(e).strip()}, 400)
        finally:
            db.close()

    def do_PATCH(self):
        p = urlparse(self.path).path.strip("/").split("/")
        if len(p) != 3 or p[0] != "api" or p[1] not in COLLECTIONS:
            return self.send_json({"error": "Unknown resource"}, 404)
        table, key, allowed = COLLECTIONS[p[1]]
        values = {k: v for k, v in self.read_body().items() if k in allowed}
        if not values:
            return self.send_json({"error": "No editable fields supplied."}, 400)
        if table == "customers" and values.get("email"):
            values["email"] = values["email"].strip().lower()
        db = connect()
        try:
            cols = list(values)
            assignments = ",".join(c + "=%s" for c in cols)
            cur = db.execute(f"UPDATE {table} SET {assignments} WHERE {key}=%s", [values[c] for c in cols] + [p[2]])
            if cur.rowcount == 0:
                db.rollback()
                return self.send_json({"error": "Record not found."}, 404)
            row = db.execute(f"SELECT * FROM {table} WHERE {key}=%s", (p[2],)).fetchone()
            db.commit()
            return self.send_json(dict(row))
        except psycopg.IntegrityError as e:
            db.rollback()
            return self.send_json({"error": str(e).strip()}, 400)
        except psycopg.Error as e:
            db.rollback()
            return self.send_json({"error": str(e).strip()}, 400)
        finally:
            db.close()

    def do_DELETE(self):
        p = urlparse(self.path).path.strip("/").split("/")
        if len(p) != 3 or p[0] != "api" or p[1] not in COLLECTIONS:
            return self.send_json({"error": "Unknown resource"}, 404)
        table, key, _ = COLLECTIONS[p[1]]
        db = connect()
        try:
            cur = db.execute(f"DELETE FROM {table} WHERE {key}=%s", (p[2],))
            if cur.rowcount == 0:
                db.rollback()
                return self.send_json({"error": "Record not found."}, 404)
            db.commit()
            return self.send_json({"ok": True})
        except psycopg.IntegrityError as e:
            db.rollback()
            return self.send_json({"error": str(e).strip()}, 409)
        finally:
            db.close()

if __name__ == "__main__":
    try:
        initialize()
    except psycopg.OperationalError as e:
        print("Could not connect to PostgreSQL. Check that the service is running, the database exists, and DATABASE_URL is correct.", file=sys.stderr)
        print(str(e).strip(), file=sys.stderr)
        raise SystemExit(1)
    except psycopg.Error as e:
        print(f"Could not initialize the PostgreSQL schema: {e}", file=sys.stderr)
        raise SystemExit(1)
    print(f"AutoFlow API ready · PostgreSQL: {DATABASE_URL.rsplit('/', 1)[-1]}")
    ThreadingHTTPServer(("127.0.0.1", 8000), Api).serve_forever()
