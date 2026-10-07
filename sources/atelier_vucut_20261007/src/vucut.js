/* ---------- VÜCUT: bölgesel incelme ailesi (9 sayfa) ----------
   Sahip kararları 2026-10-07: siyah silindir başlıklı cihaz = G5; kule cihaz = Slim Tone; bölgesel incelme
   programında Slim Tone + G5 + lenf drenaj birlikte kullanılır. Kendi çekimi olmayan sayfalarda temsilî
   görsel ya da çizim durur ve sayfada açıkça yazılır. Önce/sonra fotoğrafı yalnızca programın sayfalarında,
   programın sonucu olarak gösterilir. Sayfalar boot'ta bu veriden kurulur; görünüm kimliği kısa koddur
   (vucut, slimtone, g5...), canlı slug NAV'da durur. */
/*__VB_SVG__*/
var VM="m/ig/", VB_IG="https://www.instagram.com/p/DMxmJ7QshoE/";
var VB_ZOOM='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="6"/><path d="M20 20l-4.5-4.5M11 8v6M8 11h6"/></svg>';
var VB_ARROW='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M13 6l6 6-6 6"/></svg>';
var VB_WA='<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2a8.2 8.2 0 0 1-4.2-1.1l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.7.8-.8 1-.3.2-.6.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.3-.4.7-1.4.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 2.9 2.9 0 0 0-.9 2.2 5.1 5.1 0 0 0 1.1 2.7 11.6 11.6 0 0 0 4.4 3.9c1.7.7 2.3.7 3.1.6a2.7 2.7 0 0 0 1.8-1.2 2.2 2.2 0 0 0 .2-1.2c-.1-.1-.3-.2-.5-.3z"/></svg>';
var VB_MEDIA={
 split:{img:VM+"vucut-cift-tam-960.webp",alt:"Bölgesel incelme programı: kol arkası ve göbek, solda önce, sağda sonra; aynı danışan"},
 g5:{mp4:VM+"vucut-g5.mp4",poster:VM+"vucut-g5-poster.webp",alt:"Bacak arkasında G5 masajı, salonumuzda çekildi"},
 stk:{mp4:VM+"vucut-slimtone-kol.mp4",poster:VM+"vucut-slimtone-kol-poster.webp",alt:"Kol arkasında Slim Tone uygulaması, salonumuzda çekildi"},
 sty:{mp4:VM+"vucut-slimtone-yuz.mp4",poster:VM+"vucut-slimtone-yuz-poster.webp",alt:"Slim Tone yüz başlığıyla uygulama, salonumuzda çekildi"},
 lenf:{mp4:VM+"vucut-lenf.mp4",poster:VM+"vucut-lenf-poster.webp",alt:"Lenf drenaj giysileri uygulama odamızda"},
 stc:{img:VM+"vucut-slimtone-cihaz-720.webp",alt:"Salonumuzdaki Slim Tone cihazı: ekran ve başlıklar"}
};
var VB_TRIO=[["slimtone","Slim Tone","stk","Kol arkasında uygulama, salonumuzda."],
             ["g5","G5 masajı","g5","Bacak arkasında uygulama, salonumuzda."],
             ["lenf","Lenf drenaj","lenf","Giysili drenaj, ayrı uygulama odamızda."]];
