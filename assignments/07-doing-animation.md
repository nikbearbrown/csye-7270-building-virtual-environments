# Assignment 7 - Doing Animation with Claude and Godot

The first review measured this assignment against wiring animation to player actions. Measured against doing animation with Claude and Godot, a larger gap shows. The assignment is almost entirely about connecting clips to state and proving the connection holds. Making the clips, which is most of what "doing animation" means, gets one table of minimum requirements and no method.

There is no guidance on how a clip gets authored, what Claude is good and bad at when authoring one, or how to tell whether a clip Claude wrote animates anything. The pin-first discipline is excellent and should stay. It needs a matching discipline for creation.

## Where the weight sits now

| Area                      | Points (of 60) |
|---------------------------|----------------|
| Pinning                   | 12             |
| State machine             | 12             |
| Edges and verification    | 14             |
| Film                      | 10             |
| The animations themselves | 12             |

The animation set's 12 points are mostly for existence: a simple clip, a sheet or rig, and a cycle. The text has a planning prompt and Chapter 10's pin, change and re-pin prompts, all about behaviour. Nothing tells a student how to get Claude to make a walk cycle, or how to check one it made.

## 1. Name the authoring routes; each needs a different check

Claude can produce Godot animation in four ways. They fail differently, and the assignment should ask students to say which route each clip used.

**Keyed clips written as resource text.** Claude writes the `Animation` resource directly in the `.tscn` or `.tres` file: track paths, key times, values and transitions. This is Claude's strongest route, because it turns a timing spec into exact key times. It also fails silently. A track whose path names a node or property that doesn't exist animates nothing, and the editor marks it but the game doesn't complain. A state test that checks `current_animation` passes on a clip that moves nothing: counting is not watching, one level down.

**Clips built in code.** A GDScript builds the `Animation` with `add_track` and `track_insert_key`. This is good for parametric timing, where key times come from constants, but invisible in the editor's animation panel if built at runtime. Require baking instead: a headless tool script builds the clip and saves it with `ResourceSaver.save()` to a committed `.tres`. The editor then shows it and every diff is reviewable. That matches A6's "configured in the scene file, not built in code."

**Frames drawn by code.** Here Claude writes the drawing, as in `walker-jumpman-clawd`, and the poses are rendered into a sheet. Drawing into an `Image` works headless. Drawing with `CanvasItem` calls needs a renderer, so the sheet is rendered in a windowed run (a `SubViewport` capture or Movie Maker). Generated frames follow Assignment 2's rules and need the registration check from the first review, because drift between frames is their typical failure.

**Imported 3D clips.** Here Claude can't usefully author bone rotations in text, but it can retime clips, set loop modes and adjust blending. The trap is A5's lesson again: animations inside an imported scene are reimported. Loop mode set by editing the imported clip in the scene is lost on the next reimport. It belongs in the importer's per-animation settings, which live in the `.import` file. The A5 rule, verify from an empty cache, applies.

## 2. A read-back test for every keyed clip

The fix for the silent-track failure is a structure test, alongside the state-machine structure test the first review proposed. It checks four things:

- every track resolves to a real node and property;
- key times match the brief's phase table;
- the loop mode is what the brief says;
- frame tracks use discrete updates.

gdscript

``` gdscript
# Every track in every clip resolves to a real node and property.
static func track_problems(player: AnimationPlayer) -> Array[String]:
    var problems: Array[String] = []
    var root := player.get_node(player.root_node)
    for clip_name in player.get_animation_list():
        var clip := player.get_animation(clip_name)
        for t in clip.get_track_count():
            var path := clip.track_get_path(t)
            var node := root.get_node_or_null(NodePath(path.get_concatenated_names()))
            if node == null:
                problems.append("%s track %d: no node at %s" % [clip_name, t, path])
            elif path.get_subname_count() > 0 and not (path.get_subname(0) in node):
                problems.append("%s track %d: %s has no property %s" % [clip_name, t, node.name, path.get_subname(0)])
    return problems
```

The other three checks are one line each against the brief:

- `clip.track_get_key_time(t, k)` equals the brief's frame divided by the clip's frame rate;
- `clip.loop_mode` is `Animation.LOOP_LINEAR` for a cycle;
- `clip.value_track_get_update_mode(t)` is `Animation.UPDATE_DISCRETE` for any `frame` track.

The last check matters. A frame track left on continuous updates interpolates the frame index between keys, so a clip keyed 0 then 7 sweeps through every frame in between.

Two of these catch the course-wide Godot 3 carry-over directly. Godot 3's `Animation` had a boolean `loop`; Godot 4 uses `loop_mode`. An agent that writes `loop = true` produces a clip that doesn't loop and may load without complaint. Godot 3's `playback_speed` is Godot 4's `speed_scale`, which is the same kind of trap.

## 3. Turn the phase table into keys

The first review proposed designing the committing action in startup, active and recovery frames, measured from the motion reference. For authoring, that table is exactly what Claude needs. It converts frames into key times without rounding errors, puts a key at each phase boundary, and sets transitions so the spacing matches the phase: accelerating into the active frames, settling through recovery.

