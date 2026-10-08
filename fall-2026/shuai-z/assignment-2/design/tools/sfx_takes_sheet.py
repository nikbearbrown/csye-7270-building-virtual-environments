"""Draw every sound-effect take, kept and not chosen, as one contact sheet.

The not-chosen takes are full-size WAVs in _raw/, which is not in git. This
sheet is their small committed record, like the image thumbnails in
generated/rejected/: one row per sound, four takes per row, each take as its
waveform over its spectrogram, with its length, peak and the first 12 hex
digits of its SHA-256, so a take found later can be matched to its tile.

Run from the project root, giving the folder that holds the takes:
python3 design/tools/sfx_takes_sheet.py path/to/_raw
"""

import hashlib
import sys
import wave
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "generated/rejected/SFX-takes-sheet.png"

# The take kept for each sound (ASSET-LOG.md).
KEPT = {"SFX-JUMP": 4, "SFX-STOMP": 2, "SFX-HURT": 1, "SFX-PORTAL": 2, "SFX-SLASH": 3, "SFX-PICKUP": 2}
MODEL = {"SFX-JUMP": "Adobe Firefly"}


def read_mono(path):
    with wave.open(str(path)) as w:
        rate, ch, width = w.getframerate(), w.getnchannels(), w.getsampwidth()
        data = np.frombuffer(w.readframes(w.getnframes()), dtype={2: np.int16, 4: np.int32}[width])
    full = float(np.iinfo(data.dtype).max)
    return rate, data.reshape(-1, ch).astype(np.float64).mean(axis=1) / full


def main():
    raw = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "_raw"
    fig, axes = plt.subplots(len(KEPT) * 2, 4, figsize=(16, 2.1 * len(KEPT) * 2),
                             gridspec_kw={"height_ratios": [1, 1.3] * len(KEPT)})
    fig.suptitle("Sound-effect takes: the kept take (green) and the takes not chosen (grey). "
                 "Waveform over spectrogram, full take, before any edit.", fontsize=13)
    for row, (sound, kept) in enumerate(KEPT.items()):
        for take in range(1, 5):
            path = raw / f"{sound}-{take:02d}.wav"
            rate, x = read_mono(path)
            sha = hashlib.sha256(path.read_bytes()).hexdigest()[:12]
            t = np.arange(len(x)) / rate
            colour = "#2e8b3a" if take == kept else "#777777"
            ax_w, ax_s = axes[row * 2, take - 1], axes[row * 2 + 1, take - 1]
            ax_w.plot(t, x, color=colour, linewidth=0.5)
            ax_w.set_xlim(0, t[-1])
            ax_w.set_ylim(-1, 1)
            ax_w.set_xticks([])
            ax_w.set_yticks([])
            status = "KEPT" if take == kept else "not chosen"
            peak_db = 20 * np.log10(max(np.abs(x).max(), 1e-9))
            ax_w.set_title(f"{sound}-{take:02d} · {status} · {len(x) / rate:.2f} s · peak {peak_db:.1f} dBFS\n"
                           f"{MODEL.get(sound, 'ElevenLabs')} · sha256 {sha}", fontsize=8, color=colour)
            ax_s.specgram(x, NFFT=512, Fs=rate, noverlap=384, cmap="magma", vmin=-120)
            ax_s.set_ylim(0, 16000)
            ax_s.tick_params(labelsize=6)
            if take == 1:
                ax_s.set_ylabel("Hz", fontsize=7)
    fig.tight_layout(rect=(0, 0, 1, 0.98))
    fig.savefig(OUT, dpi=72)
    Image.open(OUT).convert("RGB").quantize(colors=128).save(OUT, optimize=True)
    print(f"wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
