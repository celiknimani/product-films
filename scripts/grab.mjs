// Usage: node grab.mjs <page.html> <out-prefix> <t1> [t2 ...]. Writes one full-size PNG per time.
// With CROP=x,y,w,h (stage pixels) it writes that region at 2x instead, for checking text landings up close.
// Grab three times 1/60 s apart (for example 4.5 4.5167 4.5333) and compare them: landed text must be identical.
import { createRequire } from 'module';
import path from 'path';
const [file, out, ...ts] = process.argv.slice(2);
if (!file || !out || !ts.length || ts.some(t => !Number.isFinite(+t))) {
  console.error('usage: node grab.mjs <page.html> <out-prefix> <t1> [t2 ...]'); process.exit(1);
}
const { chromium } = createRequire(path.resolve(file))('playwright');
const crop = process.env.CROP ? process.env.CROP.split(',').map(Number) : null;
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: 1600, height: 1600 }, deviceScaleFactor: crop ? 2 : 1 });
await p.goto('file://' + path.resolve(file));
await p.evaluate(() => window.__ready);
const m = await p.evaluate(() => window.__meta);
await p.setViewportSize({ width: m.W, height: m.H });
await p.evaluate(() => window.__capture());
for (const t of ts) {
  await p.evaluate(x => window.__seek(x), +t);
  const o = { path: `${out}-${t}.png` };
  if (crop) o.clip = { x: crop[0], y: crop[1], width: crop[2], height: crop[3] };
  await p.screenshot(o);
}
await b.close();
console.log('wrote', ts.length, 'frame(s) to', out + '-*.png');
