#!/usr/bin/env python3
"""Add the hearts inset to the gameplay capture: capture/play-01.mp4 →
capture/play-01-inset.mp4 (not in git), frame for frame.

The hearts are about 380 × 140 px of a 3840 × 2160 frame, so each frame gets
a panel at the top right: the same frame's hearts, enlarged 3× with
nearest-neighbour, and the value of tint_amount the film's driver read from
the hearts' material on that frame (capture/play-01-run.log, "frame N
tint_amount ..."). Nothing else in the frame is touched; no frame is added,
dropped, retimed or held.

    python3 tools/make_play_inset.py
"""
import re, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

REEL = Path(__file__).resolve().parents[1]
FONTS = Path("/Users/eric/csye7270/brutalist.art/runtime/fonts")
W, H = 3840, 2160
SRC, OUT = REEL / "capture/play-01.mp4", REEL / "capture/play-01-inset.mp4"
BOX = (48, 40, 432, 180)        # the three hearts: (24, 20)–(216, 90) in the 1920 × 1080 layout, × 2
K = 3
X, Y = W - 200 - (BOX[2] - BOX[0]) * K - 40, 150


def font(name, size):
    return ImageFont.truetype(str(FONTS / {"sans": "Inter/static/Inter_28pt-Regular.ttf",
                                           "bold": "Inter/static/Inter_28pt-Medium.ttf",
                                           "mono": "PT_Mono/PTMono-Regular.ttf"}[name]), size)


def main():
    values = {}
    for l in (REEL / "capture/play-01-run.log").read_text().splitlines():
        m = re.match(r"frame (\d+) tint_amount ([\d.]+) hearts (\d+)", l)
        if m:
            values[int(m[1])] = (float(m[2]), int(m[3]))
    n = int(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v", "-count_frames", "-show_entries",
                            "stream=nb_read_frames", "-of", "csv=p=0", str(SRC)], capture_output=True, text=True, check=True).stdout)
    if sorted(values) != list(range(n)):
        raise SystemExit(f"log has {len(values)} frame values, capture has {n} frames")
    dec = subprocess.Popen(["ffmpeg", "-v", "error", "-i", str(SRC), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", "30",
                            "-i", "-", "-c:v", "libx264", "-preset", "slow", "-crf", "14", "-pix_fmt", "yuv420p", str(OUT)],
                           stdin=subprocess.PIPE)
    pw, ph = (BOX[2] - BOX[0]) * K, (BOX[3] - BOX[1]) * K
    for i in range(n):
        raw = dec.stdout.read(W * H * 3)
        im = Image.frombytes("RGB", (W, H), raw)
        hearts = im.crop(BOX).resize((pw, ph), Image.NEAREST)
        d = ImageDraw.Draw(im, "RGBA")
        d.rounded_rectangle((X - 24, Y - 24, X + pw + 24, Y + ph + 190), radius=18, fill=(20, 18, 16, 215))
        im.paste(hearts, (X, Y))
        v, hearts_left = values[i]
        d.text((X, Y + ph + 22), "INSET · the hearts from this frame, 3× nearest-neighbour", font=font("bold", 40), fill=(255, 255, 255))
        d.text((X, Y + ph + 90), f"tint_amount {v:.3f}   hearts {hearts_left}", font=font("mono", 48),
               fill=(153, 224, 255) if v > 0 else (230, 230, 230))
        enc.stdin.write(im.tobytes())
    enc.stdin.close()
    if enc.wait() or dec.wait():
        raise SystemExit("ffmpeg failed")
    print(f"wrote {OUT.name}: {n} frames")


if __name__ == "__main__":
    main()
