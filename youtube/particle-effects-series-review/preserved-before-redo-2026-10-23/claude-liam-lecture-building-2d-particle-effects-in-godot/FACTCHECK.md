# FACTCHECK.md — Building 2D Particle Effects in Godot

All factual claims verified against Chapter 9 text (source of truth) and the cited primary sources below.

| Claim | Source | Status |
|---|---|---|
| walker-2d-dodge-the-creeps is 480×720, Compatibility renderer | Ch. 9 "The Walker example" | ✅ |
| Trail: amount=10, speed_scale=2, zero gravity, colour ramp, z_index=-1, emitting=true | Ch. 9 "Its one particle node" | ✅ |
| DeathBurst parent = Main (not Player): hide() propagates to all children | Ch. 9 Session 1 | ✅ |
| DeathBurst config: emitting=false, one_shot=true, explosiveness=1.0, amount=32, lifetime=0.6 | Ch. 9 table "The change" | ✅ |
| ParticleProcessMaterial: spread=180, velocity 150–300, gravity 0, scale curve 1→0, colour ramp opaque→transparent | Ch. 9 table | ✅ |
| game_over(): two lines — global_position and restart() | Ch. 9 Session 1 code block | ✅ |
| Allow list `Bash(godot:*)` blocks absolute path `/Applications/Godot.app/…` | Ch. 9 Session 1 | ✅ |
| Session 1 ran 40 turns; predicted output table had two wrong predictions | Ch. 9 Session 1 | ✅ |
| test_particles.gd Session 2 result: 6/7 pass | Ch. 9 Session 2 | ✅ |
| GDScript lambda captures local by value; lambda cannot reassign outer local | Ch. 9 Session 3; [GDScript basics lambda] | ✅ |
| Fix: Dictionary (reference type) used so lambda can mutate the flag | Ch. 9 Session 3 | ✅ |
| null texture → 1×1 pixel squares (class reference) | Ch. 9 Session 3; [GPUParticles2D class ref] | ✅ |
| Fix texture: 16×16 GradientTexture2D, radial, white→transparent | Ch. 9 Session 3 | ✅ |
| particle_flag_disable_z defaults false; official 2d/particles README says enable it | Ch. 9 "process material is 3D"; [2d/particles README at a3b5c113] | ✅ |
| 9 checks pass after Session 3 | Ch. 9 Session 3 output block | ✅ |
| Headless frame loop sleeps to 6,900 µs (6.9 ms) when cannot draw: `low_processor_mode_sleep_usec` | Ch. 9 "The cost measurement"; [core/os/os.cpp 4.7.2-stable] | ✅ |
| `--fixed-fps 60` skips that sleep; measurement becomes meaningful | Ch. 9 "The cost measurement" | ✅ |
| CPUParticles2D at 1k/10k/50k with --fixed-fps 60: 0.035 / 0.33 / 1.61 ms/frame | Ch. 9 cost table | ✅ |
| GPUParticles2D cost headless ≈ 0.002–0.003 ms (dummy renderer — not real cost) | Ch. 9 cost table | ✅ |
| Session ran on Apple M4 Pro, Godot 4.7.2, Claude Code 2.1.150, 27 Sep 2026 | Ch. 9 "What we actually ran" | ✅ |

**No unchecked claims in the film.**
