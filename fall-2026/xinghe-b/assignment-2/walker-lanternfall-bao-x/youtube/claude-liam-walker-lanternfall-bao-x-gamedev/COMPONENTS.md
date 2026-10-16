# COMPONENTS — what the film takes apart

Game: `walker-lanternfall-bao-x/godot` at **8a6f988** · 75 authored files (no `.godot/`, no `.uid`): 72 tied to a component below, 3 excluded with reasons (`gamedev-evidence.json`). Code panels are verbatim excerpts; each is followed by the beat that shows its result.

| Component | Files | Data in → what changes → what the player sees | Why this design · the trade-off | Code → result |
|---|---|---|---|---|
| **Session & state machine** | `game/session.gd`, `game/game_state.gd`, `game/main.tscn`, `project.godot` | one `tick()` per physics frame at 60 Hz; input actions → MENU / PLAYING / LEVELUP / PAUSED / WON / LOST → everything else reacts to `state.changed` | a single source of truth makes runs reproducible from a seed (the film's takes depend on it) · every system must be driven from the tick, never from wall time | B23 → B24 (input → mute); B16 → B17 (weapons in the tick) |
| **Courier** | `features/player/player.gd` | input axis → position (+ knockback), facing with a 0.1 dead-zone, i-frames, `choose_pose()` → `_draw()` cuts one 32 × 32 frame from `pc_sheet.png` at `SPRITE_ORIGIN (16, 23)`, mirrored for left | right-facing art only, code flips it (half the frames to generate); hurtbox centred on the generated torso · an r = 10 hurtbox now also reaches the lower lamp | B07 → B08, B09 → B10, B21 → B22 |
| **Character sprite asset (ART-PC-01)** | `assets/art/pc_sheet.png(.import)`, `palettes.json`, `assets/art/manifest.json`, `features/art.gd` | 24 FLUX runs → 10 accepted frames → keyed, mirrored, lamp 12 px, Lab palette lock, 4× supersample → one 320 × 32 sheet; `art.gd` loads it or falls back to placeholders | per-pose prompts after the 3D-looking first batch; palette lock keeps every frame on 5 colours · at 32 px detail is lost (satchel becomes a blob) | B04–B06 (trace) → B07 → B08 |
| **Other generated art** | 13 PNGs + `.import` (moth, wraith, stall, cart, post, crates, puddle, leaves, ground tile, beam, orbit moth, sunflare, gem) | drawn by their owners; sprite boxes and solid boxes measured from the PNGs | measured boxes mean "what you hit / bump into is what you see" · the wraith has the lowest contrast on the ground (0.03) | seen throughout; B17 (moth box), B22 (stall box) |
| **Weapons & hit tests** | `features/weapons/beam_shot.gd`, `weapon_fx.gd`, `features/enemies/enemy.gd` | each tick a bolt moves and is tested as a 14 px segment against each monster's visible box (`touches_segment`); pierce decrements; moths orbit and test `touches()` | the change from a centre circle (10 px for a moth) to the visible box answered Bao's playtest · sampling every 2 px costs a little per bolt per enemy | B16 → B17 |
| **Progression & evolution** | `features/progression/progression.gd` | XP → level-up queue → three cards from a seeded shuffle; when beam and moths are both 3/3 the Sunflare card is placed first | the fusion can't be missed once earned · the offer is less random once it is due | B18 → B19 |
| **Audio** | `audio/audio_bus.gd`, `audio/sfx_gate.gd`, 7 WAV + 2 OGG (+ `.import`), `assets/manifest.json` | session signals → `sfx(id)` asks the pure gate (cooldown, voice cap, once-per-run on the tick clock) → AudioStreamPlayers; `state.changed` → low-pass / duck / fade / stinger; mute keys flip bus flags | sound only listens: a test proves a silent run ends in the same state · a cooldown can merge genuinely separate events (pickups merge inside a 300 ms voice slot) | B11 → B12, B13 → B14, B23 → B24; heard in B03, B15, B20, B25, B26 |
| **World & camera** | `features/world/ground.gd`, `camera_fx.gd` | fixed-seed layout of 14 clusters; solid boxes; `push_out` moves the courier's circle out of a box by the shortest way; camera push-in, hit tilt, Sunflare zoom-out, fog lift | the same map every run, with or without textures · monsters ignore the boxes, so props can corner you but never shelter you | B21 → B22; B19 (zoom-out) |
| **Pacing** | `features/enemies/spawner.gd`, `features/pickups/gem.gd`, `features/tuning.gd` | six 30-second spawn phases, HP × (1 + 0.5 per whole minute), gems pulled inside the pickup radius | numbers live in one table · balance is tuned against Bao's play and scripted bots only | B12 (dense wave, counted) |
| **HUD** | `ui/hud.gd` | rebuilt from state every frame, including `MUSIC on/off SFX on/off` from the bus flags | the screen always says what the speakers are doing (readable muted) · text-only HUD | B23 → B24 |
| **Tests** | `tests/harness.gd`, `test_logic.gd`, `test_gameplay.gd`, `test_audio.gd`, `tests/capture.gd` | headless suites, 32 + 65 + 25 checks; a suite that stops early fails; `capture.gd` renders the in-game row of the character comparison | runs in seconds on a fresh copy · cannot judge feel, which is why the playtests exist | B27 → B28; B08 (comparison) |

## Excluded from the explanation (still hashed and counted)

| File | Reason |
|---|---|
| `tests/capture_map.gd` | renders `design/map-overview.png`; the map overview is not shown in this film |
| `tests/probe_balance.gd` | scripted balance bots for `evidence/balance-probe-*.txt`; not part of the playable slice |
| `tests/rasterize_storyboard.gd` | rasterises the storyboard for its comparison image, which this film does not show |

## Saved scene vs. running tree

`game/main.tscn` holds one node with `session.gd`; everything else (player, ground, enemies, HUD, AudioBus and its players) is created by code at run time. The film therefore shows scripts, not a saved node tree, and never presents a runtime node as part of the `.tscn`.
