# Assignment 6 - Creating Particle Effects with Godot and Claude

Measured against its purpose, students being able to create particle effects with Godot and Claude, this assignment's centre of gravity is off. It is strongest on what a headless run cannot tell you and on what an effect costs. It is weakest on creation itself: how an effect is designed and tuned, and how to work with an agent that cannot see what it built.

The verification and pricing material is good and should stay. But as written, a student can earn most of the 60 points by building two effects that technically fire, pricing them carefully and testing their state, without ever learning to make an effect that reads well. Nor would they learn a working method for directing Claude on something visual.

## Where the weight sits now

Of the 60 implementation points:

| Area                   | Points                        |
|------------------------|-------------------------------|
| The effects themselves | 22 (Effect A 12, Effect B 10) |
| Verification           | 10                            |
| Price                  | 10                            |
| Film                   | 10                            |
| Intent                 | 8                             |

In the text, pricing gets its own subsection, about a quarter of the assignment.

The guidance on creation amounts to two things: a list of setting names in the brief, and one planning prompt. There is no prompt for building an effect, no prompt for tuning one, and no method for getting visual feedback into the agent's loop. For an assignment whose goal is creation, the ratio should roughly invert.

## 1. Claude can't see the effect, and the assignment never closes that loop

The assignment correctly says a headless run draws no GPU particles and that "you are the only instrument that can see." That is true of the headless run, but not of Claude. Claude Code can read image files. The missing piece is a way to put real rendered frames of the effect in front of it.

Godot already has that piece. Movie Maker mode renders the real scene, on the real renderer, at a fixed frame rate, and writes each frame to disk as a numbered PNG sequence:

bash

``` bash
godot --path godot res://previews/hit_burst_preview.tscn --write-movie captures/hit_burst/frame.png --fixed-fps 30 --quit-after 45
```

This proposal has five parts.

1.  **A preview scene per effect.** It holds the effect at in-game camera scale, over a representative stretch of the real background, with a script that triggers the effect at a set frame. It is a labelled fixture, like the chapter's frozen mob, so captures from it are labelled as fixture captures in the film.
2.  **A frame strip after every build or tuning step.** Claude reads a handful of frames (say 0, 2, 5, 10, 20 and 40) and reports what it sees against the intent. Too small to read at character scale? Lost against the background? A flat fade? Single pixels?
3.  **Predict, then look.** Before each tuning change, Claude states what the strip should look like afterward. Then it regenerates the strip and compares. This is the course's predict-then-check loop, applied to craft.
4.  **Claude's reading is a claim.** Its visual judgment is useful and fallible, like everything else it reports. The student's dated verdict, in the running game at the target window size, is still what gets graded. The frame strips make that verdict reviewable: a TA can see what the student saw.
5.  **Controlled randomness.** Particle randomness differs between runs, which confounds before-and-after comparisons. If the pinned Godot version offers a fixed seed on particle nodes, use it for strips; if not, compare more frames and say so.

Movie Maker needs a real renderer, so this runs windowed. It is not covered by the `godot --headless` allow rule. The capture command gets its own rule, `Bash(godot --path godot:*)` scoped as narrowly as the student's Claude Code version allows, or the student runs the capture and Claude reads the frames. Either way works. What matters is that frames, not descriptions, reach the agent.

This is also the single most transferable thing the assignment could teach about working with Claude: when the agent can't observe the result, build it an instrument that can.

## 2. Teach how an effect reads, not just which settings exist

The brief asks for size, speed, duration, colour and shape, and the emission, process and draw settings. That is a parts list, not design guidance. A student who has never made an effect doesn't know what makes a burst read as a hit and not as a flicker. Add a short section on how effects read, and fields in the brief that use it:

