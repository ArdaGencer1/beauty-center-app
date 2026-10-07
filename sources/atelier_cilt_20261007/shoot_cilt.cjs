// CİLT ATLASI v4 · tarayıcı doğrulaması (Playwright, Chromium).
// Kullanım:  python3 -m http.server 8765 -d website &   NODE_PATH=$(npm root -g) node sources/atelier_cilt_20261007/shoot_cilt.cjs [çıktı-klasörü]
// Her yol için mobil (390×844) ve masaüstü (1280×800): konsol hatası, başarısız istek, yatay taşma, WhatsApp
// bağlantısında [W-XXXXXX] kodu, data-track-label biçimi; sayfa boyunca kaydırıp videoların yüklenmesini tetikler.
const { chromium } = require("playwright");
const path = require("path");
const fs = require("fs");

const BASE = process.env.BASE || "http://127.0.0.1:8765/index.html";
const OUT = process.argv[2] || "shots";
const SLUGS = ["", "cilt-bakimi-fiyatlari", "klasik-cilt-bakimi", "cilt-temizligi", "akne-bakimi", "cilt-yenileme", "ton-esitleme",
  "saten-yuz-germe", "anti-aging-bakimi", "goz-cevresi-bakimi", "cilt-analizi", "yuz-bakimi", "leke-bakimi", "hollywood-bakimi",
  "paris-isiltisi-bakimi", "dermabrazyon", "hydra-elite", "hassas-cilt", "antioksidan-bakimi", "dudak-bakimi", "cilt-inceltme",
  "cilt-kararma-bakimi", "sirt-bakimi", "koltuk-alti-bakimi", "dirsek-bakimi"];
const VPS = [["m", { width: 390, height: 844 }, true], ["d", { width: 1280, height: 800 }, false]];

