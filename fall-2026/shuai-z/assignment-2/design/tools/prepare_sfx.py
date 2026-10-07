"""Make the game's sound effects from the accepted takes in generated/accepted/.

For each sound: cut it to the start and end below (the start is where the sound
becomes audible, so it plays on the event's frame), fade in and out, mix to
mono, normalize the peak to -1 dBFS, and write 16-bit WAV at the take's sample
rate into game/systems/audio/sfx/. The take's XMP chunk, which links to its
Content Credentials, is copied into the game file unchanged.

The cut points were chosen from a 10 ms loudness envelope of each take.

Usage: python3 design/tools/prepare_sfx.py
"""

import struct
import wave
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "generated" / "accepted"
OUT = ROOT / "game" / "systems" / "audio" / "sfx"

PEAK_DBFS = -1.0

# ID: (accepted take, start ms, end ms, fade-in ms, fade-out ms)
CUTS = {
    # Before 210 ms the take is more than 30 dB under its peak (at 320 ms);
    # after 500 ms it is more than 44 dB under it.
    "SFX-JUMP": ("SFX-JUMP-04.wav", 210, 500, 5, 60),
    # The take starts at its peak, on a sample at 41% of full scale, so a 3 ms
    # fade-in removes the click. After 190 ms it is more than 33 dB under its
    # loudest 10 ms.
    "SFX-STOMP": ("SFX-STOMP-02.wav", 0, 320, 3, 100),
    # Loud from the first sample; after 120 ms it is more than 33 dB under its
    # loudest 10 ms, with only low noise left.
    "SFX-HURT": ("SFX-HURT-01.wav", 0, 200, 3, 60),
    # Swells from the start to its peak at about 0.5 s, then rings out; after
    # 1.56 s it is more than 50 dB under the peak. The file ends in a click.
    "SFX-PORTAL": ("SFX-PORTAL-02.wav", 0, 1680, 3, 200),
    # Silent for the first 50 ms; before 85 ms it is more than 30 dB under its
    # peak (at 240 ms), so the peak comes 155 ms after the key, inside the
    # hitbox's 0.03-0.18 s.
    "SFX-SLASH": ("SFX-SLASH-03.wav", 85, 400, 5, 80),
    # Starts at once; after 540 ms it is more than 50 dB under its loudest
    # 10 ms. The file ends in a click.
    "SFX-PICKUP": ("SFX-PICKUP-02.wav", 0, 600, 3, 120),
}


def read(path: Path) -> tuple[np.ndarray, int]:
    with wave.open(str(path)) as w:
        assert w.getsampwidth() == 2, f"{path.name}: expected 16-bit PCM"
        rate = w.getframerate()
        data = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16)
        data = data.reshape(-1, w.getnchannels()).astype(np.float64) / 32768.0
    return data.mean(axis=1), rate


def chunks(path: Path) -> dict[bytes, bytes]:
    data = path.read_bytes()
    assert data[:4] == b"RIFF" and data[8:12] == b"WAVE", f"{path.name}: not a WAV file"
    found, i = {}, 12
    while i + 8 <= len(data):
        cid, size = data[i : i + 4], struct.unpack("<I", data[i + 4 : i + 8])[0]
        found[cid] = data[i + 8 : i + 8 + size]
        i += 8 + size + (size & 1)
    return found


def write(path: Path, mono: np.ndarray, rate: int, xmp: bytes | None) -> None:
    pcm = np.round(np.clip(mono, -1.0, 1.0) * 32767.0).astype(np.int16)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(rate)
        w.writeframes(pcm.tobytes())
    if xmp:
        data = path.read_bytes() + b"XMP " + struct.pack("<I", len(xmp)) + xmp + b"\0" * (len(xmp) & 1)
        path.write_bytes(data[:4] + struct.pack("<I", len(data) - 8) + data[8:])


def prepare(take: str, start_ms: int, end_ms: int, fade_in_ms: int, fade_out_ms: int) -> tuple[np.ndarray, int]:
    mono, rate = read(SRC / take)
    clip = mono[rate * start_ms // 1000 : rate * end_ms // 1000].copy()
    fade_in = rate * fade_in_ms // 1000
    fade_out = rate * fade_out_ms // 1000
    clip[:fade_in] *= np.linspace(0.0, 1.0, fade_in)
    clip[-fade_out:] *= np.linspace(1.0, 0.0, fade_out)
    clip *= 10 ** (PEAK_DBFS / 20) / np.abs(clip).max()
    return clip, rate


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for sound_id, cut in CUTS.items():
        clip, rate = prepare(*cut)
        write(OUT / f"{sound_id}.wav", clip, rate, chunks(SRC / cut[0]).get(b"XMP "))
        print(f"{sound_id}.wav  {len(clip) / rate * 1000:.0f} ms  from {cut[0]} {cut[1]}-{cut[2]} ms")


if __name__ == "__main__":
    main()
