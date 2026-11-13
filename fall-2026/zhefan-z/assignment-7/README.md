# walker-magic — Assignment 7: animation with Godot and Claude

Zhefan Zhang (zhefan-z), CSYE 7270 Fall 2026. *walker-magic* is a 2D side-scroller: a mage crosses a cave and casts fireballs at a wolf. Godot 4.7.2-stable, Forward+, Windows. Starting point: my Assignment 6 project, unchanged (`027a0ab`). Tag: none, per the instructor (2026-10-09); the submitted commit is named in the Canvas note.

![Before and after, the same physics tick of the same scripted lunge](captures/look/before_after.png)

*The same moment (`take_lunge`, physics tick 40) before Assignment 7 (`2276069`) and now: the wolf's lunge is a keyed cutout rig with a crouch, a stretch and an afterimage; the mage runs a four-frame cycle; the cave is lit by flickering torches with drifting embers. Gameplay in this scenario is identical on every tick; across all eight pin scenarios only the two growl-hit scenarios changed, by design (pin, below).*

Paths: game files (`tests/`, `effects/`, `features/`, `tools/`, `design/`) are relative to `walker-magic-zhefan/`; `captures/`, `logs/` and the documents are relative to this folder.

## Evidence at a glance

**8** behaviour pin scenarios compared tick by tick at **30, 60 and 144 fps** · **7** new suites · **13** earlier suites unchanged · the **four published mutations**, each from a worktree (three caught, the empty-cache reimport shown safe), plus four more · edges: an interrupt **one tick before, on and after every phase boundary** (25 / 0 at three rates) · the phase table measured from the game (31 / 22 / 36 ticks) · every visual upgrade added with the pin still **8/8**.

| Rubric criterion (of 60) | Where the evidence is |
|---|---|
| **Brief and pins before the change (10)** | `CHANGE-BRIEF.md` committed before the first prompt (`2cc97d0`), restated in the published structure (revision 2026-11-13: both routes, phase table in frames with `step`, cycle spec and seam rule, state machine, two clocks, one authority, evidence split, short answers); pins before the change (`a9b4bc1`) and re-run after; `CLAUDE.md` agent draft (`9115352`) and my reviews committed apart (`2a53662` and the second review) |
| **The animation set (12)** | Run: Sprite2D + AnimationPlayer frame track, sheet credited (`assets/sprites/mage/ATTRIBUTION.md`, original in `design/a7/`), slicing 62×69, 4 × 1, read back by `test_clip_run.gd` (17/0). Lunge: cutout rig keyed as resource text, read back by `test_clip_lunge.gd` (18/0) with the published `track_problems()`. Seam by track type; the lunge keyed at every phase boundary |
| **State machine and authority (10)** | `test_anim_structure.gd` (11/0) asserts the state table against the scenes; one authority per animated node, named in `CLAUDE.md` ("One authority") and the brief; current clip read through `current_animation` |
| **Edges, re-pins and verification (10)** | `test_anim_edges.gd` (25/0 at 30, 60, 144); mutations M1–M4 (`logs/mutation-a7-M*`); the behaviour change apart (`72f37b8`) and re-pinned after play in its own commit (`ff71bbb`) |
| **Feel and readability (8)** | real-render lunge strip read at each phase boundary (`captures/lunge/game-r0/`); observation-driven revisions with predictions, two strips and my verdicts (`TUNING.md`: run r0 → r1 reverted → r2 kept; visual upgrades r0 → r1 kept); my checks: the three phases read as distinct, the cycle wraps cleanly over five wraps |
| **Film (10)** | see Film below |

## The two clips

| | Clip 1: mage run cycle | Clip 2: wolf lunge |
|---|---|---|
| Route | Sprite2D with an AnimationPlayer frame track | Cutout rig keyed as resource text |
| Driven by (one authority) | the player's state machine (RUN) → the mage's AnimationPlayer | the wolf's state machine (GROWL → LUNGE → RECOVER) → the wolf's AnimationPlayer |
| Loop | `LOOP_LINEAR`, 4 frames at 10 fps, `step` 0.1 (24 ticks per cycle; 5/6/6/7 ticks per frame after the first loop) | `LOOP_NONE`, committing action, 89 ticks at 60 fps, `step` 1/60 |
| Source | 4-frame sheet drawn by Gemini from my prompt with my A2 sprite as the reference, cleaned onto my A2 palette (`tools/clean_run_cycle.py`) | my A2 `wolf_lunge.png`, unchanged, as two `region_rect` parts on hip and shoulder pivots |
| Timing | cycle 0.4 s; seam: no duplicate across the wrap, last-key gap = key interval | phase table measured by the pin: growl 31, lunge 22, recover 36 ticks; keys at frames 0, 25, 31, 37, 53, 65, 89 |
| Motion reference | Muybridge, *Animal Locomotion* plate 60, a man running (1887, public domain) | Muybridge plate 707, a dog galloping (1887, public domain) |

