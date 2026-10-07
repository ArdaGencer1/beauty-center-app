/* ---------- CİLT ATLASI: alt sayfa motoru ----------
   Yol: #cilt/<slug> (tabanın genel görünüm/parametre yolu).  Alt sayfalar cilt görünümünün içinde açılır; böylece S.view "cilt" kalır ve davetiye,
   alt çubuk, [W-] kodu ve sayaç olduğu gibi çalışır.  Her buton data-track-label="at-<kod>-<yer>" taşır. */
var CA={cur:null,film:null,obs:[]};
var CA_PKG={paris:1,akne:1,hollywood:1,leke:1,yenileme:1,derma:1};
var CA_ROMAN=["I","II","III","IV","V","VI"];
PLANS.cilt.opts=PLANS.cilt.opts.concat([
 {id:"ton",n:"Ton eşitleme",p:null,d:null,s:"Alana göre 4.500 / 5.500 / 6.500 TL"},
 {id:"saten",n:"Saten yüz germe",p:4500,d:60},
 {id:"dudak",n:"Dudak bakımı",p:null,d:null,s:"3 seviye: 1.000 / 1.500 / 2.000 TL"},
 {id:"sirt",n:"Sırt bakımı",p:null,d:null,s:"Bölgeye göre 3.500 TL'den"},
 {id:"koltuk",n:"Koltuk altı bakımı",p:4500,d:30}]);
var CA_OPT2SLUG={};
Object.keys(CP).forEach(function(s){ if(CP[s].opt) CA_OPT2SLUG[CP[s].opt]=s; });
NAV.forEach(function(g){ if(g[0]==="Cilt") g[1].forEach(function(it){ if(!it[2] && CP[it[0]]) it[2]="cilt/"+it[0]; }); });

function caOpt(id){ return PLANS.cilt.opts.filter(function(x){ return x.id===id; })[0]||null; }
function caRoute(){ return CA.cur?"cilt/"+CA.cur:"cilt"; }
function caL(code,place){ return ' data-track-label="at-'+code+'-'+place+'"'; }
function caPoster(k){ var m=CM[k]; if(!m) return "m/monogram.png"; if(m.img) return "m/ig/"+m.img+"-480.webp"; return m.v?"m/ig/"+m.v+"-poster.webp":"m/ig/"+m.pair+"-sonra-"+m.s+".webp"; }
function caPriceTxt(p){ var o=p.opt?caOpt(p.opt):null; if(!o) return "Rehber · size uygun bakım";
  if(p.from) return p.from.toLocaleString("tr-TR")+" TL'den";
  return fmtTL(o.p)+(o.d?" · "+o.d+" dk":""); }
function caMedia(k,lazy){ var m=CM[k]; if(!m) return "";
  if(m.img) return '<img src="m/ig/'+m.img+'-720.webp" srcset="m/ig/'+m.img+'-480.webp 480w, m/ig/'+m.img+'-720.webp 720w" sizes="(min-width:960px) 50vw, 100vw" alt="'+m.alt+'" width="720" height="900" decoding="async"'+(lazy?' loading="lazy"':'')+'>';
  if(m.v) return '<video class="'+(lazy?"ca-lv":"auto-vid")+'" muted playsinline loop preload="none" poster="m/ig/'+m.v+'-poster.webp" data-src="m/ig/'+m.v+'.mp4" aria-label="'+m.alt+'"></video>';
  var b="m/ig/"+m.pair+"-", rows=m.s!==480;
  return '<div class="ca-pair'+(rows?" rows":"")+'"><figure><img src="'+b+"once-"+m.s+'.webp" alt="Önce: '+m.alt+'" loading="lazy"><span class="cmp-tag">Önce</span></figure><figure><img src="'+b+"sonra-"+m.s+'.webp" alt="Sonra: '+m.alt+'" loading="lazy"><span class="cmp-tag">Sonra</span></figure></div>'; }
