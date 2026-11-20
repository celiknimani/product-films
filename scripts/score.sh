#!/bin/bash
# Usage: bash score.sh <film-folder>. Runs score.py, then masters to -16 LUFS with a -1.5 dB peak ceiling (AAC adds about 0.4 dB, so the MP4 stays under -1) and prints levels.
set -e
[ $# -ge 1 ] || { echo "usage: score.sh <film-folder>"; exit 1; }
HERE="$(cd "$(dirname "$0")" && pwd)"; cd "$1" || exit 1
[ -f score.py ] || { echo "score.py missing in $1"; exit 1; }
PY="$HOME/.cache/product-film/venv/bin/python"
PYTHONPATH="$HERE" "$PY" score.py
# The score and the page must have the same length, or the render is cut short. This also catches the 6 s example score left in place.
SD=$(ffprobe -v error -show_entries format=duration -of csv=p=0 mix.wav)
HD=$(node "$HERE/page-dur.mjs" src.html 2>/dev/null || true)
if [ -z "$HD" ]; then echo "warning: could not read DUR from src.html, check it matches the score ($SD s)"
else python3 -c "import sys;sys.exit(0 if abs($SD-$HD)<0.05 else 1)" || { echo "length differs: score $SD s, page $HD s. Make DUR equal in score.py and src.html."; exit 1; }; fi
read I P <<< "$(ffmpeg -hide_banner -nostats -i mix.wav -af ebur128=peak=true:framelog=quiet -f null - 2>&1 | awk '/^ +I:/{i=$2}/^ +Peak:/{p=$2}END{print i,p}')"
# Gain to -16 LUFS, then a look-ahead limiter caps peaks at -1.5 dBFS, so big hits no longer pull the whole film below -16.
G=$(python3 -c "print(round(-16-($I),2))")
ffmpeg -y -loglevel error -i mix.wav -af "lowpass=f=16000,volume=${G}dB,alimiter=limit=0.84:attack=5:release=60:level=false" -c:a pcm_s16le master.wav
ffmpeg -y -loglevel error -i master.wav -c:a aac -b:a 160k -movflags +faststart page-audio.m4a
echo "mix ${I} LUFS, peak ${P} dB, gain ${G} dB"
L=$(ffmpeg -hide_banner -nostats -i master.wav -af ebur128=peak=true:framelog=quiet -f null - 2>&1 | grep -E "^ +(I|Peak):"); echo "$L"
TP=$(echo "$L" | awk '/Peak:/{print $2}'); python3 -c "import sys;sys.exit(0 if float('${TP:-0}')<=-1 else 1)" || echo "WARNING: true peak $TP dBFS, above -1. Lower the loudest hit before rendering, or the MP4 will clip after AAC."
