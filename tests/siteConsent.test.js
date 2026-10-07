'use strict';

const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');
const vm = require('node:vm');

const SITE = '/var/www/seldagencerbeauty.com/public_html';
const FORBIDDEN_BROWSER_STORAGE_KEYS = ['gclid', 'gbraid', 'wbraid', 'click_id'];

test('consent bootstrap defaults all advertising signals to denied', () => {
  const events = [];
  const storage = new Map();
  const context = {
    window: {
      dataLayer: [],
      localStorage: {
        getItem: (key) => storage.get(key) || null,
        setItem: (key, value) => storage.set(key, value),
      },
    },
    document: { dispatchEvent: (event) => events.push(event) },
    CustomEvent: class CustomEvent {
      constructor(name, options) { this.type = name; this.detail = options.detail; }
    },
    Date,
    JSON,
    Object,
  };
  vm.runInNewContext(
    fs.readFileSync(path.join(SITE, 'consent-bootstrap.js'), 'utf8'),
    context,
  );
  const defaultCall = context.window.dataLayer.find((row) => row[0] === 'consent' && row[1] === 'default');
  assert.equal(defaultCall[2].ad_storage, 'denied');
  assert.equal(defaultCall[2].ad_user_data, 'denied');
  assert.equal(context.window.SGBConsent.isGranted(), false);

  assert.equal(context.window.SGBConsent.setChoice('granted'), true);
  const updateCall = context.window.dataLayer.find((row) => row[0] === 'consent' && row[1] === 'update');
  assert.equal(updateCall[2].ad_storage, 'granted');
  assert.equal(updateCall[2].ad_user_data, 'granted');
  assert.equal(events.at(-1).detail.choice, 'granted');
});

test('tracked HTML loads consent before GTM and has no inline Meta/GTM noscript bypass', () => {
  const files = [];
  function walk(dir) {
    for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
      const full = path.join(dir, entry.name);
      if (entry.isDirectory()) walk(full);
      else if (entry.isFile() && entry.name.endsWith('.html')) files.push(full);
    }
  }
  walk(SITE);
  const tracked = files.filter((file) => fs.readFileSync(file, 'utf8').includes('GTM-M7S9BF8J'));
  assert.ok(tracked.length >= 90);
  for (const file of tracked) {
    const html = fs.readFileSync(file, 'utf8');
    const consentAt = html.indexOf('/consent-bootstrap.js?v=20260721-v1');
    const gtmAt = html.indexOf('googletagmanager.com/gtm.js');
    assert.ok(consentAt >= 0 && consentAt < gtmAt, file);
    assert.equal(html.includes('connect.facebook.net/en_US/fbevents.js'), false, file);
    assert.equal(html.includes('googletagmanager.com/ns.html'), false, file);
    assert.equal(html.includes('facebook.com/tr?id='), false, file);
  }
});

test('site script never sends raw Google click IDs to dataLayer or Meta URL', () => {
  const source = fs.readFileSync(path.join(SITE, 'script.js'), 'utf8');
  assert.equal(source.includes("payload[prefix + '_gclid']"), false);
  assert.equal(source.includes("payload[prefix + '_wbraid']"), false);
  assert.equal(source.includes("payload[prefix + '_gbraid']"), false);
  assert.equal(source.includes('event_source_url: window.location.href'), false);
  assert.ok(source.includes('event_source_url: eventSourceUrl'));
  for (const key of FORBIDDEN_BROWSER_STORAGE_KEYS) {
    assert.equal(source.includes(`parsed.${key} =`), false);
  }
});
