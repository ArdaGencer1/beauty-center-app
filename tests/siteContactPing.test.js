'use strict';

// First-party contact counter + campaign-coded channel marker in ads-tracking.js (2026-09-17).
// Runs only the two marked blocks, so the rest of the file needs no DOM. Before deployment point
// SGB_ADS_TRACKING_JS at the patched copy; afterwards the live file is the default.

const assert = require('node:assert/strict');
const fs = require('node:fs');
const test = require('node:test');
const vm = require('node:vm');

const SOURCE_PATH = process.env.SGB_ADS_TRACKING_JS ||
  '/var/www/seldagencerbeauty.com/public_html/ads-tracking.js';
const FULL_SOURCE = fs.readFileSync(SOURCE_PATH, 'utf8');
const START = FULL_SOURCE.indexOf('// >>> SGB_CHANNEL_MARKER');
const END_MARK = '// <<< SGB_CONTACT_PING';
const END = FULL_SOURCE.indexOf(END_MARK);
const BLOCKS = FULL_SOURCE.slice(START, END + END_MARK.length);

const GCLID = 'CjwKCA-contact-ping-test-click-1234567890';
const AD_SEARCH = `?gclid=${GCLID}&utm_source=google&utm_medium=cpc&utm_campaign=23644911563` +
  '&agid=194698056952&adid=700000000001&utm_term=lazer%20epilasyon%20fiyat&tid=kwd-298391650213' +
  '&mt=p&net=g&dev=m';

function makeAnchor(href, attrs = {}) {
  const attributes = new Map(Object.entries(attrs));
  attributes.set('href', href);
  const anchor = {
    getAttribute: (name) => (attributes.has(name) ? attributes.get(name) : null),
    setAttribute: (name, value) => attributes.set(name, String(value)),
    matches: (selector) => selector === 'a[href]',
    closest: (selector) => (selector === 'a[href]' ? anchor : null),
    querySelectorAll: () => []
  };
  return anchor;
}

function createHarness({ search = AD_SEARCH, pathname = '/laser-signature', anchors = [], fetch = true } = {}) {
  const requests = [];
  const beacons = [];
  const clickListeners = [];
  const storageTouches = [];
  const clock = { now: 1_000_000 };
  const guard = (name) => new Proxy({}, {
    get(_, prop) { storageTouches.push(`${name}.${String(prop)}`); throw new Error('storage used'); }
  });
  const document = {
    readyState: 'complete',
    body: {},
    querySelectorAll: (selector) => (selector === 'a[href]' ? anchors : []),
    addEventListener(name, callback, capture) {
      if (name === 'click') {
        assert.equal(capture, true, 'click listeners must use the capture phase');
        clickListeners.push(callback);
      }
    }
  };
  Object.defineProperty(document, 'cookie', {
    get() { storageTouches.push('cookie.get'); return ''; },
    set() { storageTouches.push('cookie.set'); }
  });
  const window = {
    location: {
      origin: 'https://seldagencerbeauty.com',
      href: `https://seldagencerbeauty.com${pathname}${search}`,
      pathname,
      search
    },
    navigator: { sendBeacon: (url) => { beacons.push(url); return true; } }
  };
  Object.defineProperty(window, 'localStorage', { get() { return guard('localStorage'); } });
  Object.defineProperty(window, 'sessionStorage', { get() { return guard('sessionStorage'); } });
  if (fetch) {
    window.fetch = (url, options) => {
      requests.push({ url, options });
      return Promise.resolve({ ok: true });
    };
  }
  class MutationObserver { observe() {} }
  vm.runInNewContext(BLOCKS, {
    window,
    document,
    MutationObserver,
    URL,
    URLSearchParams,
    Object,
    String,
    Date: { now: () => clock.now }
  });
  const pings = () => requests.map((r) => new URL(r.url, 'https://seldagencerbeauty.com'));
  return {
    window,
    requests,
    beacons,
    storageTouches,
    clock,
    pings,
    click(anchor) { clickListeners.forEach((listener) => listener({ target: anchor })); }
  };
}

