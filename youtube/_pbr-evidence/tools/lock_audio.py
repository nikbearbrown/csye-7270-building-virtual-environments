#!/usr/bin/env python3
"""After TTS: add real lead/tail silence, record measured durations, sync Remotion durationSeconds. Keeps unpadded originals."""
from pathlib import Path
import json, sys, subprocess, hashlib, shutil
reel = Path(sys.argv[1]).resolve(); sp = reel / 'beat_sheet.json'
sheet = json.loads(sp.read_text()); cache = reel / 'audio-originals'; cache.mkdir(exist_ok=True)
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
dur = lambda p: float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=nw=1:nk=1', str(p)], text=True))
for b in sheet['beats']:
    src = reel / b['audio_file']; tag = cache / (b['beat_id'] + '.json')
    rec = json.loads(tag.read_text()) if tag.exists() else {}
    if rec.get('padded_sha256') != sha(src):
        orig = cache / (b['beat_id'] + '-' + sha(src)[:12] + src.suffix)
        if not orig.exists(): shutil.copy2(src, orig)
        lead = float(b.get('lead_silence_s', 0)); tail = float(b.get('tail_silence_s', 0))
        if lead or tail:
            out = reel / 'mp3' / (b['beat_id'] + '-padded.wav')
            subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-i', str(orig), '-af', f'adelay={round(lead*1000)}:all=1,apad', '-t', str(dur(orig) + lead + tail), '-c:a', 'pcm_s16le', str(out)], check=True)
            b['audio_file'] = str(out.relative_to(reel)); src = out
        tag.write_text(json.dumps({'original': str(orig), 'padded_sha256': sha(src)}, indent=2) + '\n')
    b['actual_duration_s'] = dur(src)
    if 'remotion' in b.get('shot', {}): b['shot']['remotion']['props']['durationSeconds'] = b['actual_duration_s']
sp.write_text(json.dumps(sheet, indent=2, ensure_ascii=False) + '\n')
print(reel.name, 'timeline', round(sum(b['actual_duration_s'] for b in sheet['beats']), 2), 's')
for b in sheet['beats']: print(' ', b['beat_id'], round(b['actual_duration_s'], 2), b['shot'].get('manim', {}).get('class') or b['shot'].get('remotion', {}).get('props', {}).get('video', ''))
