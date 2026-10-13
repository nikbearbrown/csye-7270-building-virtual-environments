#!/usr/bin/env python3
"""capture_list.py: which beat owns which capture, and how long that beat is.

Prints one tab-separated line per capture, in capture order:
    C01  hook-walk.mp4  B01  12.20  estimate
columns: capture id, output file name (the file the lane names), beat id, seconds, where the seconds come from
("measured" = actual_duration_s and audio_file written by generate_audio_kokoro.py, "estimate" = estimated_duration_s of the layout).

Reads ../../lanes/act*.json (capture_spec begins with the capture id; props.video names the file) and ../../beat_sheet.json.
Stdlib only. Usage: python3 capture_list.py [--json]
"""
import glob
import json
import re
import sys
from pathlib import Path

FILM = Path(__file__).resolve().parents[2]


def main():
    lanes = {}
    for f in sorted(glob.glob(str(FILM / "lanes" / "act*.json"))):
        lanes.update(json.loads(Path(f).read_text()))
    sheet = json.loads((FILM / "beat_sheet.json").read_text())
    beats = {b["beat_id"]: b for b in sheet["beats"]}
    rows = []
    for bid, lane in sorted(lanes.items()):
        m = re.match(r"(C\d\d)\b", lane.get("capture_spec", ""))
        if not m:
            continue
        video = lane["props"]["video"].split("/")[-1]
        b = beats[bid]
        # generate_audio_kokoro.py pre-fills actual_duration_s from the estimate and overwrites it when it voices the beat, writing
        # audio_file at the same time: a beat counts as measured only when it has both
        if b.get("actual_duration_s") and b.get("audio_file"):
            secs, src = float(b["actual_duration_s"]), "measured"
        else:
            secs, src = float(b["estimated_duration_s"]), "estimate"
        rows.append((m.group(1), video, bid, secs, src))
    rows.sort()
    if "--json" in sys.argv:
        print(json.dumps([dict(zip(("capture", "file", "beat", "seconds", "source"), r)) for r in rows], indent=1))
    else:
        for cid, video, bid, secs, src in rows:
            print(f"{cid}\t{video}\t{bid}\t{secs:.2f}\t{src}")


if __name__ == "__main__":
    main()
