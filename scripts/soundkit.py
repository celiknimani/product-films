"""Sound toolkit for product films. Usage:

    from soundkit import *
    init(dur=30.0)
    pad = blank(); add(pad, 1.0, piano(m2f(60)), pan=.2, gain=.3)
    ...
    finish({'keys': keys, 'drums': drums}, {'sfx': sfx}, verb_sends={'keys': .3})

Instruments return mono or stereo arrays. Every sound is synthesized, so nothing here needs a licence.
These are building blocks. Each film needs its own genre, tempo and key; see references/music.md.
"""
import wave
import numpy as np
from scipy.signal import butter, sosfilt, fftconvolve, lfilter

SR = 48000
DUR = 0.0
N = 0
rng = np.random.default_rng(38)


def init(dur, seed=38):
    """Set the film length in seconds. Call once, before blank() or add()."""
    global DUR, N, rng
    DUR = dur
    N = int(dur * SR)
    rng = np.random.default_rng(seed)


def m2f(m): return 440.0 * 2 ** ((m - 69) / 12)
def blank(): return np.zeros((N, 2))
def tvec(d): return np.arange(int(d * SR)) / SR


def add(buf, t, sig, pan=0.0, gain=1.0):
    """Mix a mono or stereo signal into buf at time t with an equal-power pan."""
    i = int(t * SR)
    if i >= N or i < 0: return
    sig = sig[: N - i]
    if sig.ndim == 1:
        a = (pan + 1) * np.pi / 4
        buf[i:i + len(sig), 0] += sig * np.cos(a) * gain
        buf[i:i + len(sig), 1] += sig * np.sin(a) * gain
    else:
        buf[i:i + len(sig)] += sig * gain


def lp(x, f, o=2): return sosfilt(butter(o, f, 'low', fs=SR, output='sos'), x, axis=0)


def hp(x, f, o=2): return sosfilt(butter(o, f, 'high', fs=SR, output='sos'), x, axis=0)


def bp(x, a, b, o=2): return sosfilt(butter(o, [a, b], 'band', fs=SR, output='sos'), x, axis=0)


# Electronic, from the first Zani score
def pad_note(f, d, bright=.4, atk=.25, rel=1.2):
    t = tvec(d + rel)
    env = np.minimum(t / atk, 1) * np.where(t > d, np.exp(-(t - d) / (rel / 3)), 1)
    out = np.zeros((len(t), 2))
    for det, pan in ((-.0035, -.7), (0, 0), (.0035, .7)):
        ff = f * (1 + det)
        s = np.zeros(len(t))
        for n in range(1, 11):
            if ff * n > 9000: break
            s += np.sin(2 * np.pi * ff * n * t + rng.uniform(0, 6.28)) / n ** (2.1 - bright * 1.3)
        a = (pan + 1) * np.pi / 4
        out[:, 0] += s * np.cos(a)
        out[:, 1] += s * np.sin(a)
    return out * env[:, None] * .2


def fm_pluck(f, d=.42, idx=2.2, vel=1.0):
    t = tvec(d)
    I = idx * np.exp(-t * 16) * vel
    s = np.sin(2 * np.pi * f * t + I * np.sin(2 * np.pi * f * 2 * t))
    s += .22 * np.sin(2 * np.pi * f * 4.01 * t) * np.exp(-t * 34)
    atk = np.minimum(t / .002, 1)
    return s * atk * np.exp(-t * 6.5) * vel


def bell(f, d=2.2, vel=1.0):
    t = tvec(d)
    s = np.sin(2 * np.pi * f * t + 1.3 * np.exp(-t * 3) * np.sin(2 * np.pi * f * 3.5 * t))
    s += .3 * np.sin(2 * np.pi * f * 2 * t) * np.exp(-t * 3.5)
    return s * np.minimum(t / .003, 1) * np.exp(-t * 2.4) * vel


def bass_note(f, d, vel=1.0):
    t = tvec(d)
    s = np.sin(2 * np.pi * f * t) + .18 * np.sin(2 * np.pi * f * 2 * t)
    s = np.tanh(1.6 * s) / 1.2
    env = np.minimum(t / .006, 1) * np.minimum((d - t) / .03, 1).clip(0)
    return s * env * vel


def kick(vel=1.0):
    t = tvec(.34)
    ph = 2 * np.pi * np.cumsum(46 + 92 * np.exp(-t * 32)) / SR
    s = np.sin(ph) * np.exp(-t * 8.5)
    c = hp(rng.normal(size=len(t)), 2500) * np.exp(-t * 400) * .12
    return (s + c) * vel


