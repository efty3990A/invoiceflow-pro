"""Create schema and non-production demo accounts from environment variables."""
import os
import secrets
import sqlite3
from pathlib import Path
from werkzeug.security import generate_password_hash

ROOT = Path(__file__).resolve().parents[1]
DB = Path(os.environ.get("DATABASE_PATH", str(ROOT / "database" / "invoiceflow.sqlite3"))).expanduser()
DB.parent.mkdir(parents=True, exist_ok=True)

# Demo users are deliberately created with per-deployment random passwords.
# No default password or credential is shipped in source control.
admin_password = os.environ.get("DEMO_ADMIN_PASSWORD", "").strip()
user_password = os.environ.get("DEMO_USER_PASSWORD", "").strip()
if not admin_password or not user_password:
    if os.environ.get("ALLOW_RANDOM_DEMO_PASSWORDS", "1") == "1":
        admin_password = admin_password or secrets.token_urlsafe(24)
        user_password = user_password or secrets.token_urlsafe(24)
        print("Generated one-time demo credentials (save these securely):")
        print(f"DEMO_ADMIN_PASSWORD={admin_password}")
        print(f"DEMO_USER_PASSWORD={user_password}")
    else:
        raise SystemExit("Set DEMO_ADMIN_PASSWORD and DEMO_USER_PASSWORD before seeding.")
if min(len(admin_password), len(user_password)) < 16:
    raise SystemExit("Demo passwords must each contain at least 16 characters.")

with sqlite3.connect(DB) as db:
    db.execute("PRAGMA foreign_keys=ON")
    db.executescript((ROOT / "database" / "schema.sql").read_text(encoding="utf-8"))
    for username, password, role in (("demo-admin", admin_password, "admin"), ("demo-user", user_password, "user")):
        db.execute(
            "INSERT INTO users(username,password_hash,role) VALUES(?,?,?) "
            "ON CONFLICT(username) DO UPDATE SET password_hash=excluded.password_hash, role=excluded.role, active=1",
            (username, generate_password_hash(password, method="scrypt"), role),
        )
print(f"Database initialized: {DB}")
