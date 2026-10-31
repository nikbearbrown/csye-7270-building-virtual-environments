"""Include film paperwork and compact visual evidence without rendered media."""
from pathlib import Path
import json
import shutil

ROOT=Path(__file__).resolve().parents[2]
REEL=ROOT/"youtube/claude-liam-downfall-a5-shaders-gamedev"
TARGET=ROOT.parent/"csye-7270-course/fall-2026/jingyao-y/assignment-5/walker-downfall"
selected=list(REEL.glob("*.md"))+list(REEL.glob("*.json"))
selected+=list((REEL/"_qc").glob("*.md"))+list((REEL/"_qc").glob("*.json"))
selected+=list((REEL/"_qc/beat-frames").glob("*-50.png"))
selected+=list((REEL/"exports/landscape").glob("*.verified.json"))
copied=[]
for source in selected:
    relative=source.relative_to(ROOT)
    destination=TARGET/relative
    destination.parent.mkdir(parents=True,exist_ok=True)
    shutil.copy2(source,destination)
    copied.append(relative.as_posix())
(ROOT/"logs/a5-film-record-paths.json").write_text(json.dumps(copied,indent=2)+"\n",encoding="utf-8")
print(f"Copied {len(copied)} film records and review frames")
