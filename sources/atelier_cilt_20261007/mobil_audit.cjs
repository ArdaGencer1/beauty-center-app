// Mobil / yön denetimi: 10 ekran (320 dikey … 1920 masaüstü, yatay telefonlar, tabletler).
// Kullanım: BASE=http://127.0.0.1:8766/index.html [ROUTES=cilt,kas,…] [SHOT=l844,t768] NODE_PATH=$(npm root -g) node mobil_audit.cjs <çıktı>
// Ölçer: yatay taşma ve taşan öğe, H1 ilk ekranda mı, kahraman/sahne/film boyutu, alt çubuk konumu, 32 px altı dokunma hedefleri.
const { chromium } = require("playwright");
const VPS = [["s320",320,568,1],["p390",390,844,1],["p430",430,932,1],["l568",568,320,1],["l844",844,390,1],["l932",932,430,1],["t768",768,1024,1],["t1024",1024,768,1],["d1366",1366,900,0],["d1920",1920,1080,0]];
const ROUTES = (process.env.ROUTES || "cilt,cilt/akne-bakimi,cilt/klasik-cilt-bakimi,cilt/saten-yuz-germe,cilt/cilt-analizi,cilt/cilt-bakimi-fiyatlari,cilt/hollywood-bakimi,cilt/cilt-yenileme,cilt/dudak-bakimi,cilt/dermabrazyon").split(",");
const SHOT = process.env.SHOT; const out = process.argv[2];
(async () => {
  const b = await chromium.launch(); const rows = [];
  for (const [k, w, h, mob] of VPS) {
    const ctx = await b.newContext({ viewport: { width: w, height: h }, isMobile: !!mob, hasTouch: !!mob, deviceScaleFactor: 1 });
    const p = await ctx.newPage(); const errs = [];
    p.on("pageerror", e => errs.push(e.message));
    for (const r of ROUTES) {
      await p.goto("about:blank"); await p.goto((process.env.BASE || "http://127.0.0.1:8766/index.html") + "#" + r, { waitUntil: "load" }); await p.waitForTimeout(500);
      const m = await p.evaluate(() => {
        const W = innerWidth, H = innerHeight, sec = document.querySelector("main > [data-view]:not([hidden])");
        const vis = e => e.offsetParent !== null || getComputedStyle(e).position === "fixed";
        const scroller = e => { for (let x = e.parentElement; x; x = x.parentElement) { const s = getComputedStyle(x); if (/(auto|scroll|hidden|clip)/.test(s.overflowX) && x !== document.body && x !== document.documentElement) return true; } return false; };
        const off = [...sec.querySelectorAll("*")].filter(e => { const r = e.getBoundingClientRect(); return r.width && (r.right > W + 1 || r.left < -1) && !scroller(e); }).slice(0, 4).map(e => e.tagName.toLowerCase() + "." + [...e.classList].join(".") + "@" + Math.round(e.getBoundingClientRect().right));
        const h1 = [...sec.querySelectorAll("h1")].find(vis); const hr = h1 ? h1.getBoundingClientRect() : null;
        const media = sec.querySelector(".hero-media:not([hidden])") ; const mr = media && media.offsetParent ? media.getBoundingClientRect() : null;
        const stage = [...sec.querySelectorAll(".ca-stage")].find(vis); const sr = stage ? stage.getBoundingClientRect() : null;
        const film = sec.querySelector(".ca-film-box"); const fr = film && film.offsetParent ? film.getBoundingClientRect() : null;
        const bar = document.querySelector("nav.bar"); const br = bar ? bar.getBoundingClientRect() : null;
        const cta = [...sec.querySelectorAll(".hero .btn-gold, .hero .ca-ctas .btn-gold")].find(vis); const cr = cta ? cta.getBoundingClientRect() : null;
        const small = [...sec.querySelectorAll("button, a")].filter(vis).filter(e => { const r = e.getBoundingClientRect(); return r.width > 0 && (r.height < 32 || r.width < 32); }).map(e => (e.className || e.tagName) + ":" + Math.round(e.getBoundingClientRect().height)).slice(0, 4);
        return { ov: document.documentElement.scrollWidth - W, off, h1Top: hr && Math.round(hr.top), h1Bot: hr && Math.round(hr.bottom), H,
          media: mr && Math.round(mr.height) + "x" + Math.round(mr.width), stage: sr && Math.round(sr.width) + "x" + Math.round(sr.height), film: fr && Math.round(fr.width) + "x" + Math.round(fr.height),
          barTop: br && Math.round(br.top), ctaBot: cr && Math.round(cr.bottom), small };
      });
      rows.push({ vp: k, r, ...m, errs: errs.splice(0) });
      if (SHOT && SHOT.split(",").includes(k)) await p.screenshot({ path: `${out}/${k}-${r.replace(/\//g, "_")}.png` });
    }
    await ctx.close();
  }
  await b.close();
  for (const x of rows) {
    const flags = [];
    if (x.ov > 0) flags.push("TAŞMA " + x.ov + " " + x.off.join(" "));
    if (x.h1Bot && x.h1Bot > x.H) flags.push("H1 ilk ekranda değil (" + x.h1Top + ">" + x.H + ")");
    if (x.errs.length) flags.push("HATA " + x.errs[0]);
    console.log((flags.length ? "XX " : "ok ") + x.vp.padEnd(6) + x.r.padEnd(30) + ` medya=${x.media} sahne=${x.stage} film=${x.film} h1=${x.h1Top}/${x.H} bar=${x.barTop} cta=${x.ctaBot} küçük=${x.small.join(",")} ${flags.join(" | ")}`);
  }
})();
