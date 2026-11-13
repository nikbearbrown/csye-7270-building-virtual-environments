# Capture record — claude-liam-walker-survival-shooting-a6-gamedev

Every game pixel in this film is real engine output. Two kinds are used, and every shot says which on screen.

## 1. Fixture frame strips (submitted)
- Source: `captures/` in the course repository (`assignment-6/walker-survival-shooting/captures/`), the strips cited in `TUNING.md`. Preview scenes (`godot/previews/*.tscn`) run windowed with Movie Maker, `--fixed-fps 30`, 2048 × 1152, fixed seed 7270 on the preview instance. Labelled **FIXTURE** in the film.
- Used: `landing_dust/r0` and `r1` (bright-fade, dark-fade, bright-retrigger), `light_dust/r0`, `r1`, `redesign`, `redesign-2` (dark).
- The film crops and scales them (never stretches) and adds labels (`scripts/make_figures.py`).
- **Difference tiles are computed analysis, not screenshots:** `|frame − reference| × 8` per pixel (max over RGB), then a 5-pixel max filter so the 1–2 px specks survive downscaling. Reference = frame 61 (lights on, dust hidden), or frame 9 for the lights-off frames. Labelled "computed" on screen.

## 2. This film's native-4K captures (new, scripted input)
- Tool: `capture/play_capture.gd` (copied into `res://film_capture/` of an isolated copy only). It instantiates the unmodified `res://base.tscn` inside a 3840 × 2160 `SubViewport` in a real window (not headless) and saves every rendered frame.
- Isolated copy: `git archive` of the course repository at `1828bb6b` (`fall-2026/zhe-l/assignment-6/walker-survival-shooting/godot`), imported once (`--headless --import`, exit 0, no error or warning lines). The course repository was not modified.
- Engine: `Godot Engine v4.7.2.stable.official.ed1daf0bf`, `D3D12 12_0 - Forward+ - Using Device #0: NVIDIA - NVIDIA GeForce RTX 5070 Ti Laptop GPU`.
- Command: `godot_console --path <copy> --rendering-driver d3d12 --fixed-fps 30 --script res://film_capture/play_capture.gd -- shot=<landing|lights> [cam=film] out=<dir>`. `--fixed-fps 30` = offline rendering at 30 fps with 60 physics ticks per second; **not evidence of real-time frame rate.**
- Input: keys sent with `Input.parse_input_event()` through the project's InputMap (the same method as the submitted state tests); one mouse-motion event pushed into the SubViewport to tilt the player camera 23° down. Everything is logged per physics tick to `inputs.jsonl`.

| Take | Camera | Script | Result | Used |
|---|---|---|---|---|
| `landing-run-01` | player | Space ×6, D held | 6 landings; camera walked into the right wall, dust at the frame edge | not used |
| `landing-run-02` | player, tilted 23° down | Space at ticks 60, 210, 340, 400, 460, 520; A held 330–540 | landed at ticks 118, 268, 398, 458, 518, 578 (exit 0); 351 frames | B02 still, B08 clip |
| `lights-run-01` | player | S held until inside the switch area | stopped by me: the area check never released S; a stray process kept running until killed | deleted |
| `lights-run-02` | player | S held 1 s, F at +60 and +180 ticks, pause, hide | lights_changed at ticks 242 (off) and 362 (on), exit 0; the player's body covers the view and the dust is not visible 8 m away | not used |
| `lights-film-01` | **film camera** added by the script at (0.8, 1.6, −1.2) looking at (0, 1.9, −3.7), fov 60 | same as lights-run-02 | lights_changed at 242 / 362; paused ticks 480–540; hidden 600–660; exit 0; 391 frames | B02 still, B16 clip |

Checks on `lights-film-01` (pixel comparison): paused frames 242 and 268 are identical (0 px differ); hidden frames 300 and 328 identical; shown-vs-hidden at frame 290 vs 310: 14,387 px differ, 492 by more than 10, max 42.

## 3. Clips in the film
- `media/B08.mp4` = `landing-run-02` frames 0–350 at 30 fps, then the same 351 frames again as a 2× crop of (480, 1060)–(2400, 2140), labelled "replay: 2x crop of the same frames". A landing counter from the logged ticks is burned in.
- `media/B16.mp4` = `lights-film-01` frames 0–390 with an inset `|frame − same view with the dust hidden| × 8` (reference f00315 while the lights are on, f00150 while off), labelled "computed".
- No retiming, trimming or slow motion. Any held final frame is labelled "held final frame".
