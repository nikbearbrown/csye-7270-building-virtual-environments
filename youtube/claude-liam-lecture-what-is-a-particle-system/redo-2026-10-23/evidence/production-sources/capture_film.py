from pathlib import Path
import subprocess,time,json,sys,math,shutil
work=Path(sys.argv[1]).resolve();reel=Path(sys.argv[2]).resolve();window=sys.argv[3]
sheet=json.loads((reel/'beat_sheet.json').read_text());beats=[b for b in sheet['beats'] if b.get('capture_actions')]
cap=reel/'captures';cap.mkdir(exist_ok=True)
raw=cap/'native-editor-take-01.mov'
if raw.exists():raise SystemExit('Refusing to overwrite existing take')
request=work/'.lecture/request.json';log=work/'.lecture/actions.jsonl'
total=sum(math.ceil(float(b['actual_duration_s'])*30)/30 for b in beats)
proc=subprocess.Popen(['/usr/sbin/screencapture','-v','-V'+str(math.ceil(total+3)),'-l'+window,str(raw)],stdout=(cap/'capture.stdout').open('w'),stderr=(cap/'capture.stderr').open('w'))
t0=time.monotonic();start=1.0;timeline=[];rid=int(time.time())
for beat in beats:
 duration=math.ceil(float(beat['actual_duration_s'])*30)/30
 print(beat['beat_id'],round(start,3),round(duration,3),flush=True)
 record={'beat_id':beat['beat_id'],'start_s':start,'duration_s':duration,'actions':[]}
 for action in beat['capture_actions']:
  when=start+action.get('at',0.05)
  time.sleep(max(0,when-(time.monotonic()-t0)))
  rid+=1;req={k:v for k,v in action.items() if k!='at'};req.update(id=rid,label=action.get('label',beat['act']))
  request.write_text(json.dumps(req));sent=time.monotonic()-t0
  deadline=time.monotonic()+3
  ack=None
  while time.monotonic()<deadline:
   if log.exists():
    for line in reversed(log.read_text().splitlines()[-12:]):
     try:r=json.loads(line)
     except:continue
     if r.get('request',{}).get('id')==rid:ack=r;break
   if ack:break
   time.sleep(.05)
  if not ack or 'error' in ack.get('result',{}):
   (cap/'failed-action.json').write_text(json.dumps({'request':req,'ack':ack},indent=2))
   proc.send_signal(2);proc.wait(timeout=15)
   raise SystemExit('Editor action failed: '+str(req))
  record['actions'].append({'sent_at_s':sent,'ack_at_s':time.monotonic()-t0,'receipt':ack})
 timeline.append(record);(cap/'timeline.json').write_text(json.dumps(timeline,indent=2))
 start+=duration
proc.wait(timeout=max(10,math.ceil(total+8-(time.monotonic()-t0))))
if proc.returncode:raise SystemExit('native capture failed '+str(proc.returncode))
shutil.copy2(log,cap/'editor-actions.jsonl')
print('CAPTURE COMPLETE',raw,total,flush=True)