test('blocks are present and in order', () => {
  assert.ok(START >= 0 && END > START, `marked blocks missing in ${SOURCE_PATH}`);
  assert.ok(BLOCKS.indexOf('SGB_CHANNEL_MARKER_BOUND') < BLOCKS.indexOf('SGB_CONTACT_PING_BOUND'));
});

test('ad landing sends one land ping with ad IDs and no click ID', () => {
  const h = createHarness();
  const pings = h.pings();
  assert.equal(pings.length, 1);
  const p = pings[0];
  assert.equal(p.pathname, '/api/public/contact-ping');
  assert.equal(p.searchParams.get('e'), 'land');
  assert.equal(p.searchParams.get('s'), 'g');
  assert.equal(p.searchParams.get('p'), '/laser-signature');
  assert.equal(p.searchParams.get('c'), '23644911563');
  assert.equal(p.searchParams.get('g'), '194698056952');
  assert.equal(p.searchParams.get('t'), 'kwd-298391650213');
  assert.equal(p.searchParams.get('k'), 'lazer epilasyon fiyat');
  assert.equal(p.searchParams.get('m'), 'p');
  assert.equal(p.searchParams.get('d'), 'm');
  assert.equal(p.searchParams.get('n'), 'g');
  assert.equal(p.searchParams.get('cc'), 'LZ');
  assert.ok(!h.requests[0].url.includes(GCLID), 'click ID must never be sent');
  assert.ok(!h.requests[0].url.includes('gclid'));
  assert.deepEqual(
    { method: h.requests[0].options.method, keepalive: h.requests[0].options.keepalive,
      credentials: h.requests[0].options.credentials, referrerPolicy: h.requests[0].options.referrerPolicy },
    { method: 'POST', keepalive: true, credentials: 'omit', referrerPolicy: 'no-referrer' }
  );
});

test('WhatsApp and phone taps are counted without any consent object', () => {
  const wa = makeAnchor('https://wa.me/905330390076?text=Merhaba');
  const tel = makeAnchor('tel:+905330390076');
  const h = createHarness({ anchors: [wa, tel] });
  assert.equal(h.window.SGBConsent, undefined);
  h.click(wa);
  h.click(tel);
  const events = h.pings().map((p) => p.searchParams.get('e'));
  assert.deepEqual(events, ['land', 'wa', 'tel']);
  h.pings().slice(1).forEach((p) => assert.equal(p.searchParams.get('c'), '23644911563'));
});

test('organic visits count taps as s=o, send no land ping and carry nothing', () => {
  const wa = makeAnchor('https://wa.me/905330390076?text=Merhaba');
  const internal = makeAnchor('/lazer-epilasyon-fiyatlari-ankara');
  const h = createHarness({ search: '', anchors: [wa, internal] });
  assert.equal(h.requests.length, 0);
  h.click(wa);
  const p = h.pings()[0];
  assert.equal(p.searchParams.get('e'), 'wa');
  assert.equal(p.searchParams.get('s'), 'o');
  assert.equal(p.searchParams.get('c'), null);
  assert.equal(p.searchParams.get('cc'), null);
  assert.equal(internal.getAttribute('href'), '/lazer-epilasyon-fiyatlari-ankara');
  assert.equal(wa.getAttribute('href'), 'https://wa.me/905330390076?text=Merhaba');
});

test('malformed ad parameters are dropped', () => {
  const h = createHarness({
    search: '?utm_source=google&utm_medium=cpc&utm_campaign=abc&agid=12x&tid=evil%3Cscript%3E' +
      '&utm_term=a%0Ab&mt=%3Cb%3E&dev=m'
  });
  const p = h.pings()[0];
  assert.equal(p.searchParams.get('s'), 'g');
  for (const key of ['c', 'g', 't', 'k', 'm', 'cc']) assert.equal(p.searchParams.get(key), null, key);
  assert.equal(p.searchParams.get('d'), 'm');
});

