from pathlib import Path
from PIL import Image,ImageOps
import io,base64,json,html,platform,sys
ROOT=Path('/Users/bear/Downloads/enterprise-build')
FOLDER='enterprise-ncc-1701-codex'
BASE='https://github.com/nikbearbrown/csye-7270-building-virtual-environments'
RAW=f'{BASE}/raw/main/blender/{FOLDER}'
PAGES=f'https://nikbearbrown.github.io/csye-7270-building-virtual-environments/blender/{FOLDER}/'
FALLBACK=f'https://htmlpreview.github.io/?{RAW}/index.html'
a=json.loads((ROOT/'audit.json').read_text())
stats=f"{a['mesh_objects']} meshes · {a['triangles']:,} triangles · {a['materials']} materials · 128.0 × 290.3 × 77.192 m (X/Y/Z) · Blender {a['blender']} · Codex"
views=[('hero','Forward quarter','The saucer, copper deflector and red-orange Bussard collectors in a studio overview.'),('side','Side profile','Orthographic side view for checking the swept neck, hull taper and nacelle placement.'),('front','Forward elevation','Orthographic front view showing the saucer dish and diagonal nacelle supports.'),('top','Dorsal plan','Orthographic plan with the bow at left, matching the supplied drawing orientation.'),('aft','Aft quarter','Rear view of the nacelle endcaps, intercoolers, impulse exhaust and shuttle bay.'),('underside','Ventral quarter','The saucer underside, sensor dome, engineering hull and deflector assembly.'),('detail','Saucer detail','Curved registry lettering, bridge decks, navigation lights and modeled panel lines.')]
comp=[('side','Side profile comparison','The supplied high-resolution Constitution-class sheet is at left; the actual model render is at right. The class-sheet registry is NCC-1700; the model is marked NCC-1701.'),('front','Forward elevation comparison','The forward-view crop from the supplied low-resolution sheet is at left. Framing and source quality limit exact matching.'),('top','Dorsal plan comparison','The top-view crop from the supplied poster is at left; the actual orthographic render is at right.')]
limitations='A blueprint-based exterior reconstruction, not a screen-exact studio miniature. Overall proportions were estimated from the supplied views; the 290.3 m length is the chosen working scale, not a verified canonical dimension. Small windows, pennants, grille slats, colors and surface finish are interpretations. The bridge is simplified, the engineering stern is smoother than the plan, and nacelle tail/intercooler details differ. No deck interiors, animated mechanisms, LODs, collision mesh or production rig are included. Separate components are parented to a master transform for rigid movement; this does not constitute animation validation. Human review: Professor Bear — pending.'
built=f'Builder: Codex. Created for Nik Bear Brown. Method: scripted Blender mesh construction through the MCP for Blender add-on socket bridge; 3 documented visual comparison/review rounds. Tools: Blender 4.2.0, MCP add-on bl_info 1.7 / protocol 11 (local archived add-on), Python {platform.python_version()} for packaging, Pillow {Image.__version__}. Build date: 2026-10-20 (America/New_York). Human review: Professor Bear — pending.'
md=['# U.S.S. Enterprise — NCC-1701','', 'Classic Constitution-class exterior reconstructed from supplied plans, with Enterprise markings.', '',stats,'']
for k,title,cap in views:md += ['## '+title,'',cap,'',f'![{title}](renders/web/{k}.jpg)','',f'[Full-size render](renders/{k}.png)','']
md+=['## Reference comparisons','','The panels contain supplied reference pixels and actual Blender renders. Lighting is interpretive and framing is approximate. No comparison evidence was generated with an image model.','']
for k,title,cap in comp:md+=['### '+title,'',cap,'',f'![{title}](compare/{k}-comparison.jpg)','',f'[Full-size comparison](compare/{k}-comparison.jpg)','']
md+=['## Film','','Companion film: coming soon','<!-- FILM_URL -->','','## Downloads','','| File | Size | Purpose | Download |','|---|---:|---|---|']
for f,desc in [('enterprise-ncc-1701.blend','Full editable scene, cameras, lights and materials'),('enterprise-ncc-1701.glb','Model with flat PBR colors and modeled details; no image textures'),('index.html','Self-contained offline image review viewer')]:
    size=f'{(ROOT/f).stat().st_size/1048576:.2f} MiB' if (ROOT/f).exists() else 'see file'
    md+=[f'| {f} | {size} | {desc} | [Download]({RAW}/{f}) |']
