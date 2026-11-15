// Usage: node render.js <outDir> [fps] [--preview t1,t2,...]
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');
(async () => {
  const out = process.argv[2]; const fps = +(process.argv[3] || 30);
  const prevIdx = process.argv.indexOf('--preview');
  fs.mkdirSync(out, { recursive: true });
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  await page.goto('file://' + path.resolve(__dirname, 'scene.html'));
  await page.evaluate(() => document.fonts.ready);
  const times = prevIdx > 0 ? process.argv[prevIdx + 1].split(',').map(Number)
    : [...Array(Math.round(fps * await page.evaluate(() => DURATION))).keys()].map(i => i / fps);
  for (let i = 0; i < times.length; i++) {
    await page.evaluate(t => render(t), times[i]);
    await page.screenshot({ path: path.join(out, `f${String(i).padStart(5, '0')}.jpg`), type: 'jpeg', quality: 92 });
  }
  await browser.close();
})();
