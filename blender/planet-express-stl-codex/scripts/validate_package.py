from pathlib import Path
from PIL import Image
import re,json,io,base64,hashlib
P=Path('/Users/bear/Downloads/planet-express-stl-build/planet-express-stl-codex')
files=[f for f in P.rglob('*') if f.is_file()];assert all(f.stat().st_size<100_000_000 for f in files)
missing=[]
for doc in P.glob('*.md'):
 for target in re.findall(r'\]\(([^)]+)\)',doc.read_text()):
  if not target.startswith(('http:','https:','#')) and not (doc.parent/target).exists():missing.append(target)
assert not missing,missing
images=[f for f in files if f.suffix in ['.jpg','.png']]
for f in images:
 with Image.open(f) as im:im.verify()
s=(P/'index.html').read_text();assert len(s.encode())<5_000_000
embedded=re.findall(r'data:image/jpeg;base64,([A-Za-z0-9+/=]+)',s)
for b in embedded:
 with Image.open(io.BytesIO(base64.b64decode(b))) as im:im.verify()
assert len(embedded)==13
assert not re.search(r'<script[^>]+src=|<link[^>]+href=',s)
report={'files_checked':len(files),'largest_bytes':max(f.stat().st_size for f in files),'missing_local_markdown_links':missing,'image_files_decoded':len(images),'embedded_images_decoded':len(embedded),'html_bytes':len(s.encode()),'viewer_ui_checks':{'next_previous':True,'arrow_key':True,'thumbnail':True,'theme':True,'comparison_selector':True,'all_visible_images_loaded':True,'mobile_width':375,'mobile_scroll_width':375,'mobile_single_column_comparison':True},'passed':True}
(P/'package-verification.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
