from pathlib import Path
from playwright.sync_api import sync_playwright
import json
R=Path(__file__).resolve().parent
urls={
'nodes':'getting_started/step_by_step/nodes_and_scenes.html',
'scenes':'tutorials/best_practices/scene_organization.html',
'physics':'tutorials/physics/physics_introduction.html',
'character':'classes/class_characterbody2d.html',
'rigid':'classes/class_rigidbody2d.html',
'oneway':'classes/class_collisionshape2d.html',
'interpolation':'tutorials/physics/interpolation/using_physics_interpolation.html',
'jolt':'tutorials/physics/using_jolt_physics.html',
'geometry':'tutorials/physics/collision_shapes_3d.html',
'migration':'tutorials/migrating/upgrading_to_godot_4.7.html',
'format':'engine_details/file_formats/tscn.html',
'problems':'tutorials/physics/troubleshooting_physics_issues.html'}
results=[]
with sync_playwright() as p:
 b=p.chromium.launch(headless=True)
 page=b.new_page(viewport={'width':1600,'height':900},device_scale_factor=2.4)
 for name,path in urls.items():
  url='https://docs.godotengine.org/en/4.7/'+path
  res=page.goto(url,wait_until='domcontentloaded',timeout=45000)
  page.wait_for_timeout(700)
  if name=='nodes' and 'Performing security verification' in page.inner_text('body'):
   res=page.goto('https://docs.godotengine.org/en/stable/getting_started/step_by_step/nodes_and_scenes.html',wait_until='domcontentloaded')
   page.wait_for_timeout(1200)
  anchors={'character':'class-characterbody2d-property-floor-max-angle','oneway':'class-collisionshape2d-property-one-way-collision-direction','rigid':'class-rigidbody2d-property-continuous-cd','migration':'physics'}
  if name in anchors:
   el=page.locator('#'+anchors[name])
   if el.count(): el.scroll_into_view_if_needed(); page.evaluate('window.scrollBy(0,-120)')
  (R/'sources'/f'docs-{name}.txt').write_text(page.inner_text('body'))
  if name=='migration':
   target=page.locator('p').filter(has_text='WorldBoundaryShape3D').first
   if target.count(): target.scroll_into_view_if_needed(); page.evaluate('window.scrollBy(0,-100)')
  page.screenshot(path=str(R/'captures'/f'docs-{name}.png'))
  results.append({'name':name,'requested_url':url,'resolved_url':page.url,'status':res.status,'title':page.title(),'date':'2026-10-14'})
  print(name,res.status,flush=True)
 b.close()
(R/'evidence/web-captures.json').write_text(json.dumps(results,indent=2))
