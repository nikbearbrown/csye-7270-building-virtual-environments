"""Make media/<BID>.mp4 for the beats that show what exists, from the film's own Movie Maker PNG takes and document frames.

Every clip gets a burned-in disclosure strip. No retiming or slow motion: a clip is cut to segments (a cut is
announced in the strip) and, if the narration is longer, its last frame is held with "held final frame" on screen.
Frames come from <film-work>/a8/captures/<take>/frameNNNNNNNN.png (2048 x 1152, scaled to 1920 x 1080).
Run: python -I scripts/prepare_media.py [BID ...]
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

REEL = Path(__file__).resolve().parents[1]
CAP = Path(r"<film-work>/a8\captures")
FONT = Path(r"<brutalist.art>\runtime\fonts\Lato\static\Lato-Bold.ttf")
F32 = ImageFont.truetype(str(FONT), 32)
F28 = ImageFont.truetype(str(FONT), 28)
W, H, FPS = 1920, 1080, 30
STRIP = 72

# beat: (strip text, [segments]); segment = (take, first, last, crop box in 2048x1152 or None, top label or None)
PLAN = {
    "B00": ("SCRIPTED INPUT · f13431bf · Tab, then a long Tab", [("tablet", 0, 164, None, None)]),
    "B07": ("SCRIPTED INPUT · f13431bf · edited: one cut", [("tablet", 175, 299, None, None), ("tablet", 330, 469, None, None)]),
    "B08": ("STANDALONE DEBUG SCENE · SCRIPTED INPUT · f13431bf · 2x crop", [
        ("mome1", 80, 201, (0, 0, 1024, 576), "read-only memo: the typing changes nothing"),
        ("mome2", 80, 228, (0, 0, 1024, 576), "editable memo: the typing is added")]),
    "B10": ("SCRIPTED INPUT · f13431bf · front camera", [("b10", 0, 250, None, None)]),
    "B11": ("SCRIPTED INPUT · f13431bf · landing dust GPU cost +0.001 ms on an NVIDIA GeForce RTX 5070 Ti Laptop GPU", [
        ("b10", 54, 99, (1024, 576, 2048, 1152), "screen glow, 2x crop"),
        ("b11", 20, 215, None, None)]),
    "B13": ("SCRIPTED INPUT · f13431bf · W held with two hands, then with one hand", [("tablet", 470, 673, None, None)]),
}
STILLS = {"B09": "docs/b09-readme-keys.png", "B12": "docs/b12-tests.png"}


def text_box(d, xy, text, font, pad=14):
    x, y = xy
    tw = d.textlength(text, font=font)
    d.rectangle([x - pad, y - pad + 2, x + tw + pad, y + font.size + pad], fill=(0, 0, 0))
    d.text((x, y), text, font=font, fill=(255, 255, 255))


def frame_image(take, n, crop, top, strip, caption):
    im = Image.open(CAP / take / f"frame{n:08d}.png").convert("RGB")
    if crop:
        im = im.crop(crop)
    im = im.resize((W, H), Image.LANCZOS)
    d = ImageDraw.Draw(im)
    d.rectangle([0, H - STRIP, W, H], fill=(0, 0, 0))
    d.text((48, H - STRIP + 18), strip, font=F32, fill=(255, 255, 255))
    if top:
        text_box(d, (48, 40), top, F32)
    if caption:
        text_box(d, (W - 48 - d.textlength(caption, font=F28), 40), caption, F28)
    return im


def encode(folder, out, count):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", str(FPS), "-i", str(folder / "m%05d.png"),
                    "-frames:v", str(count), "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", str(out)], check=True)


def build(bid, sheet):
    need = round(sheet[bid]["actual_duration_s"] * FPS) + 1
    out = REEL / "media" / f"{bid}.mp4"
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        k = 0
        if bid in STILLS:
            im = Image.open(CAP / STILLS[bid]).convert("RGB").resize((W, H), Image.LANCZOS)
            im.save(tmp / "m00000.png")
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-framerate", str(FPS), "-i", str(tmp / "m00000.png"),
                            "-frames:v", str(need), "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", str(out)], check=True)
            return need, 0
        strip, segs = PLAN[bid]
        caption = "AI voice · script by Zhe Liu" if bid == "B00" else None
        last = None
        for take, a, b, crop, top in segs:
            for n in range(a, b + 1):
                if k >= need:
                    break
                last = frame_image(take, n, crop, top, strip, caption)
                last.save(tmp / f"m{k:05d}.png")
                k += 1
        real = k
        if k < need:
            d = ImageDraw.Draw(last)
            text_box(d, (W - 48 - d.textlength("held final frame", font=F32), 40), "held final frame", F32)
            while k < need:
                last.save(tmp / f"m{k:05d}.png")
                k += 1
        encode(tmp, out, need)
        return real, need - real


sheet = {b["beat_id"]: b for b in json.load(open(REEL / "beat_sheet.json", encoding="utf-8"))["beats"]}
todo = sys.argv[1:] or list(PLAN) + list(STILLS)
report = {}
for bid in todo:
    real, held = build(bid, sheet)
    report[bid] = {"frames_real": real, "frames_held": held, "audio_s": sheet[bid]["actual_duration_s"]}
    print(bid, report[bid])
old = {}
rp = REEL / "media" / "prepare_media.json"
if rp.exists():
    old = json.load(open(rp))
old.update(report)
json.dump(old, open(rp, "w"), indent=1)
