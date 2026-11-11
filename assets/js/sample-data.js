/* Clearly fictional demo data. Replace with the buyer's own information. */
(function (root) {
  'use strict';
  root.InvoiceFlowSampleData = {
    clients: [{ name: 'Northstar Studio', contact: 'accounts@example.test', address: '12 Demo Street, Sample City' }],
    invoice: {
      businessName: 'Your Creative Studio', businessContact: 'hello@example.test', businessAddress: 'Sample Business Address',
      invoiceNumber: 'DEMO-1001', currency: 'USD', issueDate: '2026-11-01', dueDate: '2026-11-15', template: 'classic',
      paymentStatus: 'Unpaid', clientName: 'Northstar Studio', clientContact: 'accounts@example.test',
      clientAddress: '12 Demo Street, Sample City', taxRate: '5', discount: '10', notes: 'Thank you for your business.',
      logoData: '', id: null,
      items: [
        { description: 'Website design package', quantity: 1, rate: 450 },
        { description: 'Content updates', quantity: 3, rate: 35 }
      ]
    }
  };
})(window);
