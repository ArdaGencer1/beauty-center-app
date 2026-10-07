// Element snapshots: node snap.mjs OUT route:selector[:waitMs][:click-selector] ...  (390 px phone unless W=1400)
import { createRequire } from "node:module";
import http from "node:http";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const req = createRequire(import.meta.url);
let pw;
try { pw = req("playwright"); } catch (e) { pw = req(req("node:child_process").execSync("npm root -g").toString().trim() + "/playwright"); }
const SITE = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../../website");
const [out, ...jobs] = process.argv.slice(2);
fs.mkdirSync(out, { recursive: true });
const T = { ".html": "text/html; charset=utf-8", ".webp": "image/webp", ".png": "image/png", ".mp4": "video/mp4" };
const srv = http.createServer((q, s) => {
  const f = path.join(SITE, decodeURIComponent(q.url.split("?")[0]));
  if (!fs.existsSync(f) || fs.statSync(f).isDirectory()) { s.writeHead(404); return s.end(); }
  s.writeHead(200, { "Content-Type": T[path.extname(f)] || "application/octet-stream" }); s.end(fs.readFileSync(f));
});
await new Promise((r) => srv.listen(0, r));
const W = +(process.env.W || 390);
const b = await pw.chromium.launch();
const ctx = await b.newContext({ viewport: { width: W, height: W < 800 ? 844 : 900 }, deviceScaleFactor: W < 800 ? 2 : 1, isMobile: W < 800, hasTouch: W < 800 });
await ctx.route(/fonts\.g|wa\.me|google|instagram/, (r) => r.abort());
let n = 0;
for (const job of jobs) {
  const [route, sel, wait, click] = job.split("|");
  const pg = await ctx.newPage();
  const errs = [];
  pg.on("pageerror", (e) => errs.push(e.message));
  await pg.goto(`http://127.0.0.1:${srv.address().port}/index.html#${route}`, { waitUntil: "load" });
  await pg.evaluate(() => { document.getElementById("proto").hidden = true; });
  await pg.waitForTimeout(600);
  if (sel) { await pg.evaluate((s) => { const e = document.querySelector(s); if (e) e.scrollIntoView({ block: "center" }); }, sel); }
  if (click) { await pg.evaluate((s) => { const e = document.querySelector(s); if (e) e.click(); }, click); }
  await pg.waitForTimeout(+(wait || 2500));
  const file = path.join(out, `snap${++n}-${route.replace(/\W+/g, "_")}.png`);
  await pg.screenshot({ path: file });
  console.log(file, errs.length ? "ERR " + errs[0] : "");
  await pg.close();
}
await b.close(); srv.close();
