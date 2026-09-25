"""Conform completed slots early using compile.py's own function and cache key.
Does not assemble, modify the beat sheet, or declare unfinished slots complete.
"""
import importlib.util,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
ART=Path('/Users/bear/Documents/CoWork/bear-textbooks/books/brutalist-art')
spec=importlib.util.spec_from_file_location('compiler',ART/'runtime/scripts/compile.py')
compiler=importlib.util.module_from_spec(spec);spec.loader.exec_module(compiler)
sheet=json.loads((ROOT/'beat_sheet.json').read_text())
clips=ROOT/'clips';clips.mkdir(exist_ok=True);work=clips/'_work';work.mkdir(exist_ok=True)
manifest_path=clips/'manifest.json';manifest=json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
for b in sheet['beats']:
    bid=b['beat_id'];src,status=compiler.resolve_slot(ROOT,bid)
    if src is None: continue
    # Only fully completed Remotion slots carry a render receipt. Manim outputs
    # are copied to the slot only after the renderer exits successfully.
    if b['shot'].get('remotion') and not b['shot']['remotion'].get('rendered'): continue
    d=float(b['actual_duration_s']);shot=b['shot'];fit=sheet['metadata'].get('fit','crop')
    key=(f'L3|3840x2160@24|{fit}|{d:.3f}|{shot.get("motion", "")}|{shot.get("focus", "")}|{shot.get("treatment", "")}|tail:0.000|'+compiler.sha1(src))
    out=clips/f'{bid}.mp4'
    if manifest.get(bid)==key and out.exists():continue
    compiler.compile_clip(ROOT,b,out,3840,2160,24,compiler.find_font(),work,fit=fit,tail_s=0)
    manifest[bid]=key;manifest_path.write_text(json.dumps(manifest,indent=2));print('CONFORMED',bid,flush=True)
