"""One-time typography revision, retaining superseded render slots for comparison."""
import json, re, shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sheet_path=ROOT/'beat_sheet.json'
sheet=json.loads(sheet_path.read_text())
if sheet['metadata'].get('typography_revision'):
    raise SystemExit('Revision already prepared; use lock-and-render.py remotion --only to resume.')
classes={name.split('_')[0]:name for name in re.findall(r'class (B\d+_\w+)\(CourseMechanism\)',(ROOT/'scenes.py').read_text())}
for b in sheet['beats']:
    b['lane']=b['shot']['lane']
    if b['lane']=='MANIM': b['shot']['manim']['scene']=classes[b['beat_id']]
    if b['lane']=='VOX':
        # The source image is archival; its designed heading/footer still needs pixel QC.
        b['shot']['type']='REMOTION'
    if b['beat_id']=='B34':
        # Legacy audit field; the canonical outro hardcodes this same handle.
        b['shot']['remotion']['props']['handle']='@NikBearBrown'
stale=['B03','B04','B06','B08','B10','B12','B13','B14','B16','B17','B19']
archive=ROOT/'_qc/font-revision';archive.mkdir(exist_ok=True)
for bid in stale:
    src=ROOT/'media'/f'{bid}.mp4';dst=archive/src.name
    if dst.exists(): raise SystemExit(f'Refusing overwrite of revision evidence: {dst}')
    if src.exists(): shutil.move(src,dst)
sheet['metadata']['typography_revision']='Footer 50 logical px; card labels 54; source evidence shells included in pixel checks.'
sheet_path.write_text(json.dumps(sheet,indent=2)+'\n')
print('Rerender:', ' '.join(stale))
