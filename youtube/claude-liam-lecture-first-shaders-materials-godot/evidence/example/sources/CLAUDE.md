@AGENTS.md
@CHANGE-BRIEF.md
@assignments/05-shaders-materials/CHANGE-BRIEF.md

# Signal Garden context

The inherited 2D game stays the default (`godot/project.godot`). The worked
historical feature-bundle scene is `godot/signal-garden/main.tscn`, launched by
`signal-garden.command`. Corrected Canvas briefs are in `assignments/course-briefs/`.
Current instructor examples cover Assignments 1–9, excluding the final; their
index is `assignments/course-series.json`. Old numbered feature folders are history.
The isolated expanded lab is `godot/course-series/main.tscn`; the generated
asset exercise is `godot/course-series/asset-slice.tscn`.

## State and boundaries

`godot/signal-garden/garden.gd` owns movement, charge, gate state and completion.
Move with WASD/arrows; E charges on the pad; R resets; P/Escape pauses; M mutes.
Speed is 3 m/s, charge 0.6 seconds, at 60 physics ticks/second. The pad's
`activation` uniform moves from 0 to 1 with charge/0.6 and remains 1 when open;
reset returns it to 0. No global TIME or render-frame counter controls gameplay.
The quiet/active colors and eight stripes are in `signal.gdshader`.

`mascot-rig.gd` creates idle/walk/charge/celebrate clips on the existing nine-bone
mascot. Animation observes gameplay, never changes colliders or gate rules.
`effects/burst.tscn` fires at gate opening and completion; `ambient.tscn` emits
while the gate is open, the run unfinished, and the scene visible. Both pause.
`sound.gd` supplies temporary, authored test tones. The separate asset slice uses
actual local SD-Turbo images and MusicGen audio; prompts, revisions, seeds and
edits are in `assignments/02-generated-assets/`. They are not hand-drawn assets.
Buses are declared in `godot/default_bus_layout.tres`. Audio does not decide state.

Do not change Shipping Lane, original tests, tuning or its evidence to repair a
Signal Garden failure. Keep known-bad shaders in `signal-garden/audit/`; never
load them into the playable scene. The demonstrated audit is disclosed, not blind.

## Checks

From repo root:
- `godot --headless --path godot --editor --import --quit`
- `python3 scripts/check-garden.py`
- `python3 scripts/check-garden.py test-timing 30` (also 60 and 144)
- `python3 scripts/check-garden.py test-marker-parity`
- `godot --headless --path godot --script res://signal-garden/tests/test-audio.gd`
- `python3 scripts/bench-garden.py`
- `python3 scripts/mutate-garden.py` (isolated disposable copies)
- `godot --path godot --fixed-fps 60 --disable-vsync --script res://signal-garden/tests/shader-bench.gd`
- `python3 scripts/shader-oracle.py`

The course lab uses saved idle/walk/charge/celebrate animation resources,
two textured ShaderMaterials, fixed-seed particle curves and a read-only V probe.
Shaders and language examples drafted by Codex are instructor scaffolds, not a
claim that Bear or a student fulfilled the brief's handwritten requirement.

Additional checks: `scripts/course-series/run_test.py` with scripts under
`res://course-series/tests/`; teaching exercises use `--project teach/starter`
or `teach/solution`. Expected starter assertion failures are not script errors.

The Python check wrapper bounds run time and treats engine errors as failures even
when Godot exits zero. Keep failed receipts. Source index: `assignments/README.md`.
Do not claim human playtesting, listening, GPU timings, films, tags, publication,
or a Claude Code session unless those actually occurred. Bear now requests one
Brutalist lecture with Liam per assignment, actual audio/video drafts for review.
Retain verified A1/A3 masters; reuse inspected native captures and rendered scenes.
Current film status: `youtube/ASSIGNMENT-FILMS.md`. Do not publish implicitly.
