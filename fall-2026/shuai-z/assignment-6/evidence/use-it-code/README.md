# Use It — code-driven editor evidence

> **Note added by Claude Code on 2026-11-06, at my request.** The PNG screenshots in this folder are half-size copies, made with a Lanczos resize: game frames are 640 × 360 and editor screenshots 1710 × 1002. The full-size originals are not in the repository; they stay on this machine in `originals/`, which `.gitignore` excludes. Pixel coordinates and counts in this README, `pixel-checks.json` and `snapshots.json` refer to the originals. The pairs this README calls pixel-identical (`50`/`51`, `53`/`54`, `supplement/80`/`81`) are still identical after the reduction.

Measured on 2026-11-06 from source commit `d60fb037` using Godot 4.7.2, GL Compatibility (OpenGL 4.1 on Metal), Apple M3, and a standalone 1280 × 720 game window launched by the Godot editor.

## Method and scope

The original `game/` was copied to `/tmp/a6-use-it/game`. A temporary editor plugin used `EditorInterface.play_custom_scene()` to start an instrumentation scene, which instantiated the original `Main` and made it the current scene. The plugin started the actual Visual Profiler and read its and Monitors' live `Tree` cells. The original project's 168 non-cache files still match `source-hashes.json`. No original game source, generated shader, project setting, or report was edited.

Fixtures place Rudy near each test location and reset his velocity/camera position; gameplay then uses the existing input actions and effect driver. The sword comes from walking into the real pickup. F9 is delivered as an `InputEventKey`; the runtime log confirms vsync off and then restored on. The complete/restart case uses the real portal and real scene reload. This is targeted scenario coverage, not a continuous human traversal of the level.

The temporary plugin is enabled only in the scratch project's `project.godot`; the source project is unchanged. The scripts and plugin configuration here preserve the instruments actually run. To reproduce, copy the game to a scratch project, place `use_it_runner.gd` and `.tscn` at its root, place `editor_run.gd` and `plugin.cfg` together under an editor addon, enable that addon in the scratch project, disable embedded game mode for that project, and launch its editor. Adjust the scripts' absolute `OUT` and phase-file paths for another machine. The `supplement/` and `detail/` scripts are follow-up runs with the same source game.

## Performance

Each case has a 1.5 s warm-up and a 5 s measurement. The editor's live cells are sampled every 0.5 s; `summary.json` discards the first three records of each case and takes the median of the remaining displayed values. Rows can repeat between engine monitor refreshes, as they do when reading the panel by eye. Screenshots of the profiler were taken during warm-up, outside the timed 5 s game-frame count.

| Live editor metric | A off, idle | A heavy, repeated slash | B off, idle | B heavy, run/turn |
|---|---:|---:|---:|---:|
| Visual Profiler GPU column | 0.0 ms | 0.0 ms | 0.0 ms | 0.0 ms |
| Monitors → Time → FPS, median | 438 | 239 | 357 | 311 |
| FPS range in retained editor samples | 413–504 | 222–261 | 271–395 | 284–321 |
| Monitors → Time → Process, displayed median | 11.80 ms | 11.69 ms | 10.94 ms | 9.41 ms |
| Monitors → Raster → Total Draw Calls, displayed median | 9 | 12 | 9 | 10 |
| Independently counted game frames / elapsed wall time | 427.1 FPS | 229.2 FPS | 347.8 FPS | 296.9 FPS |

The actual monitor category in this editor is **Raster**, not Rendering. Process is reported as displayed; it is not GPU time and must not be substituted into the GPU budget. Independently counted FPS and the panel's periodically refreshed FPS use different sampling windows.

`DisplayServer.screen_get_refresh_rate()` reported 60 Hz. Every retained FPS reading exceeded that rate; these measurements were not capped at the reported refresh rate. F9 restored vsync after measurement (`VSYNC_RESTORED_MODE 1` in `runtime.log`). All sampled GPU cells, including Update GPUParticles and Render Viewports, read 0.0 ms; the runtime viewport GPU-time API also returned zero. **The 0.25 ms per-effect GPU budget cannot be evaluated on these readings. Zero is not evidence of zero cost or a pass.** FPS varied substantially even between the two idle baselines, so the differences should not be presented as isolated particle GPU costs.

A heavy uses a fresh slash every 20 physics ticks (about 3/s); two bursts were alive on 112/300 timed ticks, with a maximum of two. B runs and reverses between x 2600 and 2890; dust emitted on 251/300 ticks, with the remaining ticks including the game's turn holds. These match the requested repeated-slash and back-and-forth scenarios, but neither is a synthetic constant-peak workload.

Evidence: [raw editor cells](editor-profiler.json), [runtime samples](performance.json), [summary](summary.json), [runtime log](runtime.log), [editor log](editor.log). Profiler screenshots: [A off](01_A_off_editor.png), [A heavy](02_A_heavy_editor.png), [B off](03_B_off_editor.png), [B heavy](04_B_heavy_editor.png).

## Image and state observations

