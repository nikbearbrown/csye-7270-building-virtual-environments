"""Extract actual-master frames for visual review; never substitute a probe for it."""
from pathlib import Path
import hashlib
import json
import math
import subprocess
from PIL import Image,ImageDraw,ImageFont

ROOT=Path(__file__).resolve().parents[2]
REEL=ROOT/"youtube/claude-liam-downfall-a5-shaders-gamedev"
MASTER=REEL/"exports/landscape"/(REEL.name+".mp4")
QC=REEL/"_qc"
QC.mkdir(exist_ok=True)
frames=QC/"frames-2fps";frames.mkdir(exist_ok=True)
shots=QC/"beat-frames";shots.mkdir(exist_ok=True)
contacts=QC/"contact-sheets";contacts.mkdir(exist_ok=True)
probe=json.loads(subprocess.check_output(["ffprobe","-v","error","-show_streams","-show_format","-of","json",str(MASTER)],text=True))
video=next(s for s in probe["streams"] if s["codec_type"]=="video")
assert (video["width"],video["height"])==(3840,2160)
assert video["r_frame_rate"]=="30/1"
subprocess.run(["ffmpeg","-v","error","-y","-i",str(MASTER),"-vf","fps=2,scale=960:540",str(frames/"%05d.png")],check=True)
sheet=json.loads((REEL/"beat_sheet.json").read_text(encoding="utf-8"));timeline=[];at=0
for beat in sheet["beats"]:
    duration=beat.get("render_duration_s",math.ceil(beat["actual_duration_s"]*30)/30)
    row={"beat":beat["beat_id"],"start":at,"duration":duration,"samples":[]}
    for fraction in (.15,.5,.85):
        moment=at+duration*fraction
        destination=shots/(beat["beat_id"]+f"-{int(fraction*100):02}.png")
        subprocess.run(["ffmpeg","-v","error","-y","-ss",str(moment),"-i",str(MASTER),"-frames:v","1","-vf","scale=1920:1080",str(destination)],check=True)
        row["samples"].append({"fraction":fraction,"time":moment,"path":destination.relative_to(REEL).as_posix()})
    timeline.append(row);at+=duration
paths=sorted(frames.glob("*.png"))
font=ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf",23)
for page in range(math.ceil(len(paths)/24)):
    board=Image.new("RGB",(1920,1320),"#ddd9d0");draw=ImageDraw.Draw(board)
    for cell,path in enumerate(paths[page*24:(page+1)*24]):
        image=Image.open(path).convert("RGB");image.thumbnail((480,270),Image.Resampling.LANCZOS)
        x=(cell%4)*480;y=(cell//4)*220
        # A 16:9 frame is contained in a 480x190 cell, with a timestamp below.
        image.thumbnail((480,190),Image.Resampling.LANCZOS)
        board.paste(image,(x+(480-image.width)//2,y))
        draw.text((x+16,y+192),f"{(int(path.stem)-1)/2:.1f} s",font=font,fill="#222")
    board.save(contacts/f"page-{page+1:02}.png")
receipt={"master":MASTER.name,"sha256":hashlib.sha256(MASTER.read_bytes()).hexdigest(),"width":video["width"],"height":video["height"],"fps":video["r_frame_rate"],"duration":float(probe["format"]["duration"]),"frames_2fps":len(paths),"contact_pages":math.ceil(len(paths)/24),"beat_samples":timeline,"review_status":"Frames extracted; visual inspection is recorded separately in REPORT.md."}
(QC/"review-samples.json").write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
print(json.dumps({k:v for k,v in receipt.items() if k!="beat_samples"},indent=2))
