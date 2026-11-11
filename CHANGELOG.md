# Changelog

## 1.2.0 — Audit hardening
- Removed hard-coded demo credentials and weak fallback application secret.
- Added deployment-generated demo account passwords and one-click demo session endpoint.
- Added CSRF checks for state-changing API routes, login throttling, security headers and health endpoint.
- Enforced owner scoping and admin role checks; retained parameterized SQL.
- Pinned runtime dependency set and added lockfile, Gunicorn and reproducible Docker startup.
- Expanded API security tests and installation documentation.

## 1.1.1
- Added Vibe96 demo tracking script to public pages.

## 1.1.0
- Added Flask/SQLite demo API, role-aware demo access and marketplace setup documentation.

## 1.0.0
- Initial browser-based invoice maker.
