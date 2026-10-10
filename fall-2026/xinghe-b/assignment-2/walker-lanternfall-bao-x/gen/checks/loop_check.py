#!/usr/bin/env python3
"""Check 5: music loops have no click and no silent gap at the wrap point; layers share length.

    python gen/checks/loop_check.py godot/assets/music/mus_01_night_market.ogg [godot/assets/music/mus_02_sunflare_layer.ogg]
"""
import json, sys
from pathlib import Path
import numpy as np
import soundfile as sf

ROOT = Path(__file__).resolve().parents[2]


def analyse(path: str) -> dict:
    y, sr = sf.read(path, always_2d=True)
    m = y.mean(axis=1)
    d = np.abs(np.diff(m))
    p99 = float(np.percentile(d, 99))
    jump = float(abs(m[0] - m[-1]))
    win = int(0.05 * sr)
    rms = lambda s: float(np.sqrt(np.mean(s ** 2)) + 1e-12)
    overall, head, tail = rms(m), rms(m[:win]), rms(m[-win:])
    ok = jump <= p99 and head >= 0.25 * overall and tail >= 0.25 * overall
    return {"file": path, "frames": int(len(m)), "sr": int(sr), "seconds": round(len(m) / sr, 3), "wrap_jump": round(jump, 5),
            "p99_step": round(p99, 5), "head_rms_ratio": round(head / overall, 3), "tail_rms_ratio": round(tail / overall, 3),
            "status": "PASS" if ok else "FAIL"}


results = [analyse(p) for p in sys.argv[1:]]
if len(results) == 2:
    same = results[0]["frames"] == results[1]["frames"]
    results.append({"check": "layer-length-match", "status": "PASS" if same else "FAIL",
                    "frames": [results[0]["frames"], results[1]["frames"]]})
(ROOT / "evidence").mkdir(exist_ok=True)
(ROOT / "evidence" / "loop-check.json").write_text(json.dumps(results, indent=2) + "\n")
for r in results:
    print(r)
sys.exit(0 if all(r["status"] == "PASS" for r in results) else 1)
