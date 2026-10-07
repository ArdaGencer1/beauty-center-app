#!/usr/bin/env node
// Consent bar check (D-2026-10-02 consent v3): renders site pages from DISK in headless Chromium at
// phone and desktop width and checks the KVKK/consent bar the way a visitor meets it.
//
//   node consent_check.mjs [--root DIR] [--overlay DIR] [--pages /kas-alimi,/] [--out DIR] [--bar v2|v3]
//
// Nothing leaves the machine: every same-origin request is answered from --overlay (patched files)
// then --root (default the live public_html); every other host is aborted (no Google, Meta, GA4 hits)
// and /api/public/* is answered 204 and recorded, so a run never writes a visitor row, a contact or an
// analytics hit (memory: tag_probe with a gclid pollutes first-party data).
//
// Per width it reports: bar height / share of the viewport, the buttons' computed style (equal
// prominence), what the bar covers (floats, sticky action bar), whether a WhatsApp float behind the bar
// is still tappable, JS errors; then walks each choice and reads back localStorage, the
// sgb_external_id cookie, the gtag consent commands, the beacons sent and whether a second page shows
// the bar again. Exit 1 when a hard check fails; screenshots + report.json land in --out.
import { chromium, devices } from 'playwright';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

const args = Object.fromEntries(process.argv.slice(2).reduce((acc, a, i, all) => {
  if (a.startsWith('--')) acc.push([a.slice(2), all[i + 1] && !all[i + 1].startsWith('--') ? all[i + 1] : true]);
  return acc;
}, []));
const ROOT = path.resolve(args.root || '/var/www/seldagencerbeauty.com/public_html');
const OVERLAY = args.overlay ? path.resolve(args.overlay) : '';
const PAGES = String(args.pages || '/kas-alimi,/').split(',');
const OUT = path.resolve(args.out || path.join(os.tmpdir(), 'consent_check'));
const BAR = args.bar || 'auto';
// --variant v2|v3 pins the bar of the 50/50 test (sgb_bar_variant_v1) so each bar is checked on purpose.
const VARIANT = args.variant || '';
const ORIGIN = 'https://seldagencerbeauty.com';
fs.mkdirSync(OUT, { recursive: true });

const TYPES = { '.html': 'text/html; charset=utf-8', '.js': 'application/javascript', '.css': 'text/css',
  '.svg': 'image/svg+xml', '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.webp': 'image/webp',
  '.avif': 'image/avif', '.woff2': 'font/woff2', '.woff': 'font/woff', '.ico': 'image/x-icon', '.json': 'application/json',
  '.webmanifest': 'application/manifest+json' };

function localFile(pathname) {
  const clean = decodeURIComponent(pathname).replace(/\/+$/, '') || '/index';
  const rel = clean === '/' ? '/index' : clean;
  for (const base of [OVERLAY, ROOT].filter(Boolean)) {
    for (const cand of [rel, `${rel}.html`, `${rel}/index.html`]) {
      const f = path.join(base, cand);
      if (f.startsWith(base) && fs.existsSync(f) && fs.statSync(f).isFile()) return f;
    }
  }
  return '';
}

const exe = process.env.CRM_TAB_CHROME || (() => {
  const base = path.join(os.homedir(), '.cache', 'ms-playwright');
  const dir = fs.existsSync(base) && fs.readdirSync(base).filter((d) => d.startsWith('chromium_headless_shell-')).sort().pop();
  return dir ? path.join(base, dir, 'chrome-headless-shell-linux64', 'chrome-headless-shell') : undefined;
})();
const browser = await chromium.launch(exe ? { executablePath: exe } : {});

const VIEWS = [
  ['mobile', { ...devices['iPhone 13'], viewport: { width: 390, height: 844 } }],
  ['desktop', { viewport: { width: 1400, height: 900 } }]
];
const failures = [];
const report = { root: ROOT, overlay: OVERLAY, pages: PAGES, views: {} };
const fail = (msg) => failures.push(msg);

