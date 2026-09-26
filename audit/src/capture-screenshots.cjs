const { chromium } = require('C:/Users/MPS/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const path = require('path');
const fs = require('fs');

const root = path.resolve(__dirname, '..');
const out = path.join(root, 'screenshots');
fs.mkdirSync(out, { recursive: true });

async function settle(page, delay = 1800) {
  await page.waitForLoadState('domcontentloaded');
  await page.waitForTimeout(delay);
}

async function capturePublic(browser) {
  const context = await browser.newContext({ viewport: { width: 1440, height: 1000 }, deviceScaleFactor: 1 });
  const page = await context.newPage();
  await page.goto('https://wiltondental.co.uk/', { waitUntil: 'domcontentloaded', timeout: 45000 });
  await settle(page, 2500);
  for (let attempt = 0; attempt < 5; attempt += 1) {
    const body = await page.locator('body').innerText().catch(() => '');
    if (!body.includes('Checking your browser before accessing')) break;
    await page.waitForTimeout(5000);
  }
  await page.screenshot({ path: path.join(out, 'current-home-full.png'), fullPage: true });
  await page.screenshot({ path: path.join(out, 'current-home-hero.png') });
  const team = page.getByRole('heading', { name: 'Our Team', exact: true });
  if (await team.count()) {
    await team.scrollIntoViewIfNeeded();
    await page.waitForTimeout(500);
    await page.screenshot({ path: path.join(out, 'current-team.png') });
  }
  await context.close();
}

async function capturePrototype(browser) {
  const context = await browser.newContext({ viewport: { width: 1440, height: 1000 }, deviceScaleFactor: 1 });
  const page = await context.newPage();
  await page.goto('http://localhost:4173/', { waitUntil: 'domcontentloaded', timeout: 20000 });
  await settle(page, 2200);
  await page.screenshot({ path: path.join(out, 'prototype-home-full.png'), fullPage: true });
  await page.screenshot({ path: path.join(out, 'prototype-home-hero.png') });
  await page.goto('http://localhost:4173/#treatments', { waitUntil: 'domcontentloaded', timeout: 20000 });
  await page.waitForTimeout(1500);
  await page.screenshot({ path: path.join(out, 'prototype-treatments.png') });
  for (const [selector, filename] of [
    ['.science-panel', 'prototype-precision.png'],
    ['#doctor', 'prototype-doctor.png'],
    ['#visit', 'prototype-conversion.png'],
  ]) {
    const section = page.locator(selector).first();
    await section.scrollIntoViewIfNeeded();
    await page.waitForTimeout(500);
    await page.screenshot({ path: path.join(out, filename) });
  }
  await context.close();

  const mobile = await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 1 });
  const mobilePage = await mobile.newPage();
  await mobilePage.goto('http://localhost:4173/', { waitUntil: 'domcontentloaded', timeout: 20000 });
  await settle(mobilePage, 2200);
  await mobilePage.screenshot({ path: path.join(out, 'prototype-mobile-hero.png') });
  await mobilePage.goto('http://localhost:4173/#doctor', { waitUntil: 'domcontentloaded', timeout: 20000 });
  await mobilePage.waitForTimeout(1800);
  await mobilePage.screenshot({ path: path.join(out, 'prototype-mobile-doctor.png') });
  await mobile.close();
}

(async () => {
  const browser = await chromium.launch({
    headless: true,
    executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe',
    args: ['--disable-gpu', '--hide-scrollbars'],
  });
  try {
    await capturePublic(browser);
    await capturePrototype(browser);
  } finally {
    await browser.close();
  }
})();
