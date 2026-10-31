"""Import a project and retain exact before/after settings for changed sidecars."""
from pathlib import Path
import argparse
import difflib
import hashlib
import json
import os
import subprocess
import time

def main():
    parser=argparse.ArgumentParser();parser.add_argument("project",type=Path);parser.add_argument("--out",default="evidence/a5/clean-import");args=parser.parse_args()
    root=args.project.resolve();assert (root/"project.godot").exists()
    output=root/args.out;output.mkdir(parents=True,exist_ok=True)
    before={p.relative_to(root).as_posix():p.read_bytes() for p in root.rglob("*.import") if ".godot" not in p.relative_to(root).parts}
    cache_was_absent=not (root/".godot").exists()
    engine=Path(os.environ.get("GODOT",str(Path(__file__).resolve().parents[3]/"Godot_v4.7.2-stable_win64_console.exe")))
    started=time.monotonic()
    with (output/"import.log").open("wb") as log:
        process=subprocess.run([str(engine),"--headless","--editor","--path",str(root),"--import"],stdout=log,stderr=subprocess.STDOUT,timeout=3600)
    after={p.relative_to(root).as_posix():p.read_bytes() for p in root.rglob("*.import") if ".godot" not in p.relative_to(root).parts}
    changed=[]
    for path,data in before.items():
        if after.get(path)!=data:
            changed.append(path)
            destination=output/"before"/path;destination.parent.mkdir(parents=True,exist_ok=True);destination.write_bytes(data)
            destination=output/"after"/path;destination.parent.mkdir(parents=True,exist_ok=True);destination.write_bytes(after.get(path,b""))
            diff="".join(difflib.unified_diff(data.decode("utf-8").splitlines(True),after.get(path,b"").decode("utf-8").splitlines(True),fromfile="before/"+path,tofile="after/"+path))
            (output/(path.replace("/","__")+".diff")).write_text(diff,encoding="utf-8")
    report={"engine":str(engine),"cache_was_absent":cache_was_absent,"exit_code":process.returncode,"seconds":round(time.monotonic()-started,2),"before_count":len(before),"after_count":len(after),"changed":changed,"created":sorted(set(after)-set(before)),"before_hashes":{p:hashlib.sha256(b).hexdigest() for p,b in before.items()},"after_hashes":{p:hashlib.sha256(b).hexdigest() for p,b in after.items()}}
    (output/"summary.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({k:v for k,v in report.items() if not k.endswith("hashes")},indent=2),flush=True)
    return process.returncode

if __name__=="__main__":raise SystemExit(main())