async function newContext(opts, storage) {
  const ctx = await browser.newContext({ ...opts, locale: 'tr-TR' });
  if (VARIANT) storage = { sgb_bar_variant_v1: VARIANT, ...(storage || {}) };
  const beacons = [];
  await ctx.route('**/*', async (route) => {
    const req = route.request();
    const url = new URL(req.url());
    if (url.origin !== ORIGIN) return route.abort();
    if (url.pathname.startsWith('/api/')) {
      let body = req.postData() || '';
      try { body = JSON.parse(body); } catch { /* keep text */ }
      beacons.push({ path: url.pathname, body });
      return route.fulfill({ status: 204, body: '' });
    }
    const f = localFile(url.pathname);
    if (!f) return route.fulfill({ status: 404, body: 'not found' });
    return route.fulfill({ status: 200, body: fs.readFileSync(f), contentType: TYPES[path.extname(f)] || 'application/octet-stream' });
  });
  if (storage) {
    await ctx.addInitScript((s) => {
      try { for (const [k, v] of Object.entries(s)) window.localStorage.setItem(k, v); } catch { /* none */ }
    }, storage);
  }
  // Record gtag consent commands without loading Google: dataLayer is plain JS.
  await ctx.addInitScript(() => {
    window.__consentLog = [];
    const dl = window.dataLayer = window.dataLayer || [];
    const push = dl.push.bind(dl);
    dl.push = function (...items) {
      for (const it of items) {
        if (it && it[0] === 'consent') window.__consentLog.push([it[1], JSON.parse(JSON.stringify(it[2] || {}))]);
      }
      return push(...items);
    };
  });
  return { ctx, beacons };
}

async function open(ctx, page, url) {
  const p = await ctx.newPage();
  const errors = [];
  p.on('pageerror', (e) => errors.push(e.message));
  await p.goto(`${ORIGIN}${url}`, { waitUntil: 'load' });
  await p.waitForTimeout(600);
  return { p, errors };
}

async function barState(p) {
  return p.evaluate(() => {
    const bar = document.querySelector('.kvkk-bar:not(.is-hidden)');
    if (!bar) return null;
    const r = bar.getBoundingClientRect();
    const btns = [...bar.querySelectorAll('button')].map((b) => {
      const cs = getComputedStyle(b);
      const br = b.getBoundingClientRect();
      return { text: b.textContent.trim(), cls: b.className, w: Math.round(br.width), h: Math.round(br.height),
        bg: cs.backgroundImage !== 'none' ? cs.backgroundImage.slice(0, 60) : cs.backgroundColor,
        color: cs.color, font: cs.fontSize, weight: cs.fontWeight, border: cs.borderColor };
    });
    const floats = ['.whatsapp-float', '.call-float', '.instagram-float', '.lp-sticky-actionbar',
      '.sgb-consent-settings-button', '.scroll-cue-float'].map((sel) => {
      const el = document.querySelector(sel);
      if (!el) return null;
      const cs = getComputedStyle(el);
      const fr = el.getBoundingClientRect();
      const visible = cs.display !== 'none' && cs.visibility !== 'hidden' && Number(cs.opacity) > 0.05 && fr.width > 0;
      const overlap = visible && !(fr.right <= r.left || fr.left >= r.right || fr.bottom <= r.top || fr.top >= r.bottom);
      let tappable = null;
      if (visible) {
        const hit = document.elementFromPoint(fr.left + fr.width / 2, fr.top + fr.height / 2);
        tappable = !!hit && (hit === el || el.contains(hit));
      }
      return { sel, visible, overlap, tappable };
    }).filter(Boolean);
    return { h: Math.round(r.height), w: Math.round(r.width), top: Math.round(r.top), vh: window.innerHeight,
      share: Math.round((r.height * r.width) / (window.innerWidth * window.innerHeight) * 1000) / 10,
      text: bar.querySelector('.kvkk-bar-text')?.textContent.trim().slice(0, 300) || '', btns, floats,
      overlay: getComputedStyle(document.body).overflow === 'hidden' };
  });
}

async function readBack(ctx, p) {
  const ls = await p.evaluate(() => ({
    consent: localStorage.getItem('sgb_consent_v2'), site: localStorage.getItem('sgb_site_consent_v1'),
    variant: localStorage.getItem('sgb_bar_variant_v1'),
    cons: window.SGBConsent && window.SGBConsent.getCons ? window.SGBConsent.getCons() : (window.SGBConsent ? window.SGBConsent.getChoice() : null),
    log: window.__consentLog
  }));
  const cookies = await ctx.cookies(ORIGIN);
  return { ...ls, vidCookie: !!cookies.find((c) => c.name === 'sgb_external_id') };
}