- **Timing phases.** A burst reads through its shape in time: a strong first frame, a fast outward phase, and a slower dissipation. The brief should state each phase's rough duration and what happens in it. "Lifetime 0.6 s" is a setting; "bright on frame one, gone by the time the next hit could land" is an intent.
- **Contrast against the real background.** Value contrast, not hue, is what makes an effect readable. Judge the effect over the actual level art, not over the editor's grey.
- **Scale against the character.** The brief already asks for this. Make the frame strip the evidence for it.
- **Change over life.** Colour, alpha and scale curves are most of the look. A burst that fades only in alpha, at constant size and colour, usually reads as flat.
- **Variation.** Randomness in velocity, scale, hue and rotation keeps repeats from looking stamped. This matters for Effect A, which fires many times.
- **Layering.** Good effects are usually several emitters: a flash, sparks, a puff. Say explicitly that one effect may be several emitters under one node, and that the tests and price cover the whole group.

## 3. The failures students will hit are in the draw step and in Godot 3 names

The chapter's predicted failures, a null texture and Disable Z, are real but 2D-only. Students working in 3D, or with an agent writing their scene files, will hit a different set. Name these in the brief guidance as candidate predicted failures.

**Godot 3 property names.** This is the agent-specific one, and the most important. Agents trained on mixed Godot 3 and Godot 4 material write Godot 3 names: `ParticlesMaterial` instead of `ParticleProcessMaterial`, `initial_velocity` instead of `initial_velocity_min` and `initial_velocity_max`, `scale` and `scale_random` instead of `scale_min` and `scale_max`. A scene file with names the class doesn't have may load without complaint and leave those settings at their defaults. The effect then fires, every state test passes, and it looks like the defaults.

The fix is a configuration test that reads each setting from the brief back from the loaded resource:

gdscript

``` gdscript
var burst := (load("res://effects/hit_burst.tscn") as PackedScene).instantiate() as GPUParticles2D
var pm := burst.process_material as ParticleProcessMaterial
check("one_shot", burst.one_shot)
check("spread", is_equal_approx(pm.spread, 180.0))
check("velocity min", is_equal_approx(pm.initial_velocity_min, 120.0))
check("disable z", pm.particle_flag_disable_z)
```

The values come from the brief, so the test also catches drift between the brief and the scene.

**3D draw-material settings:**

- A colour ramp has no visible effect unless the draw material uses vertex colour as albedo (`vertex_color_use_as_albedo`).
- An alpha fade needs a transparent material.
- Camera-facing quads need the particle billboard mode, which flipbook animation also depends on.

All three fail silently: the effect fires and looks wrong.

**2D draw materials.** Additive glow and flipbook animation both need a `CanvasItemMaterial`, with the blend mode or particle animation set and the frame counts matching the texture.

**The visibility rectangle.** A GPU effect whose `visibility_rect` (2D) or `visibility_aabb` (3D) is too small gets culled when its rectangle leaves the view. The usual symptom is a large effect popping out at the edge of the screen. The editor can generate the rectangle; the brief should say it was generated, or set and checked.

**`preprocess`.** An ambience effect without it starts empty when the scene loads and fills in over one lifetime. Players notice that on every scene load.

## 4. Give Claude prompts for creating and tuning, not just planning

The assignment has one prompt, and it plans. A5 gives a prompt for each stage. A6 needs at least two more. These are drafts.

The build prompt, one effect at a time:

text

``` text
Read CLAUDE.md first. Effect A's intent is in CHANGE-BRIEF.md.

Build Effect A as a scene file using Godot 4 class and property names
for the version in CLAUDE.md; if you are unsure a property exists in
this version, say so instead of guessing. Configure it in the scene
file, not in code. Add a configuration test that reads back every
setting the brief names, and a preview scene in godot/previews/ that
triggers the effect at frame 10.

Run the configuration test through ./scripts/run-test.sh and show the
real output. Then tell me the capture command to run, and stop. Do not
change gameplay code. Do not commit.
```

The tuning prompt, one lever at a time:

text

``` text
Read CLAUDE.md first. Effect A's intent is in CHANGE-BRIEF.md.
The current frame strip is in captures/hit_burst/. What I saw in the
running game: <what you saw, in visual terms>.

Read frames 0, 2, 5, 10, 20 and 40 and say how they compare to the
intent. Then propose one change to one setting. Before editing, give
the setting, its old and new value, and what the frame strip should
look like afterward. After I approve, make only that change, update
the configuration test's expected value, and stop so I can recapture.
Do not commit.
```

