# CAPTURE.md — how this film's gameplay evidence was made

## Revision under demonstration

The game source is commit `111bf6e` of `coldfish432/GodotGame` ("Commit the music and stings that a broad ignore rule left out").

The source ledger (`gamedev-evidence.json`) hashes a **pristine `git clone` of that commit**, not the working folder. The working folder also holds local-only files: raw MP3s, full-size generations and PRTS references.

## Isolated capture copy

All footage was recorded from a separate `git clone` of `111bf6e` in a scratch folder. **The real project and its save were never touched.** Saves were also never written: `PixelDisplay.persist_sessions = false` in the capture script.

The only differences from the commit:

1. **One added script,** `tests/capture_a2_film.gd`. The authored copy is in `capture/` beside this file. It is choreography, not shipped game code.
2. **Two window settings in `project.godot`:** `window/size/window_width_override=3840` and `window/size/window_height_override=2160`. The canvas stays 1280×720 with `stretch/mode="canvas_items"`, so 3840×2160 is an exact 3× and the UI renders natively at 4K. The 3D world still renders at 640×360 through `PixelDisplay` and is upscaled 6×, nearest-neighbour.
3. **One movie setting:** `[editor] movie_writer/mjpeg_quality=0.95`, which reduces MJPEG noise on the pixel art.

## Engine and command

Godot `4.7.2.stable.official.ed1daf0bf`, GL Compatibility, on Windows 11 with an NVIDIA GeForce RTX 4060 Laptop GPU.

```
Godot_v4.7.2-stable_win64_console.exe --path <clone> --script res://tests/capture_a2_film.gd \
  --rendering-method gl_compatibility --write-movie <clip>.avi --fixed-fps 30 -- <clip>
```

Each clip is Godot's own Movie Maker output: MJPEG video at 3840×2160 and 30 fps, plus the game's real mixed audio as PCM. It is the game's audio, not a dub. Every scripted decision is logged with its frame number in `capture/<clip>-inputs.jsonl`. Camp buttons are clicked at the button's own centre, mapped through `Viewport.get_screen_transform()`. A first 4K take used fixed 1280×720 coordinates, missed the button, and was discarded.

## Method

**Scripted input, not a human playtest.** The capture script drives the real main scene (`game/main.tscn`) through the same paths a player uses:

| Input | Path used |
|---|---|
| Movement | `Player.set_move_target` (the right-click path) |
| Walking | real `InputEventKey` W, A, S, D through `Input.parse_input_event` |
| Attacks | `Player.attack` (the left-click path) |
| Pause / resume | real Esc key events |
| Camp buttons | real `InputEventMouseButton` clicks |

There are **no disabled collisions and no direct HP or state writes.**

## Disclosed setup steps

| Clip | Setup |
|---|---|
| `hall` | None. It boots in the base and walks from the arrival point to the dispatch console and on toward the warehouse terminal. |
| `warehouse` | One teleport at frame 20, before recording anything meaningful, puts Lappland beside the warehouse door instead of a 26 s walk across the hall. From then on she walks. |
| `death` | `BaseState.unlock_camp("city", 30)` in memory stands in for walking floors 1–30. The contract starts at that camp, a real click on 继续 enters floor 31, and she fights there without dodging or drinking until killed (the recorded take, map seed 2026: settled by frame 349, about 9 s after the click). On floor 1 she out-heals the damage and does not die within 150 s. |
| `extract` | `BaseState.unlock_camp("mine", 10)` in memory, then a contract from that camp and a real click on 撤离. |
| `combat` | The contract starts with `GameManager.start_contract("city")`, the call the dispatch console makes. When a relic choice appears, the script takes the first offer through `GameManager.choose_build`. |

## Conforming to narration

Narration is the master clock. Each gameplay beat uses a contiguous window of its clip, trimmed to the action. Any shortfall is padded with a **labelled freeze-hold** on the last frame. **Nothing is sped up or slowed down.**

Two beats, B07 and B10, are `clock: source` / `audio_policy: preserve`. They play the clip's own audio with no narration over it, under a burned label: "SLICE AUDIO · no narration".

## A capture finding that changed the game

A 720p trial capture of the `extract` clip, recorded from a clean clone of `f770e26`, came out silent: −91 dB across the whole file. The music files were missing from git, because the ignore rule `music/` also matched `audio/music/`. Commit `111bf6e` fixes it. All final captures are from `111bf6e`. See `CHANGE-BRIEF.md`, "Audio revisions (observed while recording the film…)".

## Script versions

`capture/capture_a2_film.gd` is the final version. The `warehouse` and `combat` takes were recorded with an earlier version of it. That version did not yet have the seed argument, `click_button` or the `hall` clip, and neither clip uses any of those. Hashes of the raw AVIs are in `capture/raw-avi-sha256.json`. The AVIs themselves (2.0 GB) stay local.
