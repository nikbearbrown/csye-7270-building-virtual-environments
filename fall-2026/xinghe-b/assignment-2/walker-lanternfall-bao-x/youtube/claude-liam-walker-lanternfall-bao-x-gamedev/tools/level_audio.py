#!/usr/bin/env python3
"""Even out the film's loudness without touching what the game sounds like.

Kokoro narration comes out near -24.7 LUFS with spiky peaks; the game-sound-only beats are near -10 to -15 LUFS.
Played back to back, the game would jump 10-14 dB louder than the voice. So:
  * narration (voice-over, not evidence): EBU R128 loudness normalisation to -16 LUFS, true peak -1.5 dBTP,
    written as mp3/beat-<BID>.wav next to the Kokoro mp3, and the beat's audio_file points at it;
  * game-sound-only beats: one constant gain for all of them (no compression, no EQ, relative levels kept),
    applied to media/<BID>.mp4's audio with the video stream copied;
  * the outro jingle is left as it is.
Writes media/_work/levels.json (before/after measurements; copied to audio-levels.json) for SOURCES.md.

    python3 tools/level_audio.py
"""
import json, re, shutil, subprocess
from pathlib import Path

REEL = Path(__file__).resolve().parents[1]
GAME_GAIN_DB = -5.5
TARGET = "loudnorm=I=-16:TP=-1.5:LRA=11"


def lufs(path):
    r = subprocess.run(["ffmpeg", "-nostats", "-i", str(path), "-vn", "-af", "ebur128=peak=true:framelog=quiet", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    i = re.findall(r"I:\s+(-?[\d.]+) LUFS", r)
    p = re.findall(r"Peak:\s+(-?[\d.]+) dBFS", r)
    return (float(i[-1]) if i else None, float(p[-1]) if p else None)


def dur(path):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
                                capture_output=True, text=True).stdout.strip())


def main():
    sheet_p = REEL / "beat_sheet.json"
    sheet = json.loads(sheet_p.read_text())
    log = {"narration": {}, "game_sound": {}, "game_gain_db": GAME_GAIN_DB, "narration_filter": TARGET}
    for b in sheet["beats"]:
        bid = b["beat_id"]
        if b.get("kind") == "source_report":
            src = REEL / "media" / f"{bid}.mp4"
            orig = REEL / "media" / "_work" / f"{bid}-unlevelled.mp4"
            if not orig.exists():
                shutil.copy2(src, orig)
            before = lufs(orig)
            tmp = src.with_suffix(".tmp.mp4")
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(orig), "-map", "0:v", "-map", "0:a", "-c:v", "copy",
                            "-af", f"volume={GAME_GAIN_DB}dB", "-c:a", "aac", "-b:a", "256k", "-ar", "48000",
                            "-movflags", "+faststart", str(tmp)], check=True)
            tmp.replace(src)
            log["game_sound"][bid] = {"before": before, "after": lufs(src)}
            continue
        af = b.get("audio_file") or ""
        if not af.startswith("mp3/beat-") or bid == "B33":
            continue
        mp3 = REEL / af.replace(".wav", ".mp3")
        wav = REEL / f"mp3/beat-{bid}.wav"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(mp3), "-af", TARGET, "-ar", "48000", "-ac", "2",
                        "-c:a", "pcm_s16le", str(wav)], check=True)
        d0, d1 = dur(mp3), dur(wav)
        if abs(d0 - d1) > 0.05:
            raise SystemExit(f"{bid}: levelled narration changed length {d0:.3f} -> {d1:.3f}")
        b["audio_file"] = f"mp3/beat-{bid}.wav"
        b["audio_levelled"] = {"from": f"mp3/beat-{bid}.mp3", "filter": TARGET}
        log["narration"][bid] = {"before": lufs(mp3), "after": lufs(wav)}
    sheet_p.write_text(json.dumps(sheet, indent=1, ensure_ascii=False) + "\n")
    (REEL / "media" / "_work" / "levels.json").write_text(json.dumps(log, indent=1))
    for k in ("narration", "game_sound"):
        vals = [v["after"][0] for v in log[k].values() if v["after"][0] is not None]
        print(k, len(vals), "beats, integrated after:", min(vals), "to", max(vals), "LUFS")


if __name__ == "__main__":
    main()
