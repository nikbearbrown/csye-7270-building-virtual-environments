"""Make the A5 evidence clips; footage is cut at normal speed, stills are held."""
from pathlib import Path
import json
import math
import subprocess
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[2]
REEL=ROOT/"youtube/claude-liam-downfall-a5-shaders-gamedev"
E=ROOT/"evidence/a5"
OUT=REEL/"media"
IMG=REEL/"images"
CAP=ROOT.parent/"evidence/change-brief-2026-10-30"
FONT=ROOT.parent/"brutalist.art/runtime/fonts/EB_Garamond/static/EBGaramond-Regular.ttf"
SANS=Path("C:/Windows/Fonts/segoeui.ttf")
PAPER="#FAF9F5";INK="#302d27";ACCENT="#D97757"
W,H=3840,2160
sheet=json.loads((REEL/"beat_sheet.json").read_text(encoding="utf-8"))
dur={b["beat_id"]:math.ceil(b.get("actual_duration_s",b["estimated_duration_s"])*30)/30 for b in sheet["beats"]}

def run(args):
    subprocess.run(args,check=True,stdout=subprocess.DEVNULL)

def fit(image,box):
    source=Image.open(image).convert("RGB")
    scale=min((box[2]-box[0])/source.width,(box[3]-box[1])/source.height)
    source=source.resize((round(source.width*scale),round(source.height*scale)),Image.Resampling.LANCZOS)
    return source,(box[0]+(box[2]-box[0]-source.width)//2,box[1]+(box[3]-box[1]-source.height)//2)

def board(name,title,items,note=""):
    image=Image.new("RGB",(W,H),PAPER);draw=ImageDraw.Draw(image)
    draw.text((210,120),title,font=ImageFont.truetype(str(FONT),112),fill=INK)
    columns=2 if len(items)>1 else 1
    rows=math.ceil(len(items)/columns)
    cw=(W-420)//columns;ch=1540//rows
    for i,(path,label) in enumerate(items):
        x=210+(i%columns)*cw;y=340+(i//columns)*ch
        source,position=fit(path,(x+15,y,x+cw-30,y+ch-100));image.paste(source,position)
        draw.text((x+30,y+ch-94),label,font=ImageFont.truetype(str(SANS),49),fill=INK)
    if note:draw.text((210,1900),note,font=ImageFont.truetype(str(SANS),43),fill=INK)
    draw.text((2850,1980),"@NikBearBrown",font=ImageFont.truetype(str(FONT),55),fill=INK)
    path=IMG/(name+".png");image.save(path);return path

def still(bid,parts):
    outputs=[]
    for i,(image,seconds) in enumerate(parts):
        part=OUT/f"_{bid}_{i}.mp4";outputs.append(part)
        run(["ffmpeg","-v","error","-y","-loop","1","-framerate","30","-i",str(image),"-t",f"{seconds:.9f}",
             "-c:v","libx264","-preset","fast","-threads","4","-crf","17","-pix_fmt","yuv420p","-an",str(part)])
    concat(bid,outputs)

def concat(bid,parts):
    listing=OUT/f"_{bid}.txt";listing.write_text("".join(f"file '{p.as_posix()}'\n" for p in parts),encoding="utf-8")
    run(["ffmpeg","-v","error","-y","-f","concat","-safe","0","-i",str(listing),"-c","copy",str(OUT/f"{bid}.mp4")])
    for path in parts:path.unlink()
    listing.unlink();print("Completed",bid,flush=True)

def build():
    OUT.mkdir(parents=True,exist_ok=True);IMG.mkdir(exist_ok=True)
    manifest=[]
    def sequence(bid,title,entries,note=""):
        fraction=dur[bid]/len(entries);parts=[]
        for i,(items,caption) in enumerate(entries):
            path=board(bid+f"-{i}",title,items,caption or note);parts.append((path,fraction))
        still(bid,parts);manifest.append({"beat":bid,"sources":[str(p.relative_to(ROOT)) for items,_ in entries for p,_ in items],"duration":dur[bid]})
    sequence("B03","Fire Over The City",[([(E/"use-it/fire-r1.png","fire_remaining = 1.0")],"Linear · exposure 1 · flicker_amount 0")])
    sequence("B05","Predicted Before Capture",[
        ([(E/"use-it/fire-r1.png","r = 1 → A (210,210,67)"),(E/"use-it/fire-r05.png","r = 0.5 → A (158,121,67)")],"Center samples match the original prediction exactly."),
        ([(E/"use-it/fire-r0.png","r = 0 → A (58,58,67)"),(E/"use-it/fire-r2.png","r = 2 → A (210,255,67)")],"hint_range does not clamp code-assigned values.")])
    # Select two contiguous intervals from the native 4K take. No speed change.
    frames=CAP/"a5-gameplay-frames-jpg"
    clips=[]
    lengths=[7.0,dur["B07"]-7.0]
    total=len(list(frames.glob("*.jpg")))/30
    starts=[0.0,total-lengths[1]]
    for i,(start,length) in enumerate(zip(starts,lengths)):
        part=OUT/f"_B07_{i}.mp4";clips.append(part)
        run(["ffmpeg","-v","error","-y","-framerate","30","-start_number",str(round(start*30)),"-i",str(frames/"%05d.jpg"),"-t",f"{length:.9f}",
             "-vf","drawtext=fontfile='C\\:/Windows/Fonts/georgia.ttf':text='@NikBearBrown':x=w-tw-210:y=h-150:fontsize=50:fontcolor=white:box=1:boxcolor=black@0.6:boxborderw=12",
             "-c:v","libx264","-preset","fast","-threads","4","-crf","17","-pix_fmt","yuv420p","-an",str(part)])
    concat("B07",clips);manifest.append({"beat":"B07","source":"native 3840x2160 frames","intervals":[[s,s+n] for s,n in zip(starts,lengths)],"retiming":False,"audio":"Muted game bus beneath local narration"})
    sequence("B09","The Hint Changes The Numbers",[([(E/"hint-experiment/hint-experiment.png","Top: source_color · Bottom: raw")],"64 / 128 / 192  →  64 / 128 / 192 with source_color; 137 / 188 / 225 without")])
    sequence("B11","Same Panel, Same Light",[
        ([(E/"normal-map-check/normal-map-check-review.png","GL / DX raw / DX with Y inversion")],"Review light: corrected DX differs from GL by at most 1 RGB8 level."),
        ([(E/"normal-map-check/normal-map-check-raking.png","GL / DX raw / DX with Y inversion")],"Raking light: corrected DX differs from GL by at most 2 RGB8 levels.")])
    entries=[]
    for name in ["uv_scale","tint_color","roughness_scale","normal_strength"]:
        light="raking" if name=="normal_strength" else "review"
        entries.append(([(E/f"use-it/sweep-{name}-{tag}-{light}.png",f"{name}: {tag}") for tag in ["min","default","max"]],"Other parameters use shader defaults; panel B remains the reference."))
    sequence("B13","Minimum · Default · Maximum",entries)
    sequence("B15","One Program, Independent Values",[
        ([(E/"use-it/materials-baseline.png","Original materials"),(E/"use-it/materials-shared-shader-change.png","Shared ALBEDO statement × 0.5")],"Both panels change when the shared program changes."),
        ([(E/"use-it/materials-baseline.png","Restored program"),(E/"use-it/materials-a-only.png","Only A.tint_color changes")],"Panel B is pixel-identical after changing only A."),
        ([(E/"use-it/base-crates-overview.png","The two actual hall crate_stack props")],"ACES · scene lighting and post-processing retained")])
    sequence("B17","The Generated Shader Renders",[([(E/"use-it/standard-generated.png","BoxMesh + generated Shader + three bound textures")],"Comparison resource only; no game material references this program.")])
    (REEL/"media-provenance.json").write_text(json.dumps(manifest,indent=2)+"\n",encoding="utf-8")

if __name__=="__main__":build()