md+=['','## Import','','Open `enterprise-ncc-1701.blend` in Blender 4.2 or later. Reopening was verified in Blender 4.2.0. For the GLB, use **File → Import → glTF 2.0**. The GLB was reimported in Blender 4.2.0 with matching mesh count, triangle count, materials and bounds.','','The GLB has **flat PBR material colors and no image textures**. Panel seams, windows, grilles and markings are geometry and survive export. Studio lighting, world, cameras and Blender render settings are excluded. Emissive strength uses `KHR_materials_emissive_strength`, so its appearance depends on the viewer.','','## Viewer','',f'[GitHub Pages viewer]({PAGES}) · [HTML preview fallback]({FALLBACK})','','The single HTML file works offline after download. External model/film links need connectivity. GitHub Pages availability is separate from the file delivery. The viewer navigates rendered views; it is not a live 3D orbit viewer.','','## Built by','',built,'','Reference provenance: drawings supplied by Nik Bear Brown. The main side sheet credits Franz Joseph Designs and ©1973 Paramount Pictures Corporation. Star Trek and the Enterprise are referenced here for a course modeling study; this is not an official asset.','','## Limitations and human review','',limitations,'','[Build notes and reproduction](BUILD_NOTES.md) · [Audited statistics](audit.json) · [File validation](verification.json)']
# viewer images

def data(path,crop=None,width=1200):
    im=Image.open(path).convert('RGB')
    if crop:im=im.crop(crop)
    im.thumbnail((width,1000),Image.Resampling.LANCZOS);buf=io.BytesIO();im.save(buf,format='JPEG',quality=82)
    return 'data:image/jpeg;base64,'+base64.b64encode(buf.getvalue()).decode()
