"""Copy the complete distributable Godot project into the course assignment."""
from pathlib import Path
import argparse
import hashlib
import json
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[2]
COURSE = ROOT.parent / "csye-7270-course"
TARGET = COURSE / "fall-2026/jingyao-y/assignment-5/walker-downfall"

def main():
    parser=argparse.ArgumentParser();parser.add_argument("--dry-run",action="store_true");args=parser.parse_args()
    assert TARGET.resolve().is_relative_to(COURSE.resolve())
    assert (COURSE/".git").is_dir() and (ROOT/"project.godot").is_file()
    # Merge prior A5 evidence before copying; historical records stay intact.
    if not args.dry_run:
        for path in (TARGET/"evidence/a5/mutations").rglob("*"):
            if path.is_file():
                destination=ROOT/path.relative_to(TARGET)
                if not destination.exists():
                    destination.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(path,destination)
        guide=ROOT/"CHANGE-BRIEF-GUIDE.md"
        if not guide.exists(): shutil.copy2(TARGET/guide.name,guide)
    names=subprocess.check_output(["git","ls-files","--cached","--others","--exclude-standard","-z"],cwd=ROOT).decode().split("\0")
    files={Path(name) for name in names if name and (ROOT/name).is_file()}
    # Include the required write-ups even though the development checkout ignores Markdown.
    files.update(path.relative_to(ROOT) for path in ROOT.glob("*.md"))
    for folder in ("a5","evidence/a5","textures","materials","tools/a5"):
        files.update(path.relative_to(ROOT) for path in (ROOT/folder).rglob("*.md"))
    files.update(path.relative_to(ROOT) for path in ROOT.rglob("LICENSE*") if not any(part in (".git",".godot","node_modules","youtube") for part in path.relative_to(ROOT).parts))
    excluded=[];selected=[]
    for path in sorted(files):
        source=ROOT/path
        reason=""
        if source.suffix.lower() in (".mp4",".mp3",".avi",".mov"):reason="Rendered media is delivered outside GitHub."
        elif source.stat().st_size>25_000_000:reason="Course GitHub file-size limit; retained locally."
        elif path.as_posix()=="a5/sessions/session-2b.jsonl":reason="Oversize session; the annotated excerpt is included."
        elif any(part in (".git",".godot","node_modules","__pycache__","youtube") for part in path.parts):reason="Regenerable cache or separate film output."
        if reason:excluded.append({"path":path.as_posix(),"reason":reason});continue
        selected.append(path)
    manifest={"source_git_head":subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT,text=True).strip(),"source_worktree":"Includes the current working-tree game and A5 changes.", "project_root":"walker-downfall", "file_count":len(selected),"total_bytes":sum((ROOT/path).stat().st_size for path in selected), "excluded":excluded,"files":[]}
    copied=0
    for path in selected:
        source=ROOT/path
        if args.dry_run:continue
        destination=TARGET/path
        data=source.read_bytes();digest=hashlib.sha256(data).hexdigest()
        if not destination.exists() or hashlib.sha256(destination.read_bytes()).hexdigest()!=digest:
            destination.parent.mkdir(parents=True,exist_ok=True);destination.write_bytes(data);copied+=1
        manifest["files"].append({"path":path.as_posix(),"bytes":len(data),"sha256":digest})
    if not args.dry_run:
        attributes=TARGET/".gitattributes"
        attributes.write_text("# Preserve the measured project snapshot byte-for-byte across checkouts.\n* -text\n",encoding="utf-8")
        manifest["files"].append({"path":".gitattributes","bytes":attributes.stat().st_size,"sha256":hashlib.sha256(attributes.read_bytes()).hexdigest()})
        manifest["file_count"]=len(manifest["files"])
        manifest["total_bytes"]=sum(row["bytes"] for row in manifest["files"])
        output=TARGET/"evidence/a5/delivery-manifest.json";output.parent.mkdir(parents=True,exist_ok=True)
        output.write_text(json.dumps(manifest,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({k:v for k,v in manifest.items() if k!="files"},indent=2))
    print("Copied",copied,"files")

if __name__=="__main__":main()
