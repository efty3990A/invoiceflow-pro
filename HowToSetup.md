# InvoiceFlow Pro 1.2.0 — Clean Installation

## Stack
HTML5, CSS3, Vanilla JavaScript; Flask 3.1.2 API; SQLite; Gunicorn; Docker. The original invoice editor retains browser Local Storage for its existing draft/history workflow. The authenticated API stores its own invoice records in SQLite; the two stores are intentionally documented as separate until an explicit migration/sync feature is implemented.

## Required configuration
Copy `.env.example` to a private `.env`. Set a unique `SECRET_KEY` (at least 32 random characters), two different demo passwords (at least 16 characters each), and `DATABASE_PATH`. Never commit `.env` or production credentials. The source archive contains placeholders only.

## VPS / Python installation
1. Install Python 3.12 and a virtual environment.
2. `python -m venv .venv` then activate it.
3. `pip install -r requirements.lock`.
4. Export variables from your private `.env` (or load them with your process manager).
5. Run `python database/seed.py` to create schema and demo accounts.
6. Run `gunicorn --bind 0.0.0.0:${PORT:-5000} --workers 2 --threads 4 backend.app:app`.
7. Put HTTPS reverse proxy in front; set `COOKIE_SECURE=1`.

## Docker
1. Install Docker Engine and Docker Compose.
2. Copy `.env.example` to `.env`, replace all placeholders with unique values.
3. Run `docker compose up --build -d`.
4. Visit `http://localhost:5000`; health check is `/healthz`.
5. Stop with `docker compose down`; named volume `invoiceflow_data` persists SQLite data.

## Demo access
The login page provides one-click Admin and User demo sessions through `/api/demo-login/<role>`. This is intentionally enabled for marketplace review and can be disabled by setting `ENABLE_DEMO_LOGIN=0`. The demo accounts are seeded with deployment-specific passwords from `DEMO_ADMIN_PASSWORD` and `DEMO_USER_PASSWORD`; no default passwords are embedded in source. The public demo-login feature should be used only with non-production sample data.

## Security controls
- `SECRET_KEY` is mandatory; startup fails if missing or shorter than 32 characters.
- Passwords are stored as scrypt hashes.
- Session cookies are HttpOnly and SameSite=Lax; set Secure on HTTPS.
- Mutating API endpoints require authentication and a session CSRF token in `X-CSRF-Token`.
- Admin routes enforce the admin role; invoice queries and mutations are scoped to the current owner. The workspace page is not served to anonymous sessions.
- SQL uses parameterized statements; foreign keys and indexes are created from `database/schema.sql`.
- `/healthz` is available for hosting health checks.
- Vibe96 framing is permitted by CSP; no X-Frame-Options header is emitted.

## API summary
`POST /api/login`, `POST /api/demo-login/admin|user`, `POST /api/logout`, `GET /api/me`, `GET|POST /api/invoices`, `PUT|DELETE /api/invoices/<id>`, `GET /api/admin/users`, `GET /healthz`.

## Branding
Edit landing page copy in `index.html`, styles in `assets/css/`, and screenshots in `screenshots/`.
