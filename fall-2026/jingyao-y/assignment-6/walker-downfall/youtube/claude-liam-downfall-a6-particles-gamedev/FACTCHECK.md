# Fact check

Every number spoken or shown was checked against the files below at commit `6f980233fe3c31f11b4957b50b30e020bae61fda` (working-tree hashes in gamedev-evidence.json).

- Event sites: `_hit_spark(target)` is called at entities/player.gd 915 (basic hit), 977 (Lappland cross) and 1784 (Amiya cut); the function is lines 948–954 and adds the burst to `game`.
- Feedback mapping: entities/fire_pit.gd 104–110, `ratio = LOW_RATIO + (1 - LOW_RATIO) * clamp(burn_left / FULL_FIRE)` with LOW_RATIO 0.3, FULL_FIRE 120; `amount` is not written.
- Intent blocks: CHANGE-BRIEF.md 52–62 (A) and 205–212 (B), shown verbatim.
- Sparks: amount 14, lifetime 0.35, randomness 0.4, one_shot, explosiveness 1.0, local_coords false (effects/hit_spark.tscn 177–191); sphere r 0.1, spread 180, velocity 3–6, gravity −9.8, damping 6–10, hue ±0.03 (79–95).
- Puff draw: blend_mode 0 (MIX), unshaded, billboard 3 (particles), vertex colour as albedo (145–152); QuadMesh_puff 1.0 × 1.0 since r1 (154–156; brief r4). Before r1 it was 0.5.
- Effect A r1 (TUNING.md): proposal and prediction committed in cc9ebfaf before any edit; first declined ("Don't change."), later approved; edit bac2d460; strips ca1b6142. Predicted the snow patch 630–650 × 378–386 ≤ 150 on frames 15/20; measured 158.3 on every frame in r0-snow and r1-snow (miss). Changes confined to 621–661 × 340–376. City patch ≤ 3 levels (held). User verdict: "Keep."
- Strip r0: bursts at frames 10 and 16, seeds 7370/7371, the log reports 0 HitSpark nodes at frame 50; Claude's still reading and the user's "I can see it splashing outward" are quoted from TUNING.md (translated).
- r0-snow: 158.3 luminance on every frame (TUNING.md, Claude's measurement); the user's "I can see it" / "Barely see a little."
- Effect B r0/r0b/r1: occlusion diagnosis withdrawn after the user's screenshot; fixture fixed with seed_rng + pit 1; Flames quad 0.30 → 0.55, warm px r0b 72/58/76/36 → r1 170/164/162/108 (frames 12/40/54/70); top rose 2–3 px, predicted ≥ 5 (miss); verdict "Keep."
- Shader: shaders/particles_generated.gdshader line 140 (initial velocity from min/max), 161–162 (scale curve, colour ramp), 236 (AMOUNT_RATIO skip). Attempt 1 (evidence/a6/step6/) lacks the sphere radius, ramp and curve; the on-screen diff is the actual `diff` output.
- Tests: config 165/0 (A) and 123/0 (B); M1 exit 1 with "got 0.0, 6.0"; M1b exit 0; M2 exit 1 "got 4.0, 4.0"; A state 0 failures (22 PASS); B state 0 failures, monitor 11846 samples, 352 ratios, 0 violations; suites 78/89 before, 82/93 after (logs/baseline-*/summary.txt). These logs predate r1 except the config result, which the main session re-ran after r1 (165/0, TUNING.md).
- Prices: cost_effects SUMMARY (empty 0.0032 ms, game_off 7.6759 ms, A_8 +0.0248 ± 0.0287, B_1 −0.0132, B_all +0.0621; all within 2 SE). GPU: Update GPU Particles 0.14 ms (A) and 0.09 ms (B) from the user's screenshots, budgets 0.25 / 0.15 ms, predictions 0.05 / 0.06. Both prices predate Effect A r1 (TEST-REPORT order note).
- New captures (B03, B05, B11, B19): see SOURCES.md; event frames come from their capture logs.
- Not claimed: human play footage, fun, legibility for players in general, the draw-step GPU cost, the boss-arena fire on screen.
