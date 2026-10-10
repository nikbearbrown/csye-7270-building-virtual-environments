"""Build the film's figure PNGs from real inputs only.

Every figure is either a crop/arrangement of a native Godot capture, a plot
drawn by FFmpeg from an accepted sound file, or a table whose text is copied
from the submitted docs (TEST-REPORT.md, SOURCES.md, README.md) at f848d84.
Run from the reel folder:  python -I scripts/make_figures.py <toolkit-fonts-dir>
"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

REEL = Path(__file__).resolve().parents[1]
FONTS = Path(sys.argv[1])
FIG = REEL / "figures"
CAP = REEL / "capture"
PAGE, INK, SOFT, SPARK, LINE = "#FFFDF8", "#3D3929", "#73705F", "#D97757", "#CFC6B5"
GOOD, BAD, PART = "#3E6B48", "#A44A32", "#8A6A1F"


def font(name, size):
    hits = sorted(FONTS.rglob(name))
    return ImageFont.truetype(str(hits[0]), size)


SERIF = lambda s: font("EBGaramond-Regular.ttf", s)
SANS = lambda s: font("Lato-Regular.ttf", s)
SANSB = lambda s: font("Lato-Bold.ttf", s)
MONO = lambda s: font("PTMono-Regular.ttf", s)


def label(draw, xy, text, f, fill=INK, anchor="la"):
    draw.text(xy, text, font=f, fill=fill, anchor=anchor)


def stairs_compare():
    """Normal render vs --debug-collisions render, same orthographic film camera."""
    W, H = 3400, 1060
    out = Image.new("RGB", (W, H), PAGE)
    d = ImageDraw.Draw(out)
    # crop the same region from both takes: steps + landing, floor line
    box = (0, 160, 3840, 2160 - 0)
    for i, (name, cap) in enumerate((("stairs_side", "Normal render"),
                                     ("stairs_side_collision", "--debug-collisions (orange = collision shapes)"))):
        im = Image.open(CAP / f"{name}.png").convert("RGB").crop(box)
        tw = (W - 60) // 2
        th = int(im.height * tw / im.width)
        im = im.resize((tw, th), Image.LANCZOS)
        x = 20 + i * (tw + 20)
        out.paste(im, (x, 110))
        label(d, (x, 30), cap, SANSB(54))
        label(d, (x, 110 + th + 18), f"capture/{name}.png · native 3840×2160 · film camera added by capture script",
              SANS(34), SOFT)
    return out


def power_on_audio():
    """Waveform + spectrogram of design/sfx_sound/sfx_power_on.flac (FFmpeg plots)."""
    W, H = 2400, 1000
    out = Image.new("RGB", (W, H), PAGE)
    d = ImageDraw.Draw(out)
    wave = Image.open(FIG / "power_on_wave.png").convert("RGBA")
    bg = Image.new("RGBA", wave.size, PAGE)
    bg.alpha_composite(wave)
    out.paste(bg.convert("RGB").resize((2400, 380)), (0, 70))
    label(d, (10, 8), "Waveform · sfx_power_on.flac (ComfyUI output 00042, unedited) · 0 to 2.41 s · amplitude shown on a square-root scale", SANSB(44))
    spec = Image.open(FIG / "power_on_spec.png").convert("RGB")
    spec = spec.resize((2400, H - 520), Image.LANCZOS)  # whole plot, squeezed vertically
    label(d, (10, 470), "Spectrogram (FFmpeg showspectrumpic, 0–8 kHz)", SANSB(40))
    out.paste(spec, (0, 520))
    return out


def sequence():
    """The listening segment: three accepted files, unaltered, separated by silence."""
    W, H = 3400, 1280
    out = Image.new("RGB", (W, H), PAGE)
    d = ImageDraw.Draw(out)
    total = 9.744308
    wave = Image.open(FIG / "sequence_wave.png").convert("RGBA")
    bg = Image.new("RGBA", wave.size, PAGE)
    bg.alpha_composite(wave)
    x0, ww, y0, wh = 60, W - 120, 260, 700
    out.paste(bg.convert("RGB").resize((ww, wh)), (x0, y0))
    segs = [(0.8, 2.414875, "1  Power on", "sfx_power_on.flac · 00042"),
            (4.214875, 2.414875, "2  Power off", "sfx_power_off.flac · 00044"),
            (7.62975, 1.114558, "3  Button press", "sfx_botton_press.flac · 00070")]
    for start, dur, name, src in segs:
        a = x0 + int(ww * start / total)
        b = x0 + int(ww * (start + dur) / total)
        d.rectangle((a, y0 - 20, b, y0 + wh + 20), outline=SPARK, width=6)
        label(d, (a + 12, 60), name, SANSB(64))
        label(d, (a + 12, 150), src, SANS(40), SOFT)
    for t in range(0, 10):
        x = x0 + int(ww * t / total)
        d.line((x, y0 + wh + 30, x, y0 + wh + 50), fill=SOFT, width=4)
        label(d, (x, y0 + wh + 60), f"{t} s", SANS(36), SOFT, "ma")
    label(d, (x0, H - 110), "Generated sound files played back to back at their original level; no processing. "
          "Not in the Godot project, not triggered by any game event.", SANS(42), INK)
    return out


def table(title, rows, widths, foot, foot2=""):
    W, H = 3400, 1500
    out = Image.new("RGB", (W, H), PAGE)
    d = ImageDraw.Draw(out)
    label(d, (40, 20), title, SANSB(64))
    y = 120
    rh = (H - 120 - (190 if foot2 else 110)) // len(rows)
    for r, row in enumerate(rows):
        x = 40
        if r == 0:
            d.rectangle((30, y, W - 30, y + rh - 8), fill="#EFE9DD")
        for c, cell in enumerate(row):
            fill = INK
            if isinstance(cell, tuple):
                cell, fill = cell
            f = SANSB(56) if r == 0 else SANS(56)
            label(d, (x + 12, y + rh // 2 - 4), cell, f, fill, "lm")
            x += widths[c]
        d.line((30, y + rh - 4, W - 30, y + rh - 4), fill=LINE, width=3)
        y += rh
    if foot2:
        label(d, (40, H - 160), foot2, SANSB(48), INK)
    label(d, (40, H - 80), foot, SANS(44), SOFT)
    return out


def status_table():
    rows = [["Assignment requirement", "Status at f848d84", "Evidence"],
            ["Concept, storyboard (10 panels), character sheet", ("Written and committed", GOOD), "the three design docs"],
            ["10 pose images, silhouette test, collision overlay", ("Not made", BAD), "CHARACTER-SHEET status lines"],
            ["Character in two states in the running slice", ("Not built: no character", BAD), "TEST-REPORT, README"],
            ["Four sound events firing in real play", ("3 sounds accepted, none wired", PART), "SOURCES rows · design/sfx_sound/"],
            ["Seamless music loop", ("Not generated", BAD), "TEST-REPORT"],
            ["Mute that keeps the slice readable", ("No controls at all", BAD), "README: Controls"],
            ["Runs from a fresh copy + one automated check", ("Done (greybox scene)", GOOD), "TEST-REPORT automated check 1"]]
    return table("What this build can and cannot show", rows, [1430, 880, 1050],
                 "Statuses copied from TEST-REPORT.md and README.md (drafts, not yet committed).")


def models_table():
    rows = [["Model / tool", "Who made it", "What it produced", "Outcome"],
            ["ChatGPT image generation", "OpenAI", "Turnaround, 9 extra views, 4 tablet refs", ("Accepted as refs", GOOD)],
            ["ChatGPT image generation", "OpenAI", "Character drafts CHAR-REF-01, -03, -04", ("Rejected", BAD)],
            ["ChenkinNoob-XL V0.5 (local ComfyUI)", "ChenkinNoob / ChenkinLab", "Early character drafts", ("All rejected", BAD)],
            ["Stable Audio 3 Small SFX (local ComfyUI)", "Stability AI (UK)", "161 terminal sound outputs", ("3 accepted", GOOD)],
            ["Claude Code · Claude Opus 5.5", "Anthropic", "base.tscn greybox, test_chair.glb", ("Greybox / test", PART)],
            ["Kokoro-82M · am_onyx (local)", "hexgrad (open weights)", "This film's narration (Liam)", ("Film only", SOFT)]]
    return table("Which model produced which asset", rows, [1150, 700, 1080, 450],
                 "From SOURCES.md at f848d84. Kokoro row = this film's narration, not a game asset.",
                 "Assignment text: Claude's code-drawn art does not satisfy the generative-model requirement. "
                 "Professor (to the designer): basic-shape 3D builds count.")


def test_log():
    """Real command output recorded while making this film (evidence/*.log)."""
    W, H = 3400, 1380
    out = Image.new("RGB", (W, H), "#202531")
    d = ImageDraw.Draw(out)
    ev = REEL / "evidence"
    lines = ["$ godot --headless --path <fresh copy of f848d84>/godot --import      -> exit 0",
             "$ godot --headless --path <fresh copy>/godot --quit-after 120 res://base.tscn  -> exit 0"]
    run = (ev / "fresh-run-120.log").read_text(encoding="utf-8").strip().splitlines()
    lines += ["  " + l for l in run]
    lines += ["  matches for error|warning|failed in that log: 0", "",
              "$ godot --headless --path <capture copy>/godot --script res://ramp_check.gd   -> exit 0"]
    lines += ["  " + l for l in (ev / "ramp-check.log").read_text(encoding="utf-8").strip().splitlines()]
    y = 40
    for l in lines:
        col = "#8BC7F3" if l.startswith("$") else "#EDF1F7"
        label(d, (40, y), l, MONO(52), col)
        y += 88
    return out


if __name__ == "__main__":
    for name, fn in (("stairs_compare", stairs_compare), ("power_on_audio", power_on_audio),
                     ("sequence", sequence), ("status_table", status_table),
                     ("models_table", models_table), ("test_log", test_log)):
        fn().save(FIG / f"{name}.png", optimize=True)
        print("wrote figures/%s.png" % name)
