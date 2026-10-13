"""Word times of the REAL narration audio of beats B08-B13 (faster-whisper tiny.en/base.en) -> word_times.json. Re-run: python3 word_times.py"""
import json, os
from faster_whisper import WhisperModel
here = os.path.dirname(os.path.abspath(__file__)); mp3 = os.path.join(here, "..", "..", "mp3")
m = WhisperModel("base.en", device="cpu", compute_type="int8")
out = {}
for b in ["B08", "B09", "B10", "B11", "B12", "B13"]:
    segs, _ = m.transcribe(os.path.join(mp3, f"beat-{b}.mp3"), word_timestamps=True)
    out[b] = [(w.word.strip(), round(w.start, 2), round(w.end, 2)) for s in segs for w in s.words]
json.dump(out, open(os.path.join(here, "word_times.json"), "w"), indent=1)
for b, ws in out.items(): print(b, " ".join(f"{w}@{s}" for w, s, e in ws))
