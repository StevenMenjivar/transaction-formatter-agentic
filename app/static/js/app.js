const $ = id => document.getElementById(id);
let selectedFile = null, currentResult = null, statusChart = null, currencyChart = null;
const example = [
 {id:"tx_001",amount:"100.50",currency:"USD",timestamp:"2025-03-10 14:22:00",status:"completed",description:"Compra de prueba"},
 {transaction_id:204,total:10050,currency_code:"usd",created_at:"10/03/2025 14:22",state:"OK"},
 {ref:"A-77",amount:"€99,99",date:"2025-03-10T14:22:00Z",result:"success",concept:"Pago de servicio"},
 {id:"bad-04",status:"pending",currency:"EUR"}
];
function showNotice(message,type='info'){const n=$('notice');n.className=`notice ${type}`;n.textContent=message;n.classList.remove('hidden');}
function hideNotice(){$('notice').classList.add('hidden');}

// Navegación lateral: cada opción desplaza a su sección correspondiente.
document.querySelectorAll('.nav-item[data-target]').forEach(item=>{
 item.addEventListener('click',()=>{
  const target=$(item.dataset.target);
  if(!target)return;
  document.querySelectorAll('.nav-item[data-target]').forEach(nav=>{
   nav.classList.remove('active');
   nav.removeAttribute('aria-current');
  });
  item.classList.add('active');
  item.setAttribute('aria-current','page');
  target.scrollIntoView({behavior:'smooth',block:'start'});
 });
});
function setFile(file){if(!file)return;if(!file.name.toLowerCase().endsWith('.json')){showNotice('Selecciona un archivo con extensión .json.','error');return;}selectedFile=file;$('fileName').textContent=file.name;$('jsonInput').value='';hideNotice();}
$('chooseFile').onclick=()=>$('fileInput').click();
$('fileInput').onchange=e=>setFile(e.target.files[0]);
$('jsonInput').addEventListener('input',()=>{if($('jsonInput').value.trim()){selectedFile=null;$('fileName').textContent='';$('fileInput').value='';}});
$('dropzone').addEventListener('dragover',e=>{e.preventDefault();$('dropzone').classList.add('drag')});
$('dropzone').addEventListener('dragleave',()=>$('dropzone').classList.remove('drag'));
$('dropzone').addEventListener('drop',e=>{e.preventDefault();$('dropzone').classList.remove('drag');setFile(e.dataTransfer.files[0])});
$('loadExample').onclick=()=>{selectedFile=null;$('fileName').textContent='';$('jsonInput').value=JSON.stringify(example,null,2)};
$('clearBtn').onclick=()=>{selectedFile=null;$('fileInput').value='';$('fileName').textContent='';$('jsonInput').value='';$('results').classList.add('hidden');hideNotice();currentResult=null;};
function escapeHtml(v){return String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));}
function pretty(v){return JSON.stringify(v,(k,val)=>typeof val==='bigint'?val.toString():val,2)}
async function processData(){hideNotice();$('processBtn').disabled=true;$('processBtn').textContent='Procesando…';try{
 const form=new FormData();if(selectedFile)form.append('file',selectedFile);else{const text=$('jsonInput').value.trim();if(!text)throw new Error('Carga un archivo o pega un contenido JSON.');form.append('json_text',text);}form.append('timezone',$('timezone').value);form.append('date_order',$('dateOrder').value);
 const response=await fetch('/api/process',{method:'POST',body:form});const data=await response.json();if(!response.ok)throw new Error(data.detail||'No se pudo procesar el JSON.');currentResult=data;render(data);$('results').classList.remove('hidden');$('results').scrollIntoView({behavior:'smooth',block:'start'});showNotice('Procesamiento completado correctamente.','success');
 }catch(err){showNotice(err.message,'error');}finally{$('processBtn').disabled=false;$('processBtn').innerHTML='▶ &nbsp; Normalizar transacciones';}}