test('repeated taps on the same link within a second count once', () => {
  const wa = makeAnchor('https://wa.me/905330390076?text=Merhaba');
  const h = createHarness({ anchors: [wa] });
  h.click(wa);
  h.clock.now += 400;
  h.click(wa);
  h.clock.now += 1500;
  h.click(wa);
  assert.equal(h.pings().filter((p) => p.searchParams.get('e') === 'wa').length, 2);
});

test('appointment form WhatsApp is counted as waform and gets the marker at click time', () => {
  const h = createHarness();
  const temp = makeAnchor('https://wa.me/905330390076?text=Merhaba%2C%20randevu',
    { 'data-track-label': 'appointment_form_whatsapp_pref' });
  h.click(temp);
  const last = h.pings().at(-1);
  assert.equal(last.searchParams.get('e'), 'waform');
  assert.match(new URL(temp.getAttribute('href')).searchParams.get('text'), / \[G-LZ\]$/);
});

test('campaign-coded marker is added once; unknown campaign keeps [G]', () => {
  const wa = makeAnchor('https://wa.me/905330390076?text=Merhaba');
  createHarness({ anchors: [wa] });
  const text = () => new URL(wa.getAttribute('href')).searchParams.get('text');
  assert.equal(text(), 'Merhaba [G-LZ]');

  const h2 = createHarness({ anchors: [wa] });
  h2.click(wa);
  assert.equal(text(), 'Merhaba [G-LZ]', 'marker must not repeat');

  const legacy = makeAnchor('https://wa.me/905330390076?text=Merhaba%20%5BG%5D');
  createHarness({ anchors: [legacy] });
  assert.equal(new URL(legacy.getAttribute('href')).searchParams.get('text'), 'Merhaba [G]');

  const other = makeAnchor('https://wa.me/905330390076?text=Selam');
  const h3 = createHarness({ search: '?utm_source=google&utm_medium=cpc&utm_campaign=999', anchors: [other] });
  assert.equal(new URL(other.getAttribute('href')).searchParams.get('text'), 'Selam [G]');
  assert.equal(h3.pings()[0].searchParams.get('cc'), null);
});

test('internal links carry sanitised ad source, never the click ID', () => {
  const internal = makeAnchor('/lazer-epilasyon-fiyatlari-ankara#tum-vucut');
  const absolute = makeAnchor('https://seldagencerbeauty.com/eylul-firsatlari');
  const external = makeAnchor('https://www.instagram.com/seldagencerbeauty');
  const tel = makeAnchor('tel:+905330390076');
  const hash = makeAnchor('#yorumlar');
  const samePage = makeAnchor('/laser-signature#fiyat');
  const image = makeAnchor('/images/logo.webp');
  const already = makeAnchor('/cilt-bakimi?utm_source=google&utm_medium=cpc&utm_campaign=1');
  createHarness({ anchors: [internal, absolute, external, tel, hash, samePage, image, already] });

  const carried = new URL(internal.getAttribute('href'), 'https://seldagencerbeauty.com');
  assert.equal(carried.pathname, '/lazer-epilasyon-fiyatlari-ankara');
  assert.equal(carried.hash, '#tum-vucut');
  assert.equal(carried.searchParams.get('utm_source'), 'google');
  assert.equal(carried.searchParams.get('utm_medium'), 'cpc');
  assert.equal(carried.searchParams.get('utm_campaign'), '23644911563');
  assert.equal(carried.searchParams.get('agid'), '194698056952');
  assert.equal(carried.searchParams.get('tid'), 'kwd-298391650213');
  assert.ok(!internal.getAttribute('href').includes('gclid'));
  assert.ok(absolute.getAttribute('href').startsWith('/eylul-firsatlari?utm_source=google'));

  assert.equal(external.getAttribute('href'), 'https://www.instagram.com/seldagencerbeauty');
  assert.equal(tel.getAttribute('href'), 'tel:+905330390076');
  assert.equal(hash.getAttribute('href'), '#yorumlar');
  assert.equal(samePage.getAttribute('href'), '/laser-signature#fiyat');
  assert.equal(image.getAttribute('href'), '/images/logo.webp');
  const kept = new URL(already.getAttribute('href'), 'https://seldagencerbeauty.com');
  assert.equal(kept.searchParams.get('utm_campaign'), '1', 'existing parameters are not overwritten');
});