function caWaMsg(p){ return p.kind==="H"?"Merhaba, sitede "+p.t.toLocaleLowerCase("tr-TR")+" sayfasındayım. Uygun bir saat var mı? "+visitCode()
  :"Merhaba, "+p.t.toLocaleLowerCase("tr-TR")+" için hangi bakımın bana uygun olduğunu sormak istiyorum. "+visitCode(); }
function caMainOpt(p){ if(p.opt) return p.opt; var r=(p.route||[]).filter(function(s){ return CP[s]&&CP[s].opt; })[0]; return r?CP[r].opt:"klasik"; }
var CA_LIPS='<svg viewBox="0 0 200 110" aria-hidden="true"><path d="M8 52C40 40 62 14 84 18c8 1 12 8 16 8s8-7 16-8c22-4 44 22 76 34-30 6-48 48-92 50C52 100 38 58 8 52z" fill="#C46E66" opacity=".85"/><path d="M8 52c34 4 60 8 92 8s58-4 92-8" fill="none" stroke="#5a2e2c" stroke-width="3"/><path d="M60 30c10-4 22-2 30 4M140 30c-10-4-22-2-30 4" stroke="#F4E6BE" stroke-width="2" opacity=".6" fill="none"/></svg>';

/* ---------- parçalar ---------- */
function caHero(p){ var tag='<span class="ca-film-tag"><i></i>Salonumuzda çekildi</span>', media;
  if(p.hero==="type:dudak") media='<div class="ca-type">'+CA_LIPS+'<b>Dudak bakımı</b></div>';
  else if(/^type:/.test(p.hero)) media='<div class="ca-type"><img src="m/monogram.png" alt="" width="120" height="120" style="position:static;width:120px;height:120px;opacity:.55"><b>'+p.hero.slice(5)+'</b></div>';
  else media=caMedia(p.hero,false)+tag;
  var o=p.opt?caOpt(p.opt):null, wa=waHref(caWaMsg(p));
  return '<div class="hero ca-hero"><div class="hero-split"><div class="hero-media lit">'+media+'</div>'+
   '<div class="hero-copy"><button class="ca-crumb" data-go="cilt"'+caL(p.code,"geri")+'><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M15 6l-6 6 6 6"/></svg>Cilt Atlası</button>'+
   '<span class="eyebrow">Konutkent · Çankaya</span><h1>'+p.h1[0]+' <em>'+p.h1[1]+'</em></h1><p class="lede">'+p.lede+'</p>'+
   '<div class="chips"><span class="chip chip-in"><span class="star">★</span> 4,6 · 263 yorum</span><span class="chip chip-in price">'+caPriceTxt(p)+'</span>'+(o&&CA_PKG[o.id]?'<span class="chip chip-in">5 seans paketi</span>':'')+'</div>'+
   '<div class="ca-ctas">'+(p.kind==="H"?'<button class="btn-gold shine" data-plan="cilt" data-opt="'+p.opt+'"'+caL(p.code,"hero-saat")+'><span class="lbl">Saatimi seç</span></button>':'<button class="btn-gold shine" data-plan="cilt" data-opt="'+caMainOpt(p)+'"'+caL(p.code,"hero-saat")+'><span class="lbl">Bakımımı seçip saat al</span></button>')+
   '<a class="btn-line" href="'+wa+'" target="_blank" rel="noopener"'+caL(p.code,"hero-wa")+'>WhatsApp</a></div>'+
   '<p class="hero-note">'+p.heroNote+'</p></div></div></div>'; }

function caStoryHTML(acts,head,code){ var keys=[]; acts.forEach(function(a){ if(keys.indexOf(a.m)<0) keys.push(a.m); });
  return '<div class="sec gutter ca-story"><div class="sec-head"><span class="eyebrow">'+head[0]+'</span><h2>'+head[1]+'</h2></div>'+
   '<div class="ca-scrolly" data-ca-story><div class="ca-stage">'+keys.map(function(k){ return '<div class="ca-layer" data-k="'+k+'">'+caMedia(k,true)+'</div>'; }).join("")+
   '<span class="ca-count">'+CA_ROMAN[0]+' / '+CA_ROMAN[acts.length-1]+'</span><span class="ca-cap"></span></div>'+
   '<ol class="ca-acts">'+acts.map(function(a,i){ return '<li class="ca-act" data-i="'+i+'" data-k="'+a.m+'"><div class="ca-card"><span class="ca-num">'+CA_ROMAN[i]+'</span>'+(a.w?'<span class="ca-when">'+a.w+' · '+a.k+'</span>':'<span class="ca-when">'+a.k+'</span>')+'<h3>'+a.h+'</h3><p>'+a.p+'</p></div></li>'; }).join("")+'</ol></div></div>'; }

