# Paid social ads

`$PF` is the skill's `scripts/` folder, `~/.claude/skills/product-films/scripts` (see SKILL.md, Process).

Use this when the video is a paid ad on Instagram or Facebook rather than an organic film. First made for an ad aimed at roofers in Germany (2026-10-31).

## Shape

These figures come from third-party guides on Meta Reels ads and are not verified against Meta's own documentation.

| Setting | Default |
| --- | --- |
| Format | 9:16 Reel only, 1080x1920. Render with `bash $PF/render.sh <dir> <slug> reel` |
| Length | 15 to 30 seconds. 20 seconds worked |
| Hook | The problem on screen within the first 1.5 to 3 seconds, before any logo |
| Safe zone | Keep text out of the top 14%, the bottom 35% and 6% on each side. Instagram's caption, name and buttons cover those areas. On the template's 900x1600 Reel stage, set `.reel .sc` padding to 224 top, 560 bottom and 54 on each side. This replaces the film default of y 170 to 1250 |
| Ending | Logo, one call to action, the URL. This replaces the ending card in `ending.md` |
| Sound | Designed to work muted: the words on screen carry the message. Music and effects are a bonus |

## Content rules

- Never name clients, even from published case studies. Describe them by trade and country, such as "a roofing company in Bavaria".
- Use the target market's language and trade words. Show the person every line and ask for a native read before rendering.
- Tie the visual to the viewer's own work: for roofers, a roof, rain and a loose tile, not generic charts.

## Report to the person

Raise these every time, since none can be checked from code:

- The ad needs the platform's paid-partnership or "Werbung" label (Germany) when it runs.
- Ranking or "number one" claims may need a legal check under the local unfair competition law, such as the UWG in Germany.
- Whether a landing page exists in the ad's language. Sending German roofers to an English page wastes the click.
- The music has not been heard.
