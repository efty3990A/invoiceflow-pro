# InvoiceFlow Pro — Invoice Maker

InvoiceFlow Pro helps freelancers and small businesses create and manage professional invoices. It is a responsive web application built with HTML, CSS and Vanilla JavaScript, with a Flask API and SQLite database for authenticated demo accounts and server-side invoice records.

## Features
- Invoice creation, live preview, automatic calculations, themes and currency display
- Customer and business details, logo upload, print and PDF export
- Browser-local draft/history and JSON backup/restore
- Admin/User demo access, authenticated API, owner-scoped invoice records
- SQLite schema and seed utility; Docker and VPS deployment guides

## Technology
HTML5, CSS3, Vanilla JavaScript, Python 3.12, Flask 3.1.2, SQLite, Gunicorn and Docker.

## Quick start
1. Copy `.env.example` to `.env` and replace every placeholder.
2. Install `pip install -r requirements.lock`.
3. Export the `.env` variables to your shell/process.
4. Run `python database/seed.py`.
5. Run `gunicorn --bind 0.0.0.0:5000 backend.app:app`.
6. Open `http://localhost:5000`.

See `HowToSetup.md` for VPS and Docker installation, security settings, and demo configuration. Never publish `.env` or production secrets.

## Data boundary
The existing invoice editor retains Local Storage for its browser history and drafts. The Flask API maintains a separate SQLite-backed invoice dataset. Automatic synchronization between these stores is not currently included.

## License
See `LICENSE-NOTE.md` and `LICENSE-NOTICE.txt`.