vdata=[{'key':k,'title':title,'caption':cap,'src':data(ROOT/'renders'/f'{k}.png')} for k,title,cap in views]
refs=[('side','constitution-side-supplied.jpg',None),('front','constitution-elevations.jpg',(14,3,214,124)),('top','constitution-general-plan.jpg',(10,139,442,328))]
cdata=[]
for (k,f,crop),(_,title,cap) in zip(refs,comp):cdata.append({'key':k,'title':title,'caption':cap,'ref':data(ROOT/'references'/f,crop),'model':next(v['src'] for v in vdata if v['key']==k)})
css='''*{box-sizing:border-box} :root{--bg:#0c131a;--card:#16212b;--fg:#e9edf1;--muted:#a9b8c3;--line:#34434f;--accent:#ffa16e} [data-theme=light]{--bg:#f4f2eb;--card:#fff;--fg:#172430;--muted:#566673;--line:#cbd2d6;--accent:#9b451c} body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.55 system-ui,-apple-system,sans-serif}main{max-width:1220px;margin:auto;padding:42px 24px 70px}header{position:relative;border-bottom:1px solid var(--line);padding-bottom:26px}h1{font-size:clamp(30px,5vw,57px);font-weight:550;letter-spacing:-2px;line-height:1.08;margin:14px 0}h2{font-size:26px;margin:44px 0 14px}h3{font-size:18px}.eyebrow,.stats{font:12px/1.7 ui-monospace,monospace;letter-spacing:.6px;color:var(--muted)}.eyebrow{color:var(--accent);text-transform:uppercase}p{max-width:940px}.toolbar{display:flex;gap:8px;flex-wrap:wrap;margin:22px 0 14px}button,select{border:1px solid var(--line);border-radius:5px;background:var(--card);color:var(--fg);padding:10px 14px;font:inherit;cursor:pointer}button[aria-pressed=true]{color:var(--bg);background:var(--accent);border-color:var(--accent)}button:hover,a:hover{filter:brightness(1.18)}button:focus-visible,select:focus-visible,a:focus-visible{outline:3px solid var(--accent);outline-offset:3px}.theme{position:absolute;right:0;top:0;font-size:13px}.stage{margin:0;background:#10171e;border:1px solid var(--line);border-radius:8px;overflow:hidden}.stage img{display:block;width:100%;height:min(62vw,650px);object-fit:contain}.caption{padding:17px 20px;background:var(--card)}.caption strong{display:block;margin-bottom:3px}.caption span,.hint{color:var(--muted);font-size:14px}.thumbs{display:grid;grid-template-columns:repeat(7,1fr);gap:8px;margin-top:13px}.thumbs button{padding:0;overflow:hidden}.thumbs img{width:100%;height:80px;display:block;object-fit:cover}.thumbs span{font-size:11px;display:block;padding:5px}.compare{display:grid;grid-template-columns:1fr 1fr;gap:18px}.compare figure{margin:0;border:1px solid var(--line);border-radius:8px;overflow:hidden;background:var(--card)}.compare img{width:100%;height:350px;object-fit:contain;background:#10171e;display:block}.compare figure:first-child img{background:#f6f5f1}.compare figcaption{padding:13px;font-size:13px;color:var(--muted)}a{color:var(--accent);text-underline-offset:3px}.downloads{display:flex;gap:12px;flex-wrap:wrap}.downloads a{padding:10px 16px;border:1px solid var(--line);border-radius:5px;text-decoration:none}.note{padding:20px;border-left:3px solid var(--accent);background:var(--card)}footer{margin-top:40px;border-top:1px solid var(--line);padding-top:22px;color:var(--muted);font-size:13px}@media(max-width:620px){main{padding:24px 16px 44px}h1{letter-spacing:-1px}.theme{position:static;margin-top:14px}.toolbar button{font-size:13px;padding:8px}.thumbs{grid-template-columns:repeat(4,1fr)}.thumbs img{height:65px}.compare{grid-template-columns:1fr}.compare img{height:260px}.stage img{height:65vw}.stats{font-size:11px}}'''
page='''<!doctype html><html lang="en" data-theme="dark"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>U.S.S. Enterprise NCC-1701 — Codex</title><style>'''+css+'''</style></head><body><main><header><div class="eyebrow">Constitution class / blueprint reconstruction</div><button class="theme" id="theme">Light theme</button><h1>U.S.S. Enterprise<br>NCC-1701</h1><p>A classic starship exterior built from the supplied drawings, through Blender MCP.</p><div class="stats">'''+html.escape(stats)+'''</div></header><nav class="toolbar" id="views" aria-label="Model views"></nav><figure class="stage"><img id="stage" alt=""><figcaption class="caption" aria-live="polite"><strong id="title"></strong><span id="caption"></span></figcaption></figure><div class="toolbar"><button id="prev" aria-label="Previous view">← Previous</button><button id="next" aria-label="Next view">Next →</button><span class="hint">Use ← → keys to move through actual renders.</span></div><div class="thumbs" id="thumbs"></div><h2>Reference / reconstruction</h2><p class="hint">Supplied drawing pixels alongside actual model renders. Framing is approximate; colors and lighting are interpreted.</p><div class="toolbar"><label for="comparison">Compare view </label><select id="comparison"></select></div><div class="compare"><figure><img id="reference" alt="Supplied reference drawing"><figcaption>REFERENCE / supplied drawing</figcaption></figure><figure><img id="current" alt="Actual Blender render"><figcaption>CURRENT / actual Blender render</figcaption></figure></div><p id="compare-caption" class="hint"></p><h2>Film</h2><p id="film">Companion film: coming soon</p><h2>Download and open</h2><div class="downloads"><a href="'''+RAW+'''/enterprise-ncc-1701.blend">Blender scene</a><a href="'''+RAW+'''/enterprise-ncc-1701.glb">GLB model</a><a href="'''+BASE+f'/tree/main/blender/{FOLDER}'+'''">Complete package</a></div><p>Open the native scene in Blender 4.2 or later, or choose File → Import → glTF 2.0 for the GLB. Both files were checked in Blender 4.2.0.</p><p class="hint">GLB: 12 flat PBR materials, no image textures. Modeled panel seams and markings survive export. Studio lights, cameras and world do not. The master transform supports rigid movement; no animation is supplied.</p><h2>Built by</h2><p>'''+html.escape(built)+'''</p><h2>Limitations and review</h2><p class="note">'''+html.escape(limitations)+'''</p><footer>Drawings supplied by Nik Bear Brown. The main sheet credits Franz Joseph Designs and ©1973 Paramount Pictures Corporation. Course modeling study; not an official Star Trek asset.<br>This gallery works offline. Download and film links require connectivity.</footer></main><script>
const FILM_URL = "";
const views='''+json.dumps(vdata)+''';
const comparisons='''+json.dumps(cdata)+''';
let selected=0;
const $=id=>document.getElementById(id);
views.forEach((v,i)=>{const b=document.createElement('button');b.textContent=v.title;b.onclick=()=>show(i);$('views').append(b);const t=document.createElement('button');t.setAttribute('aria-label',v.title);t.innerHTML='<img alt="" src="'+v.src+'"><span>'+v.title+'</span>';t.onclick=()=>show(i);$('thumbs').append(t);});
function show(i){selected=(i+views.length)%views.length;const v=views[selected];$('stage').src=v.src;$('stage').alt=v.title;$('title').textContent=v.title;$('caption').textContent=v.caption;[...$('views').children].forEach((b,j)=>b.setAttribute('aria-pressed',j===selected));[...$('thumbs').children].forEach((b,j)=>b.setAttribute('aria-pressed',j===selected));}
$('prev').onclick=()=>show(selected-1);$('next').onclick=()=>show(selected+1);
document.addEventListener('keydown',e=>{if(['SELECT','INPUT','TEXTAREA'].includes(e.target.tagName))return;if(e.key==='ArrowRight'){e.preventDefault();show(selected+1)}if(e.key==='ArrowLeft'){e.preventDefault();show(selected-1)}});
$('theme').onclick=()=>{const light=document.documentElement.dataset.theme==='dark';document.documentElement.dataset.theme=light?'light':'dark';$('theme').textContent=light?'Dark theme':'Light theme';};
comparisons.forEach((c,i)=>{const o=document.createElement('option');o.value=i;o.textContent=c.title;$('comparison').append(o)});
function compare(i){const c=comparisons[i];$('reference').src=c.ref;$('current').src=c.model;$('compare-caption').textContent=c.caption;}
$('comparison').onchange=e=>compare(Number(e.target.value));
if(FILM_URL){const a=document.createElement('a');a.href=FILM_URL;a.textContent='Watch companion film';$('film').replaceChildren(a)}show(0);compare(0);
</script></body></html>'''
(ROOT/'index.html').write_text(page)
# HTML exists now so its download size is accurate.
md=[line.replace('| index.html | see file |',f'| index.html | {(ROOT/"index.html").stat().st_size/1048576:.2f} MiB |') for line in md]
(ROOT/'README.md').write_text('\n'.join(md)+'\n')
notes=f'''# Build notes — Enterprise NCC-1701

{stats}

## Source and scope

The user requested a Starship Enterprise through Blender MCP from drawings in the Star Trek folder, then supplied enhanced images. The high-resolution `0001-topaz-denoise.jpg` (12,032 × 3,526 px) was the most useful side reference; its source pixels are preserved as `references/constitution-side-supplied.jpg`. The heavily enhanced 4× small originals were easier to view but contained distorted labels and details. Original general plan, front/rear elevation and nacelle drawings were used for cross-checking. The class drawing says NCC-1700; Enterprise is listed as NCC-1701 on the same sheet. No source mesh, image-to-3D asset or generated picture was used.

Scope: a detailed exterior reconstruction. Interior deck plans informed the overall arrangement but no interiors were built. Palette and illumination are interpretations of monochrome plans. Native units are metres, +Y aft, +Z up, X lateral. Dimensions are chosen reconstruction scale; they are not a canonical-size claim.

## Construction and MCP evidence

Blender 4.2.0 ran in an isolated GUI session. `scripts/start_mcp.py` loaded the pre-existing archived MCP for Blender add-on, bl_info version 1.7, protocol 11. `scripts/mcp_client.py` sent `execute_code` requests through the add-on's localhost port 9876. The Codex tool registry did not expose a Blender tool, so the socket bridge normally used by the stdio MCP relay was called directly. This is disclosed rather than claiming a registered Codex MCP tool.

`build_enterprise.py` makes a contoured revolved saucer, sloped bridge decks, a swept neck, a variable-radius engineering hull loft, diagonal support pylons, longitudinal nacelle shells, hemispherical collectors, copper dish, vents, grilles, segmented hangar doors, windows and registry meshes. Text was converted to mesh and conformed to the saucer surface. Small details and seams are mesh geometry. Pylons overlap the hull shell at their roots; separate components are not boolean-unioned into a single printable solid. Mesh normals were recalculated before export.

The scene includes seven orthographic cameras, four area lights, a world, named components, and a master empty for rigid ship motion. No animation, bones, collision shapes or LODs exist. Render engine: Cycles, 48 samples, denoising, AgX. Final renders are 1,600 px wide; aspect ratios vary by view.

## Auditable comparison rounds

1. **Initial side/front/hero check.** The main class silhouette was compared to the supplied side and forward elevations. Saucer text partly entered the sloped hull and the collector mesh intersected the pale underlying front shell. Evidence: `compare/round-1/`. Fixed by projecting registry vertices onto the hull surface, removing the overlapping nacelle nose, recalculating normals and adjusting the main camera.
2. **Corrected views and close-ups.** Checked the corrected side/top/front silhouettes and the detailed quarter views. The saucer text and collectors were improved. Close-up review exposed pylon roots sitting slightly above the tapered secondary hull and bridge windows sitting inside the deck shell. Evidence: `compare/round-2/`. Moved pylon roots into the hull, lowered the neck base, and moved bridge panes to the visible surface.
3. **Final exterior review.** Inspected actual final views and side/front/top comparison panels. Pylon connections are continuous at the visible surface, registry is readable and the collector overlap is removed. Overall arrangement is recognizable and follows the main class proportions; it is not a film-miniature match. The bridge and stern profile remain simplified; thin windows and some applied pennants are not exact plan tracings. Human visual acceptance is still pending.

Comparisons are photographic composites of supplied drawing pixels at left and real Blender renders at right. No synthetic evidence. Orthographic projections align view directions; framing and lighting are not identical. Front-reference source is only 450 × 132 px and is visibly enlarged. The side panel preserves the whole sheet, including labels.

## Audit and validation

Read `audit.json`, `glb-structure.json` and `verification.json`. The native scene was reopened independently in Blender 4.2.0. The GLB was then imported into an empty Blender 4.2.0 scene. Mesh count, triangle count, used materials and bounds match; all inspected vertex coordinates are finite. This validates file readability and geometric export consistency, not visual fidelity or animation readiness.

GLB is glTF 2.0, 270 mesh objects, {a['triangles']:,} triangles, 12 materials, 0 image textures, 0 animations. Geometry carries panel lines, grilles, windows and text. PBR flat colors, roughness, metalness and emission export; `KHR_materials_emissive_strength` is used. Scene cameras, studio lights, world and render settings are excluded. Engine lighting can change its appearance.

## Reproduce

1. Use Blender 4.2+ and an MCP for Blender add-on session listening on localhost:9876. The startup helper records the add-on path used on the build machine; change that path to your installed add-on if needed. Do not load a valuable unsaved scene: the builder clears its active scene.
2. In Blender, set `os.environ['ENTERPRISE_OUTPUT']` to the output directory. Execute `scripts/build_enterprise.py` through `mcp_client.py run /absolute/path/to/build_enterprise.py`. The same file can be run with Blender's `--python` command for reproduction without the MCP transport.
3. Execute `scripts/render_views.py` in the same scene. `ENTERPRISE_VIEWS`, `ENTERPRISE_RESOLUTION` and `ENTERPRISE_SAMPLES` can select view names, percentage and samples. Defaults are all seven views, 100%, and 32 samples; the delivered final run used 48.
4. `scripts/verify_files.py` reopens/imports files when invoked by Blender, and `make_comparisons.py` plus `package_model.py` assemble evidence and documentation with Pillow. Packaging paths reflect this actual build and may be changed for another machine.

## Credit, date and review

{built}

Plans: supplied by Nik Bear Brown; the main sheet credits Franz Joseph Designs and ©1973 Paramount Pictures Corporation. Fan/course reconstruction, not an official asset.

## Remaining limitations

{limitations}

Companion film: coming soon
<!-- FILM_URL -->
'''
(ROOT/'BUILD_NOTES.md').write_text(notes)
print(json.dumps({'html_bytes':(ROOT/'index.html').stat().st_size,'python':platform.python_version(),'pillow':Image.__version__},indent=2))
