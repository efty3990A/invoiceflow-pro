/* JSON backup. Full schema validation occurs before storage mutation. */
(function(root){
  'use strict';function create(o){
    function exportBackup(){
      const data={
        app:'InvoiceFlow Pro',version:o.config.version||'1.0.4',exportedAt:new Date().toISOString(),invoices:o.store.getInvoices(),draft:o.renderer.collect()
      };const url=URL.createObjectURL(new Blob([JSON.stringify(data,null,2)],{
        type:'application/json'
      }));const a=document.createElement('a');a.href=url;a.download='invoiceflow-backup-'+new Date().toISOString().slice(0,10)+'.json';document.body.append(a);a.click();a.remove();URL.revokeObjectURL(url);o.message('Backup exported.')
    }
    function importBackup(file){
      if(!file)return;if(file.size>5*1024*1024){
        o.message('Backup must be 5 MB or smaller.',true);return
      }
      const r=new FileReader();r.onload=()=>{
        try{
          const d=o.validation.validateBackup(JSON.parse(String(r.result)));const merged=[...d.invoices,...o.store.getInvoices()];const unique=[...new Map(merged.map(x=>[x.id||JSON.stringify(x),x])).values()];if(unique.length>500)throw Error('Import would exceed 500 invoices.');o.store.setInvoices(unique);if(d.draft&&root.confirm('Backup imported. Load its draft now?'))o.renderer.apply(d.draft);o.message('Backup imported successfully.')
        }
        catch(e){
          o.message(e.message||'Could not import this backup.',true)
        }

      };r.onerror=()=>o.message('Could not read backup file.',true);r.readAsText(file)
    }
    return{
      exportBackup,importBackup
    }

  }
  root.InvoiceFlowBackup={
    create
  }

})(window);

