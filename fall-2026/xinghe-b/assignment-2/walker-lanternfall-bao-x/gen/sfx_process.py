#!/usr/bin/env python3
"""Trim, fade, mono, peak-normalise an accepted SFX to 44.1 kHz 16-bit WAV.

    python gen/sfx_process.py gen/accepted/SFX-01/<run>.wav godot/assets/sfx/sfx_01_kill.wav --max-s 0.35
"""
import argparse, json
from pathlib import Path
import librosa
import numpy as np
import soundfile as sf

ap = argparse.ArgumentParser()
ap.add_argument("src")
ap.add_argument("dst")
ap.add_argument("--max-s", type=float, required=True)
ap.add_argument("--top-db", type=float, default=40)
ap.add_argument("--peak-db", type=float, default=-1.0)
ap.add_argument("--sidecar", help="gen/log/<ID>/<run>.json to record this edit in")
a = ap.parse_args()
y, sr = librosa.load(a.src, sr=44100, mono=True)
y, _ = librosa.effects.trim(y, top_db=a.top_db)
y = y[: int(a.max_s * sr)]
fi, fo = int(0.004 * sr), min(int(0.03 * sr), len(y) // 3)
y[:fi] *= np.linspace(0, 1, fi)
y[-fo:] *= np.linspace(1, 0, fo)
y *= 10 ** (a.peak_db / 20) / max(1e-9, np.abs(y).max())
Path(a.dst).parent.mkdir(parents=True, exist_ok=True)
sf.write(a.dst, y, sr, subtype="PCM_16")
result = {"tool": "gen/sfx_process.py", "src": a.src, "dst": a.dst, "trim_top_db": a.top_db, "max_s": a.max_s,
          "fade_in_ms": 4, "fade_out_ms": round(fo / sr * 1000), "peak_db": a.peak_db, "seconds": round(len(y) / sr, 3)}
import sys; sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import log_processing
log_processing(a.sidecar, result)
print(json.dumps(result))