The workflow becomes:

1.  The student measures the reference and writes the phase table.
2.  Claude writes the keys and a table pairing each key time with its source frame.
3.  The read-back test pins those key times.
4.  The frame strip shows whether the motion reads.

Each layer checks the one before. When play says the timing is wrong, the student changes the phase table, not the keys, and the change flows down.

## 4. Prompts for making clips, not just wiring them

Two drafts. They pair with the pin, change and re-pin prompts the chapters already supply.

The authoring prompt, one clip at a time:

text

``` text
Read CLAUDE.md first. The phase table for <action> is in CHANGE-BRIEF.md,
in frames at <fps>.

Write the <action> clip for the AnimationPlayer in <scene>, using Godot 4
Animation properties for the version in CLAUDE.md (loop_mode, not loop;
discrete update mode for any frame track). Put a key at every phase
boundary in the table, and list each key's time beside the frame it comes
from. Add a read-back test that asserts every track path resolves to a
real node and property, every key time matches the table, and the loop
mode and update modes are as stated. Run it through ./scripts/run-test.sh
and show the real output. Do not wire the clip into the state machine
yet. Do not commit.
```

The tuning prompt, one change at a time:

text

``` text
Read CLAUDE.md first. The current capture is in captures/<action>/ and
its per-frame log is in logs/. What I saw playing at normal speed and at
--time-scale 0.25: <what you saw, in visual terms>.

Read the frames at each phase boundary in CHANGE-BRIEF.md, with the log
lines for the same frames, and say where the motion and the table
disagree. Then propose one change, to the phase table or to one key's
transition. Before editing, say what the capture should show afterward.
After I approve, make only that change, update the read-back test's
expected values, and stop so I can recapture and play. Do not commit.
```

The tuning prompt changes the clip and its read-back expectations together. That is legitimate here, because the read-back pins the clip's structure, not the game's behaviour. Behaviour pins still change only in their own re-pin step, after play. Say this explicitly in the assignment, or students will reasonably think it contradicts "keep the change and the re-pin apart."

## 5. Give the creation side its own section in the assignment

The current Build It runs: baseline, pin, build the animation set and state machine, edges, re-pin. "Build the animation set" hides most of the work. I'd split it in the text, without changing the order.

**Make the clips.** For each item of the minimum set:

- the authoring route;
- the phase table, or the cycle's frame count and seam rule;
- the read-back test;
- a frame strip judged against the motion reference.

New clips change nothing the pin covers until they're wired, so this can happen before or after the pin.

**Wire them.** The state machine, its structure test, the behaviour changes, edges and re-pins, as written now.

The rubric's animation-set line then grades making the clips, not their mere existence.

| Animation-set criterion | Points |
|----|----|
| Simple animation, with route and read-back | 3 |
| Sheet or rig, with editable sources, provenance, registration or import settings checked, and read-back | 5 |
| Cycle, with a correct seam for its track type and read-back | 4 |

The total stays 12. With the first review's proposed rubric, the creation share rises to 20 of 60: the animation set plus the new feel-and-readability line. The pin discipline keeps 30 across pinning, the state machine and verification.

## Still standing from the first pass

These all carry into the rewrite.

- **Numbering.** The headers run 5, 6, 7 while the A6 and A7 bodies run one ahead. The rewrites will treat the headers as correct and fix the tags, dates, `SUBMISSION.md` titles and cross-references, unless you say otherwise.
- **Cycle seam.** Give the rule by track type. Continuous tracks match at 0 and `length`. Frame tracks have no duplicate across the wrap, and the gap from the last key to `length` equals the key interval.
- **Injected input.** Make `Input.parse_input_event` the default. `action_press` never reaches `_input` or `_unhandled_input`.
- **Two clocks.** The brief records each animation node's `callback_mode_process`, and which tick gameplay reads any keyed gameplay fact on. Method tracks are deferred.
- **`AnimationTree` traps.** Name the advance-expression base node alongside `advance_mode`, and add a structure test of the state table against the resource.
- **Watching.** Run the pin test or a replay with a renderer, Movie Maker and `--debug-collisions`, so frame N lines up with log line N. Claude's reading of the frames is a claim.
- **Phases.** Design the committing action in startup, active and recovery frames, with interrupts per phase, and test edges at the phase boundaries.
- **Concepts.** Make the four objectives explicit: tracks of keys, one authority, two clocks, feel designed in frames.
- **Continuity.** Replace the brief's contents, and extend the wrapper's error patterns to resource-load failures. Keep read-only git and the result-event check. Add a rule for resuming interrupted sessions, and use `git worktree` for the mutation check.
- **Rubric.** Add a feel-and-readability line, with the pinning, verification and film lines reduced as proposed.
- **Small fixes.** Strip the `?si=` links, move the due-date line, match A5's header order, and drop "the course's earlier animation assignment." Alias the skill spelling, explain how to produce the second tick offset, fix the effects cross-reference, and run the verify commands through the wrapper.
