# Music and sound

Claude cannot hear. Judge a score by structure and measurement, and say so in the report.

## Writing a score

1. Choose a genre, tempo, key and instruments that differ from every row in `private/used.md`. Avoid using the same instruments in a new order: that reads as the same track.
2. Pick the tempo from the cut list. One bar lasts `240 / BPM` seconds. 125 BPM gives 1.92 s, 100 BPM gives 2.4 s, 96 BPM gives 2.5 s. Move scene cuts onto bars.
3. Shape energy by scene: sparse under setup, thin under text that needs reading, full on proof and results, a clear landing on the close.
4. Place effects from the same times as the animation: typing per character, a whoosh centered on each cut, pops for arrivals, a pitched note for each stat or status. Keep chimes in the song's key.
5. To stretch or insert time, wrap `add` with a time map rather than editing every cue.

## Toolkit (`scripts/soundkit.py`)

| Family | Functions |
| --- | --- |
| Electronic | `pad_note fm_pluck bell bass_note kick hat clap` |
| Acoustic | `piano strings ks` (plucked string) `snap shaker soft_kick` |
| Mallet and wood | `mar low wood tom box_kick rim shk stab drone` |
| Garage | `rhodes chop` (vocal) `sub gkick snare chat rim2` |
| Effects | `noise_swell tick tap pop thump` |
| Mixing | `add blank init m2f lp hp bp swing verb pump finish write_wav` |

These are parts. Add new instruments to the score when the genre needs them: brass, choir, tape, drum machines. Good unused directions: drum and bass, lo-fi hip hop, cinematic strings, Balkan brass, afrobeats, synthwave, ambient, funk.

## Mix targets

Measure each scene with RMS, and view a spectrum if the mix seems flat:

- A scene RMS range of about 8 to 10 dB, from intro to fullest section. Leave the final hit and the quiet credit card out of the range.
- Check that a pad or strings stem is not the loudest thing. High-pass pads near 170 Hz to clear the low mids.
- `score.sh` masters to -16 LUFS with peaks no higher than -1.5 dB (under -1 dB after AAC encoding).

Stems are written as `music.wav` and `sfx.wav`, so a licensed track can replace the music while the effects stay.

## Notes

- `from soundkit import *` copies `N` and `rng` at import time, so they stay at their old values after `init()`. Use `soundkit.N` (after `import soundkit`) for the sample count.
- To change tempo after the page is built, keep the scene code in old-bar time and map it: `const KT=t=>t*OLD_BPM/NEW_BPM` (or a piecewise map), and call `render` with the mapped time. Every cut stays on a bar.
