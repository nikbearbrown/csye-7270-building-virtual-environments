#!/usr/bin/env python3
"""capture_contact_sheet.py <dir with the recorded MP4s> <out.png>: LOOK at every capture before using it.

For each of the nineteen captures (names from capture_list.py) that exists in the folder, takes the frames at 50 % and 85 % of the clip (the
two frames Gate V samples), scales them to 480 x 270 and lays them out four captures to a row with a label (capture id, file, length,
frame count). A missing file is marked MISSING. Compare the sheet with evidence/planning-checks/png/contact-sheet-captures.png (the same
two marks from the planning runs) and with the last column of the capture table in CAPTURE-PLAN.md.
Needs ffmpeg and ffprobe on PATH and Pillow. Writes only <out.png> (and a temporary folder it removes with TemporaryDirectory).
"""
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
TILE = (480, 270)
BAND = 34


def plan():
    out = subprocess.run([sys.executable, str(HERE / "capture_list.py")], capture_output=True, text=True, check=True).stdout
    return [line.split("\t") for line in out.splitlines() if line.strip()]


def probe(path: Path):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-count_frames", "-show_entries", "stream=nb_read_frames,duration,width,height",
                        "-of", "default=nw=1", str(path)], capture_output=True, text=True)
    d = dict(line.split("=", 1) for line in r.stdout.split() if "=" in line)
    return float(d.get("duration", 0)), int(d.get("nb_read_frames", 0)), int(d.get("width", 0)), int(d.get("height", 0))


def frame_at(path: Path, t: float, tmp: Path, name: str) -> Image.Image:
    out = tmp / name
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{t:.3f}", "-i", str(path), "-frames:v", "1", "-vf", f"scale={TILE[0]}:{TILE[1]}", str(out)], check=True)
    return Image.open(out).convert("RGB")


def main():
    folder, out = Path(sys.argv[1]), Path(sys.argv[2])
    rows = plan()
    font = ImageFont.load_default(size=22)
    per_row = 4
    w = per_row * 2 * TILE[0]
    h = ((len(rows) + per_row - 1) // per_row) * (TILE[1] + BAND)
    sheet = Image.new("RGB", (w, h), (255, 255, 255))
    d = ImageDraw.Draw(sheet)
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        for i, (cid, name, beat, secs, src) in enumerate(rows):
            x0 = (i % per_row) * 2 * TILE[0]
            y0 = (i // per_row) * (TILE[1] + BAND)
            f = folder / name
            if not f.exists():
                d.rectangle([x0, y0, x0 + 2 * TILE[0] - 1, y0 + BAND + TILE[1] - 1], outline=(200, 0, 0), width=3)
                d.text((x0 + 10, y0 + 8), f"{cid} {name}: MISSING", fill=(200, 0, 0), font=font)
                continue
            dur, frames, vw, vh = probe(f)
            d.text((x0 + 8, y0 + 6), f"{cid} {name}  {dur:.1f} s  {frames} frames  {vw}x{vh}  (beat {beat}, {src})", fill=(30, 30, 30), font=font)
            for k, frac in enumerate((0.50, 0.85)):
                tile = frame_at(f, dur * frac, tmp, f"{cid}-{k}.png")
                sheet.paste(tile, (x0 + k * TILE[0], y0 + BAND))
                d.rectangle([x0 + k * TILE[0], y0 + BAND, x0 + (k + 1) * TILE[0] - 1, y0 + BAND + TILE[1] - 1], outline=(150, 150, 150))
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out)
    print("wrote", out, sheet.size)


if __name__ == "__main__":
    main()