var VB_REG=[["kol","Kol arkası"],["gobek","Göbek"],["bel","Bel ve yanlar"],["popo","Popo"],["bacak","Bacak ve basen"]];
var VB_NOGAR=["Sonuç garanti mi?","Hayır. Aynı programla bile sonuç kişiden kişiye değişir; beslenme ve günlük hareket de sonucu etkiler."];
var VB_PRICE=["Fiyatı ne kadar?","Program, bölgeye ve seans sayısına göre kişiye özel hazırlanır. Fiyatı ön görüşmede, planla birlikte iletiriz."];
var VB_HOW_GEN={h:"Görüşme, plan, seans.",steps:[["Görüşürüz","Beklentinizi ve uygunluğunuzu birlikte değerlendiririz."],["Planlarız","Seans sayısı ve aralığı size göre belirlenir."],["Uygularız","Seanslar uygulama odamızda, uzmanınızla yapılır."]]};
var VUCUT_PAGES=[
 {id:"vucut",nav:"Bölgesel incelme",opt:"program",svc:"Bölgesel incelme programı · Slim Tone + G5 + lenf drenaj",
  h1:"Ankara Bölgesel <em>İncelme</em>",lede:"Slim Tone, G5 ve lenf drenaj, tek programda.",chip:"Kişiye özel program",
  hero:{kind:"split",m:"split"},
  note:"Aynı danışan: solda önce, sağda sonra. Programda Slim Tone, G5 ve lenf drenaj birlikte kullanıldı; sonuç kişiden kişiye değişir. Fotoğraf Instagram hesabımızda paylaşıldı.",
  map:true,proof:true,trio:"hub",reviews:true,inv:"Önce görüşelim, sonra planlayalım.",
  how:{h:"Görüşme, plan, seans.",steps:[["Görüşürüz","Bölgeyi, beklentinizi ve uygunluğunuzu birlikte değerlendiririz."],["Planlarız","Slim Tone, G5 ve lenf drenajın seans sayısı ve sırası bölgeye göre belirlenir."],["Seanslar başlar","İlerlemeyi uzmanınızla birlikte takip edersiniz."]]},
  faq:[["Kaç seans gerekir?","Bölgeye ve hedefinize göre değişir. Seans sayısını ön görüşmede uzmanınız planlar."],VB_NOGAR,["Fotoğraflar gerçek mi?","Evet. Önce ve sonra fotoğrafları salonumuzda çalıştığımız bir danışana ait; Instagram hesabımızda paylaşıldı."],VB_PRICE]},
 {id:"slimtone",nav:"Slim tone",opt:"slimtone",svc:"Slim Tone",
  h1:"Ankara Slim <em>Tone</em>",lede:"Bölgesel incelme programımızın cihazı.",chip:"Ön görüşme",
  hero:{kind:"video",m:"stk",cap:"Salonumuzda çekildi"},
  note:"Salonumuzdaki Slim Tone cihazıyla kol arkası uygulaması. Bölgesel incelme programında G5 ve lenf drenajla birlikte kullanılır.",
  duo:true,proof:true,trio:"member",inv:"Slim Tone için ön görüşme.",
  how:{h:"Bölge, başlık, program.",steps:[["Bölge belirlenir","Ön görüşmede uygulanacak bölgeleri birlikte seçeriz."],["Başlık uygulanır","Uzmanınız Slim Tone başlığını seçilen bölge üzerinde gezdirir."],["Programla tamamlanır","Bölgesel incelme programında G5 ve lenf drenajla birlikte planlanır."]]},
  faq:[["Slim Tone tek başına uygulanır mı?","Bölgesel incelme programımızda G5 ve lenf drenajla birlikte kullanılır. Bölgenize göre planı uzmanınız yapar."],["Yüze de uygulanıyor mu?","Yüz başlığıyla yapılan uygulamayı yukarıdaki videoda görebilirsiniz. Size uygunluğunu ön görüşmede değerlendiririz."],VB_NOGAR,VB_PRICE]},
 {id:"g5",nav:"G5 masajı",opt:"g5",svc:"G5 masajı",
  h1:"Ankara G5 <em>Masajı</em>",lede:"Uzman elinde, G5 cihazıyla.",chip:"Ön görüşme",
  hero:{kind:"video",m:"g5",cap:"Salonumuzda çekildi"},
  note:"Salonumuzdaki G5 cihazıyla bacak arkası uygulaması. Bölgesel incelme programında Slim Tone ve lenf drenajla birlikte kullanılır.",
  proof:true,trio:"member",inv:"G5 masajı için ön görüşme.",
  how:{h:"Hazırlık, masaj, program.",steps:[["Bölge hazırlanır","Uygulama bölgesi masaj yağıyla hazırlanır."],["G5 uygulanır","Uzmanınız G5 başlığını bölge üzerinde gezdirir."],["Programla devam edilir","Bölgesel incelme programında Slim Tone ve lenf drenajla birlikte planlanır."]]},
  faq:[["Hangi bölgelere uygulanır?","Videoda bacak arkasında görüyorsunuz. Uygulanacak bölgeleri ön görüşmede birlikte belirleriz."],VB_NOGAR,VB_PRICE]},
 {id:"lenf",nav:"Lenf drenaj",opt:"lenf",svc:"Lenf drenaj",
  h1:"Ankara Lenf <em>Drenaj</em>",lede:"Giysili drenaj, ayrı bir odada.",chip:"Ön görüşme",
  hero:{kind:"video",m:"lenf",cap:"Uygulama odamız"},
  note:"Lenf drenaj giysilerimiz uygulama odamızda. Bölgesel incelme programında Slim Tone ve G5 ile birlikte kullanılır.",
  proof:true,trio:"member",inv:"Lenf drenaj için ön görüşme.",
  how:{h:"Giysi, uzanma, program.",steps:[["Giysi seçilir","Bacak ve kol bölmeli giysilerden bölgenize uygun olanı kullanılır."],["Uzanırsınız","Seans boyunca uygulama yatağında uzanırsınız."],["Programla devam edilir","Bölgesel incelme programında Slim Tone ve G5 ile birlikte planlanır."]]},
  faq:[["Ayrı bir odada mı yapılıyor?","Evet. Lenf drenaj ayrı uygulama odamızda yapılır."],VB_NOGAR,VB_PRICE]},
 {id:"em",nav:"EM vücut bakımı",opt:"em",svc:"EM vücut bakımı",
  h1:"Ankara EM Vücut <em>Bakımı</em>",lede:"Bölgenize göre planlanan cihaz seansı.",chip:"Ön görüşme",
  hero:{kind:"still",m:"stc",cap:"Görselde: Slim Tone cihazımız"},tag:"Temsilî görsel",
  note:"Görselde salonumuzdaki Slim Tone cihazı yer alıyor. Bu bakımın kendi çekimi hazırlanıyor.",
  link:true,trio:"other",inv:"EM vücut bakımı için ön görüşme.",how:VB_HOW_GEN,
  faq:[["Bölgesel incelme programıyla birlikte yapılır mı?","Uygunluğunu ve sırasını ön görüşmede uzmanımız değerlendirir."],VB_NOGAR,VB_PRICE]},
 {id:"heykeltras",nav:"Heykeltraş",opt:"heykeltras",svc:"Heykeltraş",
  h1:"Ankara <em>Heykeltraş</em>",lede:"Bölgenize göre planlanan seans.",chip:"Ön görüşme",
  hero:{kind:"still",m:"g5",cap:"Görselde: G5 uygulaması"},tag:"Temsilî görsel",
  note:"Görselde salonumuzdaki G5 uygulaması yer alıyor. Heykeltraş uygulamasının kendi çekimi hazırlanıyor.",
  link:true,trio:"other",inv:"Heykeltraş için ön görüşme.",how:VB_HOW_GEN,
  faq:[["Bölgesel incelme programıyla birlikte yapılır mı?","Uygunluğunu ve sırasını ön görüşmede uzmanımız değerlendirir."],VB_NOGAR,VB_PRICE]},
 {id:"pasif",nav:"Pasif jimnastik",opt:"pasif",svc:"Pasif jimnastik",
  h1:"Ankara Pasif <em>Jimnastik</em>",lede:"Pedler yerleştirilir, siz uzanırsınız.",chip:"Ön görüşme",
  hero:{kind:"art",art:"pasif",cap:"Ped yerleşimi · temsilî çizim"},tag:"Temsilî çizim",
  note:"Çizim, pedlerin göbek ve bacağa yerleşimini temsil eder. Uygulamanın kendi çekimi hazırlanıyor.",
  link:true,trio:"other",inv:"Pasif jimnastik için ön görüşme.",
  how:{h:"Görüşme, ped, seans.",steps:[["Görüşürüz","Beklentinizi ve uygunluğunuzu birlikte değerlendiririz."],["Pedler yerleştirilir","Pedler, çalışılacak bölgelere uzmanınız tarafından yerleştirilir."],["Uzanırsınız","Seans boyunca uygulama yatağında uzanırsınız."]]},
  faq:[["Bölgesel incelme programıyla birlikte yapılır mı?","Uygunluğunu ve sırasını ön görüşmede uzmanımız değerlendirir."],VB_NOGAR,VB_PRICE]},
 {id:"catlak",nav:"Çatlak görünümü bakımı",opt:"catlak",svc:"Çatlak görünümü bakımı",
  h1:"Çatlak Görünümü <em>Bakımı</em>",lede:"İnce Ton protokolü, bölgenize göre.",chip:"Ön görüşme",
  hero:{kind:"art",art:"catlak",cap:"Temsilî çizim"},tag:"Temsilî çizim",
  note:"Görsel temsilî bir çizimdir. Bakımın uygulama çekimi hazırlanıyor.",
  link:true,trio:"other",inv:"Çatlak görünümü bakımı için ön görüşme.",
  how:{h:"Bakarız, planlarız, uygularız.",steps:[["Bölgeye bakarız","Çatlakların bölgesini ve görünümünü birlikte değerlendiririz."],["Protokolü planlarız","Seans sayısı ve aralığı bölgenize göre belirlenir."],["Uygularız","Seanslar uygulama odamızda, uzmanınızla yapılır."]]},
  faq:[["Çatlaklar tamamen geçer mi?","Bunu söylemek doğru olmaz. Bakımın amacı görünümü desteklemektir; sonuç kişiden kişiye değişir."],VB_PRICE]},
 {id:"popo",nav:"Popo bakımı",opt:"popo",svc:"Popo bakımı",
  h1:"Ankara Popo <em>Bakımı</em>",lede:"Bölgenize göre planlanan bakım.",chip:"Ön görüşme",
  hero:{kind:"video",m:"g5",cap:"Görselde: bacak arkasında G5"},tag:"Temsilî görsel",
  note:"Görselde salonumuzdaki G5 uygulaması yer alıyor. Popo bakımının kendi çekimi hazırlanıyor.",
  link:true,trio:"other",inv:"Popo bakımı için ön görüşme.",how:VB_HOW_GEN,
  faq:[["Bölgesel incelme programıyla birlikte yapılır mı?","Uygunluğunu ve sırasını ön görüşmede uzmanımız değerlendirir."],VB_NOGAR,VB_PRICE]}
];
var VUCUT_BY={}, VBM={sel:[],code:null};

