# F9 vsync key, checked in a window (2026-11-05)

`game/app/vsync_debug.gd` (the `VsyncDebug` node in `game/app/main.tscn`) toggles vsync with F9 for the GPU price's FPS comparison. A headless run has no window, so Claude Code checked it windowed: it copied `game/` to a scratch folder outside the repository, added `vsync_check.gd` and `vsync_check.tscn` (kept here), and ran

```bash
godot --path <scratch copy of game> --always-on-top res://vsync_check.tscn
```

The scene runs the real `Main`, presses F9 twice with injected key events, and counts frames for 2 s after each state. Output (`logs/vsync_f9_window_check.log`):

| State | Vsync mode | FPS over 2 s |
|---|---|---|
| At start | enabled | 119.9 |
| After one F9 | disabled | 578.9 |
| After a second F9 | enabled | 89.4 |

An earlier run, not logged, read 118.4, 651.5 and 119.9. The numbers move between runs, and the last one dipped below 120, but in both runs F9 switched the mode each time. So F9 works, and with vsync off the FPS rises well above the display's rate, so an FPS comparison is not capped on this Mac. `DisplayServer.screen_get_refresh_rate()` reported 60 Hz, yet vsync held the game near 120 FPS; the display may run faster than it reports, and this check does not settle which. To run it again, copy these two files into a copy of `game/`, not into `game/` itself.
