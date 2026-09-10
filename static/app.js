const typeEl = document.getElementById("type");
const targetEl = document.getElementById("target");
const resultsEl = document.getElementById("results");
const messageEl = document.getElementById("message");

function setType(type){
  typeEl.value = type;
  targetEl.focus();
}

async function investigate(){
  const target = targetEl.value.trim();
  if(!target){
    messageEl.textContent = "Enter a target first.";
    return;
  }

  messageEl.textContent = "Running public-source checks...";
  resultsEl.innerHTML = `<div class="empty"><div class="crosshair">◌</div><h3>Investigating</h3><p>Collecting authorized public intelligence…</p></div>`;

  try{
    const response = await fetch("/api/investigate", {
      method:"POST",
      headers:{"Content-Type":"application/json"},
      body:JSON.stringify({target, type:typeEl.value})
    });
    const data = await response.json();
    if(!response.ok) throw new Error(data.error || "Investigation failed");

    renderResults(data);
    messageEl.textContent = "Investigation complete.";
  }catch(err){
    messageEl.textContent = err.message;
    resultsEl.innerHTML = `<div class="empty"><h3>Request failed</h3><p>${escapeHtml(err.message)}</p></div>`;
  }
}

function renderResults(data){
  const rows = (data.findings || []).map(f => `
    <div class="finding">
      <label>${escapeHtml(f.label)}</label>
      <value class="${f.status || "info"}">${f.url ? `<a href="${escapeAttr(f.url)}" target="_blank" rel="noopener">${escapeHtml(f.value)}</a>` : escapeHtml(f.value)}</value>
    </div>
  `).join("");

  resultsEl.innerHTML = `
    <div class="result-card">
      <div class="result-head">
        <h3>${escapeHtml(data.summary || "Investigation")}</h3>
        <code>${escapeHtml(data.type || "OSINT").toUpperCase()}</code>
      </div>
      <div class="findings">${rows}</div>
      <div class="notice">⚠ ${escapeHtml(data.notice || "")}</div>
    </div>`;
}

function escapeHtml(value){
  return String(value).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[c]));
}
function escapeAttr(value){ return escapeHtml(value); }

targetEl.addEventListener("keydown", e => {
  if(e.key === "Enter") investigate();
});
