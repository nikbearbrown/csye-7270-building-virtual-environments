"""Compare a DXGI desktop capture with the same controlled engine image."""
from pathlib import Path
import json
import os
import subprocess
import time
from PIL import Image,ImageStat

ROOT=Path(__file__).resolve().parents[2]
log_path=ROOT/"logs/a5_system_comparison.log"
with log_path.open("wb") as log:
    process=subprocess.Popen([os.environ.get("GODOT",str(ROOT.parent/"Godot_v4.7.2-stable_win64_console.exe")),"--path",str(ROOT),"--script","res://tools/a5/capture_use_it.gd","--resolution","1280x720","--fixed-fps","60","--","fire"],stdout=log,stderr=subprocess.STDOUT)
    deadline=time.monotonic()+300
    while time.monotonic()<deadline and process.poll() is None:
        if "A5_OS_CAPTURE_READY" in log_path.read_text(encoding="utf-8",errors="replace"):break
        time.sleep(.1)
    destination=ROOT/"evidence/a5/use-it/fire-r1-dxgi.png"
    capture=subprocess.run(["ffmpeg","-v","warning","-y","-f","lavfi","-i","ddagrab=output_idx=0:offset_x=80:offset_y=80:video_size=1280x720:framerate=5","-frames:v","1","-vf","hwdownload,format=bgra",str(destination)],capture_output=True,text=True,timeout=30)
    process.wait(timeout=300)
result={"capture_exit_code":capture.returncode,"capture_stderr":capture.stderr,"engine_exit_code":process.returncode}
if destination.exists():
    image=Image.open(destination).convert("RGB")
    result.update({"size":image.size,"extrema":image.getextrema(),"stddev":ImageStat.Stat(image).stddev,"samples":[image.getpixel((640,420)),image.getpixel((704,420))]})
(ROOT/"evidence/a5/use-it/system-comparison.json").write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
print(json.dumps(result,indent=2))
