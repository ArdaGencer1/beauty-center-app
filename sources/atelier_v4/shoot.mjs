// ATELIER v4 checks: every route at phone + desktop width; console errors, horizontal overflow, failed media,
// unlabeled buttons/links, and screenshots (top + a few scroll stops).
//   node shoot.mjs --routes salon,lazer,pmu-kas/pudra --out DIR [--widths 390,1400] [--tier A] [--world mermer] [--stops 3]
//   node shoot.mjs --all --out DIR            (every route listed in routes.json next to this file)
import { createRequire } from "node:module";
const req = createRequire(import.meta.url);
let pw; try { pw = req("playwright"); } catch (e) { pw = req(req("node:child_process").execSync("npm root -g").toString().trim() + "/playwright"); }
const { chromium } = pw;
import http from "node:http";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const SITE = path.resolve(HERE, "../../website");
const arg = (k, d) => { const i = process.argv.indexOf("--" + k); return i > 0 ? process.argv[i + 1] : d; };
const has = (k) => process.argv.includes("--" + k);
const out = arg("out", "/tmp/atelier-shots");
fs.mkdirSync(out, { recursive: true });
let routes = has("all") ? JSON.parse(fs.readFileSync(path.join(HERE, "routes.json"), "utf8")) : arg("routes", "salon").split(",");
const widths = arg("widths", "390,1400").split(",").map(Number);
const stops = +arg("stops", "3");
const tier = arg("tier", "A");
const world = arg("world", "mermer");
const fullPage = has("full");

const TYPES = { ".html": "text/html; charset=utf-8", ".webp": "image/webp", ".png": "image/png", ".mp4": "video/mp4", ".json": "application/json", ".jpg": "image/jpeg" };
const server = http.createServer((req, res) => {
  const u = decodeURIComponent(req.url.split("?")[0]);
  const f = path.join(SITE, u === "/" ? "index.html" : u);
  if (!f.startsWith(SITE) || !fs.existsSync(f) || fs.statSync(f).isDirectory()) { res.writeHead(404); return res.end(); }
  const data = fs.readFileSync(f);
  const range = req.headers.range;
  if (range && f.endsWith(".mp4")) {
    const [a, b] = range.replace("bytes=", "").split("-");
    const s = +a, e = b ? +b : data.length - 1;
    res.writeHead(206, { "Content-Range": `bytes ${s}-${e}/${data.length}`, "Accept-Ranges": "bytes", "Content-Length": e - s + 1, "Content-Type": "video/mp4" });
    return res.end(data.subarray(s, e + 1));
  }
  res.writeHead(200, { "Content-Type": TYPES[path.extname(f)] || "application/octet-stream" });
  res.end(data);
});
await new Promise((r) => server.listen(0, r));
const base = `http://127.0.0.1:${server.address().port}/`;

