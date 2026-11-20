# The ending card

`$PF` is the skill's `scripts/` folder, `~/.claude/skills/product-films/scripts` (see SKILL.md, Process).

Every film made for a client ends with this card, unless the request says otherwise. It signs the film with Celik's name and celiknimani.com, in the colours of his site (`brands.md`). The motion dates from 2026-11-08, when Celik asked for an ending with "more power, more dynamic, more kinetic", the website in the bottom area of the screen, and "a dynamic dot moving and stopping by the .com". It became the personal card on 2026-11-20.

It sits on the film's own background (light or dark), not on a separate black frame, and lasts about 4 seconds: two bars at most tempos. Lengthen `DUR` and the score to fit it rather than squeezing the last client scene. The card may take the film past the 40-second default; that is fine. Cut to it hard on a bar line: remove any shutter or wipe transition that runs into it.

## Beats

Times are from the card's first frame. If the beat nearest 0.95 s falls at 0.95 + d, add d to every time from 0.30 on; the cut and the bars stay at 0.00, and the contact-sheet times in Rules are before the shift (add d to each). The spark starts off-frame at the top left; the final dot is 0.2em of the URL font.

Colours: ink #121212, lime #c9fe6e, light #f1f1f1, muted #777777. On a dark background the text is #f1f1f1 and the spark, ring and rule are lime. Lime is too faint on a light background, so there the text, spark, ring and rule are #121212 and lime appears only in the bars and as a soft glow around the spark.

| Time | What happens |
| --- | --- |
| 0.00 | Hard cut to the film's plain background. Three bars (lime #c9fe6e, then #f1f1f1 on a dark background or #121212 on a light one, then lime again), about 180px thick on both stages, sweep across at a -24 degree skew and clear by 0.45 s. A short camera push runs on these bars only |
| 0.30 | "Built by" types in, in a small mono label: Geist Mono 500, letter-spaced .2em, muted colour, 24px on the 16:9 stage and 20px on the Reel stage, centred above the wordmark |
| 0.45 | "CELIK NIMANI" (Geist 600, letter-spacing .08em) rises letter by letter from below, 35 ms apart, with the template's `eo` (a quartic ease-out that lands exactly) and no overshoot; set each letter's transform to `none` once landed. On the 1600x900 stage it is one line at about 130px (about 990px wide). On the 900x1600 Reel stage it is two lines, CELIK over NIMANI, at about 150px with line-height 1 (NIMANI is about 610px wide). Every letter has landed by 0.95 s and then stays still |
| 0.80 | The spark (a 22px dot with a soft glow and a short fading trail) shoots in from off-frame on a curved path and arrives at the left end of the wordmark's baseline at 0.95 s |
| 0.95 | The impact: a thin ring (300px wide, scaling from 0.35 to 2.25 while fading) bursts from the spark's arrival point. The score's biggest hit lands here |
| 0.95 to 1.40 | The spark races left to right along the baseline and draws the rule (4px, solid) behind it, ending under the last letter. On the Reel it runs under NIMANI, the last line |
| 1.40 | "celiknimani" and "com" rise 12px into the bottom area with a gap where the full stop belongs: centred, about 88% down in 16:9 and at y 1250 on the Reel stage (78% down, the edge of the safe area). For a vertical-first social promo that uses the tighter zone in `ads.md`, place it at about y 960 instead (paid ads end on logo, call to action and URL, not on this card). Geist Mono 500, about 44px on the 16:9 stage and 40px on the Reel stage, letter-spaced .06em (30px read as too small for the dot to carry the ending), same colour as the wordmark |
| 1.45 to 1.95 | The spark leaves the end of the rule, arcs down across the frame and lands in the gap as the full stop of ".com". It shrinks from 22px to the size of a bold full stop as it lands, squashes once on impact and settles. A small second ring flashes from it |
| 1.95 to end | The spark stays where it landed as the dot in "celiknimani.com". Everything holds still for at least 1.5 s. No pulsing, drifting or particles |

Without a URL (a channel promo ending on a handle), the spark lands as the full stop of a short closing line, such as "Follow the ride."

## Build

- Write the URL as three parts: `<span>celiknimani</span><span class="dotslot"></span><span>com</span>`. The slot is an empty inline-block the width of a full stop with `height:0`, so its bottom edge sits on the text baseline where a real full stop sits. The spark is a separate absolutely positioned element; at the end, set its position to the slot's centre, measured in `__ready` from `offsetLeft` and `offsetTop` (unscaled, unaffected by transforms; `getBoundingClientRect` is scaled in the preview player), rounded to whole pixels.
- Add Geist 600 and Geist Mono 500 to the Google Fonts link and to `FONTS`.
- Move the spark along a curve, such as a quadratic Bezier with a control point above the line, eased in and out. A straight slide looks weak.
- Show and hide the card's parts (bars, rule, spark, rings) with the engine's `vis()`, which uses `inherit`, never `visibility='visible'`, or they stay on screen over earlier scenes when playback seeks back.
- Round every final position to whole pixels, so nothing sits on a half pixel once it lands.
- Put the rule just under the glyphs: measure the baseline with an empty `inline-block` span of zero width and height placed after the last letter (its bottom edge is the baseline), then set the rule's top 0.06em of the wordmark's font size below it. Fixed em offsets from the top of the line box differ per font: the 0.92em used with Inter puts the rule through Geist's letters.
- The rule ends at the last letter's right edge, measured on that letter's own span minus its trailing letter-spacing (0.08em). The wordmark element is wider by its trailing letter-spacing, so measuring it makes the rule overshoot the I.

## Sound

A riser in the last bar of the client scene, a whoosh on the bars, a tick per typed letter, a hard hit with a sub drop at 0.95 s, a fast rising sweep while the spark draws the rule, a bright metallic hit when the spark lands as the dot, and the last chord ringing out under the URL. Use the film's own instruments so the ending belongs to its score. Keep the hit's peak in line with the loudest earlier section: `score.sh` lowers the whole mix to keep peaks under -1.5 dB, so an oversized hit makes the entire film quieter.

## Rules

- Text never moves after it lands. All motion after landing is on graphics (bars, rings, spark), and it ends when the spark becomes the dot.
- No overshoot or bounce on letters: an overshoot reads as wobble.
- Keep the name in capitals, CELIK NIMANI, as in the celiknimani.com films. It is a signature, not a heading, so the sentence-case rule for banners does not apply here.
- Check this card with its own contact sheet at 0.2, 0.6, 1.0, 1.4, 1.7, 2.0 and the last frame, adding the shift d to each time from 0.6 on (pass `START=` as the card start), and run `text-still.mjs`. The dot is too small to judge at contact-sheet scale: crop the URL on the last frame at full size to confirm it sits as the full stop. For the sheet, run `NAME=ending START=<card start in seconds> bash $PF/check.sh <dir> <slug> 0.2 0.6 1.0 1.4 1.7 2.0 <last>` so it does not overwrite the full-film sheets.
