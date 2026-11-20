// Usage: node text-still.mjs <page.html>. Finds text, and images that may hold text, that keep drifting after they land.
// Slow sub-pixel motion makes glyphs re-rasterize every frame, which reads as wobble. Exit code 1 when anything drifts.
import { createRequire } from 'module';
import path from 'path';
const file = process.argv[2];
const { chromium } = createRequire(path.resolve(file))('playwright');
const b = await chromium.launch();
let p = await b.newPage({ viewport: { width: 1600, height: 1600 } });
await p.goto('file://' + path.resolve(file));
await p.evaluate(() => window.__ready);
const m = await p.evaluate(() => window.__meta);
await p.setViewportSize({ width: m.W, height: m.H });
await p.evaluate(() => window.__capture());
const FPS = 30, MIN = 0.5;
const tracks = new Map();
for (let f = 0; f < m.DUR * FPS; f++) {
  const t = f / FPS;
  const rows = await p.evaluate(t => {
    window.__seek(t);
    const out = [];
    const shown = e => { for (let n = e; n && n.nodeType === 1; n = n.parentElement) { const s = getComputedStyle(n); if (s.visibility === 'hidden' || s.display === 'none' || +s.opacity < 0.5) return false } return true };
    document.querySelectorAll('body *').forEach((e, i) => {
      const own = [...e.childNodes].some(c => c.nodeType === 3 && c.textContent.trim());
      const kind = own ? 'text' : e.tagName === 'IMG' ? 'img' : null;
      if (!kind || !shown(e)) return;
      const r = e.getBoundingClientRect();
      if (r.width < 2 || r.height < 2 || r.right < 0 || r.bottom < 0 || r.left > innerWidth || r.top > innerHeight) return;
      out.push([i, kind, (own ? e.textContent.trim() : e.getAttribute('src') || '').slice(0, 40), r.x, r.y, r.width, r.height]);
    });
    return out;
  }, t);
  for (const [i, kind, label, x, y, w, h] of rows) {
    const k = tracks.get(i) || { kind, label, last: null, runStart: null, runs: [] };
    if (k.last && k.last.f === f - 1) {
      const d = Math.max(Math.abs(x - k.last.x), Math.abs(y - k.last.y), Math.abs(w - k.last.w), Math.abs(h - k.last.h));
      const drifting = d > 0.01 && d < 2;
      if (drifting && k.runStart === null) k.runStart = t - 1 / FPS;
      if (!drifting && k.runStart !== null) { if (t - k.runStart >= MIN) k.runs.push([k.runStart, t]); k.runStart = null }
    } else if (k.runStart !== null) { if (k.last.f / FPS - k.runStart >= MIN) k.runs.push([k.runStart, k.last.f / FPS]); k.runStart = null }
    k.last = { f, x, y, w, h };
    tracks.set(i, k);
  }
}
await b.close();
let bad = 0;
for (const k of tracks.values()) {
  if (k.runStart !== null && k.last.f / FPS - k.runStart >= MIN) k.runs.push([k.runStart, k.last.f / FPS]);
  if (!k.runs.length) continue;
  bad += k.kind === 'text';
  console.log(`${k.kind === 'text' ? 'TEXT DRIFTS' : 'image drifts (fine only if it holds no text)'}  "${k.label}"  ${k.runs.map(([a, z]) => a.toFixed(1) + '-' + z.toFixed(1) + 's').join(', ')}`);
}
console.log(bad ? `${bad} text element(s) drift after landing` : 'no drifting text');
process.exit(bad ? 1 : 0);
