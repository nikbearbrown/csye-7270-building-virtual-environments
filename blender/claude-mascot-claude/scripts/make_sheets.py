# make_sheets.py - composites the Blender renders onto the Claude cream stage and builds contact sheets (system python3 + PIL).
#   python3 make_sheets.py
import os, json
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
R = os.path.join(HERE, "renders")
CREAM = (250, 249, 245)
INK = (61, 57, 41)
TERRA = (217, 119, 87)


def font(size):
    for p in ("/System/Library/Fonts/Supplemental/Georgia.ttf", "/System/Library/Fonts/Helvetica.ttc"):
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def stage(path, crop=None):
    im = Image.open(path).convert("RGBA")
    bg = Image.new("RGBA", im.size, CREAM + (255,))
    bg.alpha_composite(im)
    im = bg.convert("RGB")
    if crop:
        im = im.crop(crop)
    return im


def sheet(items, cols, cell, out, title=None):
    rows = (len(items) + cols - 1) // cols
    top = 90 if title else 0
    W, H = cell
    sh = Image.new("RGB", (cols * W, rows * (H + 56) + top), CREAM)
    d = ImageDraw.Draw(sh)
    if title:
        d.text((24, 22), title, fill=INK, font=font(44))
    for i, (label, path, crop) in enumerate(items):
        im = stage(path, crop).resize((W, H), Image.LANCZOS)
        x, y = (i % cols) * W, top + (i // cols) * (H + 56)
        sh.paste(im, (x, y))
        d.text((x + 18, y + H + 6), label, fill=TERRA, font=font(34))
    sh.save(out)
    print("wrote", os.path.relpath(out, HERE))


# the render is 1600x1200 with the mascot centred; crop to the middle band so the sheets use the space
CROP = (200, 120, 1400, 1100)
turn = [("%d deg" % a, os.path.join(R, "turnaround", "az%03d.png" % a), CROP) for a in range(0, 360, 45)]
sheet(turn, 4, (600, 490), os.path.join(R, "sheet-turnaround.png"), "Claude mascot, turnaround (front = 0 deg)")

ortho = [(d, os.path.join(R, "ortho", d + ".png"), (0, 0, 1600, 1200)) for d in ("front", "back", "left", "right", "top", "bottom")]
sheet(ortho, 3, (640, 480), os.path.join(R, "sheet-orthographic.png"), "Claude mascot, orthographic (1.6 m across)")

poses = json.load(open(os.path.join(R, "poses", "poses.json")))
items = []
for n, name in enumerate(poses, 1):
    items.append((name, os.path.join(R, "poses", "%02d-%s.png" % (n, name)), CROP))
sheet(items, 6, (480, 392), os.path.join(R, "sheet-poses.png"), "Rig pose tests: the 18 named animations, one extreme frame each")


# ---- rig diagram: the front orthographic render (1000 px per metre, centre = x 0, z 0.43) with each bone's joint marked
U = 0.01
HEADS = {"Root": (0, 0), "Arm.L": (-58 * U, 56 * U), "Arm.R": (58 * U, 56 * U), "Eye.L": (-31.5 * U, 76 * U), "Eye.R": (31.5 * U, 76 * U),
         "Leg.1": (-31.5 * U, 26 * U), "Leg.2": (-10.5 * U, 26 * U), "Leg.3": (21.5 * U, 26 * U), "Leg.4": (42.5 * U, 26 * U)}
LABEL_OFFSET = {"Root": (-60, 28), "Arm.L": (-150, -50), "Arm.R": (30, -50), "Eye.L": (-150, -85), "Eye.R": (30, -85),
                "Leg.1": (-95, 62), "Leg.2": (-45, 98), "Leg.3": (-20, 98), "Leg.4": (30, 62)}
im = stage(os.path.join(R, "ortho", "front.png"))
d = ImageDraw.Draw(im)
for name, (x, z) in HEADS.items():
    px, py = 800 + x * 1000, 600 - (z - 0.43) * 1000
    d.ellipse([px - 11, py - 11, px + 11, py + 11], outline=INK, width=4, fill=(255, 255, 255))
    d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=TERRA)
    ox, oy = LABEL_OFFSET[name]
    d.text((px + ox, py + oy), name, fill=INK, font=font(34))
d.text((24, 22), "Rig: 9 bones, all children of Root; each bone points up (local Y = up, X = right, Z = toward the viewer)", fill=INK, font=font(34))
im.crop((0, 0, 1600, 1100)).save(os.path.join(R, "rig-diagram.png"))
print("wrote renders/rig-diagram.png")