def hat(vel=1.0, dec=70):
    t = tvec(.08)
    return hp(rng.normal(size=len(t)), 7500) * np.exp(-t * dec) * vel


def clap(vel=1.0):
    t = tvec(.2)
    n = bp(rng.normal(size=len(t)), 1100, 4200)
    e = np.exp(-t * 26) + .6 * np.exp(-np.maximum(t - .012, 0) * 60) * (t > .012)
    return n * e * vel


# Sound effects
def noise_swell(d, f0, f1, peak=.75, stereo=True):
    """Filtered noise that sweeps f0 to f1 and peaks at `peak` of its length. Whooshes and risers."""
    n = int(d * SR)
    x = rng.normal(size=n)
    out = np.zeros(n)
    hop = 512
    prev = np.zeros(n)
    y = np.zeros(n)
    # Crude time-varying one-pole lowpass, sample-accurate enough for a sweep.
    fc = f0 * (f1 / f0) ** (np.arange(n) / n)
    a = 1 - np.exp(-2 * np.pi * fc / SR)
    z = 0.0
    for i in range(n):
        z += a[i] * (x[i] - z)
        y[i] = z
    y = hp(y, 90)
    t = np.arange(n) / n
    env = np.where(t < peak, (t / peak) ** 2, ((1 - t) / (1 - peak)) ** 1.6)
    y = y * env
    y /= np.abs(y).max() + 1e-9
    if not stereo: return y
    p = np.sin(t * np.pi)  # gentle stereo drift
    return np.stack([y * (1 - .35 * p), y * (.65 + .35 * p)], 1)


def tick(f=1800, d=.03, vel=1.0):
    t = tvec(d)
    return np.sin(2 * np.pi * f * t) * np.exp(-t * 170) * vel + hp(rng.normal(size=len(t)), 3000) * np.exp(-t * 500) * .35 * vel


def tap(vel=1.0):
    t = tvec(.09)
    body = np.sin(2 * np.pi * (520 + 260 * np.exp(-t * 90)) * t) * np.exp(-t * 62)
    return (body + hp(rng.normal(size=len(t)), 2600) * np.exp(-t * 420) * .5) * vel


def pop(f=660, vel=1.0):
    t = tvec(.16)
    ph = 2 * np.pi * np.cumsum(f * (1 + .55 * (1 - np.exp(-t * 34)))) / SR
    return np.sin(ph) * np.minimum(t / .004, 1) * np.exp(-t * 24) * vel


def thump(f=44, d=1.4, vel=1.0):
    t = tvec(d)
    ph = 2 * np.pi * np.cumsum(f + 70 * np.exp(-t * 18)) / SR
    return np.tanh(1.5 * np.sin(ph)) * np.exp(-t * (4 / d)) * vel


# Acoustic, from the astraHR score
def piano(f, d=1.8, vel=1.0):
    t = tvec(d)
    s = np.zeros(len(t))
    B = .0004
    for n in range(1, 11):
        fn = f * n * np.sqrt(1 + B * n * n)
        if fn > 7000: break
        s += np.sin(2 * np.pi * fn * t + n) * (1 / n ** (1.9 - .7 * vel)) * np.exp(-t * (1.1 + .85 * n))
    s += lp(rng.normal(size=len(t)), 900) * np.exp(-t * 60) * .25   # felt on the string
    return s * np.minimum(t / .006, 1) * vel


def strings(f, d, atk=.55, rel=.9, bright=.45):
    t = tvec(d + rel)
    env = np.minimum(t / atk, 1) ** 1.5 * np.where(t > d, np.exp(-(t - d) / (rel / 3)), 1)
    vib = 1 + .0028 * np.sin(2 * np.pi * 5.1 * t + rng.uniform(0, 6)) * np.minimum(t / .8, 1)
    out = np.zeros((len(t), 2))
    for det, pan in ((-.003, -.8), (-.001, -.3), (.001, .3), (.003, .8)):
        ph = 2 * np.pi * np.cumsum(f * (1 + det) * vib) / SR
        v = sum(np.sin(n * ph + rng.uniform(0, 6)) / n ** (2.3 - bright) for n in range(1, 9) if f * n < 8000)
        a = (pan + 1) * np.pi / 4
        out[:, 0] += v * np.cos(a); out[:, 1] += v * np.sin(a)
    return out * env[:, None] * .14