function equalProminence(btns, label) {
  if (btns.length < 2) return;
  const [a, ...rest] = btns;
  for (const b of rest) {
    for (const k of ['bg', 'color', 'font', 'weight']) {
      if (a[k] !== b[k]) fail(`${label}: "${a.text}" ve "${b.text}" farklı ${k}: ${a[k]} / ${b[k]}`);
    }
    if (Math.abs(a.h - b.h) > 1) fail(`${label}: buton yükseklikleri farklı ${a.h}/${b.h}`);
  }
}

for (const [name, opts] of VIEWS) {
  const view = report.views[name] = { pages: {}, flows: {} };
  for (const url of PAGES) {
    const { ctx, beacons } = await newContext(opts);
    const { p, errors } = await open(ctx, null, url);
    const st = await barState(p);
    await p.screenshot({ path: path.join(OUT, `${name}${url.replace(/\//g, '_') || '_root'}.png`) });
    view.pages[url] = { bar: st, errors, beacons: beacons.length };
    const label = `${name} ${url}`;
    if (errors.length) fail(`${label}: JS hatası ${errors.join(' | ').slice(0, 200)}`);
    if (!st) { fail(`${label}: çubuk görünmüyor`); await ctx.close(); continue; }
    if (st.overlay) fail(`${label}: çubuk sayfayı kilitliyor (body overflow hidden)`);
    if (name === 'mobile' && st.h > 150) fail(`${label}: mobil çubuk ${st.h}px (> 150)`);
    if (name === 'mobile') for (const b of st.btns) if (b.h < 44) view.pages[url].small_targets = (view.pages[url].small_targets || []).concat(`${b.text} ${b.h}px`);
    for (const f of st.floats) {
      if (f.overlap && f.sel !== '.scroll-cue-float') view.pages[url].overlaps = (view.pages[url].overlaps || []).concat(f.sel);
      if (f.sel === '.whatsapp-float' && f.visible && f.tappable === false) fail(`${label}: WhatsApp düğmesi çubuk açıkken tıklanamıyor`);
      if (BAR === 'v3' && ['.call-float', '.lp-sticky-actionbar'].includes(f.sel) && f.visible && f.tappable === false) fail(`${label}: ${f.sel} çubuk açıkken tıklanamıyor`);
    }
    if (BAR === 'v3') {
      equalProminence(st.btns, label);
      if (st.btns.length !== 3) fail(`${label}: ${st.btns.length} buton (3 bekleniyor)`);
      if (name === 'mobile') for (const b of st.btns) if (b.h < 44) fail(`${label}: ${b.text} ${b.h}px (< 44)`);
    }
    await ctx.close();
  }

  // Flows on the first page: each button, then a second page.
  const url = PAGES[0];
  const choices = BAR === 'v3' ? ['granted', 'denied', 'site'] : ['granted', 'denied'];
  for (const choice of choices) {
    const { ctx, beacons } = await newContext(opts);
    const { p, errors } = await open(ctx, null, url);
    if (choice === 'site') {
      await p.click('.kvkk-bar [data-consent="prefs"]');
      await p.waitForSelector('.sgb-prefs', { timeout: 3000 }).catch(() => fail(`${name}: Tercihler paneli açılmadı`));
      await p.screenshot({ path: path.join(OUT, `${name}_prefs.png`) });
      await p.evaluate(() => {
        const set = (n, v) => { const el = document.querySelector(`.sgb-prefs input[name="${n}"]`); if (el) el.checked = v; };
        set('ads', false); set('site', true);
      });
      await p.click('.sgb-prefs [data-prefs="save"]');
    } else {
      await p.click(`.kvkk-bar [data-consent="${choice}"]`);
    }
    await p.waitForTimeout(500);
    const after = await readBack(ctx, p);
    // tap a WhatsApp link: does it carry the visit code?
    const wa = await p.evaluate(() => {
      const a = [...document.querySelectorAll('a[href]')].find((x) => /wa\.me|whatsapp/i.test(x.getAttribute('href')));
      if (!a) return null;
      a.addEventListener('click', (e) => e.preventDefault(), { once: true });
      a.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true }));
      return a.getAttribute('href');
    });
    const { p: p2 } = await open(ctx, null, PAGES[1] || '/');
    const again = await barState(p2);
    view.flows[choice] = { ...after, wa_has_code: wa ? /W-[0-9A-Z]{6}/.test(decodeURIComponent(wa)) : null,
      bar_again: !!again, errors, beacons: beacons.map((b) => b.body && b.body.e ? `${b.body.e}:${b.body.cons || b.body.v || ''}${b.body.vid ? '+vid' : ''}${b.body.bv ? ':' + b.body.bv : ''}` : b.path) };
    const lab = `${name} ${choice}`;
    if (again) fail(`${lab}: ikinci sayfada çubuk yine çıktı`);
    if (errors.length) fail(`${lab}: JS hatası ${errors.join(' | ').slice(0, 200)}`);
    const lastUpdate = (after.log || []).filter((l) => l[0] === 'update').pop();
    const adsState = lastUpdate ? lastUpdate[1].ad_storage : null;
    if (choice === 'granted' && adsState !== 'granted') fail(`${lab}: Google onayı granted değil (${adsState})`);
    if ((choice === 'denied' || choice === 'site') && adsState !== 'denied') fail(`${lab}: Google onayı denied değil (${adsState})`);
    if (choice === 'denied' && after.vidCookie) {
      // a cookie written before the click may remain; the beacons must not carry it after the choice
      view.flows[choice].note = 'sgb_external_id çerezi seçimden önce yazılmış olabilir';
    }
    if (choice === 'denied' && view.flows[choice].wa_has_code) fail(`${lab}: Reddet sonrası WhatsApp linkinde ziyaret kodu var`);
    if (choice === 'site' && view.flows[choice].wa_has_code === false) fail(`${lab}: yalnız site ölçümünde WhatsApp kodu yok`);
    await ctx.close();
  }

  if (BAR === 'v3') {
    // after a choice the "Çerez tercihleri" link opens the preferences straight away; Esc closes them
    const { ctx } = await newContext(opts, { sgb_consent_v2: JSON.stringify({ version: '2026-07-21-v1', choice: 'denied' }),
      sgb_site_consent_v1: JSON.stringify({ choice: 'granted' }) });
    const { p, errors } = await open(ctx, null, url);
    if (await barState(p)) fail(`${name}: seçim varken çubuk yine çıktı`);
    // since 2026-10-02 the control is a link at the bottom of the page (was a floating button)
    await p.click('.sgb-consent-link');
    const opened = await p.waitForSelector('.sgb-prefs', { timeout: 3000 }).then(() => true).catch(() => false);
    const states = opened ? await p.evaluate(() => ({
      site: document.querySelector('.sgb-prefs input[name="site"]').checked,
      ads: document.querySelector('.sgb-prefs input[name="ads"]').checked,
      focus: document.activeElement && document.activeElement.getAttribute('name') })) : null;
    if (opened) await p.screenshot({ path: path.join(OUT, `${name}_settings_prefs.png`) });
    await p.keyboard.press('Escape');
    const closed = await p.evaluate(() => !document.querySelector('.sgb-prefs'));
    view.settings = { opened, states, closed, errors };
    if (!opened) fail(`${name}: Çerez tercihleri paneli açmadı`);
    else if (!(states.site === true && states.ads === false)) fail(`${name}: panel o anki durumu göstermiyor ${JSON.stringify(states)}`);
    if (!closed) fail(`${name}: Esc paneli kapatmadı`);
    await ctx.close();
  }
}

await browser.close();
report.failures = failures;
fs.writeFileSync(path.join(OUT, 'report.json'), JSON.stringify(report, null, 2));
console.log(JSON.stringify(report, null, 1).slice(0, 12000));
console.log(failures.length ? `FAIL ${failures.length}\n- ${failures.join('\n- ')}` : 'PASS');
process.exit(failures.length ? 1 : 0);