function caFilmHTML(f){ return '<div class="sec gutter" style="padding-bottom:0"><div class="sec-head"><span class="eyebrow">'+f.k+'</span><h2>'+f.h+'</h2><p>'+f.p+'</p></div></div>'+
  '<section class="ca-film" id="caFilm" data-n="48" data-cols="8" data-fw="360" data-fh="640"><div class="ca-film-pin"><div class="ca-film-box"><img src="m/ig/cilt-saten-poster.webp" alt="Saten yüz germe uygulaması, salonumuzda çekildi"><canvas width="360" height="640"></canvas><i class="ca-film-bar"></i>'+
  '<div class="ca-film-cap"><b>Yanaktan şakağa</b><span>Başlık yavaşça gezdirilir.</span></div></div></div></section>'; }
var CA_FILM_CAPS=[[0,"Yanaktan şakağa","Başlık yavaşça gezdirilir."],[.42,"Alın","Küçük, düzenli hareketlerle."],[.62,"Göz çevresi","En ince deriye en nazik dokunuş."]];

var CA_ZONES={alin:["Alın","Alında en sık siyah nokta, matlık ve ince çizgiler görürüz.",["klasik-cilt-bakimi","cilt-temizligi","saten-yuz-germe"]],
 goz:["Göz çevresi","Yüzün en ince derisi: kaz ayağı ve yorgun görünüm.",["goz-cevresi-bakimi","saten-yuz-germe"]],
 burun:["Burun ve T bölgesi","Gözenek ve siyah noktanın en yoğun olduğu bölge.",["cilt-temizligi","klasik-cilt-bakimi"]],
 yanak:["Yanaklar","Kızarıklık, sivilce ve ton farkı en çok burada görünür.",["akne-bakimi","ton-esitleme","hassas-cilt"]],
 dudak:["Dudaklar","Kuruluk ve pürüz.",["dudak-bakimi"]],
 cene:["Çene hattı","Sivilce ve sıkılık kaybı sık görülür.",["akne-bakimi","cilt-inceltme"]]};
function caMapHTML(code){ var z=function(id,shape){ return '<g class="z" data-z="'+id+'" tabindex="0" role="button" aria-pressed="false" aria-label="'+CA_ZONES[id][0]+'"'+caL(code,"harita")+'>'+shape+'</g>'; };
  return '<div class="sec gutter"><div class="sec-head"><span class="eyebrow">Yüz haritası</span><h2>Bir bölgeye <em>dokunun</em>.</h2><p>Hangi bölgede ne sık görülür, hangi bakım yakındır? Bu bir yönlendirmedir; analizin yerini tutmaz.</p></div>'+
   '<div class="ca-map"><div class="ca-face"><svg viewBox="0 0 200 270" role="group" aria-label="Yüz haritası"><ellipse class="ol" cx="100" cy="135" rx="80" ry="112"/><path class="ol" d="M52 92q18-10 36 0M112 92q18-10 36 0"/>'+
   z("alin",'<ellipse cx="100" cy="58" rx="54" ry="24"/><text x="100" y="61" text-anchor="middle">Alın</text>')+
   z("goz",'<ellipse cx="68" cy="110" rx="22" ry="11"/><ellipse cx="132" cy="110" rx="22" ry="11"/>')+
   z("burun",'<ellipse cx="100" cy="138" rx="13" ry="26"/>')+
   z("yanak",'<ellipse cx="58" cy="155" rx="22" ry="25"/><ellipse cx="142" cy="155" rx="22" ry="25"/>')+
   z("dudak",'<ellipse cx="100" cy="193" rx="24" ry="10"/>')+
   z("cene",'<ellipse cx="100" cy="226" rx="36" ry="13"/><text x="100" y="229" text-anchor="middle">Çene</text>')+
   '</svg></div><div class="ca-zone" id="caZone" aria-live="polite"><h3>Yüzünüzde bir bölge seçin</h3><p>Seçtiğiniz bölgeye göre ilgili bakım sayfalarını gösterelim.</p></div></div></div>'; }

