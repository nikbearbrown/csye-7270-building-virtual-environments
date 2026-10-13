"""Pre-check Gate V (final_frame_check.analyze_frame) on the 50% and 85% frames of local 1080p clips."""
import sys, subprocess, importlib.util, tempfile, os
sys.path.insert(0, "/Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art/runtime/scripts")
spec = importlib.util.spec_from_file_location("fv", "/Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art/runtime/qc/final_frame_check.py")
fv = importlib.util.module_from_spec(spec); spec.loader.exec_module(fv)
d = tempfile.mkdtemp()
for mp4 in sys.argv[1:]:
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", mp4], capture_output=True, text=True).stdout)
    for frac in (0.5, 0.85):
        f = os.path.join(d, "f.png")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(dur * frac), "-i", mp4, "-frames:v", "1", f], check=True)
        defects, cover = fv.analyze_frame(f)
        hard = [x for x in defects if x[1] not in ("underfill", "clustered")]
        print(os.path.basename(mp4)[:-4], frac, f"cover={cover:.2f}", hard if hard else "ok", [x[1] for x in defects if x[1] in ("underfill", "clustered")])
