// Live-copy click test (plan §7.2): network off except the copy itself, /api answers 204.
// For each page: no JS error, no horizontal overflow, a map tap puts the region + [W-] code into the WhatsApp
// links, every a/button in the vitrine is labelled, the laser bar replaced the old one; phone + desktop shots.
//   node tests/click_test.mjs OUTDIR SHOTDIR
import { createRequire } from "node:module";
import http from "node:http";
import fs from "node:fs";
import path from "node:path";

const req = createRequire(import.meta.url);
let pw;
try { pw = req("playwright"); } catch (e) { pw = req(req("node:child_process").execSync("npm root -g").toString().trim() + "/playwright"); }
const [root, shots] = process.argv.slice(2);
fs.mkdirSync(shots, { recursive: true });
const T = { ".html": "text/html; charset=utf-8", ".css": "text/css", ".js": "text/javascript", ".webp": "image/webp", ".mp4": "video/mp4", ".woff2": "font/woff2" };
const srv = http.createServer((q, s) => {
  const u = decodeURIComponent(q.url.split("?")[0]);
  if (u.startsWith("/api/")) { s.writeHead(204); return s.end(); }
  let f = path.join(root, u);
  if (fs.existsSync(f + ".html")) f += ".html";
  if (!fs.existsSync(f) || fs.statSync(f).isDirectory()) { s.writeHead(404); return s.end(); }
  s.writeHead(200, { "Content-Type": T[path.extname(f)] || "application/octet-stream" });
  s.end(fs.readFileSync(f));
});
await new Promise((r) => srv.listen(0, r));
const base = `http://127.0.0.1:${srv.address().port}`;
const pages = fs.readdirSync(root).filter((f) => f.endsWith(".html")).map((f) => f.slice(0, -5));
const b = await pw.chromium.launch();
let fails = 0;
for (const [w, h] of [[390, 844], [1400, 900]]) {
  const ctx = await b.newContext({ viewport: { width: w, height: h }, isMobile: w < 800, hasTouch: w < 800, deviceScaleFactor: w < 800 ? 2 : 1 });
  await ctx.route((u) => !u.toString().startsWith(base), (r) => r.abort());
  await ctx.addInitScript(() => { window.SGBVisit = { mark: () => "[W-TEST42]" }; window.__leads = 0; window.bindLeadTracking = () => { window.__leads++; }; });
  for (const p of pages) {
    const pg = await ctx.newPage();
    const errs = [];
    pg.on("pageerror", (e) => errs.push(e.message));
    pg.on("console", (m) => { if (m.type() === "error" && !/ERR_FAILED|404/.test(m.text())) errs.push(m.text()); });
    await pg.goto(`${base}/${p}`, { waitUntil: "load" });
    await pg.waitForTimeout(1200);
    await pg.screenshot({ path: `${shots}/${p}-${w}.png` });
    const r = await pg.evaluate(async () => {
      const part = document.querySelector(".lz-body.on .lz-part[data-part='koltuk'], .lz-body.on .lz-part[data-part='gogus'], .lz-facesvg.on .lz-part");
      if (part) part.dispatchEvent(new MouseEvent("click", { bubbles: true }));
      await new Promise((z) => setTimeout(z, 300));
      const was = [...document.querySelectorAll('a[href^="https://wa.me/"]')].filter((a) => a.closest(".lz,.lz-bar")).map((a) => decodeURIComponent(a.getAttribute("href")));
      const vit = document.querySelector(".lz");
      const unl = [...vit.querySelectorAll("a,button")].filter((x) => !x.getAttribute("data-track-label")).length;
      return {
        picked: part && part.getAttribute("data-part"), was: was.length, withCode: was.filter((x) => x.includes("[W-TEST42]")).length,
        withRegion: was.filter((x) => /Bölgeler:/.test(x)).length, unl, bar: !!document.querySelector(".lz-bar"),
        oldbar: !!document.querySelector(".lp-sticky-actionbar"), docW: document.documentElement.scrollWidth, vw: innerWidth,
        leads: window.__leads, h1: document.querySelectorAll("h1").length,
      };
    });
    const bad = errs.length || r.unl || !r.bar || r.oldbar || r.docW > r.vw || r.h1 !== 1 || (r.picked && r.withRegion === 0) || r.withCode !== r.was;
    fails += bad ? 1 : 0;
    console.log(`${bad ? "FAIL" : "OK  "} ${p} @${w} errs=${errs.length} part=${r.picked} wa=${r.was} code=${r.withCode} region=${r.withRegion} unlabeled=${r.unl} bar=${r.bar} oldbar=${r.oldbar} docW=${r.docW}/${r.vw} h1=${r.h1} leads=${r.leads}`);
    errs.slice(0, 3).forEach((e) => console.log("   ERR", e));
    await pg.close();
  }
  await ctx.close();
}
await b.close();
srv.close();
process.exit(fails ? 1 : 0);
