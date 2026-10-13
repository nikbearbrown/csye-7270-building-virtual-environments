#!/usr/bin/env python3
"""patch_build_prompts.py: inserts one shared section, "HOW TO RUN THIS BUILD", into every laid-out film's BUILD-PROMPT.md.
It makes the build audio-first (Brutalist doctrine: narration is generated and measured first and its durations are the clock for
captures and scenes) and makes a long build resumable from BUILD-LOG.md. Idempotent: a film that already has the section is left alone
unless --force is given, which replaces it.   python3 patch_build_prompts.py [slug ...] [--force]"""
import re
import sys
from pathlib import Path

SERIES = Path(__file__).resolve().parent
sys.path.insert(0, str(SERIES))
import series_config as S  # noqa: E402

MARK = "## HOW TO RUN THIS BUILD"
END = "<!-- /HOW-TO-RUN -->"

BLOCK = """{mark} (read before any phase below; it overrides the phase order where they differ)

**Audio first.** Brutalist is audio-first: the measured narration is the clock for everything else. After the shared pieces exist (Phase 0, if the film needs them built) and **before you record a single capture or write a Manim scene**, voice the film. It is free and quick.

```bash
python3 brutalist.art/runtime/scripts/generate_audio_kokoro.py {film}
```

Then read each beat's measured `actual_duration_s` from `{film}/beat_sheet.json` and use it:

- **Captures:** record each clip at its beat's measured duration. A clip that is a loop (a `TIME`-driven sweep, for example) is recorded for one period and `ShaderLab` loops it. Any scripted change inside a capture (a uniform sweep, a key press, a step) is timed as a fraction of that duration (`--length` and fractional keyframes in the harness, see `COMPONENT-SPECS.md`), so the picture lands on the words.
- **Manim scenes:** size each scene to the measured duration; the midpoint rule applies at the measured midpoint.
- **Voice check now, not at the end:** transcribe with faster-whisper, compare with `narration.py`, and listen for G L S L, G P U, U V, "Godot", "tween", "sine", "fract", "tau", "sawtooth", "instance uniform" and the film's own terms. Do not edit `brutalist.art/runtime/pronunciation/liam.json`; report any mispronunciation to Bear.
- If a measured duration makes one beat longer than 40 seconds, or the film longer than 15 minutes, stop and report. Do not edit the narration to fix it.
- Where a later phase below repeats the voice command, it is already done: skip it unless a line of narration changed (then re-voice only that beat with `--only <BID>`).

**Keep this build resumable.** Write `{film}/BUILD-LOG.md` as you go, and after each phase append a line `PHASE <name> DONE <date>`. If `BUILD-LOG.md` already exists when you start, read it first and resume at the first phase not marked DONE; never redo a finished phase. Log every mistake you made and how you fixed it ("Mistakes worth not repeating").

**Editor frames.** Godot's own editor is recorded by script, never by hand. The driver, its scratch project, the state scripts and the finished frames are in `{series}/editor-capture/` (read its `README.md` first). If this film has editor frames, they are in `{series}/editor-capture/png/1920x1080/<film folder name without the claude-liam-lecture- prefix>/` (the same states at the native 3456x1944 are beside them): copy them into the film's public asset folder under the names its lanes use, and re-record with the driver only if the film's shader or scene changed or a lane needs a state that is not there. Popups and dialogs are recorded only with the editor setting `interface/editor/display/single_window_mode` on (the driver's settings files do that). Label every such clip "scripted editor session". Nobody needs to record a screen by hand.
{end}
"""


def patch(slug, force=False):
    film = S.folder(slug)
    bp = film / "BUILD-PROMPT.md"
    if not bp.exists():
        return f"{slug}: no BUILD-PROMPT.md"
    text = bp.read_text()
    had = MARK in text
    if had and not force:
        return f"{slug}: already patched"
    if had:
        text = re.sub(re.escape(MARK) + r".*?" + re.escape(END) + r"\n?", "", text, flags=re.S)
    block = BLOCK.format(mark=MARK, film=str(film), series=str(SERIES), end=END)
    # insert before the first "## Phase" heading; failing that, before the first heading after "Read first"; failing that, append
    m = re.search(r"^## Phase", text, re.M)
    if not m:
        m = re.search(r"^## (?!Read first)", text, re.M)
        m = m if (m and m.start() > text.find("## Read first")) else None
    if m:
        text = text[: m.start()] + block + "\n" + text[m.start():]
    else:
        text = text.rstrip() + "\n\n" + block
    bp.write_text(text)
    return f"{slug}: patched"


def main():
    force = "--force" in sys.argv
    slugs = [a for a in sys.argv[1:] if not a.startswith("--")] or [s for s, _, _ in S.FILMS]
    for s in slugs:
        print(patch(s, force))


if __name__ == "__main__":
    main()
