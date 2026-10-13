"""series_config.py — constants shared by every film in the Godot shader lecture series.

One place to change the playlist name, the channel, the handle and the pace constants. Every film's make_sheet.py reads this
(through make_sheet_shared.py), so a change here plus a re-run of each make_sheet.py updates the whole series.

NOTHING VIEWER-FACING IS EVER NUMBERED (Bear, 2026-10-11): the order in FILMS below is for planning and tooling only.
"""
from pathlib import Path

SERIES_DIR = Path(__file__).resolve().parent
YOUTUBE_DIR = SERIES_DIR.parent
BOOKS_DIR = SERIES_DIR.parents[2]
TK = BOOKS_DIR / "brutalist.art"

CHANNEL = "claude-liam"
HANDLE = "@NikBearBrown"
PERSONA = "Liam (in for Bear)"
VOICE = "am_onyx"

# Bear has not named a playlist yet. While this is empty, BOPEN says "<title>. <summary>" and no series field is printed.
# When he names it: set it here, re-run every film's make_sheet.py, regenerate BOPEN audio and the title cards.
PLAYLIST = ""

GODOT = "4.7.2"          # installed engine used for every capture and check
GODOT_DOCS = "4.7"       # documentation version fact-checked against

# Pace, measured on 57 shipped lecture films (median): Liam speaks about 0.34 s per word; the six fixed bookend beats
# (opening card, writer, terms, recap, your turn, outro) take about 78 s together.
# lint_series.py estimates minutes as (ALL spoken words x SEC_PER_WORD + 4 s) / 60, bookend words included, so the
# estimate errs long. SPINE_SECONDS is informational only (the measured bookend time); nothing computes with it.
SEC_PER_WORD = 0.34
SPINE_SECONDS = 78
TARGET_MIN, TARGET_MAX, HARD_MAX = 9.0, 11.5, 15.0      # minutes: preferred band, soft ceiling, hard ceiling (Bear, 2026-10-13)

# (slug, working title, group). Order is the recommended watching/building order inside a group.
FILMS = [
    ("godot-shaders", "Godot Shaders", "Foundations"),
    ("godot-shader-language", "Godot Shader Language", "Foundations"),
    ("shader-math-toolkit", "The Shader Math Toolkit", "Foundations"),
    ("textures-and-color", "Textures and Color", "Foundations"),
    ("shaders-in-3d", "Shaders in 3D", "Foundations"),
    ("uv-space", "UV Space", "Fragment techniques"),
    ("patterns-and-pixelation", "Patterns and Pixelation", "Fragment techniques"),
    ("drawing-shapes-with-math", "Drawing Shapes with Math", "Fragment techniques"),
    ("soft-edges-glow-and-noise", "Soft Edges, Glow and Noise", "Fragment techniques"),
    ("time-and-waves", "Time and Waves", "Fragment techniques"),
    ("trigonometry-for-shaders", "Trigonometry for Shaders", "Fragment techniques"),
    ("lines-and-shine", "Lines and Shine", "Fragment techniques"),
    ("outlines", "Outlines", "Fragment techniques"),
    ("vertex-shaders", "Vertex Shaders", "Vertex and space"),
    ("matrices-and-fake-3d", "Matrices and Fake 3D", "Vertex and space"),
    ("local-world-and-screen-space", "Local, World and Screen Space", "Vertex and space"),
    ("reading-the-screen", "Reading the Screen", "Screen, textures and light"),
    ("reflections", "Reflections", "Screen, textures and light"),
    ("subviewports", "SubViewports", "Screen, textures and light"),
    ("light-shaders", "Light Shaders", "Screen, textures and light"),
]


def folder(slug):
    return YOUTUBE_DIR / f"claude-liam-lecture-{slug}"


def full_slug(slug):
    return f"claude-liam-lecture-{slug}"


def est_seconds(text):
    """Estimated spoken seconds for a narration string (calibrated on shipped films)."""
    return round(len(text.split()) * SEC_PER_WORD, 1)


def bopen(title, summary):
    """The narrated first beat: playlist (if any), exact film title, a very short summary (lecture skill)."""
    head = f"{PLAYLIST}. {title}." if PLAYLIST else f"{title}."
    return f"{head} {summary}"
