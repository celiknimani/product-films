# Real footage

Use this when a film is built around real video: a creator's own rides, event footage, or a client's supplied clips. First made for the Newman Explorer reel (2026-11-08, `~/Movies/product-films/newmanexplorer/`, see its `edl.py`).

`$PF` is the skill's `scripts/` folder, `~/.claude/skills/product-films/scripts` (see SKILL.md, Process).

## Sources

- Prefer original files from the person. Downloading from a platform needs the person's yes in chat for the exact videos, with titles and sizes listed first, and only for their own content. `yt-dlp` with `-f "bv*[height<=1080][ext=mp4]"` fetches video only; for long videos use `--download-sections "*start-end"`.
- Put downloads in `<film folder>/footage/`.
- Free stock footage: Pexels clips allow commercial use with no credit, but Pexels blocks automated downloads, so get them through the person's own browser. Avoid clips with prominent brand logos (container lines, trucks). Record each clip's source URL in `brief.md`.

## Shot selection

1. Make a thumbnail grid of each source (one frame every 2 to 3 seconds) and pick candidate windows.
2. For each window, look at its first, middle and last frames for burned-in text: title cards, subtitles, overlays, watermarks. Move the window until it is clean.
3. Write the choices as an edit decision list (source, start, length in frames on the bar grid at 60fps) in a small script that cuts them with ffmpeg.

## Playback

- Playwright's Chromium cannot play H.264. Re-encode the cut to VP9 webm (`-c:v libvpx-vp9 -b:v 4M`). Keep each webm under 15MB so the preview artifact can carry it.
- `__seek` must wait for the video: set `currentTime`, await the `seeked` event, then two animation frames. `capture.mjs` and `preview.mjs` await whatever `__seek` returns. `__ready` must also wait for each video's `loadeddata`.
- Cover the full frame with the footage (`object-fit: cover`, overscanned like any full-bleed layer).

## Rules

- Never zoom or slowly push footage that shows readable text.
- For a 9:16 crop of 16:9 point-of-view footage, a centre crop puts the dashboard in the middle: check for readable speeds and crop higher or pick another moment. Tell the person about any speed that is readable.
- No white flash into the end card: it washes out the last footage frames. Hard cut.
- `text-still.mjs` still checks the type on top. The frame-difference crop check is meaningless over moving footage: judge text sharpness by eye on the crops instead.

## Source audio

- Download the audio separately (`yt-dlp -f ba -x --audio-format m4a`, same sections as the video) when the video files are video-only.
- Platform videos often carry added music. Use only stretches that are pure engine, wind or room sound: check a spectrogram per minute (engine harmonics glide with rpm; music shows held pitches, chord stacks and a steady beat), and reject stretches with steady tonal lines or a regular beat. Never reuse music from the source. Say in the report that this is a measurement, not a listen.
- Give each shot its own clean audio where possible, crossfade about 25 ms on the cut, and duck it under big hits.
- To change only the sound of a finished film, remux instead of re-rendering: `ffmpeg -i film.mp4 -i master.wav -map 0:v -map 1:a -c:v copy -af apad -c:a aac -b:a 256k -shortest out.mp4`.