function caRouteCard(s,code,place){ var q=CP[s]; if(!q) return "";
  return '<button class="ca-route" data-go="cilt/'+s+'"'+caL(code,place)+'><img src="'+caPoster(q.hero)+'" alt="" loading="lazy"><span><b>'+q.t+'</b><small>'+caPriceTxt(q)+'</small></span><em>Sayfası →</em></button>'; }

function caMenuHTML(code){ var rows=PLANS.cilt.opts.map(function(o){ var s=CA_OPT2SLUG[o.id];
   return '<div class="ca-row" data-d="'+(o.d||0)+'">'+(s?'<button data-go="cilt/'+s+'"'+caL(code,"menu-sayfa")+'>':'<span>')+'<b>'+o.n+'</b><br><small>'+(o.d?o.d+" dk":(o.s||""))+(s?' · sayfası →':'')+'</small>'+(s?'</button>':'</span>')+
    '<button class="pr" data-plan="cilt" data-opt="'+o.id+'"'+caL(code,"menu-saat")+'>'+(o.p?fmtTL(o.p):"Ön görüşme")+'</button>'+
    (CA_PKG[o.id]?'<span class="pk">5 seans paketi: <b>'+fmtTL(o.p*4.5)+'</b> (tek seansın 4,5 katı)</span>':'')+'</div>'; }).join("");
  return '<div class="sec gutter"><div class="sec-head"><span class="eyebrow">Bakım menüsü</span><h2>Süreye göre <em>seçin</em>.</h2><p>Fiyata dokunun, davetiyeniz o bakımla açılsın.</p></div><div class="ca-menu">'+
   '<div class="ca-filter">'+[["0","Tümü"],["30","30 dk"],["60","60 dk"],["90","90 dk"],["120","120 dk"]].map(function(f,i){ return '<button data-caf="'+f[0]+'" aria-pressed="'+(i===0)+'"'+caL(code,"menu-filtre")+'>'+f[1]+'</button>'; }).join("")+'</div>'+
   '<div class="ca-rows">'+rows+'</div><p class="menu-src">Randevu sistemindeki aktif menüden · 7 Ekim 2026</p></div></div>'; }

function caDuelHTML(sc,code){ var side=function(s){ var q=CP[s], o=caOpt(q.opt), here=s===CA.cur;
   return '<article class="'+(here?"here":"")+'"><span class="eyebrow">'+(here?"Bu sayfa":"Kardeşi")+'</span><h3>'+q.t+'</h3><span class="pr">'+fmtTL(o.p)+'</span><small class="muted">'+o.d+' dk · '+q.lede+'</small>'+
    '<div class="row"><button class="btn-line" data-plan="cilt" data-opt="'+o.id+'"'+caL(code,"duello-saat")+'>Saatimi seç</button>'+(here?'':'<button class="btn-line" data-go="cilt/'+s+'"'+caL(code,"duello-git")+'>Sayfası →</button>')+'</div></article>'; };
  return '<div class="sec gutter"><div class="sec-head"><span class="eyebrow">Işıltı düellosu</span><h2>Hollywood mu, <em>Paris</em> mi?</h2><p>İkisi de iki saatlik ışıltı bakımı; ürün ve adımları farklı. Hangisinin cildinize uygun olduğunu uzmanımız cildinize bakarak söyler.</p></div>'+
   '<div class="ca-duel">'+side(sc.a)+'<span class="vs">ya da</span>'+side(sc.b)+'</div></div>'; }

