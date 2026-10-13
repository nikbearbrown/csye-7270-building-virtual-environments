#!/usr/bin/env python3
"""word_times.py — Act III pacing evidence: faster-whisper word timestamps for B16..B22 (read-only on mp3/), beside the kit's
character-share estimate (what until() uses), so each until(..., lead=...) lands on the real word.  -> evidence/act3/word_times.json
  python3 evidence/act3/word_times.py"""
import json, re, pathlib
from faster_whisper import WhisperModel
REEL = pathlib.Path(__file__).resolve().parents[2]
sheet = json.loads((REEL / "beat_sheet.json").read_text())
B = {b["beat_id"]: b for b in sheet["beats"]}
IDS = ["B16", "B17", "B18", "B19", "B20", "B21", "B22"]
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
    print("  share:   " + "  ".join(f"{e[1]:.2f} {e[0]}" for e in est))
(REEL / "evidence/act3/word_times.json").write_text(json.dumps(out, indent=1))
