#!/usr/bin/env python3
"""Word timestamps (faster-whisper, local) for each beat's ORIGINAL (unpadded) audio; writes <reel>/word_times.json."""
import json, sys
from pathlib import Path
from faster_whisper import WhisperModel
m = WhisperModel('small.en', device='cpu', compute_type='int8')
for reel in map(Path, sys.argv[1:]):
    sheet = json.loads((reel / 'beat_sheet.json').read_text()); out = {}
    for b in sheet['beats']:
        a = reel / b['audio_file']
        segs, _ = m.transcribe(str(a), word_timestamps=True, language='en')
        words = [(w.word.strip(), round(w.start, 2), round(w.end, 2)) for s in segs for w in s.words]
        out[b['beat_id']] = {'duration': b['actual_duration_s'], 'heard': ' '.join(w[0] for w in words), 'words': words}
    (reel / 'word_times.json').write_text(json.dumps(out, indent=1) + '\n')
    for k, v in out.items(): print(reel.name[20:], k, '|', v['heard'][:150])
