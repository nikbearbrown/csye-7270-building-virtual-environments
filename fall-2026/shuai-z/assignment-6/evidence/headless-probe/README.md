# Headless particles probe (2026-11-04, for the CLAUDE.md review)

A throwaway Godot project, not part of the game. Claude Code wrote and ran it
on 2026-11-04, after the unedited CLAUDE.md draft was committed, to confirm
on this machine (Apple M3, macOS, Godot 4.7.2) the "Headless facts" the
assignment asks to add, and the property names the draft listed as
unconfirmed. Its renderer setting matches the game's, GL Compatibility.

`probe_particles.gd` (`extends SceneTree`, run with `--script`) has five parts:

1. the display server and renderer the run gets;
2. whether each class and property name the brief uses exists in 4.7.2, and
   whether the Godot 3 names do; `godot3_names.tscn` is a scene file written
   with two Godot 3 lines, loaded to see what they set;
3. the node state a test can observe on a one-shot `GPUParticles2D` burst;
4. whether anything drawn can be observed: `capture_rect()` and the frame;
5. headless CPU time per frame for an empty scene, 20,000 GPU particles and
   20,000 CPU particles (headless only).

## How it was run

From `assignment-6/`, with `godot` on PATH (`/opt/homebrew/bin/godot`, which
reports `4.7.2.stable.official.ed1daf0bf`):

```bash
godot --headless --path evidence/headless-probe --import
timeout 300 godot --headless --fixed-fps 60 --path evidence/headless-probe --script res://probe_particles.gd > logs/probe_particles_headless.log 2>&1
timeout 300 godot --fixed-fps 60 --path evidence/headless-probe --script res://probe_particles.gd > logs/probe_particles_window.log 2>&1
timeout 120 godot --headless --path evidence/compat-probe --write-movie <scratch>/frame.png --fixed-fps 30 --quit-after 45 > logs/probe_movie_headless.log 2>&1
```

The second command opens a window for a few seconds. The last one runs the
earlier Compatibility probe (`evidence/compat-probe/`) under Movie Maker, but
headless; its windowed frames are already in that folder.

## What it found

| Question | Headless (`logs/probe_particles_headless.log`) | Windowed (`logs/probe_particles_window.log`) |
|---|---|---|
| Renderer | Display server `headless`, no video adapter (line 3). The frame read-back error comes from `servers/rendering/dummy/` (lines 29-30) | Display server `macOS`, adapter `Apple M3` (line 5) |
| Names the brief uses | All present: 6 classes, 16 `GPUParticles2D` properties, 18 `ParticleProcessMaterial` properties, the texture properties (lines 4-9, 12-16) | Same |
| Godot 3 names | `Particles2D`, `ParticlesMaterial`, `flag_disable_z` and `flag_align_y` are absent. `initial_velocity`, `scale`, `damping` and `hue_variation` exist, but only as editor-only `Vector2` ranges that are not stored (lines 10-11, 17-21) | Same |
| A scene file with Godot 3 lines | `initial_velocity = 300.0` and `scale = 2.0` load without an error and leave `initial_velocity_min/_max` 0/0 and `scale_min/_max` 0/0. The default scale is 1/1, so `scale` hides the particles; it does not leave them at the default (line 22) | Same |
| One-shot burst, 0.45 s at 60 fps (27 frames) | `finished` at frame 27, `emitting` false by frame 28 (line 24) | Same |
| Other node state | `amount_ratio` reads back what was set; a container's child count is the instance count; hiding the container makes `is_visible_in_tree()` false but leaves `emitting` true (lines 25-27) | Same |
| `capture_rect()` | Empty rectangle (line 28) | Also empty, after two GL errors: the particle buffer could not be read back (lines 31-39) |
| The frame | Nothing can be read back (line 33) | A 1152 × 648 image with 2,653 bright particle pixels on the grey background (line 40) |
| CPU time per frame, `--fixed-fps 60` | Empty scene 0.0028 ms; 20,000 GPU particles 0.0040 ms; 20,000 CPU particles 0.7385 ms (mean of three runs, lines 35-37) | Skipped: windowed frame time includes vsync and the GPU |
| Movie Maker under `--headless` (`logs/probe_movie_headless.log`) | It starts recording (line 3), hits the dummy renderer's null texture (line 7) and crashes with signal 11 (line 10). It wrote no PNG | The windowed run wrote frames (`evidence/compat-probe/compatibility_frame30.png`) |

So a headless test can see node state and timing, but nothing drawn. The
windowed contrast for the look is the frame, not `capture_rect()`, which
returned an empty rectangle in both runs. The GPU emitters' headless CPU time
is within about 0.001 ms of the empty scene, while the same number of CPU
particles cost about 0.73 ms; that is the instrument, not the GPU's cost.
These numbers come from one machine on one evening, for the CLAUDE.md facts;
Step 7 prices the effects themselves with the course's cost script.

## The Godot 3 names in a scene file (`probe_mutation.gd`)

Run on 2026-11-04 after the review commit, to correct failure 1 in
CHANGE-BRIEF.md (its Revision 2). From `assignment-6/`:

```bash
timeout 120 godot --headless --path evidence/headless-probe --script res://probe_mutation.gd > logs/probe_mutation.log 2>&1
```

`godot3_mutations.tscn` holds four materials written with Godot 3 lines, and
`godot3_class.tscn` a `Particles2D` node with a `ParticlesMaterial`
sub-resource. What they load as (`logs/probe_mutation.log`):

| Lines in the scene file | Loads as | Line |
|---|---|---|
| (Godot saving a material with `initial_velocity_min` 260 and `_max` 420) | `initial_velocity_min` is written before `initial_velocity_max` | 3 |
| `initial_velocity = 260.0`, then `initial_velocity_max = 420.0` | velocity 0 to 420 | 4 |
| `initial_velocity_max = 420.0`, then `initial_velocity = 260.0` | velocity 0 to 0 | 5 |
| `scale = 0.7`, then `scale_max = 1.0` | scale 0 to 1 | 6 |
| `flag_disable_z = true`, `flag_align_y = true` | `particle_flag_disable_z` true; `particle_flag_align_y` false, its default | 7 |
| `[node type="Particles2D"]` with `[sub_resource type="ParticlesMaterial"]` and `initial_velocity_min = 260.0` | a `GPUParticles2D` with a `ParticleProcessMaterial`, `initial_velocity_min` 260 | 8-10 |

None of these printed a warning or an error. So a Godot 3 class name, or
`flag_disable_z`, changes nothing at all, while `flag_align_y` and the two range names
tested here change the effect without a message.
