/* Safe DOM renderer and form serializer. */
(function(root){
  'use strict';function create(o){
    const $=o.getElement,s=o.symbols,state=o.state;function money(n){
      const c=$('currency').value,d=c==='JPY'?0:2;return(s[c]||'')+Math.max(0,Number(n)||0).toLocaleString(undefined,{
        minimumFractionDigits:d,maximumFractionDigits:d
      })
    }
    function addLine(description='',quantity=1,rate=0){
      const row=document.createElement('div');row.className='item-row';const make=(cls,type,label,value)=>{
        const el=document.createElement('input');el.className=cls;el.type=type;el.setAttribute('aria-label',label);if(type==='number'){
          el.min='0';el.step='any'
        }
        el.value=String(value??'');return el
      };const desc=make('desc','text','Description',description);desc.maxLength=140;desc.placeholder='Product or service';const qty=make('qty','number','Quantity',Math.max(0,Number(quantity)||0));const rateEl=make('rate','number','Rate',Math.max(0,Number(rate)||0));const amount=make('line-amount','text','Amount','');amount.readOnly=true;const remove=document.createElement('button');remove.type='button';remove.className='remove-line';remove.setAttribute('aria-label','Remove item');remove.textContent='×';[desc,qty,rateEl].forEach(x=>x.addEventListener('input',render));remove.addEventListener('click',()=>{
        row.remove();if(!$('itemsList').children.length)addLine();render()
      });row.append(desc,qty,rateEl,amount,remove);$('itemsList').append(row);render()
    }
    function readLines(){
      return Array.from($('itemsList').children).map(r=>({
        description:r.querySelector('.desc').value.trim(),quantity:Math.max(0,Number(r.querySelector('.qty').value)||0),rate:Math.max(0,Number(r.querySelector('.rate').value)||0)
      }))
    }
    function calculate(){
      const lines=readLines(),t=root.InvoiceFlowMath.calculateTotals(lines,$('taxRate').value,$('discount').value);lines.forEach((x,i)=>{
        $('itemsList').children[i].querySelector('.line-amount').value=money(t.lineAmounts[i])
      });return{
        ...t,lines
      }

    }
    function render(){
      const t=calculate(),v={
        pBusiness:$('businessName').value||'Your Business Name',pBusinessAddress:$('businessAddress').value,pBusinessContact:$('businessContact').value,pInvoiceNo:$('invoiceNumber').value||'—',pIssueDate:$('issueDate').value||'—',pDueDate:$('dueDate').value||'—',pClient:$('clientName').value||'Client name',pClientAddress:$('clientAddress').value,pClientContact:$('clientContact').value,pPaymentStatus:$('paymentStatus').value,pStatus:$('paymentStatus').value.toUpperCase(),pNotes:$('notes').value||'Thank you for your business.',pFooterNo:$('invoiceNumber').value||''
      };Object.entries(v).forEach(([id,x])=>{
        $(id).textContent=x
      });const body=$('pItems');body.replaceChildren();t.lines.forEach(x=>{
        const tr=document.createElement('tr');[x.description||'—',String(x.quantity),money(x.rate),money(x.quantity*x.rate)].forEach(value=>{
          const td=document.createElement('td');td.textContent=value;tr.append(td)
        });body.append(tr)
      });$('pSubtotal').textContent=money(t.subtotal);$('pTax').textContent=money(t.tax);$('pDiscount').textContent='− '+money(t.discount);$('pTotal').textContent=money(t.total);$('paper').className='paper theme-'+$('template').value;const logo=$('previewLogo');if(state.logoData){
        logo.src=state.logoData;logo.style.display='block'
      }
      else{
        logo.removeAttribute('src');logo.style.display='none'
      }

    }
    function collect(){
      const d={

      };o.fieldIds.forEach(id=>d[id]=$(id).value);d.logoData=state.logoData;d.items=readLines();d.id=state.currentId;d.updatedAt=new Date().toISOString();return d
    }
    function apply(d){
      o.fieldIds.forEach(id=>{
        if(d[id]!==undefined)$(id).value=String(d[id])
      });state.logoData=typeof d.logoData==='string'?d.logoData:'';state.currentId=d.id||null;$('itemsList').replaceChildren();(Array.isArray(d.items)?d.items:[]).forEach(x=>addLine(x.description,x.quantity,x.rate));if(!$('itemsList').children.length)addLine('Product or service',1,0);render()
    }
    return{
      addLine,readLines,calculate,render,collect,apply,money
    }

  }
  root.InvoiceFlowRenderer={
    create
  }

})(window);

