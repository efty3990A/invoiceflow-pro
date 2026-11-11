"""InvoiceFlow Pro API: Flask sessions, CSRF protection, role and owner scoping."""
from __future__ import annotations

import hmac
import json
import os
import secrets
import sqlite3
import time
from collections import defaultdict, deque
from functools import wraps
from pathlib import Path
from typing import Callable

from flask import Flask, abort, jsonify, request, send_from_directory, session
from werkzeug.security import check_password_hash

ROOT = Path(__file__).resolve().parents[1]
DB = Path(os.environ.get("DATABASE_PATH", str(ROOT / "database" / "invoiceflow.sqlite3"))).expanduser()
SECRET_KEY = os.environ.get("SECRET_KEY", "").strip()
if len(SECRET_KEY) < 32:
    raise RuntimeError("SECRET_KEY must be set to a unique random value of at least 32 characters.")

app = Flask(__name__, static_folder=str(ROOT), static_url_path="")
app.secret_key = SECRET_KEY
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=os.environ.get("COOKIE_SECURE", "1") == "1",
    MAX_CONTENT_LENGTH=1 * 1024 * 1024,
    JSON_SORT_KEYS=False,
)

# Lightweight per-process throttling for public demo/login endpoints.
_attempts: dict[str, deque[float]] = defaultdict(deque)

def limited(key: str, maximum: int = 12, window: int = 60) -> bool:
    now = time.monotonic()
    q = _attempts[key]
    while q and now - q[0] > window:
        q.popleft()
    if len(q) >= maximum:
        return False
    q.append(now)
    return True


def connect() -> sqlite3.Connection:
    DB.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(DB, timeout=10)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys=ON")
    con.execute("PRAGMA busy_timeout=10000")
    return con


def authenticated(role: str | None = None, mutation: bool = False) -> Callable:
    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapped(*args, **kwargs):
            if not session.get("user_id"):
                return jsonify(error="Authentication required"), 401
            if role and session.get("role") != role:
                return jsonify(error="Insufficient role"), 403
            if mutation:
                supplied = request.headers.get("X-CSRF-Token", "")
                expected = session.get("csrf_token", "")
                if not supplied or not expected or not hmac.compare_digest(supplied, expected):
                    return jsonify(error="CSRF validation failed"), 403
            return fn(*args, **kwargs)
        return wrapped
    return decorator


@app.after_request
def security_headers(response):
    # Vibe96 demo bar must be able to frame the public demo.
    response.headers.pop("X-Frame-Options", None)
    response.headers["Content-Security-Policy"] = "default-src 'self' https: data:; script-src 'self' 'unsafe-inline' https://vibe96.com; style-src 'self' 'unsafe-inline' https:; img-src 'self' data: https:; connect-src 'self' https:; frame-ancestors https://vibe96.com https://*.vibe96.com 'self'"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
    return response


@app.get("/healthz")
def healthz():
    try:
        with connect() as db:
            db.execute("SELECT 1")
        return jsonify(status="ok"), 200
    except sqlite3.Error:
        return jsonify(status="error"), 503


@app.get("/")
def home():
    return send_from_directory(ROOT, "index.html")


@app.get("/<path:path>")
def static_files(path: str):
    if path == "workspace.html" and not session.get("user_id"):
        return send_from_directory(ROOT, "login.html"), 401
    target = (ROOT / path).resolve()
    if ROOT.resolve() not in target.parents or not target.is_file():
        abort(404)
    return send_from_directory(ROOT, path)


def establish_session(row: sqlite3.Row):
    session.clear()  # rotate session state on authentication
    session["user_id"] = int(row["id"])
    session["username"] = row["username"]
    session["role"] = row["role"]
    session["csrf_token"] = secrets.token_urlsafe(32)


@app.post("/api/login")
def login():
    ip = request.headers.get("X-Forwarded-For", request.remote_addr or "unknown").split(",")[0].strip()
    if not limited(f"login:{ip}"):
        return jsonify(error="Too many attempts. Try again shortly."), 429
    data = request.get_json(silent=True) or {}
    username = str(data.get("username", ""))[:80]
    password = str(data.get("password", ""))[:256]
    with connect() as db:
        row = db.execute("SELECT id, username, password_hash, role FROM users WHERE username=? AND active=1", (username,)).fetchone()
    if not row or not check_password_hash(row["password_hash"], password):
        return jsonify(error="Invalid credentials"), 401
    establish_session(row)
    return jsonify(username=row["username"], role=row["role"], csrf_token=session["csrf_token"])