def ks(f, d=1.0, g=.992, bright=2600):
    """Karplus-Strong plucked string, run as a comb filter so it stays fast."""
    n = int(d * SR); L = max(2, int(round(SR / f)))
    x = np.zeros(n); x[:L] = lp(rng.uniform(-1, 1, L), bright)
    a = np.zeros(L + 2); a[0] = 1; a[L] = -g * .5; a[L + 1] = -g * .5
    return lfilter([1], a, x)


def snap(vel=1.0):
    t = tvec(.12)
    return bp(rng.normal(size=len(t)), 1500, 5200) * np.exp(-t * 48) * vel


def shaker(vel=1.0):
    t = tvec(.07)
    return hp(rng.normal(size=len(t)), 5200) * np.minimum(t / .012, 1) * np.exp(-t * 75) * vel


def soft_kick(vel=1.0):
    t = tvec(.3)
    ph = 2 * np.pi * np.cumsum(52 + 60 * np.exp(-t * 40)) / SR
    return np.sin(ph) * np.exp(-t * 11) * vel


# Mallets and wood
def mar(f, d=.8, vel=1.0):
    t = tvec(d)
    s = np.sin(2 * np.pi * f * t) + .42 * np.sin(2 * np.pi * f * 3.93 * t) * np.exp(-t * 26) + .13 * np.sin(2 * np.pi * f * 9.2 * t) * np.exp(-t * 70)
    return s * np.minimum(t / .0015, 1) * np.exp(-t * (4.2 + f / 520)) * vel


def low(f, d, vel=1.0):
    t = tvec(d)
    s = sum(((-1) ** k) * np.sin(2 * np.pi * f * (2 * k + 1) * t) / (2 * k + 1) ** 2 for k in range(4))
    return np.tanh(1.3 * s) * np.minimum(t / .004, 1) * np.exp(-t * 3.2) * np.minimum((d - t) / .02, 1).clip(0) * vel


def wood(f=1050, vel=1.0):
    t = tvec(.07)
    return (np.sin(2 * np.pi * f * t) + .5 * np.sin(2 * np.pi * f * 2.7 * t)) * np.exp(-t * 95) * vel


def tom(f=92, vel=1.0):
    t = tvec(.5)
    ph = 2 * np.pi * np.cumsum(f * (1 + .7 * np.exp(-t * 28))) / SR
    return np.sin(ph) * np.exp(-t * 7.5) * vel


def box_kick(vel=1.0):
    t = tvec(.26)
    ph = 2 * np.pi * np.cumsum(58 + 74 * np.exp(-t * 42)) / SR
    return (np.sin(ph) + .16 * hp(rng.normal(size=len(t)), 1800) * np.exp(-t * 160)) * np.exp(-t * 13) * vel


def rim(vel=1.0):
    t = tvec(.05)
    return (np.sin(2 * np.pi * 1720 * t) + bp(rng.normal(size=len(t)), 1900, 6000) * .8) * np.exp(-t * 130) * vel


def shk(vel=1.0):
    t = tvec(.06)
    return hp(rng.normal(size=len(t)), 6000) * np.minimum(t / .008, 1) * np.exp(-t * 90) * vel


def stab(notes, d=.5, vel=1.0):
    t = tvec(d)
    s = np.zeros(len(t))
    for m in notes:
        f = m2f(m)
        s += sum(np.sin(2 * np.pi * f * (1 + e) * n * t) / n ** 1.5 for n in range(1, 7) for e in (-.002, .002)) / 2
    return s * np.minimum(t / .01, 1) * np.exp(-t * 6) * vel


def drone(f, d, atk=.6):
    t = tvec(d)
    s = np.sin(2 * np.pi * f * t) + .5 * np.sin(2 * np.pi * f * 2.003 * t) + .2 * np.sin(2 * np.pi * f * 3 * t)
    return s * np.minimum(t / atk, 1) * np.minimum((d - t) / .7, 1).clip(0)


# Garage
def rhodes(f, d=.8, vel=1.0):
    t = tvec(d)
    I = 1.6 * vel * np.exp(-t * 7)
    s = np.sin(2 * np.pi * f * t + I * np.sin(2 * np.pi * f * t)) + .22 * np.sin(2 * np.pi * f * 14 * t) * np.exp(-t * 34) * vel
    return s * (1 + .12 * np.sin(2 * np.pi * 4.6 * t)) * np.minimum(t / .003, 1) * np.exp(-t * 3.4) * np.minimum((d - t) / .03, 1).clip(0) * vel


