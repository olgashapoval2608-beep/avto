// Рендерить tools/html/*.html у PNG (img/) через Chromium.
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
(async () => {
  const dir = path.join(__dirname, 'html'), out = path.join(__dirname, '..', 'img');
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const page = await browser.newPage({ deviceScaleFactor: 2, viewport: { width: 1300, height: 800 } });
  for (const f of fs.readdirSync(dir).filter(f => f.endsWith('.html'))) {
    await page.goto('file://' + path.join(dir, f));
    const el = await page.$('body > *');
    await el.screenshot({ path: path.join(out, f.replace('.html', '.png')) });
  }
  await browser.close();
})();
