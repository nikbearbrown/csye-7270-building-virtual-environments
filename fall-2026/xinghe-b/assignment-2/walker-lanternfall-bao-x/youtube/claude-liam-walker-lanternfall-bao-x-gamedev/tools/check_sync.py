#!/usr/bin/env python3
"""Check that the final film's game-sound beats carry the take's audio with no offset.

For each game-sound-only beat: cut its span out of the final master, cut the same frames out of the take, and
cross-correlate the two audio tracks. The film's audio was levelled by a constant gain, so the correlation peak
should sit at 0 ms. A zero offset means every frame-based SFX label is exactly where the sound is.

    gen/.venv-audio/bin/python youtube/<reel>/tools/check_sync.py exports/landscape/<slug>.mp4
"""
import json, subprocess, sys, tempfile
from pathlib import Path
import numpy as np
import soundfile as sf

REEL = Path(__file__).resolve().parents[1]
SR = 48000


def pcm(src, start, dur, out):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{start:.4f}", "-t", f"{dur:.4f}", "-i", str(src), "-vn",
                    "-ac", "1", "-ar", str(SR), "-c:a", "pcm_s16le", str(out)], check=True)
    a, _ = sf.read(out, dtype="float32")
    return a


def main():
    film = REEL / sys.argv[1]
    sheet = json.loads((REEL / "beat_sheet.json").read_text())
    t, rows = 0.0, []
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        for b in sheet["beats"]:
            d = float(b.get("render_duration_s") or b.get("actual_duration_s"))
            if b.get("kind") == "source_report":
                spec = json.loads((REEL / "media" / "_work" / f"{b['beat_id']}.json").read_text())
                vid = next(L for L in spec["layers"] if L["kind"] == "video" and L["src"].startswith("capture/"))
                a = pcm(film, t, d, tmp / "a.wav")
                ref = pcm(REEL / vid["src"], vid["ss"], d, tmp / "b.wav")
                n = min(len(a), len(ref))
                a, ref = a[:n], ref[:n]
                win = int(0.2 * SR)        # search ±200 ms
                spec_a, spec_r = np.fft.rfft(a, 2 * n), np.fft.rfft(ref, 2 * n)
                xc = np.fft.irfft(spec_a * np.conj(spec_r))
                lags = np.concatenate([xc[-win:], xc[:win + 1]])
                lag = int(np.argmax(lags)) - win
                corr = float(np.max(lags) / (np.linalg.norm(a) * np.linalg.norm(ref) + 1e-9))
                rows.append((b["beat_id"], round(t, 3), round(lag / SR * 1000, 2), round(corr, 3)))
            t += d
    for r in rows:
        print(f"{r[0]}: starts {r[1]} s · audio offset {r[2]} ms · correlation {r[3]}")
    bad = [r for r in rows if abs(r[2]) > 1.0 or r[3] < 0.9]
    print("SYNC OK" if not bad else f"SYNC PROBLEM: {bad}")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
