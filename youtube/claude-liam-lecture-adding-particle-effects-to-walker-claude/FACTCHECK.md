# FACTCHECK.md — Adding Particle Effects to Walker Claude

All claims verified against Chapter 9 text and cited sources.

| Claim | Source | Status |
|---|---|---|
| GPUParticles2D parented under Player is hidden when player calls hide() | Ch. 9 "Triggering: a particle node is a node"; agent Session 1 explanation | ✅ |
| Correct parent for DeathBurst is Main, not Player | Ch. 9 Session 1 record; walker-2d-dodge-the-creeps main.tscn | ✅ |
| Two lines in game_over(): global_position = player.global_position; restart() | Ch. 9 Session 1 record | ✅ |
| Session 1: agent predicted 3 failures; 2 of 3 were wrong | Ch. 9 Session 1 record (real run showed 1 failure, not 3) | ✅ |
| Session 2: agent explained lambda bug as "dummy renderer never advances timers" — also wrong | Ch. 9 Session 2 record | ✅ |
| GDScript lambda cannot reassign outer local variable | Ch. 9 Session 3; GDScript basics — lambda functions doc | ✅ |
| Probe confirmed: one-shot GPUParticles2D with lifetime 0.5 emits `finished` in headless at ~0.5s | Ch. 9 "Session 3: correcting with evidence"; probe logs | ✅ |
| null texture draws 1×1-pixel squares (GPUParticles2D class ref) | Ch. 9 Session 3; GPUParticles2D class reference | ✅ |
| particle_flag_disable_z defaults to false; official 2d/particles demo README says enable it | Ch. 9 Session 3; 2D particle systems docs; demo README at commit a3b5c113 | ✅ |
| Fix: Dictionary reference type allows lambda mutation; switch from bool to Dict | Ch. 9 Session 3 change summary | ✅ |
| 9 checks in final test_particles.gd; final run: 9/9 PASS | Ch. 9 Session 3; verify section | ✅ |
| Headless Godot sleeps ~6.9 ms per frame (low_processor_mode_sleep_usec = 6900) | Ch. 9 cost measurement; Godot source core/os/os.cpp | ✅ |
| Cost script without --fixed-fps: every case ≈ 6.9 ms — not particle cost | Ch. 9 "The cost measurement"; Codex output in chapter | ✅ |
| --fixed-fps bypasses sleep: fixed-fps 60 returns before add_frame_delay | Ch. 9; Godot source main/main.cpp | ✅ |
| Fixed-fps results: CPUParticles2D 0.035 ms at 1k, 0.33 ms at 10k, 1.61 ms at 50k | Ch. 9 cost table | ✅ |
| CPU particle cost ≈ 0.032 µs per particle per frame | Ch. 9 (derived from table: 1.61 ms / 50000 = 0.032 µs) | ✅ |
| GPUParticles2D fixed-fps rows ≈ 0.002 ms — dummy renderer doing nothing | Ch. 9 cost table | ✅ |
| Godot one_shot → Unity Looping off; finished → OnParticleSystemStopped | Ch. 9 Unity comparison table; Unity docs 2026-09-27 | ✅ |
| Godot one_shot → Unreal Emitter State Loop Behavior Once; finished → OnSystemFinished | Ch. 9 Unreal comparison table; Unreal docs 2026-09-27 | ✅ |

**No unchecked claims in the film.**
