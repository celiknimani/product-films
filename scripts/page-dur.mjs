// Internal: prints the page's DUR as the browser computes it, so formulas like DUR=18*B work. node page-dur.mjs <page.html>
import { createRequire } from 'module';
import path from 'path';
const file = process.argv[2];
const { chromium } = createRequire(path.resolve(file))('playwright');
const b = await chromium.launch();
const p = await b.newPage();
await p.goto('file://' + path.resolve(file));
await p.evaluate(() => window.__ready);
console.log(await p.evaluate(() => window.__meta.DUR));
await b.close();