function vbVideo(m,cls){ return '<video class="auto-vid'+(cls?" "+cls:"")+'" muted playsinline loop preload="none" poster="'+m.poster+'" data-src="'+m.mp4+'" aria-label="'+m.alt+'"></video>'; }
function vbHero(p){ var h=p.hero, m=VB_MEDIA[h.m]||{}, tag=p.tag?'<span class="tile-tag">'+p.tag+'</span>':'', cap=h.cap?'<span class="vb-cap">'+h.cap+'</span>':'';
  if(h.kind==="split") return '<div class="vb-split" data-vb-split><img src="'+m.img+'" alt="'+m.alt+'" width="960" height="1200" fetchpriority="high"><i class="seam"></i><span class="cmp-tag b">Önce</span><span class="cmp-tag a">Sonra</span><canvas class="dust" data-dust></canvas><button class="zoom-btn" data-zoom="'+m.img+'" aria-label="Fotoğrafı yakından görün">'+VB_ZOOM+'</button></div>';
  if(h.kind==="video") return '<div class="vb-stage">'+tag+vbVideo(m)+'<canvas class="dust" data-dust></canvas>'+cap+'</div>';
  if(h.kind==="still") return '<div class="vb-stage kb">'+tag+'<img src="'+(m.img||m.poster)+'" alt="'+m.alt+'" fetchpriority="high"><canvas class="dust" data-dust></canvas>'+cap+'</div>';
  return '<div class="vb-stage vb-art" role="img" aria-label="'+(h.cap||"Temsilî çizim")+'">'+tag+VB_SVG[h.art]+cap+'</div>'; }
