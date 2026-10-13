# Godot captures: INDEX

**What this is.** Real renders of ten Walker Godot projects, recorded 2026-10-09 on this Mac (Godot 4.7.2 stable, Apple M4 Pro) as evidence for the 3-film CSYE 7270 opening lecture series. All ten projects ran.
- **Captured:** 73 PNG screenshots and 11 MP4 clips. Every PNG was checked by eye, either directly or in a montage, and every clip through its contact sheet; none is black or blank.
- **Not done:** nothing is published, and no source project was modified.
- **Problems worth knowing before you cut:**
  - The rhythm game's timing is not certified.
  - The Dodge PNGs are portrait at 720x1080.
  - The Pong PNGs are 2133x1200.
  - Two clips are shorter than 8 s on purpose: 3D platformer 5.5 s, 3D kinematic 6.0 s.

## Method (same for every project)
1. **Scratch copy.** `rsync` of `books/<project>/godot` into `/private/tmp/claude-501/capture-work/<project>/godot`, excluding `.godot`, `evidence` and `youtube`. The source tree was only read.
2. **Copy-only edits.**
   - A capture autoload (`capture_driver.gd`) is registered in the copy's `project.godot`.
   - The window override is set to the recording size. This is 1920x1080, except Dodge (720x1080, portrait) and Pong (2134x1200, integer scaling).
   - walker-claude also sets the game's `test_mode` flag, whose only effect is no auto-pause when the window loses focus.
3. **Import** once headless, then **one windowed Movie Maker run**:
   `godot --path <copy> --write-movie frames/f.png --fixed-fps 30 --resolution WxH --always-on-top [scene] -- --plan=<plan.json> --out=<folder>`
   `--always-on-top` matters: one early run without it recorded frozen frames while the window was covered. Every `raw-log` ends with a distinct-frame count as a check.
4. **Input is real input.** The driver injects events with `Input.parse_input_event` (InputEventKey or InputEventAction), timed by frame or reacting to the observed game state: tracking the ball, seeking coins, steering to waypoints, hitting the next note. It never writes positions, velocities or scores. Every press and release is logged as an `INPUT f=<frame>` line.
5. **Outputs.**
   - Screenshots come from `get_viewport().get_texture().get_image()`.
   - Clips are encoded with ffmpeg as H.264 yuv420p, CRF 16, 30 fps, 1920x1080 (letterboxed or pillarboxed when needed).
   - Game audio is muxed as AAC only when the recording is not silent, and never for the rhythm game.
6. **Per-project folder files:**
   - `capture.sh`: the exact command.
   - `run_capture.sh` + `capture_driver.gd` + `plan.json`: the exact scripts used.
   - `raw-log.txt`: raw Godot output.
   - `contact-sheet-clip.png`: one frame per second of the clip.
   - `NOTES.md`: what is on screen and what input was scripted.
   - walker-claude has its own `capture.sh` + `capture_driver.gd`, and two raw logs.

Folder root: `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_conducting-series-evidence/godot-captures/`

---

## 1. walker-claude: Jumpman platformer starring Clawd + 18-animation gallery (DONE)
Notes: `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_conducting-series-evidence/godot-captures/walker-claude/NOTES.md`

