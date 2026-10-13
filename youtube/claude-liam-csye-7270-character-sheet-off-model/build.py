"""lock: measured Kokoro mp3 → frame-padded, −1.5 dBTP limited wav (outro +1.0 s tail); source_report beats keep their own clock.
cues: bind card cues to spoken phrases via mp3/words.json."""
import argparse, json, math, re, subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parent; SHEET=ROOT/'beat_sheet.json'; FPS=30
probe=lambda p: float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(p)],text=True))
load=lambda: json.loads(SHEET.read_text()); save=lambda s: SHEET.write_text(json.dumps(s,indent=1)+'\n')
def lock():
    s=load(); (ROOT/'audio').mkdir(exist_ok=True)
    for b in s['beats']:
        bid=b['beat_id']
        if b.get('kind')=='source_report':
            b['actual_duration_s']=round(probe(ROOT/'media'/f'{bid}.mp4'),3); continue
        src=ROOT/'mp3'/f'beat-{bid}.mp3'; lead=float(b.get('lead_silence_s',0)); tail=1.0 if b.get('kind')=='outro_voice' else 0.3
        nar=probe(src); d=math.ceil((nar+lead+tail)*FPS)/FPS; dst=ROOT/'audio'/f'{bid}-lim.wav'
        subprocess.run(['ffmpeg','-v','error','-y','-i',str(src),'-af',f'adelay={round(lead*1000)}:all=1,apad,aresample=48000,alimiter=limit=0.841:attack=5:release=50:level=false','-t',str(d),'-ar','48000','-ac','2','-c:a','pcm_s16le',str(dst)],check=True)
        b.update(audio_file=f'audio/{bid}-lim.wav',actual_duration_s=d,narration_duration_s=round(nar,3))
        b['shot']['remotion']['props']['durationSeconds']=d
    s['metadata']['audio_locked']=True; s['metadata']['duration_s']=round(sum(b['actual_duration_s'] for b in s['beats']),3); save(s); print('LOCKED',s['metadata']['duration_s'])
def cues():
    s=load(); w=json.loads((ROOT/'mp3/words.json').read_text()); fps=w['fps']; n=lambda t:re.sub('[^a-z0-9]','',t.lower())
    for b in s['beats']:
        if not b.get('cue_phrases'): continue
        toks=w['beats'][b['beat_id']]; out=[]
        for k,c in enumerate(b['cue_phrases']):
            tg=[n(x) for x in c['phrase'].split() if n(x)]; hits=[i for i in range(len(toks)) if [n(t['text']) for t in toks[i:i+len(tg)]]==tg]
            at=toks[hits[0]]['startFrame']/fps+float(b.get('lead_silence_s',0)) if hits else b['actual_duration_s']*(k+.5)/len(b['cue_phrases'])
            if not hits: print('UNMATCHED',b['beat_id'],c['phrase'])
            out.append({'at':round(at,2),'card':c['card']})
        b['shot']['remotion']['props']['cues']=sorted(out,key=lambda x:x['at'])
    save(s); print('cues bound')
if __name__=='__main__':
    a=argparse.ArgumentParser(); a.add_argument('task',choices=['lock','cues']); {'lock':lock,'cues':cues}[a.parse_args().task]()
