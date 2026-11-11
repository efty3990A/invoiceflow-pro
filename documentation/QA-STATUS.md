# QA Status — InvoiceFlow Pro 1.0.5

## Package checks
- Landing page, demo access page and original invoice workspace are included.
- Existing invoice workspace JavaScript modules are retained.
- Marketplace cover and all gallery screenshots are 400 × 225 px.
- Square product image is 1080 × 1080 px.
- No contact details, website URLs or social media links appear in the generated marketplace images.
- Product documentation explicitly discloses browser-local storage and the absence of real authentication/roles.

## Checks still required by the seller
- Run `node tests/calc.test.js` and `node tests/calculations.test.js` in an environment with Node.js.
- Manually test landing → login → workspace in a current browser.
- Deploy to a public stable host and verify the URL signed out in a private window returns HTTP 200.
- Marketplace license compatibility and Vibe96-specific image upload fields must be checked by the seller.

A ZIP cannot change Netlify account-level deployment protection or create a permanent hosted URL. Public hosting must be configured in the hosting account.