function vbMap(){ return '<div class="sec gutter"><div class="regions vb-map" data-vb-map>'+
  '<div class="sec-head" style="margin:0"><span class="eyebrow">Bölge haritası</span><h2>Hangi <em>bölge</em> için geliyorsunuz?</h2><p>Silüette ya da listede bölgeye dokunun. Programı ön görüşmede bu bölgelere göre planlarız.</p></div>'+
  '<div class="vb-figs"><figure class="vb-fig">'+VB_SVG.on+'<figcaption>Ön</figcaption></figure><figure class="vb-fig">'+VB_SVG.arka+'<figcaption>Arka</figcaption></figure></div>'+
  '<div class="vb-ctl" style="display:grid;gap:14px"><div class="rg-chips" data-vb-chips role="group" aria-label="Bölgeler"></div><div class="rg-sum" data-vb-sum></div><div class="vb-sug" data-vb-sug hidden></div>'+
  '<div class="rg-actions"><a class="btn-gold shine" data-vb-wa href="https://wa.me/'+WA+'" target="_blank" rel="noopener" data-track-label="at-vucut-harita-wa">'+VB_WA+'<span class="lbl">WhatsApp\'tan ön görüşme iste</span></a><button class="btn-line" data-plan="vucut">Saat de seçeyim</button></div>'+
  '<p class="hero-note">Mesaj hazır; göndermek size kalır.</p></div></div></div>'; }
