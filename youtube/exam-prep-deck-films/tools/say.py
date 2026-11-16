#!/usr/bin/env python3
"""say.py - show how the film's voice (Kokoro) will read a word or phrase, as phonemes. Free, local, instant.

    python3 say.py "IK" "I K" "glTF" "A star"

Use it on acronyms, engine class names and unusual words before trusting them in a narration.
If the phonemes are wrong, find a plain respelling that comes out right and put it in narration.json
under say_as: [{"term": "IK", "say": "I K"}]. The narration keeps the normal spelling; only the voice changes.
"""
import sys
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")
sys.path.insert(0, str(Path(__file__).resolve().parent))
from films import TOOLKIT  # noqa: E402

sys.path.insert(0, str(TOOLKIT / "runtime" / "scripts"))
import generate_audio_kokoro as gk  # noqa: E402

for w in sys.argv[1:]:
    print(f"{w:28s} {gk.phonemize(w).strip()}")
