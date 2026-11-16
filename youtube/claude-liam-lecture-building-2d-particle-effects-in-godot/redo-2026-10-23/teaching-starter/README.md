# Original 2D particle teaching arena

Godot 4.7.2, Compatibility renderer. This isolated project belongs to the corrective lecture rebuild. It does not modify Walker Claude or the course's existing examples.

Open `arena.tscn` for real editor construction. Run `game.tscn` for the centered arena. Space creates a temporary pickup effect, arrows move the marker, T changes the stream condition, H hides the marker, and R resets. The lecture's scripted events use `Input.parse_input_event` and the same `_unhandled_input` callback; they do not call the burst function directly.

`build_assets.gd` produces the original procedural soft dot, scale curve, color ramp, and reusable baseline burst. The lecture constructs and saves a new burst through the real editor. `staged_hidden_owner` deliberately demonstrates a visibility fault and defaults to false. The delivered capture plugin is disabled after packaging; action recipes and timestamps remain with the film.

Run the source and ownership checks using a real renderer: `godot --path . --max-fps 60 --script test_lab.gd`. The test waits for real-renderer one-shot completion; it is not a performance measurement. Inspect the rendered result separately.

The project is a teaching arena, not a claim of a completed gameplay integration. GPU and CPU conversion are compared visually, and GPU-specific feature equivalence is not assumed.
