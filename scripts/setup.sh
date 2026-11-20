#!/bin/bash
# Usage: bash setup.sh <film-folder> [overlay]. Creates the folder and the shared tools once per machine.
# With "overlay" it starts from the sponsor banner template instead of the film template.
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
FILM="$1"; [ -z "$FILM" ] && { echo "usage: setup.sh <film-folder> [overlay]"; exit 1; }
TOOLS="$HOME/.cache/product-film"
# ffmpeg, Node and Python are not installed here. Stop with a clear message if one is missing.
MISSING=""; for c in ffmpeg ffprobe node npm python3; do command -v "$c" >/dev/null || MISSING="$MISSING $c"; done
if [ -n "$MISSING" ]; then echo "missing:$MISSING. On macOS: brew install ffmpeg node python"; exit 1; fi
mkdir -p "$TOOLS" "$FILM"
[ -x "$TOOLS/venv/bin/python" ] || python3 -m venv "$TOOLS/venv"
# The cache keeps its old name (~/.cache/product-film) on purpose: renaming it would reinstall Chromium for every existing film folder.
"$TOOLS/venv/bin/python" -c "import numpy, scipy" 2>/dev/null || "$TOOLS/venv/bin/pip" install -q numpy scipy
if [ ! -d "$TOOLS/node_modules/playwright" ]; then (cd "$TOOLS" && npm init -y >/dev/null && npm i playwright 2>&1 | tail -1); fi
# Chromium renders the frames. This is quick when the matching browser is already cached.
(cd "$TOOLS" && npx playwright install chromium 2>&1 | tail -1)
ln -sfn "$TOOLS/node_modules" "$FILM/node_modules"
if [ "$2" = overlay ]; then [ -f "$FILM/banner.html" ] || cp "$HERE/../assets/overlay.html" "$FILM/banner.html"; echo "ready: $FILM"; exit 0; fi
mkdir -p "$FILM/img"
[ -f "$FILM/src.html" ] || cp "$HERE/../assets/stage.html" "$FILM/src.html"
[ -f "$FILM/score.py" ] || cp "$HERE/../assets/score_example.py" "$FILM/score.py"
echo "ready: $FILM"
