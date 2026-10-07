'use strict';

const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');
const vm = require('node:vm');

const SITE = '/var/www/seldagencerbeauty.com/public_html';
const CLIENT_SOURCE = fs.readFileSync(path.join(SITE, 'ads-attribution.js'), 'utf8');
const CLICK_ID = 'CjwKCA-behavior-test-click-1234567890';
const OPAQUE_REF = 'R'.repeat(32);

function createHarness({ enabled = true, granted = true, search = `?gclid=${CLICK_ID}&utm_campaign=22273182653&agid=123` } = {}) {
  const storage = new Map();
  const listeners = new Map();
  const requests = [];
  const beacons = [];
  const anchor = {
    href: 'https://wa.me/905330390076?text=Merhaba',
    getAttribute(name) { return name === 'href' ? this.href : null; },
    setAttribute(name, value) { if (name === 'href') this.href = value; },
    closest(selector) { return selector === 'a[href]' ? this : null; }
  };
  const document = {
    readyState: 'complete',
    documentElement: {},
    querySelectorAll: () => [anchor],
    addEventListener(name, callback) { listeners.set(name, callback); }
  };
  const window = {
    location: {
      origin: 'https://seldagencerbeauty.com',
      pathname: '/protez-tirnak',
      search
    },
    localStorage: {
      getItem: (key) => storage.get(key) || null,
      setItem: (key, value) => storage.set(key, value),
      removeItem: (key) => storage.delete(key)
    },
    SGBConsent: {
      version: '2026-07-21-v1',
      isGranted: () => granted
    },
    SGB_GOOGLE_ADS_ATTRIBUTION_CONFIG: {
      enabled,
      withdrawalEnabled: enabled,
      endpoint: '/api/public/google-ads-attribution/capture',
      withdrawalEndpoint: '/api/public/google-ads-attribution/withdraw',
      whatsappClickEndpoint: '/api/public/google-ads-attribution/whatsapp-click'
    },
    navigator: {
      sendBeacon(...args) {
        beacons.push(args);
        return true;
      }
    },
    fetch: async (url, options) => {
      requests.push({ url, options });
      return {
        ok: true,
        async json() {
          return { ref: OPAQUE_REF, expires_at: '2099-01-01T00:00:00.000Z', reused: false };
        }
      };
    }
  };
  class MutationObserver {
    observe() {}
  }
  const context = {
    window,
    document,
    MutationObserver,
    URL,
    URLSearchParams,
    Promise,
    Object,
    JSON,
    Date,
    Number,
    String,
    Boolean
  };
  vm.runInNewContext(CLIENT_SOURCE, context);
  return {
    window,
    document,
    storage,
    listeners,
    requests,
    beacons,
    anchor,
    setGranted(value) { granted = value; }
  };
}

test('consent yoksa click kimliği gönderilmez veya saklanmaz', async () => {
  const harness = createHarness({ granted: false });
  await harness.window.SGBGoogleAdsAttribution.capture();
  assert.equal(harness.requests.length, 0);
  assert.equal(harness.storage.size, 0);
  assert.equal(harness.anchor.href.includes('[SGB:'), false);
});

test('consentli click same-origin APIye gider; tarayıcıda yalnız opaque ref kalır', async () => {
  const harness = createHarness();
  await harness.window.SGBGoogleAdsAttribution.capture();
  assert.equal(harness.requests.length, 1);
  assert.equal(harness.requests[0].url, '/api/public/google-ads-attribution/capture');
  const body = JSON.parse(harness.requests[0].options.body);
  assert.equal(body.click_id, CLICK_ID);
  assert.equal(body.campaign_id, '22273182653');
  assert.equal(body.landing_path, '/protez-tirnak');
  assert.equal(harness.requests[0].options.referrerPolicy, 'no-referrer');

  const persisted = [...harness.storage.values()].join('\n');
  assert.equal(persisted.includes(CLICK_ID), false);
  assert.equal(persisted.includes(OPAQUE_REF), true);
  assert.equal(decodeURIComponent(harness.anchor.href).includes(`[SGB:${OPAQUE_REF}]`), true);
});

test('feature flag kapalıysa API çağrısı ve marker yoktur', async () => {
  const harness = createHarness({ enabled: false });
  await harness.window.SGBGoogleAdsAttribution.capture();
  assert.equal(harness.requests.length, 0);
  assert.equal(harness.anchor.href.includes('[SGB:'), false);
});

test('WhatsApp CTA click yalnız boş-body same-origin beacon yollar ve navigasyonu tutmaz', async () => {
  const harness = createHarness();
  await harness.window.SGBGoogleAdsAttribution.capture();
  let prevented = false;

  assert.doesNotThrow(() => harness.listeners.get('click')({
    target: harness.anchor,
    preventDefault() { prevented = true; }
  }));

  assert.equal(prevented, false);
  assert.equal(harness.beacons.length, 1);
  assert.equal(
    harness.beacons[0][0],
    'https://seldagencerbeauty.com/api/public/google-ads-attribution/whatsapp-click'
  );
  assert.equal(harness.beacons[0].length, 1);
  assert.equal(harness.requests.length, 1);
});

test('consent veya feature flag yoksa WhatsApp click beaconı yoktur', async () => {
  for (const harness of [
    createHarness({ granted: false }),
    createHarness({ enabled: false })
  ]) {
    await harness.window.SGBGoogleAdsAttribution.capture();
    harness.listeners.get('click')({ target: harness.anchor });
    assert.equal(harness.beacons.length, 0);
  }
});

test('consent geri çekilince opaque ref ve WhatsApp markerı kaldırılır', async () => {
  const harness = createHarness();
  await harness.window.SGBGoogleAdsAttribution.capture();
  harness.setGranted(false);
  harness.listeners.get('sgb:consent-changed')({ detail: { choice: 'denied' } });
  await new Promise((resolve) => setImmediate(resolve));
  assert.equal(harness.storage.size, 0);
  assert.equal(decodeURIComponent(harness.anchor.href).includes('[SGB:'), false);
  assert.equal(harness.requests.length, 2);
  assert.equal(harness.requests[1].url, '/api/public/google-ads-attribution/withdraw');
  assert.deepEqual(JSON.parse(harness.requests[1].options.body), {});
  assert.equal(harness.requests[1].options.keepalive, true);
});

test('takipli sayfalarda attribution client consentten sonra ve GTMden önce yüklenir', () => {
  function htmlFiles(root) {
    const files = [];
    for (const entry of fs.readdirSync(root, { withFileTypes: true })) {
      const fullPath = path.join(root, entry.name);
      if (entry.isDirectory()) files.push(...htmlFiles(fullPath));
      else if (entry.isFile() && entry.name.endsWith('.html')) files.push(fullPath);
    }
    return files;
  }
  const files = htmlFiles(SITE);
  const tracked = files.filter((file) => fs.readFileSync(file, 'utf8').includes('GTM-M7S9BF8J'));
  assert.ok(tracked.length >= 90);
  for (const file of tracked) {
    const html = fs.readFileSync(file, 'utf8');
    const consentAt = html.indexOf('/consent-bootstrap.js?v=20260721-v1');
    const configAt = html.indexOf('/ads-attribution-config.js');
    const clientAt = html.indexOf('/ads-attribution.js?v=20260721-shadow02');
    const gtmAt = html.indexOf('googletagmanager.com/gtm.js');
    assert.ok(consentAt >= 0 && consentAt < configAt && configAt < clientAt && clientAt < gtmAt, file);
  }
});
