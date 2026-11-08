# walker-rudy — particle effects (Assignment 6)

CSYE 7270, Assignment 6: *Creating Particle Effects with Godot and Claude*. By Shuai Zhang.

**How this README was made:** Claude Code (Claude Opus 5.5) drafted it on 2026-11-07 at my request ("接着写", "carry on writing"), from this folder's files and records. I reviewed it the same day, before it was committed ("看过了，没问题", "I've read it; no problems").

walker-rudy is my 2D side-scroller from Assignment 2: Rudy crosses Level 1, Harvest Fields, past spikes, goblins and a waystone checkpoint to the teleport circle. This assignment adds one layer, two particle effects, both on Rudy and both in the 2D game:

- **Effect A, sword-swing sparks (`SlashSparks`).** A one-shot burst, a white flash and 28 streaks of sparks, on the spot and at the moment his sword's hitbox goes live. The hitbox is live for only 0.15 s of a 0.3 s swing, and nothing on screen showed it before.
- **Effect B, a running dust trail (`RunDust`).** While Rudy runs on the ground, a line of dark dust stays behind his boots and rises as it thins. It stops the moment he stops or leaves the ground.

| | |
|---|---|
| Starting point | Tag `a5`. `game/` is [`../assignment-5/game/`](../assignment-5/game/) as committed at `a5`, copied with `git archive` in `e61e8025` (142 files). `game/project.godot` has not changed since. No change of game since Assignment 2 |
| Godot | 4.7.2.stable.official.ed1daf0bf, the standard build |
| Renderer | GL Compatibility on desktop and mobile (`game/project.godot` lines 16, 95–96). It does not draw particle trails, so Effect B's trail is made without them ([evidence/compat-probe/](evidence/compat-probe/)) |
| Machine | macOS 15.1, Apple M3. Not tested on any other system |
| Effect A | Event: `Rudy/SwordHitbox/Shape.disabled` turning from true to false, read every physics tick (no signal exists for it, and none was added). Nodes: a `Node2D` root with two `GPUParticles2D`, `Flash` and `Sparks`. Retrigger rule: **overlap**. Every cut gets its own burst, and at most 2 are alive at once |
| Effect B | Job: a trail. Condition: in play, on the floor and moving faster than 1 px/s, read every physics tick. Node: one `GPUParticles2D` with `local_coords` off, so each puff stays where it was born. Features Effect A does not use: **damping** and a box emission shape |
| Budget | 0.25 ms of GPU time per effect, compared on GPU time from the editor's Visual Profiler. On this Mac the profiler's GPU column read 0.0 ms, so the budget could not be evaluated (Known limitations) |
| Textures | None sourced and none generated. Every texture is a `GradientTexture2D` defined inside the effect scenes; [SOURCES.md](SOURCES.md), "Textures", is the credits record |
| Assistance | Claude Code (Claude Opus 5.5), in the desktop app and as scoped `claude -p` sessions; Codex (OpenAI's coding agent) for the Use It measurements and captures. Who did what: [SOURCES.md](SOURCES.md) and [FRICTIONAL.md](FRICTIONAL.md) |
| Final film | *Sparks and Dust for Walker Rudy.* (Brutalist `godot-gamedev`, `walker` modifier; 12:22, 3840×2160), file `claude-liam-walker-rudy-particles.mp4`, SHA-256 `6bdc9809c6edd052f5a3ba99150cf553da3ceb6ecdb9bfeb7761e7407aeebbe9`. It shows the game source at `d0ed4152`, unchanged since `d60fb037`; the commit that adds the film's folder (`3d120352`) changes nothing in `game/`. Course media: [claude-liam-walker-rudy-particles.mp4 on Google Drive](https://drive.google.com/file/d/1qAWW-L9Z0K5cUQ3Nql18tFhFgYpp4KuR/view?usp=sharing). The MP4 is not in git; its beat sheet, prompts, evidence and checks are in [youtube/claude-liam-walker-rudy-particles/](youtube/claude-liam-walker-rudy-particles/) |

## Run it

In a fresh clone, import the project once, from this folder:

```bash
godot --headless --path game --import
```

`godot` is the Godot 4.7.2 binary (on macOS, `/Applications/Godot.app/Contents/MacOS/Godot`).

**The game.** Open `game/project.godot` in Godot 4.7.2 and press F5, or run `godot --path game`. The main scene is `res://app/main.tscn`. The dust shows as soon as Rudy runs. For the sparks, run right past the first spikes and goblin to the sword pickup at x 2500, then press J or X; press it again and again to see two bursts at once.

**The previews.** Both are fixtures, not the game: the real level frozen behind the effect, with a still sprite of Rudy for scale (CHANGE-BRIEF.md, section 6). The frame strips in `captures/` were recorded from them with Movie Maker, for example:

```bash
godot --path game res://previews/slash_sparks_preview.tscn --write-movie "$PWD/captures/slash_sparks/r1/frame.png" --fixed-fps 30 --quit-after 60
```

`res://previews/run_dust_preview.tscn` runs the same way, with `--quit-after 70`. To watch a preview at real speed instead, use `--fixed-fps 30 --max-fps 30` without `--write-movie`.

## Controls

The game's, unchanged from Assignment 2, plus F9:

- A/D or ←/→ move. On the ground, a tap of the other direction turns Rudy on the spot; hold it to move.
- Space, W or ↑ jump.
- J or X slash, once Rudy has the sword.
- Enter on the title starts play; on the end card it plays the level again.
- Esc pauses and resumes. While paused, both effects freeze where they are and stay visible.
- M mutes the music and N the sound effects.
- F1 shows or hides the debug line.
- **F9 turns vsync off and on again**, for the FPS comparison in the GPU price. It is read by `game/app/vsync_debug.gd` (the `VsyncDebug` node in `game/app/main.tscn`), works while paused, and prints the new mode to the Output panel. No other action used F9, and no project setting changed for it.

## Tests

Run every test through the course's wrapper, from this folder: `scripts/run-test.sh <test-file in game/tests/> <fps|realtime> [timeout-seconds]`. It pins the frame rate and times out after 120 s by default; status 124 means a hang. It writes `logs/<test>_<fps>fps.log`, and fails on any `SHADER ERROR` or `SCRIPT ERROR` line whatever Godot's exit code. Every test here runs at a fixed frame rate, not realtime: none waits on audio.

| Command | Expected | What it checks |
|---|---|---|
| `scripts/run-test.sh checks.tscn 60` | 141 `PASS`, `all checks passed` | Assignment 2's checks, unchanged |
| `scripts/run-test.sh invulnerable_tint_checks.tscn 30` (and `60`, `144`) | 15 `PASS`, `all checks passed` at each rate | Assignment 5's tint checks, unchanged |
| `scripts/run-test.sh test_slash_sparks_config.gd 60` | 108 `PASS`, then `PASS  test_slash_sparks_config: 0 failure(s)` | Every setting of `slash_sparks.tscn` against the brief, with Godot 4 names, and a text scan for Godot 3 names |
| `scripts/run-test.sh test_slash_sparks_state.tscn 60` | 14 `PASS` (S1–S14), `all checks passed` | Effect A in the real `Main` through the real input actions: one burst per live cut and none otherwise, its place and facing, two cuts 19 ticks apart overlapping, the bursts' parent, pause |
| `scripts/run-test.sh test_run_dust_config.gd 60` | 61 `PASS`, then `PASS  test_run_dust_config: 0 failure(s)` | Every setting of `run_dust.tscn` against the brief as revised, including damping and the box emission shape |
| `scripts/run-test.sh test_run_dust_state.tscn 60` | 14 `PASS` (D1–D14), `all checks passed` | Effect B in the real `Main`: `emitting` against the condition every tick through running, stopping, turning, jumping, a knockback and a respawn; its place at his feet; pause; hidden; its place in the tree |
| `scripts/run-test.sh cost_effects.gd 60 300` (a 300 s limit, as its header says) | A table, not a pass or fail: empty scene about 0.004 ms per frame, the game without effects about 0.05 ms, each effect less than 0.01 ms more | The headless CPU price, with an empty-scene control (Example 09's script, adapted) |

The results, the eight mutations that fail these tests, the reading of the generated process shader, the prices and what a headless run cannot show are in [TEST-REPORT.md](TEST-REPORT.md). The wrapper writes every run of a test to the same log, so each mutation's log was copied to `logs/mutation_*_60fps.log`.

A headless run draws nothing, so the look is judged from the frame strips and in the running game ([TUNING.md](TUNING.md), [TEST-REPORT.md](TEST-REPORT.md), "Use It"). The windowed captures are not headless tests: the two previews above, and the F9 check in [evidence/vsync-check/](evidence/vsync-check/).

## What this assignment added

- **The specification, before any prompt.** [CHANGE-BRIEF.md](CHANGE-BRIEF.md), revision 1 (`cc9f7195`), after the Compatibility probe it depends on (`9e19fe47`). It holds the state of the game, both effects' jobs, intent, settings and observable rules, the boundaries, the evidence split, frame-by-frame predictions for both strips, 13 predicted failures, the prices and budget, and the short answers. Revisions 2–4 are dated at its end: Godot 3 names in a scene file, Effect A's tuning, Effect B's tuning.
- **Context for the agent.** [CLAUDE.md](CLAUDE.md), 92 lines. A scoped `claude -p` session drafted it, committed unedited (`998fd175`). The review, with the headless particles probe behind it, was committed apart from the draft (`a3242b9d`), and one line on Godot 3 names was added with Revision 2 (`06c16892`).
- **Effect A.** `game/effects/slash_sparks.tscn`, its preview `game/previews/slash_sparks_preview.tscn` and `game/tests/test_slash_sparks_config.gd`, written by a scoped session (`ea4419ae`). One tuning round: `Sparks` `amount` 14 → 28 (`fed848b8`). The trigger, `game/effects/effects_driver.gd` on an `Effects` node after `Rudy` in `game/app/main.tscn`, and `game/tests/test_slash_sparks_state.gd`, written by a scoped session from its approved plan (`ebe2d9d5`).
- **Effect B.** `game/effects/run_dust.tscn`, its preview `game/previews/run_dust_preview.tscn` and `game/tests/test_run_dust_config.gd`, written by a scoped session (`017e8a52`). Three tuning rounds: a darker, opaque colour ramp (`0c45ac1e`), `amount` 20 → 40 (`ed46992c`), initial velocity 40/90 → 80/160 px/s (`9a3d1c16`). The wiring, a `DustTrail` node before `Rudy` and the same driver placing and switching it, and `game/tests/test_run_dust_state.gd` (`d0abc9dd`).
- **Tuning.** [TUNING.md](TUNING.md): for every round, my first look before Claude read a frame, Claude's reading and prediction, the strips before and after, Claude's comparison and my verdict in the running game. The strips, labelled fixture captures, are in [captures/](captures/).
- **The process shader.** `game/shaders/particles_generated.gdshader`, generated by me in the editor from a copy of `Sparks`' material and unedited; my reading is in TEST-REPORT.md, "The process shader" (`8b795772`). The game does not use it.
- **The price.** `game/tests/cost_effects.gd`, written by a scoped session (`fe303c70`), and the report (`6c6676d0`); the F9 key (`d60fb037`); the GPU price and the checks in play, recorded by Codex at my request in [evidence/use-it-code/](evidence/use-it-code/) (`d0ed4152`).
- **Records.**
  - [TEST-REPORT.md](TEST-REPORT.md), [FRICTIONAL.md](FRICTIONAL.md) and [SOURCES.md](SOURCES.md).
  - The scoped sessions' prompts, plans and full transcripts are in [sessions/](sessions/). Every transcript is under 1 MB (the largest is 0.85 MB), so none is an excerpt. `sessions/plan-3.md` is Claude's English translation of a plan the session wrote in Chinese, and says so.
  - The logs cited are in [logs/](logs/), and the probes in [evidence/compat-probe/](evidence/compat-probe/) and [evidence/headless-probe/](evidence/headless-probe/).
- **The film.** It is linked in the table above (`3d120352`).

## Known limitations

- **The GPU price was not measured.** The Visual Profiler's GPU column read 0.0 ms in every row and every state, and the runtime GPU-time API returned 0 (the brief's predicted failure 12). A zero is not a pass, so the 0.25 ms budget is not evaluated. The FPS fallback with vsync off (239–438 FPS, above the reported 60 Hz) is not GPU time, and the two idle baselines alone differ by about 80 FPS. The next step is to measure GPU time on a machine whose profiler reports it.
- **An unexplained frame rate.** With vsync on, the game held about 120 FPS on a display that reports 60 Hz (`evidence/vsync-check/README.md`). The display may run faster than it reports; the check does not settle which.
- **Some checks in play are Codex's captures, not my own item-by-item checks.** I played the game after each effect was wired in and on 2026-11-06, and found no problem; after Step 3 I did not list which checks I made. The edge-of-screen and against-the-background checks rest on Codex's sampled frames, not on a continuous look (TEST-REPORT.md, "Use It").
- **What the tests cannot see.** Headless, nothing is drawn: the tests prove node state, not the look. The state tests press keys through `Input.action_press`, not a keyboard. Effect B being hidden has no path in play, so only its state test covers it (D9, D10); defeat and the teleport circle are covered only by the driver's `mode` check.
- **Effect B rises higher than the first brief planned.** Its band reaches about 58 px above the walk line at its far end, above Revision 1's limit of about 40 px. I chose that after round r2, where the dust stayed inside the grass (CHANGE-BRIEF.md, Revision 4).
- **Effect A's preview frames more than the brief asked.** At zoom 1 it shows x 1240–3160, not x 1950–2450, so the frozen goblins and the sword pickup are in the picture.
- **Tested on one machine by one person.** Everything ran on macOS 15.1 on an Apple M3, and nobody else has played the game.

## Files

| Path | What |
|---|---|
| `game/` | The 2D game: the effects and their driver in `effects/`, the previews in `previews/`, the generated process shader in `shaders/`, the F9 key in `app/`, and the tests and cost script in `tests/` |
| `scripts/run-test.sh` | The course's Assignment 6 test wrapper, changed in four places for this folder (listed at its top) |
| `CHANGE-BRIEF.md`, `CLAUDE.md`, `TUNING.md`, `TEST-REPORT.md`, `FRICTIONAL.md`, `SOURCES.md` | The specification, the agent's context, the tuning rounds, the results, the honest log, and the credits with who did what |
| `captures/` | The frame strips, every revision's, and the frames kept from the two mutated previews; all fixture captures |
| `sessions/` | Prompts, plans and transcripts of the scoped `claude -p` sessions |
| `logs/` | Every log the records cite |
| `evidence/` | The Compatibility probe (`compat-probe/`), the headless probes (`headless-probe/`), the F9 check (`vsync-check/`) and the Use It measurements and captures (`use-it-code/`; full-size screenshots are not in git) |
| `youtube/claude-liam-walker-rudy-particles/` | The film's beat sheet, prompts, fact check, capture driver and log, ledger, stills and build tools (the MP4 is not in git) |
