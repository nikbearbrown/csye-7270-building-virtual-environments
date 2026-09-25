"""Local QC contacts and complete, word-clock-derived sidecar subtitles."""
import argparse, hashlib, json, math, subprocess, textwrap
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
ROOT=Path(__file__).resolve().parents[1]
def probe(p):
    return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(p)],text=True))
def contacts():
    sheet=json.loads((ROOT/'beat_sheet.json').read_text());frames=[]
    folder=ROOT/'_qc/frames';folder.mkdir(exist_ok=True)
    for b in sheet['beats']:
        bid=b['beat_id']; candidates=[ROOT/'media'/f'{bid}.mp4',ROOT/'manim'/f'{bid}.mp4']; src=next((p for p in candidates if p.exists()),None)
        if not src: continue
        data=probe(src);dur=float(data['format']['duration']); stream=next(s for s in data['streams'] if s['codec_type']=='video')
        if (stream['width'],stream['height'])!=(3840,2160):raise ValueError(f'{bid}: not 4K')
        for part in [.15,.5,.85]:
            out=folder/f'{bid}-{int(part*100)}.png'
            if not out.exists() or out.stat().st_mtime<src.stat().st_mtime:
                subprocess.run(['ffmpeg','-v','error','-y','-ss',str(dur*part),'-i',str(src),'-frames:v','1',str(out)],check=True)
            frames.append((out,bid,part))
    font=ImageFont.truetype('/Users/bear/Library/Fonts/EBGaramond-Regular.ttf',25)
    for start in range(0,len(frames),12):
        canvas=Image.new('RGB',(1800,1480),'#FAF9F5');draw=ImageDraw.Draw(canvas)
        for i,(p,bid,part) in enumerate(frames[start:start+12]):
            im=Image.open(p).convert('RGB');im.thumbnail((580,326));x=(i%3)*600+10;y=(i//3)*370+35;canvas.paste(im,(x,y));draw.text((x,y-30),f'{bid} · {part:.0%}',font=font,fill='#3D3929')
        canvas.save(ROOT/'_qc'/f'contact-{start//12+1:02}.jpg',quality=95)
    print('contacts',len(frames),'samples',flush=True)
def subtitles():
    sheet=json.loads((ROOT/'beat_sheet.json').read_text());words=json.loads((ROOT/'mp3/words.json').read_text());cues=[];offset=0;fps=words.get('fps',sheet['metadata'].get('fps',24))
    def stamp(t):
        m=round(t*1000);h,m=divmod(m,3600000);mins,m=divmod(m,60000);s,ms=divmod(m,1000);return f'{h:02}:{mins:02}:{s:02},{ms:03}'
    for b in sheet['beats']:
        bid=b['beat_id']; seq=words['beats'].get(bid,[]);groups=[];cur=[]
        for w in seq:
            cur.append(w)
            if len(' '.join(x['text'] for x in cur))>58 or (len(cur)>=5 and cur[-1]['text'].endswith(('.', '?','!'))):groups.append(cur);cur=[]
        if cur:groups.append(cur)
        for i,g in enumerate(groups):
            start=g[0]['startFrame']/fps; end=max(g[-1]['endFrame']/fps,start+.3)
            if i+1<len(groups):end=min(end,groups[i+1][0]['startFrame']/fps)
            if end<=start:continue
            end=min(end,b['actual_duration_s']);text=' '.join(w['text'] for w in g)
            cues.append(f'{len(cues)+1}\n{stamp(offset+start)} --> {stamp(offset+end)}\n'+'\n'.join(textwrap.wrap(text,42)))
        offset+=b['actual_duration_s']
    target=ROOT/f"{sheet['metadata']['slug']}.srt";target.write_text('\n\n'.join(cues)+'\n')
    print(target,len(cues),'complete word-aligned cues, no burned captions')
def report():
    sheet=json.loads((ROOT/'beat_sheet.json').read_text());out=ROOT/f"{sheet['metadata']['slug']}.mp4";data=probe(out)
    v=next(s for s in data['streams'] if s['codec_type']=='video');a=next(s for s in data['streams'] if s['codec_type']=='audio')
    assert (v['width'],v['height'])==(3840,2160)
    expected=sum(b['actual_duration_s'] for b in sheet['beats']);actual=float(data['format']['duration']);assert abs(actual-expected)<.15,(actual,expected)
    assert a['codec_name']=='aac'
    dest=ROOT/'exports/landscape'/out.name
    if not dest.exists():dest.symlink_to(Path('../../')/out.name)
    srt=ROOT/f"{sheet['metadata']['slug']}.srt";sub=dest.with_suffix('.srt')
    if not sub.exists():sub.symlink_to(Path('../../')/srt.name)
    receipt={'file':str(dest),'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'duration_s':actual,'video':v,'audio':a,'human_review':'pending','publication':'not published','source':'user course text; identified archived game captures; constructed diagrams labelled'}
    (ROOT/'_qc/master-receipt.json').write_text(json.dumps(receipt,indent=2));print(json.dumps({k:receipt[k] for k in ['file','sha256','duration_s','human_review','publication']}))
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('task',choices=['contacts','subtitles','report']);args=ap.parse_args();globals()[args.task]()
