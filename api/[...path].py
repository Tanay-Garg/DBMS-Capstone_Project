"""Vercel catch-all function for the existing AutoFlow REST API."""
import logging
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import server

_initialized = False


class handler(server.Api):
    """Adapt the project's HTTP API handler to Vercel's Python runtime."""

    def log_message(self, fmt, *args):
        logging.info("%s - %s", self.address_string(), fmt % args)

    def _initialize_database(self):
        global _initialized
        if not os.getenv("DATABASE_URL"):
            raise RuntimeError("DATABASE_URL is not configured for this deployment.")
        if not _initialized:
            server.initialize()
            _initialized = True

    def _dispatch(self, method):
        try:
            self._initialize_database()
        except Exception:
            logging.exception("AutoFlow database initialization failed")
            return self.send_json({"error": "The database is not ready. Check the deployment's DATABASE_URL setting."}, 503)
        return getattr(super(), method)()

    def do_GET(self):
        return self._dispatch("do_GET")

    def do_POST(self):
        return self._dispatch("do_POST")

    def do_PATCH(self):
        return self._dispatch("do_PATCH")

    def do_DELETE(self):
        return self._dispatch("do_DELETE")

    def do_OPTIONS(self):
        return super().do_OPTIONS()
