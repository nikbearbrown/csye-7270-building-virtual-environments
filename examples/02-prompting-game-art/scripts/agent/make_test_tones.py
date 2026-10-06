#!/usr/bin/env python3
"""
Write 16-bit mono 44.1 kHz WAV test tones to godot/audio/placeholder/.

  jump.wav         80 ms   900 Hz sine,  72 complete cycles
                   Period = 49 samples (44100/900 = 49, exact integer)
                   3528 samples / 49 = 72 cycles

  fail.wav        250 ms   300 Hz sine,  75 complete cycles
                   Period = 147 samples (44100/300 = 147, exact integer)
                   11025 samples / 147 = 75 cycles

  music_loop.wav    4.0 s  100 Hz sine, 400 complete cycles
                   Period = 441 samples (44100/100 = 441, exact integer)
                   176400 samples / 441 = 400 cycles exactly
                   Zero crossing at sample 0 (sin(0) = 0); the mathematical
                   function returns to phase 0 at t = 4.000 s (100 * 4 = 400
                   integer), giving a seamless Forward loop from first to last
                   sample.  The loop seam audibility is a human check.

All output uses Python standard-library modules only (math, os, struct, wave).

Godot 4 WAV importer edit/loop_mode values (different from AudioStreamWAV.LoopMode):
  0 = Detect from file (reads SMPL chunk)  1 = Disabled  2 = Forward
  3 = Ping-pong  4 = Backward
music_loop.wav.import uses edit/loop_mode=2 (Forward).
"""

import math
import os
import struct
import wave

SR = 44_100           # sample rate (Hz)
AMPLITUDE = 0.5       # half scale; well below clip

_HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(_HERE, "..", "godot", "audio", "placeholder")


def _sine_bytes(freq_hz: float, n_samples: int) -> bytes:
    """Return little-endian 16-bit PCM bytes for one channel of a sine wave."""
    two_pi_f = 2.0 * math.pi * freq_hz / SR
    raw = [round(AMPLITUDE * 32767.0 * math.sin(two_pi_f * k))
           for k in range(n_samples)]
    return struct.pack(f"<{n_samples}h", *raw)


def write_tone(name: str, freq_hz: float, n_samples: int) -> None:
    os.makedirs(OUT_DIR, exist_ok=True)
    path = os.path.join(OUT_DIR, name)
    data = _sine_bytes(freq_hz, n_samples)
    with wave.open(path, "wb") as w:
        w.setnchannels(1)     # mono
        w.setsampwidth(2)     # 16-bit
        w.setframerate(SR)
        w.writeframes(data)
    duration_ms = n_samples * 1000 / SR
    cycles = n_samples / (SR / freq_hz)
    first = data[0:2]
    last  = data[-2:]
    s0 = struct.unpack("<h", first)[0]
    sN = struct.unpack("<h", last)[0]
    print(f"  {name}: {n_samples} samples  {duration_ms:.1f} ms  "
          f"{freq_hz:.0f} Hz  {cycles:.0f} cycles  "
          f"sample[0]={s0}  sample[N-1]={sN}")


if __name__ == "__main__":
    print(f"Output: {os.path.abspath(OUT_DIR)}")
    write_tone("jump.wav",        900.0,    3_528)   #  80 ms, period=49
    write_tone("fail.wav",        300.0,   11_025)   # 250 ms, period=147
    write_tone("music_loop.wav",  100.0,  176_400)   #   4 s,  period=441
    print("Done.")
