"""Make media/B15.mp4 from the native 4K crates_open PNG take: encode frames 0-595 and burn in a label.

The take was captured at exactly B15's render length (596 frames at 30 fps, --fixed-fps 30), so no
retiming, trimming or slow motion is applied; only the disclosure label is drawn. The driver writes one
extra PNG after quit(); it is not encoded.
Run: python -I scripts/prepare_media.py <crates_open PNG folder> <path-to-Lato-Bold.ttf>
"""
import subprocess
import sys
from pathlib import Path

REEL = Path(__file__).resolve().parents[1]
frames = Path(sys.argv[1])
font = Path(sys.argv[2]).as_posix().replace(":", "\\:")
N = 596
label = ("Native Godot 4.7.2 render  ·  3840x2160  ·  base.tscn unchanged  ·  film camera and the crates' own "
         "open/close animations played by capture script  ·  no player, no input")
label = label.replace(":", "\\:").replace("'", "’")
vf = (f"drawbox=x=0:y=ih-150:w=iw:h=150:color=black@0.55:t=fill,"
      f"drawtext=fontfile='{font}':text='{label}':fontcolor=white:fontsize=50:x=90:y=h-104")
(REEL / "media").mkdir(exist_ok=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", "30", "-start_number", "0",
                "-i", str(frames / "f%05d.png"), "-frames:v", str(N), "-vf", vf,
                "-c:v", "libx264", "-preset", "slow", "-crf", "12", "-pix_fmt", "yuv420p", "-r", "30", "-an",
                str(REEL / "media" / "B15.mp4")], check=True)
out = subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-show_entries", "stream=nb_read_frames,width,height",
                      "-of", "csv=p=0", str(REEL / "media" / "B15.mp4")], capture_output=True, text=True).stdout.strip()
print("media/B15.mp4", out)
