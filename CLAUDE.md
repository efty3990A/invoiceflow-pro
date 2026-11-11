# AI coding guide

## Architecture
- `index.html`, `login.html`, `workspace.html`: public landing, role demo login, invoice UI.
- `assets/css/`: landing and workspace styles.
- `assets/js/`: browser-local invoice modules; preserve the Local Storage schema unless migration is explicitly requested.
- `backend/app.py`: Flask routes, session authentication, role checks, owner-scoped SQLite invoice API.
- `database/schema.sql`: schema; `database/seed.py`: evaluation users.

## Conventions
Use parameterized SQL, password hashes, session checks on mutations, and owner_id predicates on invoice reads/updates/deletes. Never commit `.env`, database files, credentials or generated artifacts. Do not claim the browser editor syncs with the API; they are currently separate stores.

## Run and test
Follow `HowToSetup.md`. Run `python -m unittest discover -s tests`; run the browser calculation checks with `node tests/calc.test.js` and `node tests/calculations.test.js`.
