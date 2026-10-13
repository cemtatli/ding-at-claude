# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy"]
# ///
"""Synthesize notification sounds (no samples needed) into ~/.claude/sounds/, outside the repo."""

import os
import subprocess
import wave

import numpy as np

SR = 48000
OUT_DIR = os.environ.get("CLAUDE_SOUND_DIR", os.path.expanduser("~/.claude/sounds"))


def t(dur):
    return np.arange(int(SR * dur)) / SR


def env(n, attack=0.004, decay=0.5):
    x = np.arange(n) / SR
    a = np.clip(x / attack, 0, 1)
    return a * np.exp(-x / decay)


def tone(freq, dur, partials=((1, 1.0),), decay=0.5, attack=0.004):
    x = t(dur)
    y = sum(amp * np.sin(2 * np.pi * freq * ratio * x) * np.exp(-x / (decay / ratio**0.5))
            for ratio, amp in partials)
    return y * env(len(x), attack, 1e9)


def place(parts, total):
    """parts: list of (start_sec, signal)."""
    out = np.zeros(int(SR * total))
    for start, sig in parts:
        i = int(SR * start)
        n = min(len(sig), len(out) - i)
        out[i:i + n] += sig[:n]
    return out


# Timbres
BELL = ((1, 1.0), (2.0, 0.5), (2.76, 0.35), (5.4, 0.2), (8.93, 0.1))  # inharmonic church/hand bell
MARIMBA = ((1, 1.0), (4.0, 0.25), (9.2, 0.05))
GLASS = ((1, 1.0), (2.32, 0.4), (4.25, 0.2), (6.63, 0.1))
KALIMBA = ((1, 1.0), (5.4, 0.3), (12.0, 0.08))
SINE = ((1, 1.0),)


def note(n):
    """MIDI note number -> Hz."""
    return 440.0 * 2 ** ((n - 69) / 12)


def bell_done():
    return place([(0, tone(note(76), 2.2, BELL, decay=0.9))], 2.2)


def marimba_resolve():
    # G5 -> C6: kapanış hissi veren tam kadans
    return place([(0, tone(note(79), 0.8, MARIMBA, 0.25)),
                  (0.12, tone(note(84), 1.0, MARIMBA, 0.35))], 1.1)


def glass_chord():
    return place([(0.00, tone(note(72), 1.6, GLASS, 0.6)),
                  (0.06, tone(note(76), 1.6, GLASS, 0.6)),
                  (0.12, tone(note(79), 1.6, GLASS, 0.6)),
                  (0.18, tone(note(84), 1.6, GLASS, 0.7))], 1.8)


def kalimba_done():
    return place([(0, tone(note(74), 0.9, KALIMBA, 0.3)),
                  (0.1, tone(note(78), 0.9, KALIMBA, 0.3)),
                  (0.2, tone(note(81), 1.2, KALIMBA, 0.45))], 1.4)


def soft_success():
    return place([(0, tone(note(81), 0.5, SINE, 0.15)),
                  (0.11, tone(note(88), 0.8, SINE, 0.3))], 0.9)


def bell_question():
    # Yükselen iki nota: soru tonlaması gibi
    return place([(0, tone(note(72), 1.0, BELL, 0.5)),
                  (0.16, tone(note(79), 1.4, BELL, 0.7))], 1.6)


def marimba_question():
    return place([(0, tone(note(72), 0.6, MARIMBA, 0.2)),
                  (0.1, tone(note(76), 0.6, MARIMBA, 0.2)),
                  (0.2, tone(note(81), 0.9, MARIMBA, 0.3))], 1.1)


def pop_question():
    x = t(0.35)
    # Hızlı yukarı pitch sweep -> "pop?" efekti
    freq = 600 + 900 * (x / x[-1]) ** 0.5
    phase = 2 * np.pi * np.cumsum(freq) / SR
    y = np.sin(phase) * env(len(x), 0.002, 0.08)
    return place([(0, y), (0.14, tone(note(86), 0.5, SINE, 0.12))], 0.6)


def glass_ping():
    return place([(0, tone(note(84), 1.4, GLASS, 0.5))], 1.4)


def kalimba_question():
    return place([(0, tone(note(78), 0.7, KALIMBA, 0.25)),
                  (0.13, tone(note(83), 1.0, KALIMBA, 0.4))], 1.2)


SOUNDS = {
    "done_bell": bell_done,
    "done_marimba": marimba_resolve,
    "done_glass_chord": glass_chord,
    "done_kalimba": kalimba_done,
    "done_soft": soft_success,
    "question_bell": bell_question,
    "question_marimba": marimba_question,
    "question_pop": pop_question,
    "question_glass": glass_ping,
    "question_kalimba": kalimba_question,
}


def write(name, y):
    y = y / np.max(np.abs(y)) * 0.89
    fade = int(SR * 0.02)
    y[-fade:] *= np.linspace(1, 0, fade)
    wav = os.path.join(OUT_DIR, f"{name}.wav")
    with wave.open(wav, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((y * 32767).astype(np.int16).tobytes())
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", wav, "-c:a", "libopus", "-b:a", "64k",
                    os.path.join(OUT_DIR, f"{name}.opus")], check=True)
    os.remove(wav)


if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)
    for name, fn in SOUNDS.items():
        write(name, fn())
        print(os.path.join(OUT_DIR, f"{name}.opus"))
