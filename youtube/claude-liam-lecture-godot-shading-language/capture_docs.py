from pathlib import Path
from playwright.sync_api import sync_playwright
import json,datetime
R=Path(__file__).resolve().parent
urls={
'language':'https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/shading_language.html',
'first2d':'https://docs.godotengine.org/en/stable/tutorials/shaders/your_first_shader/your_first_2d_shader.html',
'first3d':'https://docs.godotengine.org/en/stable/tutorials/shaders/your_first_shader/your_first_3d_shader.html',
'visual':'https://docs.godotengine.org/en/stable/tutorials/shaders/visual_shaders.html',
'compute':'https://docs.godotengine.org/en/stable/tutorials/shaders/compute_shaders.html',
'book':'https://thebookofshaders.com/',
'community':'https://godotshaders.com/',
'migration':'https://docs.godotengine.org/en/stable/tutorials/shaders/converting_glsl_to_godot_shaders.html'}
with sync_playwright() as p:
 b=p.chromium.launch(headless=True)
 page=b.new_page(viewport={'width':1600,'height':900},device_scale_factor=2.4)
 results=[]
 for name,url in urls.items():
  try:
   res=page.goto(url,wait_until='domcontentloaded',timeout=60000)
   page.wait_for_timeout(1400)
   page.screenshot(path=str(R/'captures'/f'docs-{name}.png'))
   (R/'sources'/f'docs-{name}.txt').write_text(page.inner_text('body'))
   results.append({'name':name,'requested_url':url,'resolved_url':page.url,'status':res.status,'date':'2026-10-13','title':page.title()})
   print(name,res.status,page.title(),flush=True)
  except Exception as e: results.append({'name':name,'error':str(e)}); print(name,str(e),flush=True)
 (R/'evidence/web-captures.json').write_text(json.dumps(results,indent=2))
 b.close()
