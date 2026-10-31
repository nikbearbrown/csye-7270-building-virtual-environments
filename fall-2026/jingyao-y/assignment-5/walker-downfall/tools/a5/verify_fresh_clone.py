"""Verify the published A5 project in a new GitHub checkout and empty Godot cache."""
from pathlib import Path
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time

ROOT=Path(__file__).resolve().parents[2]
COURSE=ROOT.parent/"csye-7270-course"
PREFIX="fall-2026/jingyao-y/assignment-5/walker-downfall"
REMOTE="https://github.com/nikbearbrown/csye-7270-building-virtual-environments.git"
OUT=ROOT.parent/"evidence/a5-release-verification"
OUT.mkdir(parents=True,exist_ok=True)
parser=argparse.ArgumentParser()
parser.add_argument("--existing",type=Path)
args=parser.parse_args()
CLONE=args.existing or ROOT.parent/"build"/("a5-github-fresh-"+time.strftime("%Y%m%d-%H%M%S"))
command=["git","clone","--depth","1","--filter=blob:none","--single-branch","--branch","Jingyao_Y","--no-checkout",REMOTE,str(CLONE)]
if args.existing:
    assert (CLONE/".git").is_dir() and not (CLONE/PREFIX/".godot").exists()
    subprocess.run(["git","fetch","origin","Jingyao_Y"],cwd=CLONE,check=True)
    subprocess.run(["git","checkout","--detach","FETCH_HEAD"],cwd=CLONE,check=True)
else:
    assert not CLONE.exists()
    subprocess.run(command,check=True)
    subprocess.run(["git","sparse-checkout","set",PREFIX],cwd=CLONE,check=True)
    subprocess.run(["git","checkout"],cwd=CLONE,check=True)
commit=subprocess.check_output(["git","rev-parse","HEAD"],cwd=CLONE,text=True).strip()
project=CLONE/PREFIX
assert not (project/".godot").exists()
assert not (CLONE/".git/objects/info/alternates").exists()
with (OUT/"git-fsck.log").open("wb") as log:
    subprocess.run(["git","fsck","--full"],cwd=CLONE,stdout=log,stderr=subprocess.STDOUT,check=True)
manifest=json.loads((project/"evidence/a5/delivery-manifest.json").read_text(encoding="utf-8"))
mismatches=[]
for row in manifest["files"]:
    path=project/row["path"]
    if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest()!=row["sha256"]:mismatches.append(row["path"])
assert not mismatches,mismatches
runtime={p.relative_to(project).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in project.rglob("*") if p.is_file() and not any(x in (".godot","evidence","logs","a5","youtube","tools") for x in p.relative_to(project).parts) and p.suffix.lower() in (".gd",".gdshader",".tscn",".tres",".godot",".png",".glb",".gltf",".import",".uid",".wav",".ogg",".ttf")}
receipt={"remote":REMOTE,"branch":"Jingyao_Y","tested_commit":commit,"clone":str(CLONE),"project":str(project),"clone_command":command,"git_objects":"Downloaded from GitHub with a blob-filtered sparse checkout; no local object reference or alternates.","godot_cache_initially_absent":True,"manifest_file_count":len(manifest["files"]),"manifest_mismatches":mismatches,"runtime_source_hashes":runtime,"status":"RUNNING"}
(OUT/"release-verification.json").write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
env=dict(os.environ,PYTHONUTF8="1",GODOT=str(ROOT.parent/"Godot_v4.7.2-stable_win64_console.exe"))
subprocess.run([sys.executable,str(project/"tools/a5/import_audit.py"),str(project),"--out","evidence/a5/fresh-clone/import"],env=env,check=True)
imported=json.loads((project/"evidence/a5/fresh-clone/import/summary.json").read_text(encoding="utf-8"))
assert imported["cache_was_absent"] and imported["exit_code"]==0 and not imported["changed"]
subprocess.run([sys.executable,str(project/"tools/a5/run_regression.py"),"--jobs","4","--out","evidence/a5/fresh-clone/regression"],env=env,check=True)
tests=json.loads((project/"evidence/a5/fresh-clone/regression/summary.json").read_text(encoding="utf-8"))
expected={"test_combat","test_loading_screen","test_item_icons"}
assert tests["baseline_suite_count"]==73 and tests["baseline_passed"]==70,tests["baseline_failures"]
assert set(tests["baseline_failures"])==expected
assert tests["protected_sources_unchanged"]
a5=[r for r in tests["runs"] if r["category"]=="a5"]
assert len(a5)==5 and all(r["passed"] for r in a5)
for r in a5:
    if r["suite"]=="test_fire_shader":assert r["pass_lines"]==89
    if r["suite"]=="test_materials":assert r["pass_lines"]==120
shutil.copytree(project/"evidence/a5/fresh-clone",OUT/"fresh-clone",dirs_exist_ok=True)
receipt.update(status="PASS",baseline_passed=70,baseline_total=73,baseline_failures=sorted(expected),a5_runs=a5,import_seconds=imported["seconds"],import_changed=imported["changed"])
(OUT/"release-verification.json").write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
print(json.dumps({k:v for k,v in receipt.items() if k not in ("runtime_source_hashes","a5_runs")},indent=2),flush=True)
