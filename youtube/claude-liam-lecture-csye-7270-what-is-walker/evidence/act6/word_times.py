#!/usr/bin/env python3
"""word_times.py — Act VI pacing evidence: faster-whisper word timestamps for B24..B26 (read-only on mp3/).
  python3 evidence/act6/word_times.py      -> evidence/act6/word_times.json (and a printout)"""
import json, pathlib
from faster_whisper import WhisperModel
REEL = pathlib.Path(__file__).resolve().parents[2]
sheet = json.loads((REEL / "beat_sheet.json").read_text())
B = {b["beat_id"]: b for b in sheet["beats"]}
model = WhisperModel("base", device="cpu", compute_type="int8")
out = {}
for bid in ["B24", "B25", "B26"]:
    b = B[bid]
    segs, _ = model.transcribe(str(REEL / b["audio_file"]), word_timestamps=True, language="en")
    words = [(w.word.strip(), round(w.start, 2), round(w.end, 2)) for s in segs for w in s.words]
    out[bid] = {"duration": float(b["actual_duration_s"]), "whisper": words}
    print(f"== {bid} {b['actual_duration_s']}s")
    print("  " + "  ".join(f"{w[1]:.2f} {w[0]}" for w in words))
(REEL / "evidence/act6/word_times.json").write_text(json.dumps(out, indent=1))
