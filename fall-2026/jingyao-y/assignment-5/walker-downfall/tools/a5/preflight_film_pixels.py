"""Check repaired media-slot pixels before spending another full master encode."""
from pathlib import Path
import importlib.util
import json
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[2]
REEL=ROOT/"youtube/claude-liam-downfall-a5-shaders-gamedev"
module_path=ROOT.parent/"brutalist.art/runtime/qc/final_frame_check.py"
spec=importlib.util.spec_from_file_location("a5_frame_gate",module_path)
gate=importlib.util.module_from_spec(spec);spec.loader.exec_module(gate)
sheet=json.loads((REEL/"beat_sheet.json").read_text(encoding="utf-8"))
folder=REEL/"_qc/slot-preflight";folder.mkdir(exist_ok=True)
rows=[]
for beat in sheet["beats"]:
    if beat["beat_id"] not in ["B01","B02","B03","B05","B07","B09","B11","B13","B15","B17"]:continue
    for fraction in (.5,.85):
        destination=folder/f"{beat['beat_id']}-{int(fraction*100)}.png"
        duration=float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",str(REEL/"media"/(beat["beat_id"]+".mp4"))],text=True))
        subprocess.run(["ffmpeg","-v","error","-y","-ss",str(duration*fraction),"-i",str(REEL/"media"/(beat["beat_id"]+".mp4")),"-frames:v","1",str(destination)],check=True)
        qc=beat.get("qc",{})
        defects,cover=gate.analyze_frame(destination,regions=qc.get("contrast_regions"))
        if qc.get("full_bleed"):defects=[d for d in defects if d[1]!="edge-bleed"]
        rows.append({"beat":beat["beat_id"],"fraction":fraction,"cover":cover,"defects":defects,"image":destination.relative_to(REEL).as_posix()})
(REEL/"_qc/slot-preflight.json").write_text(json.dumps(rows,indent=2)+"\n",encoding="utf-8")
print(json.dumps([{k:v for k,v in r.items() if k!="image"} for r in rows],indent=2))
raise SystemExit(1 if any(r["defects"] for r in rows) else 0)
