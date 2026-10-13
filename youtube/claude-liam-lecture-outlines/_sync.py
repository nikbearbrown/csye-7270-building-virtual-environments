"""_sync.py: planning helper (tooling, never viewer-facing). Estimates WHEN a phrase of a beat's narration is spoken, from word counts at the
series pace (0.34 s per word, series_config.SEC_PER_WORD), so capture timelines, code-highlight cues and readouts are planned to land near the words
they illustrate. Kokoro's real pacing differs by perhaps 10 to 15 percent: the build stretches every capture to the measured audio (see CAPTURE-PLAN.md,
"Timing"), so what matters is the *fraction* of the beat at which a thing happens, and that is what the lanes carry.

    when("B13", "Thickness one, two, three, four", k=3)   ->  seconds into B13 at which the 4th word of that phrase begins
    frac("B13", seconds)                                    ->  that moment as a fraction of the beat (nudged out of the 45 to 55 percent window)
"""
import importlib.util
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("narration_outlines", HERE / "narration.py")
N = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(N)

SPW = 0.34
TEXT = {bid: text for bid, _, text in N.BODY}
ACT_OF = {bid: ai for bid, ai, _ in N.BODY}
EST = {bid: round(len(t.split()) * SPW, 2) for bid, t in TEXT.items()}


def _norm(w):
    return re.sub(r"[^\w']", "", w).lower()


def when(bid, phrase, k=0, lead=0.0):
    words = [_norm(w) for w in TEXT[bid].split()]
    ph = [_norm(w) for w in phrase.split()]
    for i in range(len(words) - len(ph) + 1):
        if words[i:i + len(ph)] == ph:
            return round((i + k) * SPW + lead, 2)
    raise KeyError(f"{bid}: phrase not found in the narration: {phrase!r}")


def frac(bid, sec, nudge=True):
    f = max(0.03, min(0.96, sec / EST[bid]))
    if nudge and 0.45 <= f <= 0.55:          # Gate V: no cue starts inside the 45 to 55 percent window
        f = 0.44 if f < 0.5 else 0.56
    return round(f, 2)
