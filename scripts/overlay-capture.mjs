// Internal: one overlay render worker. node overlay-capture.mjs <alpha|green> <page.html> <dir> <shard> <shards>
// node overlay-capture.mjs host <page.html> <out.png> writes the sample background for the preview.
import { createRequire } from 'module';
import path from 'path';
const [mode, file, out, shard, shards] = process.argv.slice(2);
const { chromium } = createRequire(path.resolve(file))('playwright');
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
await p.goto('file://' + path.resolve(file));
await p.evaluate(() => window.__ready);
const m = await p.evaluate(() => window.__meta);
if (mode === 'host') {
  await p.evaluate(() => { window.__capture(false); document.getElementById('host').style.display = 'block'; window.__seek(0) });
  await p.screenshot({ path: out });
} else {
  await p.evaluate(g => window.__capture(g), mode === 'green');
  for (let f = +shard; f < Math.round(m.DUR * 60); f += +shards) {
    await p.evaluate(t => window.__seek(t), f / 60);
    await p.screenshot({ path: `${out}/f${String(f).padStart(5, '0')}.png`, omitBackground: mode === 'alpha' });
  }
}
await b.close();
