/**
 * Per-button runtime prober.
 *
 * `tag_probe.mjs` clicks the FIRST WhatsApp or tel: link on a page. Real pages
 * here carry several of each -- hero CTA, sticky bar, footer NAP, offer cards --
 * and a conversion that fires from the hero proves nothing about the footer.
 * This walks every one of them.
 *
 * Each link is tested in a FRESH browser context, because ads-tracking.js
 * de-duplicates: once a WhatsApp conversion has been sent in a session, later
 * clicks are deliberately silent. Sharing one context would therefore report
 * every button after the first as broken when the truth is the opposite. A
 * fresh context resets the flag, so each button is judged on its own.
 *
 * Measurement requests are recorded and then ABORTED -- nothing reaches Google.
 */
import { chromium } from 'playwright';

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

const url = opt('url');
const consent = opt('consent', 'granted');
const settle = Number(opt('settle', '3500'));
const waWait = Number(opt('wa-wait', '9000'));
if (!url) { console.error('usage: node tag_probe_all.mjs --url <url>'); process.exit(2); }

const WA_SEL = 'a[href*="wa.me"], a[href*="whatsapp.com/send"], a[href*="api.whatsapp.com/"]';
const TEL_SEL = 'a[href^="tel:"]';

function labelOf(u) {
  const m = u.match(/\/(?:viewthroughconversion|1p-conversion|conversion)\/(\d+)\//);
  const id = m ? `AW-${m[1]}` : null;
  let label = null;
  try { label = new URL(u).searchParams.get('label'); } catch { /* ignore */ }
  return id && label ? `${id}/${label}` : id;
}

const browser = await chromium.launch({ args: ['--no-sandbox'] });

async function newPage(sink) {
  const context = await browser.newContext({
    viewport: { width: 390, height: 844 },
    userAgent:
      'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 '
      + '(KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
  });
  if (consent !== 'unset') {
    await context.addInitScript(([choice]) => {
      try {
        window.localStorage.setItem('sgb_consent_v2',
          JSON.stringify({ version: '2026-07-21-v1', choice }));
      } catch (e) { /* private mode */ }
    }, [consent]);
  }
  // A tel: click navigates to an external protocol handler, which can tear the
  // page down before the conversion beacon leaves -- reporting a button as
  // broken when it fired correctly. page.route() cannot intercept non-http
  // schemes, so the navigation is cancelled in the page instead. This runs in
  // the CAPTURE phase, so the site's own click listener (bound on the anchor,
  // bubble phase, {passive:true}) still runs and still fires the conversion:
  // only the navigation is suppressed, never the measurement.
  await context.addInitScript(() => {
    document.addEventListener('click', (e) => {
      const a = e.target && e.target.closest && e.target.closest('a[href^="tel:"]');
      if (a) e.preventDefault();
    }, true);
  });
  const page = await context.newPage();
  page.on('pageerror', (e) => sink.pageErrors.push(`${e.name}: ${e.message}`));
  await page.route('**/*', async (route) => {
    const t = route.request().url();
    if (MEASUREMENT.some((rx) => rx.test(t))) {
      sink.hits.push({ url: t, label: labelOf(t) });
      return route.abort();
    }
    // Leaving for WhatsApp would end the run before the conversion fires.
    if (/wa\.me|whatsapp\.com|whatsapp:\/\//.test(t) && route.request().isNavigationRequest()) {
      return route.abort();
    }
    return route.continue();
  });
  return { page, context };
}

// -- inventory: what buttons does this page actually have? --------------------
const inv = { hits: [], pageErrors: [] };
const first = await newPage(inv);
await first.page.goto(url, { waitUntil: 'networkidle', timeout: 45000 }).catch(() => {});

const describe = (sel) => first.page.$$eval(sel, (els) => els.map((el) => ({
  href: el.getAttribute('href') || '',
  text: (el.innerText || el.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 42),
  aria: el.getAttribute('aria-label') || '',
  cls: (el.className || '').toString().slice(0, 48),
  visible: !!(el.offsetParent || el.getClientRects().length),
})));

const waLinks = await describe(WA_SEL);
const telLinks = await describe(TEL_SEL);
const loadErrors = [...inv.pageErrors];
await first.context.close();

// -- test each button in its own session --------------------------------------
async function testOne(kind, index) {
  const sink = { hits: [], pageErrors: [] };
  const { page, context } = await newPage(sink);
  await page.goto(url, { waitUntil: 'networkidle', timeout: 45000 }).catch(() => {});
  const sel = kind === 'wa' ? WA_SEL : TEL_SEL;
  // sgb-offers.js injects CTAs after load, so an index captured on one page
  // load can point at a different anchor on the next. The descriptor is read
  // from the same page instance that is clicked, so the report always names
  // the button that was actually exercised.
  const seen = await page.$$eval(sel, (els, i) => {
    const el = els[i];
    if (!el) return null;
    return {
      href: el.getAttribute('href') || '',
      text: (el.innerText || el.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 42),
      cls: (el.className || '').toString().slice(0, 48),
      visible: !!(el.offsetParent || el.getClientRects().length),
      bound: el.dataset.sgbIntentBound === 'true',
    };
  }, index).catch(() => null);
  const link = page.locator(sel).nth(index);
  let acted = 'none';
  if (await link.count()) {
    // A forced click fires at the element's coordinates without scrolling, so
    // a footer anchor at y=4389 in an 844px viewport was clicked into empty
    // space and reported as a dead button -- a defect in the test, not the
    // site. Scroll it into view and click normally; fall back to dispatching
    // the event on the element itself, which is what the handler listens for.
    await link.scrollIntoViewIfNeeded({ timeout: 4000 }).catch(() => {});
    const clicked = await link.click({ noWaitAfter: true, timeout: 5000 })
      .then(() => true).catch(() => false);
    if (!clicked) {
      await page.$$eval(sel, (els, i) => {
        const el = els[i];
        if (el) el.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true }));
      }, index).catch(() => {});
    }
    acted = clicked ? 'click' : 'dispatch';
    if (kind === 'wa') {
      // ads-tracking.js fires on visibilitychange, not on the click itself:
      // hidden within 3 s means "WhatsApp opened". Navigation is aborted above,
      // so the page never backgrounds on its own and the trigger would never run.
      const vis = (hidden) => page.evaluate((h) => {
        Object.defineProperty(document, 'hidden', { value: h, configurable: true });
        Object.defineProperty(document, 'visibilityState',
          { value: h ? 'hidden' : 'visible', configurable: true });
        document.dispatchEvent(new Event('visibilitychange'));
      }, hidden);
      await vis(true);
      acted = 'click+app-switch';
      await page.waitForTimeout(waWait);
      await vis(false);
      await page.waitForTimeout(1200);
    }
  } else {
    acted = 'link-not-found';
  }
  await page.waitForTimeout(settle);
  const labels = [...new Set(sink.hits.map((h) => h.label).filter((l) => l && l.includes('/')))];
  await context.close();
  return { acted, labels, pageErrors: sink.pageErrors, seen };
}

// A page can carry 25 WhatsApp buttons and each needs a 9-second app-switch.
// --max samples the first N of each kind so several pages can be covered in
// one run; binding coverage for the rest comes from tag_coverage.mjs.
const max = Number(opt('max', '0')) || Infinity;

const results = [];
for (let i = 0; i < Math.min(waLinks.length, max); i += 1) {
  const r = await testOne('wa', i);
  results.push({ kind: 'whatsapp', index: i, ...waLinks[i], ...r });
}
for (let i = 0; i < Math.min(telLinks.length, max); i += 1) {
  const r = await testOne('tel', i);
  results.push({ kind: 'phone', index: i, ...telLinks[i], ...r });
}

await browser.close();

console.log(JSON.stringify({
  url,
  consent,
  load_page_errors: loadErrors,
  counts: { whatsapp: waLinks.length, phone: telLinks.length },
  buttons: results,
}, null, 1));
