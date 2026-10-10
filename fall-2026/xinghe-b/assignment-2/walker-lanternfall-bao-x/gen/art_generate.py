#!/usr/bin/env python3
"""Generate image candidates with FLUX.1-schnell (mflux, local) and log one sidecar per image.

The model is loaded once per invocation and reused for every pose x seed.

    gen/.venv-art/bin/python gen/art_generate.py gen/prompts/ART-PC-01.json --seeds 11 23
    gen/.venv-art/bin/python gen/art_generate.py gen/prompts/ART-PC-01.json --seeds 5 --poses hurt defeat
    gen/.venv-art/bin/python gen/art_generate.py gen/prompts/ART-EN-01.json --seeds 3 7 9

A spec either has one "prompt", or a "template" containing {pose} plus a "poses" list of
{"name": ..., "text": ...}; the full expanded prompt is what gets logged.
"""
import argparse
import json
import time
from importlib.metadata import version
from pathlib import Path

from common import ROOT, new_run_id, rel, thumbnail_image, write_sidecar

ap = argparse.ArgumentParser()
ap.add_argument("spec")
ap.add_argument("--seeds", type=int, nargs="+", required=True)
ap.add_argument("--poses", nargs="*", help="only these pose names (default: all)")
a = ap.parse_args()
spec = json.loads(Path(a.spec).read_text())

if "poses" in spec:
    jobs = [(p["name"], spec["template"].format(pose=p["text"])) for p in spec["poses"] if not a.poses or p["name"] in a.poses]
else:
    jobs = [(None, spec["prompt"])]

import mlx.core as mx
from huggingface_hub.constants import HF_HUB_CACHE
from mflux.models.common.config.model_config import ModelConfig
from mflux.models.flux.variants.txt2img.flux import Flux1

quantize = spec.get("quantize", 4)
# A 16 GB machine swaps itself to a standstill if MLX keeps its buffer cache between images
# (2026-09-29: 40 s -> 6620 s per image within one process). Cap the cache and clear it after every image.
mx.set_cache_limit(512 * 1024 * 1024)
saved = ROOT / "gen" / "cache" / f"flux-schnell-{quantize}bit"
revision = (Path(HF_HUB_CACHE) / "models--black-forest-labs--FLUX.1-schnell" / "refs" / "main").read_text().strip()
if saved.exists():
    flux = Flux1(model_config=ModelConfig.schnell(), model_path=str(saved))
    weights = f"{quantize}-bit copy saved locally with mflux-save from FLUX.1-schnell @ {revision[:7]}"
else:
    flux = Flux1(model_config=ModelConfig.schnell(), quantize=quantize)
    weights = f"FLUX.1-schnell @ {revision[:7]}, quantized to {quantize}-bit at load"

for pose, prompt in jobs:
    for seed in a.seeds:
        run_id = new_run_id(spec["asset_id"], seed) + (f"-{pose}" if pose else "")
        out = ROOT / "gen" / "raw" / spec["asset_id"] / f"{run_id}.png"
        out.parent.mkdir(parents=True, exist_ok=True)
        t0 = time.time()
        image = flux.generate_image(seed=seed, prompt=prompt, num_inference_steps=spec.get("steps", 4),
                                    width=spec["width"], height=spec["height"])
        image.save(path=str(out))
        del image
        mx.clear_cache()
        thumb = thumbnail_image(out, spec["asset_id"], run_id)
        settings = {"seed": seed, "width": spec["width"], "height": spec["height"], "steps": spec.get("steps", 4),
                    "quantize": quantize, "seconds": round(time.time() - t0, 1),
                    "peak_gb": round(mx.get_peak_memory() / 1e9, 2)}
        if pose:
            settings["pose"] = pose
        side = write_sidecar({
            "asset_id": spec["asset_id"], "run_id": run_id,
            "model": "black-forest-labs/FLUX.1-schnell", "model_version": f"mflux {version('mflux')} (Python API); {weights}",
            "license": "Apache-2.0 (FLUX.1-schnell weights); outputs usable without restriction",
            "prompt": prompt, "negative_prompt": spec.get("negative_prompt", ""),
            "settings": settings, "raw_outputs": [rel(out)], "thumbnail": rel(thumb),
            "storyboard_panels": spec["storyboard_panels"],
        })
        print(side.name, settings["seconds"], "s, peak", settings["peak_gb"], "GB, active",
              round(mx.get_active_memory() / 1e9, 2), "GB", flush=True)
        mx.reset_peak_memory()
