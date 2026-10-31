"""Keep two independent real-renderer hint receipts on each installed adapter."""
from pathlib import Path
import hashlib
import json
import os
import shutil
import subprocess

ROOT=Path(__file__).resolve().parents[2]
output=ROOT/"evidence/a5/hint-experiment"
results=[]
for adapter in (0,1):
    for repeat in (1,2):
        folder=output/"runs"/f"adapter-{adapter}-run-{repeat}"
        folder.mkdir(parents=True,exist_ok=True)
        command=[os.environ.get("GODOT",str(ROOT.parent/"Godot_v4.7.2-stable_win64_console.exe")),"--path",str(ROOT),"--script","res://tests/a5_capture_hint.gd","--gpu-index",str(adapter),"--resolution","1280x720","--fixed-fps","60"]
        with (folder/"capture.log").open("wb") as log:
            process=subprocess.run(command,stdout=log,stderr=subprocess.STDOUT,timeout=300)
        assert process.returncode==0
        for name in ("measurement.json","hint-experiment.png"):shutil.copy2(output/name,folder/name)
        measurement=json.loads((folder/"measurement.json").read_text(encoding="utf-8"))
        row={"adapter_index":adapter,"repeat":repeat,"exit_code":process.returncode,"measurement":measurement,"image_sha256":hashlib.sha256((folder/"hint-experiment.png").read_bytes()).hexdigest(),"receipt":folder.relative_to(ROOT).as_posix()}
        results.append(row);print(json.dumps(row),flush=True)
(output/"four-runs.json").write_text(json.dumps(results,indent=2)+"\n",encoding="utf-8")
