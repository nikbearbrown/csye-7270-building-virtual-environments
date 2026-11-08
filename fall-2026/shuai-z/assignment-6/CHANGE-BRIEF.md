# CHANGE-BRIEF — Assignment 6: sword-swing sparks and a running dust trail for Rudy

**Revision 1 — 2026-11-04, committed before the first prompt.** Later changes are added as dated revisions at the end; this revision stays as it is.

**How this brief was made:** Claude Code (Claude Opus 5.5) drafted all of it from the assignment, Chapter 9 and this folder's files: the design, the settings, the rules, the predictions and the short answers. The choice of effects is mine: on 2026-11-04 I chose the sword-swing sparks over a goblin-defeat burst, and the world-space dust trail over switching the renderer, after Claude reported why the first ideas could not work (section 1). I reviewed the brief before committing it. The values are a first design; the tuning loop exists to change them, with a revision here each time.

`CLAUDE.md` imports this file (`@CHANGE-BRIEF.md`), so it is the contract the agent works to.

This folder holds one Godot project, `game/`, the 2D game copied from tag `a5`. The course's commands say `godot/`; here they say `game/`. New effect files go in `game/effects/`, preview scenes in `game/previews/`, and tests in `game/tests/`. Frame strips go in `captures/<effect>/r<N>/` in this folder.

## 1. The state

- **Engine and renderer.** Godot 4.7.2 (`logs/checks_60fps.log:1`), GL Compatibility on desktop and mobile (`game/project.godot:16`, `game/project.godot:95-96`). The viewport is 1920 × 1080 with `canvas_items` stretch, shown in a 1280 × 720 window (`game/project.godot:25-29`). **The project's window size is 1280 × 720**, so every on-screen size below is drawn at 2/3 in the window.
- **Camera.** `Main/Camera` is a `Camera2D` at zoom 1 that follows Rudy sideways only (`game/app/main.tscn:16-22`, `game/app/main.gd:88`). In-game camera scale is therefore 1 game px = 1 viewport px.
- **Rudy.** His origin is at his soles (`game/content/rudy/rudy.gd:5`). His sprite is drawn at half scale (`game/content/rudy/rudy.tscn:27-32`) and stands about 160 px from soles to the top of his head (`../assignment-2/evidence/1a/1a-run-a.png`). He walks on the line y = 840 (`game/content/level_1/level_1.tscn:40-44`).
- **The sword.** With the sword, a fresh press of slash starts a swing only when no swing is under way (`rudy.gd:223-226`). A swing lasts `slash_time` 0.3 s, and its hitbox is live from 0.03 s to 0.18 s into it (`rudy.gd:66-68`). `_swing()` puts the hitbox `slash_reach` 50 px in front of him and sets `Rudy/SwordHitbox/Shape.disabled` every tick, false while live (`rudy.gd:239-242`); the shape sits 76 px above his soles (`rudy.tscn:34-43`). A hit cancels a swing (`rudy.gd:143`). The sword comes from the pickup at x = 2500 (`level_1.tscn:79-80`) and is lost on a hit.
- **Running.** `_pick_pose()` shows a run pose when he is on the floor and `absf(velocity.x) > 1.0` (`rudy.gd:298`, `rudy.gd:306-309`), unless he is swinging (`rudy.gd:295-296`). He is under control only in `Mode.PLAY` (`rudy.gd:202`). Run speed is 560 px/s, reached or lost in 0.1 s (`rudy.gd:55-56`).
- **Pause.** Esc sets `get_tree().paused` in play (`main.gd:152-161`); only `SystemKeys` and the music keep running (`system_keys.gd:15`).
- **Goblins.** Three goblins start 1,500 px or more apart and patrol 400 px to their right, so no two ever come within about 1,100 px of each other (`level_1.tscn:69-77`, `goblin.gd:27`). A defeated goblin hides after `SQUASH_TIME` 0.4 s (`goblin.gd:25`, `goblin.gd:51-54`) and is never freed: a death resets it (`goblin.gd:77-85`, `main.gd:129-130`).
- **No particles yet.** No scene or script in `game/` mentions a particle class (checked with grep on 2026-11-04).

**Why the first ideas changed.** A burst on a goblin's defeat cannot happen twice inside one burst lifetime in real play, because the goblins are too far apart, so Effect A moved to the sword swing. Godot's trail feature (`trail_enabled`) draws nothing under GL Compatibility: the engine prints `The Compatibility renderer does not support particle trails.` and the trail emitter stays empty, while the same probe draws trails under Forward+ (`evidence/compat-probe/`). Changing the renderer would change the whole game, so Effect B is a trail made the way Chapter 9's Dodge the Creeps makes one: an ordinary emitter with `local_coords` off, whose particles stay behind as it moves.

**The backgrounds the effects play over** (sampled from `../assignment-2/evidence/1a/1a-run-a.png`; relative luminance with gamma 2.2):

| Where | Colour | Luminance | Where it is |
|---|---|---|---|
| Sky | `#CFE0E6` | 0.73 | above the hills; behind a slash at the top of a jump |
| Pale hills | `#BFD2C4` | 0.62 | around y 500 |
| Green hills, grass strip | `#8FA85E` | 0.35 | around y 600, and the strip on the walk line |
| Wheat | `#D8B858` | 0.50 | from about y 620 down to the walk line: behind Rudy's chest and feet |
| Ground | `#9C8463` | 0.25 | below the walk line |
| Pit shade | `#5A4E44` | 0.08 | in the pits (`level_1.tscn:31-36`) |
| The art's line colour | `#290F0D` | 0.01 | the outline on every sprite (`game/systems/art/outline.gdshader:12`) |

