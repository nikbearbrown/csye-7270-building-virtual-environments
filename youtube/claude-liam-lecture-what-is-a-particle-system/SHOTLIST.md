# SHOTLIST — What Is a Particle System?

Lane histogram: Manim 10, GodotDevWorkbench/Remotion 6, Card/Bookend 4 — total 20 beats.  
Every beat auditioned at least two lanes; runner-up listed.

| Beat | About | Lane Picked | Runner-up | Why this one wins |
|---|---|---|---|---|
| BOPEN | Portrait/title/summary | CARD (lecture-title-slide-16x9) | — | Fixed spine, required |
| BIDEA | Framing correction: checkboxes → loop | REMOTION BrutalistHesitantWriter | Show Tell card | The writer correction IS the lesson's premise change |
| BDEFS | 5 prerequisite terms | REMOTION ClaudeDefinitions | FormACard | Terms with one-line explanations; card test passes |
| B01 | Reeves 1983; birth–life–death loop named | MANIM (text card + credit line) | VOX still (book cover) | Concept not a photo; the loop diagram is the evidence |
| B02 | Position/velocity/acceleration — three jobs | MANIM (three labeled arrows on dot) | Isometric | Geometric arrows ARE the claim; motion shows vectors changing independently |
| B03 | Update step: pos += vel × delta | MANIM (equation → dot moving frame by frame) | ClaudeCodeBeat | The equation in motion IS the teaching point; code would need a screen |
| B04 | One dot tracing an arc under gravity | MANIM (animated trajectory with labels) | GodotDevWorkbench | Pure physics motion; Godot code would show a result not the mechanism |
| B05 | Lifetime, age, normalized fade | MANIM (age bar + fading dot) | ShowTellCard | The fade IS the mechanism; motion from opacity over time is the claim |
| B06 | Collection of dots — spray pattern | MANIM (multi-particle fan, varying velocities) | AlgArtOrganicTurbulence | Teaching, not art — must show individual velocity vectors, not fluid |
| B07 | Population calculation: 20/s × 2s ≈ 40 | MANIM (counter + formula annotation) | ClaudeVerdictArtifact | The calculation building is the motion; a card would be static |
| B08 | Missing cleanup → unbounded growth | MANIM (counter climbing + dots piling up; then restored) | ShowTellCard timeline | Before/after visual with live counter requires animation |
| B09 | Moving emitter; particles keep original velocity | MANIM (emitter dot moves; particle trails diverge) | GodotDevWorkbench code | The spatial relationship is the claim; must show motion |
| B10 | Narrow cone vs wide spread | MANIM (side-by-side comparison; angles labeled) | GodotDevWorkbench | Two simultaneous shapes comparing angle = pure geometric motion claim |
| B11 | Shared force / wind bending particles | MANIM (force vector; particles bend together) | Isometric (wind metaphor) | The collective bending motion IS the claim |
| B12 | Stream vs burst (explosiveness 0 vs 1) | MANIM (side by side; timing bars) | GodotDevWorkbench particle preview | The birth-timing difference is the motion; needs frame-accurate timing shown |
| B13 | Emission/Process/Draw — three separable parts | MANIM (animated table with Godot node names) | Isometric pipeline | The table is the chapter's own structure; needs source names, not boxes |
| B14 | Four node types — GPU vs CPU, what each supports | REMOTION GodotDevWorkbench (node comparison table) | Manim diagram | This is a Godot Inspector/Scene question; source-backed reconstruction shows real node names |
| B15 | Timing: amount/lifetime/explosiveness/one_shot | REMOTION GodotDevWorkbench (inspector view) | Manim parameter animation | Inspector IS the real evidence; label-accurate reconstruction with Disable Z values |
| B16 | Process material 3D defaults; Disable Z | REMOTION GodotDevWorkbench (inspector + gravity annotation) | ClaudeCodeBeat | Exact property values from source; GodotDevWorkbench with Inspector layout is clearest |
| B17 | Parenting and visibility; parent hides → child hidden | MANIM (scene tree diagram; parent node fades → child follows) | GodotDevWorkbench scene tree | The hierarchy motion — visibility propagating — is the claim |
| B18 | Built-in node replacing the hand-built loop | REMOTION GodotDevWorkbench (scene + node with inspector) | Manim side-by-side | The lesson IS the Godot node — reconstruction with real source values proves the equivalence |
| BVDT | Recap — five statements | REMOTION ClaudeVerdictArtifact | FormACard | Fixed spine; recap in pairs |
| BHTF | Your Turn — fountain task with two checks | REMOTION ClaudeComposerAsk | FormACard | Fixed spine; prompt read aloud |
| BOUT | Outro | REMOTION ClaudeTitleOutro | — | Fixed spine, OUTRO-LOCK |

## Tool beats requiring SHOW-THE-THING

| Beat | Tool | Rung used |
|---|---|---|
| B14 | Godot editor / node types | GodotDevWorkbench (source-backed reconstruction, labeled) |
| B15 | Godot Inspector — timing properties | GodotDevWorkbench (source-backed reconstruction, labeled) |
| B16 | Godot Inspector — process material | GodotDevWorkbench (source-backed reconstruction, labeled) |
| B18 | Godot scene + node with inspector | GodotDevWorkbench (source-backed reconstruction, labeled) |

All GodotDevWorkbench beats are labeled "Godot editor reconstruction" per godot-gamedev skill rules. Source paths and property values are drawn from Chapter 9 and Godot 4.7.2 class reference.

## Evidence required before render

- [ ] Teaching simulation GDScript code verified against Godot 4.7.2 docs (can be tested headlessly)
- [ ] Inspector values in B14-B16 drawn from Chapter 9's ClassDB probe results
- [ ] Particle node property names verified from class reference
