#!/bin/bash
# Usage: bash check.sh <film-folder> <slug> [times...]. Reports format and loudness, and samples frames from the final MP4s into contact sheets.
# Set START to add an offset to every time (times relative to a scene). Set NAME to keep a second sheet, for example NAME=ending writes check-ending-film.jpg instead of check-film.jpg.
[ $# -ge 2 ] || { echo "usage: check.sh <film-folder> <slug> [times...]"; exit 1; }
HERE="$(cd "$(dirname "$0")" && pwd)"; cd "$1" || exit 1; SLUG="$2"; shift 2
for k in film reel; do F="$SLUG-$k.mp4"; [ -f "$F" ] || continue
  ffprobe -v error -show_entries stream=codec_name,width,height,duration -of compact=p=0 "$F"
  L=$(ffmpeg -hide_banner -nostats -i "$F" -af ebur128=peak=true:framelog=quiet -f null - 2>&1 | grep -E "^ +(I|Peak):"); echo "$L"
  PK=$(echo "$L" | awk '/Peak:/{print $2}'); python3 -c "import sys;sys.exit(0 if float('${PK:-0}')<=-1 else 1)" || echo "WARNING: $F peaks at $PK dBFS after AAC. Lower the hit or low-pass harsh square or noise parts, re-run score.sh, re-render."
  D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$F"); T=$(mktemp -d)
  if [ $# -gt 0 ]; then TS=$(python3 -c "import sys;print(' '.join(str(round(float(a)+${START:-0},3)) for a in sys.argv[1:]))" "$@"); else TS=$(python3 -c "d=$D;print(' '.join(str(round(d*(i+.5)/15,2)) for i in range(15)))"); fi
  i=0; for t in $TS; do ffmpeg -y -loglevel error -ss "$t" -i "$F" -frames:v 1 -q:v 3 "$T/m$(printf %03d $i).jpg"; i=$((i+1)); done
  C=5; [ "$k" = reel ] && C=8
  ffmpeg -y -loglevel error -pattern_type glob -i "$T/m*.jpg" -filter_complex "tile=${C}x$(( (i + C - 1) / C )):padding=6,scale=2000:-1" -frames:v 1 "check${NAME:+-$NAME}-$k.jpg"; rm -rf "$T"
  echo "sheet: $PWD/check${NAME:+-$NAME}-$k.jpg"
done
P="$SLUG-film.html"; [ -f "$P" ] || P="$SLUG-reel.html"
node "$HERE/sound-test.mjs" "$PWD/$P" 2>/dev/null || echo "sound test failed: run node $HERE/sound-test.mjs $PWD/$P to see why"
