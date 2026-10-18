#!/usr/bin/env python3
"""Package finished SEIS v005 renders for an offline review. Never invokes Blender.

SEIS_OUTPUT=/absolute/output/path python3 scripts/package_review.py
Only creates derived JPEGs, copied review references, review.html and README.txt.
The original render PNGs, references and native Blender files are never modified.
"""
from __future__ import annotations
import html
import json
import os
from pathlib import Path
import shutil
from PIL import Image, ImageDraw, ImageFont, ImageOps

SOURCE_V004 = Path('/home/user/Documents/CoWork/bear-textbooks/books/seis-ai-lab/seis-bot/blender/seis-bot-v004-detailed')
REFERENCE_NAMES = (('generated_video_frame_000360-topaz-upscale-4x', 'On-model front'), ('generated_video_frame_000240-topaz-upscale-4x', 'Head and arm profile'), ('generated_video_frame_000000-topaz-upscale-4x', 'Seated full body'), ('generated_video_frame_000120-topaz-upscale-4x', 'Neck and chest'), ('generated_video_frame_000480-topaz-upscale-4x', 'Working hands'), ('generated_video_frame_000600-topaz-upscale-4x', 'Side construction'))
VIEW_SPECS = (
    ('hero','Hero',('hero.png',)),
    ('front','Front',('front.png',)),
    ('side','Side',('side.png',)),
    ('back','Back',('back.png',)),
    ('portrait','Portrait',('portrait.png',)),
    ('torso','Torso',('torso-detail.png','torso.png')),
    ('hands','Hands',('hand-detail.png','hands.png')),
    ('back-detail','Back detail',('back-detail.png',)),
    ('posed','Posed',('thinker.png','posed.png','pose.png')),
)

def esc(s): return html.escape(str(s), quote=True)

def save_web(source: Path, target: Path, maximum: int = 1800):
    """Render a derived JPEG without touching the source PNG."""
    if source.resolve() == target.resolve():
        raise ValueError('Refusing to overwrite an original image')
    target.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(source) as im:
        im=ImageOps.exif_transpose(im)
        if im.mode in ('RGBA','LA') or 'transparency' in im.info:
            rgba=im.convert('RGBA'); bg=Image.new('RGBA',rgba.size,(239,239,236,255)); bg.alpha_composite(rgba); im=bg.convert('RGB')
        else: im=im.convert('RGB')
        im.thumbnail((maximum,maximum),Image.Resampling.LANCZOS)
        im.save(target,'JPEG',quality=92,optimize=True,subsampling=0)
        return im.size

def font(size,root):
    paths=(
        root/'assets'/'Lato-Regular.ttf',
        Path('/home/user/Documents/CoWork/bear-textbooks/books/seis-ai-lab/07-fonts/Lato/Lato-Regular.ttf'),
        Path('/System/Library/Fonts/Supplemental/Arial.ttf'),
    )
    for p in paths:
        if p.exists(): return ImageFont.truetype(str(p),size)
    return ImageFont.load_default()