function vbTrio(p){ var head=p.trio==="hub"?["Program","Üç cihaz, <em>tek</em> program.","Bölgesel incelme seanslarımızda Slim Tone, G5 ve lenf drenaj birlikte kullanılır. Hangisinin ne kadar uygulanacağını bölgeye göre uzmanınız belirler."]:
   (p.trio==="member"?["Bölgesel incelme programı","Programın <em>üç</em> parçası.","Bu bakım, bölgesel incelme programımızın bir parçası. Diğer iki uygulamayı da salonumuzda çektik."]:
   ["Salonumuzda","Vücut <em>cihazlarımız</em>.","Bölgesel incelme programımızda kullandığımız üç uygulama; hepsi salonumuzda çekildi."]);
  return '<div class="sec dark-band gutter"><div class="sec-head"><span class="eyebrow">'+head[0]+'</span><h2>'+head[1]+'</h2><p>'+head[2]+'</p></div><div class="vb-trio">'+
   VB_TRIO.map(function(t){ var here=t[0]===p.id, m=VB_MEDIA[t[2]];
     return '<article class="vb-card'+(here?' here':'')+'">'+vbVideo(m)+(here?'<span class="tile-tag">Buradasınız</span>':'')+'<div class="tx"><b>'+t[1]+'</b><span>'+t[3]+'</span>'+(here?'':'<a class="btn-line" href="#'+t[0]+'" data-go="'+t[0]+'">Sayfayı açın →</a>')+'</div></article>'; }).join("")+'</div></div>'; }
function vbProof(){ return '<div class="sec gutter"><div class="sec-head"><span class="eyebrow">Gerçek sonuç · bölgesel incelme programı</span><h2>Basılı tutun, <em>öncesini</em> görün.</h2><p>Aynı danışanın fotoğrafları, Instagram hesabımızdan. Programda Slim Tone, G5 ve lenf drenaj birlikte kullanıldı. Sonuç kişiden kişiye değişir.</p></div>'+
  '<div class="gal" data-vb-gal></div><div class="vb-actions"><button class="btn-line" data-zoom="'+VB_MEDIA.split.img+'">Orijinal paylaşımı açın</button><a class="btn-line" href="'+VB_IG+'" target="_blank" rel="noopener">Instagram\'da görün →</a></div></div>'; }
