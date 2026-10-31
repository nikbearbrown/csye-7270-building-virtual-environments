"""Bind the shipped channel jingle to the locked title card without cutting it."""
from pathlib import Path
import hashlib
import json
import math
import subprocess

ROOT=Path(__file__).resolve().parents[2]
REEL=ROOT/"youtube/claude-liam-downfall-a5-shaders-gamedev"
pool=sorted((ROOT.parent/"brutalist.art/logos/bear-brown").glob("*.mp3"))
assert pool,"Missing shipped channel jingle pool"
source=pool[sum(map(ord,REEL.name))%len(pool)]
duration=float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",str(source)],text=True))
target_duration=math.ceil((duration+1)*30)/30
target=REEL/"audio/outro-stock.wav";target.parent.mkdir(exist_ok=True)
subprocess.run(["ffmpeg","-v","error","-y","-i",str(source),"-af","apad","-t",str(target_duration),"-ar","48000","-ac","2","-c:a","pcm_s16le",str(target)],check=True)
path=REEL/"beat_sheet.json";sheet=json.loads(path.read_text(encoding="utf-8"));beat=sheet["beats"][-1]
assert beat["shot"]["remotion"]["pattern"]=="ClaudeTitleOutro"
beat.update({"audio_policy":"music","audio_file":"audio/outro-stock.wav","engine":"stock","reuse_audio":True,"actual_duration_s":target_duration,"estimated_duration_s":target_duration,"narration_text":""})
beat.pop("silent",None)
path.write_text(json.dumps(sheet,indent=2)+"\n",encoding="utf-8")
receipt={"pool":"brutalist.art/logos/bear-brown","source":source.name,"source_sha256":hashlib.sha256(source.read_bytes()).hexdigest(),"jingle_seconds":duration,"beat_seconds":target_duration,"silence_tail_seconds":target_duration-duration,"narration":False,"selection":"sum of slug codepoints modulo sorted pool size","output_sha256":hashlib.sha256(target.read_bytes()).hexdigest()}
(REEL/"outro-audio.json").write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
print(json.dumps(receipt,indent=2))
