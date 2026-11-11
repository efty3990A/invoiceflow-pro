# Test Plan — InvoiceFlow Pro 1.0.4

## Automated tests
Run from the project root:
```bash
node tests/calc.test.js
node tests/calculations.test.js
```
Expected: both scripts report that tests passed.

## Manual browser tests
1. **Clean start:** Use a fresh browser profile; confirm CSS and all controls load without console errors.
2. **First-run demo:** Confirm the fictional demo invoice is seeded into Local Storage and appears in the editor on first visit.
3. **Demo reset:** Delete `invoiceflow_pro_v1` and `invoiceflow_pro_draft_v1` from this origin's Local Storage, refresh, and confirm demo seeding repeats.
4. **Calculations:** Change quantities, rates, tax and discount; confirm line amounts and totals update and total never becomes negative.
5. **Validation:** Try saving without required business/client/invoice fields or a valid line item.
6. **History:** Save, open, load, delete and clear invoice history.
7. **Draft:** Save a draft, refresh, and confirm it reloads.
8. **Backup:** Export JSON, import it, and confirm invoices return. Also try malformed JSON and an invoice with an unsupported currency; import must reject it without changing storage.
9. **Logo:** Upload a PNG/JPG/WebP image up to 1 MB; confirm unsupported and oversized files are rejected.
10. **PDF:** Print to PDF and inspect page size, clipping, text, totals and logo.
11. **Responsive:** Test desktop and mobile-width layouts.
12. **Privacy:** Confirm no login, API key, external service or account is required.
13. **Public demo:** Test the published URL signed out in a private window; it must return HTTP 200, not 401 or a login redirect.

Record browser/version, date, pass/fail and notes before marking marketplace QA complete.
