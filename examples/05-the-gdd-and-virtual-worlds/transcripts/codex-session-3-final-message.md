Implemented and verified AC-01.

Key review correction: the partial criterion-1 test was raycasting against the pad itself. I fixed it to exclude the pad and verify the underlying floor, its upward normal, and exact pad-floor contact. I also strengthened criterion 3 to prove the player exits and genuinely re-enters the pad.

Results:

- Import: exit 0
- Checkpoint test: exit 0; all six criteria passed
  - Pad is 4 m from start
  - Reached by input in 64 frames
  - Actual exit/re-entry confirmed
  - Activation count remained exactly 1
  - Reset and constructed-fall recovery were within 0.2 m
- Input regression probe: exit 0; movement, jump, projectile, and reset all true
- Feature route: exit 0; 2 coins collected and enemy hit
- `godot/project.godot`: unchanged
- `git diff --check`: clean

Evidence was written to ignored files:

- `evidence/probe-after.json`
- `evidence/route-after.json`

Godot continued to emit the project’s existing macOS certificate/log-write and shutdown leak warnings; none caused a failed command.

Final `git status --short`:

```text
 M godot/game.tscn
 M godot/player/player.gd
?? godot/checkpoint/
?? tests/floor_probe.gd
?? tests/test_checkpoint.gd
```

Final `git diff --stat`:

```text
 godot/game.tscn        | 4 ++++
 godot/player/player.gd | 3 ++-
 2 files changed, 6 insertions(+), 1 deletion(-)
```

That stat excludes the untracked checkpoint and test files until they are staged.

Still needs a person to check in the editor:

- Pad visibility and visual clarity
- Whether its purpose is understandable
- Whether its placement feels fair
- Sound, if desired
- Touch and gamepad behavior
- Exported-build behavior