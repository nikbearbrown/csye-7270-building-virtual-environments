from pathlib import Path
from PIL import Image, ImageOps, ImageDraw, ImageFont
import base64,io,json,html,platform,hashlib,shutil,ast
R=Path('/Users/bear/Downloads/planet-express-stl-build')
P=R/'planet-express-stl-codex';P.mkdir(exist_ok=True)
F=P.name;BASE='https://github.com/nikbearbrown/csye-7270-building-virtual-environments';RAW=f'{BASE}/raw/main/blender/{F}'
PAGES=f'https://nikbearbrown.github.io/csye-7270-building-virtual-environments/blender/{F}/';FALLBACK=f'https://htmlpreview.github.io/?{RAW}/index.html'
for name in ['planet-express-ship.blend','planet-express-ship.glb','audit.json','verification.json','glb-structure.json','assembly-transforms.json','source-audit.json','components.json']:shutil.copy2(R/name,P/name)
for d in ['scripts','references','renders/web','compare']: (P/d).mkdir(parents=True,exist_ok=True)
for f in (R/'scripts').glob('*.py'):shutil.copy2(f,P/'scripts'/f.name)
shutil.copy2('/Users/bear/Downloads/enterprise-build/scripts/mcp_client.py',P/'scripts/mcp_client.py')
views=[('hero','Forward quarter','The assembled STL kit in turquoise, dark teal, ivory and red.'),('port','Side profile','A side view of the long dorsal fin, engine bell and hull proportions.'),('rear','Rear quarter','The engine nozzle cluster and fitted aft components.'),('top','Top view','The wing arrangement, turret and closed flight configuration.'),('front','Front view','The cockpit frame, projecting portholes and red hull trim.'),('turret','Turret detail','The assembled cannon, blue dome and added antenna.'),('engine','Engine detail','The original kit engine geometry with ivory and graphite materials.')]
comps=[('front',7,'Front comparison','The kit has deeper panel grooves, more prominent portholes and a different cockpit shape.'),('rear',8,'Rear comparison','The kit engine has more nozzle openings, while the vent and trim seating remain approximate.'),('turret',9,'Turret comparison','The kit turret and folded cannon differ from the smooth reference; the thin antenna was added.')]
refs=Path('/Users/bear/Documents/CoWork/bear-textbooks/books/higgsfield/2026-10-18')
ids=['211629_82267214-a49f-416e-b751-12a18cb7d109','211629_f0d92e89-d13a-4435-aa23-eff30bfa3c70','211630_2c6b096b-c4a7-41a3-b7d9-f35b81e88ef8','211630_3ac4f9c9-f830-4f4e-8418-f071e676129f','211630_b1ed22eb-81b5-4550-bd32-46581ca54977','211630_c9d6504f-0512-4625-b6ea-7039aa872558','211630_f7504575-e585-45d0-b8de-03817b335f90','211631_68be5d41-9d04-4f28-930f-697c2d4e30e1','211630_5b01619d-4d2a-4881-b3ba-696db8d08d5d','211631_7976063d-3233-4e78-8f8e-93eb489124d3','211630_05091ed6-e46d-4930-a1a4-758b3cba8c35','211631_c43bffb8-f352-421d-9de6-ec664e432484']
manifest=[]
for n,key in enumerate(ids,1):
 f=refs/f'hf_20261018_{key}.png';dest=P/'references'/f'ref{n:02}.png';shutil.copy2(f,dest);manifest.append({'file':dest.name,'original':f.name,'pixels':Image.open(f).size,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()})
(P/'references/manifest.json').write_text(json.dumps(manifest,indent=2))
source=Path('/Users/bear/Documents/CoWork/bear-textbooks/books/Planet_Express_Ship_-_FUTURAMA')
(P/'source-hashes.json').write_text(json.dumps({f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(source.glob('*.stl'))},indent=2))
for k,_,_ in views:
 shutil.copy2(R/'renders'/f'{k}.png',P/'renders'/f'{k}.png');im=Image.open(R/'renders'/f'{k}.png').convert('RGB');im.thumbnail((1200,1000));im.save(P/'renders/web'/f'{k}.jpg',quality=82)
