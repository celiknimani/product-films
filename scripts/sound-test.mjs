// Usage: node sound-test.mjs <page.html>. Presses the sound button and confirms the embedded audio plays.
import { createRequire } from 'module';
import path from 'path';
const req = createRequire(path.resolve(process.argv[2]));
const { chromium } = req('playwright');
const b = await chromium.launch({ channel: 'chromium', args: ['--autoplay-policy=no-user-gesture-required'] });
const p = await b.newPage({ viewport: { width: 1280, height: 900 } });
await p.goto('file://' + path.resolve(process.argv[2]));
await p.evaluate(() => window.__ready);
await p.click('#snd');
await p.waitForTimeout(2200);
const r = await p.evaluate(() => { const v = document.querySelector('#au'); return { dur: v.duration, cur: v.currentTime, paused: v.paused, err: v.error && v.error.message }; });
console.log('sound test', r);
await b.close();
process.exit(r.err || r.paused || !(r.cur > 1) ? 1 : 0);
