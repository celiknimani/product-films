# Pitfalls

Each of these reached a contact sheet at least once.

| Symptom | Cause | Fix |
| --- | --- | --- |
| A scene, caption or view shows through a later scene | A child inside a hidden parent was set to `visibility:visible` | Children use `inherit`. The engine's `vis()` does this |
| Text stale after seeking backward, or a wrong frame in one render shard | State depended on the previous frame | Set every property from `t` alone in `scene(t)`. Test by previewing times out of order |
| Table text missing or wrong in local renders | The page ran without a doctype (quirks mode), so tables stop inheriting | The template now starts with `<!doctype html>`. Keep it |
| A logo letter or element is suddenly huge or off-frame | Duplicate id: a new wrapper reused an existing id | Check new ids against the page |
| Fallback font in the MP4 | Font missing from `FONTS` | List every family and weight the page uses |
| Words run together in streamed text | Splitting into words dropped a leading space | Keep whitespace in the split, use `white-space:pre-wrap` |
| Reel clipped to a narrow column | A strong width rule also applied while capturing | Keep the `body.cap` overrides more specific than the reel rules |
| Clock or label sits on a phone or another label | Fixed furniture was placed for one scene only | Place it against every scene, then preview them all |
| Reel looks top-heavy with small text | The 16:9 sizes were kept | Center inside y 170 to 1250, raise body text to about 25px or more at stage scale |
| A word breaks mid-line in the Reel | Character-split text wraps anywhere | Set a size where each line fits, and preview the Reel hero |
| Text pulses, shimmers or wobbles after it lands | A camera zoom, shake or beat pulse was applied to text. Scaled text re-rasterizes every frame, and a looping zoom jumps when it resets | Text stays still once it lands. Apply camera moves to graphics only, and never scale a container of text continuously |
| `text-still.mjs` fails on a long, smooth text move | Any ease on text longer than about 0.8 s spends its last half second below 2 px per frame, which reads as drift | Keep text eases at 0.8 s or less; for a longer flourish, move fast and lock to rest early |
| Letters jiggle as a line lands | Each letter has its own transform, and an exponential ease or an overshoot leaves sub-pixel creep or a bounce at the end | Use an ease that finishes exactly (the template's `eo` is a quartic ease-out since 2026-11-08; never `1-2^-kx`), no overshoot on text, and set the transform to `none` once landed |
| Text inside a screenshot shimmers | A screenshot with text was scaled, tilted or scrolled slowly, so its glyphs resample every frame | Scroll screenshots in fast eased steps with holds between them, at whole-pixel offsets, flat (no tilt) during a scroll. Slow pushes only on photos without text |
| A thin white or coloured line along a frame edge | Most often the browser's default 8px body margin during capture, which shifts the whole stage in from the top and left (the template sets `body.cap{margin:0}` since 2026-11-08; keep it). Otherwise a full-bleed layer stops short of the frame: it is inset, moved by a slide or camera move, scaled below 1, masked or blurred at its edge, or a panel or browser frame sits a few pixels in from the edge with the page colour behind it. Rejected on 2026-11-08 | Full-bleed backgrounds overscan: `inset:-4%` (or `scale` of at least 1.04 at every moment of a move) so no edge ever enters the frame. Set the stage and body background to the scene's own colour. A deliberately framed panel needs a clear margin of at least 40 stage px, never a hairline gap. `edge-check.py` must pass on both MP4s |
| A highlight or marker hides the text on a white card it passes over | It was drawn as an opaque layer above the card | Draw it with `mix-blend-mode: multiply` so the text shows through, and switch to its final style once it arrives |
| The whole stage is blank in the capture | A film class named `.cap` matched the template's capture class (`body.cap`) and hid the stage | Never name a film class `cap`; prefix film classes with a short project tag |
| A decorative link between two panels reads as a stray button | A connector glyph (a ring or dot) was parked on the seam between a chat panel and an app window, overlapping the app. Rejected on 2026-11-14 | Show the link with motion instead: a chip or spark that travels from one panel to the other and disappears. Nothing decorative stays on screen over UI |
| A rebuilt UI element takes on the wrong size or style | Its class name (such as `.box`, `.full`, `.sum`) collides with a template or page class | Prefix the film's own classes with a short project tag, such as `.ch-box` |
| A showreel or case-study run feels boring | Projects slide past on an even rail at one cut per bar, and services sit on a static board with thumbnails. Rejected on 2026-11-08 | Cut on half bars or faster, vary the transition per project (whip pan with motion blur, gradient mask wipe, split screen, grid burst, quick 3D flip landing flat, speed-ramped push), add short 3-shot bursts, flip a big project counter, and show services as huge kinetic words with clips flashing behind. Clips move only while travelling fast and hold still once landed |
| A screen is cut off in the Reel | A 16:9 screen or a phone was cropped to fill the 9:16 box, so the crop lines fell through a clock, a tab row, text or a window edge. Rejected on 2026-11-14 | In 9:16, show the whole phone (status bar to home indicator) or the whole Mac or browser window (title bar and all four edges), scaled to fit as large as possible. Zoom in only as a second shot, to one complete unit (a card, a sheet, a list section, a control bar) cropped at its own edges. Review every landed Reel frame and confirm no text, number or control touches a crop edge |
| A label band cuts through a clip | A lower-third slab was placed across the middle of the frame, over the clip's subject. Rejected on 2026-11-08 | Keep labels in a slim band at the bottom (16:9) or below the clip (9:16), and frame each clip so its subject sits whole above the band. In 9:16, make the clip box near full width and tall (about y 90 to 1300 on the 1600 stage) with the band right under it: Celik prefers bigger clips over a clear caption zone (a large empty band below the label was rejected on 2026-11-08). Check a landed frame of every project in both formats |
| Viewers will not read the film | Too much descriptive text. A full film of paragraphs under titles was rejected for this | Titles and numbers only, 5 words or fewer per shot, 30 to 40 seconds |
| Case studies look flat | Image cards with a small caption. Rejected as "meh" | Use the case study's published problem, then the result: one stark line, then a cut to the outcome |
| The ending feels flat | A quiet "Built by" credit line faded in on a plain background. Rejected on 2026-11-08 | Use the kinetic card in `ending.md`: wipe bars, wordmark rising letter by letter, impact ring, spark drawing the rule, URL in the bottom area |
| Particles pulse on the end card | A beat kick moved every particle, or points were left drifting behind the wordmark | No beat motion on particles or the spark. End on the plain background with no particles |
| A thin line along the edge of a case study image | The site's framed image was cropped too loosely | Crop inside the frame, then check the edges on a contact sheet |
| A rounded or shortened figure on screen | A counter dropped the source's "close to" or "about" | Keep the qualifier next to the number |
| An arrow or accent shows as garbled characters | The rendered page has no charset | Use HTML entities such as `&amp;rarr;` |
| A spark or accent sits beside its letter | It was positioned against the word | Attach it to the letter's own element |
| A script file ends up empty | `open(f,'w').write(open(f).read())` truncates before reading | Read first, then write |
| Long lines overlap the next element | A headline wrapped to one more line than planned | Preview the longest caption in each language |
| Tool call dies on a long render | Render ran in the foreground | Run `render.sh` in the background |
| The first frames miss a photo or screenshot | `__ready` resolved before the image loaded | The template waits for images and CSS background images. Keep that wait if you rewrite `__ready` |
| The film is 6 seconds long, or the music stops early | `score.sh` ran on the copied `score_example.py` before it was replaced | Write `score.py` first, and match its `DUR` to `src.html` |

## Content

- Marketing claims can outrun the code. Search `src` for the feature's strings before showing it.
- Client sites can contradict themselves. Compare the headline figure with the chart below it, and the case study with the blog.
- Paid ads never name clients, even from published case studies. Use trade and country.
- Real names may be wanted, but they are the person's call. Without an instruction, use the repo's demo data and leave real staff and clients out.
- Reenacted AI answers and chat messages are invented content. Say so in the report.
- Do not state availability, such as "on the App Store", unless it is confirmed.
- Albanian and other non-English copy needs the person's eye before the render. Literal translations read as strange to native speakers.
