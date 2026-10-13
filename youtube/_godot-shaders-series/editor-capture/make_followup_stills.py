#!/usr/bin/env python3
"""make_followup_stills.py <run_root> <png_out_dir> [--prefix renderer-path_]

<run_root> holds editor/, pm/ and fresh/ (each: states.json + named/*.png written by extract_marks.py).
Copies every named still to <png_out_dir>, and adds crops cut from those SAME frames (nothing is redrawn):
  <name>.dialog.png          the decorated embedded dialog (title bar included), cut with the window rectangle the driver logged with the mark
  <name>.renderer-block.png  Project Manager only: the Renderer: label, the three radio buttons, the bullet list and the footer sentence
  <name>.title-strip.png     the top strip of the editor window (the title bar), full width
Then two composites made from two real frames (cropped, never retouched, no labels drawn):
  renderer-path_R3_title-bar_OFF-vs-ON_side-by-side.png   right part of the title bar, setting OFF on the left, ON on the right
  renderer-path_R3_title-bar_OFF-over-ON_stacked.png      the full-width title strips, OFF above ON
Writes <png_out_dir>/stills.json (what each file is, which frame it came from, its size).
"""
import argparse, json, os, shutil, sys
from PIL import Image

POPUP_CLASSES = ("PopupMenu", "PopupPanel", "Popup")

ap = argparse.ArgumentParser()
ap.add_argument("run_root")
ap.add_argument("out_dir")
ap.add_argument("--prefix", default="renderer-path_")
a = ap.parse_args()
os.makedirs(a.out_dir, exist_ok=True)

index = {}

def clamp(box, size):
    x0, y0, x1, y1 = box
    return (max(0, int(x0)), max(0, int(y0)), min(size[0], int(x1)), min(size[1], int(y1)))

def window_size(log, mark):
    return mark.get("window_size") or log.get("window_size")

for part in ("editor", "pm", "fresh"):
    root = os.path.join(a.run_root, part)
    states = os.path.join(root, "states.json")
    named = os.path.join(root, "named")
    if not (os.path.isfile(states) and os.path.isdir(named)):
        print("skip", part, "(no states.json / named/)")
        continue
    log = json.load(open(states))
    marks_json = json.load(open(os.path.join(named, "marks.json")))["marks"]
    dumps = {d["name"]: d for d in log.get("dumps", [])}
    for name, m in log["marks"].items():
        src = os.path.join(named, name + ".png")
        if not os.path.isfile(src):
            continue
        dst = os.path.join(a.out_dir, a.prefix + name + ".png")
        shutil.copyfile(src, dst)
        im = Image.open(dst).convert("RGB")
        rec = {"file": os.path.basename(dst), "size": list(im.size), "session": part, "process_frame": m.get("process_frame"),
               "movie_file": marks_json[name]["file"], "settled": marks_json[name]["settled"], "settle_info": marks_json[name]["settle_info"], "crops": {}}
        ws = window_size(log, m) or list(im.size)
        sx, sy = im.size[0] / float(ws[0]), im.size[1] / float(ws[1])
        # dialog crop
        dialogs = [w for w in m.get("open_windows", []) if w.get("embedded") and w.get("class") not in POPUP_CLASSES and w["size"][0] > 300]
        if dialogs:
            w = dialogs[-1]
            th = float(w.get("title_height", 0))   # the drawn frame is the client rectangle plus the title bar above it (the logged border margins are inside it)
            box = clamp(((w["position"][0] - 3) * sx, (w["position"][1] - th - 3) * sy, (w["position"][0] + w["size"][0] + 3) * sx, (w["position"][1] + w["size"][1] + 3) * sy), im.size)
            crop = im.crop(box)
            p = os.path.join(a.out_dir, a.prefix + name + ".dialog.png")
            crop.save(p)
            rec["crops"]["dialog"] = {"file": os.path.basename(p), "size": list(crop.size), "window": {"class": w["class"], "title": w.get("title", "")}}
        # PM renderer block
        if part == "pm" and dialogs and name.startswith(("R4-B", "R4-C", "R4-D")):
            key = {"R4-B": "create-dialog-forward-plus", "R4-C": "create-dialog-mobile", "R4-D": "create-dialog-compatibility"}[name[:4]]
            d = dumps.get(key)
            if d:
                w = dialogs[-1]
                ys = []; xs = []
                for e in d["texts"]:
                    t = e.get("text", "")
                    if e["class"] in ("Label", "CheckBox") and e.get("rect_px") and (t == "Renderer:" or t in ("Forward+", "Mobile", "Compatibility") or t.startswith("•") or t.startswith("The renderer can be changed")):
                        x, y, ww, hh = e["rect_px"]
                        ys += [y, y + hh]; xs += [x, x + ww]
                if ys:
                    x0 = w["position"][0]; y0 = w["position"][1]
                    box = clamp(((x0 - 10) * sx, (y0 + min(ys) - 12) * sy, (x0 + w["size"][0] + 10) * sx, (y0 + max(ys) + 14) * sy), im.size)
                    crop = im.crop(box)
                    p = os.path.join(a.out_dir, a.prefix + name + ".renderer-block.png")
                    crop.save(p)
                    rec["crops"]["renderer_block"] = {"file": os.path.basename(p), "size": list(crop.size)}
        # title strip (editor sessions)
        if part in ("editor", "fresh"):
            h = int(round(90 * sy))
            strip = im.crop((0, 0, im.size[0], h))
            p = os.path.join(a.out_dir, a.prefix + name + ".title-strip.png")
            strip.save(p)
            rec["crops"]["title_strip"] = {"file": os.path.basename(p), "size": list(strip.size)}
        index[name] = rec

