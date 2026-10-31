"""Commit the authorized course asset snapshot in bounded Git upload batches."""
from pathlib import Path
import json
import subprocess

ROOT=Path(__file__).resolve().parents[2]
COURSE=ROOT.parent/"csye-7270-course"
PREFIX="fall-2026/jingyao-y/assignment-5/walker-downfall/"
TARGET=COURSE/PREFIX
manifest=json.loads((TARGET/"evidence/a5/delivery-manifest.json").read_text(encoding="utf-8"))
rows=[r for r in manifest["files"] if r["path"].split("/")[0] in ("art","godot_assets","audio","textures")]
batches=[];batch=[];size=0
for row in rows:
    if batch and size+row["bytes"]>650_000_000:batches.append(batch);batch=[];size=0
    batch.append(row["path"]);size+=row["bytes"]
if batch:batches.append(batch)
receipts=[]
for i,batch in enumerate(batches):
    if i==0:batch=[".gitattributes"]+batch
    paths=ROOT/"logs"/f"a5-stage-assets-{i+1}.paths"
    paths.write_bytes(b"\0".join((PREFIX+p).encode("utf-8") for p in batch)+b"\0")
    subprocess.run(["git","add","--force","--pathspec-from-file="+str(paths),"--pathspec-file-nul"],cwd=COURSE,check=True)
    staged=subprocess.run(["git","diff","--cached","--quiet"],cwd=COURSE).returncode
    if not staged:continue
    subprocess.run(["git","commit","-m",f"Include complete A5 project assets ({i+1}/{len(batches)})"],cwd=COURSE,check=True,stdout=subprocess.DEVNULL)
    commit=subprocess.check_output(["git","rev-parse","HEAD"],cwd=COURSE,text=True).strip()
    receipts.append({"batch":i+1,"commit":commit,"path_count":len(batch)})
    print(json.dumps(receipts[-1]),flush=True)
(ROOT/"logs/a5-asset-commits.json").write_text(json.dumps(receipts,indent=2)+"\n",encoding="utf-8")
