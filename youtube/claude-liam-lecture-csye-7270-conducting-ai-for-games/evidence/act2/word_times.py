#!/usr/bin/env python3
"""word_times.py — Act II pacing evidence: faster-whisper word timestamps for B06..B15 (read-only on mp3/).
Writes evidence/act2/word_times.json and prints, per beat, "t word" so each pacing cue lands on the real spoken word.
  python3 evidence/act2/word_times.py
"""
import json, pathlib
from faster_whisper import WhisperModel
REEL = pathlib.Path(__file__).resolve().parents[2]
sheet = json.loads((REEL / "beat_sheet.json").read_text())
B = {b["beat_id"]: b for b in sheet["beats"]}
IDS = [f"B{n:02d}" for n in range(6, 16)]
model = WhisperModel("base", device="cpu", compute_type="int8")
out = {}
for bid in IDS:
    b = B[bid]; T = float(b["actual_duration_s"])
    segs, _ = model.transcribe(str(REEL / b["audio_file"]), word_timestamps=True, language="en")
    words = [(w.word.strip(), round(w.start, 2), round(w.end, 2)) for s in segs for w in s.words]
    out[bid] = {"duration": T, "whisper": words}
    print(f"== {bid} {T}s")
    print("  " + "  ".join(f"{w[1]:.2f} {w[0]}" for w in words))
(REEL / "evidence/act2/word_times.json").write_text(json.dumps(out, indent=1))
