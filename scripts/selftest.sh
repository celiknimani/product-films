#!/bin/bash
# Usage: bash selftest.sh. Builds the template film in a temp folder and runs every script and check on it.
# Takes about a minute. Run it after changing any script or template.
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
PY="$HOME/.cache/product-film/venv/bin/python"
T="$(mktemp -d)/selftest film"
step(){ echo "== $1"; }
step setup;      bash "$HERE/setup.sh" "$T" | tail -1
step score;      bash "$HERE/score.sh" "$T" | tail -1
step build;      python3 "$HERE/build.py" "$T" t "Selftest"
step preview;    node "$HERE/preview.mjs" "$T/t-film.html" "$T/sheet-film.jpg" 1 4
step text-still; node "$HERE/text-still.mjs" "$T/t-film.html" | tail -1; node "$HERE/text-still.mjs" "$T/t-reel.html" | tail -1
step render;     bash "$HERE/render.sh" "$T" t >/dev/null
step edge-check; "$PY" "$HERE/edge-check.py" "$T/t-film.mp4"; "$PY" "$HERE/edge-check.py" "$T/t-reel.mp4"
step formats
for k in film reel; do ffprobe -v error -show_entries stream=width,height:format=duration -of csv=p=0 "$T/t-$k.mp4" | tr '\n' ' '; echo; done
step overlay;    O="$T-overlay"; bash "$HERE/setup.sh" "$O" overlay | tail -1
sed -i '' 's/const DUR=20/const DUR=2/' "$O/banner.html"
bash "$HERE/overlay-render.sh" "$O" o | awk '{print $5, $9}'
rm -rf "$(dirname "$T")"
echo "selftest passed"