const browser = await chromium.launch({ executablePath: fs.existsSync("/opt/pw-browsers/chromium") ? undefined : undefined });
const report = [];
const REQ = new Set();
for (const w of widths) {
  const ctx = await browser.newContext({ viewport: { width: w, height: w < 800 ? 844 : 900 }, deviceScaleFactor: w < 800 ? 2 : 1, isMobile: w < 800, hasTouch: w < 800 });
  await ctx.route(/wa\.me|google\.com|fonts\.g|instagram|seldagencerbeauty/, (r) => r.abort());
  await ctx.addInitScript(([t, wd]) => { try { localStorage.setItem("atelier_world", wd); } catch (e) {} window.__TIER = t; }, [tier, world]);
  for (const route of routes) {
    const page = await ctx.newPage();
    const errs = [], bad = [];
    page.on("pageerror", (e) => errs.push(String(e.message || e)));
    page.on("console", (m) => { if (m.type() === "error" && !/net::ERR_FAILED/.test(m.text())) errs.push(m.text()); });
    page.on("response", (r) => { if (r.status() >= 400 && r.url().startsWith(base)) bad.push(r.status() + " " + r.url().slice(base.length)); });
    page.on("request", (q) => { const u = q.url(); if (u.startsWith(base + "m/")) REQ.add(decodeURIComponent(u.slice(base.length).split("?")[0])); });
    await page.goto(base + "index.html#" + route, { waitUntil: "load" });
    await page.evaluate((t) => { const b = document.querySelector(`[data-ctl="tier"] [data-v="${t}"]`); if (b) b.click(); document.getElementById("proto").hidden = true; }, tier);
    await page.waitForTimeout(1800);
    const slug = route.replace(/[^a-z0-9-]+/gi, "_") + "-" + w;
    if (fullPage) await page.screenshot({ path: path.join(out, slug + "-full.png"), fullPage: true });
    else await page.screenshot({ path: path.join(out, slug + "-0.png") });
    const H = await page.evaluate(() => document.documentElement.scrollHeight);
    for (let k = 1; k <= stops && !fullPage; k++) {
      await page.evaluate((y) => window.scrollTo(0, y), Math.round((H * k) / (stops + 1)));
      await page.waitForTimeout(700);
      await page.screenshot({ path: path.join(out, `${slug}-${k}.png`) });
    }
    // walk the whole page so lazy media load, then measure
    for (let y = 0; y < H; y += 700) { await page.evaluate((yy) => window.scrollTo(0, yy), y); await page.waitForTimeout(60); }
    await page.waitForTimeout(500);
    const m = await page.evaluate(() => {
      const vw = document.documentElement.clientWidth;
      const sec = document.querySelector("main > [data-view]:not([hidden])");
      const over = [];
      sec.querySelectorAll("*").forEach((el) => {
        const r = el.getBoundingClientRect();
        if (r.width && (r.right > vw + 1 || r.left < -1)) {
          let p = el.parentElement, clipped = false;
          while (p && p !== document.body) { const cs = getComputedStyle(p); if (/(auto|scroll|hidden|clip)/.test(cs.overflowX)) { const pr = p.getBoundingClientRect(); if (pr.right <= vw + 1 && pr.left >= -1) { clipped = true; break; } } p = p.parentElement; }
          if (!clipped) over.push((el.className && el.className.baseVal === undefined ? el.className : el.tagName) + " " + Math.round(r.left) + ".." + Math.round(r.right));
        }
      });
      const unl = [...sec.querySelectorAll("a,button")].filter((b) => !b.closest("[hidden]") && !b.getAttribute("data-track-label")).map((b) => (b.className || b.tagName) + ":" + (b.textContent || "").trim().slice(0, 24));
      const brokenImg = [...sec.querySelectorAll("img")].filter((i) => i.complete && i.getAttribute("src") && i.naturalWidth === 0 && !i.closest("[hidden]")).map((i) => i.getAttribute("src"));
      return { view: sec.dataset.view, docW: document.documentElement.scrollWidth, vw, over: over.slice(0, 8), unl: unl.slice(0, 12), nUnl: unl.length, brokenImg };
    });
    report.push({ route, w, errs, bad, ...m });
    console.log(`${route} @${w}: view=${m.view} errs=${errs.length} bad=${bad.length} docW=${m.docW}/${m.vw} over=${m.over.length} unlabeled=${m.nUnl} brokenImg=${m.brokenImg.length}`);
    for (const e of errs.slice(0, 5)) console.log("   ERR", e.slice(0, 200));
    for (const e of bad.slice(0, 5)) console.log("   404", e);
    for (const e of m.over.slice(0, 4)) console.log("   OVER", e);
    for (const e of m.unl.slice(0, 6)) console.log("   UNLABELED", e);
    await page.close();
  }
  await ctx.close();
}
fs.writeFileSync(path.join(out, "report.json"), JSON.stringify(report, null, 1));
fs.writeFileSync(path.join(out, "requested.json"), JSON.stringify([...REQ].sort(), null, 0));
const bad = report.filter((x) => x.errs.length || x.bad.length || x.over.length || x.nUnl || x.brokenImg.length || x.docW > x.vw);
console.log(`SUMMARY routes=${report.length} failing=${bad.length} media-requested=${REQ.size}`);
await browser.close();
server.close();
