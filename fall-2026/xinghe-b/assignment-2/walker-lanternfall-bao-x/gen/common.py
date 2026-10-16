"""Shared helpers for the generation pipeline: run ids, JSON sidecars and thumbnails."""
import datetime as dt
import json
import platform
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = f"local — {platform.machine()} macOS {platform.mac_ver()[0]} (Apple M4 Pro, 16 GB)"


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def new_run_id(asset_id: str, seed: int) -> str:
    return f"{asset_id}-{dt.datetime.now(dt.timezone.utc):%Y%m%dT%H%M%SZ}-s{seed}"


def write_sidecar(meta: dict) -> Path:
    meta = {"created_utc": utc_now(), "runtime": RUNTIME, "decision": None, **meta}
    path = ROOT / "gen" / "log" / meta["asset_id"] / f"{meta['run_id']}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(meta, indent=2) + "\n")
    return path


def rel(p: Path) -> str:
    return str(Path(p).resolve().relative_to(ROOT))


def thumbnail_image(src: Path, asset_id: str, run_id: str) -> Path:
    from PIL import Image
    out = ROOT / "gen" / "thumbs" / asset_id / f"{run_id}.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    im = Image.open(src).convert("RGB")
    im.thumbnail((256, 256))
    im.save(out, optimize=True)
    return out


def thumbnail_audio(src: Path, asset_id: str, run_id: str) -> Path:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np
    import soundfile as sf
    y, sr = sf.read(src, always_2d=True)
    m = y.mean(axis=1)
    out = ROOT / "gen" / "thumbs" / asset_id / f"{run_id}.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    fig, (a, b) = plt.subplots(2, 1, figsize=(3.2, 1.8), dpi=80)
    a.plot(np.arange(len(m)) / sr, m, linewidth=0.4)
    a.set_axis_off()
    b.specgram(m, Fs=sr, NFFT=512, noverlap=256)
    b.set_axis_off()
    fig.tight_layout(pad=0.1)
    fig.savefig(out)
    plt.close(fig)
    return out


def log_processing(sidecar: str | None, step: dict) -> None:
    """Append one processing step (tool, parameters, result) to a generation sidecar, so every edit is on record."""
    if not sidecar:
        return
    path = Path(sidecar)
    if not path.is_absolute() and not path.exists():
        path = ROOT / path
    meta = json.loads(path.read_text())
    meta.setdefault("processing", []).append({"utc": utc_now(), **step})
    path.write_text(json.dumps(meta, indent=2) + "\n")
