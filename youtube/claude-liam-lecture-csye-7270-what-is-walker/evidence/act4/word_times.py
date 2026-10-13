#!/usr/bin/env python3
"""word_times.py B15 B17 — faster-whisper word times for the beats' mp3s -> evidence/act4/word_times.json"""
import sys, json
from pathlib import Path
from faster_whisper import WhisperModel
REEL = Path(__file__).resolve().parents[2]
m = WhisperModel("base.en", device="cpu", compute_type="int8"); out = {}
for b in sys.argv[1:]:
    segs, _ = m.transcribe(str(REEL / "mp3" / f"beat-{b}.mp3"), word_timestamps=True)
    out[b] = [(w.word.strip(), round(w.start, 2), round(w.end, 2)) for s in segs for w in s.words]
(REEL / "evidence/act4/word_times.json").write_text(json.dumps(out, indent=0))
for b, ws in out.items():
    print(b, " ".join(f"{w}@{s}" for w, s, e in ws))
