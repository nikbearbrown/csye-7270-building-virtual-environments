# Writes the three probe inputs: a 16x16 half-transparent PNG, a 0.1 s 440 Hz WAV, and an Ogg made from it.
import math, struct, subprocess, wave
from PIL import Image
Image.new("RGBA", (16, 16), (255, 0, 0, 128)).save("t.png")
w = wave.open("s.wav", "wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(44100)
w.writeframes(b"".join(struct.pack("<h", int(8000 * math.sin(2 * math.pi * 440 * i / 44100))) for i in range(4410))); w.close()
# ffmpeg's built-in (experimental) Vorbis encoder; any Ogg Vorbis file works
subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", "s.wav", "-c:a", "vorbis", "-strict", "-2", "-ac", "2", "m.ogg"], check=True)
