#!/usr/bin/env python3
"""Re-run logged generations from their sidecars and compare each result with the logged output.

    gen/.venv-audio/bin/python gen/reproduce.py ART-PC-01-20260929T210117Z-s11-walk_contact MUS-01-20260930T013739Z-s5

For each run id: the prompt, seed and settings are read from gen/log/<ID>/<run>.json and written into a one-run spec,
which goes through the same generator that made the original (art_generate.py, sfx_generate.py or
music_generate.py) inside a temporary copy of gen/, so the repository and its log are not touched. The new file is
compared with the logged output: the full-size raw if it is on disk (gen/raw/, not committed), else the accepted copy
(gen/accepted/, committed), else the committed thumbnail. Needs the local venvs and model downloads (SOURCES.md).
"""
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def spec_for(meta):
    s = meta["settings"]
    base = {"asset_id": meta["asset_id"], "storyboard_panels": meta["storyboard_panels"],
            "prompt": meta["prompt"], "negative_prompt": meta.get("negative_prompt", "")}
    model = meta["model"]
    if "FLUX" in model:
        return "art", base | {k: s[k] for k in ("width", "height", "steps", "quantize")}
    if "stable-audio" in model:
        return "sfx", base | {"steps": s["steps"], "cfg": s["cfg"], "duration_s": s["duration_s"]}
    if "musicgen" in model:
        return "music", base | {"model": model, "duration_s": s["duration_s"], "guidance_scale": s["guidance_scale"],
                                "condition_on": s.get("condition_on")}
    raise SystemExit(f"unknown model {model}")


def reference(meta):
    copies = meta.get("accepted_copies") or []
    for p in [*meta.get("raw_outputs", []), *(copies if isinstance(copies, list) else [copies])]:
        if (ROOT / p).exists():
            return ROOT / p, "file"
    return ROOT / meta["thumbnail"], "thumbnail"


def compare(new, ref):
    if new.suffix == ".png":
        import numpy as np
        from PIL import Image
        a, b = (np.asarray(Image.open(p).convert("RGB")).astype(int) for p in (new, ref))
        if a.shape != b.shape:
            return False, f"size {a.shape[1]}x{a.shape[0]} vs {b.shape[1]}x{b.shape[0]}"
        diff = np.abs(a - b).max(axis=2)
        n = int((diff > 0).sum())
        return n == 0, f"{n} of {diff.size} pixels differ (largest channel difference {int(diff.max())})"
    import numpy as np
    import soundfile as sf
    a, sa = sf.read(new, always_2d=True)
    b, sb = sf.read(ref, always_2d=True)
    if a.shape != b.shape or sa != sb:
        return False, f"shape {a.shape} @ {sa} Hz vs {b.shape} @ {sb} Hz"
    d = float(np.abs(a - b).max())
    corr = float(np.corrcoef(a.ravel(), b.ravel())[0, 1])
    return d == 0, f"{a.shape[0]} samples, largest sample difference {d:.3g}, correlation {corr:.6f}"


def main():
    ok_all = True
    for run_id in sys.argv[1:]:
        found = list((ROOT / "gen" / "log").glob(f"*/{run_id}.json"))
        if not found:
            raise SystemExit(f"no sidecar for {run_id}")
        meta = json.loads(found[0].read_text())
        kind, spec = spec_for(meta)
        tmp = Path(tempfile.mkdtemp(prefix="reproduce-"))
        (tmp / "gen").mkdir()
        for py in (ROOT / "gen").glob("*.py"):
            shutil.copy(py, tmp / "gen" / py.name)
        # Runs before 2026-09-30 00:32 UTC quantized FLUX to 4-bit at load; the full weights were then replaced by the
        # saved 4-bit copy in gen/cache/, which every later run used and this re-run uses too.
        if kind == "art" and (ROOT / "gen" / "cache").exists():
            (tmp / "gen" / "cache").symlink_to(ROOT / "gen" / "cache")
        if spec.get("condition_on"):
            (tmp / spec["condition_on"]).parent.mkdir(parents=True, exist_ok=True)
            (tmp / spec["condition_on"]).symlink_to(ROOT / spec["condition_on"])
        (tmp / "spec.json").write_text(json.dumps(spec, indent=2))
        venv = "art" if kind == "art" else "audio"
        script = {"art": "art_generate.py", "sfx": "sfx_generate.py", "music": "music_generate.py"}[kind]
        subprocess.run([str(ROOT / "gen" / f".venv-{venv}" / "bin" / "python"), str(tmp / "gen" / script),
                        str(tmp / "spec.json"), "--seeds", str(meta["settings"]["seed"])], cwd=tmp, check=True)
        new_raw = next((tmp / "gen" / "raw" / meta["asset_id"]).iterdir())
        ref, what = reference(meta)
        new = new_raw if what == "file" else next((tmp / "gen" / "thumbs" / meta["asset_id"]).iterdir())
        same, detail = compare(new, ref)
        ok_all &= same
        print(f"{run_id}: {'IDENTICAL' if same else 'DIFFERENT'} to {ref.relative_to(ROOT)} — {detail} (new file: {new_raw})",
              flush=True)
    return 0 if ok_all else 1


if __name__ == "__main__":
    raise SystemExit(main())