(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const browser = await chromium.launch({ executablePath: process.env.CHROMIUM || undefined });
  const rows = []; let bad = 0;
  for (const [vk, vp, mobile] of VPS) {
    const ctx = await browser.newContext({ viewport: vp, isMobile: mobile, hasTouch: mobile, deviceScaleFactor: mobile ? 2 : 1 });
    const page = await ctx.newPage();
    let errs = [], fails = [];
    page.on("console", m => { if (m.type() === "error") errs.push(m.text()); });
    page.on("pageerror", e => errs.push("pageerror: " + e.message));
    page.on("requestfailed", r => { const u = r.url(); if (u.startsWith("http://127.0.0.1") && !/net::ERR_ABORTED/.test(r.failure().errorText)) fails.push(u + " " + r.failure().errorText); });
    page.on("response", r => { if (r.status() >= 400 && r.url().startsWith("http://127.0.0.1")) fails.push(r.status() + " " + r.url()); });
    await page.goto(BASE + "#cilt", { waitUntil: "load" });
    await page.waitForTimeout(400);
    for (const s of SLUGS) {
      errs = []; fails = [];
      const route = s ? "cilt/" + s : "cilt";
      // her yol taze yüklenir (derin bağlantı açılışı); uygulama içi geçişler ayrıca tıklama akışında denenir
      await page.goto("about:blank"); await page.goto(BASE + "#" + route, { waitUntil: "load" });
      await page.waitForTimeout(700);
      // sayfa boyunca kaydır: hikâye perdeleri, film ve videolar yüklensin
      const H = await page.evaluate(() => document.documentElement.scrollHeight);
      for (let y = 0; y < H; y += Math.round(vp.height * 0.7)) { await page.evaluate(yy => window.scrollTo(0, yy), y); await page.waitForTimeout(60); }
      await page.waitForTimeout(300);
      const info = await page.evaluate(() => {
        const vis = el => el && !el.closest("[hidden]");
        const sec = document.querySelector("main > [data-view='cilt']");
        const was = [...sec.querySelectorAll("a[href*='wa.me']")].filter(vis);
        const waBad = was.filter(a => !/%5BW-[A-Z0-9]{6}%5D/.test(a.href)).map(a => a.textContent.trim());
        const lbls = [...sec.querySelectorAll("button,a")].filter(vis);
        const noLbl = lbls.filter(b => !b.hasAttribute("data-track-label") && !b.closest(".gal")).map(b => (b.textContent || b.getAttribute("aria-label") || "").trim().slice(0, 30));
        const badLbl = lbls.map(b => b.getAttribute("data-track-label")).filter(l => l && !/^[a-z0-9_-]{1,48}$/.test(l));
        const imgs = [...sec.querySelectorAll("img")].filter(vis).filter(i => i.complete && i.naturalWidth === 0 && i.getAttribute("loading") !== "lazy").map(i => i.src);
        return { route: location.hash, title: (document.querySelector("#ciltPage:not([hidden]) h1, #ciltHub:not([hidden]) h1") || {}).textContent,
          overflow: document.documentElement.scrollWidth - window.innerWidth, wa: was.length, waBad, noLbl: noLbl.slice(0, 5), badLbl, imgs,
          acts: sec.querySelectorAll(".ca-act").length, vids: [...sec.querySelectorAll("video")].filter(vis).length,
          bar: (document.querySelector("#barLbl") || {}).textContent };
      });
      await page.evaluate(() => { document.documentElement.style.scrollBehavior = "auto"; window.scrollTo(0, 0); }); await page.waitForTimeout(600);
      await page.screenshot({ path: path.join(OUT, `${vk}-${s || "hub"}.png`) });
      // hikâye sahnesi: üçüncü perde ortadayken sahne ile perde aynı medyayı göstermeli
      const story = await page.evaluate(async () => {
        const box = [...document.querySelectorAll("[data-ca-story]")].find(b => !b.closest("[hidden]")); if (!box) return null;
        const act = box.querySelectorAll(".ca-act")[2]; if (!act) return null;
        const r = act.getBoundingClientRect(); window.scrollTo(0, scrollY + r.top + r.height / 2 - innerHeight / 2);
        await new Promise(res => setTimeout(res, 900));
        const on = box.querySelector(".ca-act.on"), lay = box.querySelector(".ca-layer.on");
        return { act: on && on.dataset.k, layer: lay && lay.dataset.k, i: on && on.dataset.i };
      });
      if (story) await page.screenshot({ path: path.join(OUT, `${vk}-${s || "hub"}-hikaye.png`) });
      info.story = story;
      const storyOk = !info.story || (info.story.act === info.story.layer && info.story.i === "2");
      const ok = storyOk && !errs.length && !fails.length && info.overflow <= 0 && !info.waBad.length && !info.badLbl.length && !info.imgs.length && info.route === "#" + route;
      if (!ok) bad++;
      rows.push({ vp: vk, s: s || "hub", ok, ...info, errs, fails });
    }
    await ctx.close();
  }
  await browser.close();
  for (const r of rows) console.log(`${r.ok ? "OK " : "XX "} ${r.vp} ${r.s.padEnd(22)} taşma=${r.overflow} wa=${r.wa} video=${r.vids} perde=${r.acts} bar="${r.bar}" hikaye=${r.story ? r.story.i + ":" + r.story.act + "=" + r.story.layer : "-"}` +
    (r.ok ? "" : ` | hata=${JSON.stringify(r.errs).slice(0, 300)} istek=${JSON.stringify(r.fails).slice(0, 300)} waBad=${r.waBad} badLbl=${r.badLbl} img=${r.imgs} route=${r.route}`) +
    (r.noLbl.length ? ` | etiketsiz=${JSON.stringify(r.noLbl)}` : ""));
  console.log(`\n${rows.length - bad}/${rows.length} geçti`);
  fs.writeFileSync(path.join(OUT, "report.json"), JSON.stringify(rows, null, 1));
  process.exit(bad ? 1 : 0);
})();
