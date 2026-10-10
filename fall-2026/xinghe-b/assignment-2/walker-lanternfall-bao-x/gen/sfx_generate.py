#!/usr/bin/env python3
"""Generate SFX candidates with Stable Audio Open 1.0 (local) and log a sidecar per seed.

    gen/.venv-audio/bin/python gen/sfx_generate.py gen/prompts/SFX-01.json --seeds 1 2 3 4
"""
import argparse, json, time
from pathlib import Path
import soundfile as sf
import torch
import diffusers
from diffusers import StableAudioPipeline
from huggingface_hub import snapshot_download
from common import ROOT, new_run_id, rel, thumbnail_audio, write_sidecar

REPO = "stabilityai/stable-audio-open-1.0"
ap = argparse.ArgumentParser()
ap.add_argument("spec")
ap.add_argument("--seeds", type=int, nargs="+", required=True)
a = ap.parse_args()
spec = json.loads(Path(a.spec).read_text())
revision = Path(snapshot_download(REPO, local_files_only=True)).name
device = "mps" if torch.backends.mps.is_available() else "cpu"
pipe = StableAudioPipeline.from_pretrained(REPO, torch_dtype=torch.float32).to(device)
import sfx_sampler_fix  # the model's default sampler fails on its last step without this (see the module docstring)

FIX = sfx_sampler_fix.apply()
SCHEDULER = f"{type(pipe.scheduler).__name__} (model default); {FIX}"
sr = pipe.vae.sampling_rate

for seed in a.seeds:
    run_id = new_run_id(spec["asset_id"], seed)
    out = ROOT / "gen" / "raw" / spec["asset_id"] / f"{run_id}.wav"
    out.parent.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    g = torch.Generator("cpu").manual_seed(seed)
    audio = pipe(spec["prompt"], negative_prompt=spec["negative_prompt"], num_inference_steps=spec.get("steps", 100),
                 guidance_scale=spec.get("cfg", 7.0), audio_end_in_s=spec["duration_s"], generator=g).audios[0]
    sf.write(out, audio.T.float().cpu().numpy(), sr)
    if device == "mps":
        torch.mps.empty_cache()
    thumb = thumbnail_audio(out, spec["asset_id"], run_id)
    print(write_sidecar({
        "asset_id": spec["asset_id"], "run_id": run_id,
        "model": REPO, "model_version": f"snapshot {revision}, diffusers {diffusers.__version__}",
        "license": "Stability AI Community License (free for non-commercial and < $1M revenue use; outputs owned by the user)",
        "prompt": spec["prompt"], "negative_prompt": spec["negative_prompt"],
        "settings": {"seed": seed, "duration_s": spec["duration_s"], "steps": spec.get("steps", 100), "cfg": spec.get("cfg", 7.0),
                     "sample_rate": sr, "device": device, "scheduler": SCHEDULER, "seconds": round(time.time() - t0, 1)},
        "raw_outputs": [rel(out)], "thumbnail": rel(thumb), "storyboard_panels": spec["storyboard_panels"],
    }))
