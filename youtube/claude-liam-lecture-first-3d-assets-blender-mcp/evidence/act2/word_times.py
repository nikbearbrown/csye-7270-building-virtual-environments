"""word_times.py — word-level timestamps of the Act II narration (faster-whisper base.en, CPU), so cues land on the spoken word.
Run from the reel folder: python3 evidence/act2/word_times.py  -> evidence/act2/word_times.json (+ a readable .txt)."""
import json
from faster_whisper import WhisperModel
m = WhisperModel("base.en", device="cpu", compute_type="int8")
out, txt = {}, []
for bid in ["B15", "B16", "B17", "B18", "B19", "B20"]:
    segs, _ = m.transcribe(f"mp3/beat-{bid}.mp3", language="en", beam_size=5, word_timestamps=True)
    words = [(w.word.strip(), round(w.start, 2), round(w.end, 2)) for s in segs for w in s.words]
    out[bid] = words
    txt.append(bid + ": " + " ".join(f"{w}@{a:.2f}" for w, a, b in words))
json.dump(out, open("evidence/act2/word_times.json", "w"), indent=1)
open("evidence/act2/word_times.txt", "w").write("\n".join(txt) + "\n")
print("\n".join(txt))