**Behaviour change (one, by design):** a fireball hit during the growl cancels the lunge; a hit during the lunge does not; death wins in every phase. Measured in play with real clicks: from sight distance only a cast in the first 12 of 31 growl ticks (0.2 s) arrives in time (`captures/figures/growl_window.png`).

## Beyond the requirements

| Upgrade | What you see | Evidence |
|---|---|---|
| Flickering cave torches | warm pools of light on both walls, a looping continuous-track clip | `effects/cave_lights.tscn`, `test_clip_flicker.gd` (12/12, seam per track) |
| Drifting embers | 144 slow sparks across the level | `effects/embers.tscn` |
| Lunge afterimage | about five warm ghosts trail the dash | `features/wolf/lunge_afterimage.gd`, `test_afterimage.gd` (6/6 at 30, 60, 144) |
| Four-frame run | from two flickering pictures to a run, after three rejected attempts | `TUNING.md` run r0–r2 |
| Measured readability | the mage's robe-to-cave contrast 3.07, above the 2.74 before A7 | `TUNING.md` visual r1 |
| Figures from the logs | pin timeline, growl window, two clocks, lunge onion skin, run cycle | `captures/figures/`, `tools/make_figures.py` |

Every upgrade is visual only: the pin passes 8/8 at 30, 60 and 144 fps after each.

## Run it

- Open `walker-magic-zhefan/project.godot` in Godot 4.7.2 and press F5. Controls: A/D or arrows to walk, Space/W/Up to jump, left mouse to cast, Esc to pause, R to restart, M and N to mute.
- Tests, from this folder in Git Bash, after `godot --headless --path walker-magic-zhefan --import` once:
  - `./scripts/run-test.sh test_pin_behaviour.gd 60` (also 30 and 144; `PIN_MODE=record` re-records)
  - `./scripts/run-test.sh test_anim_edges.gd 60` (also 30, 144), `test_afterimage.gd` (30, 60, 144), `tests/probe_two_clocks.gd` (30, 60, 144)
  - `./scripts/run-test.sh test_clip_run.gd 60`, `test_clip_lunge.gd`, `test_clip_flicker.gd`, `test_anim_structure.gd`
  - the thirteen earlier suites as listed in `CLAUDE.md`
- Documents: `CHANGE-BRIEF.md` (spec and dated revisions), `TUNING.md` (every observation, prediction, comparison and verdict), `TEST-REPORT.md`, `FRICTIONAL.md`, `SOURCES.md`.

## Known limitations

- The growl-cancel window is 0.2 s from sight distance, kept by my decision.
- The run's planted foot still slides while a frame is held; frame 1 of the Gemini sheet is close to my A2 contact pose.
- The wolf's removal after death runs on the frame clock (tick 79 at 60 fps, 80 at 30 and 144); gameplay never reads it.

## Film

*Keys on the Tick: A Run Cycle and a Wolf Lunge*, about 6:15, 3840×2160, 30 fps, narrated by Liam (AI).

- Link: https://drive.google.com/file/d/1oc7IkXeZJKSzBW5NfGxx9UoAIhihSnLg/view?usp=sharing
- File: `claude-liam-walker-magic-animation-gamedev.mp4` (77,177,746 bytes)
- SHA-256: `7f4874b987db96eaf0b495cf8fb4c108d038e09c3fc9a3c06c9123ba6e182f4a`
- Game source shown: `f860fed`. In-play footage is real engine output from scripted input (a windowed Movie Maker capture at 60 fps, one frame per physics tick); harness images are labelled fixture captures. Film records: `walker-magic-zhefan/youtube/claude-liam-walker-magic-animation-gamedev/`. The MP4 is not in git.
