#!/usr/bin/env python3
"""make_claude_code_prompts.py: writes CLAUDE-CODE-PROMPTS.md, one ready-to-paste Claude Code prompt per laid-out film, in
series_config.FILMS order (the recommended build order), using the exact template in books/CLAUDE.md ("Two-stage builds").
Run after the films are laid out:  python3 make_claude_code_prompts.py"""
import sys
from pathlib import Path

SERIES = Path(__file__).resolve().parent
sys.path.insert(0, str(SERIES))
import series_config as S  # noqa: E402

TEMPLATE = ("You are running from books/. Read {path}/BUILD-PROMPT.md completely and follow it exactly. "
            "Use ./brutalist.art/art for every step: generate the audio, check the stills, run the review cut and the final master at 4K, "
            "and run every gate to PASS. Do not change the narration, the scene design or the beat sheet; if a gate fails, fix the smallest "
            "unit and re-run only that, and log it in BUILD-LOG.md. Do not publish or stage anything. Report the master's absolute path, "
            "runtime, and any gate that did not pass.")


def main():
    out = ["# Claude Code prompts: build the Godot shader films\n",
           "**What this is.** One ready-to-paste prompt per film, in the order I recommend building them (the order of the list below). Each points a medium-effort Claude Code session, launched from `/Users/bear/Documents/CoWork/bear-textbooks/books`, at that film's `BUILD-PROMPT.md`.",
           "**Why.** Your two-stage rule: a higher-effort session lays the film out; a medium-effort Claude Code session builds it. The layouts are finished and checked; these start the builds.",
           "**Found.** Build **Godot Shaders** first. Its build also creates the three shared pieces every other film reuses (the `ShaderLab` Remotion component, the Manim helper kit `shader_kit.py` and the capture harness). Each build is audio-first (the film is voiced before anything is recorded) and resumable (it keeps `BUILD-LOG.md` and marks each phase DONE), so if a session ends early, paste the same prompt again. Nothing is published or staged by any of them. Nobody needs to record a screen by hand: the editor frames are recorded by script.\n",
           "Switch the session to medium effort, launch it from `books/`, paste one prompt, and let it run.\n"]
    group = None
    for slug, title, grp in S.FILMS:
        folder = S.folder(slug)
        if grp != group:
            group = grp
            out.append(f"# {grp}\n")
        if not (folder / "BUILD-PROMPT.md").exists():
            out.append(f"## {title}\n\nNot laid out yet.\n")
            continue
        out.append(f"## {title}\n")
        out.append("```")
        out.append(TEMPLATE.format(path=str(folder)))
        out.append("```\n")
    (SERIES / "CLAUDE-CODE-PROMPTS.md").write_text("\n".join(out) + "\n")
    print("wrote CLAUDE-CODE-PROMPTS.md")


if __name__ == "__main__":
    main()
