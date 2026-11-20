#!/bin/bash
# Usage: bash render.sh <film-folder> <slug> [reel]. Renders 16:9 and 9:16 at 1080p60 with sound, then runs the checks.
# With "reel" it renders only the 9:16 version (paid ads). Run it in the background.
set -e
[ $# -ge 2 ] || { echo "usage: render.sh <film-folder> <slug> [reel]"; exit 1; }
HERE="$(cd "$(dirname "$0")" && pwd)"; cd "$1" || exit 1; SLUG="$2"
[ -f master.wav ] || { echo "master.wav missing: run score.sh first"; exit 1; }
one(){ local f="$1" d="$2" o="$3" pids=() p want got
  [ -f "$f" ] || { echo "$f missing: run build.py first"; exit 1; }
  rm -rf "$d"; mkdir "$d"
  for i in 0 1 2 3 4 5; do node "$HERE/capture.mjs" "$f" "$d" $i 6 & pids+=($!); done
  # A failed worker leaves gaps in the frames, so stop instead of encoding a short, out-of-sync film.
  for p in "${pids[@]}"; do wait "$p" || { echo "capture shard failed for $f"; exit 1; }; done
  want=$(node "$HERE/page-dur.mjs" "$f" | python3 -c "import sys;print(round(float(sys.stdin.read())*60))")
  got=$(find "$d" -name 'f*.jpg' | wc -l | tr -d ' ')
  [ "$got" = "$want" ] || { echo "captured $got of $want frames for $f"; exit 1; }
  ffmpeg -y -loglevel error -framerate 60 -pattern_type glob -i "$d/f*.jpg" -vf "scale=in_range=full:out_range=tv,format=yuv420p" -c:v libx264 -preset slow -crf 17 -color_range tv -colorspace bt709 -color_primaries bt709 -color_trc bt709 -movflags +faststart "$d.mp4"
  ffmpeg -y -loglevel error -i "$d.mp4" -i master.wav -map 0:v -map 1:a -c:v copy -af apad -c:a aac -b:a 256k -shortest -movflags +faststart "$o"
  rm -f "$d.mp4"; }
[ "$3" = reel ] || one "$SLUG-film.html" frames-film "$SLUG-film.mp4"
one "$SLUG-reel.html" frames-reel "$SLUG-reel.mp4"
bash "$HERE/check.sh" . "$SLUG"
# The frames-* folders are kept for re-encoding (about 200 MB per 40 s film). Delete them once the film is approved.
