# Fact check

Every number spoken or shown was checked against the files below at commit `299ef97305ac5347081044695b17507457b31af3` (working-tree hashes in gamedev-evidence.json).

- npc_idle (animations/npc_idle.tscn 5–21, 28–40): length 1.33333, loop_mode 1 (LOOP_LINEAR), step 0.0833333, one value track `.:frame`, interp 0, keys at 0 / 0.333333 / 0.666667 / 1 with values 0–3, update 1 (discrete); NpcIdle Sprite3D hframes 4 (vframes default 1), texture npc_closure_idle.png (256×64); AnimationPlayer callback_mode_process 1 (IDLE), autoplay idle.
- track_problems (tests/a7_readback.gd 36–38): the ordinary-track branch `sub in node`; bone and blend-shape branches above it.
- Mutations (logs/a7_mutations/): m1 "FAIL  track_problems is empty  (wave_release track 4: ArmFront has no property rotaton)", RESULT exit=1; m2 FAIL loop_mode (0), exit=1; m3 FAIL key 3 inside the sheet (4), exit=1; m4 both exit=0.
- One authority: world/continuous_world_map.gd 2719–2729 (the seeded draw kept as `phase`, then `clip.seek(...)`); entities/player.gd 362–376 (`_wave_begin` writes Billboard.visible, Rig.scale.x, the sprite's visible). Structure test S7 squad phases [0.3333325, 0.3333325, 0.666665] (logs/test_wave_state_machine_60fps.log) — not all equal, two coincide.
- Two clocks: entities/player.gd 380–388 (`_tick_wave`: advance(delta × rate), wave_frame from _wave_time); D4 lines: r=1 → 12/20/40 unfrozen ticks (16/24/44 with 4 frozen); r=1.5 → 8/14/27 (12/18/31); "every wave tick: clip position == state machine time" PASS at both rates; tolerance 1e-4 s (tests/test_wave_state_machine.gd).
- Phase table (CHANGE-BRIEF.md 155–164): 30 fps, startup 6, active 4, recovery 10; rig keys (animations/lappland_wave_rig.tscn 108–116, ArmBack:rotation) at 0, 0.2, 0.333333, 0.666667, transitions 2 / 1 / 0.5 / 1 (the narration's "transition two eases into the sweep, point five eases out" refers to the first and third), values 0, −0.7, 1.4, 0.
- State table: entities/player.gd 318–331 (WAVE_CLIPS, WAVE_TRANSITIONS 6/10/20).
- r0 strip (the user's capture, captures/wave_release/r0): 27 click, 29 first STARTUP, 36/37 f5/f6 (charge mark gone on 37), 40/41 f9/f10, 49/50 end (TUNING.md). User's words quoted verbatim from TUNING.md.
- Edges (tests/test_wave_edges.gd 198–203; log): 39 passed / 0 failed; f5 no wave, charge 3; f6 wave +1, charge 0; spawn tick position 0.200000.
- Scripted dodges (capture/wave_dodges/capture.log): take 2 dodge at frame 120 in STARTUP → READY at 121, waves 0, charge 3; take 3 dodge at 213 on the first ACTIVE frame → wave out, charge 0; take 4 dodge at 308 in RECOVERY (wave_frame 13) → READY at 309.
- Suites: npc read-back PASS (55), rig read-back PASS (136), pins 11/5 after wiring and 16/0 re-pinned, structure 51/0, edges 39/0; baseline 93 of 103 before, 99 of 108 after (logs/baseline-*/summary.txt).
- Human checks quoted from evidence/a7/human-checks.md and TUNING.md ("All fine", "Reads well", the translated interrupt and contrast reports, "I saw the record. everything is nice, we did a good job.", "Keep r0, no revision").
- Provenance: gpt sol 6.1 (CHANGE-BRIEF r7, animations/ATTRIBUTION.md); terms not supplied.
- Not claimed: human play footage, fun, legibility for players in general, the untested interrupt paths (death, stuns, operator swap, leaving mid-release), edges at r > 1.
