# CAPTURE.md — how the pitch film's gameplay footage was made

Recorded 2026-11-23.

## Revision

All footage comes from a separate `git clone` of commit **`1fbc309a`** of `coldfish432/GodotGame`, made in a scratch folder. The working project and its saves were not touched.

The clone differs from the commit in four ways:

1. **Added `tests/capture_pitch_film.gd`.** It is filming choreography, not game code, and is copied here.
2. **`project.godot`, 4K window.** Added `window/size/window_width_override=3840` and `window_height_override=2160`. The canvas stays 1280×720 (`canvas_items`), so the UI is drawn natively at 3×.
3. **`project.godot`, movie quality.** Added `[editor] movie_writer/mjpeg_quality=0.95`.
4. **`project.godot`, separate data folder.** `config/name` was changed to `downfall-pitch-capture`, so `user://` (settings and save slots) is a separate folder from the real game's.

Re-importing in the clone also rewrote `.import` files. These are import cache metadata, not source changes.

## Engine and command

- Godot `4.7.2.stable.official`, **Forward+ on D3D12**, NVIDIA GeForce RTX 4060 Laptop GPU, Windows 11. The renderer and adapter are recorded in the `start` line of every input log.
- Command:

```
Godot_v4.7.2-stable_win64_console.exe --path <clone> --script res://tests/capture_pitch_film.gd \
  --write-movie <clip>.avi --fixed-fps 30 --quit-after <cap> -- <clip> <seed>
```

- **Output:** Godot Movie Maker, MJPEG 3840×2160 at 30 fps, with the game's own audio as PCM.
- **Speed:** Movie Maker is offline rendering, so these clips say nothing about real-time frame rate.
- **UI language:** set to English (`I18n.set_language("en")`) to match the English narration. The game ships both Chinese and English.
- **Crash at exit:** every run ended with a segmentation fault at exit, *after* its log was written and the AVI was finalised. This is the known static-cache crash at exit. All seven AVIs probe with full durations.

## Method: scripted input, not a human playtest

- **Combat and walking:** done by `tests/ai_driver.gd` (AiDriver), which is already in the repo. It re-reads game state every tick and makes the same calls a click makes: `Player.set_move_target`, `Player.attack` and `GameManager._interact`.
- **Keys and buttons:** keys are real `InputEventKey` events (E). Title buttons are real mouse clicks at the button's centre.
- **Choices:** the driver takes route and relic choices with `advance(0)` and `choose_build(first)`. Each choice is held on screen first.
- **No cheats:** no invulnerability and no HP writes in any clip.
- **Logs:** every decision is logged with its frame number in `<clip>-inputs.jsonl`.

## Clips and disclosed setup

| Clip | Seconds | Beat | Setup shortcuts (all in the input log) |
|---|---|---|---|
| `title` | 24.7 | B09 | None. The main scene runs as the current scene, as in the exe. Path: Start, New save, loading, base, PRTS welcome card. Not a timing measurement. |
| `mine` | 83.1 | B00, B03 | None. Mine, floor 1, the driver fights. Sword waves and enemy telegraphs are visible. The 75 s window ran out before it reached the descent. |
| `regions` | 42.0 | B02, B06 | None. Lungmen upper city, Sami snowfield and Siracusa, 12 s of play each. Between regions a `settle(true)` call ends the contract; that moment is not used in the film. |
| `bridge` | 6.5 | B02 | Snow, seed 1002. One teleport to 8 m before the bridge centre, and the field cleared so the walk is not interrupted. She then walks across the deck. |
| `route` | 24.7 | B04 | One teleport beside the floor-1 descent marker, standing in for clearing the floor. Then a real E press opens the route map. The driver picks the first route and floor 2 loads. |
| `camp` | 18.3 | B04 | Camp 10\|11 unlocked in memory, standing in for walking floors 1–10. The E press opened a nearby weapon crate, not the beacon, so the script called `GameManager.camp_extract()`, which is what the beacon calls (logged as `fallback_camp_extract`). The settlement screen that follows is real. Trim out the crate window. |
| `base` | 22.2 | B05 | Exchange and research set as built in memory, because a fresh state has them unbuilt. Screens opened with `open_station` / `open_exchange`, which is what the station hotkey or E does. Trim the one transition frame. |

The A5 fire, A6 particles and A7 rig shots for B06 are not in these clips. **B06 has to be cut from the tagged evidence** of those assignments (each clip with its tag in the corner), or recorded separately.

## Files

- Raw AVIs (about 3 GB) stay local in `D:\CSYE 7370\build\pitch-raw\`. They are not in git.
- SHA-256 hashes and durations are in `raw-avi-sha256.json`.
- Input logs are in `*-inputs.jsonl`.
- The choreography script is `capture_pitch_film.gd`.
