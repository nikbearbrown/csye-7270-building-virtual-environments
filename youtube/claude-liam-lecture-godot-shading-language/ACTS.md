# Godot Shading Language — coverage and cast

CSYE 7270 Building Virtual Environments. One self-contained lecture; Liam, in for Bear; @NikBearBrown. This is a film preparation package, not a rendered film.

| Act | Source coverage | Beats | Recurring cast |
|---|---|---|---|
| I · A Program for the Surface | Transcript 0:00–2:14, 3:29–5:38; user language overview | B01–B07, including B02A/B06A | One quad, its vertices and fragments; real 2D patch and 3D cube |
| II · Coordinates, Not Memory | Transcript 2:15–3:28; user per-pixel mental model | B08–B14 | Same quad, fixed collider outline, UV field, time dial |
| III · Types You Can See | Transcript 5:39–13:04 plus arrays 23:33–24:08 | B15–B21 | Four vector cells; column-major matrix; three array slots |
| IV · Who Owns the Value? | Transcript 13:05–18:43 | B22–B28 | Two patches, one shared material, then independent values |
| V · Passing Values, Choosing Paths | Transcript 18:44–23:32 | B29–B35 | Vertex-to-fragment ramp; one branch token; bounded loop cursor |
| VI · Build, Verify, Keep Learning | User learning path, alternatives, shader practice; transcript outro | B36–B44 | Tint test at 0/0.5/1; actual logs and real documentation pages |

Prerequisite swap: arrays move before flow control so the bounded-loop example has a known collection. The source introduces them after loops. Varyings stay after uniforms; their interpolation is shown explicitly.

Opening: approved Professor Bear portrait/title, then hesitant writer correcting “remember the last pixel” to “compute from their inputs”; then terms: GPU, Vertex, Fragment, Material, UV.
Closing: six recap statements, a runnable learner prompt with two checks, locked title/handle outro. Course credit in greeting and recap block.

## LEFT OUT
- Filler, repeated variable renaming, sponsor/supporter thanks: no independent teaching content.
- Deliberately freezing the editor with an infinite loop: replaced by a bounded trace and an unexecuted warning; no GPU hang is induced.
- Unattributed source author's goodbye: replaced by course/channel bookends; source author/title/URL were not supplied and will not be guessed.
- Extra shader categories not listed in the user's overview: the five supplied are examples, not an exhaustive version-dependent count.
- Full noise/SDF derivations and compute implementation: introduced as next learning paths, as in the user's notes; this film earns the foundation rather than claiming to teach those advanced topics.
