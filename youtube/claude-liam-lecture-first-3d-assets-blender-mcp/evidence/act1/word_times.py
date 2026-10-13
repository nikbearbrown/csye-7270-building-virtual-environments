#!/usr/bin/env python3
"""word_times.py — Act I pacing evidence: faster-whisper word timestamps for the Act I beats (read-only on mp3/).
Prints, per word, the real spoken start time beside the kit's character-share estimate (what until() uses), so each
until(..., lead=...) can be set to land the motion on the real word.  Output: evidence/act1/word_times.json
  python3 evidence/act1/word_times.py
"""
import json, re, pathlib
from faster_whisper import WhisperModel
REEL = pathlib.Path(__file__).resolve().parents[2]
sheet = json.loads((REEL / "beat_sheet.json").read_text())
B = {b["beat_id"]: b for b in sheet["beats"]}
IDS = ["B01", "B02", "B03", "B04", "B05", "B06", "B07", "B08", "B09A", "B09B", "B10", "B11", "B12", "B13", "B14"]
model = WhisperModel("base", device="cpu", compute_type="int8")
out = {}
for bid in IDS:
    b = B[bid]; n = b["narration_text"]; T = float(b["actual_duration_s"])
    segs, _ = model.transcribe(str(REEL / b["audio_file"]), word_timestamps=True, language="en")
    words = [(w.word.strip(), round(w.start, 2), round(w.end, 2)) for s in segs for w in s.words]
    est = [(m.group(), round(T * m.start() / len(n), 2)) for m in re.finditer(r"\S+", n)]
    out[bid] = {"duration": T, "whisper": words, "char_share": est}
    print(f"== {bid} {T}s")
    print("  whisper: " + "  ".join(f"{w[1]:.2f} {w[0]}" for w in words))
(REEL / "evidence/act1/word_times.json").write_text(json.dumps(out, indent=1))
