#!/usr/bin/env python3
"""verify_recorded_clips.py <dir with the recorded MP4s>: is every capture there, at the right size, rate and length?

For each of the nineteen captures (names and lengths from capture_list.py) it reads the clip with ffprobe and checks: 3840 x 2160, 30 fps,
and a frame count equal to the beat's length x 30 (the length capture_all.sh was given). Prints one line per clip and a summary; exit code 1
if any clip is missing or wrong. It does not judge the picture: LOOK at capture_contact_sheet.py's sheet for that.
Needs ffprobe on PATH. Stdlib only.
"""
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main():
    folder = Path(sys.argv[1])
    rows = [line.split("\t") for line in subprocess.run([sys.executable, str(HERE / "capture_list.py")], capture_output=True, text=True, check=True).stdout.splitlines() if line.strip()]
    bad = 0
    for cid, name, beat, secs, src in rows:
        f = folder / name
        if not f.exists():
            print(f"{cid} {name}: MISSING")
            bad += 1
            continue
        r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-count_frames", "-show_entries", "stream=nb_read_frames,width,height,r_frame_rate", "-of", "json", str(f)],
                           capture_output=True, text=True)
        s = json.loads(r.stdout)["streams"][0]
        expected = round(float(secs) * 30)
        ok = int(s["nb_read_frames"]) == expected and s["width"] == 3840 and s["height"] == 2160 and s["r_frame_rate"] == "30/1"
        bad += not ok
        print(f"{cid} {name} beat {beat} {secs} s ({src}): {s['nb_read_frames']} frames, expected {expected}, {s['width']} x {s['height']}, {s['r_frame_rate']} fps  {'OK' if ok else 'MISMATCH'}")
    print(f"\n{len(rows) - bad} of {len(rows)} clips as expected")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
