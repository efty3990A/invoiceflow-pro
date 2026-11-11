/* Browser-only Local Storage adapter. */
(function(root){
  'use strict';const K={
    invoices:'invoiceflow_pro_v1',draft:'invoiceflow_pro_draft_v1'
  };function read(k,f){
    try{
      const v=root.localStorage.getItem(k);return v===null?f:JSON.parse(v)
    }
    catch(e){
      return f
    }

  }
  function write(k,v){
    try{
      root.localStorage.setItem(k,JSON.stringify(v))
    }
    catch(e){
      throw Error('Browser storage is unavailable or full. Export a backup and free space.')
    }

  }
  root.InvoiceFlowStorage={
    getInvoices(){
      const v=read(K.invoices,[]);return Array.isArray(v)?v.filter(x=>x&&typeof x==='object'&&!Array.isArray(x)):[]
    },setInvoices(v){
      if(!Array.isArray(v)||v.length>500)throw TypeError('Invoices must be an array of up to 500 records.');write(K.invoices,v)
    },getDraft(){
      const v=read(K.draft,null);return v&&typeof v==='object'&&!Array.isArray(v)?v:null
    },setDraft(v){
      if(!v||typeof v!=='object'||Array.isArray(v))throw TypeError('Draft must be an object.');write(K.draft,v)
    },clearInvoices(){
      write(K.invoices,[])
    }

  }

})(window);

