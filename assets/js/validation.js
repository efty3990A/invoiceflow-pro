/* Strict import validation. */
(function(root){
  'use strict';const currencies=new Set(['BDT','USD','EUR','GBP','INR','CAD','AUD','JPY']),themes=new Set(['classic','minimal','emerald']),statuses=new Set(['Unpaid','Paid','Partially paid']);const fields=['businessName','businessContact','businessAddress','invoiceNumber','currency','issueDate','dueDate','template','paymentStatus','clientName','clientContact','clientAddress','taxRate','discount','notes'];function text(v,n=600){
    return typeof v==='string'&&v.length<=n
  }
  function validInvoice(x){
    if(!x||typeof x!=='object'||Array.isArray(x)||!fields.every(k=>text(x[k]??'',k==='notes'?600:300)))return false;if(!currencies.has(x.currency)||!themes.has(x.template)||!statuses.has(x.paymentStatus))return false;if(!Array.isArray(x.items)||x.items.length>200||!x.items.every(i=>i&&typeof i==='object'&&text(i.description,140)&&Number.isFinite(Number(i.quantity))&&Number(i.quantity)>=0&&Number.isFinite(Number(i.rate))&&Number(i.rate)>=0))return false;if(x.logoData!==undefined&&(!text(x.logoData,1400000)||(x.logoData&&!/^data:image\/(png|jpeg|webp);base64,[a-z0-9+/=]+$/i.test(x.logoData))))return false;return true
  }
  function validateBackup(d){
    if(!d||typeof d!=='object'||Array.isArray(d)||d.app!=='InvoiceFlow Pro'||!Array.isArray(d.invoices)||d.invoices.length>500||!d.invoices.every(validInvoice))throw Error('Invalid InvoiceFlow backup or invoice data.');if(d.draft!=null&&!validInvoice(d.draft))throw Error('Backup draft contains invalid fields.');return d
  }
  const api={
    validInvoice,validateBackup,limits:{
      invoices:500
    }

  };root.InvoiceFlowValidation=api;if(typeof module!=='undefined'&&module.exports)module.exports=api
})(typeof window!=='undefined'?window:globalThis);

