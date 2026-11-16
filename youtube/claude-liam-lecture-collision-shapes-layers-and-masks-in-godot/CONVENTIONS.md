# Suggested project conventions — review before adopting

Engine: Godot 4.7.x for this lab; record the actual version and backend.

- Prefer reusable scenes with injected dependencies or signals. Run each scene in a suitable standalone fixture.
- Keep internal references local; parents wire children. Autoloads hold persistent state when needed.
- Preserve existing scene and resource identifiers. Save generated scene trees through PackedScene/ResourceSaver.
- Name collision layers in project settings and mirror one-based numbers in layers.gd.
- Resize shape resources rather than scaling physics bodies. Duplicate shared resources when independence is intended.
- In overlap callbacks, defer physics-server mutations; use an immediate gameplay latch for one-time events.
- Use physics callbacks for collision-based motion. Acceleration uses delta; move_and_slide consumes velocity directly.
- Distinguish previous-move floor state from current-move floor state. Reset interpolation after teleports.
- Use contacts and coordinate conversion for tile selection; document probe distance and boundary behavior.
- Treat timestep travel distance as a diagnostic, never a sufficient no-tunneling proof.
- Run the isolated physics tests, inspect errors, and record the version. Report untested behaviors and human-playtest needs.
- No universal claim that all scenes run without context or all agents lack vision: state the actual harness and available evidence.

Do not replace a reference game's existing AGENTS.md or CLAUDE.md without reviewing these policies in that project's context.
