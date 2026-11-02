"""Make media/B06.mp4 from the native 4K tablet-run-02 PNG take and burn in a disclosure label.

No retiming, trimming or slow motion. If the measured narration is longer than the take, pass
--hold <seconds>: the last frame is held and a second label says so ("held frame").
Run: python -I scripts/prepare_media.py [--hold S]
"""
import subprocess
import sys
from pathlib import Path

REEL = Path(__file__).resolve().parents[1]
FRAMES = REEL.parents[1] / "captures" / "tablet-run-02" / "frames"
FONT = Path("<brutalist.art>/runtime/fonts/Lato/static/Lato-Bold.ttf").as_posix().replace(":", "\\:")
N = 391                                    # frames f00000-f00390, 30 fps, 13.03 s
hold = float(sys.argv[sys.argv.index("--hold") + 1]) if "--hold" in sys.argv else 0.0


def esc(t):
    return t.replace(":", "\\:").replace("'", "’")


label = esc("Native Godot 4.7.2 render  ·  3840x2160  ·  scripted input (Tab key, one mouse turn), not a human "
            "playtest  ·  offline 30 fps capture")
vf = (f"drawbox=x=0:y=ih-150:w=iw:h=150:color=black@0.6:t=fill,"
      f"drawtext=fontfile='{FONT}':text='{label}':fontcolor=white:fontsize=50:x=90:y=h-104")
if hold > 0:
    vf += (f",tpad=stop_mode=clone:stop_duration={hold},"
           f"drawtext=fontfile='{FONT}':text='{esc('held final frame')}':fontcolor=white:fontsize=50:"
           f"x=w-tw-90:y=60:enable='gte(t,{N / 30:.4f})'")
(REEL / "media").mkdir(exist_ok=True)
out = REEL / "media" / "B06.mp4"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", "30", "-start_number", "0",
                "-i", str(FRAMES / "f%05d.png"), "-frames:v", str(N + round(hold * 30)), "-vf", vf,
                "-c:v", "libx264", "-preset", "slow", "-crf", "12", "-pix_fmt", "yuv420p", "-r", "30", "-an",
                str(out)], check=True)
info = subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-show_entries",
                       "stream=nb_read_frames,width,height", "-of", "csv=p=0", str(out)],
                      capture_output=True, text=True).stdout.strip()
print("media/B06.mp4", info)
