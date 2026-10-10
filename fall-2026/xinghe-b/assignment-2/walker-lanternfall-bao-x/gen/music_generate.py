#!/usr/bin/env python3
"""Generate music candidates with MusicGen (local, transformers) and log a sidecar per seed.

    gen/.venv-audio/bin/python gen/music_generate.py gen/prompts/MUS-01.json --seeds 5 8 13 21
"""
import argparse, json, time
from pathlib import Path
import librosa
import soundfile as sf
import torch
import transformers
from huggingface_hub import snapshot_download
from transformers import AutoProcessor, MusicgenForConditionalGeneration, MusicgenMelodyForConditionalGeneration
from common import ROOT, new_run_id, rel, thumbnail_audio, write_sidecar

ap = argparse.ArgumentParser()
ap.add_argument("spec")
ap.add_argument("--seeds", type=int, nargs="+", required=True)
a = ap.parse_args()
spec = json.loads(Path(a.spec).read_text())
repo = spec["model"]
melody = "melody" in repo
revision = Path(snapshot_download(repo, local_files_only=True)).name
proc = AutoProcessor.from_pretrained(repo)
device = "mps" if torch.backends.mps.is_available() else "cpu"
# fp32 on a 16 GB Mac grew to 14 GB and lived in swap (2026-09-29); fp16 on MPS peaks at ~6 GB and is ~10x faster.
dtype = torch.float16 if device == "mps" else torch.float32
model = (MusicgenMelodyForConditionalGeneration if melody else MusicgenForConditionalGeneration).from_pretrained(repo, torch_dtype=dtype)
model = model.to(device)
sr = model.config.audio_encoder.sampling_rate
tokens = int(spec["duration_s"] * model.config.audio_encoder.frame_rate)

for seed in a.seeds:
    run_id = new_run_id(spec["asset_id"], seed)
    out = ROOT / "gen" / "raw" / spec["asset_id"] / f"{run_id}.wav"
    out.parent.mkdir(parents=True, exist_ok=True)
    torch.manual_seed(seed)
    kwargs = {"text": [spec["prompt"]], "padding": True, "return_tensors": "pt"}
    if melody:
        cond, _ = librosa.load(ROOT / spec["condition_on"], sr=proc.feature_extractor.sampling_rate, mono=True)
        kwargs.update(audio=cond, sampling_rate=proc.feature_extractor.sampling_rate)
    # floating inputs (the melody model's chroma features) must match the model dtype on MPS
    inputs = {k: (v.to(device, dtype=dtype) if v.is_floating_point() else v.to(device)) if hasattr(v, "to") else v
              for k, v in proc(**kwargs).items()}
    t0 = time.time()
    audio = model.generate(**inputs, do_sample=True, guidance_scale=spec.get("guidance_scale", 3.0), max_new_tokens=tokens)
    sf.write(out, audio[0, 0].float().cpu().numpy(), sr)
    if device == "mps":
        torch.mps.empty_cache()
    thumb = thumbnail_audio(out, spec["asset_id"], run_id)
    print(write_sidecar({
        "asset_id": spec["asset_id"], "run_id": run_id,
        "model": repo, "model_version": f"snapshot {revision}, transformers {transformers.__version__}",
        "license": "MusicGen weights CC-BY-NC-4.0 (non-commercial coursework use); AudioCraft code MIT",
        "prompt": spec["prompt"], "negative_prompt": spec["negative_prompt"],
        "settings": {"seed": seed, "duration_s": spec["duration_s"], "max_new_tokens": tokens, "guidance_scale": spec.get("guidance_scale", 3.0),
                     "sample_rate": sr, "device": device, "dtype": str(dtype).replace("torch.", ""), "condition_on": spec.get("condition_on"), "seconds": round(time.time() - t0, 1)},
        "raw_outputs": [rel(out)], "thumbnail": rel(thumb), "storyboard_panels": spec["storyboard_panels"],
    }))
