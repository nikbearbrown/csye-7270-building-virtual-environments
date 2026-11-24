# PROJECT-BRIEF — Rhodes Daily (working title; repo name Downfall)

Godot 4.7.2 · GDScript · Forward+ on D3D12 · Windows desktop export · built with Claude Code.
Target role: **gameplay programmer / technical designer**. Reader: **hiring manager or lead**.

## 1. What is it?

A single-player PC extraction ARPG: you take operators down a stack of one-way floors, and on every floor you decide whether to push deeper or extract; what you bring out feeds a Rhodes Island base you run, trade from and upgrade.

When it is done, it will be a **Windows desktop build** plus a **headless test suite a stranger can rerun** from a fresh clone, with its test report.

## 2. Why would anyone care?

Every floor is a fresh push-or-extract decision, and the base gives the loot a long-term use: an economy of factions, an exchange, research and a ship voyage, all running on scaled real time.

## 3. What does it give the player?

A run where the tension rises floor by floor (danger grows with depth and the backpack is lost on death), followed by a base where those decisions pay off over days, not minutes.

## 4. How is it different?

- **Escape from Duckov** — a raid there is one map. In Rhodes Daily a run is a one-way stack of floors, so the extract-or-continue choice comes back every floor, not once per raid.
- **Greedy Cave (贪婪洞窟)** — gave me the one-way descent. Rhodes Daily adds real-time combat won by positioning and timing (every enemy attack has a four-frame telegraph) and a base economy where extracted goods are traded across nine factions.

Whether this is more fun is not something I can claim yet; that will be decided by playtests.

## 5. Who opens it, and what do they do in the first sixty seconds?

A hiring manager double-clicks the exe: title → new save → a PRTS tutorial card → the base → the first field run. A new save currently walks a short base storyline before the first run; **whether that fits in sixty seconds has not been measured yet — I will measure it and report the time.**

## 6. What does it prove about me?

| Skill | Evidence (exists) |
|---|---|
| Shaders and materials | A5 Molotov fire shader: predicted pixel values matched measured ones; fire checks pass at 30/60/144 fps (tag `a5`) |
| Particle effects | A6 GPU particles: hits, rain with puddle reflection, snow with trails (tag `a6`) |
| Animation and state | A7 NPC idle sprite-sheet loop and Lappland's sword-wave cutout rig, driven by the player state machine (tag `a7`) |
| Profiling | 2026-10-24: switching Windows from Vulkan to D3D12 moved rendering from the AMD 610M iGPU to the RTX 4060 Laptop; mine region ~9 → ~150 fps at 2560×1600, no vsync. Measured once; the log was not committed — **will re-measure and commit the log** |
| Verification habits | Headless suite run with `tests/run_all.ps1`; fixed-seed RNG streams; `test_flow` simulates a new save through the main storyline; human checks for what tests cannot see; Claude Code directed through written briefs and scoped tools |

## 7. In, out, first

- **In (still to do):** music (region and combat tracks); cross-system optimisation and balance (economy, exchange, research, contracts, time scale); bug testing and regression fixes.
- **Out:** multiplayer.
- **First:** the core loop already runs; the film opens on real captured play from commit `1fbc309a`.

## 8. What could sink it?

The game is large and its systems interlock: change one number and another system drifts. `test_flow` already shows LMD as a bottleneck everywhere and a first voyage costing about 1.08 million (a simulation, not playtest data). It needs more time to verify and balance. What I will do: run the economy probe and `test_flow` after every change, keep a balance log with fixed seeds, and use human playtests for the feel that tests cannot measure.

## 9. Why this project?

A mix. **Already had:** systems and numbers design — the design documents, the economy probe and the `test_flow` simulation in the repo. **New to me in this course:** shaders (`a5`), GPU particles (`a6`), Blender modelling (`a3`), animation rigs (`a7`), and Godot itself.

---

## Exists today

| Thing | Where to see it |
|---|---|
| Playable core loop: base → field run → extraction → settlement | dev repo `1fbc309a` |
| A2 game slice | `7b1a10c` (A2 submission) |
| Blender assets | course tag `a3` = `ec51731a` |
| Shaders + fire | course tag `a5` = `4327a7f5` |
| GPU particles | course tag `a6` = `f92a3cf3` |
| Animation (idle loop, sword-wave rig, strike frames) | course tag `a7` = `171a5830`; dev `456ba631` |
| Overpasses in four regions | dev `22651e36` |
| Contract board | dev `3d4caaeb` |
| Base time scaling | dev `3bac73db` |
| Exchange unified price lines | dev `4678647b` |

## Will exist

- Music for regions and combat, credited in SOURCES.md
- Balanced cross-system economy, with a balance log
- Bug-test pass with a rerunnable test report from a fresh clone
- A measured first-sixty-seconds time and a committed profiling log
