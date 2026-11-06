# FRICTIONAL — Assignment 6

What I tried, what happened, what I checked and changed, and who did what. Organized by claude.ai (chat) from my session of 2026-11-05 to 2026-11-06; every entry is something that happened, checked by me. "Agent" means Claude Code (desktop app, Opus 5.5, manual permissions). Tuning details are in `TUNING.md`; entries point there rather than repeat it.

## Entries

**1. Setup ran as one script, but `git fetch` hung.** To commit the brief before any prompt, setup (branch, copy from A5 `2b68e0a` with a tree-ID check, `run-test.sh`, baseline) ran as a script I executed. Its first run hung on `git fetch` (my network); I stopped it, checked nothing had changed, and reran it with a 90 s timeout on the fetch. Baseline: 9 suites, all 0 failures (`1cebbd8`).

**2. I let the agent make the commits.** The assignment keeps the agent's git read-only so a reviewer can see who wrote what. To save time I let it commit, under a rule in CLAUDE.md: only commits I ask for, each message naming the author ("agent, unedited", "agent, approved by me", "mine, committed by Claude Code at my request"), no push, nothing under `shaders/`. My first brief commit (`d81ce93`) I made myself, before any prompt.

**3. My first short answers were generic.** claude.ai corrected four of my six answers against my own brief: the feature CPU particles lack is turbulence, the burst count is 6 × 32, `preprocess` would be wrong for a trail, and the colour ramp belongs to process, not draw (noted in `CHANGE-BRIEF.md`).

**4. The CLAUDE.md draft found a test conflict.** My brief put the A2 flash inside the new impact; the agent found that `test_cast.gd:55–56` counts `Burst` children of `Main`, which would have failed an earlier suite. I revised the brief to keep the flash outside (`e392507`).

**5. The ClassDB check found three things I had wrong or missing.** The camera follows the player (my brief said fixed); `particle_flag_disable_z` must be set or a 180° spread becomes a 3D cone; and Godot 3 names such as `initial_velocity` still exist in 4.7.2 as Vector2 pairs. Brief revision `46df992`.

**6. The Godot 3 name mutation failed silently in the engine.** Renaming `initial_velocity_min = 90.0` to `initial_velocity = 90.0` gave no error or warning; the effect still fired, with a speed range of 0–160. Only the configuration test's read-back caught it (`ab0784c`).

**7. Pruning the strips.** My first prune loop stopped halfway on one folder; a single `find -delete` worked. I learned that Movie Maker also writes a `frame.wav`, which I delete.

**8. "Stamped" repeats were the preview's fault.** I saw the two impacts in the retrigger strip as the same. The agent measured it (0.83 scale fit, 1.6 px vs 4.1 px for a rotated control) and traced it to the preview's seed + 1. Fixing the seeds changed no effect value, and afterwards I saw them differ (TUNING r0b, `0069149`, `9ef647d`).

**9. I overruled one strip reading.** Claude read frame 20 as too dark too soon; in slow motion I judged it right and changed nothing (TUNING r0b).

**10. Effect A r1 taught a timing offset.** I wanted the impact brighter or longer. The agent found the smoke drawn over the sparks at full opacity from frame 0 and proposed a fade-in; frame 10 roughly doubled its bright pixels, but frame 12 missed the prediction. Its explanation, backed by spark distances: frame n of a strip shows about (n − 9)/30 s, not (n − 10)/30 s. Kept after play (TUNING r1, `35a1f70`).

**11. My first look at Effect B ran at the wrong rate.** I watched the trail preview windowed without `--fixed-fps`; it stops its carrier by frame count, so the fireball flew only about 0.28 s at my display's rate. My observations stood, but I noted it (TUNING).

**12. "World space" in my brief was wrong.** A windowed probe on the RTX 5060 showed the trail's direction follows the fireball's rotation and gravity stays in world space: the look I wanted, described wrongly (revision 2026-11-06, `e174c96`).

**13. Effect B r1 closed the gaps only partly.** I wanted a thicker trail; the scale curve went 1 → 0 to 2 → 0. The head now joins up, but 1–3 px gaps remain further back, because each dot shrinks with age. The 8.7 px dot spacing equals one 1/30 s step at 260 px/s; the agent guessed `GPUParticles2D`'s default fixed 30 fps, not confirmed (TUNING, `cc1f2f2`).

**14. The cost script nearly measured itself.** The agent's first draft timed its own bookkeeping (+41 / +81 µs); it then timed only the frame and added dry cases, giving A +8.2 µs and B +25.1 µs. It also found `Performance.TIME_PROCESS` reporting identical values for different cases headless (`f7787c4`).

**15. GPU price in the editor.** Case 1 has no "Update GPUParticles" row at all; A adds about 0.02 ms and B about 0.10 ms of GPU time, within budgets of 0.5 and 0.3 ms. With vsync off, FPS rose to about 1000 in all three cases, under 1% apart, so FPS would have hidden both costs.

**16. Step 6 mistakes in the editor.** I first typed 90 into Inherit Velocity instead of Initial Velocity, and my first Save As saved the whole ShaderMaterial (`.tres`) instead of the shader; both fixed before saving `particles_generated.gdshader`.

## Human and AI contributions

- **Mine:** choosing both effects and their look (layers, size, feel), every prediction and every verdict, approving every tuning change, all play testing and human checks, the strip captures, the GPU readings, the generated-shader conversion and my answer on process versus draw.
- **Claude Code:** CLAUDE.md drafts, both effect scenes, the texture-writing script, configuration and state tests, previews, mutations, the trail direction probe, the cost script and the GPU price scene, strip readings, predictions and comparisons. Accepted after review; changed or rejected by me: the flash kept outside the impact, preview seeds fixed before any effect change, its frame-20 reading overruled, approval step by step.
- **claude.ai (chat):** planning, commands, the setup script, proposing setting values from my choices, compiling CHANGE-BRIEF, TUNING, TEST-REPORT and this file from what happened, correcting four of my short answers, and translating my Chinese.

## Still open

- Why the trail beads at an 8.7 px spacing (the 30 fps simulation guess), why vsync-off FPS stops near 1000, and whether the GPU keeps simulating a hidden emitter.
- The `_spent` guard is not exercised by any test.
