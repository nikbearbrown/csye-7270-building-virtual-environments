# FACTCHECK — every claim in the narration, and where it is backed

Checked 2026-11-23 against the repo at `1fbc309a` and the course tags.

| Beat | Claim | Status | Evidence |
|---|---|---|---|
| B00 | Footage is the game running, captured from the build | exists | `pitch/capture/CAPTURE.md`, `raw-avi-sha256.json`, `mine-inputs.jsonl` |
| B01 | Godot 4.7.2, Forward+ on Direct3D 12 | exists | `start` line of every input log: `forward_plus`, `d3d12`, `4.7.2-stable` |
| B01 | Windows build plus a test suite rerunnable from a fresh clone | **will** | Said as "Done, it will be…" |
| B02 | Four regions and overpasses | exists | `regions.avi`, `bridge.avi`; overpasses at dev commit `22651e36` |
| B03 | Four-frame enemy telegraph; strikes land on authored frames | exists | `敌人攻击动画与预警设计案.md`; strike frames in `456ba631` (A7 methods) |
| B04 | Route map between floors, a camp every ten floors, settlement shows kept / insured / lost | exists | `route.avi`, `camp.avi`; `FieldCatalog.CAMP_INTERVAL` |
| B05 | Walkable ship base, faction exchange, contracts, research | exists | `base.avi`; contract board `3d4caaeb`, unified exchange lines `4678647b` |
| B06 | GPU particles and animation rigs (A6, A7) | exists | tags `a6` f92a3cf3, `a7` 171a5830; raw capture frames from those films |
| B07 | Danger grows with depth; base runs on scaled real time | exists | `D = 3.5×(floor−1) + route` (撤离与营地修订案 §4); time scale `3bac73db` |
| B08 | Escape from Duckov: a raid is one map; Greedy Cave: one-way descent | author's own play | Played by the author. Not compared to any market data |
| B08 | "More fun" | **not claimed** | Playtests will decide |
| B09 | Title → new save → tutorial → base → first run; not timed yet | exists / **will** | `title.avi`; the 60 s measurement is future work |
| B10 | Fire: predicted pixels matched measured at 30/60/144 fps | exists | A5 `TEST-REPORT.md` (pixel table; 89/89 at each rate) |
| B10 | Vulkan → D3D12: mine ~9 → ~150 fps on RTX 4060 Laptop | measured once; log **will** be committed | 2026-10-24 session note. No committed log, so the film says so |
| B10 | Headless suite, fixed seeds, test_flow simulation, human checks, Claude briefs | exists | `tests/run_all.ps1`, `GameManager.seed_rng`, `tests/test_flow.gd`, A5–A7 human-check files, CHANGE-BRIEF files |
| B11 | Music, cross-system optimisation, bug testing | **will** | Scope decision 2026-11-23 |
| B11 | Out: multiplayer | decision | — |
| B12 | test_flow: money a bottleneck; first voyage ≈ 1.08 million | simulation result | `tests/test_flow.gd` run of 2026-11-04. Said as "simulated, not playtested" |
| B13 | Systems design already had; Blender, shaders, particles, animation, Godot new | author's statement | Tags `a3` ec51731a, `a5`, `a6`, `a7`; design docs in the repo |

No invented players, quotes, downloads, wishlists or metrics appear.
