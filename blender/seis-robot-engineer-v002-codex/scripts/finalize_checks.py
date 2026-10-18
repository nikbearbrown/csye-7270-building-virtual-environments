from pathlib import Path
import json,hashlib,re,subprocess
from PIL import Image
R=Path(__file__).resolve().parents[1]
blend=R/'seis_robot_engineer_v002.blend';glb=R/'exports/seis_robot_engineer_v002.glb'
assert '"problems": []' in (R/'reports/glb-roundtrip.log').read_text()
assert json.loads((R/'reports/controls.json').read_text())['status']=='PASS'
views=list((R/'renders').glob('engineer-*.png'));assert len(views)==12,len(views)
for p in views:
 assert p.stat().st_mtime>blend.stat().st_mtime,p
 im=Image.open(p);im.verify()
for r in json.loads((R/'references/manifest.json').read_text()):
 if 'original_model' in r:
  assert hashlib.sha256(Path(r['original_model']).read_bytes()).hexdigest()==r['sha256']
 else:
  assert hashlib.sha256((R/r['copy']).read_bytes()).hexdigest()==r['sha256']
for link in re.findall(r'(?:src|href)="([^"]+)"',(R/'review.html').read_text()):
 if link.startswith(('http','#')) or link=='reports/CHECKS.md':continue
 assert (R/link).exists(),link
video=R/'renders/wrist-readout-preview.mp4'
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(video)]))
assert abs(float(probe['format']['duration'])-4)<.1
m=json.loads((R/'reports/asset-manifest.json').read_text())
record={'status':'technical checks passed; design approval pending','files':{str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [blend,glb,video]+views},'model':m,'source_v001_unchanged':True,'png_views':len(views),'readout_preview_seconds':float(probe['format']['duration'])}
(R/'reports/delivery-manifest.json').write_text(json.dumps(record,indent=2)+'\n')
(R/'reports/CHECKS.md').write_text(f"""# Technical checks — engineer v002

2026-10-17. Ready for design review; this is not human approval of the design.

- Saved Blender model: {m['meshes']} meshes, {m['triangles']:,} triangles, {m['bones']} bones.
- Every mechanical vertex has exactly one full-weight bone.
- Six spool caps and both mouth morph targets are present.
- Connector deployment was evaluated at 0, .25, .5, .75 and 1. Fingers fold first; the palm separates; the solid plug then travels 0.24 m. These are prototype proportions, not manufacturing dimensions.
- Digital text moves between timeline frames. Display lettering is flat and emissive; a four-second silent preview demonstrates the readout.
- Twelve actual model views rendered. Inspected front, side, back, top, hero, silent face, hand mode, wrist reading, wrist detail, connector detail, hand detail and wireframe. Side review prompted bringing the chest numeral/calibration marks and leg trim back onto their supporting surfaces.
- GLB exported and reimported in Blender with matching mesh count, triangle count, bone count and dimensions. The first export used the rest pose; export_rest_position_armature=False corrected the mismatch. Mouth morph names survived; no external buffers are required.
- Export preserves the displayed pose and rigged geometry. Blender drivers and scrolling logic are not portable glTF behavior. No game-engine runtime import was tested.
- The previous v001 model and seven supplied image copies match their recorded source hashes.
- Local review links resolve. File hashes are recorded in delivery-manifest.json.

The right arm remains a visual/mechanical concept. Cable payout, live agent connections, iris/quarantine state logic and voice-synchronized mouth animation are future work.
""")
print('Delivery checks passed. Models, views and preview saved.')

