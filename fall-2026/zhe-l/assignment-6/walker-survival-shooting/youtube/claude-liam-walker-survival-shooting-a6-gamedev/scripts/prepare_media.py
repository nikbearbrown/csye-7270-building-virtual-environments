"""Make the two real-footage clips from this film's native 4K PNG takes, with burned-in disclosure labels.

media/B08.mp4 (PLAY_A) = landing-run-02 (Effect A, player camera, scripted Space/A keys), played once full frame, then the
         same frames again as a 2x crop of the lower middle, labelled "replay, 2x crop of the same frames".
media/B16.mp4 (PLAY_B) = lights-film-01 (Effect B, film camera, scripted S/F keys; pause and hide set from code), full frame,
         with an inset: |this frame - the same view with the dust hidden| x 8, specks enlarged (computed).
         Reference frames: f00315 (lights on, dust hidden) while the lights are on, f00150 (lights off) while off.
No retiming, trimming or slow motion. If narration is longer, the last frame is held (--hold-a / --hold-b),
and the held part says so.
Run: python -I scripts/prepare_media.py [a] [b] [--hold-a S] [--hold-b S]
"""
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

REEL = Path(__file__).resolve().parents[1]
CAP = REEL.parents[1] / "captures"
TMP = REEL.parents[1] / "media-frames"
FONT = Path("<brutalist.art>/runtime/fonts/Lato/static/Lato-Bold.ttf")
F50 = ImageFont.truetype(str(FONT), 50)
F44 = ImageFont.truetype(str(FONT), 44)


def arg(name):
    return float(sys.argv[sys.argv.index(name) + 1]) if name in sys.argv else 0.0


def bar(im, text, top=None):
    d = ImageDraw.Draw(im)
    d.rectangle([0, im.height - 150, im.width, im.height], fill=(0, 0, 0))
    d.text((90, im.height - 104), text, font=F50, fill=(255, 255, 255))
    if top:
        tw = d.textlength(top, font=F50)
        d.rectangle([im.width - tw - 150, 40, im.width - 40, 140], fill=(0, 0, 0))
        d.text((im.width - tw - 95, 64), top, font=F50, fill=(255, 255, 255))
    return im


def encode(folder, out, hold):
    vf = "null"
    if hold > 0:
        vf = (f"tpad=stop_mode=clone:stop_duration={hold},drawtext=fontfile='"
              + FONT.as_posix().replace(":", "\\:") + "':text='held final frame':fontcolor=white:fontsize=50:"
              f"box=1:boxcolor=black:boxborderw=20:x=90:y=60:enable='gte(n,{len(list(folder.glob('m*.png')))})'")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", "30", "-start_number", "0",
                    "-i", str(folder / "m%05d.png"), "-vf", vf,
                    "-c:v", "libx264", "-preset", "slow", "-crf", "12", "-pix_fmt", "yuv420p", "-r", "30", "-an",
                    str(out)], check=True)
    info = subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-show_entries",
                           "stream=nb_read_frames,width,height", "-of", "csv=p=0", str(out)],
                          capture_output=True, text=True).stdout.strip()
    print(out.name, info)


def play_a(hold):
    src = CAP / "landing-run-02" / "frames"
    n = len(list(src.glob("f*.png")))
    tmp = TMP / "play_a"
    tmp.mkdir(parents=True, exist_ok=True)
    landed = [118, 268, 398, 458, 518, 578]       # physics ticks printed in logs/landing-run-02.log; frame = tick // 2
    base = ("Native Godot 4.7.2 render  ·  3840x2160  ·  scripted input (Space, A), not a human playtest  ·  "
            "offline 30 fps capture")
    k = 0
    for rep in (0, 1):
        for i in range(n):
            im = Image.open(src / f"f{i:05d}.png").convert("RGB")
            if rep == 1:
                im = im.crop((480, 1060, 2400, 2140)).resize((3840, 2160), Image.LANCZOS)
            count = sum(1 for t in landed if t // 2 <= i)
            top = f"landings: {count}" + ("   ·   replay: 2x crop of the same frames" if rep else "")
            bar(im, base, top).save(tmp / f"m{k:05d}.png")
            k += 1
    encode(tmp, REEL / "media" / "B08.mp4", hold)
    return k


def play_b(hold):
    src = CAP / "lights-film-01" / "frames"
    n = len(list(src.glob("f*.png")))
    tmp = TMP / "play_b"
    tmp.mkdir(parents=True, exist_ok=True)
    ref_on = np.asarray(Image.open(src / "f00315.png").convert("RGB")).astype(np.int32)
    ref_off = np.asarray(Image.open(src / "f00150.png").convert("RGB")).astype(np.int32)

    # frame -> state, from inputs.jsonl / the log: lights_changed at ticks 242 (off) and 362 (on),
    # paused ticks 480-540, hidden ticks 600-660; frame = tick // 2
    def state(i):
        t = i * 2
        if t < 242:
            return "lights on", ref_on
        if t < 362:
            return "lights OFF (F key)", ref_off
        if 480 <= t < 540:
            return "PAUSED from code (the game has no pause feature yet)", ref_on
        if 600 <= t < 660:
            return "LightDust hidden from code", ref_on
        return "lights on again (F key)", ref_on

    base = ("Native Godot 4.7.2 render  ·  3840x2160  ·  FILM CAMERA added by the capture script  ·  scripted "
            "S/F keys; pause and hide set from code")
    for i in range(n):
        if "--reuse" in sys.argv and (tmp / f"m{i:05d}.png").exists():
            continue                               # labelled frames already made by an earlier run of this script
        im = Image.open(src / f"f{i:05d}.png").convert("RGB")
        what, ref = state(i)
        a = np.asarray(im).astype(np.int32)
        d = np.clip(np.abs(a - ref).max(axis=2) * 8, 0, 255).astype(np.uint8)
        ins = Image.fromarray(d).filter(ImageFilter.MaxFilter(5)).resize((1280, 720), Image.LANCZOS).convert("RGB")
        dr = ImageDraw.Draw(ins)
        dr.rectangle([0, 0, 1280, 62], fill=(0, 0, 0))
        dr.text((16, 8), "computed: |frame - same view, dust hidden| x 8", font=F44, fill=(255, 255, 255))
        dr.rectangle([0, 0, 1279, 719], outline=(255, 255, 255), width=4)
        im.paste(ins, (3840 - 1280 - 60, 2160 - 150 - 720 - 50))
        bar(im, base, what).save(tmp / f"m{i:05d}.png")
    encode(tmp, REEL / "media" / "B16.mp4", hold)
    return n


if __name__ == "__main__":
    (REEL / "media").mkdir(exist_ok=True)
    which = [a for a in sys.argv[1:] if a in ("a", "b")] or ["a", "b"]
    res = {}
    if "a" in which:
        res["PLAY_A"] = play_a(arg("--hold-a"))
    if "b" in which:
        res["PLAY_B"] = play_b(arg("--hold-b"))
    print(json.dumps(res))
