# AutoFlow — DBMS Capstone

A fleet and rental operations dashboard backed by PostgreSQL. It covers vehicles, customers, bookings, rentals, payments, and vehicle maintenance, with transactional API operations, foreign keys, indexes, triggers, a reporting view, and live database documentation.

The demo is localized for an Indian rental fleet: prices display in INR, dates use Indian formatting, mileage is in kilometres, and sample vehicles, registrations, contact numbers, and customer names reflect the local market. It includes 50 additional synthetic sample records across all six business tables for richer dashboard and query-lab examples.

## Prerequisites

- PostgreSQL 14+ installed and running locally (pgAdmin is included with the Windows installer).
- Python 3.10+ and Node.js 20+.

## First-time setup on Windows

1. In pgAdmin, connect to your local PostgreSQL server. Create a database named `autoflow_db` (right-click **Databases** → **Create** → **Database**). The API user needs permission to create tables, indexes, functions, and triggers in its schema.
2. Copy `.env.example` to `.env` and set `DATABASE_URL` to your PostgreSQL username and password. In PowerShell:

   ```powershell
   Copy-Item .env.example .env
   notepad .env
   ```

   The example uses `postgres` as the user; replace `YOUR_PASSWORD` with the password chosen during PostgreSQL installation.
3. Open PowerShell in this project folder and install the Python adapter:

   ```powershell
   python -m pip install -r requirements.txt
   ```

4. Start the API in one terminal:

   ```powershell
   npm run api
   ```

   On the first start, the API applies `sql/schema.sql` and loads `sql/seed.sql` if the database has no customers. Keep this terminal open; it should show `AutoFlow API ready`.

5. Start the website in a second terminal in the project folder:

   ```powershell
   npm install
   npm run dev
   ```

6. Open the `http://localhost:5173` address printed by Vite.

## PostgreSQL connection

The API reads `DATABASE_URL` from `.env` or the process environment. Example:

```text
postgresql://postgres:YOUR_PASSWORD@localhost:5432/autoflow_db
```

If the password includes URL-reserved characters, URL-encode them in the connection string. Never commit `.env` or share its password.

## DBMS features

- 3NF-oriented entities with primary keys, foreign keys, unique constraints, checks, and explicit delete behavior.
- Indexes on common search and join paths; a view for rental detail reporting.
- Rental creation locks the selected vehicle row inside a PostgreSQL transaction to prevent two concurrent rentals from taking the same available car.
- Database triggers synchronize vehicle availability with rental and maintenance status changes.
- The in-app Database page reads table, column, relationship, and index metadata from PostgreSQL catalogs and runs a curated set of read-only SQL examples.

## Project layout

- `src/` — React interface and styling
- `server.py` — Python REST API using Psycopg 3
- `requirements.txt` — Python dependencies
- `sql/schema.sql` — PostgreSQL schema, indexes, view, and triggers
- `sql/seed.sql` — initial sample data for a ready-to-use demo
- `sql/additional_demo_data.sql` — one-time 50-record demo batch, tracked by the API migration ledger

The previous SQLite file, if present, is not used by the PostgreSQL API. The demo data is seeded into PostgreSQL on its first API start; existing SQLite changes are not automatically migrated.
