// Usage: node preview.mjs <page.html> <out.jpg> <t1> <t2> ... Screenshots each time and tiles them into one contact sheet.
import { createRequire } from 'module';
import { execFileSync } from 'child_process';
import { mkdtempSync, rmSync } from 'fs';
import { tmpdir } from 'os';
import path from 'path';
const req = createRequire(path.resolve(process.argv[2]));
const { chromium } = req('playwright');
const [file, out, ...ts] = process.argv.slice(2);
// zsh does not split a variable holding several times, so they would arrive as one NaN.
if (!ts.length || ts.some(t => !Number.isFinite(+t))) { console.error('pass each time as its own number argument, got:', ts); process.exit(1); }
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: 1600, height: 1600 } });
const errs = []; p.on('pageerror', e => errs.push(e.message));
await p.goto('file://' + path.resolve(file));
await p.evaluate(() => window.__ready);
const m = await p.evaluate(() => window.__meta);
await p.setViewportSize({ width: m.W, height: m.H });
await p.evaluate(() => window.__capture());
const dir = mkdtempSync(path.join(tmpdir(), 'pf-'));
for (const [i, t] of ts.entries()) {
  await p.evaluate(x => window.__seek(x), +t);
  await p.screenshot({ path: `${dir}/s${String(i).padStart(3, '0')}.jpg`, type: 'jpeg', quality: 75 });
}
await b.close();
const cols = m.W > m.H ? 3 : 6, rows = Math.ceil(ts.length / cols);
execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-pattern_type', 'glob', '-i', `${dir}/s*.jpg`, '-filter_complex', `tile=${cols}x${rows}:padding=6,scale=1800:-1`, '-frames:v', '1', out]);
rmSync(dir, { recursive: true, force: true });
console.log('errors:', errs.length ? errs : 'none', '->', out);
