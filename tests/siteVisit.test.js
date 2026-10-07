'use strict';

// SGB_VISIT block of ads-tracking.js (site visitor store, D-2026-09-30-01 E). Runs only that block
// in a fake browser. Before deployment point SGB_ADS_TRACKING_JS at the patched copy
// (patches/site_visit_20260930/ads-tracking.js); afterwards the live file is the default.

const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');
const vm = require('node:vm');

const SOURCE_PATH = process.env.SGB_ADS_TRACKING_JS ||
  '/var/www/seldagencerbeauty.com/public_html/ads-tracking.js';
const FULL = fs.readFileSync(SOURCE_PATH, 'utf8');
const START = FULL.indexOf('// >>> SGB_VISIT');
const END_MARK = '// <<< SGB_VISIT';
const BLOCK = START >= 0 ? FULL.slice(START, FULL.indexOf(END_MARK) + END_MARK.length) : '';
const CRM_SERVICE = path.join(__dirname, '..', 'data', 'change_plans', '20260930-site-visitors',
  'new', 'backend', 'services', 'siteVisitService.js');

function anchor(href, attrs = {}) {
  const a = new Map(Object.entries(attrs));
  a.set('href', href);
  const el = {
    nodeType: 1,
    getAttribute: (n) => (a.has(n) ? a.get(n) : null),
    setAttribute: (n, v) => a.set(n, String(v)),
    matches: (sel) => sel === 'a[href]',
    closest: (sel) => (sel === 'a[href]' ? el : null),
    querySelectorAll: () => []
  };
  return el;
}

function harness({ search = '', pathname = '/kas-alimi', referrer = '', choice = 'unset', cookie = '',
                   anchors = [], width = 390, api = null, storage = {} } = {}) {
  const posts = [];
  const winL = {};
  const docL = {};
  const intervals = [];
  const clock = { now: 1_727_700_000_000 };
  let jar = cookie;
  const document = {
    readyState: 'complete', referrer, visibilityState: 'visible', body: { scrollHeight: 2000 },
    documentElement: { scrollHeight: 2000 },
    querySelectorAll: (sel) => (sel === 'a[href]' ? anchors : []),
    addEventListener: (n, cb) => { (docL[n] = docL[n] || []).push(cb); }
  };
  Object.defineProperty(document, 'cookie', { get: () => jar, set: (v) => { jar = String(v).split(';')[0]; } });
  class FakeDate extends Date { static now() { return clock.now; } }
  const window = {
    location: { search, pathname, hostname: 'seldagencerbeauty.com', origin: 'https://seldagencerbeauty.com',
                href: `https://seldagencerbeauty.com${pathname}${search}`, protocol: 'https:' },
    innerWidth: width, innerHeight: 800, scrollY: 0,
    SGBConsent: api || { getChoice: () => choice },
    crypto: { getRandomValues: (arr) => { for (let i = 0; i < arr.length; i += 1) arr[i] = 123456789 + i; return arr; } },
    localStorage: { getItem: (k) => (k in storage ? storage[k] : null) },
    addEventListener: (n, cb) => { (winL[n] = winL[n] || []).push(cb); },
    setInterval: (fn) => { intervals.push(fn); return intervals.length; }
  };
  const navigator = { sendBeacon: (url, blob) => { posts.push({ url, body: JSON.parse(blob.text) }); return true; } };
  class Blob { constructor(parts) { this.text = parts.join(''); } }
  class MutationObserver { observe() {} }
  const ctx = { window, document, navigator, Blob, MutationObserver, URL, URLSearchParams, Date: FakeDate, Math, JSON,
                String, Number, Uint32Array, console };
  vm.createContext(ctx);
  vm.runInContext(BLOCK, ctx);
  return {
    posts, window, document, clock, anchors, cookie: () => jar,
    tick(n = 1, active = true) {
      for (let i = 0; i < n; i += 1) {
        clock.now += 1000;
        if (active) (winL.pointerdown || []).forEach((cb) => cb({}));
        intervals.forEach((fn) => fn());
      }
    },
    hide() { document.visibilityState = 'hidden'; (docL.visibilitychange || []).forEach((cb) => cb()); },
    show() { document.visibilityState = 'visible'; (docL.visibilitychange || []).forEach((cb) => cb()); },
    click(el) { (docL.click || []).forEach((cb) => cb({ target: el })); },
    emit(name, detail) { (docL[name] || []).forEach((cb) => cb({ detail })); }
  };
}

