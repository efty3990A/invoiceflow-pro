# AI Developer Guide

- Frontend: `index.html`, `workspace.html`, `login.html`, `assets/css/`, `assets/js/`.
- Backend: `backend/app.py` (Flask routes, sessions, CSRF, role and owner checks).
- Database: `database/schema.sql`, `database/seed.py`; SQLite path configured by `DATABASE_PATH`.
- Tests: `python -m unittest discover -s tests -v`; JavaScript tests use Node's built-in test runner where available.
- Install: `pip install -r requirements.lock`; configure environment from `.env.example`.
- Never hard-code credentials or weaken authentication. All SQL must remain parameterized. Every mutating API route must use `authenticated(mutation=True)` and enforce ownership/role constraints.
- Keep frontend browser Local Storage and API SQLite persistence clearly distinguished unless implementing and testing a deliberate synchronization layer.
