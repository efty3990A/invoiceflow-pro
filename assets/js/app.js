/* Application workflows and state; UI bindings and rendering are separate modules. */
(function(root){
  'use strict';const $=id=>document.getElementById(id),fieldIds=['businessName','businessContact','businessAddress','invoiceNumber','currency','issueDate','dueDate','template','paymentStatus','clientName','clientContact','clientAddress','taxRate','discount','notes'],config=root.INVOICEFLOW_CONFIG||{

  },symbols=Object.assign({
    BDT:'৳',USD:'$',EUR:'€',GBP:'£',INR:'₹',CAD:'$',AUD:'$',JPY:'¥'
  },config.currencySymbols||{

  }),state={
    logoData:'',currentId:null
  },store=root.InvoiceFlowStorage,sample=root.InvoiceFlowSampleData,validation=root.InvoiceFlowValidation;const renderer=root.InvoiceFlowRenderer.create({
    getElement:$,symbols,state,fieldIds
  });function message(t,e=false){
    $('status').textContent=t;$('status').style.color=e?'#c84e58':'#16986b'
  }
  const backup=root.InvoiceFlowBackup.create({
    config,store,renderer,validation,message
  });function invoices(){
    return store.getInvoices()
  }
  function setInvoices(v){
    store.setInvoices(v)
  }
  function validCurrent(){
    const d=renderer.collect();if(!d.businessName.trim()||!d.invoiceNumber.trim()||!d.clientName.trim()){
      message('Complete business name, invoice number and client name first.',true);return false
    }
    if(!d.items.some(x=>x.description&&x.quantity>0)){
      message('Add at least one valid line item.',true);return false
    }
    return true
  }
  function saveDraft(){
    try{
      const d=renderer.collect();if(!validation.validInvoice(d))throw Error('Please check invoice fields before saving.');store.setDraft(d);message('Draft saved in this browser.')
    }
    catch(e){
      message(e.message,true)
    }

  }
  function saveInvoice(){
    if(!validCurrent())return;try{
      const d=renderer.collect();if(!d.id)d.id=root.crypto?.randomUUID?root.crypto.randomUUID():'inv-'+Date.now();state.currentId=d.id;const list=invoices(),i=list.findIndex(x=>x.id===d.id),record={
        ...d,savedAt:new Date().toISOString()
      };if(i>=0)list[i]=record;else list.unshift(record);setInvoices(list);store.setDraft(d);message('Invoice saved to local history.')
    }
    catch(e){
      message(e.message,true)
    }

  }
  function openHistory(){
    const host=$('historyList');host.replaceChildren();const list=invoices();if(!list.length){
      const empty=document.createElement('div');empty.className='empty-history';empty.textContent='No saved invoices yet. Save an invoice to see it here.';host.append(empty)
    }
    list.forEach(x=>{
      const row=document.createElement('div'),details=document.createElement('div'),title=document.createElement('strong'),meta=document.createElement('small'),actions=document.createElement('div'),open=document.createElement('button'),del=document.createElement('button');row.className='history-item';title.textContent=x.invoiceNumber||'Untitled invoice';meta.textContent=(x.clientName||'No client')+' · '+(x.savedAt?new Date(x.savedAt).toLocaleDateString():'');details.append(title,meta);actions.className='history-actions';open.type=del.type='button';open.className=del.className='btn btn-light';open.textContent='Open';del.textContent='Delete';open.addEventListener('click',()=>{
        renderer.apply(x);$('historyDialog').close();message('Invoice loaded.')
      });del.addEventListener('click',()=>{
        if(root.confirm('Delete this saved invoice?')){
          setInvoices(invoices().filter(y=>y.id!==x.id));openHistory()
        }

      });actions.append(open,del);row.append(details,actions);host.append(row)
    });$('historyDialog').showModal()
  }
  function resetInvoice(){
    if(!root.confirm('Start a new invoice? Unsaved changes will be lost.'))return;renderer.apply({
      businessName:'Your Business Name',businessContact:'',businessAddress:'',invoiceNumber:'INV-'+Date.now().toString().slice(-6),currency:'BDT',issueDate:new Date().toISOString().slice(0,10),dueDate:'',template:'classic',paymentStatus:'Unpaid',clientName:'',clientContact:'',clientAddress:'',taxRate:'0',discount:'0',notes:'',logoData:'',id:null,items:[{
        description:'Product or service',quantity:1,rate:0
      }]
    });message('New invoice ready.')
  }
  function loadSample(){
    if(root.confirm('Load the example invoice? It will replace the current unsaved form.')){
      renderer.apply(sample.invoice);message('Example invoice loaded.')
    }

  }
  function handleLogo(file){
    if(!file)return;if(!/^image\/(png|jpeg|webp)$/.test(file.type)){
      message('Choose a PNG, JPG or WebP image.',true);return
    }
    if(file.size>1024*1024){
      message('Logo must be 1 MB or smaller.',true);return
    }
    const r=new FileReader();r.onload=()=>{
      state.logoData=String(r.result||'');renderer.render();message('Logo added to this invoice.')
    };r.onerror=()=>message('Could not read logo.',true);r.readAsDataURL(file)
  }
  function clearHistory(){
    if(root.confirm('Delete all saved invoice history from this browser?')){
      setInvoices([]);openHistory();message('Invoice history cleared.')
    }

  }
  function seed(){
    if(invoices().length||store.getDraft())return;const demo={
      ...sample.invoice,id:'demo-invoice-1001',savedAt:new Date().toISOString()
    };setInvoices([demo]);store.setDraft(sample.invoice)
  }
  function start(){
    seed();const d=store.getDraft();if(d&&validation.validInvoice(d))renderer.apply(d);else renderer.apply(sample.invoice)
  }
  root.InvoiceFlowApp={
    $,state,renderer,backup,message,saveDraft,saveInvoice,openHistory,resetInvoice,loadSample,validatePrint:validCurrent,handleLogo,clearHistory,start
  }

})(window);

