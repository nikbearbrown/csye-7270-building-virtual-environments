#!/usr/bin/env python3
"""pad_bout.py: gives BOUT its 1.0 s silent tail (lecture skill: outro_voice, tail_silence_s 1.0). Idempotent: skips if the sheet already says tail applied.
Pads mp3/beat-BOUT.mp3 with apad, writes the padded duration to beat_sheet.json (actual_duration_s). Run AFTER generate_audio_kokoro.py and BEFORE art run."""
import json, subprocess
from pathlib import Path
R = Path(__file__).resolve().parent
sp = R / "beat_sheet.json"; d = json.loads(sp.read_text())
b = next(x for x in d["beats"] if x["beat_id"] == "BOUT")
if b.get("tail_applied"): print("BOUT tail already applied"); raise SystemExit
mp3 = R / "mp3/beat-BOUT.mp3"; raw = R / "mp3/beat-BOUT.raw.mp3"
raw.write_bytes(mp3.read_bytes())
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(raw), "-af", "apad=pad_dur=1.0", "-c:a", "libmp3lame", "-q:a", "2", str(mp3)], check=True)
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(mp3)], capture_output=True, text=True).stdout)
b["actual_duration_s"] = round(dur, 2); b["tail_applied"] = True
sp.write_text(json.dumps(d, indent=2, ensure_ascii=False))
print("BOUT padded to", b["actual_duration_s"])
