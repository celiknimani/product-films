#!/bin/bash
# Usage: bash overlay-render.sh <folder> <slug>. Renders banner.html as four files: ProRes 4444 and WebM with alpha,
# a green-screen MP4, and a preview over a sample video. Run it in the background.
set -e
[ $# -ge 2 ] || { echo "usage: overlay-render.sh <folder> <slug>"; exit 1; }
HERE="$(cd "$(dirname "$0")" && pwd)"; cd "$1" || exit 1; SLUG="$2"
[ -f banner.html ] || { echo "banner.html missing: run setup.sh <folder> overlay first"; exit 1; }
for m in alpha green; do rm -rf "fr-$m"; mkdir "fr-$m"; pids=(); for i in 0 1 2 3 4 5; do node "$HERE/overlay-capture.mjs" $m banner.html "fr-$m" $i 6 & pids+=($!); done
  for p in "${pids[@]}"; do wait "$p" || { echo "capture shard failed ($m)"; exit 1; }; done; done
node "$HERE/overlay-capture.mjs" host banner.html host.png
ffmpeg -y -loglevel error -framerate 60 -i fr-alpha/f%05d.png -c:v prores_ks -profile:v 4 -pix_fmt yuva444p10le -vendor apl0 "$SLUG-alpha.mov"
ffmpeg -y -loglevel error -framerate 60 -i fr-alpha/f%05d.png -c:v libvpx-vp9 -pix_fmt yuva420p -b:v 0 -crf 28 -row-mt 1 -auto-alt-ref 0 "$SLUG-alpha.webm"
ffmpeg -y -loglevel error -framerate 60 -i fr-green/f%05d.png -c:v libx264 -preset slow -crf 16 -pix_fmt yuv420p -movflags +faststart "$SLUG-greenscreen.mp4"
ffmpeg -y -loglevel error -loop 1 -framerate 60 -i host.png -framerate 60 -i fr-alpha/f%05d.png -filter_complex "[0][1]overlay=shortest=1,format=yuv420p" -c:v libx264 -preset slow -crf 17 -movflags +faststart "$SLUG-preview.mp4"
# Contact sheet of the banner area, one frame every 3 seconds, sampled from the final preview.
ffmpeg -y -loglevel error -i "$SLUG-preview.mp4" -vf "fps=1/3,crop=1080:560:0:1100,scale=540:-1,tile=1x7" -frames:v 1 check-overlay.jpg
ls -lh "$SLUG-alpha.mov" "$SLUG-alpha.webm" "$SLUG-greenscreen.mp4" "$SLUG-preview.mp4"