test('the block exists in the file under test', () => {
  assert.ok(BLOCK.includes('SGB_VISIT_BOUND'), `no SGB_VISIT block in ${SOURCE_PATH}`);
});

test('an organic visit lands with a visitor id and a cookie', () => {
  const h = harness({ referrer: 'https://www.google.com/' });
  const land = h.posts[0].body;
  assert.equal(h.posts[0].url, '/api/public/site-events');
  assert.equal(land.e, 'land');
  assert.equal(land.src, 'organic');
  assert.equal(land.refh, 'www.google.com');
  assert.match(land.vid, /^sgb\.1\.\d{10,14}\.\d{3,30}$/);
  assert.match(h.cookie(), /^sgb_external_id=/);
  assert.equal(land.d, 'm');
  assert.equal(land.cons, 'unset');
});

test('Reddet: no id, no cookie, no visit code in WhatsApp text', () => {
  const wa = anchor('https://wa.me/905000000000?text=Merhaba');
  const h = harness({ choice: 'denied', anchors: [wa] });
  assert.equal(h.posts[0].body.vid, undefined);
  assert.equal(h.cookie(), '');
  h.click(wa);
  assert.doesNotMatch(wa.getAttribute('href'), /W-/);
});

test('engaged seconds are sent as deltas; an empty second hide sends nothing', () => {
  const h = harness();
  h.tick(12, true);
  h.tick(40, false);                 // idle more than 30 s: the idle tail is not engaged
  h.hide();
  const end1 = h.posts.find((p) => p.body.e === 'end').body;
  assert.equal(end1.sec, 12 + 29);
  assert.equal(end1.x, 'hide');
  h.show();
  h.hide();
  assert.equal(h.posts.filter((p) => p.body.e === 'end').length, 1);
  h.show();
  h.tick(5, true);
  h.hide();
  const ends = h.posts.filter((p) => p.body.e === 'end');
  assert.equal(ends.length, 2);
  assert.equal(ends[1].body.sec, 5);
});

test('a WhatsApp tap: tap event, [W-code] first, exit = tap', () => {
  const wa = anchor('https://wa.me/905000000000?text=Merhaba%20fiyat', { 'data-track-label': 'hero' });
  const h = harness({ anchors: [wa] });
  const vid = h.posts[0].body.vid;
  h.click(wa);
  const tap = h.posts.find((p) => p.body.e === 'tap').body;
  assert.equal(tap.kind, 'wa');
  assert.equal(tap.b, 'hero');
  const text = new URL(wa.getAttribute('href')).searchParams.get('text');
  const { visitCode } = require(CRM_SERVICE);
  assert.equal(text, `[W-${visitCode(vid)}] Merhaba fiyat`);
  h.click(wa);                       // idempotent
  assert.equal((new URL(wa.getAttribute('href')).searchParams.get('text').match(/W-/g) || []).length, 1);
  h.tick(3, true);
  h.hide();
  assert.equal(h.posts.find((p) => p.body.e === 'end').body.x, 'tap');
});

test('an ad visit carries the ad ids from the final URL suffix', () => {
  const h = harness({ search: '?gclid=abc&utm_source=google&utm_medium=cpc&utm_campaign=23606478186&agid=45&utm_term=ka%C5%9F%20al%C4%B1m%C4%B1&mt=e' });
  const land = h.posts[0].body;
  assert.deepEqual([land.src, land.c, land.g, land.k, land.m], ['ad', '23606478186', '45', 'kaş alımı', 'e']);
});

