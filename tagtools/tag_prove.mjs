/**
 * Per-button conversion-request proof.
 *
 * `tag_coverage.mjs` proves every anchor is BOUND. This proves the stronger
 * claim: clicking it actually produces a well-formed Google Ads conversion
 * request, and names the exact id, label, value and currency that request
 * carries.
 *
 * It is fast enough to run every button on every page because of how
 * ads-tracking.js actually works:
 *
 *   phone     fireGoogleAdsPhoneConversion() runs synchronously in the click
 *             handler, guarded by window.SGB_GADS_PHONE_SENT
 *   whatsapp  fireGoogleAdsWaConversion('whatsapp_open') runs on
 *             visibilitychange->hidden within 3 s of the click, guarded by
 *             window.SGB_GADS_WA_SENT. The 8-second MIN_WA_SECONDS gate is
 *             only for the secondary GA4 micro-signal, NOT for the Ads
 *             conversion -- so no 9-second wait per button is needed.
 *
 * Both guards are one-per-session by design (the account counts these
 * ONE_PER_CLICK). Resetting the flag between buttons is what lets each button
 * be judged on its own instead of every button after the first reporting as
 * dead.
 *
 * By default measurement requests are recorded and ABORTED -- nothing reaches
 * Google. --live-hits lets them through and reports the HTTP status Google
 * returned; use it deliberately, and read the note in the report about why a
 * ping from a browser that never clicked an ad is not a recorded conversion.
 */
import { chromium } from 'playwright';
import { readFileSync } from 'node:fs';

const CONV_RE = /googleadservices\.com\/pagead\/conversion\/|\/pagead\/1p-conversion\//;
const ANY_MEASUREMENT = /googleads\.g\.doubleclick\.net\/pagead\/|googleadservices\.com\/pagead\/|\/pagead\/1p-conversion\/|\/ccm\/collect|google-analytics\.com\/g\/collect|analytics\.google\.com\/g\/collect/;

const args = process.argv.slice(2);
const opt = (n, d = null) => { const i = args.indexOf(`--${n}`); return i === -1 ? d : args[i + 1]; };
const has = (n) => args.includes(`--${n}`);

const urlsFile = opt('urls');
const single = opt('url');
const liveHits = has('live-hits');
const concurrency = Number(opt('concurrency', '3'));
if (!urlsFile && !single) { console.error('usage: node tag_prove.mjs --urls <file> | --url <url>'); process.exit(2); }
const urls = single ? [single] : readFileSync(urlsFile, 'utf8').split('\n').map((s) => s.trim()).filter(Boolean);

const WA_SEL = 'a[href*="wa.me"], a[href*="whatsapp.com/send"], a[href*="api.whatsapp.com/"]';
const TEL_SEL = 'a[href^="tel:"]';

