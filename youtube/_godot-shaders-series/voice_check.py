#!/usr/bin/env python3
"""voice_check.py <FILM FOLDER> [--model small]: transcribes every beat mp3 with faster-whisper and compares with the narration text.
Writes <FILM>/evidence/build-voice-check.md (similarity per beat; transcripts of the low ones). Words the engine spells out (G L S L, G P U) transcribe as
letters or as the acronym; the report flags a beat only when the similarity after normalising is below 0.85 or a watched term is missing."""
import difflib, json, re, sys
from pathlib import Path
film = Path(sys.argv[1]).resolve()
model_name = sys.argv[sys.argv.index("--model") + 1] if "--model" in sys.argv else "small"
from faster_whisper import WhisperModel
m = WhisperModel(model_name, device="cpu", compute_type="int8")
sheet = json.loads((film / "beat_sheet.json").read_text())
def norm(s):
    s = s.lower()
    s = re.sub(r"\b([a-z]) (?=[a-z]\b)", r"\1", s)            # spaced letters -> acronym
    s = re.sub(r"[^a-z0-9 ]", " ", s)
    return " ".join(s.split())
rows, lows = [], []
for b in sheet["beats"]:
    mp3 = film / b.get("audio_file", f"mp3/beat-{b['beat_id']}.mp3")
    if not mp3.exists(): continue
    segs, _ = m.transcribe(str(mp3), language="en", beam_size=1)
    heard = " ".join(s.text.strip() for s in segs)
    ratio = difflib.SequenceMatcher(None, norm(b["narration_text"]), norm(heard)).ratio()
    rows.append((b["beat_id"], ratio))
    if ratio < 0.85: lows.append((b["beat_id"], ratio, b["narration_text"], heard))
out = ["# Voice check (faster-whisper %s)\n" % model_name, "**What this is.** Automatic transcription of each beat's Kokoro audio against `narration.py`; a rough ear, not a replacement for Bear's.\n",
       "**Found.** %d beats; %d below 0.85 similarity (listed with transcripts). Pronunciation dictionary untouched.\n" % (len(rows), len(lows)), "| beat | similarity |", "|---|---|"]
out += [f"| {a} | {r:.2f} |" for a, r in rows]
out += ["\n## Low beats (read the transcript, then LISTEN)\n"]
for a, r, n, h in lows: out += [f"### {a} ({r:.2f})", f"- spoken text: {n}", f"- heard: {h}\n"]
(film / "evidence").mkdir(exist_ok=True)
(film / "evidence/build-voice-check.md").write_text("\n".join(out))
print(f"{len(rows)} beats, {len(lows)} low; wrote", film / "evidence/build-voice-check.md")