| Capture (absolute path) | Resolution | Duration | Shows |
|---|---|---|---|
| `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_conducting-series-evidence/godot-captures/walker-claude/walker-claude-jumpman-gameplay.mp4` | 1920x1080 | 7.17 s, no audio | Title card, then Enter, then Clawd runs right with Right held and makes 5 Space jumps over the step, spikes, both gaps and the block. He reaches the flag and "Course complete. 5.6 seconds / 0 retries" appears. |
| `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_conducting-series-evidence/godot-captures/walker-claude/walker-claude-clawd-gallery.mp4` | 1920x1080 | 7.0 s, no audio | The gallery animating: page 1, then a Right-arrow tap, page 2, then another tap, page 3. |
| `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_conducting-series-evidence/godot-captures/walker-claude/01-title-screen.png` | 1920x1080 | still | "WALKER / JUMPMAN" title card "First steps. Real jumps." with the ENTER / START button. |
| `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_conducting-series-evidence/godot-captures/walker-claude/02-clawd-running.png` | 1920x1080 | still | Clawd running in "01 / GET MOVING". |
| `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_conducting-series-evidence/godot-captures/walker-claude/03-clawd-jumping-the-gap.png` | 1920x1080 | still | Clawd airborne over the first gap, under "02 / MIND THE GAP". |
| `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_conducting-series-evidence/godot-captures/walker-claude/04-level-complete.png` | 1920x1080 | still | "Course complete." card; Clawd at the FINISH flag. |
| `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_conducting-series-evidence/godot-captures/walker-claude/05-gallery-page-1.png` | 1920x1080 | still | Gallery 1/3: idle, bounce, wave, look, walk, run. |
| `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_conducting-series-evidence/godot-captures/walker-claude/06-gallery-page-2.png` | 1920x1080 | still | Gallery 2/3: think, type, sleep, error, nod, shake. |
| `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_conducting-series-evidence/godot-captures/walker-claude/07-gallery-page-3.png` | 1920x1080 | still | Gallery 3/3: dance, stretch, crouch, jump, spin, celebrate. |

Problems:
- The project's 1280x720 window override was raised to 1080p in the copy.
- On page 3, "spin" is caught edge-on: a real frame of the spin animation that reads as a thin sliver.
- The project has no audio.

## 2. walker-2d-dodge-the-creeps
Notes: `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_conducting-series-evidence/godot-captures/walker-2d-dodge-the-creeps/NOTES.md`

| Capture | Resolution | Duration | Shows |
|---|---|---|---|
| `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_conducting-series-evidence/godot-captures/walker-2d-dodge-the-creeps/walker-2d-dodge-the-creeps-clip.mp4` | 1920x1080 (game pillarboxed) | 8.0 s, game music | Enter, "Get Ready", then the player dodging creeps with scripted arrow-direction holds; score 0 to 5; survives the clip. |
| `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_conducting-series-evidence/godot-captures/walker-2d-dodge-the-creeps/01-title-screen.png` | 720x1080 | still | Title + Start button. |
| `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_conducting-series-evidence/godot-captures/walker-2d-dodge-the-creeps/02-get-ready.png` | 720x1080 | still | "Get Ready". |
| `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_conducting-series-evidence/godot-captures/walker-2d-dodge-the-creeps/03-dodging-creeps.png` | 720x1080 | still | Score 1, player moving among creeps. |
| `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_conducting-series-evidence/godot-captures/walker-2d-dodge-the-creeps/04-dodging-creeps-later.png` | 720x1080 | still | Score 4, more creeps. |
| `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_conducting-series-evidence/godot-captures/walker-2d-dodge-the-creeps/05-end-state.png` | 720x1080 | still | Score 6, "Game Over" (hit after the clip window). |

Problems:
- The PNGs are 720x1080: the portrait game's full area, below 1920 wide.
- The global RNG was seeded to 11, picked from 2 tries so the player survives the clip.

## 3. walker-pong
Notes: `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_conducting-series-evidence/godot-captures/walker-pong/NOTES.md`

| Capture | Resolution | Duration | Shows |
|---|---|---|---|
| `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_conducting-series-evidence/godot-captures/walker-pong/walker-pong-clip.mp4` | 1920x1080 | 8.0 s, no audio | A rally; both paddles moved by pressed up/down actions that track the ball. |
| `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_conducting-series-evidence/godot-captures/walker-pong/01-serve.png` | 2133x1200 | still | Serve toward the left paddle. |
| `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_conducting-series-evidence/godot-captures/walker-pong/02-left-paddle-return.png` | 2133x1200 | still | Ball at the left (cyan) paddle. |
| `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_conducting-series-evidence/godot-captures/walker-pong/03-rally.png` | 2133x1200 | still | Mid-rally near the right (magenta) paddle. |
| `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_conducting-series-evidence/godot-captures/walker-pong/04-rally-later.png` | 2133x1200 | still | Rally continuing. |
| `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_conducting-series-evidence/godot-captures/walker-pong/05-after-right-miss.png` | 2133x1200 | still | After a scripted right-paddle miss: the ball reset and back in play. |

