const { chromium } = require('C:/Users/MPS/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const path = require('path');
const fs = require('fs');

const root = path.resolve(__dirname, '..', '..');
const logos = path.join(root, 'brand', 'logo-concepts');
const preview = path.join(logos, 'previews');
fs.mkdirSync(preview, { recursive: true });

(async () => {
  const browser = await chromium.launch({
    headless: true,
    executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe',
    args: ['--disable-gpu'],
  });
  try {
    for (const file of fs.readdirSync(logos).filter((name) => name.endsWith('.svg'))) {
      const page = await browser.newPage({ viewport: { width: 1200, height: 400 }, deviceScaleFactor: 1 });
      await page.goto(`file:///${path.join(logos, file).replace(/\\/g, '/')}`);
      await page.screenshot({ path: path.join(preview, file.replace('.svg', '.png')) });
      await page.close();
    }
  } finally {
    await browser.close();
  }
})();
