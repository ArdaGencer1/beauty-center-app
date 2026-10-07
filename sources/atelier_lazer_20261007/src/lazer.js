/* ATELIER · FAZ L (2026-10-07) -- laser family interactions, shared by the live pages and the prototype.
   Markup comes from render.py; this file only adds behaviour.  Contact buttons stay real <a href="wa.me">
   / tel: links carrying data-track-label="at-<page>-<place>", so ads-tracking.js (contact-ping b=, SGB_VISIT
   tap, Ads conversion) and script.js (GA4) count them with no extra code.  The [W-] code comes only from
   window.SGBVisit.mark(); without it the message carries no code (ads-tracking adds it at click when allowed).
   No storage, no network except the public price-menu (minutes) and the media files. */
(function () {
  "use strict";
  if (window.ATLZ) return;
  var TR_DAYS = ["Pazar", "Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi"];
  var TR_MON = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"];
  var MON3 = ["Oca", "Şub", "Mar", "Nis", "May", "Haz", "Tem", "Ağu", "Eyl", "Eki", "Kas", "Ara"];
  var X = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 6l12 12M18 6L6 18"/></svg>';
  var WAI = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2a8.2 8.2 0 0 1-4.2-1.1l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2z"/></svg>';
  var TELI = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/></svg>';
  var DAYPARTS = [["sabah", "Sabah", "10.00–13.00", 13], ["ogle", "Öğle", "13.00–17.00", 17], ["aksam", "Akşam", "17.00–20.00", 20]];
  var PLANPREF = [["oneri", "Önerinizi bekliyorum"], ["tek", "Tek seans"], ["paket", "8 seans paket"], ["garanti", "Bitiş garantili paket"]];

  function $(s, r) { return (r || document).querySelector(s); }
  function $$(s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function low(s) { return String(s).toLocaleLowerCase("tr-TR"); }
  function relead() { try { if (typeof window.bindLeadTracking === "function") window.bindLeadTracking(); } catch (e) {} }
  function ist() {
    var p = {};
    try {
      new Intl.DateTimeFormat("en-GB", { timeZone: "Europe/Istanbul", year: "numeric", month: "2-digit", day: "2-digit", hour: "2-digit", minute: "2-digit", weekday: "short", hour12: false })
        .formatToParts(new Date()).forEach(function (x) { p[x.type] = x.value; });
    } catch (e) { var d = new Date(); return { y: d.getFullYear(), m: d.getMonth() + 1, d: d.getDate(), h: d.getHours(), min: d.getMinutes(), wd: d.getDay() }; }
    return { y: +p.year, m: +p.month, d: +p.day, h: +p.hour % 24, min: +p.minute, wd: { Sun: 0, Mon: 1, Tue: 2, Wed: 3, Thu: 4, Fri: 5, Sat: 6 }[p.weekday] };
  }
  function openState() {
    var t = ist(), m = t.h * 60 + t.min;
    if (t.wd === 1) return { open: false, txt: "Bugün kapalı · yarın 10.00" };
    if (m < 600) return { open: false, txt: "Bugün 10.00'da açılıyor" };
    if (m >= 1200) return { open: false, txt: t.wd === 0 ? "Salı 10.00'da açılıyor" : "Yarın 10.00'da açılıyor" };
    return { open: true, txt: "Şu an açık · 20.00'ye kadar" };
  }
  function detectTier() {
    try {
      if (matchMedia("(prefers-reduced-motion: reduce)").matches) return "C";
      var c = navigator.connection || {};
      if (c.saveData || /2g/.test(c.effectiveType || "")) return "C";
      var mem = navigator.deviceMemory || 8, cpu = navigator.hardwareConcurrency || 8;
      return (mem <= 2 || cpu <= 4) ? "B" : "A";
    } catch (e) { return "B"; }
  }

  function Page(root, host) {
    var self = this;
    this.root = root; this.host = host || {};
    var D = this.host.data;
    if (!D) { var js = document.getElementById("lz-data"); D = js ? JSON.parse(js.textContent) : null; }
    if (!D && window.ATLZ_DATA) D = window.ATLZ_DATA[root.getAttribute("data-lz-page")];
    this.D = D;
    this.code = D.code; this.g = D.g; this.side = "on";
    this.sel = []; this.tone = null; this.sens = false; this.start = 0; this.planPref = "oneri";
    this.tier = this.host.tier ? this.host.tier() : detectTier();
    root.setAttribute("data-lz-tier", this.tier);
    this.byId = {};
    ["kadin", "erkek"].forEach(function (g) { (D.regions[g] || []).forEach(function (r) { self.byId[g + ":" + r.id] = r; }); });
    this.initHero(); this.initRings(); this.initScroll(); this.initMap(); this.initJourney(); this.initCal(); this.initDevice();
    this.initReels(); this.initReviews(); this.initZoom(); this.initMenu(); this.initTone(); this.initQuick(); this.initFamily();
    if (!this.host.bar) this.initBar();
    this.sync();
    this.refreshMinutes();
  }
  var P = Page.prototype;

  P.vcode = function () {
    try { if (window.SGBVisit && typeof window.SGBVisit.mark === "function") { var c = window.SGBVisit.mark(); if (typeof c === "string" && /^\[W-[A-Z0-9]{6}\]$/.test(c)) return c; } } catch (e) {}
    return this.host.code ? this.host.code() : "";
  };
  P.wa = function (msg) { var c = this.vcode(); return "https://wa.me/" + this.D.wa + "?text=" + encodeURIComponent(msg + (c ? " " + c : "")); };
  P.lbl = function (el, place) { if (el) el.setAttribute("data-track-label", "at-" + this.code + "-" + place); return el; };

  /* ---------------- selection model ---------------- */
  P.reg = function (id) { return this.byId[this.g + ":" + id]; };
  P.has = function (k) { return this.sel.indexOf(k) >= 0; };
  P.name = function (k) { if (k.indexOf("pkg:") === 0) return k.slice(4); var r = this.reg(k); return r ? r.n : k; };
  P.mins = function (k) { var r = this.reg(k); return r && r.m ? r : null; };
  P.isFace = function (k) { return this.D.face.indexOf(k) >= 0; };
  P.toggle = function (k, on) {
    var i = this.sel.indexOf(k), want = on === undefined ? i < 0 : on;
    if (want && i < 0) {
      var r = this.reg(k);
      if (r && r.z === "pkg") this.sel = this.sel.filter(function (x) { return x.indexOf("pkg:") === 0; });
      else if (k.indexOf("pkg:") !== 0) this.sel = this.sel.filter(function (x) { var rr = this.reg(x); return !(rr && rr.z === "pkg"); }, this);
      if (k === "tum-kol") this.sel = this.sel.filter(function (x) { return x !== "yarim-kol"; });
      if (k === "yarim-kol") this.sel = this.sel.filter(function (x) { return x !== "tum-kol"; });
      if (k === "tum-bacak") this.sel = this.sel.filter(function (x) { return x !== "yarim-bacak"; });
      if (k === "yarim-bacak") this.sel = this.sel.filter(function (x) { return x !== "tum-bacak"; });
      if (k === "tum-yuz") this.sel = this.sel.filter(function (x) { return !this.isFace(x); }, this);
      else if (this.isFace(k)) this.sel = this.sel.filter(function (x) { return x !== "tum-yuz"; });
      this.sel.push(k);
    } else if (!want && i >= 0) this.sel.splice(i, 1);
    if (navigator.vibrate) try { navigator.vibrate(6); } catch (e) {}
    this.sync();
  };
  P.partClick = function (part, el) {
    var map = { "ust-kol": ["tum-kol", "yarim-kol"], "alt-kol": ["yarim-kol", "tum-kol"], "ust-bacak": ["tum-bacak", "yarim-bacak"], "alt-bacak": ["yarim-bacak", "tum-bacak"] };
    if (part === "yuz") { this.setSide("yuz"); return; }
    var target = part;
    if (map[part]) {
      var a = map[part][0], b = map[part][1];
      if (this.has(a) || this.has(b)) {
        if (part.indexOf("ust") === 0 && this.has(b)) { this.toggle(a, true); this.shot(el); return; }
        this.sel = this.sel.filter(function (x) { return x !== a && x !== b; }); this.sync(); return;
      }
      target = a;
    }
    if (!this.reg(target)) return;
    var was = this.has(target);
    this.toggle(target);
    if (!was) this.shot(el);
  };
  P.lit = function () {
    var on = {}, self = this, pp = this.D.pkgParts;
    this.sel.forEach(function (k) {
      if (k === "tum-kol") { on["ust-kol"] = on["alt-kol"] = 1; }
      else if (k === "yarim-kol") on["alt-kol"] = 1;
      else if (k === "tum-bacak") { on["ust-bacak"] = on["alt-bacak"] = 1; }
      else if (k === "yarim-bacak") on["alt-bacak"] = 1;
      else if (k === "tum-yuz") { on.yuz = 1; on["dudak-ustu"] = on.cene = on.gidi = on["sakal-ustu"] = on.kulak = 1; }
      else if (pp[k] === "all") on.all = 1;
      else if (pp[k]) pp[k].forEach(function (x) { on[x] = 1; });
      else on[k] = 1;
      if (self.isFace(k)) on.yuz = 1;
    });
    return on;
  };

  /* ---------------- message ---------------- */
  P.regText = function () {
    var self = this;
    if (!this.sel.length) return "";
    return this.sel.map(function (k) { return low(self.name(k)); }).join(", ") + " (" + (this.g === "kadin" ? "kadın" : "erkek") + ")";
  };
  P.extras = function () {
    var s = "";
    if (this.tone) { var t = $('[data-tone="' + this.tone + '"] span', this.root); if (t) s += " Cilt tonum: " + low(t.textContent) + "."; }
    if (this.sens) s += " Cildim hassas.";
    return s;
  };
  P.planWhen = function () {
    return ["bu ay", "gelecek ay", "2 ay sonra"][this.start] || "bu ay";
  };
  P.msg = function (place) {
    var rt = this.regText();
    if (place === "plan-wa" && rt) {
      var iv = this.interval();
      return "Merhaba, lazer epilasyon planım: " + rt + ". 8 seans, " + iv[0] + "–" + iv[1] + " hafta arayla; " + this.planWhen() + " başlamak istiyorum. Fiyat ve uygun günleri öğrenebilir miyim?" + this.extras();
    }
    var base = place === "ton-wa" ? "Merhaba, hassas cildim için lazer epilasyon ön görüşmesi istiyorum." :
      (rt ? "Merhaba, lazer epilasyon için fiyat ve plan almak istiyorum." : "Merhaba, lazer epilasyon hakkında bilgi almak istiyorum.");
    return base + (rt ? " Bölgeler: " + rt + "." : "") + this.extras();
  };

  /* ---------------- sync everything that depends on the selection ---------------- */
  P.sync = function () {
    var self = this, root = this.root, on = this.lit();
    $$(".lz-part", root).forEach(function (p) { var k = p.getAttribute("data-part"); p.classList.toggle("on", !!(on.all || on[k])); p.setAttribute("aria-pressed", !!(on.all || on[k])); });
    $$("[data-rg]", root).forEach(function (b) { b.setAttribute("aria-pressed", self.has(b.getAttribute("data-rg"))); });
    var list = $("[data-lz-plist]", root);
    if (list) {
      if (!this.sel.length) list.innerHTML = '<li class="lz-empty">Henüz bölge yok. Haritada bir bölgeye dokunun.</li>';
      else list.innerHTML = this.sel.map(function (k) {
        var r = self.mins(k);
        return '<li><span>' + esc(self.name(k)) + '</span><small>' + (r ? (r.mx && r.mx !== r.m ? r.m + "–" + r.mx : r.m) + " dk" : "") + '</small><button type="button" data-rm="' + esc(k) + '" aria-label="' + esc(self.name(k)) + ': çıkar" data-track-label="at-' + self.code + '-harita-cikar">×</button></li>';
      }).join("");
      $$("[data-rm]", list).forEach(function (b) { b.addEventListener("click", function () { self.toggle(b.getAttribute("data-rm"), false); }); });
    }
    var tot = $("[data-lz-total]", root);
    if (tot) {
      var sum = 0, known = 0;
      this.sel.forEach(function (k) { var r = self.mins(k); if (r) { sum += r.m; known++; } });
      tot.innerHTML = this.sel.length ? '<b>' + this.sel.length + ' bölge</b>' + (known ? ' · menüdeki süreler <b>≈ ' + sum + ' dk</b>' + (known < this.sel.length ? " + paket" : "") : "") + ' · <b>8 seans</b>' : "";
    }
    $$("[data-lz-wa]", root).forEach(function (a) { a.href = self.wa(self.msg(a.getAttribute("data-lz-wa"))); });
    var waLbl = $('[data-lz-wa="harita-wa"] .lz-lbl', root);
    if (waLbl) waLbl.textContent = this.sel.length ? this.sel.length + " bölgeyi WhatsApp'tan sor" : "WhatsApp'tan fiyat sor";
    var my = $("[data-lz-mybar]", root);
    if (my) { my.hidden = !this.sel.length; var c = $("[data-lz-mycount]", my); if (c) c.textContent = "Fiyat listem · " + this.sel.length + " kalem"; }
    if (this.bar) { this.bar.wa.href = this.wa(this.msg(this.sel.length ? "plan-wa" : "bar-wa")); $(".lz-lbl", this.bar.wa).textContent = this.sel.length ? "Planım · " + this.sel.length + " bölge" : "WhatsApp'tan fiyat sor"; }
    if (this.host.bar) this.host.bar(this.barText());
    this.renderCal();
    if (this.planOpen) this.renderPlan();
  };
  P.barText = function () { return this.sel.length ? this.sel.length + " bölge · günümü seç" : "Bölgelerim · günümü seç"; };

  /* ---------------- L1 hero ---------------- */
  P.initHero = function () {
    var self = this, root = this.root, stage = $(".lz-stage", root);
    if (stage && this.tier !== "C") stage.classList.add("go");
    var o = openState(), chip = $("[data-lz-open]", root);
    if (chip) chip.innerHTML = '<i class="lz-dot' + (o.open ? "" : " off") + '"></i>' + o.txt;
    var v = $(".lz-hero-vid", root);
    if (!v || this.tier === "C") return;
    function boot() {
      setTimeout(function () {
        if (!v.getAttribute("data-src")) return;
        v.src = v.getAttribute("data-src"); v.removeAttribute("data-src");
        v.addEventListener("playing", function () { v.classList.add("on"); }, { once: true });
        var p = v.play(); if (p && p.catch) p.catch(function () {});
      }, self.tier === "A" ? 300 : 1200);
    }
    if (document.readyState === "complete") boot(); else addEventListener("load", boot);
    if ("IntersectionObserver" in window) new IntersectionObserver(function (es) {
      if (!v.src) return; if (es[0].isIntersecting) { var p = v.play(); if (p && p.catch) p.catch(function () {}); } else v.pause();
    }, { threshold: 0.15 }).observe(v);
  };
  P.initScroll = function () {
    var root = this.root;
    $$("[data-lz-scroll]", root).forEach(function (a) {
      a.addEventListener("click", function (e) {
        var id = (a.getAttribute("href") || "").split("#")[1], t = id && document.getElementById(id);
        if (!t) return; e.preventDefault();
        var top = t.getBoundingClientRect().top + scrollY - (parseInt(getComputedStyle(root).getPropertyValue("--lz-top")) || 64) - 8;
        scrollTo({ top: top, behavior: "smooth" });
      });
    });
  };

  /* ---------------- rings + story viewer ---------------- */
  P.initRings = function () {
    var self = this, box = $("[data-lz-rings]", this.root);
    if (!box) return;
    box.innerHTML = this.D.stories.map(function (s, i) { return '<button type="button" class="lz-ring" data-st="' + i + '" data-track-label="at-' + self.code + '-hikaye"><i><img src="' + s.th + '" alt="" loading="lazy" decoding="async"></i><span>' + esc(s.t) + "</span></button>"; }).join("");
    $$("[data-st]", box).forEach(function (b) { b.addEventListener("click", function () { self.story(+b.getAttribute("data-st"), 0); }); });
  };
  P.story = function (si, fi) {
    var self = this, ST = this.ST = this.ST || {};
    var el = document.querySelector(".lz-story");
    if (!el) {
      el = document.createElement("div"); el.className = "lz-story"; el.setAttribute("role", "dialog"); el.setAttribute("aria-modal", "true"); el.setAttribute("aria-label", "Hikâyeler");
      el.innerHTML = '<div class="lz-stf"><div class="lz-stscrim"></div><div class="lz-stbars"></div><div class="lz-sthead"><b></b><button type="button" class="lz-x" data-stx aria-label="Kapat">' + X + '</button></div><div class="lz-stnav"><button type="button" data-stp aria-label="Önceki"></button><button type="button" data-stn aria-label="Sonraki"></button></div><div class="lz-stcap"></div></div>';
      document.body.appendChild(el);
      $("[data-stx]", el).addEventListener("click", function () { self.closeStory(); });
      $("[data-stn]", el).addEventListener("click", function () { self.stNext(); });
      $("[data-stp]", el).addEventListener("click", function () { self.stPrev(); });
      var y0 = null, f = $(".lz-stf", el);
      f.addEventListener("pointerdown", function (e) { ST.paused = true; y0 = e.clientY; });
      f.addEventListener("pointerup", function (e) { ST.paused = false; if (y0 !== null && e.clientY - y0 > 90) self.closeStory(); y0 = null; });
      addEventListener("keydown", function (e) { if (!el.classList.contains("on")) return; if (e.key === "Escape") self.closeStory(); if (e.key === "ArrowRight") self.stNext(); if (e.key === "ArrowLeft") self.stPrev(); });
    }
    ST.el = el; ST.si = si; ST.fi = fi || 0; ST.list = this.D.stories; ST.owner = this;
    el.classList.add("on"); this.showFrame();
  };
  P.closeStory = function () { var ST = this.ST; if (!ST || !ST.el) return; ST.el.classList.remove("on"); cancelAnimationFrame(ST.timer); $$("video", ST.el).forEach(function (v) { v.pause(); }); };
  P.stNext = function () { var ST = this.ST, s = ST.list[ST.si]; if (ST.fi < s.fr.length - 1) { ST.fi++; return this.showFrame(); } if (ST.si < ST.list.length - 1) { ST.si++; ST.fi = 0; return this.showFrame(); } this.closeStory(); };
  P.stPrev = function () { var ST = this.ST; if (ST.fi > 0) { ST.fi--; return this.showFrame(); } if (ST.si > 0) { ST.si--; ST.fi = 0; } this.showFrame(); };
  P.showFrame = function () {
    var self = this, ST = this.ST, s = ST.list[ST.si], f = s.fr[ST.fi], box = $(".lz-stf", ST.el), m;
    $$(".lz-stm", box).forEach(function (x) { x.remove(); });
    ST.dur = 5200;
    if (f.video) {
      m = document.createElement("video"); m.src = f.video; m.poster = f.poster || ""; m.muted = true; m.playsInline = true; m.setAttribute("playsinline", ""); m.autoplay = true;
      m.addEventListener("loadedmetadata", function () { if (isFinite(m.duration) && m.duration > 0) ST.dur = Math.min(15000, m.duration * 1000); });
      var pv = m.play && m.play(); if (pv && pv.catch) pv.catch(function () {});
    } else if (f.img) { m = document.createElement("img"); m.src = f.img; m.alt = f.cap || ""; }
    else if (f.rv) { m = document.createElement("div"); m.className = "lz-sthtml"; m.innerHTML = '<div><span style="color:#D9B26A;letter-spacing:.2em">★★★★★</span><p>“' + esc(f.rv.t) + '”</p><span style="font:600 12px system-ui;letter-spacing:.18em;text-transform:uppercase;color:#EBB7A6">' + esc(f.rv.n) + ' · Google</span></div>'; }
    else { m = document.createElement("div"); m.className = "lz-sthtml"; m.innerHTML = '<div><span style="font:600 11px system-ui;letter-spacing:.24em;text-transform:uppercase;color:#EBB7A6">Fiyat</span><p>Bölgelerinize göre, kişiye özel.</p><span style="color:#CDBDB4">Tek seans, 8 seans paket ve bitiş garantili paket seçenekleri var.</span></div>'; }
    m.classList.add("lz-stm"); box.insertBefore(m, box.firstChild);
    $(".lz-sthead b", ST.el).textContent = s.t;
    $(".lz-stbars", ST.el).innerHTML = s.fr.map(function (_, i) { return '<i><b style="width:' + (i < ST.fi ? 100 : 0) + '%"></b></i>'; }).join("");
    var last = ST.fi === s.fr.length - 1;
    var cap = $(".lz-stcap", ST.el);
    cap.innerHTML = (f.cap ? "<b>" + esc(f.cap) + "</b>" : "") + (last ? '<a class="lz-btn-gold" data-lz-stwa target="_blank" rel="noopener" href="' + esc(this.wa(this.msg("hikaye-wa"))) + '" data-track-label="at-' + this.code + '-hikaye-wa">' + WAI + '<span class="lz-lbl">WhatsApp\'tan sor</span></a>' : "");
    relead();
    ST.t0 = performance.now(); cancelAnimationFrame(ST.timer);
    var bar = $$(".lz-stbars b", ST.el)[ST.fi];
    function tick(t) { if (!ST.el.classList.contains("on")) return; if (ST.paused) ST.t0 += 16; var k = (t - ST.t0) / ST.dur; bar.style.width = Math.min(100, k * 100) + "%"; if (k >= 1) return self.stNext(); ST.timer = requestAnimationFrame(tick); }
    ST.timer = requestAnimationFrame(tick);
  };

  /* ---------------- L2 map ---------------- */
  P.initMap = function () {
    var self = this, root = this.root, ui = $(".lz-map-ui", root);
    if (!ui) return;
    $$(".lz-part", ui).forEach(function (p) {
      function go(e) { e.preventDefault(); $(".lz-figure", ui).classList.add("used"); self.partClick(p.getAttribute("data-part"), p); }
      p.addEventListener("click", go);
      p.addEventListener("keydown", function (e) { if (e.key === "Enter" || e.key === " ") go(e); });
    });
    $$("[data-lz-side]", ui).forEach(function (b) { b.addEventListener("click", function () { self.setSide(b.getAttribute("data-lz-side")); }); });
    $$("[data-lz-gender]", root).forEach(function (b) { b.addEventListener("click", function () { self.setGender(b.getAttribute("data-lz-gender")); }); });
    $$(".lz-pkg,[data-lz-rgchips] [data-rg]", ui).forEach(function (b) { b.addEventListener("click", function () { self.toggle(b.getAttribute("data-rg")); }); });
    $$("[data-lz-plan]", root).forEach(function (b) { b.addEventListener("click", function () { self.openPlan(); }); });
    this.setSide(ui.getAttribute("data-face") === "1" ? "yuz" : "on", true);
    this.setGender(this.g, true);
  };
  P.setSide = function (side, quiet) {
    var ui = $(".lz-map-ui", this.root); if (!ui) return;
    this.side = side;
    $$("[data-lz-side]", ui).forEach(function (b) { b.setAttribute("aria-pressed", b.getAttribute("data-lz-side") === side); });
    this.showFig();
    if (!quiet && side === "yuz") { var f = $(".lz-figure", ui); if (f && f.getBoundingClientRect().top < 0) f.scrollIntoView({ block: "center", behavior: "smooth" }); }
  };
  P.setGender = function (g, quiet) {
    var self = this;
    if (g !== this.g) this.sel = this.sel.filter(function (k) { return k.indexOf("pkg:") === 0 ? false : !!self.byId[g + ":" + k]; });
    this.g = g;
    $$("[data-lz-gender]", this.root).forEach(function (b) { b.setAttribute("aria-pressed", b.getAttribute("data-lz-gender") === g); });
    $$(".lz-mbody", this.root).forEach(function (m) { m.hidden = m.getAttribute("data-g") !== g; });
    var chips = $("[data-lz-rgchips]", this.root);
    if (chips) chips.innerHTML = this.D.regions[g].filter(function (r) { return r.z !== "pkg"; }).map(function (r) {
      return '<button type="button" data-rg="' + r.id + '" aria-pressed="false" data-track-label="at-' + self.code + '-liste-bolge"><span>' + esc(r.n) + "</span><small>" + (r.m ? r.m + (r.mx && r.mx !== r.m ? "–" + r.mx : "") + " dk" : "") + "</small></button>";
    }).join("");
    var pk = $(".lz-pkgs", this.root);
    if (pk) pk.innerHTML = this.D.regions[g].filter(function (r) { return r.z === "pkg"; }).map(function (r) {
      return '<button type="button" class="lz-pkg" data-rg="' + r.id + '" aria-pressed="false" data-track-label="at-' + self.code + '-harita-paket"><b>' + esc(r.n) + "</b><small>" + (r.m ? r.m + " dk" : "") + " · bitiş garantili seçenek</small></button>";
    }).join("");
    $$(".lz-pkg,[data-lz-rgchips] [data-rg]", this.root).forEach(function (b) { b.addEventListener("click", function () { self.toggle(b.getAttribute("data-rg")); }); });
    this.showFig();
    if (!quiet) this.sync();
  };
  P.showFig = function () {
    var ui = $(".lz-map-ui", this.root); if (!ui) return;
    var g = this.g, side = this.side;
    $$(".lz-body", ui).forEach(function (s) { s.classList.toggle("on", side !== "yuz" && s.getAttribute("data-g") === g && s.getAttribute("data-side") === side); });
    $$(".lz-facesvg", ui).forEach(function (s) { s.classList.toggle("on", side === "yuz" && s.getAttribute("data-g") === g); });
    $(".lz-figure", ui).setAttribute("data-view", side);
  };
  P.shot = function (el) {
    if (this.tier === "C" || !el || !el.ownerSVGElement) return;
    var svg = el.ownerSVGElement, fx = $(".lz-fx", svg), bb;
    try { bb = el.getBBox(); } catch (e) { return; }
    var NS = "http://www.w3.org/2000/svg", cx = bb.x + bb.width / 2, cy = bb.y + bb.height / 2, r = Math.max(8, Math.min(bb.width, bb.height) / 2);
    var g = document.createElementNS(NS, "g"); g.setAttribute("class", "lz-shotg");
    g.innerHTML = '<circle class="lz-flash" cx="' + cx + '" cy="' + cy + '" r="' + r * 1.4 + '"/>' +
      '<circle class="lz-shot" cx="' + cx + '" cy="' + cy + '" r="' + r + '"/>' +
      '<circle class="lz-shot lz-shot2" cx="' + cx + '" cy="' + cy + '" r="' + r + '"/>' +
      [0, 60, 120, 180, 240, 300].map(function (a) { var rad = a * Math.PI / 180, x1 = cx + Math.cos(rad) * r * .9, y1 = cy + Math.sin(rad) * r * .9, x2 = cx + Math.cos(rad) * r * 2.1, y2 = cy + Math.sin(rad) * r * 2.1;
        return '<line class="lz-spark" x1="' + x1 + '" y1="' + y1 + '" x2="' + x2 + '" y2="' + y2 + '"/>'; }).join("");
    fx.appendChild(g);
    if (navigator.vibrate) try { navigator.vibrate(12); } catch (e) {}
    setTimeout(function () { g.remove(); }, 1000);
  };
  P.refreshMinutes = function () {
    /* Minutes come from the CRM menu at build time; refresh them from the live menu when it answers. */
    var self = this;
    if (this.host.noFetch || !window.fetch) return;
    fetch("/api/public/price-menu", { credentials: "omit" }).then(function (r) { return r.ok ? r.json() : null; }).then(function (d) {
      if (!d || !d.subservices) return;
      var svc = { kadin: "KADIN LAZER EPİLASYON SEANS", erkek: "ERKEK LAZER EPİLASYON SEANS" }, changed = false;
      ["kadin", "erkek"].forEach(function (g) {
        self.D.regions[g].forEach(function (r) {
          var mins = d.subservices.filter(function (x) { return x.service_name === svc[g] && x.name === r.crm && x.is_active !== false; }).map(function (x) { return +x.duration_minutes; }).filter(function (n) { return n > 0; });
          if (!mins.length) return; var lo = Math.min.apply(null, mins), hi = Math.max.apply(null, mins);
          if (lo !== r.m || hi !== r.mx) { r.m = lo; r.mx = hi; changed = true; }
        });
      });
      if (changed) self.sync();
    }).catch(function () {});
  };

  /* ---------------- L3 journey ---------------- */
  P.initJourney = function () {
    var self = this, fig = $(".lz-jfig", this.root);
    if (!fig) return;
    var steps = $$(".lz-jtxt", this.root);
    $$("[data-wl]", $(".lz-waves", this.root) || this.root).forEach(function (b) {
      if (b === fig) return;
      b.addEventListener("click", function () { fig.setAttribute("data-wl", b.getAttribute("data-wl")); if (fig.getAttribute("data-step") === "0") fig.setAttribute("data-step", "1");
        $$(".lz-waves [data-wl]", self.root).forEach(function (x) { x.setAttribute("aria-pressed", x === b); }); });
    });
    if (this.tier === "C" || !("IntersectionObserver" in window)) { fig.setAttribute("data-step", "3"); return; }
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) self.jStep(+e.target.getAttribute("data-step")); });
    }, { rootMargin: "-38% 0px -6% 0px", threshold: 0.9 });
    steps.forEach(function (s) { io.observe(s); });
  };
  P.jStep = function (n) {
    var fig = $(".lz-jfig", this.root); if (!fig) return;
    fig.setAttribute("data-step", String(n));
    clearInterval(this.sessT);
    var fols = $$(".lz-fol", fig), sessB = $("[data-lz-sess]", fig), dots = $$(".lz-sess i", fig);
    fols.forEach(function (f) { f.classList.remove("gone"); });
    if (n !== 4) return;
    var order = [0, 4, 7, 2, 5, 3, 1, 8], k = 0;
    function tick() {
      k = k % 8 + 1; sessB.textContent = k;
      dots.forEach(function (d, i) { d.classList.toggle("on", i < k); });
      fols.forEach(function (f) { f.classList.toggle("gone", order.indexOf(+f.getAttribute("data-i")) < Math.round((k - 1) * 0.85)); });
    }
    tick(); this.sessT = setInterval(tick, 1100);
  };

  /* ---------------- L4 calendar ---------------- */
  P.initCal = function () {
    var self = this, cal = $("[data-lz-cal]", this.root);
    if (!cal) return;
    $$("[data-start]", cal).forEach(function (b) { b.addEventListener("click", function () { self.start = +b.getAttribute("data-start"); $$("[data-start]", cal).forEach(function (x) { x.setAttribute("aria-pressed", x === b); }); self.sync(); }); });
  };
  P.interval = function () {
    var face = 0, body = 0, self = this;
    this.sel.forEach(function (k) { if (self.isFace(k)) face++; else body++; });
    return (face && !body) ? [4, 6, "yüz"] : [6, 8, "vücut"];
  };
  P.renderCal = function () {
    var cal = $("[data-lz-cal]", this.root); if (!cal) return;
    var t = ist(), iv = this.interval(), start;
    if (this.start === 0) start = new Date(Date.UTC(t.y, t.m - 1, t.d, 12));
    else start = new Date(Date.UTC(t.y, t.m - 1 + this.start, 1, 12));
    var day = 864e5, nodes = [];
    for (var k = 0; k < 8; k++) {
      var e = new Date(start.getTime() + k * iv[0] * 7 * day), l = new Date(start.getTime() + k * iv[1] * 7 * day);
      var same = e.getUTCMonth() === l.getUTCMonth() && e.getUTCFullYear() === l.getUTCFullYear();
      nodes.push({ e: e, l: l, lab: k === 0 ? (this.start === 0 ? "Bu hafta" : MON3[e.getUTCMonth()]) : (same ? MON3[e.getUTCMonth()] : MON3[e.getUTCMonth()] + "–" + MON3[l.getUTCMonth()]) });
    }
    $("[data-lz-track]", cal).innerHTML = nodes.map(function (n, i) { return '<li class="lz-node" style="--i:' + i + '"><i>' + (i + 1) + "</i><span>" + n.lab + "</span></li>"; }).join("");
    var a = nodes[7].e, b = nodes[7].l;
    var when = TR_MON[a.getUTCMonth()] + (a.getUTCFullYear() !== b.getUTCFullYear() ? " " + a.getUTCFullYear() : "") + (a.getUTCMonth() === b.getUTCMonth() && a.getUTCFullYear() === b.getUTCFullYear() ? "" : " – " + TR_MON[b.getUTCMonth()]) + " " + b.getUTCFullYear();
    $("[data-lz-calsum]", cal).textContent = "8. seans ≈ " + when + " · " + iv[0] + "–" + iv[1] + " hafta arayla (" + iv[2] + (this.sel.length ? "" : ", bölge seçince güncellenir") + ")";
    this.renderPlanCard(cal, iv);
  };
  var GUAR = ["tepeden", "tum-vucut-4", "full-vucut", "kemer-ustu"];
  P.renderPlanCard = function (cal, iv) {
    var self = this, reg = $("[data-lz-pc-reg]", cal);
    if (!reg) return;
    if (!this.sel.length) {
      reg.innerHTML = '<a href="#lz-harita" data-track-label="at-' + this.code + '-plan-harita">Haritadan bölge seçin</a>';
      var a = $("a", reg);
      a.addEventListener("click", function (e) { var t = document.getElementById("lz-harita"); if (!t) return; e.preventDefault(); t.scrollIntoView({ behavior: "smooth", block: "start" }); });
    } else reg.innerHTML = this.sel.map(function (k) { return "<span>" + esc(self.name(k)) + "</span>"; }).join("");
    var sum = 0, known = 0;
    this.sel.forEach(function (k) { var r = self.mins(k); if (r) { sum += r.m; known++; } });
    $("[data-lz-pc-min]", cal).textContent = known ? "Menüdeki süreler ≈ " + sum + " dk / seans" + (known < this.sel.length ? " + paket" : "") : (this.sel.length ? "Pakete göre" : "Bölge seçince görünür");
    $("[data-lz-pc-iv]", cal).textContent = "8 seans · " + iv[0] + "–" + iv[1] + " hafta arayla (" + iv[2] + ")";
    var badge = $("[data-lz-pc-badge]", cal);
    if (badge) badge.hidden = !this.sel.some(function (k) { return GUAR.indexOf(k) >= 0 || (k.indexOf("pkg:") === 0 && /bitiş garantili/i.test(k)); });
    cal.classList.toggle("has", this.sel.length > 0);
    var lbl = $('[data-lz-wa="plan-wa"] .lz-lbl', cal);
    if (lbl) lbl.textContent = this.sel.length ? "Planı WhatsApp'a gönder" : "WhatsApp'tan plan iste";
  };

  /* ---------------- L5 device ---------------- */
  P.initDevice = function () {
    var root = this.root;
    $$(".lz-hot", root).forEach(function (h) {
      h.addEventListener("click", function () {
        var k = h.getAttribute("data-hot");
        $$(".lz-hot", root).forEach(function (x) { x.setAttribute("aria-pressed", x === h); });
        $$("[data-hotcard]", root).forEach(function (c) { c.hidden = c.getAttribute("data-hotcard") !== k; });
      });
    });
  };

  /* ---------------- L6 reels ---------------- */
  P.initReels = function () {
    var self = this, reels = $$(".lz-reel", this.root);
    var stIdx = { "lazer-film-jel": [0, 0], "lazer-film-bacak": [0, 1], "lazer-film-cene": [1, 0], "lazer-film-yuz": [1, 1] };
    reels.forEach(function (r) {
      var v = $("video", r), key = r.getAttribute("data-reel");
      r.addEventListener("click", function () {
        var at = stIdx[key];
        if (at) return self.story(at[0], at[1]);
        self.storyOne(v.getAttribute("data-src") || v.currentSrc || v.src, v.getAttribute("poster"), $(".lz-reel-t", r).textContent);
      });
      if (self.tier !== "A" || !("IntersectionObserver" in window)) return;
      new IntersectionObserver(function (es) {
        var on = es[0].isIntersecting;
        if (on && v.getAttribute("data-src")) { v.src = v.getAttribute("data-src"); v.removeAttribute("data-src"); }
        if (on) { var p = v.play(); if (p && p.catch) p.catch(function () {}); } else v.pause();
      }, { threshold: 0.6 }).observe(v);
    });
  };
  P.storyOne = function (src, poster, cap) {
    this.D.stories.push({ t: cap, fr: [{ video: src, poster: poster, cap: cap }], tmp: true });
    this.story(this.D.stories.length - 1, 0);
    this.D.stories = this.D.stories.filter(function (s) { return !s.tmp; });
  };

  /* ---------------- L7 reviews ---------------- */
  P.initReviews = function () {
    var tr = $(".lz-rvtrack", this.root); if (!tr || this.tier === "C") return;
    var n = tr.children.length;
    tr.innerHTML += tr.innerHTML.replace(/<article class="lz-rv">/g, '<article class="lz-rv" aria-hidden="true">');
    tr.style.setProperty("--dur", (n * 8) + "s"); tr.classList.add("run");
  };

  /* ---------------- zoom (hygiene, device) ---------------- */
  P.initZoom = function () {
    $$("[data-zoom]", this.root).forEach(function (b) { b.addEventListener("click", function () { lightbox(b.getAttribute("data-zoom")); }); });
  };
  function lightbox(src) {
    var lb = $(".lz-lb");
    if (!lb) {
      lb = document.createElement("div"); lb.className = "lz-lb"; lb.setAttribute("role", "dialog"); lb.setAttribute("aria-label", "Yakından görünüm");
      lb.innerHTML = '<button type="button" class="lz-x" aria-label="Kapat">' + X + '</button><img alt="Yakından görünüm">';
      document.body.appendChild(lb);
      $(".lz-x", lb).addEventListener("click", function () { lb.classList.remove("on"); });
      $("img", lb).addEventListener("dblclick", function () { lb.classList.toggle("z2"); });
      addEventListener("keydown", function (e) { if (e.key === "Escape") lb.classList.remove("on"); });
    }
    $("img", lb).src = src; lb.classList.remove("z2"); lb.classList.add("on");
  }

  /* ---------------- L9 menu ---------------- */
  P.initMenu = function () {
    var self = this, sec = $(".lz-menu", this.root); if (!sec) return;
    $$("[data-lz-mg]", sec).forEach(function (b) { b.addEventListener("click", function () {
      var mg = b.getAttribute("data-lz-mg");
      $$("[data-lz-mg]", sec).forEach(function (x) { x.setAttribute("aria-pressed", x === b); });
      $$(".lz-mbody", sec).forEach(function (m) { m.setAttribute("data-mg", mg); });
    }); });
    $$(".lz-madd", sec).forEach(function (b) { b.addEventListener("click", function () { self.toggle(b.getAttribute("data-rg")); }); });
  };

  /* ---------------- tone (hassas) / quick (bölgesel) ---------------- */
  P.initTone = function () {
    var self = this;
    $$("[data-tone]", this.root).forEach(function (b) { b.addEventListener("click", function () {
      var k = b.getAttribute("data-tone"); self.tone = self.tone === k ? null : k;
      $$("[data-tone]", self.root).forEach(function (x) { x.setAttribute("aria-pressed", x.getAttribute("data-tone") === self.tone); });
      self.sync();
    }); });
    var s = $("[data-lz-sens]", this.root);
    if (s) s.addEventListener("change", function () { self.sens = s.checked; self.sync(); });
  };
  P.initQuick = function () {
    var self = this;
    $$(".lz-qchip", this.root).forEach(function (b) { b.addEventListener("click", function () {
      var id = b.getAttribute("data-rg");
      if (!self.byId[self.g + ":" + id]) self.setGender(self.g === "kadin" ? "erkek" : "kadin");
      self.toggle(id);
    }); });
  };

  /* ---------------- family + all pages menu ---------------- */
  P.initFamily = function () {
    var self = this;
    $$("[data-lz-menu]", this.root).forEach(function (b) {
      if (self.host.menu) b.addEventListener("click", function () { self.host.menu(); });
      else if (self.D.nav) b.addEventListener("click", function () { self.openNav(); });
      else b.hidden = true;
    });
  };
  P.layer = function (side) {
    var self = this, L = document.querySelector(".lz-layer");
    if (!L) {
      L = document.createElement("div"); L.className = "lz-layer";
      L.innerHTML = '<div class="lz-scrim2"></div><div class="lz-sheet" role="dialog" aria-modal="true"><div class="lz-grab"></div><button type="button" class="lz-x" aria-label="Kapat">' + X + '</button><div class="lz-sbody"></div></div>';
      document.body.appendChild(L);
      $(".lz-scrim2", L).addEventListener("click", function () { self.closeLayer(); });
      $(".lz-x", L).addEventListener("click", function () { self.closeLayer(); });
      addEventListener("keydown", function (e) { if (e.key === "Escape" && L.classList.contains("on")) self.closeLayer(); });
    }
    L.classList.toggle("side", !!side);
    return L;
  };
  P.closeLayer = function () { var L = document.querySelector(".lz-layer"); if (L) L.classList.remove("on"); this.planOpen = false; clearInterval(this.typeT); };
  P.openNav = function () {
    var self = this, L = this.layer(true), here = location.pathname.replace(/\.html$/, "").replace(/\/$/, "");
    function fold(s) { return low(s).replace(/[çğıöşüâîû]/g, function (c) { return { "ç": "c", "ğ": "g", "ı": "i", "ö": "o", "ş": "s", "ü": "u", "â": "a", "î": "i", "û": "u" }[c]; }); }
    var n = this.D.nav.reduce(function (a, g) { return a + g[1].length; }, 0);
    var h = '<span class="lz-over">Selda Gençer · ' + n + ' sayfa</span><h2>Tüm sayfalar</h2>' +
      '<label class="lz-nsearch"><input type="search" placeholder="Ara: kaş, protez, lazer…" autocomplete="off" aria-label="Sayfalarda ara" data-track-label="at-' + this.code + '-menu-ara"></label>' +
      '<div class="lz-nquick"><a class="wa" target="_blank" rel="noopener" href="' + esc(this.wa("Merhaba, randevu almak istiyorum.")) + '" data-track-label="at-' + this.code + '-menu-wa">WhatsApp</a><a href="tel:+905330390076" data-track-label="at-' + this.code + '-menu-tel">Ara</a><a href="/price-menu" data-track-label="at-' + this.code + '-menu-fiyat">Fiyat listesi</a><a href="/konum" data-track-label="at-' + this.code + '-menu-konum">Konum</a><a href="https://www.instagram.com/seldagencerbeautycenter/" target="_blank" rel="noopener" data-track-label="at-' + this.code + '-menu-instagram">Instagram</a></div><div class="lz-nlist">' +
      this.D.nav.map(function (g) {
        return '<div class="lz-ngrp"><h3 class="lz-ng">' + esc(g[0]) + " <small>" + g[1].length + '</small></h3><div class="lz-nitems">' + g[1].map(function (it) {
          var href = "/" + it[0], cur = ("/" + it[0]).replace(/\/$/, "") === here;
          return '<a class="lz-nitem' + (cur ? " here" : "") + '" href="' + href + '" data-h="' + esc(fold(it[1] + " " + it[0].replace(/-/g, " ") + " " + g[0])) + '" data-track-label="at-' + self.code + '-menu-sayfa">' + esc(it[1]) + (cur ? " <small>Buradasınız</small>" : "") + "</a>";
        }).join("") + "</div></div>";
      }).join("") + '</div><p class="lz-nempty" hidden>Bulamadık. <a target="_blank" rel="noopener" href="' + esc(this.wa("Merhaba, bir hizmet hakkında bilgi almak istiyorum.")) + '" data-track-label="at-' + this.code + '-menu-bulamadim-wa">WhatsApp\'tan sorun</a>.</p>';
    $(".lz-sbody", L).innerHTML = h; $(".lz-sheet", L).scrollTop = 0; L.classList.add("on");
    var q = $(".lz-nsearch input", L);
    q.addEventListener("input", function () {
      var t = fold(q.value.trim()), any = false;
      $$(".lz-ngrp", L).forEach(function (g) { var vis = 0; $$(".lz-nitem", g).forEach(function (a) { var ok = !t || a.getAttribute("data-h").indexOf(t) >= 0; a.hidden = !ok; if (ok) vis++; }); g.hidden = !vis; if (vis) any = true; });
      $(".lz-nempty", L).hidden = any;
    });
    relead();
  };

  /* ---------------- L10 invitation ---------------- */
  P.days = function () {
    var t = ist(), out = [], base = Date.UTC(t.y, t.m - 1, t.d, 12), mins = t.h * 60 + t.min;
    for (var off = 0; off < 10 && out.length < 7; off++) {
      var d = new Date(base + off * 864e5), wd = d.getUTCDay();
      if (wd === 1) continue;
      if (off === 0 && mins >= 18 * 60 + 30) continue;
      out.push({ off: off, wd: wd, label: off === 0 ? "Bugün" : off === 1 ? "Yarın" : TR_DAYS[wd], full: TR_DAYS[wd] + ", " + d.getUTCDate() + " " + TR_MON[d.getUTCMonth()] });
    }
    return out;
  };
  P.openPlan = function () {
    this.planOpen = true; this.pl = this.pl || { day: 0, part: null };
    var L = this.layer(false); L.classList.add("on"); this.renderPlan();
    if (this.host.hideProto) this.host.hideProto();
  };
  P.renderPlan = function () {
    var self = this, L = this.layer(false), days = this.days(), pl = this.pl, t = ist();
    if (pl.day >= days.length) pl.day = 0;
    var day = days[pl.day], nowH = t.h + t.min / 60;
    var parts = DAYPARTS.map(function (p) { return { id: p[0], n: p[1], s: p[2], ok: !(day && day.off === 0 && nowH + 1 > p[3]) }; });
    if (!pl.part || !parts.some(function (p) { return p.id === pl.part && p.ok; })) { var f = parts.filter(function (p) { return p.ok; })[0]; pl.part = f ? f.id : null; }
    var part = parts.filter(function (p) { return p.id === pl.part; })[0];
    var regs = this.D.regions[this.g];
    var h = '<span class="lz-over">Randevu davetiyesi</span><h2>Lazer epilasyon planınız</h2>' +
      '<div class="lz-pstep"><span class="lz-over"><i>1</i> Bölgeler · ' + (this.g === "kadin" ? "kadın" : "erkek") + '</span><div class="lz-pills">' +
      regs.map(function (r) { return '<button type="button" data-prg="' + r.id + '" aria-pressed="' + self.has(r.id) + '" data-track-label="at-' + self.code + '-davetiye-bolge">' + esc(r.n) + (r.m ? "<small>" + r.m + (r.mx && r.mx !== r.m ? "–" + r.mx : "") + " dk</small>" : "") + "</button>"; }).join("") + "</div></div>" +
      '<div class="lz-pstep"><span class="lz-over"><i>2</i> Plan tercihi</span><div class="lz-pills">' +
      PLANPREF.map(function (p) { return '<button type="button" data-pref="' + p[0] + '" aria-pressed="' + (self.planPref === p[0]) + '" data-track-label="at-' + self.code + '-davetiye-plan">' + p[1] + "</button>"; }).join("") + "</div></div>" +
      '<div class="lz-pstep"><span class="lz-over"><i>3</i> Gün</span><div class="lz-pills">' +
      days.map(function (d, i) { return '<button type="button" data-pday="' + i + '" aria-pressed="' + (i === pl.day) + '" data-track-label="at-' + self.code + '-davetiye-gun">' + d.label + (d.off > 1 ? "<small>" + d.full.split(", ")[1] + "</small>" : "") + "</button>"; }).join("") + "</div></div>" +
      '<div class="lz-pstep"><span class="lz-over"><i>4</i> Saat dilimi</span><div class="lz-pills">' +
      parts.map(function (p) { return '<button type="button" data-ppart="' + p.id + '" aria-pressed="' + (p.id === pl.part) + '"' + (p.ok ? "" : " disabled") + ' data-track-label="at-' + self.code + '-davetiye-dilim">' + p.n + "<small>" + p.s + "</small></button>"; }).join("") + "</div></div>";
    var whenTxt = day ? ((day.off <= 1 ? low(day.label) : day.full) + (part ? " " + low(part.n) + " (" + part.s + ")" : "")) : "";
    var pref = PLANPREF.filter(function (p) { return p[0] === self.planPref; })[0];
    var msg = "Merhaba, lazer epilasyon için " + whenTxt + " uygun mu?" + (this.sel.length ? " Bölgeler: " + this.regText() + "." : "") + (this.planPref !== "oneri" ? " Plan: " + low(pref[1]) + "." : "") + this.extras();
    var href = this.wa(msg), c = this.vcode();
    h += '<div class="lz-pstep"><span class="lz-over"><i>5</i> Davetiyeniz</span><div class="lz-inv"><div class="lz-mono">SG</div><span class="lz-over">Selda Gençer Beauty Center</span>' +
      '<div class="lz-inv-svc">Lazer epilasyon</div><div class="lz-inv-when">' + esc(day ? day.full + (part ? " · " + part.n.toLocaleLowerCase("tr-TR") : "") : "") + "</div>" +
      '<div class="lz-inv-meta">' + esc(this.sel.length ? this.regText() : "Bölge seçilmedi") + " · kişiye özel fiyat<br>Konutkent, 3028. Cd. 8A No:A1 · Çankaya</div></div>" +
      '<div class="lz-bubble"><span data-bub></span><span class="lz-caret"></span><small>şimdi</small></div>' +
      '<div class="lz-send"><a class="lz-btn-gold lz-shine" target="_blank" rel="noopener" href="' + esc(href) + '" data-track-label="at-' + this.code + '-davetiye-wa">' + WAI + '<span class="lz-lbl">WhatsApp\'ta gönder</span></a>' +
      '<span class="lz-tiny">Mesaj hazır; göndermek size kalır. Kesin saati ekibimiz WhatsApp\'ta onaylar.' + (c ? " Kod " + c + " sizi tanımamıza yardım eder." : "") + "</span></div></div>";
    $(".lz-sbody", L).innerHTML = h;
    this.typeMsg(msg + (c ? " " + c : ""));
    $$("[data-prg]", L).forEach(function (b) { b.addEventListener("click", function () { self.toggle(b.getAttribute("data-prg")); }); });
    $$("[data-pref]", L).forEach(function (b) { b.addEventListener("click", function () { self.planPref = b.getAttribute("data-pref"); self.renderPlan(); }); });
    $$("[data-pday]", L).forEach(function (b) { b.addEventListener("click", function () { pl.day = +b.getAttribute("data-pday"); self.renderPlan(); }); });
    $$("[data-ppart]", L).forEach(function (b) { b.addEventListener("click", function () { pl.part = b.getAttribute("data-ppart"); self.renderPlan(); }); });
    relead();
  };
  P.typeMsg = function (msg) {
    var el = $("[data-bub]", this.layer(false)), self = this;
    clearInterval(this.typeT);
    if (!el) return;
    if (this.tier === "C") { el.textContent = msg; return; }
    var i = 0, step = Math.max(1, Math.ceil(msg.length / 60));
    this.typeT = setInterval(function () { i += step; el.textContent = msg.slice(0, i); if (i >= msg.length) clearInterval(self.typeT); }, 16);
  };

  /* ---------------- sticky bar (live pages) ---------------- */
  P.initBar = function () {
    var self = this, bar = document.createElement("nav");
    bar.className = "lz-bar"; bar.setAttribute("aria-label", "Hızlı iletişim");
    bar.innerHTML = '<a class="lz-btn-gold lz-shine" target="_blank" rel="noopener" href="#" data-track-label="at-' + this.code + '-bar-wa">' + WAI + '<span class="lz-lbl">WhatsApp\'tan fiyat sor</span></a>' +
      '<button type="button" class="lz-btn-round" data-track-label="at-' + this.code + '-bar-gun" aria-label="Gün seçin"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><rect x="3.5" y="5" width="17" height="15" rx="3"/><path d="M8 3v4M16 3v4M3.5 10h17"/></svg></button>' +
      '<a class="lz-btn-round" href="tel:+905330390076" data-track-label="at-' + this.code + '-bar-tel" aria-label="Arayın">' + TELI + "</a>";
    document.body.appendChild(bar); document.body.classList.add("lz-page");
    this.bar = { el: bar, wa: $("a", bar) };
    /* desktop: the hero already carries both CTAs and its proof strip; the floating bar joins once it is passed */
    var hero = $(".lz-hero", this.root);
    if (hero && "IntersectionObserver" in window && matchMedia("(min-width:960px)").matches) {
      bar.classList.add("hide");
      new IntersectionObserver(function (es) { bar.classList.toggle("hide", es[0].intersectionRatio >= 0.5); }, { threshold: [0, 0.5, 1] }).observe(hero);
    }
    $("button", bar).addEventListener("click", function () { self.openPlan(); });
    relead();
  };

  window.ATLZ = {
    mount: function (root, host) { if (!root || root.__lz) return root && root.__lz; root.__lz = new Page(root, host); return root.__lz; },
    plan: function (root) { var p = root && root.__lz; if (p) p.openPlan(); },
    barText: function (root) { var p = root && root.__lz; return p ? p.barText() : "Bölgelerim · günümü seç"; },
    lightbox: lightbox
  };
  function auto() { if (window.ATLZ_NOAUTO) return; $$(".lz[data-lz-page]").forEach(function (r) { window.ATLZ.mount(r, {}); }); relead(); }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", auto); else auto();
})();
