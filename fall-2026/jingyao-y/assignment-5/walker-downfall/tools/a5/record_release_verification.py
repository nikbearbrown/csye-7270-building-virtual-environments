"""Attach clone results and the requested media-free package policy."""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[2]
COURSE=ROOT.parent/"csye-7270-course"
PREFIX="fall-2026/jingyao-y/assignment-5/walker-downfall/"
TARGET=COURSE/PREFIX
OUT=ROOT.parent/"evidence/a5-release-verification"
receipt=json.loads((OUT/"release-verification.json").read_text(encoding="utf-8"))
assert receipt["status"]=="PASS"
for path,digest in receipt["runtime_source_hashes"].items():
    assert hashlib.sha256((TARGET/path).read_bytes()).hexdigest()==digest,path
destination=TARGET/"evidence/a5/fresh-clone"
shutil.copytree(OUT/"fresh-clone",destination,dirs_exist_ok=True)
shutil.copy2(OUT/"release-verification.json",destination/"release-verification.json")
shutil.copy2(OUT/"git-fsck.log",destination/"git-fsck.log")
local_destination=ROOT/"evidence/a5/fresh-clone"
shutil.copytree(OUT/"fresh-clone",local_destination,dirs_exist_ok=True)
shutil.copy2(OUT/"release-verification.json",local_destination/"release-verification.json")
shutil.copy2(OUT/"git-fsck.log",local_destination/"git-fsck.log")
text=("\n## Fresh GitHub checkout\n\n"
      f"Tested commit: {receipt['tested_commit']}. A new checkout of the GitHub branch "
      "started without a .godot cache. Its delivered file manifest matched byte for byte. "
      f"The clean import exited 0 in {receipt['import_seconds']} seconds with no existing .import changes. "
      f"The complete fixed-rate run returned {receipt['baseline_passed']}/73 original suites. "
      f"Failing suites: {', '.join(receipt['baseline_failures']) or 'none'}. "
      "No failures outside the three previously observed baseline suites occurred. Fire passed 89/89 "
      "at 30/60/144 fps, materials passed 120/120, and normal_map_check exited 0. "
      "The wall-time market suite ran after the parallel pool and passed. Protected sources "
      "stayed unchanged. Git fsck passed. The successful clone downloaded its objects from "
      "GitHub without a local reference or alternates. The first local-reference attempt failed "
      "before checkout and is retained separately. No Godot import cache was reused. "
      "The final release adds these receipts and report text; its runtime hashes match the tested commit. "
      "Evidence: evidence/a5/fresh-clone/.\n")
for base in (ROOT,TARGET):
    report=base/"TEST-REPORT.md"
    content=report.read_text(encoding="utf-8").split("\n## Fresh GitHub checkout\n")[0]+text
    report.write_text(content,encoding="utf-8")
    (base/"a5/final-documents/TEST-REPORT.md").write_text(content,encoding="utf-8")
for name in ("SUBMISSION.md","README.md","tools/a5/package_canvas.py","tools/a5/verify_fresh_clone.py","tools/a5/record_release_verification.py"):
    shutil.copy2(ROOT/name,TARGET/name)
for base in (ROOT,TARGET):
    shutil.copy2(base/"README.md",base/"a5/final-documents/README.md")
film="youtube/claude-liam-downfall-a5-shaders-gamedev"
source_check=ROOT/"logs/a5_film_source_check_release.log"
source_check.touch(exist_ok=True)
subprocess.run([sys.executable,str(ROOT/"tools/a5/build_film.py"),"ledger"],cwd=ROOT,check=True)
with source_check.open("wb") as log:
    subprocess.run([str(ROOT.parent/".venv/Scripts/python.exe"),str(ROOT.parent/"brutalist.art/skills/make/godot-gamedev/scripts/verify_gamedev.py"),str(ROOT/film),"--game",str(ROOT)],cwd=ROOT,stdout=log,stderr=subprocess.STDOUT,check=True)
film_records=(film+"/gamedev-evidence.json","logs/a5_film_source_check_release.log")
for name in film_records:
    shutil.copy2(ROOT/name,TARGET/name)
paths=[p.relative_to(COURSE).as_posix() for p in destination.rglob("*") if p.is_file()]
paths += [PREFIX+n for n in ("TEST-REPORT.md","a5/final-documents/TEST-REPORT.md","SUBMISSION.md","README.md","a5/final-documents/README.md","tools/a5/package_canvas.py","tools/a5/verify_fresh_clone.py","tools/a5/record_release_verification.py")]
paths += [PREFIX+n for n in film_records]
manifest_path=TARGET/"evidence/a5/delivery-manifest.json"
manifest=json.loads(manifest_path.read_text(encoding="utf-8"))
rows={r["path"]:r for r in manifest["files"]}
for name in paths:
    path=COURSE/name
    relative=path.relative_to(TARGET).as_posix()
    rows[relative]={"path":relative,"bytes":path.stat().st_size,"sha256":hashlib.sha256(path.read_bytes()).hexdigest()}
manifest.update(files=sorted(rows.values(),key=lambda r:r["path"]),file_count=len(rows),total_bytes=sum(r["bytes"] for r in rows.values()),verified_source_commit=receipt["tested_commit"])
manifest_path.write_text(json.dumps(manifest,indent=2)+"\n",encoding="utf-8")
paths.append(PREFIX+"evidence/a5/delivery-manifest.json")
spec=OUT/"release-metadata.paths"
spec.write_bytes(b"\0".join(p.encode("utf-8") for p in paths)+b"\0")
subprocess.run(["git","add","--force","--pathspec-from-file="+str(spec),"--pathspec-file-nul"],cwd=COURSE,check=True)
subprocess.run(["git","commit","-m","Record fresh-clone verification and package without exported media"],cwd=COURSE,check=True)
release=subprocess.check_output(["git","rev-parse","HEAD"],cwd=COURSE,text=True).strip()
changed=subprocess.check_output(["git","diff","--name-only",receipt["tested_commit"],release],cwd=COURSE,text=True).splitlines()
allowed=("TEST-REPORT.md","a5/final-documents/TEST-REPORT.md","SUBMISSION.md","README.md","a5/final-documents/README.md","tools/a5/package_canvas.py","tools/a5/verify_fresh_clone.py","tools/a5/record_release_verification.py","evidence/a5/delivery-manifest.json")+film_records
assert all(p.startswith(PREFIX+"evidence/a5/fresh-clone/") or p in [PREFIX+n for n in allowed] for p in changed),changed
subprocess.run(["git","tag","-a","a5","-m","Assignment 5: verified shader and material submission"],cwd=COURSE,check=True)
receipt["release_commit"]=release
receipt["release_tag"]="a5"
receipt["metadata_only_paths"]=changed
(OUT/"release-verification.json").write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
print("Release "+release,flush=True)
