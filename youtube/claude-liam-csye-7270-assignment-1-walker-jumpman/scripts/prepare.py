"""Re-run isolated starter checks; update generated source-pair facts before TTS."""
import hashlib,json,shutil,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
GAME=Path('/Users/bear/Documents/CoWork/bear-textbooks/books/walker/games/walker-jumpman')
ENGINE='/Applications/Godot.app/Contents/MacOS/Godot'
sheet=json.loads((ROOT/'beat_sheet.json').read_text()); ledger=json.loads((ROOT/'gamedev-evidence.json').read_text())
b=sheet['beats'][12]
assert b['beat_id']=='B12'
b['heading']='Watch acceleration and braking'
b['narration_text']='The player moves left to the boundary, accelerates to the right, then stops when the input is released. Opposing keys cancel. Watch the eye follow the chosen direction. This normal-input recording is the visible result of the movement code. Preserve those controls while replacing the art, and separately test jump, landing, and the one-jump contract.'
b['gameplay_take']='controls'; b['shot']['evidence_media']='media/source-controls.mp4';b['shot']['visual_intent']=b['heading'];b['shot']['show']=[{'at':'beat','event':b['heading']}]
b=sheet['beats'][13]; text='\n'.join((GAME/'godot/levels/first_steps.json').read_text().splitlines()[4:10])
b['shot']['remotion']['props'].update(code=text,startLine=5)
b['cue_phrases'][0]['line']=8;b['cue_phrases'][1]['line']=10
for e in ledger['excerpts']:
    if e['beat_id']=='B13':e.update(start_line=5,end_line=10,text=text)
for p in ledger['code_result_pairs']:
    if p['result_beat']=='B12':p.update(observation='Normal Input capture: movement, braking, opposing-key cancellation and facing.',media={'path':'media/source-controls.mp4'})
(ROOT/'beat_sheet.json').write_text(json.dumps(sheet,indent=2)+'\n');(ROOT/'gamedev-evidence.json').write_text(json.dumps(ledger,indent=2)+'\n')
(ROOT/'SCRIPT.md').write_text('# '+sheet['metadata']['title']+'\n\n'+''.join('## '+b['beat_id']+' — '+b['heading']+'\n\n'+(b['narration_text'] or '[Regular stock outro only.]')+'\n\n' for b in sheet['beats']))
for script in ['tests/test_game.gd','tests/test_keyboard.gd']:
    r=subprocess.run([ENGINE,'--headless','--path',str(ROOT/'_project'),'--script','res://'+script,'--fixed-fps','60','--quit-after','2400'],capture_output=True,text=True,timeout=60)
    (ROOT/'evidence'/f'{Path(script).stem}.log').write_text(r.stdout+'\n'+r.stderr)
    assert r.returncode==0 and 'SCRIPT ERROR' not in r.stderr,r.stderr
for p in (ROOT/'evidence').glob('*-*.json'):
    if p.name.startswith(('mechanics-','keyboard-')):
        x=json.loads(p.read_text());assert x['failures']==0,p
        print(p.name, 'failures',x['failures'])
shutil.copy2(ROOT/'scripts/preview.gd',ROOT/'_project/preview.gd')
r=subprocess.run([ENGINE,'--path',str(ROOT/'_project'),'--script','res://preview.gd','--resolution','3840x2160','--position','0,0','--quit-after','500'],capture_output=True,text=True,timeout=60)
(ROOT/'evidence/art-preview.log').write_text(r.stdout+'\n'+r.stderr)
assert r.returncode==0 and 'SCRIPT ERROR' not in r.stderr,r.stderr
for p in ledger['code_result_pairs']:
    media=ROOT/p['media']['path'];assert media.is_file();p['media']['sha256']=hashlib.sha256(media.read_bytes()).hexdigest()
(ROOT/'gamedev-evidence.json').write_text(json.dumps(ledger,indent=2)+'\n')
print('Prepared: source, tests, input recordings, native engine art, pair hashes.')
