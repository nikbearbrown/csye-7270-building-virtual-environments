"""Attach completed GitHub-clone results without changing runtime sources."""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess

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
text=("\n## Fresh GitHub checkout\n\n"
      f"Tested commit: {receipt['tested_commit']}. A new checkout of the GitHub branch "
      "started without a .godot cache. Its delivered file manifest matched byte for byte. "
      f"The clean import exited 0 in {receipt['import_seconds']} seconds with no existing .import changes. "
      "The complete fixed-rate run returned 70/73 original suites, with only test_combat, "
      "test_loading_screen and test_item_icons failing as in the baseline. Fire passed 89/89 "
      "at 30/60/144 fps, materials passed 120/120, and normal_map_check exited 0. "
      "The wall-time market suite ran after the parallel pool and passed. Protected sources "
      "stayed unchanged. Git fsck passed. The clone used local Git objects as a transfer "
      "reference, then dissociated; no alternates remain. This does not reuse Godot's import cache. "
      "The final release adds these receipts and report text; its runtime hashes match the tested commit. "
      "Evidence: evidence/a5/fresh-clone/.\n")
for base in (ROOT,TARGET):
    report=base/"TEST-REPORT.md"
    content=report.read_text(encoding="utf-8").split("\n## Fresh GitHub checkout\n")[0]+text
    report.write_text(content,encoding="utf-8")
    (base/"a5/final-documents/TEST-REPORT.md").write_text(content,encoding="utf-8")
paths=[p.relative_to(COURSE).as_posix() for p in destination.rglob("*") if p.is_file()]
paths += [PREFIX+"TEST-REPORT.md",PREFIX+"a5/final-documents/TEST-REPORT.md"]
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
subprocess.run(["git","commit","-m","Record fresh GitHub clone import and A5 regression verification"],cwd=COURSE,check=True)
release=subprocess.check_output(["git","rev-parse","HEAD"],cwd=COURSE,text=True).strip()
changed=subprocess.check_output(["git","diff","--name-only",receipt["tested_commit"],release],cwd=COURSE,text=True).splitlines()
assert all(p.startswith(PREFIX+"evidence/a5/fresh-clone/") or p in (PREFIX+"TEST-REPORT.md",PREFIX+"a5/final-documents/TEST-REPORT.md",PREFIX+"evidence/a5/delivery-manifest.json") for p in changed),changed
subprocess.run(["git","tag","-a","a5","-m","Assignment 5: verified shader and material submission"],cwd=COURSE,check=True)
receipt["release_commit"]=release
receipt["release_tag"]="a5"
receipt["metadata_only_paths"]=changed
(OUT/"release-verification.json").write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
print("Release "+release,flush=True)