function caPickHTML(p){ var k=p.pick;
  return '<div class="sec gutter"><div class="ca-pick"><span class="eyebrow">Size özel</span><h3>'+k.h+'</h3><div class="ca-opts">'+k.o.map(function(o,i){ return '<button data-cap="'+i+'" aria-pressed="false"'+caL(p.code,"secim")+'>'+o[1]+(o[2]?' <small>'+o[2]+'</small>':'')+'</button>'; }).join("")+'</div>'+
   '<div class="ca-ctas"><a class="btn-gold shine" id="caPickWa" href="'+waHref(k.msg.replace("{x}","seçmedim")+" "+visitCode())+'" target="_blank" rel="noopener"'+caL(p.code,"secim-wa")+'><span class="lbl">Seçimimi WhatsApp\'ta gönder</span></a></div><p class="fine">'+k.note+'</p></div></div>'; }

function caProofHTML(p){ if(p.proof&&p.proof.length) return '<div class="sec gutter" style="padding-bottom:0"><div class="sec-head"><span class="eyebrow">Gerçek sonuç</span><h2>Basılı tutun, <em>öncesini</em> görün.</h2><p>Salonumuzda bakım yaptıran danışanlarımız; Instagram hesabımızdan, düzenlenmeden. Sonuçlar kişiden kişiye değişir.</p></div><div class="gal" id="caGal"></div></div>';
  if(p.kind!=="H") return "";
  return '<div class="sec gutter" style="padding-bottom:0"><div class="ca-honest"><span class="eyebrow">Önce / sonra</span><b>Bu bakımın önce/sonra fotoğraflarını henüz yayınlamadık.</b><span>Sahte ya da başka salona ait görsel kullanmıyoruz. Danışanlarımızın izinli fotoğrafları hazırlanıyor; bu sayfadaki videolar salonumuzda çekilmiş gerçek uygulamalardır.</span></div></div>'; }

function caQuoteHTML(p){ if(!p.quote) return ""; var r=REVIEWS.filter(function(x){ return x.f==="cilt"&&x.n===p.quote; })[0]; if(!r) return "";
  return '<div class="sec gutter"><figure class="ca-quote"><span class="eyebrow">Bir danışanımız anlatıyor</span><blockquote>“'+r.t.replace(/</g,"&lt;")+'”</blockquote><figcaption>'+r.n+' · '+months(r.d)+' · Google ★★★★★</figcaption></figure></div>'; }

function caPriceHTML(p){ var o=caOpt(p.opt); if(!o) return "";
  var big=p.from?p.from.toLocaleString("tr-TR")+' TL<small>\'den</small>':fmtTL(o.p)+(o.d?' <small>· '+o.d+' dk</small>':'');
  return '<div class="sec gutter"><div class="two"><div class="menu-card ca-price"><span class="eyebrow">Fiyat · aktif menü</span><div class="big">'+big+'</div>'+
   (p.levels?'<div class="ca-pkg">'+p.levels+'; 3 seanslık paketler.</div>':(o.s?'<div class="ca-pkg">'+o.s+'</div>':''))+
   (CA_PKG[o.id]?'<div class="ca-pkg">5 seanslık paket: <b>'+fmtTL(o.p*4.5)+'</b> · tek seans fiyatının 4,5 katı</div>':'')+
   '<div class="ca-ctas"><button class="btn-gold shine" data-plan="cilt" data-opt="'+o.id+'"'+caL(p.code,"fiyat-saat")+'><span class="lbl">Bu bakım için saatimi seç</span></button></div><p class="menu-src">Randevu sistemindeki aktif menüden · 7 Ekim 2026</p></div>'+
   '<div><div class="sec-head" style="margin-bottom:16px"><span class="eyebrow">Nasıl geçer</span><h2 style="font-size:40px">Önce bakarız, sonra bakım.</h2></div><ol class="how"><li><div><b>Cildinize bakarız</b><p>Cilt tipiniz, hassasiyetiniz ve şikâyetiniz birlikte değerlendirilir.</p></div></li><li><div><b>Bakımı uygularız</b><p>'+p.t+(o.d?', yaklaşık '+o.d+' dakika.':'.')+'</p></div></li><li><div><b>Ev bakımını konuşuruz</b><p>Sonraki seans ve evde yapılacaklar birlikte planlanır.</p></div></li></ol></div></div></div>'; }

