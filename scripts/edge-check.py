"""Usage: python edge-check.py <video.mp4>. Finds frames where a thin strip along a frame edge differs from what is just inside it:
a full-bleed layer that was moved, scaled or inset so the page behind shows.
It looks for strips up to about 12 px wide, so real content placed 16 px or more from the edge does not trigger it. Run it with the skill's venv python. Exit code 1 if found."""
import subprocess, sys
import numpy as np
f = sys.argv[1]
probe = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v', '-show_entries', 'stream=width,height', '-of', 'csv=p=0', f], capture_output=True, text=True).stdout.strip().split(',')
W, H = int(probe[0]) // 2, int(probe[1]) // 2
FPS = 10
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', f, '-vf', f'fps={FPS},scale={W}:{H}', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True).stdout
fr = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3).astype(np.int16)

def strip(edge, inner):
    """True when the outer band is uniform along the edge and clearly different from the band just inside."""
    e, i = edge.reshape(-1, 3), inner.reshape(-1, 3)
    if e.std(0).max() > 6: return False          # the edge band itself varies: real content, not a gap
    return np.abs(e.mean(0) - i.mean(0)).max() > 10

hits = {}
for n, im in enumerate(fr):
    for side, (edge, inner) in {
        'top': (im[0:2, 8:-8], im[6:8, 8:-8]),
        'bottom': (im[-2:, 8:-8], im[-8:-6, 8:-8]),
        'left': (im[8:-8, 0:2], im[8:-8, 6:8]),
        'right': (im[8:-8, -2:], im[8:-8, -8:-6]),
    }.items():
        if strip(edge, inner): hits.setdefault(side, []).append(n / FPS)

def runs(ts):
    out, a, b = [], None, None
    for t in ts:
        if a is None: a = b = t
        elif t - b <= 1.5 / FPS: b = t
        else: out.append((a, b)); a = b = t
    if a is not None: out.append((a, b))
    return [r for r in out if r[1] - r[0] >= 0.15]

bad = False
for side, ts in hits.items():
    r = runs(ts)
    if r:
        bad = True
        print(f'{f.split("/")[-1]}: {side} edge strip at ' + ', '.join(f'{a:.1f}-{b:.1f}s' for a, b in r))
if not bad: print(f'{f.split("/")[-1]}: no edge strips')
sys.exit(1 if bad else 0)
