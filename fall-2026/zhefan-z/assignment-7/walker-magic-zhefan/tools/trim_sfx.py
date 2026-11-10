"""Trim, fade, level-match and export the picked Stable Audio Open variants as OGG.

Input:  the author's picks from E:\\7270\\tools\\sfx_raw\\ (raw WAVs, outside the repo)
Output: assets/audio/sfx/SFX-*.ogg, assets/audio/EDIT-LOG.md and edit-log.json

Per sound: trim leading silence (onset = first 2 ms window above -45 dBFS, 5 ms kept before it,
2 ms fade-in so the cut cannot click), cut to the target length, fade out (10 ms, or 250 ms for the
sustained FAIL tone), match levels on the loudest 50 ms window (short-window RMS) to one shared
target chosen so no peak exceeds -1 dBFS, then encode OGG Vorbis q6 with FFmpeg's libvorbis.

Run with the ComfyUI venv (NumPy) and FFmpeg on PATH:
    E:/7270/tools/ComfyUI/.venv/Scripts/python.exe tools/trim_sfx.py
"""

import datetime
import hashlib
import json
import shutil
import subprocess
import wave
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parent.parent
RAW = Path(r"E:\7270\tools\sfx_raw")
OUT = REPO / "assets" / "audio" / "sfx"
LOG_MD = REPO / "assets" / "audio" / "EDIT-LOG.md"
LOG_JSON = REPO / "assets" / "audio" / "edit-log.json"

REASON = ("matches the on-screen action better and reads more clearly; "
          "the other seeds fit the action less well or were less clear")
PICKS = {
    # id: (seed, rejected seeds, target length s, fade-out s)
    "SFX-CAST": (3, [1, 2], 0.4, 0.010),
    "SFX-WOLF-DOWN": (1, [2, 3], 0.6, 0.010),
    "SFX-HURT": (3, [1, 2], 0.3, 0.010),
    "SFX-FAIL": (2, [1, 3], 1.0, 0.250),   # sustained tone: gentle ending, shorter than the 1.2 s reload
    "SFX-CLEAR": (3, [1, 2], 1.2, 0.010),
}
PRE_PICKS = {"SFX-HEAL": (3, "heal is out of the slice; pre-pick for the full game, not exported")}

ONSET_DBFS = -45.0
ONSET_WIN_S = 0.002
PRE_ROLL_S = 0.005
FADE_IN_S = 0.002
LEVEL_WIN_S = 0.050
TARGET_MAX_DBFS = -14.0      # preferred loudest-window RMS, lowered if a peak would exceed the ceiling
PEAK_CEILING_DBFS = -1.0
OGG_QUALITY = 6


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def db(x):
    return 20 * np.log10(max(float(x), 1e-12))


def read_wav(path):
    with wave.open(str(path)) as w:
        rate, ch, width = w.getframerate(), w.getnchannels(), w.getsampwidth()
        a = np.frombuffer(w.readframes(w.getnframes()), dtype={2: np.int16, 4: np.int32}[width])
    full = float(np.iinfo({2: np.int16, 4: np.int32}[width]).max + 1)
    return a.reshape(-1, ch).astype(np.float64) / full, rate


def window_rms(x, n):
    """RMS of the mono mix over consecutive windows of n samples."""
    m = x.mean(axis=1)
    k = len(m) // n
    return np.sqrt((m[: k * n].reshape(k, n) ** 2).mean(axis=1))


def loudest_window_rms(x, rate):
    n = int(LEVEL_WIN_S * rate)
    hop = n // 4
    m = x.mean(axis=1)
    return max(np.sqrt((m[i:i + n] ** 2).mean()) for i in range(0, len(m) - n + 1, hop))


def process(x, rate, length_s, fade_s):
    n = int(ONSET_WIN_S * rate)
    rms = window_rms(x, n)
    above = np.where(20 * np.log10(np.maximum(rms, 1e-12)) > ONSET_DBFS)[0]
    onset = int(above[0]) * n if len(above) else 0
    start = max(0, onset - int(PRE_ROLL_S * rate))
    end = start + int(round(length_s * rate))
    if end > len(x):
        raise ValueError(f"source too short: needs {end} samples, has {len(x)}")
    y = x[start:end].copy()
    fi = int(FADE_IN_S * rate)
    y[:fi] *= np.linspace(0.0, 1.0, fi, endpoint=False)[:, None]
    fo = int(round(fade_s * rate))
    y[-fo:] *= (0.5 * (1 + np.cos(np.linspace(0, np.pi, fo))))[:, None]   # raised-cosine fade to 0
    return y, {"onset_s": round(onset / rate, 4), "cut_start_s": round(start / rate, 4),
               "cut_end_s": round(end / rate, 4), "length_s": round(len(y) / rate, 4)}


def encode_ogg(y, rate, path):
    ffmpeg = shutil.which("ffmpeg")
    cmd = [ffmpeg, "-hide_banner", "-loglevel", "error", "-y", "-f", "f32le", "-ar", str(rate),
           "-ac", str(y.shape[1]), "-i", "-", "-c:a", "libvorbis", "-q:a", str(OGG_QUALITY), str(path)]
    subprocess.run(cmd, input=y.astype("<f4").tobytes(), check=True)


