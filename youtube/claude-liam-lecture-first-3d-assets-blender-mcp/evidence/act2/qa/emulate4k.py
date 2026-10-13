#!/usr/bin/env python3
"""emulate4k.py out.png --img P --cam cx,cy,s [--win x0,y0,x1,y1] [--ring box] [--dot x,y] [--lab 'text@x,y,size'] [--thumb W,cx,cy]
4K emulation of an Act II frame that samples the capture EXACTLY as Manim 0.20's Camera.display_image_mobject does
(PIL Image.transform, BICUBIC, no antialiasing), then masks the frame, draws the outline/ring/labels, and round-trips the
frame through h264 yuv420 (crf 18) like a compiled clip. No Manim render, no 4K video."""
import argparse, subprocess, os
from PIL import Image, ImageDraw, ImageFont
U = 270.0
ap = argparse.ArgumentParser()
ap.add_argument("out"); ap.add_argument("--img"); ap.add_argument("--cam", default="1728,1003,1")
ap.add_argument("--win", default="-2.95,-3.5,6.3,3.5"); ap.add_argument("--ring", action="append", default=[])
ap.add_argument("--sw", type=int, default=22); ap.add_argument("--lab", action="append", default=[])
ap.add_argument("--dot", action="append", default=[]); ap.add_argument("--thumb", default=None)
a = ap.parse_args()
def px(x, y): return (1920 + x * U, 1080 - y * U)
src = Image.open(a.img).convert("RGBA")
F = Image.new("RGB", (3840, 2160), (242, 240, 233))
if a.thumb:      # whole capture at width W units centred at (tx, ty): no window mask
    W, tx, ty = [float(v) for v in a.thumb.split(",")]
    s = W * U / src.width
    ox, oy = px(tx - W / 2, ty + W * src.height / src.width / 2)
    X0, Y0, X1, Y1 = ox, oy, ox + src.width * s, oy + src.height * s
else:
    wx0, wy0, wx1, wy1 = [float(v) for v in a.win.split(",")]
    cx, cy, s = [float(v) for v in a.cam.split(",")]
    u = s / U
    vw, vh = (wx1 - wx0) / u, (wy1 - wy0) / u
    cx = min(max(cx, vw / 2), src.width - vw / 2); cy = min(max(cy, vh / 2), src.height - vh / 2)
    X0, Y0 = px(wx0, wy1); X1, Y1 = px(wx1, wy0)
    ox, oy = X0 - (cx - vw / 2) * s, Y0 - (cy - vh / 2) * s     # where the capture's top-left lands (4K px)
# output pixel (x, y) samples source ((x - ox)/s, (y - oy)/s)
layer = src.transform((3840, 2160), Image.Transform.AFFINE, (1 / s, 0, -ox / s, 0, 1 / s, -oy / s), resample=Image.Resampling.BICUBIC)
mask = Image.new("L", (3840, 2160), 0)
ImageDraw.Draw(mask).rectangle([X0, Y0, X1 - 1, Y1 - 1], fill=255)
alpha = Image.composite(layer.getchannel("A"), Image.new("L", (3840, 2160), 0), mask)
F.paste(layer.convert("RGB"), (0, 0), alpha)
d = ImageDraw.Draw(F)
d.rectangle([X0, Y0, X1, Y1], outline=(61, 57, 41), width=11)
def sp(x, y): return (ox + x * s, oy + y * s)
for r in a.ring:
    rx0, ry0, rx1, ry1 = [float(v) for v in r.split(",")]
    p0, p1 = sp(rx0, ry0), sp(rx1, ry1)
    d.rounded_rectangle([p0[0], p0[1], p1[0], p1[1]], radius=43, outline=(217, 119, 87), width=a.sw)
for dt in a.dot:
    x, y = [float(v) for v in dt.split(",")]
    p = sp(x, y); d.ellipse([p[0] - 35, p[1] - 35, p[0] + 35, p[1] + 35], fill=(217, 119, 87))
for l in a.lab:
    t, pos = l.rsplit("@", 1); x, y, size = [float(v) for v in pos.split(",")]
    f = ImageFont.truetype("/Users/bear/Library/Fonts/EBGaramond-VariableFont_wght.ttf", int(size * 2.15))
    p = px(x, y); d.text((p[0], p[1]), t, font=f, fill=(61, 57, 41), anchor="lm")
tmp = a.out + ".raw.png"; F.save(tmp)
mp4 = a.out + ".mp4"
subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-loop", "1", "-i", tmp, "-t", "0.5", "-r", "24", "-pix_fmt", "yuv420p",
                "-c:v", "libx264", "-crf", "23", mp4], check=True)
subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", "0.25", "-i", mp4, "-frames:v", "1", a.out], check=True)
os.remove(tmp); os.remove(mp4)
