#!/usr/bin/env python3
"""word_times.py — Act IV pacing evidence: faster-whisper word timestamps for B19..B24 (read-only on mp3/).
Prints each word's real spoken start time, so the scenes' a4_at(...) cues land on the real word.  Output: evidence/act4/word_times.json
  python3 evidence/act4/word_times.py
"""
import json, pathlib
from faster_whisper import WhisperModel
REEL = pathlib.Path(__file__).resolve().parents[2]
sheet = json.loads((REEL / "beat_sheet.json").read_text())
B = {b["beat_id"]: b for b in sheet["beats"]}
model = WhisperModel("base", device="cpu", compute_type="int8")
out = {}
for bid in ["B19", "B20", "B21", "B22", "B23", "B24"]:
    b = B[bid]; T = float(b["actual_duration_s"])
    segs, _ = model.transcribe(str(REEL / b["audio_file"]), word_timestamps=True, language="en")
    words = [(w.word.strip(), round(w.start, 2), round(w.end, 2)) for s in segs for w in s.words]
    out[bid] = {"duration": T, "whisper": words}
    print(f"== {bid} {T}s")
    print("  " + "  ".join(f"{w[1]:.2f} {w[0]}" for w in words))
(REEL / "evidence/act4/word_times.json").write_text(json.dumps(out, indent=1))
