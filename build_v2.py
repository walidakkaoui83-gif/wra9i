#!/usr/bin/env python3
"""Genere index.html, catalog.js, d/<id>.html, sitemap.xml, robots.txt, about.html depuis catalog.json"""
import json, html, os
EMAIL = 'walidakkaoui83@gmail.com'
INSTA = 'https://www.instagram.com/vision_casa_/'
SITE_URL = 'https://wra9i-silk.vercel.app'   # changez-le quand vous aurez votre .ma
data = json.load(open('catalog.json', encoding='utf-8')); docs = data['docs']; cats = {c['k']: c for c in data['cats']}
HOW = {
 'proc':'الوكالة كتخلي شخص آخر يتصرف باسمك فـ أمور محددة. عمّر المعطيات، صادق على الإمضاء حسب نوع الوكالة، وسلّمها للوكيل.',
 'plainte':'الشكاية كتوجّه للجهة المختصة. حدّد الوقائع بوضوح، أرفق الوثائق اللي كتثبت كلامك، واحتفظ بنسخة مختومة.',
 'desist':'التنازل كيكون كتابي ومؤرخ وموقّع. صادق على الإمضاء، وإذا تعلق بعقار أو حق مهم استشر موثق أو عدل.',
 'contrat':'العقد كيلزم الطرفين. دقّق فـ البنود (الثمن، المدة، الالتزامات)، وقّعو بجوج نسخ وصادقو على الإمضاءات.',
 'engage':'الالتزام وثيقة كيتعهد فيها الشخص بأمر معين. كتب المعطيات بدقة، وقّع، وصادق على الإمضاء إلا كان مطلوب.',
 'decl':'التصريح أو الشهادة كيقدّم للإدارة لإثبات واقعة. كتب المعلومات الصحيحة فقط، وقّع، وصادق على الإمضاء إلا كان مطلوب.',
 'autor':'الموافقة أو الترخيص كيتقدم للجهة المعنية. حدد الموضوع والتاريخ، ووقّع، وصادق على الإمضاء إلا كان مطلوب.',
 'demande':'الطلب كيوجّه للإدارة أو الهيئة المعنية. ذكر الموضوع والسبب، أرفق الوثائق المطلوبة، وخذ وصل الإيداع.',
 'assoc':'هاد النموذج كيخص تسيير الجمعية أو التعاونية. عدّلو حسب القانون الأساسي ديالكم، وقدّمو للجهة المعنية.',
 'cnss':'نموذج أو استمارة رسمية. عمّرها بالمعطيات الصحيحة وقدّمها للمصلحة المعنية مع الوثائق المطلوبة.',
 'cv':'عدّل المعلومات بتجربتك ودبلوماتك، وخلي السيرة الذاتية قصيرة وواضحة (صفحة أو صفحتين).',
 'guide':'هاد الوثيقة دليل أو مسطرة إدارية: قراءتها كتعاونك تعرف الوثائق والخطوات قبل ما تمشي للإدارة.',
 'autres':'نموذج للاستئناس، عدّلو حسب وضعيتك.'}
