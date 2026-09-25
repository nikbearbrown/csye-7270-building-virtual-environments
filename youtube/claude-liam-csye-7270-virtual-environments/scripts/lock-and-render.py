"""Reel-local adapter around the canonical Brutalist render/compile pipeline.
Never edits the shared Remotion registry, and fails if any renderer reports failure.
"""
import argparse, hashlib, importlib.util, json, math, os, re, shutil, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
ART=Path('/Users/bear/Documents/CoWork/bear-textbooks/books/brutalist-art')
GAME=Path('/Users/bear/Documents/CoWork/bear-textbooks/books/walker/games/walker-jumpman')
SHEET=ROOT/'beat_sheet.json'
def run(args):
    subprocess.run(list(map(str,args)),check=True,cwd=ROOT)
def probe(p):
    return float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(p)],text=True).strip())
def lock():
    sheet=json.loads(SHEET.read_text()); fps=24
    if sheet['metadata'].get('audio_locked'): raise SystemExit('Audio already locked; no duplicate padding.')
    for b in sheet['beats']:
        bid=b['beat_id']
        if b['narration_text']:
            src=ROOT/'mp3'/f'beat-{bid}.mp3'
            if not src.exists(): raise SystemExit(f'Missing {src}')
            raw=probe(src); lead=b.get('lead_silence_s',0); d=math.ceil((raw+lead+.2)*fps)/fps
            dst=ROOT/'mp3'/f'locked-{bid}.wav'
            run(['ffmpeg','-v','error','-y','-i',src,'-af',f'adelay={int(lead*1000)}:all=1,apad','-t',f'{d:.6f}','-ar','48000','-ac','1',dst])
            b['audio_file']=str(dst.relative_to(ROOT)); b['actual_duration_s']=round(d,6); b['narration_duration_s']=raw
        else:
            jingles=sorted((ART/'svg/claude/mp3').glob('*.mp3')); seed=sum(map(ord,sheet['metadata']['slug'])); selected=jingles[seed%len(jingles)]; dst=ROOT/'mp3'/'outro.mp3'; shutil.copy2(selected,dst)
            b['audio_file']='mp3/outro.mp3'; b['actual_duration_s']=math.ceil(probe(dst)*fps)/fps; b['outro_jingle_source']=str(selected)
        if b['shot'].get('remotion'): b['shot']['remotion']['props']['durationFrames']=round(b['actual_duration_s']*fps)
    sheet['metadata']['audio_locked']=True; sheet['metadata']['duration_s']=sum(b['actual_duration_s'] for b in sheet['beats']); sheet['metadata']['build_status']='audio locked; visuals pending'
    SHEET.write_text(json.dumps(sheet,indent=2))
    (ROOT/'SHOPPING.md').write_text('# Audio-locked shopping list\n\nTotal measured timeline: %.3f seconds. No external asset shopping is needed.\n\n'%sheet['metadata']['duration_s']+'| Beat | Measured seconds | Missing still | Resolution | Source |\n|---|---:|---|---|---|\n'+''.join(f"| {b['beat_id']} | {b['actual_duration_s']:.3f} | No: reuse archived game evidence | Probe source; native 4K graphic frame | prior-captures.json |\n" for b in sheet['beats'] if b['shot']['lane']=='VOX')+'\nLibrary searched; unrelated stock rejected. Six real game evidence images; no decorative still requests, no paid generation.\n')
    print('LOCKED',sheet['metadata']['duration_s'],flush=True)
def evidence():
    sheet=json.loads(SHEET.read_text()); receipts=[]
    for b in sheet['beats']:
        e=b['shot'].get('evidence')
        if not e: continue
        # Capture receipts establish a one-second menu lead. Select the actual
        # airborne, completion, pause and failure states rather than the menu.
        e['time']={'B03':.25,'B10':1.9,'B14':2.45,'B17':7.5,'B27':2.5,'B30':3.35}[b['beat_id']]
        src=GAME/'youtube/claude-liam-walker-jumpman-gamedev/media'/f"source-{e['take']}.mp4";out=ROOT/'remotion/public'/f"{b['beat_id']}.png"
        run(['ffmpeg','-v','error','-y','-ss',e['time'],'-i',src,'-frames:v','1',out])
        receipts.append({'beat':b['beat_id'],'source':str(src),'frame_at_seconds':e['time'],'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'kind':'archived actual Godot capture with scripted input; no new human test'})
    (ROOT/'evidence/frame-receipts.json').write_text(json.dumps(receipts,indent=2))
    SHEET.write_text(json.dumps(sheet,indent=2))
def remotion(only=None):
    spec=importlib.util.spec_from_file_location('canonical',ART/'runtime/scripts/remotion_scenes.py'); mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    mod.PROJECT=ROOT/'remotion';mod.ENTRY='src/index.tsx';mod.CONSUMERS=ROOT/'remotion/consumers.json'
    os.environ['ART_CHROME']='/Users/bear/Library/Caches/ms-playwright/chromium-1228/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing';os.environ['ART_CHROME_MODE']='chrome-for-testing'
    sheet=json.loads(SHEET.read_text())
    for b in sheet['beats']:
        if not b['shot'].get('remotion') or (only and b['beat_id'] not in only): continue
        print('RENDER',b['beat_id'],flush=True);result=mod.render_beat(ROOT,b,False); print(result,flush=True)
        if result.startswith('FAIL'): raise SystemExit(2)
        mod.stamp(b,ROOT,'local build; see filesystem timestamp');SHEET.write_text(json.dumps(sheet,indent=2))
    mod.update_consumers(sheet,ROOT)
def manim(only=None):
    classes=re.findall(r'class (B\d+_\w+)\(CourseMechanism\)',(ROOT/'scenes.py').read_text())
    for name in classes:
        bid=name.split('_')[0]; dst=ROOT/'manim'/f'{bid}.mp4'
        if dst.exists() or (only and bid not in only): continue
        print('MANIM',name,flush=True)
        run([sys.executable,'-m','manim','render','--disable_caching','-r','3840,2160','--fps','24','--media_dir',ROOT/'_manim','-o',bid,ROOT/'scenes.py',name])
        matches=list((ROOT/'_manim/videos').rglob(f'{bid}.mp4'))
        if len(matches)!=1:raise SystemExit(f'Expected one {bid} render, found {matches}')
        shutil.copy2(matches[0],dst)
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('task',choices=['lock','evidence','remotion','manim']);ap.add_argument('--only',nargs='*');args=ap.parse_args()
    {'lock':lambda:lock(),'evidence':lambda:evidence(),'remotion':lambda:remotion(args.only),'manim':lambda:manim(args.only)}[args.task]()
