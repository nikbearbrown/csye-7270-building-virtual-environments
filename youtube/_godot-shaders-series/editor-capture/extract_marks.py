#!/usr/bin/env python3
"""extract_marks.py <states.json> <frames_dir> <out_dir> [--prefix P] [--only NAME ...] [--crop-inspector] [--quiet]

Turns one editor recording into named stills.

states.json is the driver log written by addons/driver/plugin.gd. Each mark maps a NAME to Engine.get_process_frames() at the moment the
mark step ran (also logged: Engine.get_frames_drawn(), which is NOT usable: the editor skips drawing while idle, so it falls behind the
movie). The movie writer writes one file per main-loop iteration, so file index = process frame + offset. The driver flashes the whole
editor magenta for 2 frames before any step; this helper finds the flash in the PNG sequence, computes offset = flash_file - flash
process frame (expected 0), and copies  f{process_frame+offset:08d}.png  to  <out_dir>/<PREFIX><NAME>.png  for every mark.

It also checks the frame is settled: it compares the copied frame with the next one. identical = nothing moved after the mark.
--crop-inspector additionally writes <NAME>.inspector.png, the Inspector column cut from the frame using the rectangle the driver
logged with the mark (inspector_rect_px, window pixels).
Writes <out_dir>/marks.json (name, frame, file, size, settled) and prints one line per mark.
"""
import argparse, json, os, shutil, sys
from PIL import Image, ImageChops


def magenta_fraction(path):
    im = Image.open(path).convert("RGB")
    im.thumbnail((96, 54))
    px = list(im.getdata()) if not hasattr(im, "get_flattened_data") else list(im.get_flattened_data())
    hit = sum(1 for r, g, b in px if r > 235 and g < 25 and b > 235)
    return hit / max(1, len(px))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("states")
    ap.add_argument("frames_dir")
    ap.add_argument("out_dir")
    ap.add_argument("--prefix", default="")
    ap.add_argument("--only", nargs="*", default=None)
    ap.add_argument("--crop-inspector", action="store_true")
    ap.add_argument("--crop-dock", action="store_true", help="also write <NAME>.dock.png, the whole right dock (tabs + Inspector) cut from the frame")
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args()

    log = json.load(open(a.states))
    files = sorted(f for f in os.listdir(a.frames_dir) if f.startswith("f") and f.endswith(".png"))
    if not files:
        sys.exit("no frames in " + a.frames_dir)
    n = len(files)
    index = {int(f[1:-4]): f for f in files}

    flash = log.get("flash")
    offset = 0
    flash_file = None
    if flash:
        f0 = int(flash.get("process_frame", flash["frame"]))
        for i in range(0, min(n, f0 + 80)):
            if i in index and magenta_fraction(os.path.join(a.frames_dir, index[i])) > 0.95:
                flash_file = i
                break
        if flash_file is None:
            print("WARNING: magenta flash not found in the first %d frames; assuming offset 0" % min(n, f0 + 80))
        else:
            offset = flash_file - f0
    else:
        print("WARNING: no flash record in the log; assuming offset 0")

    os.makedirs(a.out_dir, exist_ok=True)
    out = {}
    for name, m in log["marks"].items():
        if a.only is not None and name not in a.only:
            continue
        fr = int(m.get("process_frame", m["frame"]))
        idx = fr + offset
        if idx not in index:
            print("  MISSING frame for mark %s: wanted file index %d (frame %d + offset %d), have 0..%d" % (name, idx, fr, offset, n - 1))
            continue
        src = os.path.join(a.frames_dir, index[idx])
        dst = os.path.join(a.out_dir, a.prefix + name + ".png")
        shutil.copyfile(src, dst)
        im = Image.open(dst)
        settled = None
        if idx + 1 in index:
            nxt = Image.open(os.path.join(a.frames_dir, index[idx + 1]))
            diff = ImageChops.difference(im.convert("RGB"), nxt.convert("RGB")).getbbox()
            settled = diff is None
            settle_info = "identical to the next frame" if settled else "differs from the next frame inside %s" % (diff,)
        else:
            settle_info = "last frame of the recording (no next frame to compare)"
        rec = {"frame": fr, "file": index[idx], "png": dst, "size": list(im.size), "settled": settled, "settle_info": settle_info}
        win = log.get("window_size") or [im.size[0], im.size[1]]
        sx, sy = im.size[0] / float(win[0]), im.size[1] / float(win[1])
        for flag, key, suffix in ((a.crop_inspector, "inspector_rect_px", ".inspector.png"), (a.crop_dock, "inspector_dock_rect_px", ".dock.png")):
            if flag and m.get(key):
                x, y, w, h = m[key]
                box = (int(round(x * sx)), int(round(y * sy)), int(round((x + w) * sx)), int(round((y + h) * sy)))
                crop = im.crop(box)
                cdst = os.path.join(a.out_dir, a.prefix + name + suffix)
                crop.save(cdst)
                rec[key + "_crop"] = cdst
                rec[key + "_crop_size"] = list(crop.size)
        out[name] = rec
        if not a.quiet:
            print("  %-70s process frame %-5d -> %s  %dx%d  %s" % (name, fr, index[idx], im.size[0], im.size[1], settle_info))
    json.dump({"offset": offset, "flash_file_index": flash_file, "flash_process_frame": flash.get("process_frame") if flash else None, "total_frames": n, "marks": out},
              open(os.path.join(a.out_dir, a.prefix + "marks.json"), "w"), indent=2)
    print("offset (movie file index - Engine.get_process_frames) = %d (flash found at file %s); %d frames in the recording; %d stills written to %s" % (offset, flash_file, n, len(out), a.out_dir))


if __name__ == "__main__":
    main()
