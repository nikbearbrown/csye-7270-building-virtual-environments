# PROMPTS.md — Building 3D Particle Effects in Godot

No AI-generated video or images used. All body beats are Manim or Remotion.

## Manim beats (11)

| Beat | Class | What it renders |
|---|---|---|
| B01 | B01_ThreeEffects | Three CPUParticles3D effect cards with property tables |
| B02 | B02_CPUvsGPU3D | Feature comparison table: GPUParticles3D vs CPUParticles3D |
| B03 | B03_AnimTrack | AnimationPlayer → CPUParticles3D:emitting key at t=0 diagram |
| B04 | B04_SubEmitterChain | Sub-emitter chain: parent → AT_END → child at particle death |
| B05 | B05_SubEmitterModes | sub_emitter_mode enum table (5 modes) |
| B06 | B06_SubEmitterSurprises | Three gotcha cards: stops emitting / amount capped / no self-sub |
| B07 | B07_ShaderStructure | shader_type particles; start()/process(); built-ins labeled |
| B08 | B08_HeadlessCompile | Two terminal outputs: clean shader OK; vec2 assign ERROR |
| B09 | B09_ShaderVsMaterial | Three-column table: custom forces / procedural shapes / CUSTOM channel |
| B10 | B10_DrawMaterial | StandardMaterial3D flag cards: additive / unshaded / billboard / proximity_fade |
| B11 | B11_CostLevers | Six cost lever cards with direction arrows |

## Remotion beats (11)

| Beat | Pattern | What it renders |
|---|---|---|
| BOPEN | (CARD — lecture title slide) | Title card on STAGE background |
| BIDEA | BrutalistHesitantWriter | Hesitant-writer framing beat |
| BDEFS | ClaudeDefinitions | 5 term cards: sub_emitter / particle shader / billboard / proximity_fade / visibility_aabb |
| BACT1 | FormACard | "Act 1 — CPU vs GPU in 3D" |
| BACT2 | FormACard | "Act 2 — Sub-Emitters" |
| BACT3 | FormACard | "Act 3 — Particle Shaders" |
| BACT4 | FormACard | "Act 4 — The Draw Half" |
| B12 | GodotDevWorkbench | walker-3d-platformer coin burst CPUParticles3D reconstruction |
| BVDT | ClaudeVerdictArtifact | What 3D adds / what stays same / new trap |
| BHTF | ClaudeComposerAsk | Your Turn: CPU→GPU conversion + sub-emitter + cost measurement |
| BOUT | ClaudeTitleOutro | @NikBearBrown outro |

## No AI video or image generation

No Higgsfield, no GPT Image, no AI-generated stills. All visuals are built
programmatically (Manim) or from the Remotion component library.
