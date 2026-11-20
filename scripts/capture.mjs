// Internal: one render worker. node capture.mjs <page.html> <dir> <shard> <shards> [fromFrame] [toFrame]
import { createRequire } from 'module';
import path from 'path';
const req = createRequire(path.resolve(process.argv[2]));
const { chromium } = req('playwright');
const [file, dir, shard, shards, from, to] = process.argv.slice(2);
const b = await chromium.launch();
let p = await b.newPage({ viewport: { width: 1600, height: 1600 } });
await p.goto('file://' + path.resolve(file));
await p.evaluate(() => window.__ready);
const m = await p.evaluate(() => window.__meta);
await p.close();
p = await b.newPage({ viewport: { width: m.W, height: m.H }, deviceScaleFactor: 1.2 });
await p.goto('file://' + path.resolve(file));
await p.evaluate(() => window.__ready);
await p.evaluate(() => window.__capture());
const total = Math.round(m.DUR * 60), a = +(from ?? 0), z = Math.min(+(to ?? total), total);
for (let f = a + +shard; f < z; f += +shards) {
  await p.evaluate(t => window.__seek(t), f / 60);
  await p.screenshot({ path: `${dir}/f${String(f).padStart(5, '0')}.jpg`, type: 'jpeg', quality: 93 });
}
await b.close();