## 2. Effect A — sword-swing sparks (`SlashSparks`)

### The job

- **What it tells the player:** where and when his cut can land. The hitbox is live for only 0.15 s of a 0.3 s swing, 50 px in front of him, and nothing on screen shows that today. The sparks mark that spot, at that moment.
- **Its event:** the sword's hitbox going live. That is `Rudy/SwordHitbox/Shape.disabled` changing from true to false, which `_swing()` does once per swing (`rudy.gd:241-242`). No signal exists for it, and none is added: presentation code reads the shape's `disabled` each physics tick.
- **Its place:** the hitbox's global position on that tick, Rudy's position + (50 × facing, −76).
- **Why it repeats inside one lifetime:** a new swing can start one tick after the last one ends, so cuts go live about 0.32 s apart when the key is pressed again and again. The sparks live 0.45 s.

### The intent

- **Timing phases** (at 30 fps):
  - **Strike, frame 0 (0–0.03 s):** a white flash at the hitbox, at full size and full brightness on its first frame, with every spark still inside it.
  - **Spray, 0.03–0.15 s:** the sparks fly out forward and a little upward, fast, white turning yellow. The flash grows a little and is gone by 0.12 s.
  - **Fall-off, 0.15–0.45 s:** the sparks arc down under gravity, shrink, turn orange and fade. The short-lived ones are gone by 0.27 s and the last by 0.45 s.
  - On a fast second swing, the first swing's last orange sparks are still falling when the second flash lands.
- **Contrast against the real background:** the sparks play over the wheat (luminance 0.50) on the ground, and over the pale hills and sky (0.62–0.73) at the top of a jump. Yellow and white alone do not separate from those: the ramp's yellow (luminance about 0.79) has a contrast ratio of about 1.1:1 against the sky and 1.5:1 against the wheat. So each spark and the flash carry a thin rim in the art's line colour `#290F0D` (about 14:1 against the sky and 10:1 against the wheat), in the same style as the outlined sprites. Over the dark ground and pits (0.25 and 0.08), the white core does the reading (about 3.5:1 and 8:1).
- **Scale against the character:** the flash is about 64 px across on its first frame, roughly 0.4 of Rudy's 160 px, centred on the 56 × 70 px hitbox. Sparks are streaks about 8–13 px wide and 28–44 px long. They travel up to about 190 px forward, a little more than his height, and most die within about 130 px. In the 1280 × 720 window that is a flash about 43 px across and sparks reaching about 85–125 px.
- **Change over life:** the sparks' colour runs white → yellow → orange → transparent, and their size shrinks to 0.3 of their start. The flash grows to 1.3 × while fading from opaque to transparent. Neither fades in alpha alone.
- **Variation:** spark speed 260–420 px/s, a ±30° spread, size 0.7–1.1, lifetime cut by up to 40 % at random, and hue shifted by up to ±0.03. Each swing's spray differs; the flash varies only in size (0.9–1.1).
- **Layering**, under one root node `SlashSparks`:
  - `Flash`: one large soft particle that makes the first frame strong;
  - `Sparks`: 14 streaks that carry the direction and the timing.

  There is no smoke puff: the swing is quick, and smoke would hide the next swing.

### The settings

