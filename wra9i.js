// Remplissez pour afficher le bouton "Demander ce document" (ex: whatsapp:'2126XXXXXXXX')
const CONTACT = { whatsapp: '', email: 'walidakkaoui83@gmail.com' };
const D = window.DATA, $ = s => document.querySelector(s);
const EM = {cv:'📄',proc:'🖊️',plainte:'⚖️',desist:'↩️',contrat:'🤝',engage:'✍️',decl:'📋',autor:'✅',demande:'📩',assoc:'🤲',cnss:'🏦',guide:'🪪',autres:'📁'};
const norm = s => s.toLowerCase().replace(/[\u064B-\u0652\u0640]/g,'').replace(/[أإآ]/g,'ا').replace(/ى/g,'ي').replace(/ة/g,'ه').normalize('NFD').replace(/[\u0300-\u036f]/g,'');
const esc = s => s.replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const kb = n => n > 1e6 ? (n/1e6).toFixed(1)+' MB' : Math.round(n/1e3)+' KB';
D.docs.forEach(d => d.n = norm(d.t));
const card = d => `<article class="card"><a class="t" dir="auto" href="d/${d.id}.html">${esc(d.t)}</a><div class="m"><span class="tag">${d.e}</span><span>${kb(d.s)}</span></div><div class="a"><a class="btn p" href="docs/${d.f}" download="${esc(d.t)}.${d.e}">تحميل · Télécharger</a><a class="btn" href="d/${d.id}.html">تفاصيل</a></div></article>`;
const cats = D.cats.filter(c => c.n);
$('#stats').innerHTML = [[D.docs.length,'نموذج · modèles'],[cats.length,'صنف · catégories'],['AR · FR','عربية وفرنسية'],['0 DH','مجاني · gratuit']].map(([a,b]) => `<div class="stat"><b>${a}</b><span>${b}</span></div>`).join('');
$('#chips').innerHTML = cats.map(c => `<a href="#c-${c.k}">${EM[c.k]||'📁'} ${c.ar}</a>`).join('');
$('#cats').innerHTML = cats.map(c => {
  const l = D.docs.filter(d => d.c === c.k);
  return `<section class="cat" id="c-${c.k}"><div class="sh"><h2>${EM[c.k]||'📁'} ${c.ar}<small>${c.fr} · ${c.n}</small></h2>${l.length>8?`<button data-k="${c.k}">عرض الكل ←</button>`:''}</div><div class="grid">${l.slice(0,8).map(card).join('')}</div></section>`;
}).join('');
$('#cats').addEventListener('click', e => {
  const b = e.target.closest('button[data-k]'); if (!b) return;
  const g = b.closest('section').querySelector('.grid');
  g.innerHTML = D.docs.filter(d => d.c === b.dataset.k).map(card).join(''); b.remove();
});
const q = $('#q');
q.addEventListener('input', () => {
  const w = norm(q.value.trim()).split(/\s+/).filter(Boolean), res = $('#res');
  if (!w.length) { res.style.display = 'none'; $('#main').style.display = ''; return; }
  const r = D.docs.filter(d => w.every(x => d.n.includes(x)));
  $('#main').style.display = 'none'; res.style.display = 'block';
  let ask = '';
  if (CONTACT.whatsapp || CONTACT.email) {
    const m = encodeURIComponent('بغيت هاد الوثيقة: ' + q.value);
    ask = `<p><a class="btn w" href="${CONTACT.whatsapp ? 'https://wa.me/'+CONTACT.whatsapp+'?text='+m : 'mailto:'+CONTACT.email+'?subject='+m}">اطلب هذه الوثيقة · Demander ce document</a></p>`;
  }
  res.innerHTML = r.length ? `<p class="note">${r.length} وثيقة</p><div class="grid">${r.slice(0,90).map(card).join('')}</div>` : `<div class="empty">ما لقينا والو · Aucun résultat${ask}</div>`;
});
