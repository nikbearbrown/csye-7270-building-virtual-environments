# ============================================================
# About: builds the A7 frame strip of the one-handed raise from a Movie Maker capture and its per-frame log (CHANGE-BRIEF "The frame strip")
# ============================================================
# Run (from the walker-survival-shooting folder, after the capture):
#   python tools/make_strip.py captures/tablet_raise/r0 logs/tablet_raise_r0.log
# What it does:
#   1. Reads the log lines "FRAME movie physics hold state clip_pos lit" printed by previews/tablet_raise_preview.gd.
#   2. Finds the trigger frame (the first frame whose hold is 1) and, for each clip frame the brief lists (0, 5, 7, 10, 14, 16, 18), the movie frame whose
#      clip position is that frame's time; for frame 20, the first frame where the screen is lit.
#   3. Lays those movie frames side by side, labelled, into strip.png, keeps only those frames and deletes the rest of the sequence.
# The strip is a fixture capture: it shows what one run rendered, nothing more.
import os
import sys
from PIL import Image, ImageDraw

# ============================================================
# Constants: the frames the brief asks to read
# ============================================================
CLIP_FRAMES = [0, 5, 7, 10, 14, 16, 18]  # Read by clip position
LIT_FRAME = 20  # Read as "the first frame the screen is lit"
CLIP_FPS = 30.0  # The brief's frame rate
THUMB_WIDTH = 480  # Width of each frame in the strip
LABEL_HEIGHT = 28  # Space under each frame for its label


## Reads the per-frame log into a list of dicts.
def read_log(path):
    rows = []
    for line in open(path, encoding="utf-8", errors="replace"):
        parts = line.split()
        if len(parts) == 7 and parts[0] == "FRAME" and parts[1].isdigit():
            rows.append({"movie": int(parts[1]), "physics": int(parts[2]), "hold": int(parts[3]), "state": parts[4],
                         "pos": float(parts[5]), "lit": parts[6] == "true"})
    return rows


## Picks the movie frame for each frame the brief lists; returns [(label, movie frame)].
def pick(rows):
    trigger = next(r["movie"] for r in rows if r["hold"] == 1)  # The first frame on which the game has the tablet out
    picks = [("trigger (movie %d)" % trigger, trigger)]
    raising = [r for r in rows if r["movie"] >= trigger and r["state"] == "raise_1h"]
    for f in CLIP_FRAMES:
        want = f / CLIP_FPS
        best = min(raising, key=lambda r: abs(r["pos"] - want))  # The frame whose clip position is closest to clip frame f
        picks.append(("clip frame %d (movie %d)" % (f, best["movie"]), best["movie"]))
    lit = next(r["movie"] for r in rows if r["movie"] >= trigger and r["lit"])  # The first frame the screen is lit
    picks.append(("frame %d: screen lit (movie %d)" % (LIT_FRAME, lit), lit))
    return picks


## Movie Maker names frames frame00000000.png, frame00000001.png ... (8 digits).
def frame_path(folder, movie):
    return os.path.join(folder, "frame%08d.png" % movie)


## Builds the strip, keeps the picked frames, deletes the rest of the sequence.
def main():
    folder, log = sys.argv[1], sys.argv[2]
    picks = pick(read_log(log))
    images = []
    for label, movie in picks:
        img = Image.open(frame_path(folder, movie)).convert("RGB")
        img = img.resize((THUMB_WIDTH, int(img.height * THUMB_WIDTH / img.width)))
        images.append((label, img))
    h = images[0][1].height
    strip = Image.new("RGB", (THUMB_WIDTH * len(images), h + LABEL_HEIGHT), (20, 20, 20))
    draw = ImageDraw.Draw(strip)
    for i, (label, img) in enumerate(images):
        strip.paste(img, (i * THUMB_WIDTH, 0))
        draw.text((i * THUMB_WIDTH + 8, h + 6), label + "  [fixture capture]", fill=(230, 230, 230))
    strip.save(os.path.join(folder, "strip.png"))
    keep = {os.path.basename(frame_path(folder, m)) for _, m in picks} | {"strip.png"}
    removed = 0
    for name in os.listdir(folder):
        if name.endswith(".png") and name not in keep:
            os.remove(os.path.join(folder, name))
            removed += 1
    print("strip.png from", [m for _, m in picks], "- removed", removed, "other frames")


main()
