# FACTCHECK — Sparks and Dust for Walker Rudy.

Every number and factual claim spoken or shown in the film, with its source. Paths are relative to `fall-2026/shuai-z/assignment-6/`. Claude Code checked each against the file on 2026-11-07, at source revision `d0ed4152`.

| Beat | Claim | Source |
| --- | --- | --- |
| B00 | walker-rudy started in Assignment 2; Godot 4.7.2; GL Compatibility; one 2D game | `CHANGE-BRIEF.md` §1 (Rudy's art from `../assignment-2/evidence/`); `logs/checks_60fps.log:1`; `game/project.godot:16`, `:95-96`; `FRICTIONAL.md`, first entry (this assignment changes only the 2D game) |
| B00 | effects and tests by scoped `claude -p` sessions; verdicts and approvals by shuai-z; Use It records by Codex | `FRICTIONAL.md` entries for Steps 1–7 and Use It; `TEST-REPORT.md`, Use It |
| B01 | Claude read every strip and predicted every round; shuai-z's verdict decided each | `TUNING.md`, "How this file is written" and each round's verdict |
| B02 | hitbox live 0.15 s of a 0.3 s swing, 50 px in front | `game/content/rudy/rudy.gd:66-69` (`slash_time` 0.3, live 0.03–0.18, `slash_reach` 50) |
| B02 | event: the hitbox going live; condition: in control, on the floor, moving | `game/effects/effects_driver.gd:35-37`, `:55-56` |
| B03 | line 108 `amount = 28`; line 79 gravity; shader line 311 `force = gravity;`; draw: a gradient streak with a dark rim | `game/effects/slash_sparks.tscn:108`, `:79`, `:109`, `:3-5`, `:15-21`; `game/shaders/particles_generated.gdshader:311` |
| B03 | a headless run uses a dummy renderer: no process shader, nothing drawn; the CPU pays only node bookkeeping | `CLAUDE.md`, Headless facts; `logs/probe_particles_headless.log:29-37`; `logs/cost_effects_60fps_rerun.log` (its header line) |
| B04 | strike on frame 0 at full size; spray out and a little up, white to yellow; fall-off, orange, last gone by 0.45 s; a dark rim in the art's line colour | `CHANGE-BRIEF.md` §2, The intent (read verbatim by `tools/make_stills.py`) |
| B04 | Claude drafted the brief; shuai-z chose the effect and reviewed it | `CHANGE-BRIEF.md`, "How this brief was made" |
| B05 | align Y; disable Z; 19° above forward; ±30° spread; 260–420 px/s; gravity 700; no damping; lifetime randomness 0.4 | `game/effects/slash_sparks.tscn:73-82`; `CHANGE-BRIEF.md` §2 settings table (19°) |
| B05 | built by the scoped session, `ea4419ae` | `git log`: "Add Effect A, its configuration test and its preview (agent, unedited)" |
| B06 | r0 is a fixture with 14 sparks; frame 10 flash; 12 and 15 spray, orange; frame 20 only 2 specks of the first burst | `TUNING.md`, Effect A r1, "Claude's reading of r0"; `captures/slash_sparks/r0/` |
| B06 | shuai-z watched first, before Claude read a frame: too sparse, too few | `TUNING.md`, Effect A r1, "What I saw" (三次, "感觉火花可以再多一些，现在太稀疏，太少了") |
| B06 | the spray reads as a crowd for only five frames | `TUNING.md`: "only in frames 11 to 15" |
| B07 | `emitting = false`; amount 28 (was 14); texture; lifetime 0.45; one shot; explosiveness 1.0; local coords off | `game/effects/slash_sparks.tscn:107-115`; `CHANGE-BRIEF.md` Revision 3 |
| B07 | peak 29 a burst, 58 for two; changed in `fed848b8` | `CHANGE-BRIEF.md` Revision 3; `git log` |
| B08 | predicted 16–20, about 14–18 seen; about 20 with gaps halved; predicted 3–5 specks, about 8 and higher; prediction doubled r0's two specks | `TUNING.md`, Effect A r1, "Claude's comparison" and the paragraph after it |
| B08 | three plays at real speed; kept | `TUNING.md`, Effect A r1, "My verdict" |
| B09 | reads `disabled` each physics tick; the true → false edge fires; a new burst per cut; on the hitbox; `scale.x = facing`; after Rudy in Main | `game/effects/effects_driver.gd:35-46`, `:11`; `game/app/main.tscn:21-26` |
| B09 | written by the scoped session, `ebe2d9d5` | `git log`: "Wire Effect A into Main and add its state test (agent, unedited)" |
| B10 | one cut; five as fast as the game allows; two bursts alive for a few frames; facing left the sparks fly left | `capture/play-01-run.log` (bursts 2 on frames 250–253, 260–263, 270–273, 280–283; facing −1 from 308) |
| B11 | a cut at the top of a jump; the goblin vanishes first and its sparks outlive it; paused sparks hold still and carry on | `capture/play-01-run.log` (burst at 469; goblin hidden from 573, burst to 574; paused 595–630); `CAPTURE.md` §1 (pixel-identical paused frames) |
| B11 | the bursts belong to an effects container, not the goblin | `game/app/main.tscn:23-26`; `TEST-REPORT.md` S10, S11 |
| B12 | fade-in; damping brings each puff to a stop; dissipate toward the ground's colour; a puff within two frames; empty within 0.5 s; 2.9 : 1 against the wheat | `CHANGE-BRIEF.md` §3, The intent |
| B13 | watched six times; could not see it; rendered with the dust hidden and compared; 136 pixels at frame 25; contrast assumed opaque dust over the wheat; born in the grass strip at 0.75 opacity with soft edges | `TUNING.md`, Effect B r1, "What I saw" and "Claude's reading of r0"; `FRICTIONAL.md`, Step 5 (six times) |
| B14 | the ramp darker and fully opaque; at least 500 pixels, met with 612; at least 90 levels, missed at 87; verdict quoted | `TUNING.md`, Effect B r1 |
| B15 | 20 → 40 puffs; Claude read a continuous band with both targets met; shuai-z's verdict quoted; measured afterwards at most 34 px above the walk line, inside the grass strip | `TUNING.md`, Effect B r2, and r3 "Claude's reading of r2, measured" (21, 33, 34, 32 px; strip about 40 px); `TEST-REPORT.md`, Use It, "Claude against me" |
| B16 | speed doubled, damping unchanged; predicted 50–62 px, measured 58; frames 13 and 46 lower; three plays; kept | `TUNING.md`, Effect B r3 |
| B17 | box 28 × 6 px; straight up; ±50°; 80–160 px/s (r3); no gravity; damping 120–180 px/s², the feature A lacks | `game/effects/run_dust.tscn:31-41`; `CHANGE-BRIEF.md` §3, Revision 4 |
| B18 | Enter, the run, the jumps, the sword | `capture/play-01-run.log` (Enter at 30, dust from 61, sword at 178, stop at 190) |
| B19 | `emitting = false`; amount 40 (r2); a steady stream with jittered birth times; lifetime 0.5 s; `trail_enabled` false because Compatibility does not draw it (a probe); local coords off makes the trail | `game/effects/run_dust.tscn:52-63`; `evidence/compat-probe/README.md`; `CHANGE-BRIEF.md` §1, §3 |
| B20 | no new puff in the air; the laid ones stay in the world; on again at the landing | `capture/play-01-run.log` (off 97–117, on at 118; off 136–156, on at 157) |
| B21 | kept at his soles every tick even when idle; in play, on the floor, faster than 1 px/s; visible; emitting changed only on change; paused, the driver does not run | `game/effects/effects_driver.gd:52-59`, `:16-17` |
| B21 | written by the scoped session, `d0abc9dd` | `git log`: "Wire Effect B into Main and add its state test (agent, unedited)" |
| B22 | Esc while running: puffs frozen and drawn, none born; resume; stop; trail empties; jump with a cut, no dust in the air | `capture/play-01-run.log` (paused 376–411; stop 422; airborne 457–476 with dust false); `CAPTURE.md` §1 |
| B23 | shuai-z converted a copy of Sparks' material and read it; line 139 picks the speed between two uniforms (260 / 420); line 311 starts the force from gravity, a later line adds it each step (700, down); the numbers arrive as uniforms | `game/shaders/particles_generated.gdshader:10-11`, `:43`, `:139`, `:311`, `:324`; `TEST-REPORT.md`, "The process shader"; `FRICTIONAL.md`, Step 6 |
| B24 | the real Main; the real slash action; wait for the swing to end; a second cut; 45 ticks; two bursts alive; the first the same node, not moved, still emitting; never calls the driver | `game/tests/test_slash_sparks_state.gd:181-205`; `TEST-REPORT.md`, Step 3 |
| B25 | 108 and 61 configuration checks; 14 and 14 state checks; 19 ticks apart; 27 ticks; 380 ticks; 141 and 15 unchanged | `logs/test_slash_sparks_config_60fps.log`, `test_run_dust_config_60fps.log`, `test_slash_sparks_state_60fps.log` (S7, S8), `test_run_dust_state_60fps.log` (D11), `checks_60fps.log`, `invulnerable_tint_checks_*fps.log` |
| B26 | eight mutations, each exit 1; six failures for the reused burst | `logs/mutation_*_60fps.log`; `TEST-REPORT.md`, Steps 2, 3 and 5 |
| B27 | empty scene 0.004 ms (0.0038); game without effects about 0.05; each effect under 0.01 more, inside the round spread | `logs/cost_effects_60fps_rerun.log` (+0.0063, +0.0019); `logs/cost_effects_60fps.log` (+0.0079, +0.0039); `TEST-REPORT.md`, Step 7 |
| B27 | budget 0.25 ms of GPU time per effect; GPU column 0.0 in every row; failure 12; FPS with vsync off 239–438; FPS is not GPU time | `CHANGE-BRIEF.md` §7 (12), §8; `TEST-REPORT.md`, Use It, "The GPU price"; `evidence/use-it-code/summary.json` |
| B28 | the mutated burst still sprays; headless draws nothing; Codex's captures; shuai-z found size and feel fine | `TEST-REPORT.md`, Step 2 "Mutation 1 in a window", Use It ("亲自玩过，大小和手感都没问题"); `evidence/use-it-code/README.md` |
| BVD1 | config 108/61, state 14/14, 141 and 15, eight mutations; every round judged; the r2 overrule; the invisible dust; B found missing in the game; B's scene mutations missed then run; Claude's shell in `captures/` broke shuai-z's command | `TEST-REPORT.md`; `TUNING.md`; `FRICTIONAL.md`, Step 2 ("Invalid project path specified"), Step 5 ("Why I asked", "A step that had been missed") |
| BVD1 | Claude's 3–5 specks for sparks r1 (about 8); vsync about 120 FPS on a display reporting 60 Hz, unexplained | `TUNING.md`, Effect A r1; `FRICTIONAL.md`, "The F9 vsync key" |
| BVD2 | who made what | `FRICTIONAL.md`, the Human / AI lines of every entry; `TEST-REPORT.md`, Use It |
| BVD2 | no texture files: every texture is a `GradientTexture2D` inside the scene files | `game/effects/slash_sparks.tscn:7-21`; `game/effects/run_dust.tscn:7-13`; `CHANGE-BRIEF.md` §2 ("The textures are defined inside the scene file") |
| BVD2 | source shown `d0ed415`; game source unchanged since `d60fb03` | `git log -1 -- fall-2026/shuai-z/assignment-6/game` |
| BHTF | damping 120 / 180 → 60 / 90; TUNING.md's r3 model | `game/effects/run_dust.tscn:40-41`; `TUNING.md`, Effect B r3 ("a simple model of those settings") |

## Corrections made while building

- A first draft of B15 said the trail "topped out at thirty-three pixels"; `TUNING.md` gives 33 px at frame 25 and 34 px at frame 40, so the line became "at most thirty-four".
- A first draft of the r3 strip card put "检查过了，没问题" beside the r3 verdict. Those words were said after Step 5 wired the effect in, not as the verdict on r3, which had no further reason; the card now says so.
- A first draft of B12 called the brief's 2.9 : 1 "wrong"; the brief's own revision says it assumed opaque dust over the wheat, so the line now says the prediction did not survive the first strip.
