/**
 * Artifact measurement-surface probe (TagCtx companion for the Claude Artifact prototype).
 *
 * The Artifact has no gtag/GTM; what it measures is carried by data-track-label / data-tz-place on
 * every CTA and by the [W-XXXXXX] visit code inside the WhatsApp message. This drives a real browser
 * through the given hash routes of a locally served copy and records, per route and viewport:
 *
 *   labels    every data-track-label value (with counts) after the page has been scrolled through
 *   places    every data-tz-place value
 *   wa / tel  every wa.me and tel: href (W-codes normalised to [W-*] so runs compare)
 *   planner   the WhatsApp href the "Saatimi seç" sheet builds, and whether it carries a [W-] code
 *   errors    page exceptions and console errors; broken same-origin requests (>= 400 or failed)
 *   overflow  document scrollWidth - innerWidth (horizontal scroll on a phone)
 *   google    measurement requests the page tried to make; all are recorded and ABORTED
 *
 * Read-only: nothing is clicked except the planner button, and nothing leaves the machine.
 *
 *   node artifact_probe.mjs --base http://127.0.0.1:8765/ --routes tirnak,tirnak/kalici-oje --out a.json
 *   node artifact_probe.mjs --diff before.json after.json
 */
import { readFileSync, writeFileSync } from 'node:fs';

const args = process.argv.slice(2);
const opt = (n, d = null) => { const i = args.indexOf(`--${n}`); return i === -1 ? d : args[i + 1]; };

const MEASUREMENT = [
  /googleads\.g\.doubleclick\.net\/pagead\//, /googleadservices\.com\/pagead\/conversion/,
  /google\.com(\.[a-z]{2})?\/pagead\//, /google\.com(\.[a-z]{2})?\/ccm\/collect/,
  /google-analytics\.com\/g\/collect/, /analytics\.google\.com\/g\/collect/,
  /googletagmanager\.com\//, /facebook\.com\/tr/, /connect\.facebook\.net\//,
];
const norm = (h) => decodeURIComponent(h).replace(/\[W-[A-Z0-9]{6}\]/g, '[W-*]');

function diff(a, b) {
  const A = JSON.parse(readFileSync(a, 'utf8')), B = JSON.parse(readFileSync(b, 'utf8'));
  let bad = 0;
  const say = (lvl, msg) => { if (lvl === 'FAIL') bad++; console.log(`${lvl.padEnd(4)} ${msg}`); };
  for (const key of Object.keys(B.routes)) {
    const x = A.routes[key], y = B.routes[key];
    if (!x) { say('INFO', `${key}: new route`); continue; }
    for (const f of ['labels', 'places']) {
      const lost = Object.keys(x[f]).filter((k) => !(k in y[f]));
      const added = Object.keys(y[f]).filter((k) => !(k in x[f]));
      const moved = Object.keys(x[f]).filter((k) => k in y[f] && x[f][k] !== y[f][k]);
      if (lost.length) say('FAIL', `${key}: ${f} lost ${lost.join(', ')}`);
      if (added.length) say('INFO', `${key}: ${f} added ${added.join(', ')}`);
      if (moved.length) say('WARN', `${key}: ${f} count changed ${moved.map((k) => `${k} ${x[f][k]}->${y[f][k]}`).join(', ')}`);
    }
    for (const f of ['wa', 'tel']) {
      const lost = x[f].filter((h) => !y[f].includes(h));
      if (lost.length) say('FAIL', `${key}: ${f} href lost ${lost.join(' | ')}`);
    }
    if (x.planner.wcode && !y.planner.wcode) say('FAIL', `${key}: planner WhatsApp lost its [W-] code`);
    if (y.google.length) say('FAIL', `${key}: ${y.google.length} measurement request(s) attempted`);
    if (y.errors.length > x.errors.length) say('FAIL', `${key}: errors ${x.errors.length}->${y.errors.length}: ${y.errors.slice(0, 3).join(' | ')}`);
    if (y.broken.length) say('FAIL', `${key}: broken ${y.broken.join(', ')}`);
    if (y.overflow > 0) say('FAIL', `${key}: horizontal overflow ${y.overflow}px`);
  }
  console.log(bad ? `\n${bad} failing check(s)` : '\nno newly failing checks');
  process.exit(bad ? 1 : 0);
}

