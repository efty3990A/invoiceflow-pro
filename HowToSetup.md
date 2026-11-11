# InvoiceFlow Pro 1.1.0 — Installation and Demo

## Architecture and important product boundary
The package includes the original browser-based invoice editor (HTML/CSS/vanilla JS; invoice history and drafts use browser Local Storage) plus a Flask/SQLite authentication and invoice API. The editor's existing Local Storage workflow is retained for backward compatibility; it is not silently represented as cloud-synchronised data. API invoice records are stored in SQLite and scoped to the signed-in account.

## Requirements
Python 3.11+ and pip. Docker is optional. No Node.js build is required for the product UI.

## VPS / local Python installation
1. Extract the ZIP and enter the `invoiceflow-pro` folder.
2. Create a virtual environment: `python -m venv .venv`.
3. Activate it (Windows: `.venv\\Scripts\\activate`; Linux/macOS: `source .venv/bin/activate`).
4. Install pinned packages: `pip install -r requirements.txt`.
5. Copy `.env.example` to `.env` and set a unique `SECRET_KEY`. Load the variables into your process environment; do not commit `.env`.
6. Create schema and demo accounts: `python database/seed.py`.
7. Start: `python backend/app.py` and open `http://localhost:5000`.
8. For public VPS use, put a production WSGI server and HTTPS reverse proxy in front of Flask; set `COOKIE_SECURE=1`, use a strong secret, and restrict filesystem permissions.

## Docker installation
1. Install Docker Engine and Docker Compose.
2. Set a strong `SECRET_KEY` in the shell or a private `.env` file.
3. Run `docker compose up --build -d`.
4. Open `http://localhost:5000`. SQLite data persists in the `invoiceflow_data` volume.
5. Stop with `docker compose down` (volume remains); `docker compose down -v` deletes the database volume.

## Demo accounts
- Admin: `admin-demo` / `AdminDemo!2026`
- User: `user-demo` / `UserDemo!2026`

These are evaluation-only credentials created by `database/seed.py`. Change/remove them before production. Passwords are stored as Werkzeug password hashes, not plaintext.

## Database
`database/schema.sql` creates `users` and `invoices`, foreign keys, role constraints and owner index. `database/seed.py` creates demo accounts. Back up `database/invoiceflow.sqlite3` or the Docker volume before upgrades.

## API
- `POST /api/login` — validates credentials and starts an HTTP session.
- `POST /api/logout` — authenticated session logout.
- `GET /api/me` — current session identity.
- `GET /api/invoices` — authenticated, owner-scoped list.
- `POST /api/invoices` — authenticated create.
- `PUT /api/invoices/<id>` — authenticated owner-scoped update.
- `DELETE /api/invoices/<id>` — authenticated owner-scoped delete.
- `GET /api/admin/users` — admin-only user listing.

All invoice mutation endpoints require a session and scope records to the current owner. Admin user listing is role-gated. For production, add CSRF protection, rate limiting, HTTPS, password rotation and a managed secret store before exposing the API publicly.

## Branding
Edit the product name, metadata and marketing copy in `index.html`; styles are in `assets/css/landing.css` and `assets/css/style.css`. Replace screenshots under `screenshots/` while retaining their referenced filenames.

## Existing browser-local invoice editor
The original invoice editor continues to store its own records in Local Storage for compatibility. Export JSON backups regularly. Clearing browser storage or changing browser profile/origin can remove access to those local records. API invoices are a separate SQLite-backed data set; the current editor does not automatically sync its Local Storage records to the API.
