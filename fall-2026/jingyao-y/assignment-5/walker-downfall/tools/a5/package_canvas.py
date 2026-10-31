"""Package the verified course project and film with ZIP64 and a checked index."""
from pathlib import Path
import hashlib
import json
import zipfile

def digest(path):
    result=hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda:handle.read(1024*1024),b""):result.update(block)
    return result.hexdigest()

ROOT=Path(__file__).resolve().parents[2]
COURSE=ROOT.parent/"csye-7270-course/fall-2026/jingyao-y/assignment-5/walker-downfall"
REEL=ROOT/"youtube/claude-liam-downfall-a5-shaders-gamedev"
OUTPUT=ROOT.parent/"canvas-submission/assignment-5"
OUTPUT.mkdir(parents=True,exist_ok=True)
TARGET=OUTPUT/"walker-downfall-a5-canvas.zip"
assert (COURSE/"project.godot").is_file()
MASTER=REEL/"exports/landscape"/(REEL.name+".mp4")
VERIFIED=MASTER.with_suffix(".verified.json")
assert MASTER.is_file() and VERIFIED.is_file()
receipt=json.loads(VERIFIED.read_text(encoding="utf-8"))
media_hash=digest(MASTER)
assert media_hash in json.dumps(receipt),"Final film receipt does not identify this MP4"
state=json.loads((REEL/"build-state.json").read_text(encoding="utf-8"))
review=json.loads((REEL/"_qc/final-review.json").read_text(encoding="utf-8"))
assert state["status"]=="ready" and state["sha256"]==media_hash
assert review["status"]=="PASS" and review["master_sha256"]==media_hash
files=[p for p in COURSE.rglob("*") if p.is_file() and not any(part in (".git",".godot","__pycache__","node_modules") for part in p.relative_to(COURSE).parts)]
with zipfile.ZipFile(TARGET,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=3,allowZip64=True) as archive:
    for path in files:archive.write(path,"walker-downfall/"+path.relative_to(COURSE).as_posix())
    archive.write(COURSE/"SUBMISSION.md","SUBMISSION.md")
    archive.write(MASTER,"film/"+MASTER.name)
    archive.write(VERIFIED,"film/"+VERIFIED.name)
    verification=ROOT.parent/"evidence/a5-release-verification"
    if verification.exists():
        for path in verification.rglob("*"):
            if path.is_file():archive.write(path,"verification/"+path.relative_to(verification).as_posix())
with zipfile.ZipFile(TARGET) as archive:
    bad=archive.testzip();assert bad is None,bad
    assert "walker-downfall/project.godot" in archive.namelist()
    count=len(archive.infolist())
summary={"zip":TARGET.name,"bytes":TARGET.stat().st_size,"sha256":digest(TARGET),"entries":count,"crc_check":"PASS","film_sha256":media_hash}
(OUTPUT/"zip-verification.json").write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
print(json.dumps(summary,indent=2))