Problems:
- The window is 2134x1200 because the project uses integer scaling; the clip is scaled to 1080p.
- The RNG was seeded to 7375, the project's own test seed.
- No sound in the recording.

## 4. walker-2d-kinematic-character
Notes: `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_conducting-series-evidence/godot-captures/walker-2d-kinematic-character/NOTES.md`

| Capture | Resolution | Duration | Shows |
|---|---|---|---|
| `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_conducting-series-evidence/godot-captures/walker-2d-kinematic-character/walker-2d-kinematic-character-clip.mp4` | 1920x1080 | 8.0 s, no audio | The player (small grey square) runs and jumps right, then left, across ramps and steps; moving platforms and the spinning circle animate. |
| `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_conducting-series-evidence/godot-captures/walker-2d-kinematic-character/01-start-riding-the-spinning-circle.png` | 1920x1080 | still | The player on top of the rotating circle. |
| `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_conducting-series-evidence/godot-captures/walker-2d-kinematic-character/02-airborne-moving-right.png` | 1920x1080 | still | The player mid-air, moving right. |
| `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_conducting-series-evidence/godot-captures/walker-2d-kinematic-character/03-on-the-right-ramp-moving-left.png` | 1920x1080 | still | The player on the right ramp. |
| `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_conducting-series-evidence/godot-captures/walker-2d-kinematic-character/04-by-the-left-steps.png` | 1920x1080 | still | The player at the bottom left, by the steps. |
| `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_conducting-series-evidence/godot-captures/walker-2d-kinematic-character/05-back-on-the-right-floor.png` | 1920x1080 | still | The player back on the right floor. |

Problems:
- The player sprite is small at 1080p.
- The princess goal was not reached; the route was not built for it.

## 5. walker-3d-platformer
Notes: `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_conducting-series-evidence/godot-captures/walker-3d-platformer/NOTES.md`

| Capture | Resolution | Duration | Shows |
|---|---|---|---|
| `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_conducting-series-evidence/godot-captures/walker-3d-platformer/walker-3d-platformer-clip.mp4` | 1920x1080 | **5.5 s**, game audio | The robot runs, jumps and shoots, hits a red enemy, and collects 2 coins. Input is pressed move/jump/shoot actions, steered toward coins in the manner of the project's feature_route.gd. |
| `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_conducting-series-evidence/godot-captures/walker-3d-platformer/01-start.png` | 1920x1080 | still | The robot at spawn. |
| `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_conducting-series-evidence/godot-captures/walker-3d-platformer/02-running-and-shooting.png` | 1920x1080 | still | Running and shooting; counter 0; enemy nearby. |
| `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_conducting-series-evidence/godot-captures/walker-3d-platformer/03-enemy-hit-first-coin.png` | 1920x1080 | still | Enemy hit; counter 1. |
| `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_conducting-series-evidence/godot-captures/walker-3d-platformer/04-coin-burst.png` | 1920x1080 | still | Coin burst; counter 2. |
| `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_conducting-series-evidence/godot-captures/walker-3d-platformer/05-two-coins.png` | 1920x1080 | still | Jumping; counter 2. |
| `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_conducting-series-evidence/godot-captures/walker-3d-platformer/06-lower-level-coin-ahead.png` | 1920x1080 | still | Lower level, coin ahead. |

