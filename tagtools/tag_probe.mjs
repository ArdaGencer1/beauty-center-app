/**
 * Runtime tag prober.
 *
 * Drives a real browser through a page, records every Google measurement
 * request the page tries to make, and reports which conversion labels would be
 * sent and how many times.
 *
 * Measurement requests are recorded and then ABORTED. Nothing reaches Google:
 * driving the live site with a real browser would otherwise write real
 * conversions into the account and corrupt both the reporting and the bidding
 * signal. Pass --live-hits only with a deliberate reason; it is off by default
 * and the report says which mode produced it.
 */
import { chromium } from 'playwright';

const MEASUREMENT = [
  /googleads\.g\.doubleclick\.net\/pagead\//,
  /googleadservices\.com\/pagead\/conversion/,
  /google\.com(\.[a-z]{2})?\/pagead\/1p-conversion/,
  /google\.com(\.[a-z]{2})?\/pagead\/1p-user-list/,
  /google\.com(\.[a-z]{2})?\/ccm\/collect/,
  /google-analytics\.com\/g\/collect/,
  /analytics\.google\.com\/g\/collect/,
];

const args = process.argv.slice(2);
const opt = (name, fallback = null) => {
  const i = args.indexOf(`--${name}`);
  return i === -1 ? fallback : args[i + 1];
};
const has = (name) => args.includes(`--${name}`);

const url = opt('url');
const consent = opt('consent', 'granted');       // granted | denied | unset
const scenario = opt('scenario', 'load');        // load | whatsapp | phone
const liveHits = has('live-hits');
const settle = Number(opt('settle', '4000'));

if (!url) {
  console.error('usage: node tag_probe.mjs --url <url> [--consent granted|denied|unset] [--scenario load|whatsapp|phone]');
  process.exit(2);
}