def decoded_duration(path):
    out = subprocess.run([shutil.which("ffprobe"), "-v", "error", "-show_entries", "format=duration",
                          "-of", "default=nw=1:nk=1", str(path)], capture_output=True, text=True, check=True)
    return float(out.stdout.strip())


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    items = {}
    for sid, (seed, rejected, length, fade) in PICKS.items():
        src = RAW / f"{sid}_seed{seed}.wav"
        x, rate = read_wav(src)
        y, info = process(x, rate, length, fade)
        items[sid] = dict(src=src, y=y, rate=rate, info=info, seed=seed, rejected=rejected, fade=fade,
                          rms=loudest_window_rms(y, rate), peak=float(np.abs(y).max()))
    # One shared target: as loud as TARGET_MAX_DBFS allows without any peak above the ceiling.
    headroom = min(PEAK_CEILING_DBFS - db(it["peak"]) + db(it["rms"]) for it in items.values())
    target = min(TARGET_MAX_DBFS, headroom)
    log = []
    for sid, it in items.items():
        gain_db = target - db(it["rms"])
        y = it["y"] * 10 ** (gain_db / 20)
        path = OUT / f"{sid}.ogg"
        encode_ogg(y, it["rate"], path)
        log.append({
            "id": sid, "source": str(it["src"]), "source_sha256": sha256(it["src"]), "picked_seed": it["seed"],
            "rejected_seeds": it["rejected"], "reason": REASON, **it["info"], "fade_in_s": FADE_IN_S,
            "fade_out_s": it["fade"], "loudest_50ms_rms_dbfs_before": round(db(it["rms"]), 2),
            "gain_db": round(gain_db, 2), "loudest_50ms_rms_dbfs_after": round(target, 2),
            "peak_dbfs_after": round(db(np.abs(y).max()), 2), "ogg": str(path.relative_to(REPO)).replace("\\", "/"),
            "ogg_quality": OGG_QUALITY, "ogg_duration_s": round(decoded_duration(path), 4), "ogg_sha256": sha256(path),
        })
    write_log(log, target)
    for e in log:
        print(f"{e['id']:14s} seed {e['picked_seed']}  onset {e['onset_s']:.3f}s  cut {e['cut_start_s']:.3f}-{e['cut_end_s']:.3f}s  "
              f"gain {e['gain_db']:+.2f} dB  peak {e['peak_dbfs_after']:.2f} dBFS  ogg {e['ogg_duration_s']:.3f}s")
    print(f"shared loudest-50ms RMS target: {target:.2f} dBFS")


def write_log(log, target):
    now = datetime.datetime.now().astimezone().isoformat(timespec="seconds")
    LOG_JSON.write_text(json.dumps({"generated": now, "target_rms_dbfs": round(target, 2),
                                    "pre_picks_not_exported": {k: {"seed": v[0], "note": v[1]} for k, v in PRE_PICKS.items()},
                                    "sfx": log}, indent=2), encoding="utf-8")
    L = ["# Audio edit log", "", f"Sound effects generated by `tools/trim_sfx.py` on {now}. Full data: `edit-log.json`.", "",
         "Model output: Stable Audio Open 1.0 via ComfyUI, settings and seeds in `design/audio/sfx-gen-log.md`. "
         "Raw WAVs stay outside the repo in `E:\\7270\\tools\\sfx_raw\\`.", "",
         f"Every sound: leading silence trimmed (onset = first {ONSET_WIN_S * 1000:.0f} ms window above {ONSET_DBFS:.0f} dBFS, "
         f"{PRE_ROLL_S * 1000:.0f} ms kept before it), {FADE_IN_S * 1000:.0f} ms fade-in, cut to length, raised-cosine fade-out, "
         f"levels matched on the loudest {LEVEL_WIN_S * 1000:.0f} ms window to {target:.2f} dBFS RMS (peaks at most "
         f"{PEAK_CEILING_DBFS:.0f} dBFS), OGG Vorbis q{OGG_QUALITY} (FFmpeg libvorbis).", "",
         f"Picks are the author's; reason for every pick: {REASON}.", "",
         "| Sound | Pick | Rejected | Onset s | Cut s | Length s | Fade-out ms | Gain dB | Peak dBFS | OGG s | File |",
         "|---|---|---|---|---|---|---|---|---|---|---|"]
    for e in log:
        L.append(f"| {e['id']} | seed {e['picked_seed']} | seeds {', '.join(map(str, e['rejected_seeds']))} | {e['onset_s']} | "
                 f"{e['cut_start_s']}–{e['cut_end_s']} | {e['length_s']} | {e['fade_out_s'] * 1000:.0f} | {e['gain_db']:+.2f} | "
                 f"{e['peak_dbfs_after']} | {e['ogg_duration_s']} | `{e['ogg']}` |")
    for k, v in PRE_PICKS.items():
        L.append(f"\n{k}: seed {v[0]} pre-picked — {v[1]}.")
    LOG_MD.write_text("\n".join(L) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