function caRoutesHTML(p){ var r=p.route||[]; if(!r.length) return "";
  var head=p.kind==="H"?["Bunlara da bakın","Yakın <em>bakımlar</em>."]:["Bu ihtiyaç için","Size uygun <em>bakımlar</em>."];
  return '<div class="sec gutter"><div class="sec-head"><span class="eyebrow">'+head[0]+'</span><h2>'+head[1]+'</h2>'+(p.kind==="I"?'<p>Bu sayfa bir rehberdir; fiyat seçtiğiniz bakıma göredir.</p>':'')+'</div><div class="ca-routes">'+r.map(function(s){ return caRouteCard(s,p.code,"git"); }).join("")+'</div>'+
   '<p style="margin-top:16px"><button class="btn-line" data-go="cilt"'+caL(p.code,"atlas")+'>Tüm Cilt Atlası →</button></p></div>'; }

function caFaqHTML(p){ if(!p.faq) return ""; return '<div class="sec gutter faq" style="padding-top:0"><div class="sec-head"><span class="eyebrow">Sık sorulanlar</span><h2>Aklınızdakiler</h2></div>'+p.faq.map(function(f){ return '<details><summary'+caL(p.code,"sss")+'>'+f[0]+'</summary><p>'+f[1]+'</p></details>'; }).join("")+'</div>'; }

function caEndHTML(p){ return '<div class="sec gutter"><div class="invite-teaser"><span class="eyebrow">Sizin hikâyeniz</span><h3>Cildiniz için bir saat ayırın.</h3><div class="steps-mini"><span>1 · Bakım</span><span>2 · Gün ve saat</span><span>3 · Davetiye → WhatsApp</span></div>'+
  '<div class="ca-ctas"><button class="btn-gold shine" data-plan="cilt" data-opt="'+caMainOpt(p)+'"'+caL(p.code,"son-saat")+'><span class="lbl">Davetiyemi hazırla</span></button><a class="btn-line" href="'+waHref(caWaMsg(p))+'" target="_blank" rel="noopener"'+caL(p.code,"son-wa")+'>WhatsApp\'tan sor</a></div></div></div>'; }

function caDarkHTML(d){ return '<div class="sec dark-band gutter"><div class="golden"><div class="led-frame lit">'+caMedia(d.m,false)+'</div><div class="sec-head" style="margin:0"><span class="eyebrow">'+d.k+'</span><h2>'+d.h+'</h2><p>'+d.p+'</p></div></div></div>'; }

/* ---------- davranış ---------- */
function caStory(box){ var acts=$$(".ca-act",box), layers=$$(".ca-layer",box), count=$(".ca-count",box), cap=$(".ca-cap",box), n=acts.length, cur=-1;
  function vid(l){ return $("video",l); }
  function set(i){ if(i===cur) return; cur=i; var k=acts[i].dataset.k;
    acts.forEach(function(a,j){ a.classList.toggle("on",j===i); });
    layers.forEach(function(l){ var on=l.dataset.k===k, v=vid(l); l.classList.toggle("on",on);
      if(!v) return; if(on && S.tier!=="C"){ if(v.dataset.src){ v.src=v.dataset.src; v.removeAttribute("data-src"); } var pr=v.play(); if(pr&&pr.catch) pr.catch(function(){}); } else if(!on) v.pause(); });
    count.textContent=CA_ROMAN[i]+" / "+CA_ROMAN[n-1]; cap.textContent=(CM[k]&&CM[k].alt?CM[k].alt+" · salonumuzda":""); }
  var io=new IntersectionObserver(function(es){ es.forEach(function(e){ if(e.isIntersecting) set(+e.target.dataset.i); }); },{rootMargin:"-45% 0px -45% 0px"});
  acts.forEach(function(a){ io.observe(a); }); CA.obs.push(io);
  var vis=new IntersectionObserver(function(es){ if(!es[0].isIntersecting) layers.forEach(function(l){ var v=vid(l); if(v) v.pause(); }); else if(cur>=0){ var v=vid(layers.filter(function(l){ return l.classList.contains("on"); })[0]); if(v&&!v.dataset.src&&S.tier!=="C"){ var pr=v.play(); if(pr&&pr.catch) pr.catch(function(){}); } } });
  vis.observe(box); CA.obs.push(vis); set(0); }

