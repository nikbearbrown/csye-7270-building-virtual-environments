"""Cut each gameplay beat's window out of the native 4K captures into media/<BID>.mp4.

  python tools/conform.py <capture-folder-with-clip.avi>

Narration is the master clock: each beat uses contiguous windows of real capture,
trimmed only. A shortfall is padded with a freeze of the last frame, labelled
"HELD FRAME". Nothing is retimed. Every capture beat carries a burned label saying
what it is. B07/B10 keep the game's own audio (clock: source); the rest are silent
(the compiler lays narration over them). B12/B16 are labelled still-image holds.
"""
import json, subprocess, sys
from pathlib import Path

REEL = Path(__file__).resolve().parents[1]
CAP = Path(sys.argv[1])
sheet = json.loads((REEL / "beat_sheet.json").read_text(encoding="utf-8"))
dur = {b["beat_id"]: b.get("actual_duration_s") for b in sheet["beats"]}
FONT = "C\\:/Windows/Fonts/msyh.ttc"
LABEL = "Real Godot capture · scripted input · isolated clone of 111bf6e"

# The death frame comes from the take's own input log (hp <= 0), so the windows
# follow the recording rather than a guess.
DEATH_T = next(json.loads(l)["frame"] for l in (CAP / "death-inputs.jsonl").read_text(encoding="utf-8").splitlines()
               if '"hp_zero_or_timeout"' in l) / 30.0
B09_PAUSE = (33.8, 41.0)
B09_DEATH_START = DEATH_T + 1.5 - (dur["B09"] - (B09_PAUSE[1] - B09_PAUSE[0]))

# beat -> list of (clip, start_s, end_s); end None = to fit narration
PLAN = {
    "B02": [("hall", 1.0, None)],
    "B04": [("combat", 0.7, None)],
    "B06": [("warehouse", 2.0, None)],
    "B07": [("warehouse", 2.0, 34.9)],
    "B09": [("combat", *B09_PAUSE), ("death", B09_DEATH_START, None)],
    "B10": [("death", DEATH_T + 0.5, DEATH_T + 13.5)],
    "B14": [("extract", 0.7, None)],
}
SOURCE = {"B07": "SLICE AUDIO · no narration · base music, lights on, racks, lights off",
          "B10": "SLICE AUDIO · no narration · killed on floor 31, field music stops, STING-FAIL"}
EXTRA = {"B09": "camp 30|31 unlocked in memory (stands in for floors 1–30)",
         "B14": "camp 10|11 unlocked in memory · real mouse click on 撤离"}


def run(cmd):
    subprocess.run(cmd, check=True)


def esc(t):
    return t.replace("\\", "\\\\").replace(":", "\\:").replace("'", "’").replace(",", "\\,")


def label_filter(bid):
    text = SOURCE.get(bid, LABEL)
    f = (f"drawbox=x=60:y=ih-150:w=iw*0.62:h=96:color=black@0.62:t=fill,"
         f"drawtext=fontfile='{FONT}':text='{esc(text)}':x=96:y=h-128:fontsize=44:fontcolor=white")
    if bid in EXTRA:
        f += (f",drawbox=x=60:y=ih-250:w=iw*0.62:h=90:color=black@0.62:t=fill,"
              f"drawtext=fontfile='{FONT}':text='{esc(EXTRA[bid])}':x=96:y=h-228:fontsize=40:fontcolor=#ffd75e")
    return f


def conform(bid, parts):
    target = dur[bid] if bid not in SOURCE else None
    pieces, used = [], 0.0
    for i, (clip, a, b) in enumerate(parts):
        src = CAP / f"{clip}.avi"
        if b is None:
            b = a + max(0.5, target - used)
        piece = REEL / "media" / f"_{bid}_{i}.mp4"
        audio = ["-c:a", "aac", "-b:a", "192k"] if bid in SOURCE else ["-an"]
        run(["ffmpeg", "-v", "error", "-y", "-ss", f"{a:.3f}", "-to", f"{b:.3f}", "-i", str(src),
             "-vf", label_filter(bid), "-r", "30", "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p",
             *audio, str(piece)])
        probe = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(piece)],
                               capture_output=True, text=True).stdout.strip()
        used += float(probe)
        pieces.append(piece)
    out = REEL / "media" / f"{bid}.mp4"
    listing = REEL / "media" / f"_{bid}.txt"
    listing.write_text("".join(f"file '{p.as_posix()}'\n" for p in pieces), encoding="utf-8")
    pad = (target - used) if target else 0.0
    vf = []
    if pad > 0.05:
        vf = ["-vf", f"tpad=stop_mode=clone:stop_duration={pad:.3f},"
                     f"drawtext=fontfile='{FONT}':text='HELD FRAME':x=w-360:y=60:fontsize=48:fontcolor=white:"
                     f"box=1:boxcolor=black@0.6:enable='gte(t,{used:.3f})'"]
    audio = ["-c:a", "aac"] if bid in SOURCE else ["-an"]
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(listing), *vf,
         "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", *audio, str(out)])
    for p in pieces: p.unlink()
    listing.unlink()
    print(bid, f"{used:.2f}s capture", f"+{pad:.2f}s held" if pad > 0.05 else "")


def still(bid, image, label):
    out = REEL / "media" / f"{bid}.mp4"
    run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-framerate", "30", "-t", f"{dur[bid]:.3f}", "-i", str(REEL / image),
         "-vf", f"drawtext=fontfile='{FONT}':text='{esc(label)}':x=210:y=h-200:fontsize=44:fontcolor=#2f2b26:box=1:boxcolor=#e9e4d8:boxborderw=18",
         "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", "-an", str(out)])
    print(bid, "still", dur[bid])


only = sys.argv[2:] or list(PLAN) + ["B12", "B16"]
for bid in only:
    if bid in PLAN: conform(bid, PLAN[bid])
    elif bid == "B12": still(bid, "images/B12-asset-trace.png", "STILL IMAGES · real files + engine screenshot")
    elif bid == "B16": still(bid, "images/B16-test-output.png", "RECORDED TEST OUTPUT · fresh clone")
