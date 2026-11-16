# ACTS.md — Building 2D Particle Effects in Godot

**Film 2 of 5 — CSYE 7270: Building Virtual Environments**  
**Source:** Chapter 9 — Particle Effects (2D hands-on section)  
**Slug:** `claude-liam-lecture-building-2d-particle-effects-in-godot`  
**Channel:** @NikBearBrown · Liam in for Bear · Kokoro `am_onyx`

---

## Coverage map (chapter → act)

| Chapter section | Act |
|---|---|
| The Walker example (walker-2d-dodge-the-creeps) | Act 1 |
| Build It — Step 1 (the burst); Session 1 (agent mistakes) | Act 2 |
| Session 2 (running tests); Session 3 (lambda, pixel, disable-Z) | Act 3 |
| Step 2 (cost); the sleep trap; --fixed-fps fix | Act 4 |
| What is still unverified | Recap |

---

## Fixed spine

| Beat ID | Type | Content |
|---|---|---|
| BOPEN | Manim | Title card: "Building 2D Particle Effects in Godot" |
| BIDEA | Remotion BrutalistHesitantWriter | "A headless test says it's emitting. Is there a burst?" |
| BDEFS | Remotion ClaudeDefinitions | 5 terms: one_shot · explosiveness · process_material · particle_flag_disable_z · finished |
| BACT1 | Remotion FormACard | "Act 1 — The Game and the Node" |
| BACT2 | Remotion FormACard | "Act 2 — Three Sessions" |
| BACT3 | Remotion FormACard | "Act 3 — Fixing What the Tests Missed" |
| BACT4 | Remotion FormACard | "Act 4 — What Does It Cost?" |
| BVDT | Remotion ClaudeVerdictArtifact | Recap: what 9 checks prove and don't prove |
| BHTF | Remotion ClaudeComposerAsk | Your Turn prompt |
| BOUT | Remotion ClaudeTitleOutro | @NikBearBrown outro |

---

## Act 1 — The Game and the Node

**Story:** walker-2d-dodge-the-creeps is a 480×720 portrait game on the Compatibility renderer. It already has one particle node: the Trail, a GPUParticles2D that ghosts faded copies of the player. The chapter adds a second — a death burst. We see the game tree, the Trail's config, and why a burst parented to Player would vanish with it.

| Beat | Manim class | What it shows |
|---|---|---|
| B01 | B01_GameTree | Scene tree: Main → Player (Trail inside), MobTimer, HUD — highlights that Trail is child of Player |
| B02 | B02_TrailConfig | Trail properties: amount=10, speed_scale=2, zero gravity, colour ramp, z_index=-1, emitting=true always |
| B03 | B03_ParentTrap | Diagram: player.hide() → visibility propagates → child burst invisible; "emitting ≠ visible" |

---

## Act 2 — Three Sessions

**Story:** The chapter gives Claude Code a spec prompt and runs three sessions. Session 1 gets the code right but can't run the tests — its allow list says `godot`, not the absolute app path. It fills in a predicted PASS/FAIL table. Those predictions are mostly wrong.

| Beat | Manim class | What it shows |
|---|---|---|
| B04 | B04_AllowListTrap | Diagram: allow-list rule `Bash(godot:*)` vs absolute path `/Applications/Godot.app/…`; the five refused calls |
| B05 | B05_PredictedVsReal | Two-column table: agent's predicted output vs actual test output (two predicted failures wrong) |
| B06 | B06_DeathBurstNode | GodotDevWorkbench reconstruction — DeathBurst node: main.tscn tree, parent = Main; two lines in game_over() |

---

## Act 3 — Fixing What the Tests Missed

**Story:** Session 2 runs the tests: 6/7 pass. Session 3 gets evidence and corrects three things — the lambda capture bug, the null texture (1×1 pixels), and the missing Disable Z flag.

| Beat | Manim class | What it shows |
|---|---|---|
| B07 | B07_LambdaBug | GDScript: lambda captures by value; flag never changes; fix: Dictionary reference type |
| B08 | B08_NullTexture | null texture → 1×1 pixel squares; 32 invisible pixels on a 480px screen; fix: 16×16 GradientTexture2D |
| B09 | B09_DisableZ | ParticleProcessMaterial is 3D; spread 180° sprays into Z; fix: particle_flag_disable_z = true |
| B10 | B10_NineChecks | Final 9-check table: what each checks, what none of them can see (footage) |

---

## Act 4 — What Does It Cost?

**Story:** Codex writes a benchmark. Every result — GPU or CPU — is 6.9 ms, which is Godot's headless sleep. Rerunning with `--fixed-fps 60` removes the sleep; CPU particles scale linearly (0.035 → 1.61 ms); GPU rows stay near zero (dummy renderer).

| Beat | Manim class | What it shows |
|---|---|---|
| B11 | B11_SleepTrap | Godot frame loop: `OS::add_frame_delay()` sleeps to 6.9ms when headless; everything hidden under the sleep |
| B12 | B12_CostTable | Two tables: without --fixed-fps (all 6.9ms), with --fixed-fps 60 (CPU linear, GPU zero); CPUParticles2D at 50k = 1.61ms |

---

## Recap

| Beat | Content |
|---|---|
| BVDT | 9 tests pass. What's proven: state, collision, visibility, position, finished signal, restart. What's not: looks, reads, feels, GPU cost. "Only a person at a screen can check that." |
| BHTF | "Open walker-2d-dodge-the-creeps. Die. Does the burst read as a death? Start there." |
| BOUT | @NikBearBrown outro, Liam |
