# Review me: the Godot shader films

**What this is.** Your starting page for the shader series: twenty standalone lecture films (Liam, about ten minutes each), every one laid out in full but none voiced, recorded, rendered or published. Godot Shaders and Godot Shader Language are your two titles; the other eighteen come from the seven-hour course, regrouped by idea.
**Why.** You asked for the plan and every beat sheet first, at high effort, and then a medium-effort Claude Code build. This is the plan for you to read and say yes, no or change.
**Found.** About 930 beats and 35,000 words, about 3.4 hours of film at the lint's ceiling estimate (the real total is shorter). Every Godot claim was run in Godot 4.7.2; 64 of them turned out wrong or loose in the sources, the docs or my own briefs and are corrected. The real Godot editor can be recorded by script, so you record nothing by hand. Eight decisions are yours (below).

## Read in this order

1. **One page for the whole series:** `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_godot-shaders-series/FILM-CARDS.md` (each film: the idea, the wrong assumption it opens on, length, what running Godot corrected).
2. **The pilot, first and fully:** `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-godot-shaders/SCRIPT.md`. Tone, depth and length changes there carry to the other nineteen, so settle them before reading further.
3. **The plan and your decisions:** `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_godot-shaders-series/SERIES-PLAN.md` (chapter map, what the layouts found, the Signal Garden test, the decisions).
4. **Any other film's script:** `.../youtube/claude-liam-lecture-<slug>/SCRIPT.md` (the slugs are in `FILM-CARDS.md`). Blockquotes are exactly what Liam will say; "Picture" is what is on screen.

## Your decisions (full wording in SERIES-PLAN.md, "Decisions for Bear")

1. Pilot tone and length: read it first.
2. Playlist name and titles (none is named; every film is regenerated from one setting when you name it).
3. Editor captures: settled, no recording by you (optional: a visible cursor).
4. Credit for the two third-party sources (names and addresses, if you want them credited).
5. Scope: twenty is the full regroup; candidates to drop or merge are Lines and Shine and the three advanced screen films.
6. Build order, and whether the Signal Garden redo waits for four films or all twenty.
7. A parallel film on the same subject exists: `claude-liam-lecture-godot-shading-language/`, built today by another session (58 beats, names the course, a slate cut already rendered). It overlaps my standalone Godot Shader Language. Pick one, or keep both with different jobs. I did not touch it.
8. Course credit: these films name no course. If you want them credited to the course, it is one setting and a regenerate.

## How to build (when you say go)

Switch Claude Code to medium effort and launch it from `books/`. Build **Godot Shaders first**: its build also creates the three shared pieces every other film reuses. Paste this:

```
You are running from books/. Read /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-godot-shaders/BUILD-PROMPT.md completely and follow it exactly. Use ./brutalist.art/art for every step: generate the audio, check the stills, run the review cut and the final master at 4K, and run every gate to PASS. Do not change the narration, the scene design or the beat sheet; if a gate fails, fix the smallest unit and re-run only that, and log it in BUILD-LOG.md. Do not publish or stage anything. Report the master's absolute path, runtime, and any gate that did not pass.
```

The other nineteen prompts, in the recommended order, are in `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_godot-shaders-series/CLAUDE-CODE-PROMPTS.md`. Each build voices the film first (audio-first), keeps `BUILD-LOG.md`, and marks each phase DONE, so if a session ends early, paste the same prompt again and it resumes. Run one build at a time: they share one Mac, one Lab lock and the 4K renders. Nothing is published or staged by any of them.

## What is verified, and what is not

- **Verified:** every Godot behaviour and number in the scripts, in Godot 4.7.2 on one Apple M4 Pro (mostly Forward+; where a pixel depends on the renderer the film says which). The editor labels are from real recorded editor frames.
- **Not verified yet:** how the voice says "U V", "fract", "tau", "sawtooth" and similar (checked at the voice stage, never by editing the pronunciation dictionary); GATE T on real captures (checked in the build); nothing about real-time frame rate or other GPUs.
- **Estimated, not measured:** minutes (word count at Liam's measured pace).

## Known overlaps (each film is standalone, so each re-teaches what it needs; tell me if you would rather trim)

The Math Toolkit's floor/fract/mod act overlaps the Patterns film's first act; its disc-and-ring act overlaps Drawing Shapes. The oval-circle trap appears in UV Space (the full explanation), the Toolkit, Drawing Shapes and Reading the Screen. Time and Waves and Trigonometry both define sine, in the same wording as the glossary. Every terms card re-defines shader, pixel and UV in the glossary's one wording.

## Where everything is

All under `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/`:

- `_godot-shaders-series/`: `SERIES-PLAN.md`, `FILM-CARDS.md`, `SERIES-TABLE.md`, `FINDINGS-COLLECTED.md`, `LINT-REPORT.md`, `GLOSSARY.md`, `COMPONENT-SPECS.md`, `BUILDER-BRIEF-COMMON.md`, `CLAUDE-CODE-PROMPTS.md`, `RECORDING-SESSION.md` (says nothing to record), `editor-capture/README.md` (the editor driver and the recorded frames), `briefs/` (one per film), `lab/` (the Shader Lab).
- `claude-liam-lecture-<slug>/` (twenty of them): `SCRIPT.md`, `narration.py`, `beat_sheet.json`, `ACTS.md`, `SHOTLIST.md`, `FACTCHECK.md`, `CHECKS-REPORT.md`, `SOURCES.md`, `CAPTURE-PLAN.md`, `BUILD-PROMPT.md`, `lab-shaders/`, `evidence/planning-checks/`.
- Your words and the verdict are logged in `/Users/bear/Documents/CoWork/bear-textbooks/books/walker-claude/FRICTIONAL.md` (2026-10-13 entry).