function vbDuo(){ return '<div class="sec dark-band gutter"><div class="sec-head"><span class="eyebrow">Cihazımız</span><h2>Slim Tone ve <em>başlıkları</em>.</h2><p>Salonumuzdaki cihaz; vücut başlıkları ve yüz başlığıyla.</p></div><div class="vb-duo">'+
  '<figure><img src="'+VB_MEDIA.stc.img+'" alt="'+VB_MEDIA.stc.alt+'" loading="lazy" width="720" height="900"><figcaption>Slim Tone cihazımız</figcaption></figure>'+
  '<figure>'+vbVideo(VB_MEDIA.sty)+'<figcaption>Yüz başlığıyla uygulama</figcaption></figure></div></div>'; }
function vbLink(){ return '<div class="sec gutter"><div class="sec-head"><span class="eyebrow">Gerçek sonuç</span><h2>Bölgesel incelme <em>programımız</em>.</h2><p>Slim Tone, G5 ve lenf drenajı birlikte kullandığımız programın önce ve sonra fotoğrafları kendi sayfasında.</p></div>'+
  '<a class="vb-link" href="#vucut" data-go="vucut"><img src="'+VM+'vucut-gobek-sonra-480.webp" alt="Bölgesel incelme programı sonrası göbek" loading="lazy" width="480" height="390"><span><small>Önce ve sonra</small><b>Bölgesel incelme</b><i>Slim Tone · G5 · lenf drenaj</i></span></a></div>'; }
function vbPage(p){ var h='<div class="hero"><div class="hero-split"><div class="hero-media lit">'+vbHero(p)+'</div><div class="hero-copy"><span class="eyebrow" data-personal>Konutkent · Çankaya</span><h1>'+p.h1+'</h1><p class="lede">'+p.lede+'</p>'+
   '<div class="chips"><span class="chip chip-in"><span class="star">★</span> 4,6 · 263 yorum</span><span class="chip chip-in price" style="animation-delay:.08s">'+p.chip+'</span><span class="chip chip-in" style="animation-delay:.16s" data-slot-chip="'+p.id+'"><span class="dot"></span> <span>Bugün müsait</span></span></div>'+
   '<div class="rings" data-rings="vucut"></div><p class="hero-note">'+p.note+'</p></div></div></div>';
  if(p.map) h+=vbMap();
  if(p.duo) h+=vbDuo();
  if(p.proof) h+=vbProof();
  if(p.link) h+=vbLink();
  h+=vbTrio(p);
  h+='<div class="live" data-live="'+p.id+'"></div>';
  h+='<div class="sec gutter"><div class="invite-teaser"><span class="eyebrow">Randevu davetiyesi</span><h3>'+p.inv+'</h3><div class="steps-mini"><span>1 · Bakım</span><span>2 · Gün ve saat</span><span>3 · Davetiye → WhatsApp</span></div><button class="btn-gold shine" data-plan="'+p.id+'"><span class="lbl">Davetiyemi hazırla</span>'+VB_ARROW+'</button></div></div>';
  if(p.reviews) h+='<div class="sec gutter" style="padding-top:0"><div class="sec-head"><span class="eyebrow">Salonumuz için yazılanlar</span><h2>“Kendimi iyi hissettiğim bir yer.”</h2><p>Google\'daki beş yıldızlı yorumlardan seçildi.</p></div></div><div class="reviews" data-reviews="salon"></div>';
  h+='<div class="sec gutter"><div class="two"><div class="menu-card"><span class="eyebrow">'+p.nav+'</span><h3>Fiyat neden yazmıyor?</h3><p class="muted" style="text-align:center;margin:0 0 6px">Program; bölgeye, seans sayısına ve hedefinize göre kişiye özel hazırlanır. Planı ve fiyatı ön görüşmede birlikte netleştiririz.</p><p class="menu-src">Fiyat ön görüşmede, programla birlikte iletilir.</p></div>'+
   '<div><div class="sec-head" style="margin-bottom:16px"><span class="eyebrow">Nasıl geçer</span><h2 style="font-size:40px">'+p.how.h+'</h2></div><ol class="how">'+p.how.steps.map(function(s){ return '<li><div><b>'+s[0]+'</b><p>'+s[1]+'</p></div></li>'; }).join("")+'</ol></div></div></div>';
  h+='<div class="sec gutter faq" style="padding-top:0"><div class="sec-head"><span class="eyebrow">Sık sorulanlar</span><h2>Aklınızdakiler</h2></div>'+p.faq.map(function(f){ return '<details><summary>'+f[0]+'</summary><p>'+f[1]+'</p></details>'; }).join("")+'</div>';
  return h+'<div class="sec gutter" data-visit style="padding-top:0"></div>'; }

