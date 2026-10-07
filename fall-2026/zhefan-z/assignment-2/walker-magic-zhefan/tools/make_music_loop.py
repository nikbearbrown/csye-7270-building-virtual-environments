"""Cut MUS-LOOP from the Lyria track: zero-crossing loop points and a 50 ms seam crossfade.

    E:/7270/tools/ComfyUI/.venv/Scripts/python.exe tools/make_music_loop.py preview
        -> E:\\7270\\tools\\music_raw\\preview\\ (outside the repo): a 3x repeat WAV, a seam waveform PNG and
           loop.json. Listen to the two seams before exporting.
    E:/7270/tools/ComfyUI/.venv/Scripts/python.exe tools/make_music_loop.py export
        -> assets/audio/music/MUS-LOOP.ogg (OGG Vorbis q6) and assets/audio/MUSIC-EDIT-LOG.md / music-edit-log.json.
           Loop on import is set by tools/set_ogg_loop.gd afterwards.

Source: E:\\7270\\tools\\music_raw\\Beneath_the_Unlit_Stone.mp3 (Google Gemini, Lyria). Never copied into the repo.
Needs NumPy, Pillow (ComfyUI venv) and FFmpeg on PATH.
"""

import datetime
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

REPO = Path(__file__).resolve().parent.parent
SRC = Path(r"E:\7270\tools\music_raw\Beneath_the_Unlit_Stone.mp3")
PREVIEW = Path(r"E:\7270\tools\music_raw\preview")
OUT = REPO / "assets" / "audio" / "music" / "MUS-LOOP.ogg"
LOG_MD = REPO / "assets" / "audio" / "MUSIC-EDIT-LOG.md"
LOG_JSON = REPO / "assets" / "audio" / "music-edit-log.json"

