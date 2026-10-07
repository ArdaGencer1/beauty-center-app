/**
 * Per-page measurement coverage.
 *
 * Clicking every button on every page is not a test anyone can run: 107 pages
 * carry ~3000 WhatsApp / tel: anchors and the WhatsApp conversion needs a
 * 9-second app-switch each. So this asks the question that actually decides
 * whether a button works, and asks it of every single one:
 *
 *   is this anchor BOUND to the conversion handler?
 *
 * `ads-tracking.js` stamps `data-sgb-intent-bound="true"` on each anchor it
 * binds, and the handler it attaches is identical for all of them. An anchor
 * carrying the stamp fires; one without it cannot. Clicking proves the
 * mechanism once; the stamp proves the coverage everywhere.
 *
 * Also reports, per page: whether the Ads destination got configured, whether
 * the page threw, which lead helpers are live, and every <form> with its id --
 * form tracking is bound to `#contactForm` alone (script.js:1608), so a form
 * under any other id is measured by nothing.
 *
 * Measurement requests are recorded and ABORTED. Nothing reaches Google.
 */
import { chromium } from 'playwright';
import { readFileSync } from 'node:fs';

const AW = 'AW-11538067972';
const MEASUREMENT = [
  /googleads\.g\.doubleclick\.net\/pagead\//,
  /googleadservices\.com\/pagead\/conversion/,
  /google\.com(\.[a-z]{2})?\/pagead\/1p-conversion/,
  /google\.com(\.[a-z]{2})?\/ccm\/collect/,
  /google-analytics\.com\/g\/collect/,
  /analytics\.google\.com\/g\/collect/,
];

const args = process.argv.slice(2);
const opt = (n, d = null) => { const i = args.indexOf(`--${n}`); return i === -1 ? d : args[i + 1]; };
const urlsFile = opt('urls');
const concurrency = Number(opt('concurrency', '4'));
const settle = Number(opt('settle', '2800'));
if (!urlsFile) { console.error('usage: node tag_coverage.mjs --urls <file>'); process.exit(2); }

const urls = readFileSync(urlsFile, 'utf8').split('\n').map((s) => s.trim()).filter(Boolean);
const browser = await chromium.launch({ args: ['--no-sandbox'] });

async function auditOne(url) {
  const hits = [];
  const pageErrors = [];
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
  });
  const page = await context.newPage();
  page.on('pageerror', (e) => pageErrors.push(`${e.name}: ${e.message}`));
  await page.route('**/*', (route) => {
    const t = route.request().url();
    if (MEASUREMENT.some((rx) => rx.test(t))) { hits.push(t); return route.abort(); }
    return route.continue();
  });

  let nav = 'ok';
  await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 45000 })
    .catch((e) => { nav = `nav-error: ${e.message.slice(0, 60)}`; });
  await page.waitForTimeout(settle);

  const state = await page.evaluate(() => {
    const SEL = 'a[href^="tel:"], a[href*="wa.me"], a[href*="whatsapp.com/send"], a[href*="api.whatsapp.com/"]';
    const anchors = [...document.querySelectorAll(SEL)].map((el) => {
      const href = el.getAttribute('href') || '';
      return {
        kind: href.startsWith('tel:') ? 'phone' : 'whatsapp',
        bound: el.dataset.sgbIntentBound === 'true',
        lead: el.hasAttribute('data-lead-bound'),
        visible: !!(el.offsetParent || el.getClientRects().length),
        text: (el.innerText || el.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 34),
        cls: (el.className || '').toString().slice(0, 40),
      };
    });
    const forms = [...document.querySelectorAll('form')].map((f) => ({
      id: f.getAttribute('id') || '',
      action: f.getAttribute('action') || '',
      fields: f.querySelectorAll('input,select,textarea').length,
    }));
    return {
      anchors,
      forms,
      gtag: typeof window.gtag,
      serviceValue: typeof window.SGBServiceValue,
      trackLead: typeof window.trackLeadConversion,
      bindLead: typeof window.bindLeadTracking,
      intentBound: window.SGB_LANDING_INTENT_BOUND === true,
    };
  }).catch(() => null);

  await context.close();

  const awConfigured = hits.some((h) => h.includes('/11538067972/'));
  return { url, nav, pageErrors, awConfigured, ...(state || { anchors: [], forms: [], broken: true }) };
}

const results = [];
let cursor = 0;
async function worker() {
  for (;;) {
    const i = cursor; cursor += 1;
    if (i >= urls.length) return;
    try { results.push(await auditOne(urls[i])); }
    catch (e) { results.push({ url: urls[i], nav: `crash: ${e.message.slice(0, 80)}`, anchors: [], forms: [], pageErrors: [] }); }
  }
}
await Promise.all(Array.from({ length: concurrency }, worker));
await browser.close();

results.sort((a, b) => a.url.localeCompare(b.url));
console.log(JSON.stringify({ count: results.length, pages: results }, null, 1));