@app.post("/api/demo-login/<role>")
def demo_login(role: str):
    """One-click reviewer access; can be disabled with ENABLE_DEMO_LOGIN=0."""
    if os.environ.get("ENABLE_DEMO_LOGIN", "1") != "1":
        return jsonify(error="Demo login is disabled"), 404
    if role not in {"admin", "user"}:
        return jsonify(error="Unknown demo role"), 404
    ip = request.headers.get("X-Forwarded-For", request.remote_addr or "unknown").split(",")[0].strip()
    if not limited(f"demo:{ip}", maximum=20):
        return jsonify(error="Too many demo sessions. Try again shortly."), 429
    with connect() as db:
        row = db.execute("SELECT id, username, role FROM users WHERE username=? AND role=? AND active=1", (f"demo-{role}", role)).fetchone()
    if not row:
        return jsonify(error="Demo account is not initialized"), 503
    establish_session(row)
    return jsonify(username=row["username"], role=row["role"], csrf_token=session["csrf_token"])


@app.post("/api/logout")
@authenticated(mutation=True)
def logout():
    session.clear()
    return jsonify(ok=True)


@app.get("/api/me")
@authenticated()
def me():
    return jsonify(username=session["username"], role=session["role"], csrf_token=session["csrf_token"])


@app.get("/api/invoices")
@authenticated()
def invoices():
    with connect() as db:
        rows = db.execute("SELECT id, invoice_number, client_name, total, currency, status, created_at FROM invoices WHERE owner_id=? ORDER BY id DESC", (session["user_id"],)).fetchall()
    return jsonify([dict(row) for row in rows])


@app.post("/api/invoices")
@authenticated(mutation=True)
def create_invoice():
    data = request.get_json(silent=True) or {}
    required = ("invoice_number", "client_name", "total", "currency")
    if any(data.get(key) in (None, "") for key in required):
        return jsonify(error="Missing required fields"), 400
    try:
        total = float(data["total"])
        if not (0 <= total < 1_000_000_000):
            raise ValueError
    except (TypeError, ValueError):
        return jsonify(error="Invalid total"), 400
    values = (session["user_id"], str(data["invoice_number"])[:80], str(data["client_name"])[:160], total, str(data["currency"])[:8], str(data.get("status", "Unpaid"))[:20], json.dumps(data, separators=(",", ":")))
    try:
        with connect() as db:
            cur = db.execute("INSERT INTO invoices(owner_id,invoice_number,client_name,total,currency,status,payload) VALUES(?,?,?,?,?,?,?)", values)
            return jsonify(id=cur.lastrowid), 201
    except sqlite3.IntegrityError:
        return jsonify(error="Invoice number already exists for this account"), 409


@app.put("/api/invoices/<int:invoice_id>")
@authenticated(mutation=True)
def update_invoice(invoice_id: int):
    data = request.get_json(silent=True) or {}
    try:
        total = float(data.get("total", 0))
        if not (0 <= total < 1_000_000_000):
            raise ValueError
    except (TypeError, ValueError):
        return jsonify(error="Invalid total"), 400
    values = (str(data.get("invoice_number", ""))[:80], str(data.get("client_name", ""))[:160], total, str(data.get("currency", "BDT"))[:8], str(data.get("status", "Unpaid"))[:20], json.dumps(data, separators=(",", ":")), invoice_id, session["user_id"])
    with connect() as db:
        cur = db.execute("UPDATE invoices SET invoice_number=?,client_name=?,total=?,currency=?,status=?,payload=? WHERE id=? AND owner_id=?", values)
    if not cur.rowcount:
        return jsonify(error="Invoice not found"), 404
    return jsonify(ok=True)


@app.delete("/api/invoices/<int:invoice_id>")
@authenticated(mutation=True)
def delete_invoice(invoice_id: int):
    with connect() as db:
        cur = db.execute("DELETE FROM invoices WHERE id=? AND owner_id=?", (invoice_id, session["user_id"]))
    if not cur.rowcount:
        return jsonify(error="Invoice not found"), 404
    return jsonify(ok=True)


@app.get("/api/admin/users")
@authenticated(role="admin")
def admin_users():
    with connect() as db:
        rows = db.execute("SELECT id,username,role,active,created_at FROM users ORDER BY id").fetchall()
    return jsonify([dict(row) for row in rows])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "5000")))
