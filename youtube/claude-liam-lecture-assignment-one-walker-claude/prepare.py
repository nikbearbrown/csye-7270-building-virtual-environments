"""Fit new narration to its own measured 30-fps clock; reuse gameplay unchanged."""
from pathlib import Path
import json,math,subprocess,shutil,hashlib
R=Path(__file__).resolve().parent
G=R.parents[2]/'walker-claude'
I=G/'youtube/claude-liam-walker-claude-level-one-walkthrough'
S=json.loads((R/'beat_sheet.json').read_text())
run=lambda a: subprocess.run([str(x) for x in a],check=True)
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
(R/'audio').mkdir(exist_ok=True)
for b in S['beats']:
    if b['lane']=='gameplay': continue
    bid=b['beat_id']; raw=R/'mp3'/f'beat-{bid}.mp3'
    length=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(raw)],text=True))
    lead=float(b.get('lead_silence_s',0)); tail=float(b.get('tail_silence_s',.25))
    duration=math.ceil((length+lead+tail)*30)/30
    run(['ffmpeg','-y','-v','error','-i',raw,'-af',f'adelay={round(lead*1000)}:all=1,apad','-t',str(duration),'-ar','48000','-ac','2','-c:a','pcm_s16le',R/'audio'/f'{bid}.wav'])
    b.update(audio_file=f'audio/{bid}.wav',actual_duration_s=duration,render_duration_s=duration)
    if 'remotion' in b['shot']:b['shot']['remotion']['props']['durationSeconds']=duration
(R/'beat_sheet.json').write_text(json.dumps(S,indent=2,ensure_ascii=False)+'\n')
# Native-input captures, inputs and coverage remain independent copied evidence.
(R/'capture').mkdir(exist_ok=True); (R/'evidence').mkdir(exist_ok=True)
C=json.loads((I/'coverage.json').read_text())
mapping={'B02':'B36','B03':'B22','B05':'B19','B06':'B23'}
for entry in C['captures'].values():
    for key in ['path','input_log']:
        source=I/entry[key]; target=R/entry[key]
        shutil.copy2(source,target)
        assert sha(source)==sha(target)
for f in C['features']:
    for e in f['evidence']:e['beat_id']=mapping[e['beat_id']]
(R/'coverage.json').write_text(json.dumps(C,indent=2)+'\n')
shutil.copy2(I/'CAPTURE.md',R/'CAPTURE.md')
timings=json.loads((I/'evidence/slot-timing.json').read_text())
(R/'evidence/slot-timing.json').write_text(json.dumps({mapping[k]:v for k,v in timings.items()},indent=2)+'\n')
receipt={'source_reel':str(I),'game_source_revision':S['metadata']['game_source_revision'],'game_build_id':C['game']['build_id'],'slots':{mapping[k]:{'media_sha256':sha(R/'media'/f'{mapping[k]}.mp4'),'input_media_sha256':sha(I/'media'/f'{k}.mp4'),'audio_sha256':sha(R/'audio'/f'{mapping[k]}.wav')} for k in mapping}}
(R/'evidence/input-film-reuse.json').write_text(json.dumps(receipt,indent=2)+'\n')
print('Measured duration:',sum(b['actual_duration_s'] for b in S['beats']))
print('Gameplay media and audio copied byte-for-byte; action speed and existing hold labels preserved.')