$('processBtn').onclick=processData;
function render(data){const m=data.metrics;$('mProcessed').textContent=m.processed;$('mValid').textContent=m.valid;$('mInvalid').textContent=m.invalid;$('mWarnings').textContent=m.withWarnings;$('mValidPct').textContent=`${m.validPercentage}% del total`;$('mInvalidPct').textContent=`${m.invalidPercentage}% del total`;$('mCurrency').textContent=m.unknownCurrency;$('mDates').textContent=m.unavailableDates;$('mStatuses').textContent=Object.keys(m.statusCounts).length;$('mCurrencies').textContent=Object.keys(m.currencyCounts).length;
 $('validCount').textContent=`${data.transactions.length} registros`;$('invalidCount').textContent=`${data.invalidTransactions.length} registros`;
 $('validRows').innerHTML=data.transactions.map(t=>`<tr><td>${t.id}</td><td>${escapeHtml(t.originalReference??'—')}</td><td>${escapeHtml(t.amount)}</td><td>${escapeHtml(t.currency??'—')}</td><td>${escapeHtml(t.transactionDate??'—')}</td><td><span class="status ${t.status}">${t.status}</span></td><td><button class="btn ghost detail-valid" data-id="${t.id}" style="padding:5px 8px">Ver</button></td></tr>`).join('')||'<tr><td colspan="7" class="empty">No hay transacciones válidas.</td></tr>';
 $('invalidRows').innerHTML=data.invalidTransactions.map((t,i)=>`<tr><td>${t.position}</td><td>${escapeHtml(t.sourcePath||'—')}</td><td>${escapeHtml((t.errors||[]).join('; '))}</td><td><button class="btn ghost detail-invalid" data-index="${i}" style="padding:5px 8px">Ver</button></td></tr>`).join('')||'<tr><td colspan="4" class="empty">No hay transacciones inválidas.</td></tr>';
 $('outputJson').textContent=pretty(data.transactions);
 fetch(`/api/export/${data.processingId}`).then(r=>r.text()).then(t=>{$('outputJson').textContent=t;}).catch(()=>{});
 document.querySelectorAll('.detail-valid').forEach(b=>b.onclick=()=>showValidDetail(Number(b.dataset.id)));
 document.querySelectorAll('.detail-invalid').forEach(b=>b.onclick=()=>showInvalidDetail(Number(b.dataset.index)));
 drawCharts(m.statusCounts,m.currencyCounts);
}
function drawCharts(statuses,currencies){if(statusChart)statusChart.destroy();if(currencyChart)currencyChart.destroy();if(!window.Chart)return;
 statusChart=new Chart($('statusChart'),{type:'doughnut',data:{labels:Object.keys(statuses),datasets:[{data:Object.values(statuses),backgroundColor:['#10b981','#ef4444','#f59e0b','#94a3b8'],borderWidth:0}]},options:{maintainAspectRatio:false,plugins:{legend:{position:'bottom'}}}});
 currencyChart=new Chart($('currencyChart'),{type:'bar',data:{labels:Object.keys(currencies),datasets:[{label:'Transacciones',data:Object.values(currencies),backgroundColor:'#6366f1',borderRadius:6}]},options:{maintainAspectRatio:false,plugins:{legend:{display:false}},scales:{y:{beginAtZero:true,ticks:{precision:0}}}}});}
function scrollToInspection(){
 const section=$('inspection-panel');
 if(section)section.scrollIntoView({behavior:'smooth',block:'start'});
}
function showValidDetail(id){const t=currentResult.transactions.find(x=>x.id===id);const d=currentResult.details.find(x=>x.id===id);if(!t||!d)return;$('inspection').className='detail-layout';$('inspection').innerHTML=`<div class="detail-card"><h3>JSON original</h3><pre>${escapeHtml(pretty(d.original))}</pre></div><div class="detail-card"><h3>JSON normalizado</h3><pre>${escapeHtml(pretty(t))}</pre></div><div class="detail-card"><h3>Propiedades originales y trazabilidad</h3><pre>${escapeHtml(pretty(d.trace))}</pre></div><div class="detail-card" style="grid-column:1/-1"><h3>Advertencias</h3>${d.warnings.length?d.warnings.map(w=>`<div class="warning-line">${escapeHtml(w.message)}</div>`).join(''):'<span class="muted">Sin advertencias.</span>'}</div>`;scrollToInspection();}
function showInvalidDetail(index){const t=currentResult.invalidTransactions[index];if(!t)return;$('inspection').className='detail-layout';$('inspection').innerHTML=`<div class="detail-card"><h3>JSON original · posición ${t.position}</h3><pre>${escapeHtml(pretty(t.original))}</pre></div><div class="detail-card"><h3>Errores</h3>${(t.errors||[]).map(e=>`<div class="warning-line" style="border-color:#ef4444;background:#fff1f2">${escapeHtml(e)}</div>`).join('')}</div><div class="detail-card" style="grid-column:1/-1"><h3>Campos detectados</h3><pre>${escapeHtml(pretty(t.trace||{}))}</pre></div>`;scrollToInspection();}
$('copyBtn').onclick=async()=>{if(!currentResult)return;try{const r=await fetch(`/api/export/${currentResult.processingId}`);const raw=await r.text();await navigator.clipboard.writeText(raw);showNotice('JSON normalizado copiado al portapapeles.','success')}catch{showNotice('No fue posible acceder al portapapeles del navegador.','error')}};
$('downloadBtn').onclick=async()=>{if(!currentResult)return;try{const r=await fetch(`/api/export/${currentResult.processingId}`);if(!r.ok)throw new Error('No se pudo generar el archivo.');const blob=await r.blob();const url=URL.createObjectURL(blob);const a=document.createElement('a');a.href=url;a.download='transacciones_normalizadas.json';a.click();URL.revokeObjectURL(url)}catch(e){showNotice(e.message,'error')}};