function buildVucut(){ var main=$("main"); if(!main || $("main > [data-view='vucut']")) return;
  PLANS.vucut={title:"Vücut bakımı ön görüşmesi",custom:true,opts:VUCUT_PAGES.map(function(p){ return {id:p.opt,n:p.svc,p:null,d:null,s:p.id==="vucut"?"Bölgeye göre kişiye özel program":"Ön görüşmede planlanır"}; })};
  VUCUT_PAGES.forEach(function(p){ VUCUT_BY[p.id]=p; PLANS[p.id]=PLANS.vucut; S.planOpt[p.id]=p.opt; BAR[p.id]="Ön görüşme · saatimi seç";
    var s=document.createElement("section"); s.setAttribute("data-view",p.id); s.hidden=true; s.innerHTML=vbPage(p); main.appendChild(s); });
  STORIES.vucut=[
   {t:"Önce / Sonra",th:VM+"vucut-gobek-sonra-480.webp",fr:[{img:VB_MEDIA.split.img,fit:"contain",cap:"Solda önce, sağda sonra"},{img:VM+"vucut-gobek-yan-360.webp",fit:"contain",cap:"Yandan: üstte önce, altta sonra"}]},
   {t:"Slim Tone",th:VB_MEDIA.stk.poster,fr:[{video:VB_MEDIA.stk.mp4,poster:VB_MEDIA.stk.poster,cap:"Slim Tone · kol arkası"},{video:VB_MEDIA.sty.mp4,poster:VB_MEDIA.sty.poster,cap:"Slim Tone · yüz başlığı"}]},
   {t:"G5",th:VB_MEDIA.g5.poster,fr:[{video:VB_MEDIA.g5.mp4,poster:VB_MEDIA.g5.poster,cap:"G5 masajı"}]},
   {t:"Lenf drenaj",th:VB_MEDIA.lenf.poster,fr:[{video:VB_MEDIA.lenf.mp4,poster:VB_MEDIA.lenf.poster,cap:"Lenf drenaj odamız"}]},
   {t:"Fiyat",th:"m/monogram.png",fr:"price:vucut"}]; }

