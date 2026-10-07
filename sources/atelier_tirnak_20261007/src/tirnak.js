/* ---------- TIRNAK ATELYESİ: 22 nail pages (sources/atelier_tirnak_20261007) ----------
   Pages are static <template data-tz-page> blocks written by render.py; shared blocks come in as
   <template data-tz-inc-tpl>. tzShow() clones one page into #tzMount and wires its scenes. Every name here
   starts with tz/TZ so it cannot collide with the other families' code. Uses the prototype's helpers
   ($, $$, S, lbl, waHref, visitCode, openPlanner, openStory, sampleSlots, months, initLive, initDust, SW, SHAPES). */
var TZ_PAGES=__TZ_PAGES__, TZ_REVIEWS=__TZ_REVIEWS__, TZ_QUOTES=__TZ_QUOTES__, TZ_BAKIM_HAFTA=__TZ_BAKIM__;
(function(p){ Object.keys(p).forEach(function(k){ PLANS[k]=p[k]; }); })(__TZ_PLANS__);
// Badem is a planner shape only: on the glossy bordo photo the automatic nail mask leaves the highlights out, so the
// Renk Atölyesi keeps its three clean shapes until a hand-traced mask exists.
SHAPES.badem={n:"Badem",img:"m/ig/tirnak-badem-bordo-k.webp",alt:"Bordo badem protez tırnak"};
var TZ={page:null,pg:null,model:null,ton:null,uzunluk:null,color:null,colorTouched:false,bakim:false,bkDay:null,scrollers:[],obs:[],timers:[]};
// mean nail luminance under each mask (measured on the photos); the recolour maps it onto the polish colour
var TZ_LREF={uzun:.233,kare:.217,oval:.348}, TZ_ORIG={uzun:"kiraz",kare:"kiraz",oval:"kiraz"};
var TZ_SWEEP="linear-gradient(90deg,#000 calc(var(--x) * 1.12% - 12%),transparent calc(var(--x) * 1.12%))";
STORIES["tz-merkez"]=[
  {t:"Salon",th:"m/ig/salon-tur-poster.webp",fr:[{video:"m/ig/salon-tur.mp4",poster:"m/ig/salon-tur-poster.webp",cap:"Tırnak barı ve salon"}]},
  {t:"Hijyen",th:"m/ig/tirnak-hijyen-4.webp",fr:[{img:"m/ig/tirnak-hijyen-1.webp",cap:"Önce yıkama"},{img:"m/ig/tirnak-hijyen-2.webp",cap:"Kurulama"},{img:"m/ig/tirnak-hijyen-3.webp",cap:"Tıbbi seviyede sterilizasyon"},{img:"m/ig/tirnak-hijyen-4.webp",cap:"Paketiniz yanınızda açılır"}]},
  {t:"Tasarımlar",th:"m/ig/tirnak-holo-800.webp",fr:[{img:"m/ig/tirnak-3d-800.webp",cap:"3D çiçek ve inci"},{img:"m/ig/tirnak-holo-800.webp",cap:"Aurora cat-eye"},{img:"m/ig/tirnak-mermer-k.webp",cap:"Altın hatlı kelebek"},{img:"m/ig/tirnak-gumus-800.webp",cap:"Simli ombre"}]},
  {t:"Video",th:"m/ig/tirnak-krom-poster.webp",fr:[{video:"m/ig/tirnak-papatya.mp4",poster:"m/ig/tirnak-papatya-poster.webp",cap:"3D papatya"},{video:"m/ig/tirnak-krom.mp4",poster:"m/ig/tirnak-krom-poster.webp",cap:"Krom french"},{video:"m/ig/tirnak-babyboomer.mp4",poster:"m/ig/tirnak-babyboomer-poster.webp",cap:"Baby boomer"}]},
  {t:"Yorumlar",th:"m/monogram.png",fr:"rv:tirnak"},
  {t:"Fiyat",th:"m/ig/tirnak-kirmizi-2-800.webp",fr:"price:tz-merkez"}];
STORIES["tz-oje"]=[
  {t:"Kartela",th:"m/ig/tirnak-kartela.webp",fr:[{img:"m/ig/tirnak-kartela.webp",cap:"Salondaki kartelamız"}]},
  {t:"Renkler",th:"m/ig/tirnak-kirmizi-2-800.webp",fr:[{img:"m/ig/tirnak-kirmizi-2-800.webp",cap:"Parlak kırmızı"},{img:"m/ig/tirnak-lacivert-800.webp",cap:"Lacivert"},{img:"m/ig/tirnak-neon-800.webp",cap:"Neon mor"},{img:"m/ig/tirnak-bebek-mavisi-800.webp",cap:"Bebek mavisi"}]},
  {t:"Video",th:"m/ig/tirnak-lila-poster.webp",fr:[{video:"m/ig/tirnak-lila.mp4",poster:"m/ig/tirnak-lila-poster.webp",cap:"Süt beyazı"},{video:"m/ig/tirnak-orkide.mp4",poster:"m/ig/tirnak-orkide-poster.webp",cap:"Bordo"}]},
  {t:"Yorumlar",th:"m/monogram.png",fr:"rv:tirnak"},
  {t:"Fiyat",th:"m/ig/tirnak-lacivert-desen-k.webp",fr:"price:tz-oje"}];
