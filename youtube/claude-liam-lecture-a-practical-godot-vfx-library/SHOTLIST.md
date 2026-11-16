# SHOTLIST.md — A Practical Godot VFX Library

All body beats are Manim except B12 (GodotDevWorkbench). Spine beats are Remotion.

| Beat | Render | Visual | Runner-up |
|---|---|---|---|
| BOPEN | Manim | Title card on STAGE background | Remotion ClaudeTitleIntro |
| BIDEA | Remotion BrutalistHesitantWriter | Hesitant-writer beat | Static text card |
| BDEFS | Remotion ClaudeDefinitions | 5 term cards | Manim scrolling list |
| BACT1 | Remotion FormACard | "Act 1 — The Godot Catalog" | Manim divider |
| B01 | Manim | 17 GPUParticles2D nodes listed: 2d/particles catalog, Mobile renderer | Text list |
| B02 | Manim | 3D catalog: Forward+ features — trails / attractors / SDF collision / sub-emitters | Feature grid |
| B03 | Manim | Three-part frame as library organizer: emission / process / draw, what ports where | Column table |
| BACT2 | Remotion FormACard | "Act 2 — Node Conversion" | Manim divider |
| B04 | Manim | CPU→GPU: properties preserved, new ParticleProcessMaterial gained, GPU features unlocked | Before/after |
| B05 | Manim | GPU→CPU: sub_emitter / trail_enabled / shaders crossed out — lossy path | Loss diagram |
| B06 | Manim | Compatibility map: three renderers vs particle features (trail / SDF / emit_particle) | Table |
| BACT3 | Remotion FormACard | "Act 3 — Cross-Engine Map" | Manim divider |
| B07 | Manim | Unity table: Built-in (CPU, YAML) vs VFX Graph (GPU, binary .vfx) vs Godot | Comparison table |
| B08 | Manim | Unreal Niagara table: Sim Target per emitter, .uasset binary, CPU-only events | Comparison table |
| B09 | Manim | .tscn vs binary: Godot text → agent can read/diff; Unity/Unreal binary → agent can't | Two-column |
| BACT4 | Remotion FormACard | "Act 4 — Building Your Library" | Manim divider |
| B10 | Manim | The .tres pattern: one draw material file → three effects share it | Fan diagram |
| B11 | Manim | Library entry card: name / renderer / node type / .tres file / test status | Card template |
| B12 | Remotion GodotDevWorkbench | particle_material.tres: four flags, shared by coin/enemy/bullet effects | Manim property list |
| BVDT | Remotion ClaudeVerdictArtifact | Catalog / conversion / cross-engine / .tres pattern summary | Manim two-column |
| BHTF | Remotion ClaudeComposerAsk | Your Turn: read 2d/particles, convert one effect, check Compatibility | Manim text |
| BOUT | Remotion ClaudeTitleOutro | @NikBearBrown outro | — |
