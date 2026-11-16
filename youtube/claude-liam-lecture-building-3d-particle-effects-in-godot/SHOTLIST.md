# SHOTLIST.md — Building 3D Particle Effects in Godot

All body beats are Manim except B12 (GodotDevWorkbench). Spine beats are Remotion.

| Beat | Render | Visual | Runner-up |
|---|---|---|---|
| BOPEN | Manim | Title card on STAGE background | Remotion ClaudeTitleIntro |
| BIDEA | Remotion BrutalistHesitantWriter | Hesitant-writer beat | Static text card |
| BDEFS | Remotion ClaudeDefinitions | 5 term cards | Manim scrolling list |
| BACT1 | Remotion FormACard | "Act 1 — CPU vs GPU in 3D" | Manim divider |
| B01 | Manim | Three CPUParticles3D effects: coin burst, enemy explosion, bullet glow with amount/lifetime table | GodotDevWorkbench |
| B02 | Manim | Feature comparison table: GPU3D vs CPU3D (sub_emitter, trail, process_material, shader) | GodotDevWorkbench |
| B03 | Manim | Animation track diagram: AnimationPlayer → CPUParticles3D:emitting key at t=0 | Code card |
| BACT2 | Remotion FormACard | "Act 2 — Sub-Emitters" | Manim divider |
| B04 | Manim | Sub-emitter chain diagram: parent emitter → AT_END → child emitter at particle death | Animated sequence |
| B05 | Manim | Sub-emitter mode enum table: DISABLED / CONSTANT / AT_END / AT_COLLISION / AT_START | Remotion comparison card |
| B06 | Manim | Three gotcha cards: (1) stops own emitting, (2) amount capped, (3) no self-sub | Animated reveal |
| BACT3 | Remotion FormACard | "Act 3 — Particle Shaders" | Manim divider |
| B07 | Manim | Shader anatomy: shader_type particles; start()/process(); built-ins labeled | Code card |
| B08 | Manim | Headless compile: valid shader → OK; broken shader (`vec2` assign) → ERROR message | Terminal skin |
| B09 | Manim | Three column table: custom forces / procedural shapes / CUSTOM channel; each with example | Animated reveal |
| BACT4 | Remotion FormACard | "Act 4 — The Draw Half" | Manim divider |
| B10 | Manim | StandardMaterial3D flag card: 4 flags (additive, unshaded, billboard, proximity_fade) with diagrams | GodotDevWorkbench |
| B11 | Manim | Six cost lever cards: amount · lifetime · fixed_fps · visibility_aabb · texture_size · overdraw | Remotion data viz |
| B12 | Remotion GodotDevWorkbench | walker-3d-platformer coin burst CPUParticles3D reconstruction | Manim property list |
| BVDT | Remotion ClaudeVerdictArtifact | What 3D adds / what stays same / new trap | Manim two-column |
| BHTF | Remotion ClaudeComposerAsk | Your Turn: CPU→GPU conversion + sub-emitter | Manim text |
| BOUT | Remotion ClaudeTitleOutro | @NikBearBrown outro | — |