After the recapture, the student asks Claude to compare the new strip with its prediction, then records the before-and-after pair in `FRICTIONAL.md`. Every tuning step leaves three things behind: a prediction, two strips, and a verdict.

## 5. Make Effect B teach something A didn't

Effect B's three options differ widely in difficulty. Ambience is the easiest, a feedback loop is moderate, and a 3D `trail_enabled` trail needs a ribbon or tube mesh set up correctly. Under the relative quartile, that spread is unfair in both directions.

Instead of ranking the options, require Effect B to use at least one process or draw feature that Effect A didn't, and name it in the brief. Candidates are a different emission shape, turbulence, damping, an attractor, collision, a sub-emitter, a trail, a flipbook, or a value-driven `amount_ratio`. That guarantees B teaches something new whichever option is chosen. The rule "Effect B must not be a second burst" stays.

## 6. Rebalance the rubric toward creation

This is a proposed redistribution of the 60 implementation points. The film keeps A5's 8 points.

| Criterion | Now | Proposed |
|----|----|----|
| Intent before building: a block per effect with timing phases, contrast, scale, change over life, variation and layering (4); failures, price predictions and a budget, committed before the first build step (2) | 8 | 6 |
| Effect A: fires on the real event every time and never otherwise, including the retrigger case, visible and at the right place (7); reads as intended on screen, with a working draw setup (7) | 12 | 14 |
| Effect B: a different job using a feature A didn't, starting and stopping with its condition, including pause and hidden states (6); reads as intended on screen (6) | 10 | 12 |
| Tuning with Claude: frame strips before and after each revision, with Claude's predicted change (4); at least one observation-driven revision per effect, with Claude's visual claims checked against your own verdict (4) | — | 8 |
| Verification: state and configuration read-back tests for both effects, run by you, mode stated (4); the retrigger case tested (2) | 10 | 6 |
| Price: headless CPU measurement made the chapter's way (3); GPU time on a real GPU with the effect off and on, and the budget comparison (3) | 10 | 6 |
| Brutalist explainer | 10 | 8 |
| **Subtotal** | **60** | **60** |

Pricing goes from 10 points to 6, not to zero. The two-instrument lesson is worth keeping, but it is a supporting skill here, not the point. Its text should shrink to match.

## Still standing from the first pass

These all carry into the rewrite unchanged.

- **Numbering.** The header says Assignment 6; the tag, the `SUBMISSION.md` title, the Day 70 date and the Module 9 coverage all say Assignment 7.
- **Retrigger.** On a `one_shot` node, a second event mid-burst does nothing. Require a restart, overlap or ignore rule, and test two events inside one lifetime.
- **Vsync.** It flattens the on-screen frame-time comparison to zero. Make the Visual Profiler's GPU time primary, disable vsync for any FPS comparison and confirm FPS actually rises, and compare GPU nodes to the budget on GPU time.
- **Feedback loops.** Driving `amount` restarts the system and pops. Use `amount_ratio` where the version and node support it.
- **A5 continuity.** Replace the brief's contents rather than appending below the A5 version. Give `run-test.sh` a real-time mode and an optional timeout. Real time is forced by audio, not timers. Use the chapter's refused-command-then-"Expected headless output"-table incident to motivate reading the session's result event.
- **Concepts made explicit.** Define emission, process and draw, and CPU versus GPU. The process material is a particles shader, so converting a copy to a `ShaderMaterial` and reading it connects directly to A5.
- **Small fixes.** Strip the `?si=` links, move the due-date line to an instructor note, match A5's header order, alias the `godot-waikthrough` skill spelling, add `local_coords` to the brief, give the size verdict in the running game rather than the editor viewport, say `CLAUDE.md` rather than "`CLAUDE.md` or `AGENTS.md`", and run the verify commands through the wrapper.
