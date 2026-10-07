"""Measure and draw the step 3 evidence from Godot's movie-maker recording.

Input: the AVI that capture step 3 wrote with --write-movie (its audio track is
the game's own mix, 48 kHz), and evidence/3/3-mix-events.json, which the same
run logged frame by frame (tests/capture.gd).

Output, in evidence/3/:
- 3-mix.ogg: the mix, mono (every sound in the game is mono, so the two
  channels are the same; the script checks that);
- 3-mix.png: the mix's level over the run with each sound effect and each
  state marked, and the music's gain as the game asked for it and as measured
  in the mix.
It also prints the measurements.

The music: it is the only thing playing on the title, so cross-correlating
the mix with the start of MUS-LOOP.ogg finds the sample where the loop starts.
The loop from there, at the Music bus's level, is what the mix would hold at
full level; in each 50 ms window with no sound effect, the music's measured
gain is the mix's level against that reference's.

The sound effects: each frame's log gives the music's playback position, so
the frame on which the game played a sound maps to a sample of the mix. The
position moves on in the mixer's blocks of 512 samples (10.7 ms), so that
sample is known to within a block. The mix less the music is cross-correlated
with the sound's file around there, which gives where the sound starts, from
its event's frame, and the gain it plays at.

Needs ffmpeg (decoding), oggenc (vorbis-tools), numpy, scipy and matplotlib.

Usage: python3 design/tools/plot_mix.py <recording>.avi
"""

import json
import subprocess
import sys
import tempfile
import wave
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import correlate

ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / "evidence" / "3"
AUDIO = ROOT / "game" / "systems" / "audio"
RATE = 48000
MUSIC_BUS_DB = -6.0  # game/default_bus_layout.tres
SFX_BUS_DB = 0.0
WINDOW = 2400  # 50 ms
QUIET_DB = -45.0  # windows where the reference is quieter than this are not measured
SFX_GUARD = 0.03  # s kept clear after a sound effect ends

# Light-mode roles (the dataviz reference palette).
SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK_2 = "#52514e"
GRID = "#e6e5e0"
BAND = "#efeee9"
SERIES_1 = "#2a78d6"  # blue: what was measured in the mix
SERIES_2 = "#eb6834"  # orange: what the game asked for


def decode(path: Path, channels: int) -> np.ndarray:
    raw = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", str(path), "-vn", "-f", "f32le", "-ac", str(channels), "-ar", str(RATE), "-"],
        capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, channels)


def db(power: np.ndarray) -> np.ndarray:
    return 10.0 * np.log10(np.maximum(power, 1e-12))


def peak_db(samples: np.ndarray) -> float:
    """The peak in dBFS; -inf for digital silence."""
    peak = float(np.max(np.abs(samples))) if len(samples) else 0.0
    return 20.0 * np.log10(peak) if peak > 0.0 else float("-inf")