function vbNames(){ return VBM.sel.map(function(k){ return VB_REG.filter(function(r){ return r[0]===k; })[0][1].toLocaleLowerCase("tr-TR"); }).join(", "); }
function vbMsg(){ return "Merhaba, bölgesel incelme programı için ön görüşme almak istiyorum."+(VBM.sel.length?" Bölgeler: "+vbNames()+".":"")+" "+(VBM.code||(VBM.code=visitCode())); }
function initVbMap(sec){ var box=$("[data-vb-map]",sec); if(!box) return; var chips=$("[data-vb-chips]",box), NSx="http://www.w3.org/2000/svg";
  chips.innerHTML=VB_REG.map(function(r){ return '<button data-vb-rg="'+r[0]+'" aria-pressed="false" data-track-label="at-vucut-bolge">'+r[1]+'</button>'; }).join("");
  function ping(part){ if(!part || S.tier==="C") return; try{ var b=part.getBBox(), c=document.createElementNS(NSx,"circle");
    c.setAttribute("cx",(b.x+b.width/2).toFixed(1)); c.setAttribute("cy",(b.y+b.height/2).toFixed(1)); c.setAttribute("r",Math.max(6,Math.min(b.width,b.height)/2).toFixed(1)); c.setAttribute("class","vb-ping");
    part.ownerSVGElement.appendChild(c); setTimeout(function(){ c.remove(); },950); }catch(e){} }
  function toggle(k,part){ var i=VBM.sel.indexOf(k); if(i>=0) VBM.sel.splice(i,1); else { VBM.sel.push(k); ping(part); } sync(); if(navigator.vibrate) try{ navigator.vibrate(6); }catch(e){} }
  function sync(){ var n=VBM.sel.length;
    $$(".vb-part",box).forEach(function(p){ var on=VBM.sel.indexOf(p.getAttribute("data-part"))>=0; p.classList.toggle("on",on); p.setAttribute("aria-pressed",on); });
    $$("[data-vb-rg]",chips).forEach(function(b){ b.setAttribute("aria-pressed",VBM.sel.indexOf(b.dataset.vbRg)>=0); });
    $("[data-vb-sum]",box).textContent=n?(n+" bölge: "+vbNames()):"Bölge seçin; programınızı ön görüşmede birlikte planlayalım.";
    var sug=$("[data-vb-sug]",box); sug.hidden=!n;
    if(n) sug.innerHTML='<span class="eyebrow">Ön görüşmede konuşacağımız program</span><b>Slim Tone + G5 + lenf drenaj</b><span>Hangi uygulamanın ne kadar yapılacağını uzmanınız bölgeye göre belirler.</span><div class="chips">'+
      (VBM.sel.indexOf("popo")>=0?'<a class="chip" href="#popo" data-go="popo" data-track-label="at-vucut-oneri-git">Popo bakımı →</a>':'')+
      VB_TRIO.map(function(t){ return '<a class="chip" href="#'+t[0]+'" data-go="'+t[0]+'" data-track-label="at-vucut-oneri-git">'+t[1]+' →</a>'; }).join("")+'</div>';
    var a=$("[data-vb-wa]",box); a.href=waHref(vbMsg()); $(".lbl",a).textContent=n?"Bölgelerimi WhatsApp'ta gönder":"WhatsApp'tan ön görüşme iste"; }
  $$(".vb-part",box).forEach(function(p){ var k=p.getAttribute("data-part"); p.addEventListener("click",function(){ toggle(k,p); });
    p.addEventListener("keydown",function(e){ if(e.key==="Enter"||e.key===" "){ e.preventDefault(); toggle(k,p); } }); });
  $$(".vb-hit",box).forEach(function(h){ var k=h.getAttribute("data-hit"); h.addEventListener("click",function(){ toggle(k,$('.vb-part[data-part="'+k+'"]',h.ownerSVGElement)); }); });
  $$("[data-vb-rg]",chips).forEach(function(b){ b.addEventListener("click",function(){ var k=b.dataset.vbRg; toggle(k,$('.vb-part[data-part="'+k+'"]',box)); }); });
  sync(); }
function initVucut(v){ var sec=$("main > [data-view='"+v+"']"), p=VUCUT_BY[v]; if(!sec) return;
  initAutoVids(sec);
  var sp=$("[data-vb-split]",sec); if(sp) setTimeout(function(){ sp.classList.add("on"); },200);
  var g=$("[data-vb-gal]",sec);
  if(g){ card(g,VM+"vucut-kol-sonra-480.webp",VM+"vucut-kol-once-480.webp","Kol arkası"); g.lastChild.classList.add("vb");
    card(g,VM+"vucut-gobek-sonra-480.webp",VM+"vucut-gobek-once-480.webp","Göbek, önden"); g.lastChild.classList.add("vb");
    card(g,VM+"vucut-gobek-yan-360.webp",null,"Göbek, yandan"); g.lastChild.classList.add("vb-tall"); }
  if(p.map) initVbMap(sec); }