function caFilm(sec){ var cv=$("canvas",sec), ctx=cv.getContext("2d"), bar=$(".ca-film-bar",sec), capB=$(".ca-film-cap b",sec), capS=$(".ca-film-cap span",sec),
  N=+sec.dataset.n, C=+sec.dataset.cols, fw=+sec.dataset.fw, fh=+sec.dataset.fh, img=null, cur=-1, ci=-1;
  function load(){ if(img||S.tier==="C") return; img=new Image(); img.decoding="async"; img.onload=function(){ cur=-1; update(); }; img.src="m/ig/film/cilt-saten-film.webp"; }
  var io=new IntersectionObserver(function(es){ if(es[0].isIntersecting) load(); },{rootMargin:"800px"}); io.observe(sec); CA.obs.push(io);
  function update(){ if(!sec.isConnected||S.view!=="cilt"||S.tier==="C") return; var r=sec.getBoundingClientRect(), vh=innerHeight; if(r.bottom<0||r.top>vh) return;
    var p=Math.min(1,Math.max(0,-r.top/(r.height-vh))), i=Math.min(N-1,Math.round(p*(N-1)));
    bar.style.width=(p*100).toFixed(1)+"%";
    var c=0; CA_FILM_CAPS.forEach(function(x,j){ if(p>=x[0]) c=j; }); if(c!==ci){ ci=c; capB.textContent=CA_FILM_CAPS[c][1]; capS.textContent=CA_FILM_CAPS[c][2]; }
    if(img&&img.complete&&img.naturalWidth&&i!==cur){ cur=i; ctx.drawImage(img,(i%C)*fw,Math.floor(i/C)*fh,fw,fh,0,0,cv.width,cv.height); cv.style.opacity=1; } }
  CA.film=update; update(); }

function caMap(box){ var panel=$("#caZone",box);
  function pick(g){ var id=g.dataset.z, z=CA_ZONES[id]; $$(".z",box).forEach(function(x){ x.setAttribute("aria-pressed",x===g); });
    panel.innerHTML='<span class="eyebrow">Seçtiğiniz bölge</span><h3>'+z[0]+'</h3><p>'+z[1]+'</p><div class="ca-routes">'+z[2].map(function(s){ return caRouteCard(s,CP[CA.cur].code,"harita-git"); }).join("")+'</div>'; relead(); }
  $$(".z",box).forEach(function(g){ g.addEventListener("click",function(){ pick(g); }); g.addEventListener("keydown",function(e){ if(e.key==="Enter"||e.key===" "){ e.preventDefault(); pick(g); } }); }); }

function caMenu(box){ $$("[data-caf]",box).forEach(function(b){ b.addEventListener("click",function(){ var f=+b.dataset.caf;
  $$("[data-caf]",box).forEach(function(x){ x.setAttribute("aria-pressed",x===b); });
  $$(".ca-row",box).forEach(function(r){ r.hidden=!!f && +r.dataset.d!==f; }); }); }); }

function caPick(p,box){ var k=p.pick, a=$("#caPickWa",box);
  $$("[data-cap]",box).forEach(function(b){ b.addEventListener("click",function(){ var o=k.o[+b.dataset.cap];
    $$("[data-cap]",box).forEach(function(x){ x.setAttribute("aria-pressed",x===b); });
    a.href=waHref(k.msg.replace("{x}",o[1].toLocaleLowerCase("tr-TR"))+" "+visitCode()); }); }); }

