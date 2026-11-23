// Tangkap halaman susun atur. Guna: node shot.js <html> <dpr> <transparent 0|1> <out.png>; cetak LAYOUT (JSON).
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const [html, dpr, transparent, out] = process.argv.slice(2);
  const b = await chromium.launch({ args: ['--allow-file-access-from-files'] });
  const pg = await b.newPage({ viewport: { width: 1350, height: 1800 }, deviceScaleFactor: +dpr });
  await pg.goto('file://' + path.resolve(html));
  await pg.waitForFunction('window.READY === true', null, { timeout: 120000 });
  await pg.waitForTimeout(500);
  const layout = await pg.evaluate('window.LAYOUT');
  await pg.screenshot({ path: out, omitBackground: transparent === '1', type: 'png' });
  await b.close();
  console.log(JSON.stringify(layout));
})();