function parseConv(u) {
  try {
    const url = new URL(u);
    const m = url.pathname.match(/\/(?:1p-)?conversion\/(\d+)\//);
    const q = url.searchParams;
    return {
      host: url.hostname,
      id: m ? m[1] : null,
      label: q.get('label'),
      value: q.get('value'),
      currency: q.get('currency'),
    };
  } catch { return null; }
}

const browser = await chromium.launch({ args: ['--no-sandbox'] });

async function provePage(url) {
  const recorded = [];
  const statuses = [];
  const context = await browser.newContext({
    viewport: { width: 390, height: 844 },
    userAgent:
      'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 '
      + '(KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
  });
  await context.addInitScript(() => {
    try {
      window.localStorage.setItem('sgb_consent_v2',
        JSON.stringify({ version: '2026-07-21-v1', choice: 'granted' }));
    } catch (e) { /* private mode */ }
    // tel: navigation would tear the page down mid-beacon; suppress only the
    // navigation, in the capture phase, so the site's own click listener still
    // runs and still fires the conversion.
    document.addEventListener('click', (e) => {
      const a = e.target && e.target.closest && e.target.closest('a[href^="tel:"]');
      if (a) e.preventDefault();
    }, true);
  });
  const page = await context.newPage();
  const pageErrors = [];
  page.on('pageerror', (e) => pageErrors.push(`${e.name}: ${e.message}`));
  if (liveHits) {
    page.on('response', (r) => {
      if (CONV_RE.test(r.url())) statuses.push({ url: r.url(), status: r.status() });
    });
  }
  await page.route('**/*', (route) => {
    const t = route.request().url();
    if (ANY_MEASUREMENT.test(t)) {
      if (CONV_RE.test(t)) recorded.push(t);
      if (!liveHits) return route.abort();
      return route.continue();
    }
    if (/wa\.me|whatsapp\.com/.test(t) && route.request().isNavigationRequest()) return route.abort();
    return route.continue();
  });

  let nav = 'ok';
  await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 45000 })
    .catch((e) => { nav = `nav-error: ${e.message.slice(0, 50)}`; });
  await page.waitForTimeout(2600);

  const counts = await page.evaluate(([wa, tel]) => ({
    wa: document.querySelectorAll(wa).length,
    tel: document.querySelectorAll(tel).length,
  }), [WA_SEL, TEL_SEL]);

  const buttons = [];

  async function fire(kind, i) {
    const before = recorded.length;
    const sel = kind === 'wa' ? WA_SEL : TEL_SEL;
    const info = await page.evaluate(([s, idx, k]) => {
      // Reset the one-per-session guards so this button is judged on its own.
      window.SGB_GADS_PHONE_SENT = false;
      window.SGB_GADS_WA_SENT = false;
      window.SGB_WA_CONVERSION_SENT = false;
      const el = document.querySelectorAll(s)[idx];
      if (!el) return null;
      const d = {
        text: (el.innerText || el.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 40),
        cls: (el.className || '').toString().slice(0, 40),
        href: (el.getAttribute('href') || '').slice(0, 50),
        bound: el.dataset.sgbIntentBound === 'true',
        visible: !!(el.offsetParent || el.getClientRects().length),
      };
      el.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true }));
      if (k === 'wa') {
        Object.defineProperty(document, 'hidden', { value: true, configurable: true });
        Object.defineProperty(document, 'visibilityState', { value: 'hidden', configurable: true });
        document.dispatchEvent(new Event('visibilitychange'));
      }
      return d;
    }, [sel, i, kind]).catch(() => null);

    await page.waitForTimeout(kind === 'wa' ? 550 : 320);

    if (kind === 'wa') {
      await page.evaluate(() => {
        Object.defineProperty(document, 'hidden', { value: false, configurable: true });
        Object.defineProperty(document, 'visibilityState', { value: 'visible', configurable: true });
        document.dispatchEvent(new Event('visibilitychange'));
      }).catch(() => {});
      await page.waitForTimeout(80);
    }

    const fresh = recorded.slice(before).map(parseConv).filter(Boolean);
    buttons.push({
      kind: kind === 'wa' ? 'whatsapp' : 'phone',
      index: i,
      ...(info || { missing: true }),
      requests: fresh.length,
      hosts: [...new Set(fresh.map((f) => f.host))],
      id: [...new Set(fresh.map((f) => f.id))][0] || null,
      label: [...new Set(fresh.map((f) => f.label))][0] || null,
      value: [...new Set(fresh.map((f) => f.value))][0] || null,
      currency: [...new Set(fresh.map((f) => f.currency))][0] || null,
    });
  }

  // --max bounds how many of each kind are exercised. It exists for --live-hits
  // runs, where every button tested is a real request leaving for Google.
  const max = Number(opt('max', '0')) || Infinity;
  for (let i = 0; i < Math.min(counts.tel, max); i += 1) await fire('tel', i);
  for (let i = 0; i < Math.min(counts.wa, max); i += 1) await fire('wa', i);

  await context.close();
  return { url, nav, pageErrors, counts, buttons, statuses };
}

const results = [];
let cursor = 0;
async function worker() {
  for (;;) {
    const i = cursor; cursor += 1;
    if (i >= urls.length) return;
    try { results.push(await provePage(urls[i])); }
    catch (e) { results.push({ url: urls[i], nav: `crash: ${e.message.slice(0, 70)}`, buttons: [], counts: { wa: 0, tel: 0 }, pageErrors: [], statuses: [] }); }
  }
}
await Promise.all(Array.from({ length: concurrency }, worker));
await browser.close();

results.sort((a, b) => a.url.localeCompare(b.url));
console.log(JSON.stringify({ liveHits, count: results.length, pages: results }, null, 1));
