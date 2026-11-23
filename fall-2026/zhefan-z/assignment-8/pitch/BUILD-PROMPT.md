# BUILD-PROMPT — The Little Flame Witch (pitch film)

How this film was built, so it can be rebuilt. Written by Claude Code, 2026-11-22.

**Toolkit:** Brutalist (`brutalist.art` at `29ba0e8`), free local pipeline only: Kokoro narration, Pillow and ffmpeg pictures, the toolkit's compiler and gates. No paid generation, no API key, no upload.
**Workflow:** `godot-waikthrough` (alias `godot-walkthrough`) with the `walker` modifier, for the real footage: its capture contract (isolated snapshot, scripted input through the normal input path, windowed Movie Maker, logged inputs, asserted results), `coverage.json` and its checker. The checkout has **no show-tell skill**, so the pitch beats' simple pictures are drawn by `scripts/cards.py`.
**Output:** `exports/landscape/zhefan-z-little-flame-witch-pitch.mp4`, 3840×2160, 30 fps, 216.53 s, no captions. Kept out of git.
**Voice:** Liam's voice (Kokoro `am_onyx`, local, free) speaking as the author, Zhefan Zhang, in the first person. No instructor name, persona or credit line anywhere.

## Human inputs

- `prompt-1-pitch.txt` (the author's request: beat order, dialogue lines, labels, rules).
- `PROJECT-BRIEF.md` (the seven answers; every claim in the narration comes from it or from a committed log: FACTCHECK.md).
- `art/` and `ART-PROMPTS.md` (the author's Gemini concept art and prompt record).
- One answer from the author during the build: of the two expression sheets in `art/`, the green one is `witch_expressions.png`; the transparent cut-out is left out (PROMPTS.md).
- Not yet: the author's review of this master (`beat_sheet.json` → `metadata.human_review_approved` is `false`).

## Pipeline

```bash
export PYTHONUTF8=1 PYTHONDONTWRITEBYTECODE=1
export BRUTALIST_HOME=<brutalist.art>
GODOT=<Godot_v4.7.2-stable_win64_console.exe>
REEL=fall-2026/zhefan-z/assignment-8/pitch      # from the repository root
BASE=<a scratch folder outside the repository>

# 0. isolated snapshots (git archive of a committed tree; the working tree is never run)
git archive --format=tar -o $BASE/snap840.tar 840b501:fall-2026/zhefan-z/assignment-7/walker-magic-zhefan
git archive --format=tar -o $BASE/snap2b6.tar 2b68e0a:fall-2026/zhefan-z/assignment-5/walker-magic-zhefan
mkdir -p $BASE/cap840 $BASE/cap2b6
tar --force-local -xf $BASE/snap840.tar -C $BASE/cap840; tar --force-local -xf $BASE/snap2b6.tar -C $BASE/cap2b6
$GODOT --headless --path $BASE/cap840 --import; $GODOT --headless --path $BASE/cap2b6 --import
git ls-tree -r 840b501:fall-2026/zhefan-z/assignment-7/walker-magic-zhefan | sha256sum   # coverage build_id

# 1. the two captures (windowed Movie Maker, 60 fps; CAPTURE.md)
$GODOT --path $BASE/cap840 --script $REEL/capture/driver.gd --write-movie $BASE/movie840/frame.png \
  --fixed-fps 60 --resolution 1280x720 --quit-after 4000 -- $REEL/capture/run-01-inputs.jsonl $REEL/capture/run-01-frames.jsonl
$GODOT --path $BASE/cap2b6 --script $REEL/capture/driver_a5.gd --write-movie $BASE/movie2b6/frame.png \
  --fixed-fps 60 --resolution 1280x720 --quit-after 2000 -- $REEL/capture/a5-run-01-inputs.jsonl $REEL/capture/a5-run-01-frames.jsonl
ffmpeg -framerate 60 -i $BASE/movie840/frame%08d.png -vf scale=3840:2160:flags=neighbor -c:v libx264rgb -crf 0 -preset veryfast $REEL/capture/run-01.mp4
ffmpeg -framerate 60 -i $BASE/movie2b6/frame%08d.png -c:v libx264rgb -crf 0 $REEL/capture/a5-run-01.mp4
export CAP_840B501=$BASE/movie840 CAP_2B68E0A=$BASE/movie2b6
export A6_RUN01=fall-2026/zhefan-z/assignment-6/walker-magic-zhefan/youtube/claude-liam-walker-magic-particles-gamedev/capture/run-01.mp4

# 2. beat sheet, narration (durations are the clock), padding
cd $REEL/scripts && python sheet.py && cd -
python $BRUTALIST_HOME/runtime/scripts/generate_audio_kokoro.py $REEL --speed 1.05
cd $REEL/scripts && python sheet.py --pad

# 3. pictures: stills, then the gameplay beats (frame-exact), then the records
python cards.py && python footage.py && python records.py && cd -

# 4. gates: the walkthrough checker, then the final export (beat lint, shape gate, paperwork,
#    output decode and duration check, Gate V final-frame check), then the checker again
$BRUTALIST_HOME/art godot-waikthrough --check $REEL > $REEL/_qc/walkthrough-check.json
$BRUTALIST_HOME/art final $REEL --height 2160 --fps 30 --out $REEL/exports/landscape > $REEL/_qc/final.log
$BRUTALIST_HOME/art godot-waikthrough --check $REEL > $REEL/_qc/walkthrough-check.json
```

`python` is a system Python with `kokoro-onnx`, Pillow and NumPy. FFmpeg 9.0.2 (Gyan build). Windows 11, Git Bash. The Kokoro model sits in the toolkit's `runtime/models/kokoro/`.

## Gate results (this build)

| Gate | Result | Report |
|---|---|---|
| `art godot-waikthrough --check` | PASS: 8 implemented features with evidence intervals in one 3840×2160 capture, 9 planned features with reasons | `_qc/walkthrough-check.json` |
| `art final` preflight: paperwork (FACTCHECK, SHOTLIST, PROMPTS), `beat_lint.py`, `gate_shape.py` | pass | `_qc/final.log` |
| `art final` output check: video and audio decode with `-xerror`, duration equals the timeline, audible | pass | `_qc/final.log` (exit 0) |
| Gate V, `final_frame_check.py` on the final export (the render-integrity gate): 36 frames, each beat at 50% and 85% | **0 BLOCKER, 0 MAJOR** | `_qc/REPORT.md`, `_qc/contact_sheet.png` |

Two builds were exported (the first into a scratch folder, the second into `exports/landscape/`); both gave SHA-256 `00a4dde79db7b48575471d490cbc8bfb39914f11493e99d610e76844e0aea9ce`.

**Fixed before the first export, found by the gates' rules:** the still cards first used 160 px margins and the gameplay canvas reached y 2100, outside Gate V's title-safe inset (x 192–3648, y 108–2052 at 4K); the stills are now composed and scaled to 90 % (`cards.fit_safe`), and the gameplay header was tightened so the ×5 canvas ends at y 2050. A pre-check of the stills alone flagged only B01, the full-bleed title plate, which the sheet declares `qc.full_bleed` with a contrast region on its title text (`qc.contrast_regions`, the gate's documented mechanism; every other check still runs on it). The walkthrough checker failed once on a text-encoding error when run without `PYTHONUTF8=1` (not a film defect); it passes with it.

**Warning printed by the compiler, not a gate:** "SKIN LINT: NO RENDERABLE BEATS". It means no beat uses a Remotion or Manim scene; every slot here is filled from `media/` (18/18 filled, no slates), which the same log confirms.

## Deviations from the toolkit, and why

- **No show-tell skill** in this checkout: the "simple drawn pictures" are Pillow line drawings (`scripts/cards.py`), one picture per beat, minimal text.
- **`walker` bookends not used.** The skill's walker mode opens on a reconstructed Claude prompt (`ClaudeComposerAsk`), then a "what was built" writer, and closes with Verdict and Your Turn. The author's beat order (hook, title, the seven answers, exists/will, outro) replaces them; no Claude response appears on screen.
- **Outro.** OUTRO-LOCK.md's card carries a fixed channel handle (an instructor credit). The author's rules forbid any instructor name, persona or credit line, so the slug is not `claude-liam-*` (the lock's scope) and B17 is a silent card with the title and the author's name only. The toolkit copy has no stock jingle (as in Assignments 1–7), so the outro is silent.
- **Persona.** The skill says "Liam in for Bear"; here the same Kokoro voice speaks as the author, with no instructor reference.
- **4K capture.** The checker requires a 3840×2160 capture; the game renders a 640×360 canvas. `capture/run-01.mp4` is that canvas scaled ×6 nearest neighbour, losslessly (disclosed in CAPTURE.md), not a native 4K render.
- **Narration speed.** Kokoro at `--speed 1.05`, to keep the film near 3½ minutes; some tokens are spelled for speech (`SAY` in `sheet.py`).
- **Remotion not used.** Every beat is a Pillow still or an ffmpeg-encoded gameplay clip in `media/`, compiled by `art final`.

## What was written where

- **In the reel (`pitch/`):** `beat_sheet.json`, `coverage.json`, `SHOTLIST.md`, `FACTCHECK.md`, `PROMPTS.md`, `CAPTURE.md`, `BUILD-PROMPT.md`, `SOURCES.md`, `scripts/`, `capture/` (drivers and logs), `evidence/`, `_qc/`, and, kept out of git, `mp3/`, `media/`, `clips/`, `exports/` and the capture archives.
- **Outside the repository:** the snapshots, capture copies and PNG frames in a scratch folder.
- **Not touched:** no game file, no `shaders/` folder, no earlier assignment folder (the Assignment 6 capture archive was only read and hashed), and nothing in the toolkit checkout.

## Added 2026-11-22 — rebuild from the GDD (prompt-2-gdd.txt)

Written by Claude Code. Everything above describes the first cut and stays as written; this section is how the current master was built. This master replaced the first cut's (SHA-256 `00a4dde7…`) in `exports/landscape/`.

**Human inputs added:** `prompt-2-gdd.txt`; `GDD.md` 2.0 (2026-11-21) with `A4-GDD.pdf`, the revised `PROJECT-BRIEF.md` and `ART-PROMPTS.md`, committed with the author's messages in `510f0f0a`, `336b5373`, `6045d283` after the Step 1 check (PROMPTS.md rows 4–6).

**Structure** (the updated spec's order): T00 title with the GDD's metadata → P01 the game in brief → G01–G16 the GDD's sixteen beats → Q01, Q02, Q03, Q04, Q05, Q07 (+ Q07B–D footage), the questions the GDD beats have not already answered (question 6 is G15; in and out are G12 and G13) → A01–A05 the appendix → OUT the silent outro. 33 beats, 430.83 s.

**Pipeline changes** (same environment variables as above, plus `CAP_840B501_FAIL`):

```bash
# the new capture (CAPTURE.md, "Added 2026-11-22"); trials first, headless, logs to scratch
$GODOT --headless --path $BASE/cap840 --script $REEL/capture/driver_fail.gd --fixed-fps 60 --quit-after 1500 -- <in> <out>
$GODOT --path $BASE/cap840 --script $REEL/capture/driver_fail.gd --write-movie $BASE/moviefail/frame.png \
  --fixed-fps 60 --resolution 1280x720 --quit-after 1500 -- $REEL/capture/run-02-inputs.jsonl $REEL/capture/run-02-frames.jsonl
ffmpeg -framerate 60 -i $BASE/moviefail/frame%08d.png -vf scale=3840:2160:flags=neighbor -c:v libx264rgb -crf 0 -preset veryfast $REEL/capture/run-02.mp4
# the Assignment 3 prop scene, one render
$GODOT --path $BASE/cap840 res://showcase3d/prop_room.tscn --write-movie $BASE/movieprops/frame.png --fixed-fps 30 --resolution 1920x1080 --quit-after 30
cp $BASE/movieprops/frame00000020.png $REEL/capture/props-840b501-frame20.png
export CAP_840B501_FAIL=$BASE/moviefail

cd $REEL/scripts && python sheet.py && cd -
python $BRUTALIST_HOME/runtime/scripts/generate_audio_kokoro.py $REEL --speed 1.05
cd $REEL/scripts
python sheet.py --pad        # every beat but G11
python audio.py              # G11: the narration, then the game's own music and effects; its track and timed picture
python cards2.py             # the stills (python cards.py now runs the same)
python footage.py            # G04, G05, Q07B-D, A01
python records.py            # coverage.json; SHOTLIST.md (the first-cut table kept, the rebuild appended)
cd -
$BRUTALIST_HOME/art final $REEL --height 2160 --fps 30 --out $REEL/exports/landscape > $REEL/_qc/final.log
$BRUTALIST_HOME/art godot-waikthrough --check $REEL > $REEL/_qc/walkthrough-check.json
```

**Gate results (this build):**

| Gate | Result | Report |
|---|---|---|
| `art godot-waikthrough --check` | PASS: 10 implemented features with evidence in two 3840×2160 captures of 840b501 (run-01, run-02), 9 planned with reasons | `_qc/walkthrough-check.json` |
| `art final`, first run | **REFUSED** by Gate V: Q01 at 50 % and 85 %, "ink/background luminance separation 0.24 < 0.3" (the pale-blue zip drawing averaged too close to the page) | the failing report was overwritten by the passing run; this entry records it |
| the fix | the zip drawing in `cards2.q01` filled with the darker cave blue; Q01 alone re-checked with `final_frame_check.py --frames-dir`: 0 BLOCKER, 0 MAJOR | — |
| `art final`, second run | exit 0: paperwork, beat lint, shape gate, decode and duration check, audible; **Gate V: 66 frames, 0 BLOCKER, 0 MAJOR** (P01's text checked in its declared contrast region) | `_qc/final.log`, `_qc/REPORT.md`, `_qc/contact_sheet.png` |
| G11, by measurement (not a toolkit gate) | in the master, each excerpt plays at its planned time (the music from 172.88 s, the five effects 179.68–185.17 s), at −16 to −22 dB RMS against silence in the gaps; the narration is about −24 dB RMS | this entry |

The compiler again printed the "SKIN LINT: NO RENDERABLE BEATS" warning (no Remotion or Manim beats; 33/33 slots are filled from `media/`).

**Deviations added in the rebuild:**
- **G11's track is built by `audio.py`, not by Kokoro alone:** the measured narration, then the music excerpt (the loop's first 6 s, 0.4 s fades, at −8 dB, the game's own Music bus level) and the five effects whole at their file level, with gaps. Its picture lights each row while it plays. The compiler's narration-length check holds because `actual_duration_s` is the mixed track's measured length.
- **Reused cards keep their first-cut headings:** Q02 "Why anyone would care", Q03 "Who opens it…", Q04 "What it proves…", Q07 "Why this project…" (no "Question n ·" prefix).
- **The first cut's generated media were deleted** (B00–B17 in `media/`, `mp3/`, `clips/`) before the rebuild, so none could leak into it. They were never in git and can be rebuilt with `cards.main_first_cut()` and the first cut's sheet at `8a8e23ea`.

**The prompt, word for word** (`prompt-2-gdd.txt`, the author's; the file itself is not committed):

```text
Assignment 8 changed on origin/main (135fc9d0, 2026-11-20): the film is now
built from a GDD, in four parts: the game in brief, the GDD's sixteen beats,
the seven questions, and an appendix. The full spec is at
E:/7270/a8-spec-new.md; read it first. Same rules as before: work on
zhefan-z/assignment-8 in fall-2026/zhefan-z/assignment-8/pitch/, never push,
no Co-Authored-By, never touch shaders/ or earlier assignment folders, and
never stage the crystal-palace deletions or anything outside pitch/.

I saved into pitch/: GDD.md (new), PROJECT-BRIEF.md (revised: game in
brief, appendix with the asset table) and ART-PROMPTS.md (your two
corrections fixed).

Step 1 - check, then commit.
Check every "Built" claim and every number in GDD.md and PROJECT-BRIEF.md
against my game at 840b501 and the earlier assignments' records: the
controls (move keys, jump, aim, cast), the HP and what happens on a hit
(tint, blink or invulnerability), fail and restart, the wolf phase table,
the music and sound tools and their licences as recorded in Assignment 2's
SOURCES.md, the commits cited. If a Built claim or a number is wrong,
stop and tell me before anything else; do not change my wording. If all
hold, commit in three commits: GDD.md as "GDD 2.0 for the final project
(claude.ai drafted from my answers and my A4 GDD; mine)"; PROJECT-BRIEF.md
as "PROJECT-BRIEF revised for the updated A8: game in brief, appendix
(claude.ai drafted from my answers; mine)"; ART-PROMPTS.md as
"ART-PROMPTS: two corrections (mine)".

Step 2 - rebuild the film from the GDD, in the spec's order:
 - Title card: the title, my name, and the GDD's version and date
   (2.0, 2026-11-21) as the metadata section.
 - The game in brief: what it is and the goal, with one picture (a real
   840b501 frame, labelled; the concept portrait may sit beside it,
   labelled generated).
 - The GDD, sections 1-16 of GDD.md, one beat each, one picture and a
   sentence or two. Show the thing itself wherever it exists: real
   840b501 footage for mechanics and systems (the wolf's phases and the
   growl cancel); the dialogue scenes and portraits for narrative and
   characters; for art direction, the art itself (pixel sprites, run
   cycle, lunge rig, 3D props, cave lights, the portraits) plus the planned
   look as drawn pictures; for sound and music, play short excerpts of
   the real Assignment 2 music and sound effects from the 840b501 game
   files, captioned with what each is and how it was made.
 - The seven questions, without repeating what the GDD beats already
   said: 1 the artifact and its form; 2 the unique value with the
   comparable games (names only); 3 who opens it and the first sixty
   seconds; 4 what it proves, with the A7 evidence; 5 only the first
   piece and how anyone would know it ran (in and out are GDD 12 and 13);
   7 why this project, with the A5, A6 and A7 footage by revision.
   Question 6 is GDD 15; do not repeat it.
 - Appendix: exists today (real footage), started, not started, whether
   one person can finish it and the cut order, and the asset table from
   PROJECT-BRIEF.md shown as a card.
 - The silent outro.
 Reuse everything already built and checked (captures, stills, dialogue
 scenes, the drivers); regenerate only what changes. No fixed length:
 keep each beat to one picture and a sentence or two. Every rule from
 the first prompt still holds: past tense only for what exists, every
 frame labelled real (with its revision), generated or constructed, no
 comparable-game footage, no invented numbers, Liam speaks as me, no
 instructor name, persona or credit line. Run the checker and the final
 export's render-integrity gate; fix and re-render until both pass.

Step 3 - records. Update beat_sheet.json, BUILD-PROMPT.md (add this
prompt), SOURCES.md (the music and sound excerpts with their tools and
licences), CAPTURE/FACTCHECK/SHOTLIST and the gate reports. Keep media out
of git. Commit as "Pitch film rebuilt from the GDD (agent, Brutalist)".
Report the file name, path, length, size and SHA-256, the beat list with
each beat's part (brief, GDD section, question, appendix) and label, and
stop. I will write README.md and FRICTIONAL.md after watching it.
```

## Added 2026-11-22 — tightened to under four minutes (prompt-3-tighten.txt)

Written by Claude Code. The sections above (first cut, rebuild) stay as written; this is how the current master was built. It replaced the rebuild's master (SHA-256 `a1f7ac0f…`, 7:11) in `exports/landscape/`.

**Human input added:** `prompt-3-tighten.txt` (word for word below), and the corrected `PROJECT-BRIEF.md` question 7, which I checked against the Assignment 3 branch (`8141177b`: the prop room's mage is a billboarded `Sprite3D` of `mage_idle.png`, with no script or animation) and committed with the author's message in `770a2aaf`.

**What changed, and what did not:**
- **Narration:** rewritten from GDD.md and PROJECT-BRIEF.md to the time budget, one short sentence per GDD beat (`PLAN` in `scripts/sheet.py`), and regenerated with Kokoro at `--speed 1.05`. Default silences are now 0.2 s lead and 0.3 s tail. Minimum holds: G04 and G05 7 s, Q07X 10 s, A01 7 s, and A05 (the asset table) 6 s.
- **Beats:** 31 instead of 33. Q07B, Q07C and Q07D became one footage beat, Q07X: the three revisions in one cut, each span captioned with its assignment and revision. Every required part is still its own beat: title (T00), the game in brief (P01), G01–G16, questions 1, 2, 3, 4, 5 and 7 (question 6 is G15), the appendix (A01–A05) and the outro.
- **Footage** (`scripts/footage.py`, the same captures): G04 run 140–360, cast 1515–1555, pit fail 250–385; G05 lunges 870–1030, cancel 1520–1590 with a ×0.25 replay of 1540–1556; Q07X 2b68e0a 440–560 (+ replay 472–500), 3c37fe0 290–420, 840b501 200–380; A01 15–330, 990–1040, 1520–1590. The lunge-commit span (2040–2148) is no longer shown; `coverage.json` names it under "not shown".
- **Sound cut** (`scripts/audio.py`): the music excerpt is now the loop's first 1.5 s with 0.25 s fades (was 6 s, 0.4 s), and the gaps are 0.2 s (were 0.8 s). The five effects still play whole, with every caption and the Stability AI notice on screen.
- **Cards:** only question 7's "new to me" lines changed, to the corrected brief ("a whole 3D cave level, its lighting and camera"; "2D sprites that run and fight in it (A3: one static billboard)"), set at 48 px to fit. Every other picture is reused unchanged.
- **Footage headers:** a beat that mixes revisions is now labelled "Real captures · scripted input · revisions 2b68e0a, 3c37fe0, 840b501 (each span labelled)". The first version of Q07X wrongly added "(Assignment 5)" to all three revisions and gave one frame rate for all three sources; I caught both on a sampled frame and fixed them before the export. The source line now gives each capture's own frame rate.

**Length by part** (target → result): title + brief about 15 s → 15.8 s; GDD 1–16 about 1:50 → 1:47.3; questions about 1:10 → 1:05.0; appendix about 30 s → 32.9 s; outro about 5 s → 5.0 s. **Total 225.97 s (3:46).**

**Gate results (this build):**

| Gate | Result | Report |
|---|---|---|
| `art godot-waikthrough --check` (before and after the export) | PASS: 9 implemented features with evidence intervals inside the spans now shown, 9 planned | `_qc/walkthrough-check.json` |
| `art final` | exit 0 on the first run: paperwork, beat lint, shape gate, decode and duration check, audible; **Gate V: 62 frames, 0 BLOCKER, 0 MAJOR** | `_qc/final.log`, `_qc/REPORT.md`, `_qc/contact_sheet.png` |
| G11, by measurement | in the master the music plays from 82.81 s and the five effects from 84.51 s to 87.60 s, at −16 to −22 dB RMS | this entry |

**Commands:** as in the rebuild section above; `generate_audio_kokoro.py` was run for every beat, and the capture steps were not repeated.

**The prompt, word for word** (`prompt-3-tighten.txt`, the author's; the file itself is not committed):

```text
Same branch, folder and rules as prompt-2 (never push, no Co-Authored-By,
nothing outside pitch/, media out of git, committed docs only gain dated
additions). Read E:/7270/a8-spec-new.md again if needed.

Goal: cut the film from 7:11 to between 3:30 and 3:59 while keeping every
part the updated spec requires in the film: the title card with the GDD
metadata, the game in brief with one picture, all sixteen GDD beats (each
its own beat, art and sound shown), the seven questions answered once
each, and the appendix. The full detail stays in GDD.md and
PROJECT-BRIEF.md; the film is the fast version.

I saved a revised PROJECT-BRIEF.md (question 7: what is new is a whole 3D
level with sprites that run and fight in it; Assignment 3 had only a
static billboard). Check it and commit it first as "PROJECT-BRIEF:
question 7 corrected (mine)".

Time budget (narration is the limit; pictures follow it):
 - Title card + game in brief: about 15 s together.
 - GDD 1-16: about 1:50 in total. One short sentence per beat (about 12-18
   spoken words), one picture each. GDD 4 and 5 keep real 840b501 footage,
   about 6-8 s each; GDD 11 keeps a quick cut of the real music and
   effects, about 6-8 s, still captioned with tool and licence. GDD 10
   keeps the real art beside the planned look. GDD 12 shows the
   Must/Should/Could card, GDD 14 the stack card, GDD 16 the open
   questions.
 - The seven questions: about 1:10, without repeating the GDD: 1 the
   artifact (a Windows .exe in a zip); 2 the unique value and the
   comparable games, names only; 3 who opens it and the first sixty
   seconds; 4 what it proves, with the pin and test table; 5 only the
   first room and how anyone would know it ran; 6 is GDD 15, not
   repeated; 7 why this project, with a short cut of the 2b68e0a,
   3c37fe0 and 840b501 footage.
 - Appendix: about 30 s: exists today beside real footage; started; not
   started; one person and the cut order; the asset table as one card
   held about 6 s (the full table is in PROJECT-BRIEF.md).
 - Silent outro: about 5 s.
Rewrite the narration from GDD.md and PROJECT-BRIEF.md to fit, in my
voice, keeping every honesty rule: past tense only for what exists, every
frame labelled real (with revision), generated or constructed, no
comparable-game footage, no invented numbers, no instructor name,
persona or credit line. Reuse every picture and capture already built;
change only timing, narration and any card text that must shrink.

If the narration cannot fit under 3:59 without dropping a required beat,
stop and tell me the shortest you can reach and what you would cut.

Run the checker and the final export's render-integrity gate; fix and
re-render until both pass. Then append dated sections to the records
(beat sheet, BUILD-PROMPT with this prompt word for word, SHOTLIST,
FACTCHECK, CAPTURE, SOURCES if anything changed), commit as "Pitch film
tightened to under four minutes (agent, Brutalist)", report the file
name, length, size and SHA-256 and the beat list with each beat's
duration and label, and stop.
```
