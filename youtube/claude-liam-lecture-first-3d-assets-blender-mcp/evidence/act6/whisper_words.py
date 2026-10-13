"""whisper_words.py - word-level timestamps of act VI's narration (faster-whisper, local, free), to cue the pictures on the real audio
and to whisper-check pronunciation. Usage: python3 evidence/act6/whisper_words.py > evidence/act6/whisper_words.log"""
import sys
from faster_whisper import WhisperModel
m = WhisperModel("small.en", device="cpu", compute_type="int8")
for bid in ["B50", "B51", "B52", "B53", "B54", "B55", "B56", "B57", "B58", "B59", "B60"]:
    segs, info = m.transcribe(f"mp3/beat-{bid}.mp3", word_timestamps=True, beam_size=5)
    words = [w for s in segs for w in s.words]
    print(f"== {bid}")
    print("  " + " ".join(f"{w.word.strip()}@{w.start:.2f}" for w in words))
    sys.stdout.flush()
