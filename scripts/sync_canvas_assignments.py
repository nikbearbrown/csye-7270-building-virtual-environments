#!/usr/bin/env python3
"""Import only public assignment definitions from the user-supplied Canvas export."""
from pathlib import Path
import datetime as dt,hashlib,json,re,shutil,subprocess,zipfile
import xml.etree.ElementTree as ET
from zoneinfo import ZoneInfo
ROOT=Path(__file__).resolve().parents[1]
EXPORT=ROOT/'csye7270-16373-building-virtual-environments-sec-01-fall-2026-bos-1-tr-export.imscc'
NAMES={1:'01-extend-walker-jumpman.md',2:'02-generate-art-sound-music-for-your-game.md',3:'03-first-3d-assets-with-blender-mcp.md',4:'04-create-a-game-design-document.md',5:'05-shaders-materials-and-godot-shading-language.md',6:'06-creating-particle-effects.md',7:'07-doing-animation.md',8:'08-final-project-pitch-film.md',9:'09-teach-one-game-ai-technique.md',10:'10-final-project.md'}
MODULES={1:[1],2:[2],3:[3],4:[4,5],5:[6,7],6:[9],7:[10,11],8:[5,15],9:[14],10:[15]}
def convert(html):
    # Presentation wrappers interfere with pandoc's table conversion. Content is intact.
    html=re.sub(r"</?div\b(?:[^>\"']|\"[^\"]*\"|'[^']*')*>",'',html,flags=re.I)
    return subprocess.run(['pandoc','-f','html','-t','gfm','--wrap=none'],input=html,text=True,capture_output=True,check=True).stdout

def main():
    dest=ROOT/'canvas/assignment-sources';dest.mkdir(exist_ok=True)
    backup=ROOT/'pantry/backups/assignments-before-canvas-sync-2026-10-14';backup.mkdir(exist_ok=True)
    for p in (ROOT/'assignments').glob('*.md'):
        if not (backup/p.name).exists():shutil.copy2(p,backup/p.name)
    records=[];aux=[]
    with zipfile.ZipFile(EXPORT) as z:
        for n in z.namelist():
            if not n.endswith('/assignment_settings.xml'):continue
            xml=z.read(n);root=ET.fromstring(xml);d={x.tag.split('}')[-1]:x.text for x in root}
            folder=n.split('/')[0];h=next((x for x in z.namelist() if x.startswith(folder+'/') and x.endswith('.html')),None)
            title=d['title'];m=re.match(r'Assignment (\d+)\b',title);num=int(m.group(1)) if m else (10 if title=='Final Portfolio Piece (Project)' else None)
            if num is None:
                aux.append({k:d.get(k) for k in ['title','points_possible','due_at','submission_types','workflow_state']});continue
            raw=z.read(h);(dest/f'{num:02}.html').write_bytes(raw);(dest/f'{num:02}.xml').write_bytes(xml)
            utc=d.get('due_at');local=dt.datetime.fromisoformat(utc).replace(tzinfo=dt.timezone.utc).astimezone(ZoneInfo('America/New_York')) if utc else None
            rec={'number':num,'title':title,'source':f'assignments/{NAMES[num]}','modules':MODULES[num],'canvas_identifier':folder,'points':float(d['points_possible']),'due_at_utc':utc+'Z' if utc else None,'due_at_local':local.isoformat() if local else None,'submission_types':d['submission_types'],'workflow_state':d['workflow_state'],'all_day':d.get('all_day'),'all_day_date':d.get('all_day_date'),'authority':'canvas-export' if num<10 else 'user-pasted-final-project','export_html':h,'snapshot_html':f'canvas/assignment-sources/{num:02}.html','snapshot_sha256':hashlib.sha256(raw).hexdigest()}
            records.append(rec)
            if num==10:continue
            md=convert(raw.decode('utf-8'));lines=md.splitlines()
            if lines and lines[0].startswith('# '):lines=lines[1:]
            md=f'# {title}\n\n'+'\n'.join(lines).lstrip()+'\n'
            p=ROOT/rec['source'];p.write_text(md)
            rec['imported_markdown_sha256']=hashlib.sha256(p.read_bytes()).hexdigest()
    records.sort(key=lambda x:x['number']);assert [x['number'] for x in records]==list(range(1,11))
    (ROOT/'assignments/canvas-authority.json').write_text(json.dumps({'synced':'2026-10-14','canvas_export':EXPORT.name,'timezone':'America/New_York','assignments':records,'other_gradebook_records':aux},indent=2)+'\n')
    # Keep superseded drafts in a dated archive; old links will be updated to canonical names.
    for old in ['04-specify-and-build-a-3d-interaction.md','05-shader-and-material.md','06-audit-a-shader-change.md','07-particle-effects.md','08-animation-and-state.md','09-audio-and-a-performance-budget.md']:
        p=ROOT/'assignments'/old
        if p.exists():p.unlink()
    for num in [1,2]:
        p=ROOT/'assignments'/(NAMES[num]+'.verified.json')
        if p.exists():shutil.move(p,backup/p.name)
    print('Imported Canvas Assignments 1–9 and exact assignment settings; final metadata is 250 points.')
if __name__=='__main__':main()