**Node type:** both emitters are `GPUParticles2D`. A `ParticleProcessMaterial` holds the process settings in the scene file, where a test can read them, and Step 6 converts one to its shader. This renderer draws GPU particles (the probe's reference emitter, `evidence/compat-probe/compatibility_frame30.png`). Neither emitter uses a feature Compatibility lacks (trails, SDF collision, `emit_particle()`). The cost of that choice is that the headless price is near zero by construction, so the budget is compared on GPU time (section 8).

`game/effects/slash_sparks.tscn`: root `SlashSparks` (`Node2D`, `z_index = 1`, so it draws in front of Rudy), with two children:

| Setting | `Flash` | `Sparks` |
|---|---|---|
| **Emission** | | |
| `amount` | 1 | 14 |
| `one_shot` | true | true |
| `explosiveness` | 1.0 | 1.0 |
| `lifetime` | 0.12 s | 0.45 s |
| `emitting` (as saved in the scene) | false | false |
| `preprocess` | 0 | 0 |
| `fixed_fps` | 30 (the default) | 30 |
| emission shape (`emission_shape`, on the material) | point (0) | point (0) |
| **Process** (`process_material`: a `ParticleProcessMaterial` each) | | |
| `particle_flag_disable_z` | true | true |
| `direction` | (1, 0, 0) | (0.944, −0.330, 0): 19° above forward |
| `spread` | 0° | 30° |
| `initial_velocity_min` / `_max` | 0 / 0 | 260 / 420 px/s |
| `gravity` | (0, 0, 0) | (0, 700, 0) px/s² |
| `damping_min` / `_max` | 0 / 0 | 0 / 0 (no damping: that is Effect B's feature) |
| `particle_flag_align_y` | false | true: each streak points along its velocity |
| `lifetime_randomness` | 0 | 0.4 |
| `scale_min` / `scale_max` | 0.9 / 1.1 | 0.7 / 1.1 |
| `scale_curve` (a `CurveTexture`) | 1.0 at 0 → 1.3 at 1 | 1.0 at 0 → 0.3 at 1 |
| `color_ramp` (a `GradientTexture1D`) | (1, 1, 1, 1) at 0 → (1, 1, 1, 0) at 1 | (1, 1, 1, 1) at 0 → (1, 0.9, 0.45, 1) at 0.25 → (1, 0.55, 0.2, 1) at 0.7 → (0.9, 0.35, 0.15, 0) at 1 |
| `hue_variation_min` / `_max` | 0 / 0 | −0.03 / 0.03 |
| **Draw** | | |
| `texture` | `GradientTexture2D`, 64 × 64 | `GradientTexture2D`, 12 × 40 |
| texture fill | radial, `fill_from` (0.5, 0.5), `fill_to` (1.0, 0.5) | the same |
| texture gradient | offsets 0, 0.55, 0.70, 0.85: `#FFFFF0` α 1, `#FFE58A` α 1, `#290F0D` α 1, `#290F0D` α 0 | the same |
| draw material and blend | none: the default mix blending | none |
| **Space and culling** | | |
| `local_coords` | false | false |
| `visibility_rect` | Rect2(−50, −100, 270, 230) | Rect2(−50, −100, 270, 230) |

- **Why the blend is mix, not additive.** Additive light adds to what is behind it, and the wheat and sky are already light, so an additive spark would fade into them. Mix blending keeps the dark rim dark.
- **The textures** are defined inside the scene file. There is no image asset to credit, and SOURCES.md says so.
- **`local_coords` off.** The burst is not a child of Rudy or of a goblin (section 2, rules). It is added to an effects container that never moves. With `local_coords` off, sparks already born stay in world space even if something moves the burst's root.
- **`visibility_rect`** was set by hand, not generated, from the extremes:
  - forward: 420 px/s × 0.45 s = 189 px;
  - up: 420 × sin 49° = 317 px/s, which peaks 72 px up under a gravity of 700;
  - down: 420 × sin 11° = 80 px/s, plus gravity: about 107 px down at 0.45 s;
  - a margin for the flash and the streak length.

  It is mirrored with the burst when Rudy faces left. It is checked by the edge-of-screen human check.
- **Facing.** The material points forward along +x. The trigger code mirrors the burst's root horizontally (scale x = −1) when Rudy faces left, so the sparks fly the way he faces.
- **No `preprocess`.** A burst must start at its own first frame.
- **The preview only** turns on `use_fixed_seed`, on its own instances, with `seed` 1 for the first burst and 2 for the second. The effect scene leaves it off, so repeats vary in play.

### Observable rules

- **A1 — fires on every live cut, never otherwise.** Each time `Rudy/SwordHitbox/Shape.disabled` changes from true to false, exactly one new burst starts, on that physics tick. No burst starts:
  - on scene load or on the title;
  - when slash is pressed without the sword;
  - when slash is pressed again during a swing (the game starts no new swing then);
  - while the tree is paused;
  - when a goblin is defeated by a stomp.
- **A2 — at the event's place, facing his way.** On the trigger tick, the burst root's global position equals the hitbox's global position to within 1 px. Its horizontal scale has the sign of Rudy's `facing` (`rudy.gd:78`).
- **A3 — the retrigger rule: overlap.** Each cut gets its own burst. A second cut while the first burst is alive starts a second burst and leaves the first running: it is not restarted, moved or cut short. Swings go live at least 0.3 s apart and a burst lives 0.45 s, so **at most 2 bursts are alive at once**.
- **A4 — no parent can take it away.** The bursts live in an effects container under `Main`, not under Rudy (whose `Look` flips and flashes, `rudy.gd:231-232`) and not under a goblin. Nothing on a swing frees a node. A cut that defeats a goblin hides that goblin after 0.4 s, but the burst stays visible for its whole 0.45 s life. A scene reload (Enter on the end card, `main.gd:209`) frees the bursts with everything else, which is fine: no swing can be under way then.
- **A5 — pause.** A burst alive when the tree pauses freezes where it is and stays visible. It goes on from the same point on resume.

## 3. Effect B — running dust trail (`RunDust`)

### The job

- **Which job: a trail.** While Rudy runs on the ground, he leaves a short line of dust behind his feet that hangs for half a second.
- **What it tells the player:** that he is running at speed, which way, and where his feet touch the ground. His run cycle is two frames, 0.125 s each (`rudy.gd:61`), and the camera holds him still on screen. The trail gives the run a sense of speed and shows the moment he leaves the ground, because it stops in the air.
- **Its condition:** Rudy is running on the ground under the player's control: `mode == Mode.PLAY` (`rudy.gd:80`, `rudy.gd:202`), `is_on_floor()` and `absf(velocity.x) > 1.0` (`rudy.gd:215`). That is `_pick_pose()`'s run test (`rudy.gd:298`, `rudy.gd:306`) without its swing override, so a swing while running does not cut the trail. Presentation code reads these each physics tick.
- **The feature Effect A does not use: damping** (`damping_min` / `damping_max`), which slows each puff to a stop so it hangs in the air. Effect B also uses a box emission shape where Effect A uses a point.

### The intent

- **Timing phases** for each puff:
  - **fade-in, 0–0.075 s:** it appears at his feet and rises from transparent to its full opacity of 0.75;
  - **hang, 0.075–0.3 s:** damping brings it to a stop 4–17 px above where it was born, while it grows;
  - **dissipate, 0.3–0.5 s:** it reaches full size, lightens towards the ground's colour and fades out.

  For the trail as a whole:
  - **start:** a puff is visible within two frames of the first running tick, and the trail reaches its full length after 0.5 s of running;
  - **stop:** no new puff is born from the tick he stops or leaves the ground, and the trail empties from its old end within 0.5 s.
- **Contrast against the real background:** the puffs sit just above the walk line, in front of the lower wheat (luminance 0.50), with their lower edge over the grass strip (0.35) and the ground (0.25).
  - A pale dust would be lighter than the wheat but only weakly: a cream at about 0.78 gives about 1.5:1.
  - So the dust is darker than the wheat, an earth brown `#7A6448` (about 0.14), which gives about 2.9:1 against the wheat and 2.1:1 against the grass strip.
  - Over the ground itself it is weak (about 1.6:1). I accept that: the puffs rise above the line, and the part that matters is behind his boots.
- **Scale against the character:** puffs are about 11 px across when born and grow to about 37 px, 0.07–0.23 of Rudy's height. At full speed they are born about 14 px apart, so they overlap into one band. The band is about 280 px long, 1.75 × his height, and no taller than about 40 px, which is below his knees. In the window that is about 185 px long.
- **Change over life:** opacity runs 0 → 0.75 → 0.5 → 0, size 0.5 → 1.0 → 1.15, and colour from earth brown towards the ground's `#9C8463` as it thins, so it settles into the ground instead of vanishing on the spot.
- **Variation:** puff speed 40–90 px/s within ±50° of straight up, size 0.7–1.0, lifetime cut by up to 30 % at random, birth times jittered (`randomness` 0.2), and hue shifted by up to ±0.02. A long run does not look like a row of stamps.
- **Layering:** one emitter, `RunDust`. Its job is one continuous band, and a second layer (pebbles, say) would be noise at this size.

### The settings

**Node type:** `GPUParticles2D`, for the same reasons as Effect A. Its trail does not use `trail_enabled`, which this renderer does not draw. `game/effects/run_dust.tscn`: root `RunDust` (`GPUParticles2D`, `z_index = 0`). Presentation code places it before Rudy in the tree, so it draws in front of the level art and behind Rudy.

| Setting | `RunDust` |
|---|---|
| **Emission** | |
| `amount` | 20 |
| `one_shot` | false |
| `explosiveness` | 0.0: a steady stream |
| `randomness` | 0.2 |
| `lifetime` | 0.5 s |
| `emitting` (as saved in the scene) | false |
| `preprocess` | 0 |
| `fixed_fps` | 30 (the default) |
| `trail_enabled` | false |
| emission shape (on the material) | box (3), `emission_box_extents` (14, 3, 0): a 28 × 6 px box |
| **Process** (`process_material`: a `ParticleProcessMaterial`) | |
| `particle_flag_disable_z` | true |
| `direction` | (0, −1, 0): up |
| `spread` | 50° |
| `initial_velocity_min` / `_max` | 40 / 90 px/s |
| `gravity` | (0, 0, 0) |
| `damping_min` / `_max` | 120 / 180 px/s² |
| `particle_flag_align_y` | false |
| `lifetime_randomness` | 0.3 |
| `scale_min` / `scale_max` | 0.7 / 1.0 |
| `scale_curve` (a `CurveTexture`) | 0.5 at 0 → 1.0 at 0.4 → 1.15 at 1 |
| `color_ramp` (a `GradientTexture1D`) | `#7A6448` α 0 at 0 → `#7A6448` α 0.75 at 0.15 → `#8A7356` α 0.5 at 0.6 → `#9C8463` α 0 at 1 |
| `hue_variation_min` / `_max` | −0.02 / 0.02 |
| **Draw** | |
| `texture` | `GradientTexture2D`, 32 × 32, radial, `fill_from` (0.5, 0.5), `fill_to` (1.0, 0.5); offsets 0, 0.6, 1.0: white α 1, white α 0.6, white α 0. It is white so that the colour ramp sets the colour |
| draw material and blend | none: the default mix blending |
| **Space and culling** | |
| `local_coords` | false |
| `visibility_rect` | Rect2(−320, −80, 640, 110) |

- **`local_coords` off is the trail.** The emitter rides at Rudy's feet, and each puff stays where it was born, so his motion lays them out in a line. With it on, every puff would travel with him as a clump at his feet.
- **Position.** Presentation code keeps the emitter at Rudy's soles + (0, −4) every physics tick. `rudy.tscn` gets no new child.
- **`visibility_rect`** was set by hand, not generated: about 280 px of trail behind him in either direction, plus a margin, and from 80 px above the feet to 30 px below. The emitter is always at Rudy, and the camera keeps him in view, so the rectangle is always on screen.
- **No `preprocess`.** The game opens with Rudy idle on the title, and a trail that was already running would be wrong.
- **The texture** is defined in the scene file, so there is no asset to credit.
- **The preview only** turns on `use_fixed_seed` (`seed` 1) on its own instance.

### Observable rules

- **B1 — starts and stops with the condition.** `emitting` becomes true on the first physics tick the condition holds, and false on the first tick it stops holding. That covers stopping, turning in place (a turn sets `velocity.x` to 0, `rudy.gd:204-208`), jumping, being knocked back, falling out, defeat, respawn and the teleport circle. It is false on scene load, on the title and while he stands.
- **B2 — at his feet.** While the condition holds, the emitter's global position is Rudy's position + (0, −4) on every physics tick, to within 1 px.
- **B3 — paused.** While the tree is paused, `emitting` keeps its value and the node does not process. Puffs already alive freeze in place and stay visible, no new puff is born, and on resume they carry on from the same point.
- **B4 — hidden.** While the emitter is not visible in the tree, it draws nothing and presentation code keeps `emitting` false, so no puffs build up unseen. When it is visible again and the condition holds, `emitting` is true again on that tick.
- **B5 — no flashing, no streak.** The trail is not under `Look`, so it does not flash while Rudy is invulnerable. A respawn moves him to the checkpoint while the condition is false, so no puffs are drawn along the jump.

## 4. Boundaries

- **Unchanged files:**
  - `game/content/rudy/rudy.gd`, `rudy.tscn`, `rudy_look.gd`;
  - `game/content/goblin/*`;
  - `game/content/level_1/*`;
  - `game/app/main.gd`, `game/app/system_keys.gd`;
  - `game/ui/*`;
  - `game/systems/*`, including the outline material;
  - `game/project.godot`: the renderer stays GL Compatibility, and no setting changes.
- **Unchanged behaviour:** collision, movement, input, the state machine and its timings (the 0.3 s swing and its live window, 1.2 s invulnerability, 0.35 s hurt time, the death and respawn timings).
- **Shaders:** `game/shaders/invulnerable_tint.gdshader`, my hand-written Assignment 5 shader, stays as it is, and no agent session edits anything in `game/shaders/`. The one new file there, `particles_generated.gdshader`, is generated by me in the editor in Step 6.
- **Tests:** the existing tests and what they expect stay the same: `checks.tscn` 141 checks at 60 fps, `invulnerable_tint_checks.tscn` 15 at 30, 60 and 144 fps (`logs/`). New tests are added beside them.
- **What may change:**
  - `game/app/main.tscn` may gain presentation nodes: the effects driver and its containers. Nothing else in it changes.
  - New files go in `game/effects/`, `game/previews/` and `game/tests/`.
  - Effect settings live in the effect scene files, not in code. The driver only places, mirrors, starts and stops them.
- **Presentation code** may read game state (`SwordHitbox/Shape.disabled`, `facing`, `mode`, `is_on_floor()`, `velocity`, `get_tree().paused`). It never writes game state.
- **The vsync debug key for the GPU price is F9.** No action uses it (`game/project.godot`, input map). It is read by a new debug node, not by `system_keys.gd`.

## 5. The evidence split

| Rule | Checked by | How |
|---|---|---|
| Every setting in sections 2 and 3 | headless: configuration tests | `test_slash_sparks_config.gd` and `test_run_dust_config.gd` load each scene and compare every value above with the loaded resources. The Godot 3 name mutation must fail them |
| A1 fires on every live cut, never otherwise | headless: state test | Real slash presses through the game loop. It counts new bursts per live edge, and none on load, without the sword, during a swing, while paused, or on a stomp |
| A2 place and facing | headless: state test | Burst root position against the hitbox's position on the trigger tick; the scale sign against `facing`, facing right and left |
| A3 overlap, at most 2 alive | headless: state test; strip | Two cuts about 0.33 s apart: two bursts alive, the first not restarted (it keeps its start tick and position). Strip frame 20 shows both |
| A4 no parent can take it away | headless: state test; eyes | The burst's parent is the container; after a cut that defeats a goblin, `is_visible_in_tree()` stays true for 0.45 s. I watch a cut on a goblin in play |
| A5 pause | eyes | Esc right after a swing in play: the sparks hold still and stay visible |
| B1 starts and stops | headless: state test; strip | Real move and jump input: `emitting` against the condition on each tick, through run, stop, turn, jump and land. False on load and on the title. Strip frames 10 and 46 |
| B2 at his feet | headless: state test | Emitter position against Rudy's position + (0, −4) each tick while running |
| B3 paused | headless: state test; eyes | While paused: `emitting` unchanged and `can_process()` false. The freeze itself I check by eye, with Esc while running |
| B4 hidden | headless: state test | Hide the emitter while running: `emitting` false; show it again: true |
| B5 no flashing, no streak | eyes | Run while invulnerable after a hit; die and respawn while holding a direction |
| How each effect reads (timing, contrast, scale, change over life, variation) | strip, then eyes | Claude reads the strips against sections 2 and 3, and that reading is a claim. My verdict in the running game at 1280 × 720 decides |
| Against the background | eyes | A over the sky (a slash at the top of a jump) and over a pit (a slash while falling between x 4300 and 4510); B over the wheat and ground at full speed |
| Edge of screen (`visibility_rect`) | eyes | Swing facing right at the level's right end (x near 7700, where the camera stops), and facing left at the start (x 300) |
| Scene load | eyes | The first frames after the game starts and after Enter on the end card: no dust, no sparks |
| No agent changed `game/shaders/` | the session check | `git diff --stat game/shaders/` prints nothing after every session |

## 6. The frame strips

Both previews are fixtures, and every capture of them is labelled as one.

- **Background.** Each preview instances the real level as its background, with its gameplay objects frozen, and frames the stretch x ≈ 1950–2450 of Segment 1: wheat, green and pale hills, sky and ground, with no hazard in it. The camera is at zoom 1 with the walk line at y = 840, as in the game.
- **Scale reference.** A frozen sprite of Rudy, drawn as `rudy.tscn` draws him (half scale, same offset), stands where he would.
- **Capture.** Captures are 30 fps Movie Maker runs, which I start, into `captures/<effect>/r<N>/`. Only the frames read below are committed.

**Effect A** (`game/previews/slash_sparks_preview.tscn`). Rudy's sprite is in `CHAR-SWORD-SLASH`, facing right, at x = 2200, so the hitbox is at (2250, 764), over the wheat. The burst fires at frame 10. The `retrigger` export is on by default and fires the second burst at frame 20, 0.333 s later, about the shortest gap between two swings. Run with `--quit-after 60`.

| Frame | After the first trigger | What it should show |
|---|---|---|
| 10 | 0 | The trigger frame: a white flash about 64 px across on the hitbox, with a dark rim, at full size; the sparks still inside it |
| 12 | 0.067 s | The flash larger (about 1.2 ×) and half faded; 14 white-yellow streaks 15–30 px out, fanned forward and up, pointing along their paths |
| 15 | 0.167 s | No flash; yellow streaks 40–70 px out, the lowest starting to bend down; a few already shorter |
| 20 | 0.333 s | The second trigger: a fresh flash on the hitbox, and around it the first burst's 6–10 surviving sparks, small and orange, 80–130 px out and falling. Two bursts at once, the overlap rule |
| 30 | 0.667 s | The first burst gone. The second burst at its own 0.333 s: small orange sparks falling, as frame 20 showed for the first |
| 50 | 1.333 s | Nothing but the background and the frozen Rudy |

**Effect B** (`game/previews/run_dust_preview.tscn`). The emitter and Rudy's sprite, in his run frames, move right at 560 px/s (18.67 px per frame) from x = 1950, starting at frame 10, with the camera following as in the game. At frame 40 the condition ends: they stop at about x = 2510 and the emitter stops emitting. Run with `--quit-after 70`.

| Frame | Time | What it should show |
|---|---|---|
| 10 | condition begins | At most one or two faint brown puffs at his boots, mostly transparent |
| 13 | 0.1 s running | A short line of 3–5 puffs, about 55 px long behind his boots, the oldest at full opacity |
| 25 | 0.5 s running | Steady state: a band about 280 px long behind him, densest and darkest at his boots, wider and paler at its far end |
| 40 | 1.0 s, the condition ends on this frame | The same band as frame 25 (the last frame of running) |
| 46 | 0.2 s after | No puff at his boots younger than 0.2 s; the band about 170 px long, its far end gone, the rest paler and wider |
| 56 | 0.53 s after | Nothing left |

## 7. Predicted failures and how each is caught

| # | Failure | What it would look like | Caught by |
|---|---|---|---|
| 1 | **Godot 3 names** in a scene file (`initial_velocity`, `scale`, `ParticlesMaterial`) | The scene loads, the effect fires, and those settings sit at their defaults: sparks at speed 0 piled on the flash, or puffs at scale 1 | The configuration tests read the Godot 4 names. The Step 2 mutation (`initial_velocity_min` → `initial_velocity` in `Sparks`) must fail it |
| 2 | **`emitting` left at its default, true** | Sparks fire as the level loads; dust under Rudy on the title | Both scene files save `emitting = false`, and the configuration tests read it. The state tests check that nothing fires on load. I check scene load by eye |
| 3 | **`local_coords` on for the dust** | No trail: a clump of puffs travelling with his boots | The configuration test reads `local_coords = false`. Strip frame 25 must show a line, not a clump |
| 4 | **The dropped retrigger**: one one-shot node, set `emitting = true` again while still emitting | The second swing of a fast pair has no sparks | The A3 state test (two cuts 0.33 s apart, two bursts alive); strip frame 20 |
| 5 | **Disable Z off** on a material | Part of each velocity goes into an invisible Z, so sparks fly short and slow and puffs barely rise | The configuration tests read `particle_flag_disable_z = true` on both materials |
| 6 | **A null or wrong texture** | Particles draw as tiny squares; sparks without a rim vanish over the sky | The configuration tests read each texture's class, size, fill and gradient stops. Strip frame 10 must show the rim |
| 7 | **The burst parented to Rudy's `Look` or to a goblin** | Sparks that flip with him and flash while he is invulnerable, or vanish with a goblin at 0.4 s | The A4 state test (the parent is the container, visible for 0.45 s); a cut on a goblin in play |
| 8 | **Mirroring does not reach the velocities** | Facing left, the sparks fly right, behind him | The A2 state test reads the scale sign; I swing facing left in play. The preview faces right, so this one is caught by eye |
| 9 | **`visibility_rect` too small** | Sparks pop out near the screen edge | The edge-of-screen check at both ends of the level |
| 10 | **Sparks fall through the walk line** (Compatibility has no particle collision) | Late orange sparks sinking into the brown ground | Strip frames 15 and 20, and play. A likely first tuning target |
| 11 | **The dust too weak over the wheat**, or the sparks' rims too thin at 1280 × 720 | A trail that disappears above the boots; sparks that read only on dark ground | Play over the lightest and darkest stretches (section 5). A likely first tuning target |
| 12 | **The GPU time cannot be read on this Mac** | The Visual Profiler's GPU column reads 0 or stays empty. The probe's viewport GPU timer read 0.0 ms under both renderers (`evidence/compat-probe/`) | I open the Visual Profiler before relying on it (section 8) |
| 13 | **The cost script measures itself** | Every case, the empty scene included, reads the same: the 6.9 ms frame sleep Chapter 9 found | The empty-scene control, and running it at `--fixed-fps 60` through the wrapper |

## 8. Price predictions and the budget

| | Peak particles | Predicted headless CPU price | Predicted GPU time (Apple M3) | Budget, and the price it is compared on |
|---|---|---|---|---|
| Effect A | 30 (2 bursts × 15) | Within 0.01 ms per frame of the game with both effects off. It is a GPU node, so the CPU share is only node bookkeeping and the trigger code | Under 0.05 ms | **0.25 ms of GPU time**, at 2 bursts alive |
| Effect B | 20 | Within 0.01 ms per frame of the game with both effects off, for the same reason | Under 0.05 ms | **0.25 ms of GPU time**, while running at full speed |

- **Headless predictions.** At `--fixed-fps 60` the empty scene should read about 0.002 ms per frame, Chapter 9's control on a similar Mac. The game with both effects off should read clearly more, because it runs physics and scripts every frame. My guess is 0.05–0.5 ms.
- **Why GPU time.** Both effects are GPU nodes, so the headless numbers are not the budget: they would read near zero even if the effects were expensive to draw. Both budgets are compared on GPU time, from the editor's Visual Profiler, with each effect off and then at its heaviest.
- **If GPU time cannot be read (failure 12).** If the Visual Profiler shows no GPU time on this Mac, TEST-REPORT.md says so plainly. I then record:
  - the Monitors' FPS with vsync off (F9), with each effect off and at its heaviest;
  - whether FPS actually rises above the display's refresh rate;
  - that the budget could not be compared on GPU time on this machine.

## 9. Short answers

1. **Node types and missing features.** Both effects use `GPUParticles2D`. Under GL Compatibility that node does not draw `trail_enabled` trails or SDF collision, and `emit_particle()` does not work (Chapter 9; the probe confirmed the trails). This brief uses none of them: Effect B's trail is a world-space stream, and the sparks have no collision. A `CPUParticles2D` would lack the process material, sub-emitters, trails and `amount_ratio`, but this brief needs none of those either.
2. **`local_coords` off, if the parent moves.** Effect A's parent is an effects container that never moves. If Rudy runs on after a cut, the sparks stay where the cut was. At 560 px/s he is up to about 250 px past them when the last one fades. Even if the burst's root were moved, its living sparks would stay where they are, because they are in world space.
3. **Bursts alive at once.** Overlap, with cuts at least about 0.32 s apart and bursts living 0.45 s: at most 2 alive at once, and a peak of 30 particles.
4. **The headless price and FPS.** A headless run reports a GPU effect as nearly free: within noise of the game without it. The dummy renderer runs no particle process and draws nothing, so all the CPU does is set node state. With vsync on, FPS would read the display's refresh rate both with the effect off and with it on. Vsync holds it there until a frame misses, and these effects are far too small to make one miss.
5. **Effect B on load, paused and hidden.**
   - **On load:** nothing, with `preprocess` 0 and `emitting` false, because Rudy is idle on the title. With `preprocess` set to 0.5 s and `emitting` left on, a finished band of dust would already sit at his still feet on the first frame, which is wrong.
   - **Paused:** the puffs freeze where they are and stay visible, with no new ones.
   - **Hidden:** nothing is drawn, and the driver keeps `emitting` false.
6. **Emission, process and draw.**
   - **Emission:** `amount`, `one_shot`, `explosiveness`, `randomness`, `lifetime`, `emitting`, `preprocess`, `fixed_fps`, the emission shape and box extents. (The shape is stored on the process material in a GPU node, but it decides where particles are born.)
   - **Process:** `direction`, `spread`, the initial velocities, `gravity`, damping, `particle_flag_disable_z`, `particle_flag_align_y`, `lifetime_randomness`, the scale range and curve, the colour ramp and hue variation.
   - **Draw:** the textures and the blend mode, and `z_index` and tree order, which decide what each effect is drawn in front of and behind.
   - **Neither:** `local_coords` and `visibility_rect` decide the space the particles live in and when they are culled.

## Revisions

### Revision 2 — 2026-11-04, after the Step 1 review

Probes run during the CLAUDE.md review showed that failure 1 in section 7 predicts the wrong result, and that two references are imprecise. Revision 1 above stays as it was committed; where the two differ, this revision holds. Claude Code drafted it from the probe logs; it was committed on my word.

- **Failure 1, Godot 3 names in a scene file.** Revision 1 predicted that they "sit at their defaults". In Godot 4.7.2 each name does something different (`logs/probe_particles_headless.log:17-22`, `logs/probe_mutation.log:3-10`):
  - `Particles2D` loads as `GPUParticles2D` and `ParticlesMaterial` as `ParticleProcessMaterial`, with their values kept, and `flag_disable_z` sets `particle_flag_disable_z`. The effect is unchanged, so neither a configuration test nor a strip can see these three. They are still not used.
  - `flag_align_y` is dropped without a message, so `particle_flag_align_y` stays false and the sparks no longer point along their motion. The configuration test reads `particle_flag_align_y` and catches it.
  - `initial_velocity`, `scale`, `damping` and `hue_variation` exist only as editor ranges, never saved. A number on an `initial_velocity` or `scale` line (the two tested) sets both ends of the range to 0, and a `_max` line after it sets the top end again. So `scale = 1.0` on its own hides the particles at scale 0; it does not give "puffs at scale 1".
- **The Step 2 mutation.** Godot saves `initial_velocity_min` before `initial_velocity_max` (`logs/probe_mutation.log:3`). So renaming that line to `initial_velocity` in `Sparks` loads as 0 to 420 px/s, not as speed 0 (`logs/probe_mutation.log:4`). The new prediction:
  - `test_slash_sparks_config.gd` fails on `initial_velocity_min`, which reads 0 instead of 260;
  - on screen the burst looks almost the same, with a few slow sparks left near the flash.

  The test is the check for this mutation, not the strip.
- **Section 3, Effect B's condition.** `absf(velocity.x) > 1.0` is checked at `rudy.gd:306`, and `is_on_floor()` at `rudy.gd:298`. `rudy.gd:215` is where `velocity.x` is set, not where the run test reads it.
- **Section 1, Pause.** The music keeps running while paused because `game/systems/audio/music.gd:40` sets it to always process. `system_keys.gd:15` covers only `SystemKeys`.

### Revision 3 — 2026-11-04, Effect A tuning r1: `Sparks` `amount` 14 → 28

I watched the first strip's preview (r0) in a window and found the sparks too sparse. Claude proposed one change, I approved it, and after strip r1 I kept it (`TUNING.md`, "Effect A, revision r1"). Where Revision 1 says otherwise, this revision holds:

- **Section 2, the settings:** `Sparks` `amount` is 28, not 14. The layering line reads "`Sparks`: 28 streaks". `game/effects/slash_sparks.tscn` and `game/tests/test_slash_sparks_config.gd` both say 28.
- **Rule A3, short answer 3 and section 8:** a burst peaks at 29 particles (1 flash and 28 sparks), so two overlapping bursts peak at 58, not 30. The GPU-time prediction (under 0.05 ms) and the budget (0.25 ms of GPU time at 2 bursts alive) stay as they are.
- **Section 6, the strip:** frame 12 shows about 14–18 streaks that can be told apart, not 14, and frames 20 and 30 show about 7–8 small specks of the earlier burst, 80–140 px forward. That is within the 6–10 Revision 1 predicted; Claude's prediction of 3–5 for r1 was too low (`TUNING.md`). The other frames read as before.

Claude Code drafted this revision; it was committed on my word.

### Revision 4 — 2026-11-05, Effect B tuning r1–r3: a darker ramp, 40 puffs, twice the speed

In the first strip's preview (r0) I could not see the dust at all. Three rounds followed, each one change proposed by Claude and approved by me, each kept after I watched the new strip's preview at real speed (`TUNING.md`, "Effect B, revision r1" to "r3"). Where Revision 1 says otherwise, this revision holds:

- **Section 3, the settings:**
  - `color_ramp` (r1): `#5C4A35` α 0 at 0 → `#5C4A35` α 1.0 at 0.15 → `#6E5A43` α 0.8 at 0.6 → `#9C8463` α 0 at 1.
  - `amount` (r2): 40, not 20.
  - `initial_velocity_min` / `_max` (r3): 80 / 160 px/s, not 40 / 90.

  `game/effects/run_dust.tscn` and `game/tests/test_run_dust_config.gd` say the same.
- **Section 3, contrast.** Revision 1's figures (2.9:1 against the wheat) assumed opaque dust over the wheat. The puffs are born in the green grass strip above the walk line, at no more than 0.75 opacity with soft edges, and there they nearly vanished. At full opacity the new colour gives about 3.3:1 against the grass strip and 4.5:1 against the wheat.
- **Section 3, scale and timing.** At full speed a puff is born about every 7 px, so the puffs overlap into one band at his boots. They no longer stop 4–17 px above where they were born: the band rises as it goes back, to about 55–60 px above the walk line at its far end (58 px measured at r3's frame 25), above Revision 1's limit of about 40 px. I chose that after watching r2, where the dust stayed inside the grass.
- **Section 8:** Effect B peaks at 40 particles, not 20. The GPU-time prediction and the 0.25 ms budget stay as they are.
- **Section 6, the strip** (as r3 shows it): 10, nothing yet; 13, a short dark streak behind his rear boot; 25 and 40, a dark-brown band low at his boots that rises behind him, its far end a few loose puffs over the lower wheat; 46, pale puffs near where he stopped; 56, nothing.

Claude Code drafted this revision; it was committed on my word.
