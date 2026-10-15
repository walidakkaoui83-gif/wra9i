// DATA vient de assets/catalog.js (genere par build.py)
const DATA = window.DATA;
const norm = s => s.toLowerCase().replace(/[\u064B-\u0652\u0640]/g,'').replace(/[أإآ]/g,'ا').replace(/ى/g,'ي').replace(/ة/g,'ه').normalize('NFD').replace(/[\u0300-\u036f]/g,'');
DATA.docs.forEach(d => d.n = norm(d.t));
let cat = '', shown = 1000;
const $ = id => document.getElementById(id);
const kb = n => n > 1e6 ? (n/1e6).toFixed(1)+' MB' : Math.round(n/1e3)+' KB';

function chips(){
  const all = DATA.docs.length;
  $('chips').innerHTML = `<button class="chip ${cat===''?'on':''}" data-k="">Tous · الكل <small>${all}</small></button>` +
    DATA.cats.filter(c=>c.n).map(c=>`<button class="chip ${cat===c.k?'on':''}" data-k="${c.k}">${c.fr} · ${c.ar} <small>${c.n}</small></button>`).join('');
}
function render(reset){
  if (reset) shown = 1000;
  const q = norm($('q').value.trim()), f = $('fmt').value;
  const words = q.split(/\s+/).filter(Boolean);
  const res = DATA.docs.filter(d => (!cat||d.c===cat) && (!f||d.e===f) && words.every(w=>d.n.includes(w)));
  $('count').textContent = res.length + ' document' + (res.length>1?'s':'');
  $('empty').hidden = res.length>0;
  $('list').innerHTML = res.slice(0,shown).map(d => `
    <article class="card">
      <h3 dir="auto">${d.t.replace(/</g,'&lt;')}</h3>
      <div class="meta"><span class="tag">${d.e}</span><span>${kb(d.s)}</span></div>
      <div class="acts">
        <a class="btn p" href="docs/${d.f}" download="${d.t.replace(/"/g,'')}.${d.e}">Télécharger · تحميل</a>
        ${d.e==='pdf' ? `<a class="btn" href="docs/${d.f}" target="_blank" rel="noopener">Voir</a>` : ''}
      </div>
    </article>`).join('');
  $('more').hidden = res.length <= shown;
}
$('chips').addEventListener('click', e => { const b = e.target.closest('.chip'); if(!b) return; cat = b.dataset.k; chips(); render(true); });
$('q').addEventListener('input', () => render(true));
$('fmt').addEventListener('change', () => render(true));
$('more').addEventListener('click', () => { shown += 1000; render(false); });
chips(); render(true);
