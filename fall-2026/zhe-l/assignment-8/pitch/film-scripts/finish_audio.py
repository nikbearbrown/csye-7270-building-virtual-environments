"""Pad the outro with 1.0 s of silence (once), measure every beat's audio, and write the durations back.
Run after generate_audio_kokoro.py and before rendering. Idempotent."""
import json
import subprocess
from pathlib import Path

R = Path(__file__).resolve().parents[1]
sheet = json.loads((R / "beat_sheet.json").read_text(encoding="utf-8"))
for b in sheet["beats"]:
    b.setdefault("audio_file", f"mp3/beat-{b['beat_id']}.mp3")
    path = R / b["audio_file"]
    if b["beat_id"] == "BOUT":
        raw = path.with_name(path.stem + "-unpad.mp3")
        if not raw.exists():
            path.rename(raw)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(raw), "-af", "apad=pad_dur=1",
                        "-c:a", "libmp3lame", "-b:a", "192k", str(path)], check=True)
    d = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                       "-of", "default=nw=1:nk=1", str(path)]))
    b["actual_duration_s"] = round(d, 3)
    if b["beat_id"] == "BOUT":
        b["shot"]["remotion"]["props"]["durationSeconds"] = round(d, 3)
(R / "beat_sheet.json").write_text(json.dumps(sheet, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
(R / "mp3/timings.json").write_text(json.dumps({b["beat_id"]: b["actual_duration_s"] for b in sheet["beats"]}, indent=1) + "\n")
print("Measured runtime: %.2f s" % sum(b["actual_duration_s"] for b in sheet["beats"]))
for b in sheet["beats"]:
    print(b["beat_id"], b["actual_duration_s"])