EM = {'cv':'📄','proc':'🖊️','plainte':'⚖️','desist':'↩️','contrat':'🤝','engage':'✍️','decl':'📋','autor':'✅','demande':'📩','assoc':'🤲','cnss':'🏦','guide':'🪪','autres':'📁'}
e = html.escape
HEAD = '<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><link rel="icon" href="%sfavicon.png"><link rel="stylesheet" href="%swra.css">'
def top(p): return f'<header class="top"><div class="wrap"><a class="brand" href="{p}index.html"><img src="{p}logo.png" alt="">وراقي · Wra9i</a><nav class="nav"><a href="{p}index.html#cats">الأصناف</a><a href="{p}about.html">من نحن</a></nav></div></header>'
def foot(p): return f'<footer>النماذج للاسترشاد فقط ولا تغني عن الاستشارة القانونية. · Modèles indicatifs, à vérifier auprès de l\'administration.<br><a href="{p}about.html">من نحن · À propos</a><a href="mailto:{EMAIL}">{EMAIL}</a><a href="{INSTA}" target="_blank" rel="noopener">Instagram</a></footer>'
open('catalog.js','w',encoding='utf-8').write('window.DATA = '+json.dumps(data, ensure_ascii=False)+';')
open('index.html','w',encoding='utf-8').write(f'''<!DOCTYPE html><html lang="ar" dir="rtl"><head>{HEAD%('','')}<title>وراقي · Wra9i: نماذج الوثائق الإدارية المغربية مجانا</title>
<meta name="description" content="وكالات، شكايات، عقود، طلبات، تصاريح، CV: حمّل نماذج الوثائق الإدارية المغربية بالعربية والفرنسية مجانا."></head><body>{top('')}
<div class="hero"><h1>وثيقتك فـ ثانية 📄</h1><p>نماذج الوثائق الإدارية المغربية · Modèles de documents administratifs</p>
<div class="search"><input id="q" type="search" placeholder="قلّب: وكالة، شكاية، عقد كراء، attestation…" autocomplete="off"></div></div>
<div class="stats" id="stats"></div><main class="wrap"><nav class="chips" id="chips"></nav><div id="res"></div><div id="main"><div id="cats"></div></div></main>
{foot('')}<script src="catalog.js"></script><script src="wra9i.js"></script></body></html>''')
by = {}
for d in docs: by.setdefault(d['c'], []).append(d)
urls = [SITE_URL+'/', SITE_URL+'/about.html']
for d in docs:
    c = cats[d['c']]; t = e(d['t']); size = f"{d['s']/1e6:.1f} MB" if d['s']>1e6 else f"{round(d['s']/1e3)} KB"
    rel = [x for x in by[d['c']] if x['id']!=d['id']][:6]
    rl = ''.join(f'<a dir="auto" href="{x["id"]}.html">{e(x["t"])}</a>' for x in rel)
    page = f'''<!DOCTYPE html><html lang="ar" dir="rtl"><head>{HEAD%('../','../')}<title>{t} — نموذج للتحميل | وراقي</title>
<meta name="description" content="حمّل نموذج {t} جاهز بصيغة {d['e'].upper()} مجانا. وثائق إدارية مغربية على وراقي."><link rel="canonical" href="{SITE_URL}/d/{d['id']}.html"></head><body>{top('../')}
<main class="wrap"><article class="doc"><div class="crumb"><a href="../index.html">الرئيسية</a> › <a href="../index.html#c-{d['c']}">{c['ar']}</a></div><h1 dir="auto">{t}</h1>
<div class="m"><span class="tag">{d['e']}</span><span>{size}</span><span>{EM.get(d['c'],'')} {c['ar']}</span></div>
<div class="a"><a class="btn p" href="../docs/{d['f']}" download="{t}.{d['e']}">⬇ تحميل · Télécharger</a><a class="btn w" id="wa" href="#">واتساب · WhatsApp</a><button class="btn" id="cp">نسخ الرابط</button></div>
<div class="how"><h2>كيفاش تستعمل هاد الوثيقة؟</h2><p>{HOW.get(d['c'],'')}</p></div><p class="note">النموذج للاسترشاد فقط. الشروط والمساطر ممكن تتغير: تأكد من الجهة المعنية قبل الإيداع.</p>
<h3 class="rel">وثائق مشابهة</h3><div class="rel-l">{rl}</div></article></main>{foot('../')}
<script>var u=location.href,t=document.title;document.getElementById('wa').href='https://wa.me/?text='+encodeURIComponent(t+' '+u);
document.getElementById('cp').onclick=function(){{navigator.clipboard&&navigator.clipboard.writeText(u);this.textContent='تم النسخ ✓'}}</script></body></html>'''
    open(f"d/{d['id']}.html",'w',encoding='utf-8').write(page); urls.append(f"{SITE_URL}/d/{d['id']}.html")
open('about.html','w',encoding='utf-8').write(f'''<!DOCTYPE html><html lang="ar" dir="rtl"><head>{HEAD%('','')}<title>من نحن | وراقي</title></head><body>{top('')}<main class="wrap"><article class="doc"><h1>من نحن · À propos</h1>
<p>وراقي موقع كيجمع نماذج الوثائق الإدارية المغربية باش تلقاها وتحمّلها بسهولة، بالعربية والفرنسية.</p>
<p class="note">النماذج المنشورة للاسترشاد فقط وما كتعوضش الاستشارة القانونية أو الإدارية. إلا لاحظتي خطأ أو بغيتي تطلب وثيقة، تواصل معنا:</p><p><a class="btn p" href="mailto:{EMAIL}">📧 {EMAIL}</a></p><p><a class="btn" href="{INSTA}" target="_blank" rel="noopener">📸 Instagram</a></p></article></main>{foot('')}</body></html>''')
open('sitemap.xml','w').write('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>{u}</loc></url>' for u in urls)+'</urlset>')
open('robots.txt','w').write(f'User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n')
print(len(docs),'pages')
