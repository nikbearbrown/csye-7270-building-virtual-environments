#!/usr/bin/env python3
"""word_times.py — Act IV pacing evidence: faster-whisper word timestamps for B23..B29 (read-only on mp3/).
Prints each word's real spoken start time; evidence/act4/word_times.json is read by hand to set a4_at(t) cues.
  python3 evidence/act4/word_times.py
"""
import json, pathlib
from faster_whisper import WhisperModel
REEL = pathlib.Path(__file__).resolve().parents[2]
sheet = json.loads((REEL / "beat_sheet.json").read_text())
B = {b["beat_id"]: b for b in sheet["beats"]}
model = WhisperModel("base", device="cpu", compute_type="int8")
out = {}
for bid in ["B23", "B24", "B25", "B26", "B27", "B28", "B29"]:
    b = B[bid]
    segs, _ = model.transcribe(str(REEL / b["audio_file"]), word_timestamps=True, language="en")
    words = [(w.word.strip(), round(w.start, 2), round(w.end, 2)) for s in segs for w in s.words]
    out[bid] = {"duration": float(b["actual_duration_s"]), "whisper": words}
    print(f"== {bid} {b['actual_duration_s']}s")
    print("  " + "  ".join(f"{w[1]:.2f} {w[0]}" for w in words))
(REEL / "evidence/act4/word_times.json").write_text(json.dumps(out, indent=1))
