/* UI event bindings only. */
(function(root){
  'use strict';function bind(app){
    const $=app.$,on=(id,event,fn)=>$(id).addEventListener(event,fn);document.querySelectorAll('[data-close]').forEach(x=>x.addEventListener('click',()=>$(x.dataset.close).close()));['businessName','businessContact','businessAddress','invoiceNumber','currency','issueDate','dueDate','template','paymentStatus','clientName','clientContact','clientAddress','taxRate','discount','notes'].forEach(id=>on(id,'input',app.renderer.render));on('addItemBtn','click',()=>app.renderer.addLine('',1,0));on('saveDraftBtn','click',app.saveDraft);on('saveInvoiceBtn','click',app.saveInvoice);on('newBtn','click',app.resetInvoice);on('historyBtn','click',app.openHistory);on('sampleBtn','click',app.loadSample);on('pdfBtn','click',()=>{
      if(app.validatePrint()){
        app.renderer.render();root.print()
      }

    });on('backupBtn','click',app.backup.exportBackup);on('importFile','change',e=>{
      app.backup.importBackup(e.target.files?.[0]);e.target.value=''
    });on('clearHistoryBtn','click',app.clearHistory);on('logoFile','change',e=>app.handleLogo(e.target.files?.[0]));on('removeLogoBtn','click',()=>{
      app.state.logoData='';$('logoFile').value='';app.renderer.render();app.message('Logo removed.')
    });on('helpBtn','click',()=>$('helpDialog').showModal())
  }
  root.InvoiceFlowUI={
    bind
  }

})(window);