STORIES["tz-protez"]=[
  {t:"Şekiller",th:"m/ig/tirnak-uzun-kirmizi-k.webp",fr:[{img:"m/ig/tirnak-yuvarlak-kirmizi-1200.webp",cap:"Oval"},{img:"m/ig/tirnak-kare-kirmizi-k.webp",cap:"Kare"},{img:"m/ig/tirnak-uzun-kirmizi-k.webp",cap:"Uzun"},{img:"m/ig/tirnak-badem-bordo-k.webp",cap:"Badem"}]},
  {t:"Video",th:"m/ig/tirnak-babyboomer-poster.webp",fr:[{video:"m/ig/tirnak-babyboomer.mp4",poster:"m/ig/tirnak-babyboomer-poster.webp",cap:"Baby boomer"},{video:"m/ig/tirnak-krom.mp4",poster:"m/ig/tirnak-krom-poster.webp",cap:"Krom french"}]},
  {t:"Hijyen",th:"m/ig/tirnak-hijyen-4.webp",fr:[{img:"m/ig/tirnak-hijyen-1.webp",cap:"Önce yıkama"},{img:"m/ig/tirnak-hijyen-3.webp",cap:"Tıbbi seviyede sterilizasyon"},{img:"m/ig/tirnak-hijyen-4.webp",cap:"Paketiniz yanınızda açılır"}]},
  {t:"Yorumlar",th:"m/monogram.png",fr:"rv:tirnak"},
  {t:"Fiyat",th:"m/ig/tirnak-gumus-800.webp",fr:"price:tz-protez"}];
STORIES["tz-art"]=[
  {t:"Tasarımlar",th:"m/ig/tirnak-3d-800.webp",fr:[{img:"m/ig/tirnak-3d-800.webp",cap:"3D çiçek ve inci"},{img:"m/ig/tirnak-mor-k.webp",cap:"Ametist ve altın"},{img:"m/ig/tirnak-bakir-desen-800.webp",cap:"Kaplumbağa kabuğu"},{img:"m/ig/tirnak-leopar-800.webp",cap:"Leopar"}]},
  {t:"Video",th:"m/ig/tirnak-papatya-poster.webp",fr:[{video:"m/ig/tirnak-papatya.mp4",poster:"m/ig/tirnak-papatya-poster.webp",cap:"3D papatya"},{video:"m/ig/tirnak-krom.mp4",poster:"m/ig/tirnak-krom-poster.webp",cap:"Krom french"}]},
  {t:"Yorumlar",th:"m/monogram.png",fr:"rv:tirnak"},
  {t:"Fiyat",th:"m/ig/tirnak-holo-800.webp",fr:"price:tz-art"}];
STORIES["tz-bakim"]=[
  {t:"Hijyen",th:"m/ig/tirnak-hijyen-4.webp",fr:[{img:"m/ig/tirnak-hijyen-1.webp",cap:"Önce yıkama"},{img:"m/ig/tirnak-hijyen-2.webp",cap:"Kurulama"},{img:"m/ig/tirnak-hijyen-3.webp",cap:"Tıbbi seviyede sterilizasyon"},{img:"m/ig/tirnak-hijyen-4.webp",cap:"Paketiniz yanınızda açılır"}]},
  {t:"Hazırlık",th:"m/ig/tirnak-hazirlik-poster.webp",fr:[{video:"m/ig/tirnak-hazirlik.mp4",poster:"m/ig/tirnak-hazirlik-poster.webp",cap:"Eldivenli eller"}]},
  {t:"Salon",th:"m/ig/salon-tur-poster.webp",fr:[{video:"m/ig/salon-tur.mp4",poster:"m/ig/salon-tur-poster.webp",cap:"Tırnak barı ve salon"}]},
  {t:"Yorumlar",th:"m/monogram.png",fr:"rv:tirnak"},
  {t:"Fiyat",th:"m/ig/tirnak-hijyen-oda.webp",fr:"price:tz-bakim"}];

