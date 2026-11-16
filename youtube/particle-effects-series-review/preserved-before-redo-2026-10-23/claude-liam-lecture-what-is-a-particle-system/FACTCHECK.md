# FACTCHECK — What Is a Particle System?

Gate F — every number and named claim verified against source or primary.

| # | Beat | Claim | Verdict | Source | Fix |
|---|---|---|---|---|---|
| 1 | BIDEA | Framing: "seven hundred checkboxes" | PASS (illustrative hyperbole for framing, not literal) | — | None; it is a framing metaphor, stated as misconception to correct |
| 2 | B01 | Reeves named the technique in 1983; Star Trek II Wrath of Khan genesis demo | PASS | Chapter 9 citing doi:10.1145/357318.357320 | — |
| 3 | B01 | "a fuzzy object as a cloud of primitives that, over time, are generated into the system, move and change form, and die from it" | PASS | Chapter 9, quoting Reeves 1983 abstract | — |
| 4 | B02 | Position, velocity, acceleration are three different jobs | PASS | Nature of Code §particle state; Chapter 9 "birth–life–death loop" | — |
| 5 | B03 | Delta time needed for frame-rate-independent motion | PASS | Standard physics simulation principle; Chapter 9 notes "particle time is frame time" | — |
| 6 | B07 | "20 births per second with a two-second lifetime tends toward about 40 live particles after warm-up" | PASS (illustrative; stated as such per SERIES-PLAN.md: "This is an illustrative calculation, not a measured performance result") | SERIES-PLAN.md explicitly labels it illustrative | Film narration labels it "an illustrative prediction, not a benchmark" |
| 7 | B08 | Godot's built-in node: GPUParticles2D, GPUParticles3D, CPUParticles2D, CPUParticles3D | PASS | Chapter 9 "Four node types, two families"; Godot docs | — |
| 8 | B08 | CPU node has "near-feature parity" but lower performance with large amounts | PASS | Chapter 9, quoting Godot 2D particle docs | — |
| 9 | B09 | Timing model: lifetime = length of one emission cycle; amount = particles in one cycle | PASS | Chapter 9 "The timing model" quoting GPUParticles2D reference | — |
| 10 | B09 | explosiveness 0 = evenly spread births; explosiveness 1 = all at start | PASS | Chapter 9 quoting Godot reference | — |
| 11 | B10 | ParticleProcessMaterial: direction default (1,0,0), spread 45°, gravity (0,-9.8,0) | PASS | Chapter 9 "The process material is 3D, even in 2D"; ParticleProcessMaterial docs | — |
| 12 | B10 | particle_flag_disable_z defaults to false; 2D games should set it true | PASS | Chapter 9 quoting official 2d/particles demo README | — |
| 13 | B11 | local_coords false: particles stay where born when emitter moves; true: travel with emitter | PASS | Chapter 9 "Triggering: a particle node is a node" | — |
| 14 | BVDT | Recap claims match acts | PASS (cross-checked against ACTS.md) | — | — |
| 15 | BHTF | Your Turn: fountain prediction task | PASS (appropriately bounded, from SERIES-PLAN.md Your Turn) | SERIES-PLAN.md | — |

## Date-sensitive claims stripped

No publication dates, release years or version numbers that will age the film are stated in the narration. "Godot's built-in particle node" is used rather than "Godot 4.7.2 GPUParticles2D" in body narration.

## Verdicts summary

All claims PASS. Illustrative calculation (beat 6) is labeled in narration. No fabricated output or performance numbers.
