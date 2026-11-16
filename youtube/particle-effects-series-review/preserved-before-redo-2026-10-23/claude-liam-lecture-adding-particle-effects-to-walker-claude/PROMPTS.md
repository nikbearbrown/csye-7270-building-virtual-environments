# PROMPTS.md — Adding Particle Effects to Walker Claude

No AI-generated video or images used. All body beats are Manim or Remotion.

## Manim beats (11)

| Beat | Class | What it renders |
|---|---|---|
| B01 | B01_ThreePartModel | Three-row table: Emission / Process / Draw — properties, where each lives, independent failure |
| B02 | B02_DeathBurstConfig | DeathBurst node property list: emitting false, one_shot, explosiveness, amount, lifetime, material |
| B03 | B03_ParentTrap | Two-column: Player parent (hidden, invisible) vs Main parent (stays visible) + two-line trigger |
| B04 | B04_NineChecks | 9-check test spec in two batches, each with a label — what it proves vs what it cannot |
| B05 | B05_SessionOneMistake | Table: session 1 predicted failures vs real output; predicted columns crossed out |
| B06 | B06_LambdaBug | Lambda capture diagram: outer var vs lambda copy; signal fires; original unchanged |
| B07 | B07_SilentDefects | Two RoundedRectangle panels: null texture (1×1 px) / Disable Z off — each with fix |
| B08 | B08_SleepOutput | Cost script output table: GPU/CPU/empty all ≈ 6.9 ms; label: "This is a sleep, not a cost" |
| B09 | B09_FixedFpsTable | Fixed-FPS cost table: CPUParticles2D at 1k/10k/50k; empty scene; GPU dummy |
| B10 | B10_HeadlessLimits | Four "cannot prove" items listed in two batches: visible / readable / GPU cost / looks right |
| B11 | B11_EngineMap | 3-engine row: Godot / Unity Built-in / Unreal Niagara — 5 mapped concepts |

## Remotion beats (11)

| Beat | Pattern | What it renders |
|---|---|---|
| BOPEN | (CARD — lecture title slide) | Title card on STAGE background |
| BIDEA | BrutalistHesitantWriter | Hesitant-writer framing: "Is there a burst?" |
| BDEFS | ClaudeDefinitions | 5 terms: one_shot / explosiveness / ParticleProcessMaterial / lambda capture / fixed_fps |
| BACT1 | FormACard | "Act 1 — The Death Burst" |
| BACT2 | FormACard | "Act 2 — Three Sessions, Three Mistakes" |
| BACT3 | FormACard | "Act 3 — Measuring the Cost" |
| BACT4 | FormACard | "Act 4 — What Only You Can See" |
| B12 | GodotDevWorkbench | game_over() two lines + DeathBurst node properties |
| BVDT | ClaudeVerdictArtifact | Parent / test / cost / visual — four verdict lines |
| BHTF | ClaudeComposerAsk | Your Turn: add DeathBurst, enable Disable Z, write 1 test, run game and die |
| BOUT | ClaudeTitleOutro | @NikBearBrown outro |

## No AI video or image generation

No Higgsfield, no GPT Image, no AI-generated stills. All visuals built
programmatically (Manim) or from the Remotion component library.