function tzEsc(s){ return String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/"/g,"&quot;"); }
function tzRoute(){ return !TZ.page||TZ.page==="tirnak"?"tirnak":"tirnak/"+TZ.page; }
function tzKey(){ return TZ.pg?"tz-"+TZ.pg.code:"tirnak"; }
function tzInView(el,fn,th){ var io=new IntersectionObserver(function(es){ if(es[0].isIntersecting){ io.disconnect(); fn(); } },{threshold:th||.35}); io.observe(el); TZ.obs.push(io); }
function tzTween(a,b,ms,fn,done){ var t0=performance.now(), h={stop:false}; (function f(t){ if(h.stop) return; var k=Math.min(1,(t-t0)/ms); fn(a+(b-a)*ease(k)); if(k<1) requestAnimationFrame(f); else if(done) done(); })(t0); return h; }
function tzColorName(){ var s=SW.filter(function(x){return x.id===TZ.color})[0]; return s?s.name:null; }
function tzBarLabel(){ var pg=TZ.pg; if(!pg) return "Tırnak · saatimi seç";
  if(TZ.model) return TZ.model+" · saatimi seç";
  if(TZ.ton) return TZ.ton.split(" (")[0]+" · saatimi seç";
  if(TZ.colorTouched && tzColorName()) return tzColorName()+" · saatimi seç";
  if(TZ.uzunluk) return TZ.uzunluk+" · saatimi seç";
  return pg.bar; }

/* planner text: shape, colour, kartela tone, model and length ride along so the team knows what was chosen */
function tzExtras(shape,withColor){ var parts=[], meta=[];
  if(shape){ parts.push("şekil: "+shape.toLocaleLowerCase("tr-TR")); }
  if(TZ.colorTouched && tzColorName() && withColor){ parts.push("renk: "+tzColorName()); meta.push(tzColorName()); }
  if(TZ.ton){ parts.push("kartelada beğendiğim ton: "+TZ.ton); meta.push(TZ.ton); }
  if(TZ.model){ var m=TZ.model.indexOf("(")>0?TZ.model:TZ.model+" (sitedeki fotoğraf)"; parts.push("model: "+m); meta.push(TZ.model); }
  if(TZ.uzunluk){ parts.push("uzunluk: "+TZ.uzunluk.toLocaleLowerCase("tr-TR")); meta.push(TZ.uzunluk); }
  return {parts:parts,meta:meta}; }
function tzMsg(o,day,time,shape,code){ var when=day?((day.label==="Bugün"||day.label==="Yarın")?day.label.toLocaleLowerCase("tr-TR"):day.full)+" "+time:"";
  var x=tzExtras(shape,/oje|protez|art/i.test(o.n)), pg=TZ.pg||{}, from=pg.semtFrom?pg.semtFrom+" yazıyorum; ":"", rest=x.parts.join(", ");
  var bk=TZ.bakim&&TZ.bkDay?" Bakım randevumu da "+TZ_BAKIM_HAFTA+" hafta sonrasına, "+TZ.bkDay+" saat "+time+" için ayırabilir misiniz?":"";
  return "Merhaba, "+from+o.n.toLocaleLowerCase("tr-TR")+" için "+when+" uygun mu?"+(rest?" "+rest.charAt(0).toLocaleUpperCase("tr-TR")+rest.slice(1)+".":"")+bk+(o.ask?" Fiyat bilgisini de alabilir miyim?":"")+" "+code; }
function tzMeta(shape,o){ var x=tzExtras(null,!o||/oje|protez|art/i.test(o.n)); return (shape?" · "+shape:"")+(x.meta.length?" · "+x.meta.join(" · "):"")+(TZ.bakim&&TZ.bkDay?" · bakım "+TZ.bkDay:""); }

/* T13 bakım randevusu: protez maintenance is every 4 weeks (owner); one tap books the next one too.
   Same weekday 4 weeks on, so it is never a Monday (closed). Called before tzMsg/tzMeta on every render. */
var TZ_BAKIM_OPTS=["mpk","uzatma","dolgu"];
function tzBakim(o,day,n){ TZ.bkDay=null; if(!o||!day||TZ_BAKIM_OPTS.indexOf(o.id)<0) return "";
  var d=new Date(day.date.getTime()+TZ_BAKIM_HAFTA*7*864e5); TZ.bkDay=d.getUTCDate()+" "+TR_MON[d.getUTCMonth()]+" "+TR_DAYS[d.getUTCDay()];
  return '<div class="pstep tz-bk"><span class="eyebrow"><i>'+n+'</i> Bakım · '+TZ_BAKIM_HAFTA+' hafta sonra</span><button class="opt" data-tz-bakim aria-pressed="'+(!!TZ.bakim)+'"><span class="rad"></span>'+
    '<span class="nm">Bakım randevumu da ayırın<small>'+TZ.bkDay+' · aynı saat · bakım aralığımız '+TZ_BAKIM_HAFTA+' hafta</small></span></button></div>'; }
function tzBakimBind(box,rerender,key){ $$("[data-tz-bakim]",box).forEach(function(b){ lbl(b,key); b.addEventListener("click",function(){ TZ.bakim=!TZ.bakim; rerender(); }); }); }

/* ---------- page engine ---------- */
function tzBoot(){
  scrollers.push(function(){ if(S.view!=="tirnak") return; TZ.scrollers.forEach(function(f){ f(); }); });
  tzFilters();
  document.addEventListener("click",function(e){ var b=e.target.closest("[data-tz-plan]"); if(!b||S.view!=="tirnak"||!TZ.pg) return;
    if(b.dataset.tzModel) TZ.model=b.dataset.tzModel; updateBar(); openPlanner(TZ.pg.fam,TZ.pg.opt||null); }); }
function tzShow(slug){ if(!TZ_PAGES[slug]) slug="tirnak"; var pg=TZ_PAGES[slug], mount=$("#tzMount");
  TZ.obs.forEach(function(o){ o.disconnect(); }); TZ.timers.forEach(clearTimeout); TZ.obs=[]; TZ.timers=[]; TZ.scrollers=[];
  $$("video",mount).forEach(function(v){ v.pause(); v.removeAttribute("src"); });
  mount.innerHTML=""; mount.appendChild(document.querySelector('template[data-tz-page="'+slug+'"]').content.cloneNode(true));
  $$("[data-tz-inc]",mount).forEach(function(el){ var f=document.querySelector('template[data-tz-inc-tpl="'+el.dataset.tzInc+'"]').content.cloneNode(true), arg=el.dataset.tzArg;
    if(arg && f.firstElementChild) f.firstElementChild.setAttribute("data-tz-arg",arg); el.parentNode.replaceChild(f,el); });
  TZ.page=slug; TZ.pg=pg; TZ.model=null; TZ.ton=null; TZ.uzunluk=null; S.route=tzRoute();
  var sel=$("#tzSel"); if(sel) sel.value=slug;
  $$("[data-tz-rings]",mount).forEach(tzRings);
  $$("[data-tz-film]",mount).forEach(tzFilm);
  $$("[data-tz-atelier]",mount).forEach(tzAtelier);
  $$("[data-tz-kartela]",mount).forEach(tzKartela);
  $$("[data-tz-hijyen]",mount).forEach(tzHijyen);
  $$(".tz-wall-sec",mount).forEach(tzWall);
  $$(".tz-sekil-sec",mount).forEach(tzSekil);
  $$("[data-tz-quotes]",mount).forEach(tzQuotes);
  $$("[data-tz-rv]",mount).forEach(tzReviews);
  $$("[data-tz-inline]",mount).forEach(tzInline);
  $$("[data-tz-saat]",mount).forEach(tzSaat);
  $$("[data-tz-katman],.tz-yerel",mount).forEach(function(el){ tzInView(el,function(){ el.classList.add("in"); }); });
  tzVids(mount); tzWa(mount);
  $$("[data-dust]",mount).forEach(initDust);
  setSemt(S.semt); initLive();
  tzLabel(mount); TZ.timers.push(setTimeout(function(){ tzLabel(mount); },0));
  relead(); }

/* every button and link: data-track-label="at-tz-<page>-<place>" (ASCII, <=48) */
function tzLabel(sc){ var c="at-tz-"+TZ.pg.code+"-";
  $$("[data-tz-place]",sc).forEach(function(b){ lbl(b,c+b.dataset.tzPlace); });
  $$("a,button,summary,input",sc).forEach(function(b){ var k=b.getAttribute("data-track-label")||""; if(k.indexOf(c)===0) return;
    var kind="diger";
    if(b.matches("summary")) kind="sss"; else if(b.matches("[data-go]")) kind="git-"+((b.dataset.go.split("/")[1]||"merkez").split("-")[0]);
    else if(b.matches("[data-zoom]")) kind="yakindan"; else if(b.matches(".ring")) kind="hikaye"; else if(b.matches(".sw")) kind="renk";
    else if(b.matches(".tz-ks")) kind="kartela"; else if(b.matches("[data-tz-shape],[data-tz-sekil]")) kind="sekil"; else if(b.matches("[data-tz-f]")) kind="suzgec";
    else if(b.matches("a[href^='tel:']")) kind="tel"; else if(b.matches("a[href*='wa.me']")) kind="wa"; else if(b.matches("a[href*='google.com/maps']")) kind="yol-tarifi";
    else if(b.matches("[data-copy]")) kind="tel-kopyala"; else if(b.matches("input")) kind="hafta"; else if(b.matches("[data-tz-plan]")) kind="davetiye-ac";
    lbl(b,c+kind); }); }
function tzRings(box){ var fam=box.dataset.tzRings; (STORIES[fam]||[]).forEach(function(s,i){ var b=document.createElement("button"); b.className="ring";
  b.innerHTML='<i><img src="'+s.th+'" alt="" loading="lazy"></i><span>'+s.t+'</span>'; b.addEventListener("click",function(){ openStory(fam,i); }); box.appendChild(b); }); }
function tzVids(sc){ $$("video.auto-vid",sc).forEach(function(v){ v.addEventListener("error",function(){ v.classList.add("tz-off"); }); }); if(S.tier==="C") return; $$("video.auto-vid",sc).forEach(function(v){ var io=new IntersectionObserver(function(es){ var on=es[0].isIntersecting;
  if(on && v.dataset.src){ v.src=v.dataset.src; v.removeAttribute("data-src"); } if(on){ var pr=v.play(); if(pr&&pr.catch) pr.catch(function(){}); } else v.pause(); },{threshold:.2}); io.observe(v); TZ.obs.push(io); }); }
function tzWa(sc){ var base=TZ.pg.code==="merkez"?"tırnak":TZ.pg.nav.toLocaleLowerCase("tr-TR");
  $$("[data-tz-wa]",sc).forEach(function(a){ a.href=waHref((a.dataset.tzMsg||"Merhaba, "+base+" için randevu almak istiyorum.")+" "+visitCode()); }); }

/* ---------- T1 / T4: scroll films from 4x3 WebP atlases (frame i lives in atlas i % n) ---------- */
function tzFilm(sec){ var slug=sec.dataset.tzFilm, N=+sec.dataset.frames, NA=+sec.dataset.atlases, walk=sec.classList.contains("walk");
  var cv=$("canvas:not(.dust)",sec), ctx=cv.getContext("2d"), atl=[], cur=-1, curStop=-1, caps=JSON.parse(sec.dataset.caps||"[]");
  var stops=(sec.dataset.stops||"").split(",").filter(Boolean).map(Number), hero=$(".walk-hero",sec), cap=$(".walk-cap",sec), rail=$(".walk-rail",sec), bar=$(".film-bar i",sec), fcap=$(".tz-fcap",sec), beam=$(".walk-beam",sec), dots=[];
  if(rail){ stops.forEach(function(){ rail.appendChild(document.createElement("li")); }); dots=$$("li",rail); }
  var loading=false;
  function load(){ if(loading||S.tier==="C") return; loading=true; var order=[0,2,1,3].filter(function(k){ return k<NA && (S.tier!=="B"||k%2===0); });
    (function next(){ var k=order.shift(); if(k===undefined) return; var im=new Image(); im.decoding="async"; im.src="m/ig/"+slug+"-atlas-"+k+".webp";
      im.onload=function(){ atl[k]=im; cur=-1; update(); next(); }; im.onerror=next; })(); }
  function size(){ var r=cv.getBoundingClientRect(), d=Math.min(2,window.devicePixelRatio||1), w=Math.round(r.width*d), h=Math.round(r.height*d); if(w&&h&&(cv.width!==w||cv.height!==h)){ cv.width=w; cv.height=h; cur=-1; } }
  function draw(i){ var k=-1; for(var d=0;d<N&&k<0;d++){ if(i-d>=0&&atl[(i-d)%NA]) k=i-d; else if(i+d<N&&atl[(i+d)%NA]) k=i+d; } if(k<0) return; size(); if(k===cur) return;
    var im=atl[k%NA], j=Math.floor(k/NA), sx=(j%4)*540, sy=Math.floor(j/4)*960, cw=cv.width, ch=cv.height, s=Math.max(cw/540,ch/960), w=540*s, h=960*s;
    ctx.drawImage(im,sx,sy,540,960,(cw-w)/2,(ch-h)/2,w,h); cv.style.opacity=1; cur=k; }
  function update(){ if(!sec.isConnected) return; if(S.tier==="C"){ if(hero){ hero.style.opacity=1; hero.style.transform=""; hero.style.pointerEvents="auto"; } return; }
    var r=sec.getBoundingClientRect(), vh=innerHeight; if(r.bottom<-60||r.top>vh+60) return;
    var tot=r.height-vh, p=Math.min(1,Math.max(0,-r.top/(tot>0?tot:1))), i=Math.min(N-1,Math.round(p*(N-1))); draw(i);
    if(walk){ var hp=Math.max(0,1-p*9); hero.style.opacity=hp.toFixed(3); hero.style.transform="translateY("+((1-hp)*-24).toFixed(1)+"px)"; hero.style.pointerEvents=hp>.2?"auto":"none";
      var st=0; stops.forEach(function(s,k){ if(i>=s) st=k; }); dots.forEach(function(d,k){ d.classList.toggle("on",k===st); });
      if(p<0.08){ if(curStop!==-1){ cap.classList.remove("show","cta"); curStop=-1; } }
      else if(st!==curStop){ curStop=st; cap.classList.remove("show"); var c=caps[st], last=st===caps.length-1;
        TZ.timers.push(setTimeout(function(){ if(curStop!==st) return; $(".n",cap).textContent=c.n+" / 0"+caps.length; $(".t",cap).textContent=c.t; $(".s",cap).textContent=c.s; cap.classList.toggle("cta",last); cap.classList.add("show"); },120));
        if(last && beam){ beam.classList.remove("go"); void beam.offsetWidth; beam.classList.add("go"); } } }
    else { if(bar) bar.style.width=(p*100).toFixed(1)+"%"; if(fcap&&caps.length){ var ci=Math.min(caps.length-1,Math.floor(p*caps.length)); if(fcap.textContent!==caps[ci]) fcap.textContent=caps[ci]; } } }
  TZ.scrollers.push(update);
  if(walk){ TZ.timers.push(setTimeout(load,document.readyState==="complete"?150:900)); if(beam) TZ.timers.push(setTimeout(function(){ beam.classList.add("go"); },60)); }
  else { var io=new IntersectionObserver(function(es){ if(es[0].isIntersecting){ io.disconnect(); load(); } },{rootMargin:"700px"}); io.observe(sec); TZ.obs.push(io); }
  update(); }

/* ---------- T2: Renk Atölyesi v2 -- 4 shapes, colour sweeps in like a brush stroke, finger drag paints ---------- */
function tzFilters(){ if($("#tzFilt")) return; var NS="http://www.w3.org/2000/svg", svg=document.createElementNS(NS,"svg");
  svg.id="tzFilt"; svg.setAttribute("width","0"); svg.setAttribute("height","0"); svg.setAttribute("aria-hidden","true"); svg.style.position="absolute";
  Object.keys(TZ_LREF).forEach(function(sh){ var L=Math.log(TZ_LREF[sh]); SW.forEach(function(s){ var f=document.createElementNS(NS,"filter"); f.setAttribute("id","tzf-"+sh+"-"+s.id); f.setAttribute("color-interpolation-filters","sRGB");
    var m=document.createElementNS(NS,"feColorMatrix"); m.setAttribute("type","saturate"); m.setAttribute("values","0"); f.appendChild(m);
    var ct=document.createElementNS(NS,"feComponentTransfer"), hex=s.c.slice(1);
    [["R",0],["G",2],["B",4]].forEach(function(c){ var v=Math.max(.03,parseInt(hex.substr(c[1],2),16)/255), fn=document.createElementNS(NS,"feFunc"+c[0]);
      fn.setAttribute("type","gamma"); fn.setAttribute("amplitude","1"); fn.setAttribute("exponent",(Math.log(v)/L).toFixed(3)); fn.setAttribute("offset","0"); ct.appendChild(fn); });
    f.appendChild(ct); svg.appendChild(f); }); });
  document.body.appendChild(svg); }
function tzAtelier(st){ var base=$(".tz-base",st), neu=$(".tz-neutral",st), T=[$(".tz-t0",st),$(".tz-t1",st)], row=$(".sw-row",st), name=$(".tz-swname",st);
  var shape=TZ_LREF[S.shape]?S.shape:"uzun", front=0, cur=null, anim=null, user=false, drag=null;
  function orig(){ return TZ_ORIG[shape]; }
  function setX(x){ st.style.setProperty("--x",x.toFixed(2)); }
  function prep(t,color,sweep){ var sh=SHAPES[shape], mi="url("+sh.mask+")"+(sweep?", "+TZ_SWEEP:"");
    t.style.backgroundImage="url("+sh.img+")"; t.style.webkitMaskImage=mi; t.style.maskImage=mi;
    t.style.webkitMaskSize=t.style.maskSize=sweep?"cover, 100% 100%":"cover"; t.style.webkitMaskPosition=t.style.maskPosition=sweep?"center, 0 0":"center";
    t.style.webkitMaskRepeat=t.style.maskRepeat="no-repeat"; t.style.webkitMaskComposite=sweep?"source-in":""; t.style.maskComposite=sweep?"intersect":"";
    t.style.filter="url(#tzf-"+shape+"-"+color+")"; }
  function neuSweep(on){ neu.style.webkitMaskImage=neu.style.maskImage=on?TZ_SWEEP:""; }
  function label(id){ var s=SW.filter(function(x){return x.id===id})[0]; name.textContent=s.name; $$(".sw",row).forEach(function(b){ b.setAttribute("aria-pressed",b.dataset.id===id); }); }
  function stop(){ if(anim){ anim.stop=true; anim=null; } }
  function settle(b,id){ st.classList.remove("sweeping"); prep(T[b],id,false); neuSweep(false); st.classList.add("painted"); if(b!==front) T[front].classList.remove("on"); front=b; cur=id; anim=null; }
  function paint(id,sweep){ stop(); label(id); TZ.color=id; var o=orig();
    if(id===o){ T.forEach(function(t){ t.classList.remove("on"); }); st.classList.remove("painted","sweeping"); neuSweep(false); cur=id; updateBar(); return; }
    var was=cur&&cur!==o, b=1-front; prep(T[b],id,sweep&&S.tier!=="C"); T[b].style.zIndex=3; T[front].style.zIndex=2; T[b].classList.add("on");
    if(!sweep||S.tier==="C"){ setX(100); settle(b,id); updateBar(); return; }
    if(!was) neuSweep(true); st.classList.add("painted","sweeping"); setX(0); anim=tzTween(0,100,950,setX,function(){ settle(b,id); });
    updateBar(); }
  SW.forEach(function(s){ var b=document.createElement("button"); b.className="sw"; b.style.setProperty("--c",s.c); b.setAttribute("aria-label",s.name); b.dataset.id=s.id;
    b.addEventListener("click",function(){ user=true; TZ.colorTouched=true; paint(s.id,true); }); row.appendChild(b); });
  function setShape(k){ if(k===shape) return; var sh=SHAPES[k]; shape=k; S.shape=k; $$("[data-tz-shape]",st).forEach(function(x){ x.setAttribute("aria-pressed",x.dataset.tzShape===k); });
    var im=new Image(); im.src=sh.img; stop();
    (im.decode?im.decode():Promise.resolve()).catch(function(){}).then(function(){ base.style.opacity=0; TZ.timers.push(setTimeout(function(){
      base.src=sh.img; base.alt=sh.alt; neu.src=sh.neutral; T.forEach(function(t){ t.classList.remove("on"); }); st.classList.remove("painted","sweeping"); neuSweep(false); cur=null; front=0;
      var c=TZ.color&&TZ.colorTouched?TZ.color:orig(); if(c!==orig()) paint(c,false); else { label(c); cur=c; } base.style.opacity=1; updateBar(); },180)); }); }
  $$("[data-tz-shape]",st).forEach(function(b){ b.setAttribute("aria-pressed",b.dataset.tzShape===shape); b.addEventListener("click",function(){ user=true; setShape(b.dataset.tzShape); }); });
  if(shape!=="uzun"){ var sh0=SHAPES[shape]; base.src=sh0.img; base.alt=sh0.alt; neu.src=sh0.neutral; }
  /* finger drag: the next colour follows the finger; let go past 40% and it settles, before that it slides back */
  function nextColor(){ var ids=SW.map(function(s){ return s.id; }).filter(function(i){ return i!==orig(); }), k=ids.indexOf(cur); return ids[(k+1)%ids.length]; }
  st.addEventListener("pointerdown",function(e){ if(e.target.closest(".palette,.ba-toggle,.zoom-btn,button")) return; drag={x0:e.clientX,id:e.pointerId,on:false}; });
  st.addEventListener("pointermove",function(e){ if(!drag||e.pointerId!==drag.id) return; var r=st.getBoundingClientRect();
    if(!drag.on){ if(Math.abs(e.clientX-drag.x0)<10) return; drag.on=true; user=true; stop(); try{ st.setPointerCapture(drag.id); }catch(_){}
      drag.c=nextColor(); drag.was=cur&&cur!==orig(); drag.b=1-front; label(drag.c); prep(T[drag.b],drag.c,true); T[drag.b].style.zIndex=3; T[front].style.zIndex=2; T[drag.b].classList.add("on");
      if(!drag.was) neuSweep(true); st.classList.add("painted","sweeping"); }
    setX(Math.max(0,Math.min(100,(e.clientX-r.left)/r.width*100))); });
  function end(ok){ if(!drag) return; var d=drag; drag=null; if(!d.on) return; var x=parseFloat(st.style.getPropertyValue("--x"))||0;
    if(ok && x>40){ TZ.color=d.c; TZ.colorTouched=true; anim=tzTween(x,100,Math.max(160,(100-x)*7),setX,function(){ settle(d.b,d.c); updateBar(); }); }
    else anim=tzTween(x,0,300,setX,function(){ T[d.b].classList.remove("on"); st.classList.remove("sweeping"); if(!d.was){ st.classList.remove("painted"); neuSweep(false); } label(cur||orig()); anim=null; }); }
  st.addEventListener("pointerup",function(){ end(true); }); st.addEventListener("pointercancel",function(){ end(false); });
  var c0=TZ.colorTouched&&TZ.color?TZ.color:orig(); if(c0!==orig()) paint(c0,false); else { label(c0); cur=c0; }
  if(S.tier!=="C" && !TZ.colorTouched) tzInView(st,function(){ var seq=["gul","gece","kiraz"].filter(function(i){ return i!==orig(); }).concat([orig()]), k=0;
    (function step(){ if(user||!st.isConnected) return; var id=seq[k++]; paint(id,id!==orig()); if(k<seq.length) TZ.timers.push(setTimeout(step,1700)); })(); },.5); }

/* ---------- T3: Gerçek Kartela ---------- */
function tzKartela(el){ var pick=$(".tz-kpick",el), ks=$$(".tz-ks",el);
  ks.forEach(function(b){ b.setAttribute("aria-pressed","false"); b.addEventListener("click",function(){ ks.forEach(function(x){ x.setAttribute("aria-pressed",x===b); });
    TZ.ton=b.dataset.n+" ("+b.dataset.r+". sıra)"; pick.style.setProperty("--c",b.style.getPropertyValue("--c")); $("b",pick).textContent=b.dataset.n; $("small",pick).textContent=b.dataset.r+". sıra · salondaki kartela";
    pick.classList.remove("on"); void pick.offsetWidth; pick.classList.add("on"); if(navigator.vibrate) try{ navigator.vibrate(6); }catch(_){} updateBar(); }); }); }

/* ---------- T5: Hijyen Yolculuğu (sticky, four steps) ---------- */
function tzHijyen(sec){ var imgs=$$(".tz-hij-img",sec), lis=$$(".tz-hij-steps li",sec), bar=$(".tz-hij-bar i",sec), cur=0;
  function set(k){ if(k===cur) return; cur=k; imgs.forEach(function(im,i){ im.classList.toggle("on",i===k); }); lis.forEach(function(li,i){ li.classList.toggle("on",i===k); }); }
  function update(){ if(!sec.isConnected||S.tier==="C") return; var r=sec.getBoundingClientRect(), vh=innerHeight; if(r.bottom<0||r.top>vh) return;
    var p=Math.min(1,Math.max(0,-r.top/Math.max(1,r.height-vh))); bar.style.width=(p*100).toFixed(1)+"%"; set(Math.min(imgs.length-1,Math.floor(p*imgs.length*.999))); }
  TZ.scrollers.push(update); update(); }

/* ---------- T6: Tasarım duvarı ---------- */
function tzWall(sec){ var bs=$$("[data-tz-f]",sec), items=$$(".tz-w",sec), cap=TZ.pg.code==="model"?items.length:12, more=null, all=false;
  function show(f){ var k=0; items.forEach(function(it){ var ok=!f || (" "+it.dataset.tags+" ").indexOf(" "+f+" ")>=0; if(ok) k++; it.hidden=!ok || (!f && !all && k>cap); });
    if(more) more.hidden=!!f||all; }
  if(items.length>cap){ more=document.createElement("div"); more.className="tz-more"; more.innerHTML='<button class="btn-line" data-tz-place="duvar-tumu">Tüm modeller ('+items.length+')</button>';
    sec.appendChild(more); $("button",more).addEventListener("click",function(){ all=true; show(""); }); }
  bs.forEach(function(b){ b.addEventListener("click",function(){ var f=b.dataset.tzF; bs.forEach(function(x){ x.setAttribute("aria-pressed",x===b); }); show(f); }); });
  show(""); }

/* ---------- T7: Şekil / uzunluk ---------- */
function tzSekil(sec){ var mode=sec.getAttribute("data-tz-arg")||"", st=$("[data-tz-sekil-stage]",sec), bs=$$("[data-tz-sekil]",sec);
  if(mode==="uzunluk"){ $(".tz-sekil-eb",sec).textContent="Uzunluk seçici"; $(".tz-sekil-h2",sec).innerHTML="Ne kadar <em>uzun</em>?";
    bs.forEach(function(b){ if(b.dataset.tzSekil==="badem") b.hidden=true; else b.textContent=b.dataset.u; }); }
  function pick(k,byUser){ $$("img",st).forEach(function(i){ i.classList.toggle("on",i.dataset.look===k); }); bs.forEach(function(b){ b.setAttribute("aria-pressed",b.dataset.tzSekil===k); }); S.shape=k;
    if(byUser){ var b=bs.filter(function(x){ return x.dataset.tzSekil===k; })[0]; if(mode==="uzunluk") TZ.uzunluk=b.dataset.u; updateBar(); } }
  bs.forEach(function(b){ b.addEventListener("click",function(){ pick(b.dataset.tzSekil,true); }); });
  pick(SHAPES[S.shape]&&!(mode==="uzunluk"&&S.shape==="badem")?S.shape:"uzun"); }

/* ---------- T10: Söz ---------- */
function tzQuotes(box){ box.innerHTML=(TZ_QUOTES[box.dataset.tzQuotes]||[]).map(function(q){ var r=TZ_REVIEWS.filter(function(v){ return v.n===q[0]; })[0], at=r.t.indexOf(q[1]);
  var pre=at>0?"…":"", post=at+q[1].length<r.t.length?"…":"";
  return '<figure class="tz-q"><blockquote>'+pre+tzEsc(q[1])+post+'</blockquote><figcaption><b>'+tzEsc(r.n)+'</b> · '+months(r.d)+' · Google</figcaption></figure>'; }).join(""); }
function tzReviews(box){ var tag=box.dataset.tzRv, list=TZ_REVIEWS.filter(function(r){ return !tag||r.tags.indexOf(tag)>=0; }); if(!list.length) return;
  var tr=document.createElement("div"); tr.className="rv-track"; tr.style.setProperty("--dur",(list.length*9)+"s");
  var html=list.map(function(r){ return '<article class="rv"><span class="st" aria-label="5 yıldız">★★★★★</span><p>'+tzEsc(r.t)+'</p><footer><b>'+tzEsc(r.n)+'</b><span>'+months(r.d)+' · Google</span></footer></article>'; }).join("");
  tr.innerHTML=html+html.replace(/<article class="rv">/g,'<article class="rv" aria-hidden="true">'); box.appendChild(tr); }

/* ---------- inline invitation (protez-tirnak-randevu): the planner, laid out on the page ---------- */
function tzInline(box){ var body=$(".tz-inline-body",box), plan=PLANS[TZ.pg.fam], st={opt:TZ.pg.opt||plan.opts[0].id,shape:(SHAPES[S.shape]||SHAPES.uzun).n,day:0,time:null}, slots=sampleSlots("tirnak"), code=visitCode(), c="at-tz-"+TZ.pg.code+"-davetiye-";
  function render(){ var o=plan.opts.filter(function(x){ return x.id===st.opt; })[0], d=slots[st.day]; if(d&&(!st.time||d.times.indexOf(st.time)<0)) st.time=d.times[0];
    var bk=tzBakim(o,d,plan.shapes?4:3), msg=tzMsg(o,d,st.time,plan.shapes?st.shape:null,code), n=1;
    var h='<div class="pstep"><span class="eyebrow"><i>'+(n++)+'</i> İşlem</span><div class="opts">'+plan.opts.map(function(x){ return '<button class="opt" data-o="'+x.id+'" aria-pressed="'+(x.id===st.opt)+'" data-track-label="'+c+'islem"><span class="rad"></span><span class="nm">'+x.n+(x.b?'<span class="badge">'+x.b+'</span>':'')+'<small>'+(x.d?x.d+' dk':(x.s||''))+'</small></span><span class="pr">'+(x.ps||fmtTL(x.p))+'</span></button>'; }).join("")+'</div></div>';
    if(plan.shapes) h+='<div class="pstep"><span class="eyebrow"><i>'+(n++)+'</i> Şekil</span><div class="shapes">'+plan.shapes.map(function(s){ return '<button data-s="'+s+'" aria-pressed="'+(s===st.shape)+'" data-track-label="'+c+'sekil">'+s+'</button>'; }).join("")+'</div></div>';
    h+='<div class="pstep"><span class="eyebrow"><i>'+(n++)+'</i> Gün ve saat</span><div class="days">'+slots.map(function(x,i){ return '<button data-d="'+i+'" aria-pressed="'+(i===st.day)+'" data-track-label="'+c+'gun">'+x.label+'</button>'; }).join("")+'</div>'+
      '<div class="times">'+(d?d.times.map(function(t){ return '<button data-t="'+t+'" aria-pressed="'+(t===st.time)+'" data-track-label="'+c+'saat">'+t+'</button>'; }).join(""):"")+'</div><span class="slot-note">Prototipte örnek saatler; canlıda randevu sistemindeki boş saatler gelir. Kesin onayı ekibimiz WhatsApp\'ta verir.</span></div>';
    if(bk){ h+=bk; n++; }
    h+='<div class="pstep"><span class="eyebrow"><i>'+(n++)+'</i> Mesajınız</span><div class="bubble"><span>'+tzEsc(msg)+'</span><small>şimdi</small></div>'+
      '<div class="send-row"><a class="btn-gold shine" href="'+waHref(msg)+'" target="_blank" rel="noopener" data-track-label="'+c+'wa"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M3 20l1.4-4.2A8.5 8.5 0 1 1 7.6 19L3 20z"/></svg><span class="lbl">WhatsApp\'ta gönder</span></a><span class="fineprint">Mesaj hazır; göndermek size kalır.</span></div></div>';
    body.innerHTML=h; tzBakimBind(body,render,c+"bakim");
    $$("[data-o]",body).forEach(function(b){ b.addEventListener("click",function(){ st.opt=b.dataset.o; render(); }); });
    $$("[data-s]",body).forEach(function(b){ b.addEventListener("click",function(){ st.shape=b.dataset.s; render(); }); });
    $$("[data-d]",body).forEach(function(b){ b.addEventListener("click",function(){ st.day=+b.dataset.d; st.time=null; render(); }); });
    $$("[data-t]",body).forEach(function(b){ b.addEventListener("click",function(){ st.time=b.dataset.t; render(); if(navigator.vibrate) try{ navigator.vibrate(8); }catch(_){} }); });
    relead(); }
  render(); }

/* ---------- T9: Bakım saati (drawing, representative) ---------- */
function tzSaat(el){ var r=$("input",el), plate=$(".s-plate",el), w=$(".s-w",el);
  function set(){ var k=+r.value; plate.style.transform="translateY("+(-k*6)+"px)"; w.textContent=k+". hafta"; el.classList.toggle("due",k>=TZ_BAKIM_HAFTA); }
  r.addEventListener("input",set); set(); }
(function(){ var sel=$("#tzSel"); if(sel) sel.addEventListener("change",function(){ hideProto(); go(sel.value==="tirnak"?"tirnak":"tirnak/"+sel.value); }); })();