def main(avi: Path) -> None:
    log = json.loads((EVIDENCE / "3-mix-events.json").read_text())
    fps = log["fps"]
    stereo = decode(avi, 2)
    channel_gap = float(np.max(np.abs(stereo[:, 0] - stereo[:, 1])))
    mix = stereo.mean(axis=1)
    loop = decode(AUDIO / "music" / "MUS-LOOP.ogg", 1)[:, 0]

    # Where the loop starts in the mix: on the title only the music plays.
    head = loop[: RATE // 2]
    corr = correlate(mix[: 3 * RATE], head, mode="valid", method="fft")
    start = int(np.argmax(corr))

    # Each logged frame's sample in the mix, from the music's position then.
    pos = np.array(log["music_pos"])
    playing = np.array(log["music_playing"])
    stop_at = int(np.argmax(~playing)) if not playing.all() else len(playing)
    frame_sample = np.full(len(pos), np.nan)
    frame_sample[:stop_at] = start + pos[:stop_at] * RATE
    # After the music stops, the frames go on at fps.
    frame_sample[stop_at:] = frame_sample[stop_at - 1] + (np.arange(stop_at, len(pos)) - stop_at + 1) * RATE / fps

    # The music as the mix would hold it at full level, until it stops.
    stop_sample = int(frame_sample[stop_at - 1] + RATE / fps) if stop_at < len(pos) else len(mix)
    ref = np.zeros_like(mix)
    n = np.arange(start, min(stop_sample, len(mix)))
    ref[n] = loop[(n - start) % len(loop)] * 10 ** (MUSIC_BUS_DB / 20)

    # The game's asked-for gain at every sample, and the states, by frame.
    asked_db = np.array(log["music_db"], dtype=float)
    gain_at = np.interp(np.arange(len(mix)), frame_sample, asked_db)
    muted_at = np.interp(np.arange(len(mix)), frame_sample, np.array(log["music_muted"], dtype=float)) > 0.5

    # The sound effects: where each starts in the mix, and at what gain.
    residual = mix - ref * 10 ** (gain_at / 20) * ~muted_at
    sounds = []
    for i, started in enumerate(log["sounds"]):
        for sound_id in started:
            clip = decode(AUDIO / "sfx" / f"SFX-{sound_id.upper()}.wav", 1)[:, 0] * 10 ** (SFX_BUS_DB / 20)
            expected = int(round(frame_sample[i]))
            lo, hi = expected - RATE // 20, expected + RATE // 10
            segment = residual[lo: hi + len(clip)]
            c = correlate(segment, clip, mode="valid", method="fft")
            at = lo + int(np.argmax(c))
            found = residual[at: at + len(clip)]
            gain = float(np.dot(found, clip) / np.dot(clip, clip))
            sounds.append({"id": sound_id, "frame": log["frames"][i], "expected": expected, "at": at,
                           "delay_ms": (at - expected) / RATE * 1000, "gain_db": 20 * np.log10(gain),
                           "end": at + len(clip)})

    # The music's measured gain in each window clear of sound effects and of the mute.
    starts = np.arange(start, min(stop_sample, len(mix)) - WINDOW, WINDOW)
    busy = np.zeros(len(mix), bool)
    for s in sounds:
        busy[s["at"]: s["end"] + int(SFX_GUARD * RATE)] = True
    measured = []
    for w in starts:
        sl = slice(w, w + WINDOW)
        ref_power = np.mean(ref[sl] ** 2)
        if busy[sl].any() or muted_at[sl].any() or db(ref_power) < QUIET_DB:
            continue
        measured.append((w + WINDOW / 2, db(np.mean(mix[sl] ** 2)) - db(ref_power), np.mean(gain_at[sl])))
    measured = np.array(measured)

    # Steady stretches: windows where the asked-for gain held one value.
    print(f"loop starts at sample {start} ({start / RATE * 1000:.1f} ms); channels differ by at most {channel_gap:.2e}")
    for level in (0.0, -6.0, -12.0, -9.0):
        held = measured[np.abs(measured[:, 2] - level) < 0.01]
        print(f"asked {level:+.0f} dB: {len(held)} windows, measured {np.median(held[:, 1]):+.2f} dB "
              f"(from {held[:, 1].min():+.2f} to {held[:, 1].max():+.2f})")
    for s in sounds:
        print(f"{s['id']:7s} frame {s['frame']:5d}: starts {s['delay_ms']:+.1f} ms from its frame's sample, at {s['gain_db']:+.2f} dB")
    # Silence: inside the mute (a frame clear of each edge), and once the music
    # has stopped and the last sound has ended.
    edge = RATE // fps
    muted = np.flatnonzero(muted_at)
    inside = mix[muted[0] + edge: muted[-1] - edge]
    tail = mix[max(stop_sample, max(s["end"] for s in sounds)):]
    print(f"inside the mute: {len(inside) / RATE:.2f} s, peak {peak_db(inside):.1f} dBFS")
    print(f"after the music stopped and the portal sound ended: {len(tail) / RATE:.2f} s, peak {peak_db(tail):.1f} dBFS")

    medians = [round(float(np.median(measured[np.abs(measured[:, 2] - level) < 0.01, 1])), 2) + 0.0
               for level in (0.0, -6.0, -12.0, -9.0)]
    worst = max(abs(s["gain_db"]) for s in sounds)
    summary = ("Music measured at {:.2f} / {:.2f} / {:.2f} / {:.2f} dB where the game asked for 0 / -6 (hit) / -12 (pause) / "
               "-9 (fall).\nEvery sound effect plays within {:.2f} dB of its file; digital silence inside the mute and on "
               "the end card.").format(*medians, worst)
    save_ogg(mix)
    draw(log, mix, frame_sample, measured, sounds, summary)


def save_ogg(mix: np.ndarray) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        wav = Path(tmp) / "mix.wav"
        with wave.open(str(wav), "wb") as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(RATE)
            w.writeframes((np.clip(mix, -1, 1) * 32767).astype("<i2").tobytes())
        subprocess.run(["oggenc", "-Q", "-q", "5", "-o", str(EVIDENCE / "3-mix.ogg"), str(wav)], check=True)


def spans(flags: list, frame_sample: np.ndarray) -> list:
    """(first sample, last sample) of each run of frames where flags is true."""
    out, begin = [], None
    for i, flag in enumerate(list(flags) + [False]):
        if flag and begin is None:
            begin = i
        elif not flag and begin is not None:
            out.append((frame_sample[begin], frame_sample[min(i, len(frame_sample) - 1)]))
            begin = None
    return out


def draw(log: dict, mix: np.ndarray, frame_sample: np.ndarray, measured: np.ndarray, sounds: list,
         summary: str) -> None:
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "text.color": INK,
                         "axes.labelcolor": INK_2, "xtick.color": INK_2, "ytick.color": INK_2})
    fig, (top, bottom) = plt.subplots(2, 1, figsize=(13, 7.2), dpi=150, sharex=True,
                                      gridspec_kw={"height_ratios": [3, 2], "hspace": 0.12})
    fig.patch.set_facecolor(SURFACE)
    seconds = lambda samples: np.asarray(samples) / RATE

    # The states, as bands under both panels.
    state = log["state"]
    bands = [
        ("title", [s == "TITLE" for s in state]),
        ("paused (Esc)", log["paused"]),
        ("music muted (M)", log["music_muted"]),
        ("fall: fade and respawn", [s == "DYING" for s in state]),
        ("end card", [s == "COMPLETE" for s in state]),
    ]
    for ax in (top, bottom):
        ax.set_facecolor(SURFACE)
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)
        for side in ("left", "bottom"):
            ax.spines[side].set_color(GRID)
        ax.grid(axis="y", color=GRID, linewidth=0.8)
        ax.set_axisbelow(True)
        for label, flags in bands:
            for a, b in spans(flags, frame_sample):
                a = 0 if label == "title" else a  # the log starts 0.5 s in; the title shows from the first frame
                ax.axvspan(seconds(a), seconds(b), color=BAND, linewidth=0, zorder=0)
    for label, flags in bands:
        for a, b in spans(flags, frame_sample):
            top.text(seconds((a + b) / 2), -2, label, ha="center", va="top", fontsize=8.5, color=INK_2)

    # Top: the mix's level, 50 ms RMS.
    hop = WINDOW
    frames = np.arange(0, len(mix) - hop, hop)
    level = db(np.array([np.mean(mix[f: f + hop] ** 2) for f in frames]))
    top.plot(seconds(frames + hop / 2), level, color=SERIES_1, linewidth=1.6)
    top.set_ylim(-60, 0)
    top.set_ylabel("mix level, dBFS (50 ms RMS)")
    fig.subplots_adjust(top=0.85)
    left = top.get_position().x0
    fig.text(left, 0.975, "The game's own mix, recorded by Godot's movie maker: each sound effect on its event",
             fontsize=11.5, color=INK, va="top")
    fig.text(left, 0.945, summary, fontsize=9, color=INK_2, va="top", linespacing=1.5)
    last_x = -10.0
    for s in sounds:
        x = seconds(s["at"])
        top.axvline(x, color=INK_2, linewidth=0.8, linestyle=(0, (2, 2)), zorder=1)
        crowded = x - last_x < 1.0
        top.text(x, 1.5, s["id"], ha="left" if crowded else "center", va="bottom", fontsize=8.5, color=INK)
        last_x = x

    # Bottom: the music's gain, asked for and measured.
    sample_of_frame = seconds(frame_sample)
    asked = np.array(log["music_db"], dtype=float)
    bottom.plot(sample_of_frame, asked, color=SERIES_2, linewidth=2, drawstyle="steps-post",
                label="asked for (Music.volume_db, per frame)")
    bottom.plot(seconds(measured[:, 0]), measured[:, 1], linestyle="none", marker="o", markersize=3.2,
                color=SERIES_1, label="measured in the mix (50 ms windows clear of sound effects)")
    bottom.set_ylim(-26, 3)
    bottom.set_yticks([0, -6, -9, -12, -24])
    bottom.set_ylabel("music gain, dB")
    bottom.set_xlabel("seconds into the recording")
    bottom.legend(loc="lower left", frameon=False, fontsize=8.5)
    fade = [i for i, s in enumerate(log["state"]) if s == "COMPLETE"]
    if fade:
        x = sample_of_frame[fade[0]]
        bottom.annotate("fades to -60 dB over 1.5 s, then stops", xy=(x + 0.9, -24), xytext=(x - 4.2, -19),
                        fontsize=8.5, color=INK_2, arrowprops={"arrowstyle": "-", "color": INK_2, "linewidth": 0.8})
    top.set_xlim(0, seconds(len(mix)))
    fig.savefig(EVIDENCE / "3-mix.png", facecolor=SURFACE, bbox_inches="tight")
    print(f"saved {EVIDENCE / '3-mix.png'}")


if __name__ == "__main__":
    main(Path(sys.argv[1]))