test('a visitor carried to a second page is still attributed', () => {
  const wa = makeAnchor('https://wa.me/905330390076?text=Merhaba');
  const h = createHarness({
    pathname: '/lazer-epilasyon-fiyatlari-ankara',
    search: '?utm_source=google&utm_medium=cpc&utm_campaign=23644911563&agid=194698056952&tid=kwd-298391650213',
    anchors: [wa]
  });
  h.click(wa);
  const p = h.pings().at(-1);
  assert.equal(p.searchParams.get('e'), 'wa');
  assert.equal(p.searchParams.get('s'), 'g');
  assert.equal(p.searchParams.get('c'), '23644911563');
  assert.equal(p.searchParams.get('cc'), 'LZ');
  assert.match(new URL(wa.getAttribute('href')).searchParams.get('text'), /\[G-LZ\]$/);
});

test('no storage or cookie is touched', () => {
  const wa = makeAnchor('https://wa.me/905330390076?text=Merhaba');
  const h = createHarness({ anchors: [wa, makeAnchor('/cilt-bakimi')] });
  h.click(wa);
  assert.deepEqual(h.storageTouches, []);
});

test('falls back to sendBeacon when fetch is unavailable', () => {
  const tel = makeAnchor('tel:+905330390076');
  const h = createHarness({ fetch: false, anchors: [tel] });
  h.click(tel);
  assert.equal(h.beacons.length, 2);
  assert.equal(new URL(h.beacons[1], 'https://x.invalid').searchParams.get('e'), 'tel');
});

test('non-contact links are not counted', () => {
  const plain = makeAnchor('/cilt-bakimi');
  const maps = makeAnchor('https://maps.app.goo.gl/abc');
  const h = createHarness({ search: '', anchors: [plain, maps] });
  h.click(plain);
  h.click(maps);
  h.click({ closest: () => null });
  h.click({});
  assert.equal(h.requests.length, 0);
});

// 2026-09-29: which of the page's buttons was pressed (b=), from page structure only.
test('taps carry the pressed button: its label, else its class area, and its position', () => {
  const hero = makeAnchor('https://wa.me/905330390076?text=Merhaba', { class: 'btn btn-primary' });
  const tel1 = makeAnchor('tel:+905330390076', { class: 'btn btn-secondary btn-phone' });
  const sticky = makeAnchor('https://wa.me/905330390076?text=Merhaba',
    { class: 'lp-sticky-primary', 'data-track-label': 'kas-alimi_sticky_whatsapp' });
  const float = makeAnchor('https://wa.me/905330390076?text=Merhaba', { class: 'whatsapp-float' });
  const callFloat = makeAnchor('tel:+905330390076', { class: 'call-float' });
  const h = createHarness({ anchors: [hero, tel1, sticky, float, callFloat] });
  [hero, sticky, float, callFloat].forEach((a) => { h.clock.now += 2000; h.click(a); });
  const b = h.pings().slice(1).map((p) => p.searchParams.get('b'));
  assert.deepEqual(b, ['sayfa#1', 'kas-alimi_sticky_whatsapp#2', 'whatsapp-float#3', 'call-float#2']);
  h.pings().forEach((p) => assert.ok(!String(p.searchParams.get('b') || '').includes('9053303'),
    'the button id never carries the number'));
});

test('a broken anchor never stops the tap from being counted', () => {
  const odd = makeAnchor('https://wa.me/905330390076');
  const plain = odd.getAttribute;
  odd.getAttribute = (name) => {
    if (name === 'class') throw new Error('boom');   // read only by buttonId()
    return plain(name);
  };
  const h = createHarness({ anchors: [odd] });
  h.click(odd);
  const last = h.pings().pop();
  assert.equal(last.searchParams.get('e'), 'wa');
  assert.equal(last.searchParams.get('b'), null);
});