def chop(f, d=.2, vowel=(700, 1150), vel=1.0):
    """A formant-filtered saw, the shape of a chopped vocal."""
    t = tvec(d)
    vib = 1 + .006 * np.sin(2 * np.pi * 6 * t)
    ph = 2 * np.pi * np.cumsum(f * vib) / SR
    s = sum(np.sin(n * ph) / n for n in range(1, 26) if f * n < 9000)
    y = bp(s, vowel[0] * .8, vowel[0] * 1.25) + .7 * bp(s, vowel[1] * .85, vowel[1] * 1.2) + .25 * bp(s, 2500, 3100)
    return y * np.minimum(t / .006, 1) * np.minimum((d - t) / .02, 1).clip(0) * vel


def sub(f0, f1, d, vel=1.0):
    t = tvec(d)
    fr = f1 + (f0 - f1) * np.exp(-t * 26)
    s = np.sin(2 * np.pi * np.cumsum(fr) / SR)
    return np.tanh(1.5 * s) * np.minimum(t / .005, 1) * np.minimum((d - t) / .025, 1).clip(0) * vel


def gkick(vel=1.0):
    t = tvec(.3)
    ph = 2 * np.pi * np.cumsum(50 + 150 * np.exp(-t * 55)) / SR
    return (np.sin(ph) * np.exp(-t * 9.5) + .1 * hp(rng.normal(size=len(t)), 3000) * np.exp(-t * 300)) * vel


def snare(vel=1.0):
    t = tvec(.2)
    tone = np.sin(2 * np.pi * 196 * t) * np.exp(-t * 34)
    n = bp(rng.normal(size=len(t)), 1400, 7000) * np.exp(-t * 22)
    return (.6 * tone + n) * vel


def chat(open_=False, vel=1.0):
    t = tvec(.22 if open_ else .05)
    return hp(rng.normal(size=len(t)), 8000) * np.exp(-t * (16 if open_ else 110)) * vel


def rim2(vel=1.0):
    t = tvec(.04)
    return (np.sin(2 * np.pi * 1900 * t) + .6 * hp(rng.normal(size=len(t)), 4000)) * np.exp(-t * 170) * vel


def swing(bar_t, step, step_len, amount=.024):
    """Time of a 16th-note step, with even steps pushed late for a shuffle."""
    return bar_t + step * step_len + (amount if step % 2 else 0)


def verb(x, seconds=1.4, decay=5.2, tone=6000):
    """A small synthetic room. Larger seconds and smaller decay give a bigger space."""
    t = tvec(seconds)
    ir = np.stack([lp(rng.normal(size=len(t)), tone), lp(rng.normal(size=len(t)), tone)], 1) * np.exp(-t * decay)[:, None]
    ir[:int(.01 * SR)] = 0
    ir /= np.sqrt((ir ** 2).sum(0))
    return np.stack([fftconvolve(x[:, c], ir[:, c])[:N] for c in (0, 1)], 1)


def pump(times, depth=.5, release=.09):
    """Sidechain envelope: multiply a stem by this so it ducks on each kick."""
    d = np.ones(N)
    for k in times:
        i = int(k * SR)
        n = min(N - i, int(release * 4.5 * SR))
        if n > 0:
            d[i:i + n] = np.minimum(d[i:i + n], 1 - depth * np.exp(-np.arange(n) / SR / release))
    return d[:, None]


def write_wav(path, x):
    with wave.open(path, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.clip(x, -1, 1) * 32767).astype('<i2').tobytes())


def finish(music, effects, verb_sends=None, fade=1.6):
    """Sum the stems and write mix.wav, music.wav and sfx.wav into the current folder.

    music and effects map names to stems. verb_sends maps a stem name to its reverb level.
    """
    verb_sends = verb_sends or {}
    m = sum(music.values()) + sum(verb(music[k]) * v for k, v in verb_sends.items() if k in music)
    m = hp(m, 32)
    fx = sum(effects.values()) + sum(verb(effects[k]) * v for k, v in verb_sends.items() if k in effects)
    peak = float(np.abs(m).max()) or 1.0
    m = m / peak * .62
    mix = np.tanh((m + fx * .85) * 1.15) / 1.15
    env = np.ones(N)
    n = int(fade * SR)
    env[-n:] = np.cos(np.linspace(0, np.pi / 2, n)) ** 1.5
    env = env[:, None]
    write_wav('mix.wav', mix * env)
    write_wav('music.wav', m * env)
    write_wav('sfx.wav', np.tanh(fx))
    print('mix peak', round(float(np.abs(mix).max()), 3))