| Requested check | Automated/image observation | Evidence |
|---|---|---|
| Repeated slashes and overlap | Repeated input produced bursts; two distinct burst nodes coexist on the second cut. The later and earlier particles are visible in the captured overlap frame. | `20_slash_first.png`, `21_slash_overlap.png`, runtime samples |
| Slash left | The visible spray is on the left of the sword/character, matching the facing. | `22_left_slash.png` |
| Goblin disappears while sparks remain | Confirmed after the goblin's squash animation ends and it becomes hidden. In a frozen scene, hiding only the burst changes 133 pixels, up to 62/255 in one channel, within x 736–787, y 479–560. This distinguishes visible residual particles from mere node existence. | `detail/90_goblin_gone_with_sparks.png`, `detail/91_same_frame_without_sparks.png`, `pixel-checks.json` |
| Dust starts/stops/jumps/lands | A visible trail accompanies running; the emitter stops after release and in the air, existing dust fades, and emission resumes on landing. | `30_dust_running.png` through `34_dust_landing.png`, `snapshots.json` |
| Size | In the 1280 × 720 captures, sparks occupy a short region ahead of the sword and dust forms a low trail behind the feet without covering Rudy. Whether this size feels appropriate remains a human judgement. | `30_dust_running.png`, `supplement/83_sky_visible.png` |
| Movement/jump/slash feel | Actions work in the exercised paths; source hashes are unchanged. This does not establish subjective control feel relative to an earlier version. | `source-hashes.json`; human confirmation still needed |
| Bright sky / dark pit / dust background | Sparks are distinguishable against the sky, and the flash/core is visible against the dark pit. Dust is distinguishable against the lower wheat/grass. Jumping over the pit keeps sparks against sky, so the dark-background supplement instead lets Rudy fall into the pit and slash before the kill line. | `supplement/83_sky_visible.png`, `supplement/88_dark_pit_sparks.png`, `30_dust_running.png` |
| Screen edges | Sampled left/right frames show normal clipping or continued particle visibility, with no observed whole-burst disappearance while it should still be visible. Dust is visible near both sides. The pre-portal location is not the true right edge: a supplement jumped over the portal trigger and ran to x 7653 without completing; a detail fixture at x 7490 captured the spray still inside the right edge. This is sampled-frame evidence, not an exhaustive continuous-video culling check. | `40_left_start.png`–`43_left_dust.png`, `supplement/85_right_edge_dust.png`, `detail/92_right_edge_early.png`–`94_right_edge_late.png` |
| Dust and sparks pause | Visible dust screenshots 0.6 s apart are pixel-identical. Visible sparks screenshots 0.7 s apart are pixel-identical. They change again after resuming. | `50_dust_paused_a.png`, `51_dust_paused_b.png`, `supplement/80_sparks_visible_paused_a.png`, `supplement/81_sparks_visible_paused_b.png`, `pixel-checks.json` |
| Invulnerability | Rudy's Look alpha changes between 0.35 and 1.0 while dust's own alpha remains 1.0 and visible dust persists. No synchronised dust flashing was observed in the samples. | `60_hurt_run_0.png`–`60_hurt_run_3.png`, `snapshots.json` |
| Fall/respawn with direction held | On the respawn snapshot dust is not emitting; after control returns it emits at Rudy's new location. The first snapshot is covered by the game's fade, and the later visible frame shows no trail spanning pit to checkpoint. | `64_fall_start.png`–`66_respawn_running.png` |
| Startup and completion/restart | Captured title/early-play frames and real portal/reload frames have no visible dust or sparks while idle; recorded emitter/burst states agree. | `10_title_first.png`–`13_play_idle.png`, `70_complete.png`–`72_restart_settled.png` |

The main run's first spark-pause capture was too early to show a developed particle spray; use the **supplement** pair, not the main `53/54` pair, for that conclusion. Likewise, use the frozen `detail/90/91` pair for the goblin-disappearance conclusion, not the earlier squash-frame image.

Contact sheets `contact-1.jpg` through `contact-5.jpg` are reduced previews of the main run; use original PNGs for visibility judgements. `snapshots.json` in each run records image dimensions and the relevant game state.

## Human judgement and the documented disagreement

No new first-person human judgement is claimed. Human approval of perceived size, control feel, and the course's HUMAN CHECK remains outstanding. A disagreement already recorded in `../../TUNING.md`, Effect B r2, is available without inventing one: Claude reported a continuous band and that both measured targets were met; the user's verdict was **“尘土扬起的角度还可以高一些，现在基本都只是在地面上”**. This feedback led to r3. It is a prior recorded judgement, not a newly elicited verdict on this run.

## Limitations and excluded attempts

An initial embedded-window attempt never entered play and was discarded. A later attempt using `--editor --script` crashed the editor and was also excluded from the reported measurements. The successful runs use a normal editor plugin. The main successful run logged two instrumentation-only `Lambda capture at index 0 was freed` errors while waiting for the old Main to be replaced on reload; the resulting new Main and clean idle state were nevertheless captured. The supplement and detail runs have no such errors. No `SCRIPT ERROR` or `SHADER ERROR` appears in the successful runtime logs. No existing test or mutation was rerun for this evidence capture; the earlier report's test counts remain earlier-run evidence.

The internal editor control approach was informed by Godot's [Visual Profiler implementation](https://github.com/godotengine/godot/blob/master/editor/debugger/editor_visual_profiler.cpp) and [game view implementation](https://github.com/godotengine/godot/blob/master/editor/run/game_view_plugin.cpp); all reported panel names, values and game behaviour were checked against the installed 4.7.2 runtime rather than assumed from that source version.
