"""Repair two measured undersize labels, retaining the first review sources."""
import json,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
p=ROOT/'beat_sheet.json';s=json.loads(p.read_text())
archive=ROOT/'_qc/label-revision';archive.mkdir(exist_ok=True)
if (archive/'beat_sheet.json').exists():raise SystemExit('Already prepared')
shutil.copy2(p,archive/'beat_sheet.json')
for b in s['beats']:
    if b['beat_id']=='B19':b['shot']['remotion']['props']['nodeSize']=60
    if b['beat_id'] in ['B16','B19','B21']:
        src=ROOT/'media'/f"{b['beat_id']}.mp4";shutil.move(src,archive/src.name)
        b['shot']['remotion'].pop('rendered',None)
p.write_text(json.dumps(s,indent=2)+'\n')
