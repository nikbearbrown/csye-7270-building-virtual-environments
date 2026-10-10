"""Make media/B14.mp4 from the native 4K pan capture: burn in a disclosure label.

The pan was captured at exactly B14's render length (614 frames at 30 fps), so
no retiming, trimming or slow-motion is applied; only the label is drawn.
Run: python -I scripts/prepare_media.py <path-to-Lato-Bold.ttf>
"""
import subprocess
import sys
from pathlib import Path

REEL = Path(__file__).resolve().parents[1]
font = Path(sys.argv[1]).as_posix().replace(":", "\\:")
label = ("Native Godot 4.7.2 render  ·  3840x2160  ·  base.tscn unchanged  ·  "
         "film camera added by capture script  ·  no player, no input")
label = label.replace(":", "\\:")
vf = (f"drawbox=x=0:y=ih-150:w=iw:h=150:color=black@0.55:t=fill,"
      f"drawtext=fontfile='{font}':text='{label}':fontcolor=white:fontsize=58:x=90:y=h-108")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(REEL / "capture/room_pan_b14.mp4"), "-vf", vf,
                "-c:v", "libx264", "-preset", "slow", "-crf", "12", "-pix_fmt", "yuv420p", "-r", "30", "-an",
                str(REEL / "media/B14.mp4")], check=True)
out = subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-show_entries", "stream=nb_read_frames,width,height",
                      "-of", "csv=p=0", str(REEL / "media/B14.mp4")], capture_output=True, text=True).stdout.strip()
print("media/B14.mp4", out)