font=ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc',25)
small=ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc',20)
for k,n,title,caption in comps:
 shutil.copy2(R/'renders'/f'compare-{k}.png',P/'renders'/f'compare-{k}.png')
 canvas=Image.new('RGB',(1800,540),'#edf0ed');draw=ImageDraw.Draw(canvas)
 draw.text((24,20),'REFERENCE / supplied image',font=font,fill='#132c2a');draw.text((920,20),'MODEL / actual Blender render',font=font,fill='#132c2a')
 for f,x in [(P/'references'/f'ref{n:02}.png',20),(P/'renders'/f'compare-{k}.png',920)]:
  im=Image.open(f).convert('RGB');im.thumbnail((860,380),Image.Resampling.LANCZOS);canvas.paste(im,(x+(860-im.width)//2,70+(380-im.height)//2))
 draw.text((24,465),'Approximate camera match; different lighting and background. No generated comparison imagery.',font=small,fill='#132c2a')
 canvas.save(P/'compare'/f'{k}-comparison.jpg',quality=92)
for round_,f in [('round-1','hull-fit'),('round-2','assembly')]:
 dest=P/'compare'/round_;dest.mkdir(exist_ok=True);Image.open(R/'compare'/round_/f'{f}.png').convert('RGB').save(dest/f'{f}.jpg',quality=86)
stat='70 visible meshes · 694,382 triangles · 7 materials · 91.39 × 243.94 × 70.97 mm (X/Y/Z) · Blender 4.2.0 · Codex'
built=f'Builder: Codex, for Nik Bear Brown. Original mesh geometry: GOODesign / GOODesignLabs. Method: scripted STL assembly and material assignment through the Blender MCP add-on socket bridge, with added antenna and mesh lettering; 3 documented comparison rounds. Tools: Blender 4.2.0, MCP add-on bl_info 1.7 / protocol 11, Python {platform.python_version()}, Pillow {Image.__version__}. Build date: 2026-10-20 (America/New_York). Human review: Professor Bear — pending.'
limits='This is a static flight assembly of the supplied kit, with approximate fitting of several parts. The creator confirms that the engraved panel lines are intentional kit details. Its long fins, cockpit and multi-nozzle engine still differ visibly from the smoother reference ship. The physical kit is designed for folding stairs, an opening hangar and a rotating turret; these motions have not been implemented or validated in this digital assembly. The vents and portholes protrude more, and some trim and canopy seams remain imperfect. It is recognizable as Planet Express, but is not an exact match to the reference. Twelve accessory meshes, including unused landing and stand parts, remain hidden in the native scene and are excluded from the GLB. No mechanism rig, animation, collision mesh, LOD or print-fit certification is included. Human review: Professor Bear — pending.'
export='The GLB contains 7 flat PBR materials and no image textures. Panel grooves, emblems and lettering are mesh geometry and survive export. Cameras, studio lights, world and render settings are excluded. GLB units are meters; the native scene displays millimeters. The master transform supports rigid placement only.'
source_text='Original kit: GOODesign / GOODesignLabs, Planet Express Ship – FUTURAMA. Reference images supplied by Nik Bear Brown. This is an assembly study of that kit, not original geometry authored entirely by Codex or an official Futurama asset.'
def data(path):
 im=Image.open(path).convert('RGB');im.thumbnail((1200,1000),Image.Resampling.LANCZOS);buf=io.BytesIO();im.save(buf,format='JPEG',quality=82);return 'data:image/jpeg;base64,'+base64.b64encode(buf.getvalue()).decode()
vdata=[{'key':k,'title':t,'caption':c,'src':data(P/'renders'/f'{k}.png')} for k,t,c in views]
cdata=[{'key':k,'title':t,'caption':c+' Camera framing and lighting differ.','ref':data(P/'references'/f'ref{n:02}.png'),'model':data(P/'renders'/f'compare-{k}.png')} for k,n,t,c in comps]
# Reuse the already exercised gallery layout and controls; content and evidence are specific to this model.
old=Path('/Users/bear/Downloads/enterprise-build/scripts/package_model.py').read_text();tree=ast.parse(old)
css=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='css' for t in n.targets))
css=css.replace('#ffa16e','#79d2bd').replace('#9b451c','#176653')+' select{max-width:100%} .downloads a{overflow-wrap:anywhere}'
controls=old.split("let selected=0;",1)[1].split('</script>',1)[0]
page='''<!doctype html><html lang="en" data-theme="dark"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Planet Express — STL assembly by Codex</title><style>'''+css+'''</style></head><body><main><header><div class="eyebrow">Futurama / GOODesign kit assembly</div><button id="theme" class="theme">Light theme</button><h1>Planet Express</h1><p>The supplied STL kit assembled and colored using your reference images.</p><div class="stats">'''+stat+'''</div></header><nav id="views" class="toolbar" aria-label="Model views"></nav><figure class="stage"><img id="stage" alt=""><figcaption class="caption" aria-live="polite"><strong id="title"></strong><span id="caption"></span></figcaption></figure><div class="toolbar"><button id="prev" aria-label="Previous view">← Previous</button><button id="next" aria-label="Next view">Next →</button><span class="hint">Use ← → keys to navigate actual renders.</span></div><div id="thumbs" class="thumbs"></div><h2>Reference / assembly</h2><p class="hint">Supplied reference at left, actual Blender render at right. Framing and lighting are approximate.</p><div class="toolbar"><label for="comparison">Compare view</label><select id="comparison"></select></div><div class="compare"><figure><img id="reference" alt="Supplied reference image"><figcaption>REFERENCE / supplied image</figcaption></figure><figure><img id="current" alt="Actual Blender render"><figcaption>MODEL / actual Blender render</figcaption></figure></div><p id="compare-caption" class="hint"></p><h2>Film</h2><p id="film">Companion film: coming soon</p><h2>Download and open</h2><div class="downloads"><a href="'''+RAW+'''/planet-express-ship.blend">Blender scene</a><a href="'''+RAW+'''/planet-express-ship.glb">GLB model</a><a href="'''+BASE+'/tree/main/blender/'+F+'''">Complete package</a></div><p>Open the native scene in Blender 4.2 or later. For the GLB choose File → Import → glTF 2.0. Both files were checked independently in Blender 4.2.0.</p><p>'''+export+'''</p><h2>Built by</h2><p>'''+built+'''</p><h2>Limitations and review</h2><p class="note">'''+limits+'''</p><footer>'''+source_text+'''<br>This rendered-view gallery works offline; it is not a live 3D orbit viewer. Download links require connectivity.</footer></main><script>
const FILM_URL="";
const views='''+json.dumps(vdata)+''';
const comparisons='''+json.dumps(cdata)+''';
let selected=0;'''+controls+'''</script></body></html>'''
(P/'index.html').write_text(page)
md=['# Planet Express — STL assembly','','GOODesign’s Planet Express kit assembled and colored by Codex from 26 supplied STL files and 12 reference images.','',stat,'']
for k,t,c in views:md+=['## '+t,'',c,'',f'![{t}](renders/web/{k}.jpg)','',f'[Full-size render](renders/{k}.png)','']
md+=['## Reference comparisons','','Supplied reference pixels at left, actual Blender renders at right. Camera match is approximate; lighting and backgrounds differ. No comparison image was synthesized.','']
for k,n,t,c in comps:md+=['### '+t,'',c,'',f'![{t}](compare/{k}-comparison.jpg)','',f'[Full-size comparison](compare/{k}-comparison.jpg)','']
md+=['## Film','','Companion film: coming soon','<!-- FILM_URL -->','','## Downloads','','| File | Size | Purpose | Download |','|---|---:|---|---|']
for f,d in [('planet-express-ship.blend','Editable scene, materials, lights, cameras and hidden accessories'),('planet-express-ship.glb','Static flight assembly with flat PBR colors'),('index.html','Self-contained offline rendered-view gallery')]:md+=[f'| {f} | {(P/f).stat().st_size/1048576:.2f} MiB | {d} | [Download]({RAW}/{f}) |']
md+=['','## Import','','Open `planet-express-ship.blend` in Blender 4.2 or later. For the GLB use **File → Import → glTF 2.0**. Independent reopening and reimport in Blender 4.2.0 confirmed matching mesh counts, triangle counts, material counts and dimensions.','',export,'','## Viewer','',f'[GitHub Pages viewer]({PAGES}) · [HTML preview fallback]({FALLBACK})','','Download `index.html` to use the gallery offline. It shows rendered views, not live 3D orbit controls. Model downloads require connectivity. GitHub Pages availability is separate from this delivery.','','## Built by','',built,'',source_text,'','[Creator listing](https://thangs.com/designer/GOODesign/3d-model/Planet%20Express%20Ship%20-%20FUTURAMA-1510142) · [Creator assembly video](https://www.youtube.com/watch?v=Jqm8zHlQoqY)','','## Limitations and human review','',limits,'','[Build notes](BUILD_NOTES.md) · [Statistics](audit.json) · [File verification](verification.json)']
(P/'README.md').write_text('\n'.join(md)+'\n')
notes=f'''# Build notes — Planet Express STL assembly

{stat}

## Input and scope

The user supplied 26 GOODesign STL files containing 737,487 triangles and 12 reference images. The source kit is credited to GOODesign / GOODesignLabs. Source file hashes are in `source-hashes.json`; reference original filenames, sizes and hashes are in `references/manifest.json`. Source STL filenames and bounds are recorded in `source-audit.json`. The original STL files are not separately duplicated in this package, but the assembled model contains their geometry.

This is a flight presentation. Printed accessories were not all installed. Twelve unused accessory meshes remain in a hidden native collection and are excluded from export. Native numerical coordinates are millimeters, X lateral, Y length and Z up. The audited visible bounds are 91.3865 × 243.9405 × 70.9728 mm. This is the assembled result, not an assertion of fictional full-size ship dimensions or exact physical kit fit.

The creator's listing and portions of the linked assembly video helped interpret the kit. The video was not followed in its entirety. The user images guided palette and visual review. Their appearance differs from the supplied kit, especially in the paneling, fin proportions and engine.

## Creator assembly notes supplied after the first build

Nik Bear Brown subsequently supplied the creator's written assembly guidance, associated with the same [assembly video](https://youtu.be/Jqm8zHlQoqY). The following is a summary of that source, not a report that these mechanical fits have now been verified in Blender.

The engraved panel lines are deliberate additions by the kit designer. They should be retained when assembling this kit; their difference from the smoother reference images is not itself an assembly error. The intended physical mechanisms are folding front boarding stairs, an opening/closing hangar and a rotating top turret. The delivered Blender/GLB remains static.

| Component | Creator's assembly guidance | Digital assembly implication |
|---|---|---|
| Turret | Glue only around the attachment edges so the turret remains free to rotate. | Preserve a separate turret and establish its pivot before adding rotation controls. Current motion is unverified. |
| Front stairs | Align the pegs and holes before insertion. | Verify hinge alignment against the source meshes before creating a folding animation. |
| Light green hangar outer wall | Check the direction of the parting line shown in the video. | Part orientation needs to be checked by its seam rather than silhouette alone. |
| Side stabilizer rings and wings | Test-fit their alignment before permanent gluing. | Check keyed fit and orientation of each paired ring/wing; visual overlap alone does not prove correct assembly. |
| Tail logo | Match the circle and triangle marks engraved on the base. | Use source registration marks to check logo orientation. |
| Landing gear covers | R/L letters identify sides and face inward when inserted. | Use those marks when installing the currently hidden landing accessories. |

The creator lists silver for windows, landing gear and engine details; leaf green for wings and canopy frame; peak green for the body and stair frame; red for the center line; dark gray for booster, stairs, cannon and cargo frame; and white for the logo frame. The current materials instead follow the supplied turquoise/ivory reference images. Neither palette is evidence that a part is correctly fitted.

Creator-reported completed dimensions are **90 × 254 × 83 mm (X/Y/Z)**, interpreting the pasted `Y m254m` as 254 mm. The largest print part is listed as **51 × 48 × 90 mm**, with an estimated **14 hours** of printing and **146 g** of plastic. These are creator-provided figures, not measurements or print estimates from this Blender scene.

Our measured visible flight assembly remains **91.39 × 243.94 × 70.97 mm**. The difference from the creator's full assembly is unresolved: configuration and part placement both need checking. It would be misleading to force a global scale to match one dimension or assume omitted landing gear explains every discrepancy. No geometry, fitting, animation or new comparison round was completed as part of this documentation update.

## Construction

Blender 4.2.0 ran in a GUI session with the archived MCP for Blender add-on (bl_info 1.7, protocol 11). The Codex tool registry did not expose a Blender tool; `mcp_client.py` used the same localhost:9876 socket protocol as its MCP relay and sent `execute_code` requests. This was a socket bridge to the add-on, not a registered Codex Blender tool.

The binary STL importer deduplicated exact vertex coordinates. Connected components were split and fitted with scripted matrices, recorded in `assembly-transforms.json`. Hull sections, wings, canopy, engine, rings, portholes, vents and logos use source mesh geometry. The cannon's print-oriented halves were folded into an assembled barrel; six resulting degenerate triangles were omitted during triangulation. Vent depth was compressed to 35% along local Z. These are deliberate modifications, not unmodified archival STL copies. Codex added a slender antenna and mesh PLANET EXPRESS lettering around the source emblems. No generative image model or image-to-3D model was used.

The native scene has a master transform, named component collections, seven presentation cameras, three comparison cameras and studio lights. Cycles renders use 64 samples, denoising and AgX. All final PNGs are 1,600 pixels wide. There is no rig or animation. Separate parts intersect or overlap at some joints and have not been boolean-unioned for printing.

## Three documented review rounds

1. **Hull and source orientation.** Imported parts arrived in print orientations. Hull placement and silhouette were checked against the references before fitting accessories. Saved evidence: `compare/round-1/hull-fit.jpg`.
2. **First complete assembly.** Fitted components and compared the assembled quarter view. Review exposed reversed/mirrored emblem orientation, cannon half-shell layout and protruding hardware. Adjusted those transforms, folded the cannon, compressed vent depth and added readable lettering. Saved evidence: `compare/round-2/assembly.jpg`.
3. **Final views and comparisons.** Rendered seven final views and three focused comparison cameras. Inspected the front, aft and turret panels. The assembly is recognizable but not a close surface match: kit panel grooves are pronounced; cockpit and vents are imperfectly seated; portholes protrude; the engine has more openings than the reference. Camera and illumination differences remain. The evidence does not support a claim of exact likeness.

These are the three documented rounds, not a count of every intermediate render experiment. Human acceptance is pending. Reference pixels are preserved; comparison panels only resize/place images and add factual captions.

## Audit and export verification

`audit.json` records 70 visible meshes, 694,382 triangles, 7 used materials and 12 hidden accessory meshes. Dimension measurements use transformed actual vertices, not rotated object bounding boxes. All checked vertex coordinates are finite. `verification.json` records independent native reopening and GLB import in Blender 4.2.0, with equal mesh/triangle/material counts and equivalent bounds after millimeter-to-meter conversion. This validates file readability and export consistency, not mechanical assembly, visual acceptance, manifoldness or animation readiness.

{export}

No image textures, bones or animations are present in the GLB. Its 0.091387 × 0.243940 × 0.070973 meter dimensions match the visible native assembly. Hidden accessories are intentionally omitted. See `glb-structure.json` for the container audit.

## Reproduction

The scripts are the actual files used for this build and contain absolute source/output paths. Edit those paths to match your machine. Start with a new empty Blender 4.2+ scene, and retain separate backups of any valuable scene.

Run `import_inspect.py`, then optional `components.py` and `assemble_draft.py` for inspection. Run `split_parts.py`, `assemble_ship.py`, `finish_render.py`, `export_audit.py`, and `render_comparisons.py` in that order in the same Blender session. Send them with `python3 scripts/mcp_client.py run /absolute/path/to/script.py` against an already running MCP add-on. Alternatively execute the Blender scripts directly inside Blender. Do not split an already split scene again. The source files must be available in their original directory or the paths adjusted.

Run Blender in background with the saved final `.blend` and `--python scripts/verify_files.py` for independent file checks. `package_model.py` makes the documentation, comparison panels and offline gallery using Pillow; it records the original build paths and reused gallery template path. It is a packaging record rather than a standalone portable installer. The kit itself is the original author's work.

## Credit and review

{built}

{source_text}

Creator listing: https://thangs.com/designer/GOODesign/3d-model/Planet%20Express%20Ship%20-%20FUTURAMA-1510142

Assembly video: https://www.youtube.com/watch?v=Jqm8zHlQoqY

## Remaining limitations

{limits}

Companion film: coming soon
<!-- FILM_URL -->
'''
(P/'BUILD_NOTES.md').write_text(notes)
print(json.dumps({'package':str(P),'files':len(list(P.rglob('*'))),'html_bytes':len(page.encode()),'largest_bytes':max(f.stat().st_size for f in P.rglob('*') if f.is_file())},indent=2))