/** Pull the Ads conversion label out of whichever parameter carries it. */
function labelOf(u) {
  const m = u.match(/\/(?:viewthroughconversion|1p-conversion|conversion)\/(\d+)\//);
  const id = m ? `AW-${m[1]}` : null;
  const label = new URL(u).searchParams.get('label');
  return id && label ? `${id}/${label}` : id;
}

const hits = [];
const consoleErrors = [];
// A thrown exception and a failed image are both "errors" in the console, but
// only one of them means the tag is broken. A deploy gate that cannot tell them
// apart either blocks on a stale favicon or waves through a ReferenceError.
const pageErrors = [];

const browser = await chromium.launch({ args: ['--no-sandbox'] });
const context = await browser.newContext({
  viewport: { width: 390, height: 844 },       // the traffic is overwhelmingly mobile
  userAgent:
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
});

// The site reads its own consent choice from localStorage before the tag loads.
if (consent !== 'unset') {
  await context.addInitScript(
    ([choice]) => {
      try {
        window.localStorage.setItem(
          'sgb_consent_v2',
          JSON.stringify({ version: '2026-07-21-v1', choice }),
        );
      } catch (e) { /* private mode: leave it unset */ }
    },
    [consent],
  );
}

const page = await context.newPage();

page.on('console', (msg) => {
  if (msg.type() === 'error') consoleErrors.push(msg.text());
});
page.on('pageerror', (err) => pageErrors.push(`${err.name}: ${err.message}`));

await page.route('**/*', async (route) => {
  const target = route.request().url();
  if (MEASUREMENT.some((rx) => rx.test(target))) {
    hits.push({ url: target, label: labelOf(target), t: Date.now() });
    if (!liveHits) return route.abort();
  }
  // Leaving the site would end the run before the conversion fires.
  if (/wa\.me|whatsapp\.com|whatsapp:\/\//.test(target) && route.request().isNavigationRequest()) {
    return route.abort();
  }
  return route.continue();
});

const started = Date.now();
await page.goto(url, { waitUntil: 'networkidle', timeout: 45000 }).catch(() => {});

let acted = 'none';
if (scenario === 'whatsapp') {
  const link = page.locator('a[href*="wa.me"], a[href*="whatsapp.com/send"], a[href*="api.whatsapp.com/"]').first();
  if (await link.count()) {
    await link.click({ force: true, noWaitAfter: true }).catch(() => {});
    acted = 'whatsapp-click';

    // ads-tracking.js does not fire on the click. It fires on visibilitychange:
    // hidden within 3 s of the click is "WhatsApp opened" (the Ads conversion),
    // and visible again after MIN_WA_SECONDS is "the visit was real" (the GA4
    // one). Navigation to wa.me is aborted above, so the page never backgrounds
    // on its own and neither trigger would ever run. Driving the visibility
    // state reproduces the real sequence; it proves the wiring, not that a
    // given handset behaves identically.
    const setVisibility = (hidden) =>
      page.evaluate((isHidden) => {
        Object.defineProperty(document, 'hidden', { value: isHidden, configurable: true });
        Object.defineProperty(document, 'visibilityState', {
          value: isHidden ? 'hidden' : 'visible',
          configurable: true,
        });
        document.dispatchEvent(new Event('visibilitychange'));
      }, hidden);

    await setVisibility(true);          // WhatsApp opens
    acted = 'whatsapp-click+app-switch';
    await page.waitForTimeout(9000);    // longer than MIN_WA_SECONDS
    await setVisibility(false);         // and the visitor comes back
    await page.waitForTimeout(1500);
  } else {
    acted = 'no-whatsapp-link-found';
  }
} else if (scenario === 'phone') {
  const link = page.locator('a[href^="tel:"]').first();
  if (await link.count()) {
    await link.click({ force: true, noWaitAfter: true }).catch(() => {});
    acted = 'phone-click';
  } else {
    acted = 'no-tel-link-found';
  }
}

await page.waitForTimeout(settle);

// What the tag actually ended up configured with, read from the live page.
const gtagState = await page.evaluate(() => ({
  gtag_is_function: typeof window.gtag === 'function',
  dataLayer_length: Array.isArray(window.dataLayer) ? window.dataLayer.length : null,
  wa_flag: window.SGB_GADS_WA_SENT === true,
  phone_flag: window.SGB_GADS_PHONE_SENT === true,
})).catch(() => null);

const byLabel = {};
for (const h of hits) {
  const key = h.label || 'ga4/collect';
  byLabel[key] = (byLabel[key] || 0) + 1;
}

// One conversion normally leaves over more than one transport -- the
// doubleclick view-through endpoint and the google.com first-party one carry
// the same event. Counting labels alone would read that as a double fire, so
// the endpoints are reported per label and only a repeat of the *same* one is
// a genuine duplicate.
const endpointsByLabel = {};
for (const h of hits) {
  const key = h.label || 'ga4/collect';
  const host = new URL(h.url).host;
  const path = new URL(h.url).pathname.replace(/\/\d{6,}\/?$/, '/<id>/');
  (endpointsByLabel[key] ||= []).push(`${host}${path}`);
}
const duplicates = Object.entries(endpointsByLabel)
  .map(([label, eps]) => {
    const seen = {};
    for (const e of eps) seen[e] = (seen[e] || 0) + 1;
    const repeated = Object.entries(seen).filter(([, n]) => n > 1);
    return repeated.length ? { label, repeated } : null;
  })
  .filter(Boolean);

console.log(JSON.stringify({
  url, consent, scenario, acted,
  hits_delivered_to_google: liveHits,
  elapsed_ms: Date.now() - started,
  hit_counts: byLabel,
  endpoints_by_label: endpointsByLabel,
  same_endpoint_repeats: duplicates,
  total_hits: hits.length,
  page_state: gtagState,
  page_errors: pageErrors,
  console_errors: consoleErrors.slice(0, 10),
}, null, 1));

await browser.close();
