---
name: product-films
description: Use when asked for a marketing video made by Celik, for one of his own projects or companies or for a client (a product or website film, demo or promo video, explainer, launch video, Instagram Reel, paid social ad, sponsor banner or overlay for someone else's video, or 3D motion graphics), including requests phrased as "make a video of", "animate this product or site", "Claude Motion", "bottom banner like this reel" or "with music and effects". Not for animating UI inside app code.
---

# Product films

A video is code: one HTML timeline rendered frame by frame, with an original synthesized score placed on the same timeline. Text, numbers and screens stay exact, and every sound lands on its cut.

Do not use AI video for screens, text or data. Motion in claude.ai is a separate product and cannot be reached from Claude Code.

## Modes

| Request | Mode | Read |
| --- | --- | --- |
| Product film, demo, promo, explainer, organic Reel | Film: the process below | This file |
| Paid Instagram or Facebook ad | Film, Reel only, with the ad rules | `references/ads.md` |
| Banner, sponsor card or overlay on someone else's video | Overlay: no music, transparent background | `references/overlay.md` |
| 3D objects, morphing shapes, fluid camera | Film with a three.js layer | `references/3d.md` |
| Film built around real footage (rides, events, supplied clips) | Film with video layers | `references/footage.md` |
| Promo for a social channel with no website | Film, 9:16 first (20 to 30 s, safe zones from `ads.md`), 16:9 for YouTube | This file |

Modes combine: a paid ad can have a 3D layer.

Other skills: the Digjitale Signal carousel uses the `digjitale-signal` skill. Use the HyperFrames skills only when the person asks for HyperFrames by name.

## Defaults

Apply these unless the request says otherwise. A request always wins, for this film only.

| Setting | Default |
| --- | --- |
| Formats | Both 16:9 (1920x1080) and 9:16 Reel (1080x1920), at 60fps |
| Length | 30 to 40 seconds, plus the ending card, which may push past 40. Go longer only if the request asks for it |
| Words | At most 5 words per shot in the main caption. A small eyebrow label and short labels inside a rebuilt UI (buttons, card titles) do not count. No paragraphs or descriptions. If a viewer cannot read it in one glance, cut it |
| Pace | A new shot every 1.5 to 2.5 seconds |
| Proof | Real published work, told as problem then result: one short line for the problem, then the outcome. Not image cards |
| Language | The product's own language for UI. Captions in the language the request asks for, else English |
| Ending | The kinetic Celik Nimani card in `references/ending.md`, on the film's own background, with celiknimani.com in the bottom area. Omit it if the request says so, if the film is about Celik himself (keep the motion; a short call to action such as "Say hello" replaces "Built by"), for a paid ad (see `references/ads.md`), or for a channel's own promo unless asked |
| Folder | `~/Movies/product-films/<slug>/` |
| Publishing | Private artifacts and local files. Never post to a public platform |

## Process

Copy these steps into your task list. Tools live in this skill's `scripts/`. Set `PF=~/.claude/skills/product-films/scripts` first; the commands below use it. Every script takes absolute paths and works from any folder, so no `cd` is needed. If the shell refuses commands built from variables or loops (worktree-isolated subagents do), write the path out as `~/.claude/skills/product-films/scripts/`, and put loops in a small script file you write first and run as one plain command.

1. **Set up.** `bash $PF/setup.sh ~/Movies/product-films/<slug>`. It needs ffmpeg, Node and Python on this machine, and installs numpy, scipy, Playwright and Chromium itself into `~/.cache/product-film`. If it reports something missing, tell the person what to install.
2. **Read the source.** The repo first: docs, design tokens, in-app screen components, demo data, and the code that implements each feature. Then the live site. Read the design feedback in any project memory. Never open a live database or production data.
3. **Write `brief.md` in the film folder.** It has four parts:
   - **Facts:** every claim and number that will appear, each with its source file or URL.
   - **Built check:** every feature to show, with the file that implements it. A feature found only in a spec, plan or marketing page goes under "Not built" and stays out of the film.
   - **Contradictions:** figures that disagree between pages. Leave them out and report them.
   - **Risks:** client and real-person names, competitors, platform terms, and anything invented for the film.
4. **Choose the concept.** Read `private/used.md` and `references/music.md`. Several 2026-11-08 films used a browser window that morphs into a phone; do not use that device transition again. Claim it at once by appending one row to `private/used.md` with "(in progress)" in the Date column, because other agents may be choosing at the same moment. Write these into `brief.md`, each different from every row in `private/used.md`: the intro idea (taken from what this product does), the visual motif, and the genre, tempo, key and instruments.
5. **Build scenes in `src.html`.** Always start from the current `assets/stage.html` (setup.sh copies it); never copy an older film's src.html, since those carry fixed bugs. Replace the template's brand and example scenes. Use the product's real fonts, tokens, logo and UI labels, and rebuild screens from its in-app components. Real screenshots and photos go in an `img/` folder next to `src.html`, cropped cleanly, and are referenced by relative path. Marketing pages are a source of copy and sample data only. Set `DUR`, `SCENES` and `FONTS`. Lay out 16:9 and 9:16 together with the `.reel` rules, keeping Reel captions between y 170 and 1250 in stage pixels. The Reel stage is 900x1600 and is exported at 1.2x, so that is 204 to 1500 in the MP4. A large clip or phone box may run from about y 90 to 1300; see the pitfalls row on label bands. Never crop a screen to fill the Reel: show the whole phone or window scaled to fit, and zoom only to a complete unit (see the pitfalls row "A screen is cut off in the Reel"). Paid ads use a tighter zone, see `references/ads.md`.
6. **Write `score.py`.** Pick a tempo whose bars land on the cuts and move the cuts onto bars. See `references/music.md`.
7. **Preview.** `bash $PF/score.sh <dir>`, `python3 $PF/build.py <dir> <slug> "<Title>"`, then `node $PF/preview.mjs <dir>/<slug>-film.html <dir>/sheet-film.jpg <times>` and `node $PF/preview.mjs <dir>/<slug>-reel.html <dir>/sheet-reel.jpg <times>`, with one time per scene, each time a separate argument (write them out; zsh does not split a variable). Use the time each scene has landed, not its start. Read each sheet and fix what you see. Then run `node $PF/text-still.mjs <dir>/<slug>-film.html` and the same for the reel: it fails if any text keeps moving after it lands, and lists drifting images to check for text inside them. Do not start step 9 until it exits 0 on both pages. Then crop 2 or 3 consecutive frames (1/60 s apart) around a few text landings and inside any scrolling screenshot, at 2x zoom, and confirm the glyphs are identical: `CROP=x,y,w,h node $PF/grab.mjs <dir>/<slug>-film.html <dir>/crop 4.5 4.5167 4.5333` (without CROP it writes full-size frames). See `references/pitfalls.md`.
8. **If captions are not in English,** show the full caption list to the person and wait for their corrections before rendering. If nobody can review (an unattended or background run), use only the site's own copy word for word, never new non-English text, and say so in the report.
9. **Render.** Run `bash $PF/render.sh <dir> <slug>` in the background (`bash $PF/render.sh <dir> <slug> reel` renders only the 9:16 version, for paid ads). Read `check-film.jpg` and `check-reel.jpg`, which are sampled from the final MP4s. Then run `~/.cache/product-film/venv/bin/python $PF/edge-check.py <dir>/<slug>-film.mp4` and the same for the reel: it fails if a thin strip of another colour shows along any frame edge. Fix and re-render until it passes. By default they sample 15 even times, so many frames are mid-animation. For a clean sheet run `bash $PF/check.sh <dir> <slug> <landed times...>`.
10. **Deliver.** Copy the MP4s to `~/Downloads`. Publish both HTML pages as private artifacts. These preview pages are the film itself, not designed artifacts, so the artifact-design pass does not apply to them. The Artifact tool only reads files under the working directory or the scratchpad, so copy the two pages and `img/` to the scratchpad first and pass the images through `files`. Artifacts load stylesheets only from Google Fonts: an icon font from another CDN (Font Awesome and similar) must be inlined as a data URI in the artifact copy. Never upload a licensed font file the licence forbids redistributing (such as Origin); the page falls back to the next font in its stack, which is fine for a preview. In `private/used.md`, complete your own row from step 4: replace "(in progress)" with the date and fill in the final details. Do not append a second row, and never edit other films' rows.

## Final report

Write it in this order:

1. What was made, with length and formats, and a plain statement that the music has not been heard, because Claude cannot hear audio. Give the loudness result.
2. The scene order.
3. Anything left out, with the reason: unbuilt features and contradicting figures.
4. Please check: invented content, names and competitors shown, public-posting risks, and copy to review.
5. File paths and artifact links.

Claim only what the checks showed. Instagram safe areas are designed, not tested.

## Reference

| File | Use |
| --- | --- |
| `private/used.md` | Every past film's intro and music, kept out of git. Read before choosing; append one row after delivering. If it is missing, create it from `used.template.md` |
| `private/brands.md` | Client brand notes, kept out of git |
| `references/music.md` | Writing a score, the instrument list, and mix targets |
| `references/pitfalls.md` | Known failures and how to spot them |
| `references/overlay.md` | Sponsor banners: layout, process, which file to send and how |
| `references/3d.md` | three.js setup, camera keys, instancing and morphs |
| `references/ads.md` | Paid ad length, hook, safe zones, and what to raise with the person |
| `references/ending.md` | The Celik Nimani end card: beats, sizes, sound and rules |
| `references/footage.md` | Building a film around real video: getting it, choosing shots, VP9, frame-exact seeking, speed readouts |
| `references/brands.md` | Pulling a brand from a live site, masking personal data, known client brands |
| `scripts/selftest.sh` | Runs every script and check on the template in a temp folder (about a minute). Run it after changing a script or template |
| `scripts/` | grab.mjs (full-size frames and 2x crops), setup.sh, score.sh (checks length with page-dur.mjs), build.py, preview.mjs, text-still.mjs, render.sh (uses capture.mjs, check.sh, sound-test.mjs), edge-check.py, overlay-render.sh (uses overlay-capture.mjs), soundkit.py |
| `assets/stage.html` | The timeline engine and its data attributes |
| `assets/overlay.html` | The banner template, a working Albanian banner |
| `assets/score_example.py` | A working score |
