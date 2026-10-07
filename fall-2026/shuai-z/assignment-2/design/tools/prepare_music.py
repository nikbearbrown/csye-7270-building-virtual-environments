"""Make the game's music loop from the accepted take in generated/accepted/.

The take is decoded at 48 kHz mono. The loop is 24 bars of it: the song's
harmony repeats every 24 bars, and at about 105 BPM that is 54.87 s. The end
point was moved 5.1 ms off the beat grid to where the waveform after it best
matches the waveform after the start. The beat after the end is crossfaded
(equal power) into the loop's first beat, so the last sample runs straight
into the first. The loop is then set to -16 LUFS, or lower if its peak would
pass -1 dBFS, and encoded with oggenc into game/systems/audio/music/. In
Godot, the file's import settings turn Loop on.

Needs ffmpeg (decoding, loudness) and oggenc (vorbis-tools).

Usage: python3 design/tools/prepare_music.py
"""

import re
import subprocess
import tempfile
import wave
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
TAKE = ROOT / "generated" / "accepted" / "MUS-LOOP-01.ogg"
OUT = ROOT / "game" / "systems" / "audio" / "music" / "MUS-LOOP.ogg"

RATE = 48000
START = 2588126  # 53.919 s: beat 94 of the grid, a downbeat
END = 5221757  # 108.787 s: 24 bars later
CROSSFADE = 27431  # one beat, 0.5715 s
TARGET_LUFS = -16.0
PEAK_DBFS = -1.0
QUALITY = 6  # oggenc -q, about 112 kbit/s for mono


def decode(path: Path) -> np.ndarray:
    raw = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", str(path), "-f", "f32le", "-ac", "1", "-ar", str(RATE), "-"],
        capture_output=True, check=True,
    ).stdout
    return np.frombuffer(raw, dtype=np.float32).astype(np.float64)


def write_wav(path: Path, mono: np.ndarray) -> None:
    pcm = np.round(np.clip(mono, -1.0, 1.0) * 32767.0).astype(np.int16)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(RATE)
        w.writeframes(pcm.tobytes())


def loudness(path: Path) -> float:
    log = subprocess.run(
        ["ffmpeg", "-hide_banner", "-nostats", "-i", str(path), "-af", "ebur128", "-f", "null", "-"],
        capture_output=True, text=True, check=True,
    ).stderr
    return float(re.findall(r"I:\s+(-?[\d.]+) LUFS", log)[-1])


def make_loop(take: np.ndarray) -> np.ndarray:
    loop = take[START:END].copy()
    t = np.linspace(0.0, np.pi / 2, CROSSFADE)
    loop[:CROSSFADE] = take[START : START + CROSSFADE] * np.sin(t) + take[END : END + CROSSFADE] * np.cos(t)
    return loop


def main() -> None:
    loop = make_loop(decode(TAKE))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        wav = Path(tmp) / "loop.wav"
        write_wav(wav, loop)
        gain_db = min(TARGET_LUFS - loudness(wav), PEAK_DBFS - 20 * np.log10(np.abs(loop).max()))
        loop *= 10 ** (gain_db / 20)
        write_wav(wav, loop)
        lufs = loudness(wav)
        subprocess.run(["oggenc", "-Q", "-q", str(QUALITY), "-o", str(OUT), str(wav)], check=True)
    print(
        f"{OUT.name}  {len(loop)} samples ({len(loop) / RATE:.3f} s)  gain {gain_db:+.1f} dB  "
        f"{lufs:.1f} LUFS  peak {20 * np.log10(np.abs(loop).max()):.1f} dBFS"
    )


if __name__ == "__main__":
    main()