/* ---------- sayfa ---------- */
function caRender(slug){ var p=CP[slug], box=$("#ciltPage");
  var acts=p.acts==="seans"?CA_SEANS:p.acts, head=p.actsHead?[p.actsHead[0],p.actsHead[1].replace(/, (.*)\.$/,", <em>$1</em>.")]:["Bir bakımın hikâyesi","Aynadan <em>koltuğa</em>."];
  var sc=p.scene||{}, h=caHero(p);
  if(sc.type==="menu") h+=caMenuHTML(p.code);
  if(sc.type==="map") h+=caMapHTML(p.code);
  h+=caStoryHTML(acts,head,p.code);
  if(p.film) h+=caFilmHTML(p.film);
  if(p.dark) h+=caDarkHTML(p.dark);
  if(sc.type==="duel") h+=caDuelHTML(sc,p.code);
  if(p.pick) h+=caPickHTML(p);
  h+=caProofHTML(p)+caQuoteHTML(p)+(p.kind==="H"?caPriceHTML(p):"")+caRoutesHTML(p)+caFaqHTML(p)+caEndHTML(p);
  box.innerHTML=h;
  $$("[data-ca-story]",box).forEach(caStory);
  var f=$("#caFilm",box); if(f) caFilm(f);
  if(sc.type==="map") caMap(box);
  if(sc.type==="menu") caMenu(box);
  if(p.pick) caPick(p,box);
  var g=$("#caGal",box); if(g) p.proof.forEach(function(k){ var m=CM[k], b="m/ig/"+m.pair; card(g,b+"-sonra-"+m.s+".webp",b+"-once-"+m.s+".webp",m.alt,m.s!==480); });
  initAutoVids(box);
  $$("[data-dust]",box).forEach(initDust);
  S.planOpt.cilt=caMainOpt(p);
  try{ document.title=p.t+" · Selda Gençer Beauty Center"; }catch(e){}
  relead(); }

function ciltRoute(sub){ var hub=$("#ciltHub"), pg=$("#ciltPage");
  CA.obs.forEach(function(o){ o.disconnect(); }); CA.obs=[]; CA.film=null;
  $$("video",pg).forEach(function(v){ v.pause(); });
  CA.cur=sub||null; S.route=caRoute();
  if(!sub){ pg.hidden=true; pg.innerHTML=""; hub.hidden=false; try{ document.title=CA.title; }catch(e){} return; }
  hub.hidden=true; pg.hidden=false; caRender(sub); }
CA.title=document.title;
scrollers.push(function(){ if(CA.film) CA.film(); });

/* ---------- hub: atlas + seans hikâyesi ---------- */
function caAtlasHTML(){ return CA_GROUPS.map(function(g){ var list=Object.keys(CP).filter(function(s){ return CP[s].grp===g[0]; }); if(!list.length) return "";
  return '<div class="ca-grp"><h3>'+g[1]+'</h3><div class="ca-grid">'+list.map(function(s){ var q=CP[s], k=q.hero, mono=!CM[k];
   return '<button class="ca-tile'+(mono?" mono":"")+'" data-go="cilt/'+s+'" data-track-label="at-cilt-atlas"><img src="'+caPoster(k)+'" alt="" loading="lazy"><span><b>'+q.t+'</b><small>'+caPriceTxt(q)+'</small></span></button>'; }).join("")+'</div></div>'; }).join(""); }
function caInitHub(){ var a=$("#ciltAtlas"); if(a && !a.dataset.done){ a.dataset.done=1; a.innerHTML=caAtlasHTML(); }
  var s=$("#ciltHubStory"); if(s && !s.dataset.done){ s.dataset.done=1; s.innerHTML=caStoryHTML(CA_SEANS,["Bir bakımın içinden","Klasik bakım, <em>adım adım</em>."],"cilt").replace('class="sec gutter ca-story"','class="ca-story"'); hubStory(); } }
function hubStory(){ var b=$("#ciltHubStory [data-ca-story]"); if(!b) return; var keep=CA.obs; CA.obs=[]; caStory(b); CA.hubObs=CA.obs; CA.obs=keep; }
/* ---------- /CİLT ATLASI ---------- */
