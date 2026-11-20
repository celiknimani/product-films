# Sponsor overlay banners

`$PF` is the skill's `scripts/` folder, `~/.claude/skills/product-films/scripts` (see SKILL.md, Process).

A sponsor banner is a short animated card that sits in the bottom area of someone else's video, such as a creator's Reel. It is a separate mode from a film: no music, no full-screen scenes, and a transparent background.

First made as an Albanian sponsor banner on 2026-11-02.

## Shape

| Setting | Default |
| --- | --- |
| Canvas | Full 1080x1920 at 60fps, with the card already placed. The editor drops it on the top track at 100% and never moves it |
| Card | left 120, top 1190, 840x380, radius 44. This copies the reference sponsor Reel and was approved for the first banner, but it overlaps the bottom 35% that `ads.md` keeps clear. A long caption on the host video can cover its lower edge. If the host's caption is long, move the card up to about top 900 |
| Length | About 20 seconds. Card enters at 1 s, exits at 17.6 to 18 s |
| States | 3 or 4: logo, one or two short messages, then the website |
| Words | At most 5 or 6 per state. The person rejected a three-column proof panel as "too complex" |
| Sound | None. The creator's audio plays underneath |

## Type and colour

Use the brand's own heading style: its font, sentence case, and its own tracking. Accent words in one solid brand colour.

Do not use bold uppercase, and do not put a gradient on text that is split into letters. Each letter gets its own copy of the gradient, so the colour bands letter by letter. The person called that version's "font weird and the color too".

Long lines are fitted to 740 px by `autofit()` after the fonts load, so a translation that runs long shrinks instead of wrapping.

## Process

1. `bash $PF/setup.sh ~/Movies/product-films/<slug> overlay` copies `assets/overlay.html` to `banner.html`.
2. Edit the brand tokens, the states in the HTML, and the `ST` timings. Each `.kl` line has a `data-k` start time for its letter rise. The shine sweep times in `render()` follow the state starts.
3. Publish `banner.html` as a private artifact so the person can watch it over a sample background with a scrubber. `preview.mjs` does not work on a banner (the page is transparent, so the white card shows on white). Your own first look is `check-overlay.jpg` from step 5. For a quick check, render a copy with `DUR` lowered.
4. If the text is not in English, show the person the lines before rendering.
5. Run `bash $PF/overlay-render.sh <dir> <slug>` in the background. Read `check-overlay.jpg`. (Edge strips do not apply here: the overlay is transparent outside its card.)
6. Copy the four files to `~/Downloads/<slug>/`.
7. Record the banner in `private/used.md`: claim a row marked "(in progress)" when you choose the design, and complete it when you deliver.

## Files to deliver

| File | For |
| --- | --- |
| `<slug>-alpha.mov` | ProRes 4444 with alpha, about 270 MB for 20 s. Premiere Pro, Final Cut Pro, DaVinci Resolve, After Effects. The default to send |
| `<slug>-greenscreen.mp4` | Phone editors without alpha support (CapCut, InShot, VN). They use Chroma Key on the green. The card is opaque white here and has no shadow, so keying stays clean |
| `<slug>-alpha.webm` | VP9 with alpha, for web pages. Most editors ignore its alpha. Do not send it to an editor |
| `<slug>-preview.mp4` | Approval only. The sample background is baked in |

Tell the person to send the `.mov` by WeTransfer or Google Drive. WhatsApp and email compress it, and compression drops the alpha. A ready line for the client: "Use the .mov in Premiere, Final Cut or DaVinci, and the green one in CapCut."