if (opt('diff')) diff(opt('diff'), args[args.indexOf('--diff') + 2]);
else {
  const { chromium } = await import('playwright');
  const base = opt('base'), out = opt('out');
  const routes = (opt('routes') || 'tirnak').split(',');
  const vp = opt('viewport', 'mobile');
  const device = vp === 'mobile'
    ? { viewport: { width: Number(opt('width', '360')), height: 780 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true }
    : { viewport: { width: 1366, height: 860 } };
  const browser = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH || undefined, args: ['--no-sandbox'] });
  const report = { base, viewport: vp, width: device.viewport.width, at: new Date().toISOString(), routes: {} };
  for (const route of routes) {
    const ctx = await browser.newContext(device);
    const page = await ctx.newPage();
    const r = { labels: {}, places: {}, wa: [], tel: [], planner: {}, errors: [], broken: [], google: [], overflow: 0 };
    const origin = new URL(base).origin;
    await page.route('**/*', (req) => {
      const u = req.request().url();
      if (MEASUREMENT.some((re) => re.test(u))) { r.google.push(u.slice(0, 120)); return req.abort(); }
      return req.continue();
    });
    page.on('pageerror', (e) => r.errors.push(`pageerror: ${e.message}`));
    page.on('console', (m) => { if (m.type() === 'error' && !/Failed to load resource/.test(m.text())) r.errors.push(`console: ${m.text()}`); });
    page.on('response', (res) => { const u = res.url(); if (u.startsWith(origin) && res.status() >= 400 && !u.endsWith('/favicon.ico')) r.broken.push(`${res.status()} ${u.slice(origin.length)}`); });
    page.on('requestfailed', (req) => { const u = req.url(); if (u.startsWith(origin) && !/ERR_ABORTED/.test(req.failure()?.errorText || '')) r.broken.push(`failed ${u.slice(origin.length)}`); });
    await page.goto(`${base}#${route}`, { waitUntil: 'load' });
    await page.waitForTimeout(900);
    // scroll through so lazy media and in-view scenes mount
    await page.evaluate(async () => {
      const step = innerHeight * 0.8;
      for (let y = 0; y < document.documentElement.scrollHeight; y += step) { scrollTo(0, y); await new Promise((f) => setTimeout(f, 120)); }
      scrollTo(0, 0);
    });
    await page.waitForTimeout(600);
    Object.assign(r, await page.evaluate(() => {
      const count = (sel, attr) => { const o = {}; document.querySelectorAll(sel).forEach((e) => { const v = e.getAttribute(attr); o[v] = (o[v] || 0) + 1; }); return o; };
      return {
        labels: count('[data-track-label]', 'data-track-label'),
        places: count('[data-tz-place]', 'data-tz-place'),
        wa: [...new Set([...document.querySelectorAll('a[href*="wa.me"]')].map((a) => a.href))],
        tel: [...new Set([...document.querySelectorAll('a[href^="tel:"]')].map((a) => a.href))],
        overflow: document.documentElement.scrollWidth - innerWidth,
      };
    }));
    r.wa = r.wa.map(norm).sort(); r.tel.sort();
    // the page's own planner button, else the sticky action bar; a DOM click, since scroll scenes keep moving it
    const opened = await page.evaluate(() => {
      const b = document.querySelector('#tzMount [data-tz-plan]') || document.querySelector('.bar .btn-gold');
      if (b) b.click(); return !!b;
    });
    if (opened) {
      await page.waitForTimeout(700);
      const href = await page.evaluate(() => { const a = document.querySelector('#sheet a[href*="wa.me"]'); return a ? a.href : null; });
      r.planner = { href: href ? norm(href).slice(0, 160) : null, wcode: !!(href && /\[W-[A-Z0-9]{6}\]/.test(decodeURIComponent(href))) };
    }
    r.broken = [...new Set(r.broken)];
    report.routes[route] = r;
    await ctx.close();
    const nl = Object.keys(r.labels).length;
    console.log(`${route.padEnd(36)} labels ${String(nl).padStart(3)}  wa ${r.wa.length}  tel ${r.tel.length}  W-code ${r.planner.wcode ? 'yes' : 'no '}  errors ${r.errors.length}  broken ${r.broken.length}  overflow ${r.overflow}  google ${r.google.length}`);
  }
  await browser.close();
  writeFileSync(out, JSON.stringify(report, null, 1));
}
