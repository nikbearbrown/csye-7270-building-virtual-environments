#!/usr/bin/env python3
"""
Generates godot/sfx/hit_click.wav and its Godot .import sidecar.

Output:  mono, 16-bit PCM, 44100 Hz, 60 ms
Signal:  1500 Hz sine wave, exponential decay (tau = 15 ms), peak at -6 dBFS
Libs:    Python 3 standard library only — wave, struct, math, hashlib, os
"""
import hashlib
import math
import os
import struct
import wave

# ── audio parameters ──────────────────────────────────────────────────────────
SAMPLE_RATE = 44100
DURATION_MS = 60
FREQ_HZ     = 1500
PEAK_DBFS   = -6.0
TAU_S       = 0.015        # 15 ms decay time constant → ~e^-4 at 60 ms

# ── paths ─────────────────────────────────────────────────────────────────────
SCRIPT_DIR   = os.path.dirname(os.path.abspath(__file__))
GODOT_DIR    = os.path.join(SCRIPT_DIR, "..", "godot")
SFX_DIR      = os.path.join(GODOT_DIR, "sfx")
WAV_PATH     = os.path.join(SFX_DIR, "hit_click.wav")
IMPORT_PATH  = WAV_PATH + ".import"
IMPORTED_DIR = os.path.join(GODOT_DIR, ".godot", "imported")

# UID used in both the .import file and main.tscn's ext_resource.
WAV_UID = "uid://b1hclk5n0t4xe"

# ── generate samples ──────────────────────────────────────────────────────────
num_samples = int(SAMPLE_RATE * DURATION_MS / 1000)   # 2646
peak_amp    = (2 ** 15 - 1) * 10 ** (PEAK_DBFS / 20)  # ≈ 16421

samples = []
for i in range(num_samples):
    t        = i / SAMPLE_RATE
    envelope = math.exp(-t / TAU_S)
    value    = peak_amp * math.sin(2 * math.pi * FREQ_HZ * t) * envelope
    samples.append(max(-32768, min(32767, int(round(value)))))

# ── write WAV ─────────────────────────────────────────────────────────────────
os.makedirs(SFX_DIR, exist_ok=True)
with wave.open(WAV_PATH, "w") as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(SAMPLE_RATE)
    wf.writeframes(struct.pack(f"<{len(samples)}h", *samples))

print(f"Wrote {len(samples)} samples ({DURATION_MS} ms) → {WAV_PATH}")

# ── compute source MD5 (used in the .godot/imported/ filename) ────────────────
with open(WAV_PATH, "rb") as f:
    wav_md5 = hashlib.md5(f.read()).hexdigest()

sample_name  = f"hit_click.wav-{wav_md5}.sample"
imported_rel = f"res://.godot/imported/{sample_name}"

# ── write Godot import sidecar ────────────────────────────────────────────────
# Godot reads the UID from this file; it reimports the .sample if missing but
# preserves the UID, so the UID in main.tscn stays consistent.
import_text = f"""\
[remap]

importer="wav"
type="AudioStreamWAV"
uid="{WAV_UID}"
path="{imported_rel}"

[deps]

source_file="res://sfx/hit_click.wav"
dest_files=["{imported_rel}"]

[params]

force/8_bit=false
force/mono=false
force/max_rate=false
force/max_rate_hz=44100
edit/trim=false
edit/normalize=false
edit/loop_mode=0
edit/loop_begin=0
edit/loop_end=-1
compress/mode=0
"""
with open(IMPORT_PATH, "w") as f:
    f.write(import_text)

print(f"Wrote import sidecar → {IMPORT_PATH}")
print(f"WAV MD5: {wav_md5}  UID: {WAV_UID}")
