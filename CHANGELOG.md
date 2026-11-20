# Changelog

## 2026-11-20

- Renamed to `product-films`, made Celik's personal toolkit, and published. The skill lives at `~/.claude/skills/product-films`.
- The ending card signs films with CELIK NIMANI and celiknimani.com in the site's colours (ink #121212, lime #c9fe6e, Geist). The rule is now placed from a measured baseline, since fixed em offsets differ per font.
- The banner template uses the personal brand.
- The film log and client brand notes moved to `private/`, which git ignores, with `used.template.md` to start a new log. Client names and client stills are out of the repo.

## 2026-11-14

- Added `scripts/grab.mjs` for full-size frames and 2x crops of text landings.
- `score.sh` warns when the master's true peak is above -1 dBFS, before rendering.
- Reels show whole screens and windows, never cropped through content.
- Pitfall: a film class named `.cap` clashes with the capture class and blanks the stage.
- The ending rule stops at the last letter minus its trailing letter-spacing.

## 2026-11-13

- The toolkit became its own project, with the skill folder as a symlink to it.
- Added README screenshots, a quick start, a third-party assets section and this changelog.
- Added `scripts/selftest.sh`, which runs every script and check on the template in a temp folder.
- `render.sh` and `overlay-render.sh` stop when a capture worker fails, and `render.sh` checks that every frame was captured. Before, a failed worker produced a short, out-of-sync film without an error.
- Every script prints its usage when called without arguments, and checks that its inputs exist.
- `setup.sh` creates `img/` (where the process puts screenshots) and reinstalls numpy and scipy if a previous install failed.
- Reference pages no longer contain a hard-coded home folder path.
- One rule for the film log: claim a row marked "(in progress)" when choosing a concept, complete that same row on delivery.
- Clearer ending-card check times, conventional headings, and a Pexels note in `references/footage.md`.

## 2026-11-10

- The ending card's parts are shown and hidden with `vis()`, so they do not stay on screen when playback seeks back.
- Reel captions stay between y 170 and 1250, while a large clip or phone box may run from about y 90 to 1300.

## 2026-11-08

- Added overlay banners, 3D, paid ads and social promos.
- The kinetic ending card, where the spark lands as the dot of the URL.
- Fixed text wobble at the source: the template's ease-out is quartic, reveals lock once landed, and there is no overshoot on text. Added `text-still.mjs`.
- Fixed the thin line along frame edges at the source (the capture page's default body margin). Added `edge-check.py`.
- Added `footage.md` for films built on real video and sound, a limiter in `score.sh`, and the length check against the page.
- Larger clips in 9:16 layouts, kinetic showreels, and labels that never cover a clip.
