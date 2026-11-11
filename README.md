# InvoiceFlow Pro 1.1.0 — Invoice Maker

InvoiceFlow Pro is an invoice creation tool for freelancers, small businesses and independent service providers. The package combines the original responsive browser invoice editor with an optional Flask/SQLite session and role-based API.

## Technology
HTML5, CSS3, vanilla JavaScript, Python 3, Flask 3.1.1 and SQLite. Frontend invoice history/drafts remain browser Local Storage; the authenticated API stores separate owner-scoped invoice records in SQLite.

## Core features
- Invoice editor with live subtotal, tax and discount calculations.
- Customer and business details, line items, invoice history and draft saving.
- Three invoice themes, eight currency display options, optional logo and A4 print-to-PDF.
- JSON export/import backup with validation.
- Demo login buttons for Admin and User roles.
- Session-protected, owner-scoped invoice API and admin-only user listing.
- Docker and Python VPS/local setup paths.

## Quick start
See [HowToSetup.md](HowToSetup.md). In brief: install `requirements.txt`, copy `.env.example` to a private `.env`, seed the SQLite database with `python database/seed.py`, then run `python backend/app.py`.

## Demo credentials
Admin: `admin-demo` / `AdminDemo!2026`  
User: `user-demo` / `UserDemo!2026`

Evaluation credentials only. Replace them and the Flask secret before production deployment.

## Screenshots
- [Cover](screenshots/cover.png)
- [Invoice workspace](screenshots/invoice-workspace.png)
- [Invoice preview](screenshots/invoice-preview.png)
- [Square landing image](screenshots/landing-square.png)

## Tests
Run `python -m unittest discover -s tests` for backend/API tests and `node tests/calc.test.js` plus `node tests/calculations.test.js` for the existing calculation checks (Node.js is needed only for those JS tests).

## Important limitations
The editor's own saved invoices and drafts still use browser Local Storage and do not sync to SQLite or across devices. The Flask API is a separate authenticated data interface. Payment collection, email delivery, cloud synchronization and third-party accounting integrations are not included. Currency choices change display symbols only; they do not convert exchange rates.

## Security notes
No live credentials or `.env` file is included. `.env.example` contains placeholders. Change demo passwords and `SECRET_KEY`, use HTTPS, and add production CSRF/rate-limit controls before public commercial deployment.

## License
See [LICENSE-NOTE.md](LICENSE-NOTE.md); verify redistribution rights for all included assets before sale.
