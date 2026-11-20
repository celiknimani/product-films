"""A working 6-second score, to show the shape of a score.py. Replace the musical choices entirely for each film."""
from soundkit import *

DUR = 6.0        # must equal DUR in src.html
BAR = 1.5        # 4 beats at 160 BPM. Pick a tempo whose bars land on your scene cuts, then move the cuts onto bars.
STEP = BAR / 16
init(DUR)

keys, bass, drums, sfx = blank(), blank(), blank(), blank()
CHORDS = [[57, 60, 64], [53, 57, 60], [55, 59, 62], [52, 55, 59]]

kicks = []
for b in range(4):
    t0 = b * BAR
    for s in (0, 6, 10):
        for m in CHORDS[b]:
            add(keys, swing(t0, s, STEP), rhodes(m2f(m), .5, .8), pan=(m - 58) / 14, gain=.2)
    for s in (0, 8):
        add(drums, t0 + s * STEP, kick(), gain=.6)
        kicks.append(t0 + s * STEP)
    add(bass, t0, sub(m2f(CHORDS[b][0] - 24), m2f(CHORDS[b][0] - 24), BAR * .8), gain=.4)

add(sfx, 2.73, noise_swell(.54, 500, 6000, .5), gain=.16)   # whoosh, centered on the cut at 3.0
add(sfx, 4.6, pop(880), gain=.16)                           # the number lands

duck = pump(kicks)
finish({'keys': keys * duck, 'bass': bass, 'drums': drums}, {'sfx': sfx}, verb_sends={'keys': .3})
