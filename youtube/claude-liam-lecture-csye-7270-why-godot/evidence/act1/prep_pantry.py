#!/usr/bin/env python3
"""prep_pantry.py — rebuilds every Act I image in pantry/ from the real captures (nothing is drawn or edited, only cropped/cut).
  python3 evidence/act1/prep_pantry.py        (the editor shot comes from capture_editor.sh)
a1_pong_001..105.jpg   Walker Pong clip 0-7.0 s, 15 fps, cropped to the playfield (x 97..1825 of 1920), scaled 1152x720
a1_license_crop.png    godot-license.png (3840x2160) crop (940,690,2880,1786): 'The engine' paragraph + the three freedoms
a1_download_btn.jpg    godot-download-mac.png crop (1100,720,2740,1290): the Godot Engine / .NET buttons and the date line
(the page's dark artwork is cropped out: it fails GATE T; see evidence/act1/cropgate.py)"""
import subprocess
from pathlib import Path
from PIL import Image
REEL = Path(__file__).resolve().parents[2]
EV = REEL.parent / "_conducting-series-evidence"
P = REEL / "pantry"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-t", "7.0", "-i", str(EV / "godot-captures/walker-pong/walker-pong-clip.mp4"),
                "-vf", "fps=15,crop=1728:1080:97:0,scale=1152:720", "-q:v", "3", str(P / "a1_pong_%03d.jpg")], check=True)
Image.open(EV / "web-captures/godot-license.png").convert("RGB").crop((940, 690, 2880, 1786)).save(P / "a1_license_crop.png")
Image.open(EV / "web-captures/godot-download-mac.png").convert("RGB").crop((1100, 720, 2740, 1290)).save(P / "a1_download_btn.jpg", quality=93)
print("ok")
