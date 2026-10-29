# walker-rudy — shaders and materials (Assignment 5)

CSYE 7270, Assignment 5: *Shaders, Materials, and the Godot Shading Language*. By Shuai Zhang.

**How this README was made:** Claude Code (Claude Opus 5.5) drafted it on 2026-10-29 at my request, from this folder's files and records. I reviewed it the same day, before it was committed ("审完了", "I've finished the review").

walker-rudy is my 2D side-scroller from Assignment 2: Rudy crosses Level 1, Harvest Fields, past spikes, goblins and a waystone checkpoint to the teleport circle. This assignment adds one layer, in two places:

- **In the 2D game, a shader driven from code.** While Rudy is invulnerable, the 1.2 s after a hit or a respawn in which hits are ignored, the hearts in the corner tint toward the lit waystone's pale blue, strongest when the window opens and fading as it runs out.
- **In the Assignment 3 props scene, a textured shader.** The waystone's Stone surface and the teleport circle's DarkStone surface get one weathered-stone shader with Poly Haven's Rock 01 textures, through two materials with different values.

The game is 2D, so the textured shader, its materials, the hint experiment and the generated shader are in the 3D scene, as the assignment allows.

| | |
|---|---|
| Starting point | Tag `a3`. `game/` is [`../assignment-2/game/`](../assignment-2/game/) and `godot/` is [`../assignment-3/godot/`](../assignment-3/godot/), both copied unchanged in `84658acf`. Neither `project.godot` has changed since. No change of game |
| Godot | 4.7.2.stable.official.ed1daf0bf, the standard build |
| Renderers | `game/`: GL Compatibility (`game/project.godot` lines 95–96). `godot/`: Forward+ (`godot/project.godot` line 16) |
| Machine | macOS 15.1, Apple M3. Not tested on any other system |
| State the shader communicates | Rudy's invulnerability window (`game/content/rudy/rudy.gd`, `_invulnerable_left` and `invulnerable_time`) |
| Object given the textured shader | The waystone's Stone surface and the teleport circle's DarkStone surface, in `godot/scenes/props_room.tscn` |
| Textures | Rock 01 by Rob Tuytel, [Poly Haven](https://polyhaven.com/a/rock_01), CC0; credits in [godot/assets/textures/rock_01/ATTRIBUTION.md](godot/assets/textures/rock_01/ATTRIBUTION.md). The hint experiment's grey strip is written by code |
| Assistance | Claude Code (Claude Opus 5.5), in the desktop app and as scoped `claude -p` sessions. I wrote the three shaders by hand. Who did what: [SOURCES.md](SOURCES.md) and [FRICTIONAL.md](FRICTIONAL.md) |
| Final film | *Two Shaders for Walker Rudy.* (Brutalist `godot-gamedev`, `walker` modifier; 12:39, 3840×2160), file `claude-liam-walker-rudy-shaders.mp4`, SHA-256 `a1bd8a3c5c20f4ab63d14884f6cf0ab5ca977fc59ff1c030d50dd238ba6d42fa`. It shows the source at `a2a3a77`; the commit that adds the film's folder (`5c89fb46`) changes nothing in `game/` or `godot/`. Course media: [claude-liam-walker-rudy-shaders.mp4 on Google Drive](https://drive.google.com/file/d/1Cx9urHkUlUhYBZ6EGtCq6PX-BPRnuqhX/view?usp=drive_link). The MP4 is not in git; its beat sheet, prompts, evidence and checks are in [youtube/claude-liam-walker-rudy-shaders/](youtube/claude-liam-walker-rudy-shaders/) |

## Run it

In a fresh clone, import each project once, from this folder:

```bash
godot --headless --path game --import
godot --headless --path godot --import
```

`godot` is the Godot 4.7.2 binary (on macOS, `/Applications/Godot.app/Contents/MacOS/Godot`).

**The game.** Open `game/project.godot` in Godot 4.7.2 and press F5, or run `godot --path game`. The main scene is `res://app/main.tscn`. To see the tint, walk Rudy right into the first spikes. The hearts pale toward blue and fade back over about 1.2 s.

**The props scene.** Open `godot/project.godot` and press F5, or run `godot --path godot`. The main scene is `res://scenes/props_room.tscn`, with the textured waystone and circle. The hint experiment is `res://scenes/hint_experiment.tscn`; open it in the editor, or run `godot --path godot res://scenes/hint_experiment.tscn`.

## Controls

The game's, unchanged from Assignment 2:

- A/D or ←/→ move. On the ground, a tap of the other direction turns Rudy on the spot; hold it to move.
- Space, W or ↑ jump.
- J or X slash, once Rudy has the sword.
- Enter on the title starts play; on the end card it plays the level again.
- Esc pauses and resumes. While paused, the tint holds its value.
- M mutes the music and N the sound effects.
- F1 shows or hides the debug line.

The props scene has no controls; it shows its own camera.

## Tests

Run every test through the course's wrapper, from this folder: `scripts/run-test.sh <game|godot> <test-file> <fps>`. It pins the frame rate and times out after 120 s; status 124 means a hang. It writes `logs/<project>_<test>_<fps>fps.log`, and fails on any `SHADER ERROR` or `SCRIPT ERROR` line whatever Godot's exit code. Godot exits 0 even after a shader error, so read the log.

| Command | Expected | What it checks |
|---|---|---|
| `scripts/run-test.sh game checks.tscn 60` | 141 `PASS`, `all checks passed` | Assignment 2's checks, unchanged |
| `scripts/run-test.sh game invulnerable_tint_checks.tscn 30` (and `60`, `144`) | 15 `PASS`, `all checks passed` at each rate | The tint shader's uniforms and defaults, where its material is, and the driver through real input: begin, fade, end, duration, retrigger, time scale, pause, reload |
| `scripts/run-test.sh godot check_props.gd 60` | 44 `ok`, `PASS: 0 failed check(s)` | Assignment 3's checks, unchanged |
| `scripts/run-test.sh godot test_materials.gd 60` | 125 `PASS`, `all checks passed` | Both 3D shaders' uniforms and sampler hints, the materials, the import settings, where each material is, the normal maps' curl ratios |
| `scripts/run-test.sh godot calibrate_normal_map_check.gd 60` | 4 `PASS`, `all checks passed` | The curl check on Rock 01's OpenGL/DirectX pair, and the 0.5 threshold |

The results, the mutations that fail these tests, and what a headless run cannot show are in [TEST-REPORT.md](TEST-REPORT.md).

The windowed captures open a window, so they are not headless tests. Each script's first comment lines give its command:

- `game/tests/capture_tint.tscn`: the hearts at controlled values;
- `godot/tests/capture_hint.gd`: the hint experiment;
- `godot/tests/capture_sweep.gd`: the interface sweep and the two materials;
- `godot/tests/capture_hint_vs_os.gd`: the engine capture against an OS screenshot.

## What this assignment added

- **The specification, before any shader.** [CHANGE-BRIEF.md](CHANGE-BRIEF.md), revision 1 (`fc9cd523`), holds the state, the colour line, the uniform table, twelve observable rules, the boundaries, the evidence split, the predicted pixel values, the hint experiment's predictions, the material plan, predicted failures and short answers. Revisions 2–4 are dated at the end.
- **Context for the agent.** [CLAUDE.md](CLAUDE.md). A scoped `claude -p` session drafted it, committed unedited (`dfeca3fb`). The review and its corrections were committed apart from that draft (`c095e9de`): Claude did them in our conversation, with two headless probes, and I approved them.
- **The shader from code.** I wrote `game/shaders/invulnerable_tint.gdshader` by hand and committed it alone (`ae0a3757`).
  - The driver is `game/ui/hud.gd` `_tint_hearts()`, with the material `game/ui/hearts_tint.tres` on `Hud/Hearts` in `game/ui/hud.tscn`.
  - Its test is `game/tests/invulnerable_tint_checks.gd`.
  - The driver and the test were written by a scoped session (`bd797945`). `rudy.gd` is unchanged.
- **The textured shader and its materials.** I wrote `godot/shaders/weathered_stone.gdshader` by hand (`a87a18be`).
  - Its materials are `godot/materials/waystone_stone.tres` and `circle_darkstone.tres`, set as surface overrides in `props_room.tscn`.
  - The Rock 01 textures are in `godot/assets/textures/rock_01/`, each with explicit import settings in its `.import` file.
- **The hint experiment.** I wrote `godot/shaders/hint_experiment.gdshader` by hand (`9481663a`). Its two materials are `godot/materials/hint_source_color.tres` and `hint_plain.tres`, in the scene `godot/scenes/hint_experiment.tscn`. The grey strip is written by `godot/tools/write_grey_strip.gd`.
- **The audit.** [godot/MATERIALS.md](godot/MATERIALS.md) and `godot/tests/test_materials.gd`, from a scoped session (`cd1e71a3`), then reviewed (`3b1084a6`).
- **The language.** `godot/shaders/standard_generated.gdshader` is the shader Godot generated from a StandardMaterial3D, annotated by me (`fe795908`). I wrote [LANGUAGE-NOTES.md](LANGUAGE-NOTES.md).
- **Records.**
  - [TEST-REPORT.md](TEST-REPORT.md), [FRICTIONAL.md](FRICTIONAL.md) and [SOURCES.md](SOURCES.md).
  - The scoped sessions' prompts and transcripts are in [sessions/](sessions/), labelled in [sessions/README.md](sessions/README.md). One transcript is over 1 MB, so it is a labelled excerpt.
  - The logs cited are in [logs/](logs/), the captures in [evidence/use-it/](evidence/use-it/), and the headless probes in [evidence/headless-probe/](evidence/headless-probe/).
- **The film.** It is linked in the table above.

## Known limitations

- **Two controls cannot be judged by eye under the scene's own light.** `normal_strength` and `roughness_offset` move the waystone's pixels by under 3 steps on average across their full ranges. The normal map is gentle, the roughness map is nearly flat, and the scene's Sun cannot put a highlight on the stone's sides (TEST-REPORT.md §7). The brief keeps that lighting, so I have not tried another light.
- **Some of the looking was Claude's.** Claude judged the interface sweep, the two-materials check and the OS-screenshot comparison at my request, and I reviewed the results afterwards. My own eyes were on the hearts in play and their fade-in, the hint scene, and the materials in the editor (TEST-REPORT.md §14).
- **The hearts' fade-in with the tint was not captured.** I checked it by eye only.
- **Two things are unexplained or unconfirmed.**
  - At `tint_amount` 0.0, one edge pixel of the hearts differs from the no-material capture by one step in green. The reason is unknown.
  - Why the hearts need no sRGB step comes from the course chapter's reading of the renderer's source, not from a check in this folder. The captures match the predictions exactly (CLAUDE.md, Unconfirmed).
- **The roughness map loses precision on import.** It is 16-bit, but the brief's VRAM compression imports it as 8-bit DXT1, and the shader reads one channel of three (MATERIALS.md, finding 1).
- **An unused texture is imported.** `rock_01_nor_dx_1k.png`, the curl check's calibration file, is imported though no material uses it. It would ship in an export unless excluded (MATERIALS.md, finding 2).
- **The props scene is separate.** It is still a separate Godot project, not connected to the 2D game.
- **Tested on one machine by one person.** Everything ran on macOS 15.1 on an Apple M3, and nobody else has played the game or looked at the scenes.

## Files

| Path | What |
|---|---|
| `game/` | The 2D game: the tint shader in `shaders/`, its driver and material in `ui/`, and its tests and capture in `tests/` |
| `godot/` | The props scene: the three shaders in `shaders/`, four materials in `materials/`, the textures and grey strip in `assets/`, both scenes, the tests in `tests/` and the scene tools in `tools/` |
| `scripts/run-test.sh` | The course's test wrapper, changed for two projects (changes listed at its top) |
| `scripts/excerpt_transcript.py` | Makes the labelled transcript excerpt |
| `CHANGE-BRIEF.md`, `CLAUDE.md`, `godot/MATERIALS.md`, `LANGUAGE-NOTES.md`, `TEST-REPORT.md`, `FRICTIONAL.md`, `SOURCES.md` | The specification, the agent's context, the audit, the language notes, the results, the honest log, the credits and who did what |
| `sessions/` | Prompts and transcripts of the scoped `claude -p` sessions |
| `logs/` | Every log the records cite |
| `evidence/` | The windowed captures (`use-it/`) and the headless probes (`headless-probe/`) |
| `youtube/claude-liam-walker-rudy-shaders/` | The film's beat sheet, prompts, fact check, capture drivers and logs, ledgers, stills and build tools (the MP4 is not in git) |
