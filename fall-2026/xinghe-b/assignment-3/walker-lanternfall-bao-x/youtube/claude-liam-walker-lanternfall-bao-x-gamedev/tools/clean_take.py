#!/usr/bin/env python3
"""Remove the stale Movie Maker frames of a take, with their audio, so frame n of the result is game frame n.

While the capture window could not draw (macOS occlusion), the capture driver paused the whole game and logged
each such engine iteration as stale (capture_driver.gd, _hold_for_window). Movie Maker still wrote a frame and an
audio chunk (1600 samples at 48 kHz / 30 fps) for those iterations. This drops the same index range from both,
with a 4 ms crossfade at each audio splice, and writes capture/clean/<take>.mov (H.264 CRF 10 + PCM).
A take with no stale frames is not rewritten: its AVI is used as it is.

    gen/.venv-audio/bin/python tools/clean_take.py capture/take-lose-seed3.avi
"""
import hashlib, json, subprocess, sys, tempfile
from pathlib import Path
import numpy as np
import soundfile as sf

REEL = Path(__file__).resolve().parents[1]
SPF = 1600   # audio samples per video frame


def runs(idx):
    out = []
    for i in sorted(idx):
        if out and i == out[-1][1] + 1:
            out[-1][1] = i
        else:
            out.append([i, i])
    return out


def main() -> None:
    avi = (REEL / sys.argv[1]).resolve() if not Path(sys.argv[1]).is_absolute() else Path(sys.argv[1])
    log = avi.with_name(avi.stem + "-inputs.jsonl")
    events = [json.loads(l) for l in log.read_text().splitlines()]
    stale = next(e for e in events if e["event"] == "movie_frames")["stale"]
    note = {"take": avi.name, "source_sha256": hashlib.sha256(avi.read_bytes()).hexdigest(), "stale_frames": stale}
    out_dir = REEL / "capture" / "clean"
    out_dir.mkdir(exist_ok=True)
    if not stale:
        note["result"] = "no stale frames; the AVI is used unchanged"
        (out_dir / (avi.stem + ".json")).write_text(json.dumps(note, indent=1))
        print(note["result"])
        return
    spans = runs(stale)
    with tempfile.TemporaryDirectory() as tmp:
        wav = Path(tmp) / "a.wav"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(avi), "-map", "0:a", "-c:a", "pcm_s16le", str(wav)], check=True)
        a, sr = sf.read(wav, dtype="float32")
        assert sr == 48000, sr
        keep, cursor, fade = [], 0, int(0.004 * sr)
        w = np.linspace(0, 1, fade, dtype=np.float32)[:, None]
        for s, e in spans:
            keep.append(a[cursor:s * SPF])
            cursor = (e + 1) * SPF
            if s > 0:   # crossfade from the audio that continued into the first dropped chunk into the resumed audio
                right = a[cursor:cursor + fade].copy()
                a[cursor:cursor + fade] = a[s * SPF:s * SPF + fade] * (1 - w) + right * w
        keep.append(a[cursor:])
        joined = np.concatenate(keep)
        clean_wav = Path(tmp) / "clean.wav"
        sf.write(clean_wav, joined, sr, subtype="PCM_16")
        expr = "+".join(f"between(n\\,{s}\\,{e})" for s, e in spans)
        out = out_dir / (avi.stem + ".mov")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(avi), "-i", str(clean_wav),
                        "-vf", f"select='not({expr})',setpts=N/30/TB", "-map", "0:v", "-map", "1:a",
                        "-c:v", "libx264", "-preset", "medium", "-crf", "10", "-pix_fmt", "yuv420p", "-r", "30",
                        "-c:a", "pcm_s16le", str(out)], check=True)
    frames = int(subprocess.run(["ffprobe", "-v", "error", "-count_packets", "-select_streams", "v",
                                 "-show_entries", "stream=nb_read_packets", "-of", "csv=p=0", str(out)],
                                capture_output=True, text=True).stdout.strip())
    note.update({"result": str(out.relative_to(REEL)), "frames_after": frames, "audio_samples_after": len(joined),
                 "dropped_spans": spans, "crossfade_ms": 4, "clean_sha256": hashlib.sha256(out.read_bytes()).hexdigest()})
    assert len(joined) == frames * SPF, (len(joined), frames)
    (out_dir / (avi.stem + ".json")).write_text(json.dumps(note, indent=1))
    print(json.dumps(note, indent=1))


if __name__ == "__main__":
    main()