def contact_sheet(output: Path, views: list[dict]):
    columns=4; tile_w=420; tile_h=520; gap=18; margin=28
    rows=(len(views)+columns-1)//columns
    sheet=Image.new('RGB',(margin*2+columns*tile_w+(columns-1)*gap,margin*2+rows*tile_h+(rows-1)*gap),(17,26,27))
    d=ImageDraw.Draw(sheet); f=font(24,output)
    for i,v in enumerate(views):
        x=margin+(i%columns)*(tile_w+gap); y=margin+(i//columns)*(tile_h+gap)
        with Image.open(output/v['web']) as image:
            image=ImageOps.contain(image.convert('RGB'),(tile_w,tile_h-48),Image.Resampling.LANCZOS)
            sheet.paste(image,(x+(tile_w-image.width)//2,y+(tile_h-48-image.height)//2))
        d.text((x,y+tile_h-37),v['label'],font=f,fill=(236,236,228))
    sheet.save(output/'web'/'contact-sheet.jpg',quality=91,optimize=True)

CSS = r'''
@font-face{font-family:Lato;src:url('assets/Lato-Regular.ttf')}@font-face{font-family:Lato;src:url('assets/Lato-Bold.ttf');font-weight:700}
:root{color-scheme:dark;--bg:#101819;--panel:#192426;--line:#344144;--ink:#f1f0e9;--muted:#b1bdbb;--red:#d43043;--gold:#b8a17a}*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font-family:Lato,Arial,Helvetica,sans-serif;line-height:1.55}a{color:inherit;text-underline-offset:4px}button,a.button{font:inherit}button{cursor:pointer}button:focus-visible,a:focus-visible{outline:3px solid var(--gold);outline-offset:5px}header,main,footer{max-width:1420px;margin:auto;padding-left:32px;padding-right:32px}.mast{display:flex;justify-content:space-between;align-items:center;padding:28px 0;border-bottom:1px solid var(--line);gap:20px}.brand{display:flex;align-items:center;gap:13px;letter-spacing:.12em;text-transform:uppercase;font-size:12px;font-weight:700}.six{display:grid;place-items:center;width:34px;height:34px;color:#fff;background:var(--red);border-radius:7px;font-size:27px;letter-spacing:0;line-height:1}.mast small{color:var(--muted)}.intro{display:grid;grid-template-columns:1.12fr 1fr;gap:60px;align-items:end;padding:58px 0 36px}.eyebrow{text-transform:uppercase;letter-spacing:.17em;color:var(--muted);font-size:11px;font-weight:700;margin:0 0 14px}h1{font-size:clamp(36px,5vw,66px);font-weight:500;letter-spacing:-.035em;line-height:1.07;margin:0}h2{font-size:29px;line-height:1.2;letter-spacing:-.02em;margin:0 0 13px;font-weight:500}p{margin:0 0 16px}.lede{color:#c6cfca;max-width:680px;font-size:17px}.actions{display:flex;gap:12px;flex-wrap:wrap;margin-top:22px}.button{display:inline-flex;align-items:center;justify-content:center;text-decoration:none;border:1px solid var(--line);border-radius:4px;padding:10px 15px;font-size:13px;background:var(--panel)}.button.primary{background:var(--ink);color:var(--bg);border-color:var(--ink)}.gallery{border:1px solid var(--line);background:#151f20}.stage{min-height:570px;height:min(80vh,1030px);background:#535b5a;display:grid;place-items:center;overflow:hidden}.stage img{max-width:100%;height:100%;object-fit:contain;display:block}.gallery-meta{display:flex;align-items:center;justify-content:space-between;gap:18px;padding:17px 20px;border-top:1px solid var(--line)}.gallery-meta p{margin:0;font-size:13px}.gallery-meta a{font-size:12px;color:var(--muted)}.tabs{display:grid;grid-template-columns:repeat(auto-fit,minmax(105px,1fr));gap:1px;background:var(--line);border-top:1px solid var(--line)}.view-tab{border:0;background:var(--panel);color:var(--muted);padding:10px 8px 12px;text-align:left;min-width:0}.view-tab img{width:100%;height:89px;object-fit:cover;object-position:center 35%;filter:saturate(.75);opacity:.67}.view-tab span{display:block;font-size:11px;margin-top:7px;white-space:nowrap}.view-tab[aria-selected=true]{background:#2a3c3e;color:var(--ink);box-shadow:inset 0 -3px var(--red)}.view-tab[aria-selected=true] img{opacity:1;filter:none}.note-grid{display:grid;grid-template-columns:1fr 1fr;gap:70px;padding:48px 0;border-bottom:1px solid var(--line)}.note-grid p{color:var(--muted)}.changes{display:flex;gap:8px;flex-wrap:wrap;margin-top:18px}.changes span{font-size:12px;border:1px solid var(--line);border-radius:30px;padding:6px 11px;color:#dce1da}.section{padding:50px 0;border-bottom:1px solid var(--line)}.section-header{display:flex;align-items:end;justify-content:space-between;gap:24px;margin-bottom:24px}.section-header p{color:var(--muted);max-width:650px;margin:0;font-size:14px}.segmented{display:inline-flex;border:1px solid var(--line);border-radius:4px;overflow:hidden;flex-shrink:0}.segmented button{border:0;border-right:1px solid var(--line);padding:10px 16px;background:var(--panel);color:var(--muted);font-size:12px}.segmented button:last-child{border-right:0}.segmented button[aria-pressed=true]{color:var(--ink);background:#334546}.compare{display:grid;grid-template-columns:1fr 1fr;gap:18px}.compare figure{margin:0;min-width:0;border:1px solid var(--line);background:#515957}.compare .image-box{height:640px;display:flex;align-items:center;justify-content:center}.compare img{display:block;width:100%;height:100%;object-fit:contain}.compare figcaption{padding:14px 16px;font-size:12px;color:#dce2dd;background:var(--panel);border-top:1px solid var(--line)}.ref-picker{display:flex;gap:10px;flex-wrap:wrap;margin-top:15px}.ref-picker button{font-size:12px;background:transparent;border:1px solid var(--line);padding:7px 11px;border-radius:3px;color:var(--muted)}.ref-picker button[aria-pressed=true]{color:var(--ink);border-color:var(--gold)}.sources{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:26px}.sources figure{margin:0}.sources img{width:100%;height:350px;object-fit:cover;object-position:top;border:1px solid var(--line)}.sources figcaption{font-size:11px;color:var(--muted);margin-top:9px}.sources strong{display:block;font-weight:500;color:var(--ink)}details{margin:32px 0 50px;border:1px solid var(--line);padding:18px 22px;background:var(--panel)}summary{cursor:pointer;font-size:14px}details .detail-content{padding-top:20px;color:var(--muted);font-size:13px}.detail-content p{max-width:900px}.file-links{display:flex;flex-wrap:wrap;gap:12px 24px;margin:14px 0}.status{font-family:ui-monospace,monospace;font-size:12px;border-left:2px solid var(--gold);padding-left:12px}footer{padding-bottom:35px;font-size:11px;color:var(--muted)}[hidden]{display:none!important}@media(max-width:1000px){.intro{grid-template-columns:1fr;gap:25px}.tabs{grid-template-columns:repeat(5,minmax(0,1fr))}.compare .image-box{height:510px}.sources img{height:260px}.note-grid{gap:30px}}@media(max-width:680px){header,main,footer{padding-left:17px;padding-right:17px}.mast small{display:none}.intro{padding:35px 0 27px}h1{font-size:39px}.stage{min-height:430px;height:70vh}.tabs{grid-template-columns:repeat(3,minmax(0,1fr))}.view-tab img{height:78px}.note-grid{grid-template-columns:1fr;padding:32px 0;gap:23px}.section{padding:35px 0}.section-header{align-items:start;flex-direction:column}.compare{gap:8px}.compare .image-box{height:380px}.compare figcaption{padding:9px;font-size:10px}.sources{grid-template-columns:repeat(2,1fr)}.sources img{height:280px}.gallery-meta{align-items:start;flex-direction:column;gap:5px}}
'''


def package(output: Path):
    output=output.expanduser().resolve()
    if not output.is_dir(): raise FileNotFoundError(f'Output directory does not exist: {output}')
    views=[]
    for key,label,names in VIEW_SPECS:
        source=next((output/'renders'/name for name in names if (output/'renders'/name).is_file()),None)
        if source is None: continue
        web=Path('web')/(key+'.jpg'); save_web(source,output/web)
        views.append({'key':key,'label':label,'web':web.as_posix(),'full':source.relative_to(output).as_posix()})
    if not views or not any(v['key']=='hero' for v in views):
        raise RuntimeError('Finished hero.png is required. Preview renders are intentionally not published as completed renders.')
    contact_sheet(output,views)
    refs=[];refs_dir=output/'review-references';refs_dir.mkdir(exist_ok=True)
    for name,label in REFERENCE_NAMES:
        dest=refs_dir/(name+'.jpg')
        source=dest if dest.is_file() else Path('/home/user/Downloads')/(name+'.png')
        if not source.is_file(): continue
        if source.resolve()!=dest.resolve():save_web(source,dest)
        refs.append({'key':name,'label':label,'web':dest.relative_to(output).as_posix(),'source_name':name+'.png'})
    previous_source=refs_dir/'previous-v004.jpg'
    if not previous_source.exists():previous_source=SOURCE_V004/'renders'/'web'/'front.jpg'
    previous=None
    if previous_source.is_file():
        dest=refs_dir/'previous-v004.jpg'
        if previous_source.resolve()!=dest.resolve():shutil.copy2(previous_source,dest)
        previous=dest.relative_to(output).as_posix()
    integrity_path=output/'reports'/'integrity.json'
    integrity=None
    if integrity_path.is_file(): integrity=json.loads(integrity_path.read_text())
    native=output/'seis_bot_v005_rebuilt.blend'
    if not native.is_file():
        raise FileNotFoundError('Missing final native model: seis_bot_v005_rebuilt.blend')
    native_href=native.name if native is not None else None
    hero=next(v for v in views if v['key']=='hero');front=next((v for v in views if v['key']=='front'),hero)
    actions=''
    if native_href: actions+=f'<a class="button primary" href="{esc(native_href)}" download>Download Blender model</a>'
    actions+='<a class="button" href="web/contact-sheet.jpg" target="_blank">All views</a>'
    tabs=''.join(f'<button class="view-tab" role="tab" id="tab-{v["key"]}" aria-controls="render-stage" aria-selected="{"true" if v["key"]=="hero" else "false"}" data-view="{v["key"]}"><img src="{esc(v["web"])}" alt="" loading="lazy"><span>{esc(v["label"])}</span></button>' for v in views)
    if refs:
        first=refs[0]
        comparison=f'''<section class="section" aria-labelledby="comparison-title"><div class="section-header"><div><p class="eyebrow">Look closely</p><h2 id="comparison-title">Reference, previous, current.</h2><p>The reference is the target for form and construction. This remains a reconstruction study; the differences are visible here rather than hidden.</p></div><div class="segmented" aria-label="Comparison source"><button data-compare="reference" aria-pressed="true">Reference</button>{'<button data-compare="previous" aria-pressed="false">Previous v004</button>' if previous else ''}</div></div><div class="compare"><figure><a id="comparison-source-link" class="image-box" href="{esc(first['web'])}" target="_blank"><img id="comparison-source" src="{esc(first['web'])}" alt="Reference image: {esc(first['label'])}"></a><figcaption id="comparison-caption">Reference image · {esc(first['label'])}</figcaption></figure><figure><a class="image-box" href="{esc(front['full'])}" target="_blank"><img src="{esc(front['web'])}" alt="Current Blender render, front view" loading="lazy"></a><figcaption>Current Blender render · v005</figcaption></figure></div><div class="ref-picker" id="reference-picker" aria-label="Reference image selection">'''
        comparison+=''.join(f'<button data-reference="{r["key"]}" aria-pressed="{"true" if i==0 else "false"}">{esc(r["label"])}</button>' for i,r in enumerate(refs))
        comparison+='</div></section>'
        sources='''<section class="section"><p class="eyebrow">Source images</p><h2>The approved visual direction.</h2><p class="lede">The newest supplied video frames are the primary references. Originals are preserved; these review copies are reduced JPEGs. These are reference images, not renders of this Blender model.</p><div class="sources">'''
        sources+=''.join(f'<figure><a href="{esc(r["web"])}" target="_blank"><img src="{esc(r["web"])}" alt="Reference image: {esc(r["label"])}" loading="lazy"></a><figcaption><strong>Reference image · {esc(r["label"])}</strong>{esc(r["source_name"])}</figcaption></figure>' for r in refs)
        sources+='</div></section>'
    else: comparison='';sources=''
    report_html=''
    if integrity is not None:
        status=integrity.get('status','Not specified')
        exact=[]
        for field,label in [('evaluated_meshes','evaluated meshes'),('evaluated_triangles','evaluated triangles'),('degenerate_triangle_count','degenerate triangles reported')]:
            if field in integrity: exact.append(f'{esc(integrity[field])} {label}')
        report_html=f'<p class="status">Saved integrity report status: <strong>{esc(status)}</strong>'+('<br>'+ ' · '.join(exact) if exact else '')+'</p><p><a href="reports/integrity.json" target="_blank">Read the saved validation report</a></p>'
    else:
        report_html='<p>No saved integrity report was present when this review was packaged.</p>'
    file_links='<a href="scripts/">Build scripts</a><a href="README.txt">README</a><a href="reports/design-direction.json">Reference direction and remaining differences</a><a href="web/contact-sheet.jpg" target="_blank">Contact sheet</a>'
    if native_href: file_links=f'<a href="{esc(native_href)}" download>{esc(native_href)}</a>'+file_links
    data={'views':views,'refs':refs,'previous':previous}
    data_json=json.dumps(data,ensure_ascii=False).replace('<','\\u003c')
    page=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>SEIS Bot v005 — Reconstruction</title><style>{CSS}</style></head><body>
<header><div class="mast"><div class="brand"><span class="six" aria-hidden="true">6</span>SEIS AI Lab</div><small>Northeastern University · Mascot development</small></div><div class="intro"><div><p class="eyebrow">SEIS Bot / Study 005</p><h1>A closer<br>reconstruction.</h1></div><div><p class="lede">The approved palette remains. The body, armor and face have been rebuilt around the supplied references, with petrol chest plates, a centered Lato six, red optical lenses, enclosing shoulder cups and broad red shin insets.</p><div class="actions">{actions}</div></div></div></header>
<main><section class="gallery" aria-label="Current Blender renders"><div class="stage" id="render-stage" role="tabpanel" aria-labelledby="tab-hero"><img id="render-image" src="{esc(hero['web'])}" alt="Current Blender render: Hero"></div><div class="gallery-meta"><p id="render-caption">Current Blender render · Hero</p><a id="render-full" href="{esc(hero['full'])}" target="_blank">Open full-resolution PNG ↗</a></div><div class="tabs" role="tablist" aria-label="Rendered views">{tabs}</div></section>
<section class="note-grid"><div><p class="eyebrow">What changed</p><h2>Construction before decoration.</h2><p>Major forms were rebuilt: substantial armor encloses the joints; continuous face surfaces replace separate facial pieces; recessed panels and compound curves give the body more coherent volume.</p><div class="changes"><span>Substantial armor</span><span>Continuous mask</span><span>Recessed panels</span><span>Curved shells</span><span>Approved palette</span><span>Lato six</span></div></div><div><p class="eyebrow">How to judge this version</p><h2>Form, then detail.</h2><p>Compare the silhouette, torso depth, shoulder construction, limb proportions and face against the supplied images. Close views expose the panel edges, joints and material response.</p><p>Remaining differences: the shoulder shells are more open, the face more angular, and the abdomen more segmented than in the primary video frames. This remains a reconstruction study.</p></div></section>
{comparison}{sources}
<details><summary>Native files and validation</summary><div class="detail-content"><p>Native Blender model rendered in Cycles, with procedural PBR materials. The FK rig supports posing this study; it is not a production animation rig. The Blender file preserves the editable geometry and material construction.</p><div class="file-links">{file_links}</div>{report_html}</div></details></main>
<footer>SEIS Bot v005 — Reconstruction · Source references and earlier studies are preserved.</footer>
<script type="application/json" id="review-data">{data_json}</script><script>
'use strict';
const data=JSON.parse(document.getElementById('review-data').textContent);
function chooseView(key){{const view=data.views.find(v=>v.key===key);if(!view)return;document.getElementById('render-image').src=view.web;document.getElementById('render-image').alt='Current Blender render: '+view.label;document.getElementById('render-caption').textContent='Current Blender render · '+view.label;document.getElementById('render-full').href=view.full;document.getElementById('render-stage').setAttribute('aria-labelledby','tab-'+view.key);document.querySelectorAll('[data-view]').forEach(b=>b.setAttribute('aria-selected',String(b.dataset.view===key)));}}
document.querySelectorAll('[data-view]').forEach((b,i,all)=>{{b.addEventListener('click',()=>chooseView(b.dataset.view));b.addEventListener('keydown',e=>{{if(e.key==='ArrowRight'||e.key==='ArrowLeft'){{e.preventDefault();const j=(i+(e.key==='ArrowRight'?1:-1)+all.length)%all.length;all[j].focus();chooseView(all[j].dataset.view);}}}});}});
let referenceKey=data.refs.length?data.refs[0].key:null;let comparisonMode='reference';
function updateComparison(){{if(!data.refs.length)return;const r=data.refs.find(r=>r.key===referenceKey)||data.refs[0];const previous=comparisonMode==='previous'&&data.previous;const src=previous?data.previous:r.web;const label=previous?'Previous v004 · Blender render':'Reference image · '+r.label;document.getElementById('comparison-source').src=src;document.getElementById('comparison-source').alt=label;document.getElementById('comparison-source-link').href=src;document.getElementById('comparison-caption').textContent=label;document.getElementById('reference-picker').hidden=!!previous;document.querySelectorAll('[data-compare]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.compare===comparisonMode)));document.querySelectorAll('[data-reference]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.reference===referenceKey)));}}
document.querySelectorAll('[data-compare]').forEach(b=>b.addEventListener('click',()=>{{comparisonMode=b.dataset.compare;updateComparison();}}));document.querySelectorAll('[data-reference]').forEach(b=>b.addEventListener('click',()=>{{referenceKey=b.dataset.reference;comparisonMode='reference';updateComparison();}}));
</script></body></html>'''
    (output/'review.html').write_text(page,encoding='utf-8')
    readme=f'''SEIS BOT v005 — RECONSTRUCTION

This newer v005 folder is a rebuild of the main shapes and construction from
Bear's supplied SEIS Bot references. The earlier v004 folder is preserved.

Open review.html for rendered views and side-by-side comparisons. The reference
images are explicitly labelled and are not presented as Blender renders.

NATIVE FILE
{native_href or '(No .blend file present when review was packaged.)'}
Native Blender / Cycles with procedural PBR materials. An FK posing study,
not a production animation rig. The Lato six is centered on the chest badge. The latest supplied video frames govern the geometry and finish.

REBUILD
From this v005 folder, with Blender available on PATH:

```sh
SEIS_OUTPUT="$(pwd)" Blender --background --python scripts/build.py
```

On the supplied macOS installation:

```sh
SEIS_OUTPUT="$(pwd)" /Applications/Blender.app/Contents/MacOS/Blender --background --python scripts/build.py
```

Render all views, create the separate seated posing study, and audit the native model:

```sh
/Applications/Blender.app/Contents/MacOS/Blender --background seis_bot_v005_rebuilt.blend --python scripts/render_final.py
/Applications/Blender.app/Contents/MacOS/Blender --background seis_bot_v005_rebuilt.blend --python scripts/pose.py
/Applications/Blender.app/Contents/MacOS/Blender --background seis_bot_v005_rebuilt.blend --python scripts/audit.py
```

Repackage finished PNG renders without starting Blender:
Requires Python 3 and Pillow. Blender rendering uses Metal on macOS and CPU
on other systems; adjust the render scripts for a different GPU backend.

```sh
SEIS_OUTPUT="$(pwd)" python3 scripts/package_review.py
```

REFERENCE SOURCES
Original video-frame PNGs are supplied in source-references/:
'''+''.join(f'- {name}.png — {label}\n' for name,label in REFERENCE_NAMES)+f'''
The review uses reduced JPEG copies of the user-supplied on-model video frames. review-references/previous-v004.jpg is the earlier model's front render.
The package script leaves original PNGs, references and .blend files untouched.

CONTENTS
renders/             Native output PNGs
web/                 Derived review JPEGs (maximum 1800 px) and contact sheet
review-references/   Copied reference inspection images and earlier v004 render
scripts/             Reproducible model and packaging code
assets/              Lato fonts and their license
reports/integrity.json  Saved validation report, if produced
reports/geometry-cleanup.json  Topology repair details; pre-repair meshes remain
                       hidden in SOURCE_GEOMETRY inside the native model

VALIDATION
'''+(f'Saved report status at packaging: {integrity.get("status","Not specified")}\nRead reports/integrity.json for exact results and limitations.\n' if integrity is not None else 'No integrity report was present when packaged.\n')
    (output/'README.txt').write_text(readme,encoding='utf-8')
    result={'review':str(output/'review.html'),'views':[v['key'] for v in views],'reference_copies':len(refs),'native_file':native_href,'integrity_status':integrity.get('status') if integrity else None}
    print(json.dumps(result,indent=2))
    return result


def main():
    default=Path(__file__).resolve().parent/'output'
    # Deployed scripts live below the completed artifact root, unlike staging.
    if Path(__file__).resolve().parent.name=='scripts': default=Path(__file__).resolve().parent.parent
    package(Path(os.environ.get('SEIS_OUTPUT',str(default))))

if __name__=='__main__': main()