Problems:
- The clip is cut at 5.5 s because the follow camera is then blocked by walls (the project's own CAPTURE.md reports the same).
- The audio peaks at 0 dBFS, as the project already notes.

## 6. walker-3d-particles
Notes: `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_conducting-series-evidence/godot-captures/walker-3d-particles/NOTES.md`

| Capture | Resolution | Duration | Shows |
|---|---|---|---|
| `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_conducting-series-evidence/godot-captures/walker-3d-particles/walker-3d-particles-clip.mp4` | 1920x1080 | 8.0 s, no audio | Next pressed every 2 s: Explosion, then Fire, then Smoke, then Attractor; the camera glides between them. |
| `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_conducting-series-evidence/godot-captures/walker-3d-particles/01-CPUParticlesForceField.png` … `14-GPUParticlesCollisionHeightfield.png` (14 files: 01 CPUParticlesForceField, 02 CPUParticlesExplosion, 03 GPUParticlesFire, 04 GPUParticlesSmoke, 05 GPUParticlesAttractor, 06 GPUParticlesTurbulence, 07 GPUParticlesCollision, 08 GPUParticlesCollisionGlobalCoords, 09 GPUParticles3DFoam, 10 GPUParticlesTrails, 11 GPUParticlesSubemitterAtEnd, 12 GPUParticlesSubemitterOnCollision, 13 GPUParticlesCollisionSDF, 14 GPUParticlesCollisionHeightfield) | 1920x1080 | stills | Every tester in the showcase, each with its on-screen name label. |

Problems: none.

## 7. walker-3d-lights-and-shadows
Notes: `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_conducting-series-evidence/godot-captures/walker-3d-lights-and-shadows/NOTES.md`

| Capture | Resolution | Duration | Shows |
|---|---|---|---|
| `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_conducting-series-evidence/godot-captures/walker-3d-lights-and-shadows/walker-3d-lights-and-shadows-clip.mp4` | 1920x1080 | 8.0 s, no audio | Omni With Shadows, then PCSS Shadows, then Projector, then Attenuation, with animated lights. |
| `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_conducting-series-evidence/godot-captures/walker-3d-lights-and-shadows/01-OmniLightNoShadows.png` … `15-AreaLightShapes.png` (15 files: omni ×5, spot ×5, area ×5; names in NOTES.md) | 1920x1080 | stills | Every light tester: torus and cones under each light type, shadow mode and projector. |

Problems: none.

## 8. walker-audio-rhythm-game (visual only)
Notes: `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_conducting-series-evidence/godot-captures/walker-audio-rhythm-game/NOTES.md`

| Capture | Resolution | Duration | Shows |
|---|---|---|---|
| `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_conducting-series-evidence/godot-captures/walker-audio-rhythm-game/walker-audio-rhythm-game-clip.mp4` | 1920x1080 | 8.0 s, **no audio by design** | Notes falling to the guide; Space pressed by a driver that reads the game's own note delta; Perfect/Good/Miss counters and the error graph updating; one deliberate miss. |
| `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_conducting-series-evidence/godot-captures/walker-audio-rhythm-game/01-start-screen-settings-and-guide.png` | 1920x1080 | still | Full UI before the first note. |
| `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_conducting-series-evidence/godot-captures/walker-audio-rhythm-game/02-first-notes-approaching-guide.png` | 1920x1080 | still | First notes falling. |
| `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_conducting-series-evidence/godot-captures/walker-audio-rhythm-game/03-after-deliberate-miss-stats.png` | 1920x1080 | still | "Miss..." labels; Perfect 6 / Miss 1. |
| `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_conducting-series-evidence/godot-captures/walker-audio-rhythm-game/04-perfect-hits-error-graph.png` | 1920x1080 | still | Perfect 14 / Good 2 / Miss 2; error graph dots. |

Problems:
- **Timing is not certified.** The conductor mixes the wall clock with the audio clock, and Movie Maker runs on fixed simulated time. Judgments vary slightly from take to take, and the +36 ms "Late" average is an artefact of the capture method. Use it for what the screen looks like, not for timing claims.
- The startup log has a harmless missing-icon UID error.

## 9. walker-2d-finite-state-machine
Notes: `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_conducting-series-evidence/godot-captures/walker-2d-finite-state-machine/NOTES.md`

| Capture | Resolution | Duration | Shows |
|---|---|---|---|
| `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_conducting-series-evidence/godot-captures/walker-2d-finite-state-machine/walker-2d-finite-state-machine-clip.mp4` | 1920x1080 | 8.0 s, no audio | Walk, sprint, move, jump, a three-hit sword combo and three bullets. The state label (IDLE / MOVE / ATTACK) and the STATESTACK pushdown panel update live. |
| `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_conducting-series-evidence/godot-captures/walker-2d-finite-state-machine/01-idle-state.png` | 1920x1080 | still | IDLE; stack "0 Idle". |
| `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_conducting-series-evidence/godot-captures/walker-2d-finite-state-machine/02-move-state.png` | 1920x1080 | still | MOVE; stack "0 Move". |
| `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_conducting-series-evidence/godot-captures/walker-2d-finite-state-machine/03-run-sprint.png` | 1920x1080 | still | Sprinting (still the MOVE state). |
| `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_conducting-series-evidence/godot-captures/walker-2d-finite-state-machine/04-jump-state-stack.png` | 1920x1080 | still | Jump pushed over Idle: "0 Jump / 1 Idle". |
| `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_conducting-series-evidence/godot-captures/walker-2d-finite-state-machine/05-attack-combo.png` | 1920x1080 | still | ATTACK with sword swing; "0 Attack / 1 Idle". |
| `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_conducting-series-evidence/godot-captures/walker-2d-finite-state-machine/06-firing-bullets.png` | 1920x1080 | still | A bullet leaving the player. |
| `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_conducting-series-evidence/godot-captures/walker-2d-finite-state-machine/07-stagger-after-simulated-damage.png` | 1920x1080 | still | STAGGER (orange); "0 Stagger / 1 Idle". |

Problems:
- A first take walked the player off-screen (the demo has no walls) and was discarded.
- The "Explanations" text is not visible in these frames.

## 10. walker-3d-kinematic-character
Notes: `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_conducting-series-evidence/godot-captures/walker-3d-kinematic-character/NOTES.md`

| Capture | Resolution | Duration | Shows |
|---|---|---|---|
| `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_conducting-series-evidence/godot-captures/walker-3d-kinematic-character/walker-3d-kinematic-character-clip.mp4` | 1920x1080 | **6.0 s**, no audio | Cubio walks to the steps and jumps up two levels to the upper platform, steered by pressed actions toward the project's own route waypoints. |
| `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_conducting-series-evidence/godot-captures/walker-3d-kinematic-character/01-start.png` | 1920x1080 | still | Cubio on the tiled floor. |
| `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_conducting-series-evidence/godot-captures/walker-3d-kinematic-character/02-walking-to-the-steps.png` | 1920x1080 | still | Walking to the steps. |
| `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_conducting-series-evidence/godot-captures/walker-3d-kinematic-character/03-jumping-up-a-step.png` | 1920x1080 | still | On the first step. |
| `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_conducting-series-evidence/godot-captures/walker-3d-kinematic-character/04-jumping-to-the-top-step.png` | 1920x1080 | still | Mid-jump to the upper level. |
| `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_conducting-series-evidence/godot-captures/walker-3d-kinematic-character/05-on-the-upper-level.png` | 1920x1080 | still | On the upper level. |

Problems:
- A longer 10-waypoint perimeter take failed: Cubio fell off at waypoint 4, because 30 Hz steering is coarser than the project's 120 Hz test. That take was discarded; only the verified 3-waypoint climb is delivered.
- The last ~2 s of the clip are Cubio standing still.

---

## Housekeeping
- **Scratch work:** `/private/tmp/claude-501/capture-work/`. It holds the copies, the raw PNG frame sequences and the plans; it can be deleted.
- **Shared scripts:** the generic runner and driver live in `/private/tmp/claude-501/capture-work/_shared/`. Their copies sit beside each capture.
- **Processes:** no Godot process from this work is left running.