test('the site and the CRM derive the same visit code', () => {
  const { visitCode } = require(CRM_SERVICE);
  const h = harness();
  const code = vm.runInContext(`(${BLOCK.match(/function visitCode\(vid\) \{[\s\S]*?\n  \}/)[0]})('sgb.1.1727700000000.123456789012')`,
    vm.createContext({ Math, String }));
  assert.equal(code, visitCode('sgb.1.1727700000000.123456789012'));
  assert.ok(h);
});

// consent v3 (2026-10-02): the site record follows the SITE choice, the ad ref the Google choice.
function v3api(cons, variant = 'v3') {
  return { getCons: () => cons, getChoice: () => (cons === 'unset' ? null : (cons === 'granted' || cons === 'ads' ? 'granted' : 'denied')),
           barVariant: () => variant };
}

test('v3 "site only": id, cookie and [W-] code stay; the ad ref does not', () => {
  const wa = anchor('https://wa.me/905000000000?text=Merhaba');
  const ref = JSON.stringify({ ref: 'AbCdEf123456', expires_at: '2099-01-01T00:00:00Z' });
  const h = harness({ api: v3api('site'), anchors: [wa], storage: { sgb_google_ads_attribution_ref_v1: ref } });
  const land = h.posts[0].body;
  assert.equal(land.cons, 'site');
  assert.match(land.vid, /^sgb\.1\./);
  assert.equal(land.ar, undefined);
  assert.equal(land.bv, undefined);           // a choice exists: no bar, no variant
  h.click(wa);
  assert.match(new URL(wa.getAttribute('href')).searchParams.get('text'), /^\[W-[0-9A-Z]{6}\] Merhaba$/);
});

test('v3 "ads only": no id, no code, but the ad ref', () => {
  const wa = anchor('https://wa.me/905000000000?text=Merhaba');
  const ref = JSON.stringify({ ref: 'AbCdEf123456', expires_at: '2099-01-01T00:00:00Z' });
  const h = harness({ api: v3api('ads'), anchors: [wa], storage: { sgb_google_ads_attribution_ref_v1: ref } });
  const land = h.posts[0].body;
  assert.equal(land.vid, undefined);
  assert.equal(land.ar, 'AbCdEf123456');
  assert.equal(h.cookie(), '');
  h.click(wa);
  assert.doesNotMatch(wa.getAttribute('href'), /W-/);
});

test('no choice yet: the land names the bar variant; a choice is one counted event', () => {
  const h = harness({ api: v3api('unset', 'v3') });
  assert.equal(h.posts[0].body.cons, 'unset');
  assert.equal(h.posts[0].body.bv, 'v3');
  h.emit('sgb:consent-changed', { cons: 'site', layer: 'prefs' });
  const ch = h.posts.find((p) => p.body.e === 'choice').body;
  assert.deepEqual([ch.v, ch.layer, ch.bv, ch.p], ['site', 'prefs', 'v3', '/kas-alimi']);
  assert.equal(ch.pv, h.posts[0].body.pv);
  h.emit('sgb:consent-changed', { cons: 'weird', layer: 'x' });   // falls back to the live state: still unset
  assert.equal(h.posts.filter((p) => p.body.e === 'choice').length, 1);
});

test('a Reddet choice is counted without an id', () => {
  let cons = 'unset';
  const api = { getCons: () => cons, getChoice: () => null, barVariant: () => 'v2' };
  const h = harness({ api });
  assert.match(h.posts[0].body.vid, /^sgb\./);
  cons = 'denied';
  h.emit('sgb:consent-changed', { cons: 'denied', layer: 'bar' });
  const ch = h.posts.find((p) => p.body.e === 'choice').body;
  assert.equal(ch.v, 'denied');
  assert.equal(ch.vid, undefined);
  assert.equal(ch.bv, 'v2');
});

test('SGBVisit.mark gives script.js the same code, or nothing after a refusal', () => {
  const h = harness({ api: v3api('granted') });
  const { visitCode } = require(CRM_SERVICE);
  assert.equal(h.window.SGBVisit.mark(), `[W-${visitCode(h.posts[0].body.vid)}]`);
  const d = harness({ api: v3api('denied') });
  assert.equal(d.window.SGBVisit.mark(), '');
});
