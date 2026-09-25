"""Verify source audio placement, preservation and the unchanged regular outro."""
import argparse,hashlib,json,subprocess
from pathlib import Path
import numpy as np
from scipy.signal import correlate,correlation_lags
ROOT=Path(__file__).resolve().parents[1]
sheet=json.loads((ROOT/'beat_sheet.json').read_text())
ap=argparse.ArgumentParser();ap.add_argument('--audio',type=Path);args=ap.parse_args()
master=args.audio or ROOT/f"{sheet['metadata']['slug']}.mp4"
def decode(path):
    return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-vn','-ac','1','-ar','16000','-f','f32le','-']),dtype=np.float32).astype(float)
master_audio=decode(master);start=0.;rows=[]
for b in sheet['beats']:
    d=b['actual_duration_s'];expected=decode(ROOT/b['audio_file']);actual=master_audio[round(start*16000):round((start+d)*16000)]
    # The canonical MP3-concat/AAC path introduces ~21 ms codec priming plus
    # sub-frame timestamp rounding. Bound placement to 40 ms (< one 24 fps
    # video frame), never seconds or unrestricted best-match realignment.
    n=min(len(expected),len(actual))
    corr=correlate(actual,expected,method='fft');lags=correlation_lags(len(actual),len(expected))
    allowed=np.abs(lags)<=640;best_lag=int(lags[allowed][np.argmax(corr[allowed])])
    lo,hi=max(0,-best_lag)+160,min(n,n-best_lag)-160
    x,y=expected[lo:hi],actual[lo+best_lag:hi+best_lag];den=np.linalg.norm(x)*np.linalg.norm(y)
    best=float(np.dot(x,y)/den) if den else 0.
    peak=float(np.max(np.abs(actual)))
    rows.append({'beat':b['beat_id'],'start_s':start,'duration_s':d,'cosine_similarity':best,'alignment_samples_16khz':best_lag,'peak':peak,'passed':best>=.95 and peak>.0001})
    print(b['beat_id'],round(best,5),best_lag,flush=True);start+=d
last=sheet['beats'][-1];assert not last['narration_text']
stock=hashlib.sha256(Path(last['outro_jingle_source']).read_bytes()).hexdigest()
assert stock==hashlib.sha256((ROOT/last['audio_file']).read_bytes()).hexdigest()
report={'passed':all(r['passed'] for r in rows),'beats':rows,'max_alignment_ms':40,'source_outro_sha256':stock,'scope':'Waveform placement/preservation including bounded codec priming; not human pronunciation approval.'}
(ROOT/'_qc'/('precompile-audio-qc.json' if args.audio else 'master-audio-qc.json')).write_text(json.dumps(report,indent=2)+'\n')
if not report['passed']:raise SystemExit('Inspect audio mismatch.')