RATE = 44100
LOOP_START_S = 60.886     # suggested by Claude's waveform analysis in chat; 12 bars at about 52.7 bpm
LOOP_END_S = 115.510
SNAP_WINDOW_S = 0.010     # search this far either side for a rising zero crossing
CROSSFADE_S = 0.050
OGG_QUALITY = 6


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def decode(path):
    raw = subprocess.run([shutil.which("ffmpeg"), "-v", "error", "-i", str(path), "-f", "f32le", "-ac", "2",
                          "-ar", str(RATE), "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, "<f4").reshape(-1, 2).astype(np.float64)


def snap_to_zero_crossing(x, idx):
    """Nearest rising zero crossing of the mono mix within SNAP_WINDOW_S (any crossing if none rises)."""
    m = x.mean(axis=1)
    w = int(SNAP_WINDOW_S * RATE)
    lo, hi = max(1, idx - w), min(len(m) - 1, idx + w)
    seg_prev, seg = m[lo - 1:hi - 1], m[lo:hi]
    rising = np.where((seg_prev < 0) & (seg >= 0))[0] + lo
    any_cross = np.where(np.signbit(seg_prev) != np.signbit(seg))[0] + lo
    cands = rising if len(rising) else any_cross
    best = int(cands[np.argmin(np.abs(cands - idx))]) if len(cands) else idx
    return best, ("rising" if len(rising) else "any") if len(cands) else "none"


def build_loop(x):
    a0, b0 = int(round(LOOP_START_S * RATE)), int(round(LOOP_END_S * RATE))
    a, a_kind = snap_to_zero_crossing(x, a0)
    b, b_kind = snap_to_zero_crossing(x, b0)
    n = int(round(CROSSFADE_S * RATE))
    loop = x[a:b].copy()
    t = np.linspace(0.0, 1.0, n, endpoint=False)[:, None]
    # Equal-power crossfade: the loop's last 50 ms fades out while the 50 ms just before the loop
    # start fades in, so the loop ends on the audio that originally led into its first sample.
    loop[-n:] = loop[-n:] * np.cos(t * np.pi / 2) + x[a - n:a] * np.sin(t * np.pi / 2)
    d = np.abs(np.diff(loop.mean(axis=1)))
    seam_jump = float(np.abs(loop[0] - loop[-1]).max())
    info = {
        "source": str(SRC), "source_sha256": sha256(SRC), "rate": RATE,
        "requested_s": [LOOP_START_S, LOOP_END_S],
        "snapped_samples": [a, b], "snapped_s": [round(a / RATE, 6), round(b / RATE, 6)],
        "snap_shift_ms": [round((a - a0) / RATE * 1000, 3), round((b - b0) / RATE * 1000, 3)],
        "snap_kind": [a_kind, b_kind],
        "loop_length_s": round(len(loop) / RATE, 6), "loop_samples": len(loop),
        "bars_at_52_7_bpm": round(len(loop) / RATE / (4 * 60 / 52.7), 3),
        "crossfade_ms": CROSSFADE_S * 1000, "crossfade": "equal-power (cos/sin)",
        "seam_sample_jump": round(seam_jump, 5),
        "median_sample_step": round(float(np.median(d)), 5), "p99_sample_step": round(float(np.percentile(d, 99)), 5),
    }
    return loop, info


def write_wav(y, path):
    subprocess.run([shutil.which("ffmpeg"), "-hide_banner", "-loglevel", "error", "-y", "-f", "f32le", "-ar", str(RATE),
                    "-ac", "2", "-i", "-", "-c:a", "pcm_s16le", str(path)], input=y.astype("<f4").tobytes(), check=True)


def seam_png(y, seams, path, half_ms=25):
    """Waveform of the mono mix around each seam of the 3x render (seam = red line)."""
    h = int(half_ms / 1000 * RATE)
    W, H = 900, 180
    img = Image.new("RGB", (W, H * len(seams) + 10 * (len(seams) - 1)), (245, 245, 248))
    d = ImageDraw.Draw(img)
    m = y.mean(axis=1)
    peak = max(np.abs(m[s - h:s + h]).max() for s in seams) or 1.0
    for k, s in enumerate(seams):
        top = k * (H + 10)
        seg = m[s - h:s + h]
        pts = [(i * (W - 1) / (len(seg) - 1), top + H / 2 - v / peak * (H / 2 - 8)) for i, v in enumerate(seg)]
        d.line([(0, top + H / 2), (W, top + H / 2)], fill=(200, 200, 210))
        d.line(pts, fill=(30, 40, 90), width=1)
        d.line([(W / 2, top), (W / 2, top + H)], fill=(220, 40, 60), width=1)
        d.text((6, top + 4), f"seam {k + 1}: +-{half_ms} ms", fill=(20, 20, 30))
    img.save(path)


def preview():
    x = decode(SRC)
    loop, info = build_loop(x)
    PREVIEW.mkdir(parents=True, exist_ok=True)
    y = np.tile(loop, (3, 1))
    wav = PREVIEW / "MUS-LOOP-preview-3x.wav"
    write_wav(y, wav)
    png = PREVIEW / "MUS-LOOP-seams.png"
    seam_png(y, [len(loop), 2 * len(loop)], png)
    info.update(preview_wav=str(wav), preview_wav_s=round(len(y) / RATE, 3), seam_times_in_preview_s=[
        round(len(loop) / RATE, 3), round(2 * len(loop) / RATE, 3)], seam_png=str(png))
    (PREVIEW / "loop.json").write_text(json.dumps(info, indent=2), encoding="utf-8")
    print(json.dumps(info, indent=2))


def export():
    x = decode(SRC)
    loop, info = build_loop(x)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run([shutil.which("ffmpeg"), "-hide_banner", "-loglevel", "error", "-y", "-f", "f32le", "-ar", str(RATE),
                    "-ac", "2", "-i", "-", "-c:a", "libvorbis", "-q:a", str(OGG_QUALITY), str(OUT)],
                   input=loop.astype("<f4").tobytes(), check=True)
    back = decode(OUT)
    info.update(ogg=str(OUT.relative_to(REPO)).replace("\\", "/"), ogg_quality=OGG_QUALITY, ogg_sha256=sha256(OUT),
                ogg_decoded_samples=len(back), ogg_decoded_s=round(len(back) / RATE, 6),
                peak_dbfs=round(20 * np.log10(np.abs(back).max()), 2))
    now = datetime.datetime.now().astimezone().isoformat(timespec="seconds")
    LOG_JSON.write_text(json.dumps({"generated": now, **info}, indent=2), encoding="utf-8")
    LOG_MD.write_text("\n".join([
        "# Music edit log (MUS-LOOP)", "", f"Generated by `tools/make_music_loop.py export` on {now}. Full data: `music-edit-log.json`.", "",
        "Source: `Beneath_the_Unlit_Stone.mp3` from Google Gemini (Lyria), kept outside the repo; see SOURCES.md for the "
        "model, prompt and SynthID note.", "",
        "| Edit | Value |", "|---|---|",
        f"| Loop points requested | {LOOP_START_S} s – {LOOP_END_S} s (suggested by Claude's waveform analysis in chat; confirmed by the author's listening) |",
        f"| Snapped to rising zero crossings | {info['snapped_s'][0]} s – {info['snapped_s'][1]} s (shift {info['snap_shift_ms'][0]} ms / {info['snap_shift_ms'][1]} ms) |",
        f"| Loop length | {info['loop_length_s']} s ({info['loop_samples']} samples, {info['bars_at_52_7_bpm']} bars at 52.7 bpm) |",
        f"| Seam crossfade | last {info['crossfade_ms']:.0f} ms of the loop into the {info['crossfade_ms']:.0f} ms before the loop start, equal-power |",
        f"| Seam sample jump | {info['seam_sample_jump']} (median step {info['median_sample_step']}, 99th percentile {info['p99_sample_step']}) |",
        f"| Export | OGG Vorbis q{OGG_QUALITY} (FFmpeg libvorbis), `{info['ogg']}`, decodes to {info['ogg_decoded_s']} s, peak {info['peak_dbfs']} dBFS |",
        "| Godot import | loop enabled on import (`MUS-LOOP.ogg.import`: `loop=true`) |",
    ]) + "\n", encoding="utf-8")
    print(json.dumps(info, indent=2))


if __name__ == "__main__":
    {"preview": preview, "export": export}[sys.argv[1] if len(sys.argv) > 1 else "preview"]()