# composites from two real frames
def load(name):
    return Image.open(os.path.join(a.out_dir, a.prefix + name + ".png")).convert("RGB")

offname, onname = "R3-A_title-bar_selector-OFF-default", "R3-B_title-bar_selector-ON"
if offname in index and onname in index:
    off, on = load(offname), load(onname)
    W, H = off.size
    sy = H / 1944.0 if H != 1944 else 1.0
    sy = H / (1944.0)
    h = int(round(90 * (H / 1944.0)))
    x0 = int(W * 0.64)   # starts right of the last tab label (Asset Store), so only the run buttons and the selector are in the crop
    gap = max(6, W // 160)
    left, right = off.crop((x0, 0, W, h)), on.crop((x0, 0, W, h))
    comp = Image.new("RGB", (left.width * 2 + gap, h), (96, 96, 96))
    comp.paste(left, (0, 0)); comp.paste(right, (left.width + gap, 0))
    p = os.path.join(a.out_dir, a.prefix + "R3_title-bar_OFF-vs-ON_side-by-side.png")
    comp.save(p)
    index["R3_title-bar_OFF-vs-ON_side-by-side"] = {"file": os.path.basename(p), "size": list(comp.size), "session": "composite",
        "made_from": [index[offname]["file"], index[onname]["file"]], "note": "left = setting OFF, right = setting ON; right 36% of the title bar of each real frame; the grey strip between them is a spacer, not part of either frame"}
    stack = Image.new("RGB", (W, h * 2 + gap), (96, 96, 96))
    stack.paste(off.crop((0, 0, W, h)), (0, 0)); stack.paste(on.crop((0, 0, W, h)), (0, h + gap))
    p2 = os.path.join(a.out_dir, a.prefix + "R3_title-bar_OFF-over-ON_stacked.png")
    stack.save(p2)
    index["R3_title-bar_OFF-over-ON_stacked"] = {"file": os.path.basename(p2), "size": list(stack.size), "session": "composite",
        "made_from": [index[offname]["file"], index[onname]["file"]], "note": "top = setting OFF, bottom = setting ON; full-width title bars; the grey strip is a spacer"}
else:
    print("composite skipped: need", offname, "and", onname)

json.dump(index, open(os.path.join(a.out_dir, "stills.json"), "w"), indent=1)
print("wrote %d entries to %s" % (len(index), os.path.join(a.out_dir, "stills.json")))
for k, v in index.items():
    print("  %-78s %s  %s" % (k, "x".join(map(str, v["size"])), ", ".join(sorted(v.get("crops", {}).keys()))))
