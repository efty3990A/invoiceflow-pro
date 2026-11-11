/* Pure invoice arithmetic; exported for browser use and dependency-free tests. */
(function (root) {
  'use strict';
  const nonNegative = value => Math.max(0, Number(value) || 0);
  function calculateTotals(lines, taxRate, discount) {
    const safeLines = Array.isArray(lines) ? lines : [];
    const lineAmounts = safeLines.map(line => nonNegative(line.quantity) * nonNegative(line.rate));
    const subtotal = lineAmounts.reduce((sum, amount) => sum + amount, 0);
    const safeTaxRate = Math.min(100, nonNegative(taxRate));
    const tax = subtotal * safeTaxRate / 100;
    const safeDiscount = nonNegative(discount);
    const total = Math.max(0, subtotal + tax - safeDiscount);
    return { lineAmounts, subtotal, tax, discount: safeDiscount, total };
  }
  root.InvoiceFlowMath = { calculateTotals };
  if (typeof module !== 'undefined' && module.exports) module.exports = root.InvoiceFlowMath;
})(typeof window !== 'undefined' ? window : globalThis);
