# Change brief — plan and predictions

> Version 1 — written 2026-10-03 to 2026-10-07. Later changes go in "Revision history" at the end; version 1 is not rewritten.
> This lists only what the **asset slice** needs, not the whole game. The slice takes place entirely inside the subway base (`STORYBOARD.md`, panels 1–5).
> Asset IDs match `STORYBOARD.md` and `CHARACTER-SHEET.md`.

## Design changes already made
The character direction was revised while I reviewed generated drafts. These changes are already part of the plan (thumbnails in `design/rejected/`, rows in the `SOURCES.md` asset log):

1. **Character material correction**
   - Generated problem: early outputs had shiny, glossy, or plastic-looking lower-body materials that read as latex / PVC rather than practical clothing.
   - My judgment: this did not fit the dark school-tactical character and gave a generic "cheap AI" look.
   - My decision: thick matte opaque black tights and matte woven fabrics; explicitly reject wet-look, latex-like, PVC-like, and overly reflective materials.
2. **Coat / skirt layering correction**
   - Generated problem: one turnaround made the coat look tucked into the skirt from the back.
   - My judgment: that clothing construction was wrong.
   - My decision: the oversized coat hangs outside the skirt and covers most of it; only the lower skirt hem is visible.
3. **Holster redesign**
   - First idea: a right-thigh handgun holster.
   - Problem: it clashed visually with the skirt and produced inconsistent generated geometry.
   - My decision: move the holster to the right waist / right hip, hidden under the coat. It is normally concealed and only shows when the coat moves or opens.
4. **Removing unnecessary identity graphics**
   - Generated problem: some drafts added crosses, emblems, patch symbols, and other decorative motifs.
   - My judgment: these over-defined the character and were not needed for this project.
   - My decision: remove them and keep the base character visually simple.
5. **Armor changed from permanent design to modular equipment**
   - First direction: early drafts built a plate carrier and tactical pouches into the character design.
   - My judgment: this made the character too specific and less flexible.
   - My decision: keep the base character lightly equipped, and move plate carriers, chest rigs, medical pouches, magazine pouches, backpacks, and tactical tablet equipment into separate modular assets.
   - Production consequence: the base character must look complete without armor, and armor is modeled as separate equippable meshes.
6. **Turnaround expanded for 3D reference**
   - First reference: front / side / back.
   - My decision: add a three-quarter view, because it shows how the front and side construction connect.
   - Production consequence: all 3D reconstruction and pose checks use the front, three-quarter, side, and back references together.

## Slice summary
The player starts on the start menu inside the subway base, with the character sitting on a bench. Clicking Start rotates the camera into the over-the-shoulder view, the character stands up, and the menu music stops. The player then walks around the base and switches the tablet between its three states (not looking, one-handed, two-handed) with a short or long Tab press. The game does not pause while the tablet is open.

## Asset list (this slice)
| Asset ID | Category | Asset | Storyboard panel(s) | Planned path | Status |
|---|---|---|---|---|---|
| CHAR-TURN | Art (reference) | Front / three-quarter / side / back turnaround | All | `design/character/turnaround.png` | Accepted |
| CHAR-BASE | Art | Base 3D player character (no armor) | 1–5 | [TBD] | Design approved; 3D model not built |
| CHAR-HOLSTER | Art | Right-waist concealed handgun holster | All | Part of CHAR-BASE | Included in the base outfit |
| CHAR-SIT | Art (state) | Sitting on the bench | 1, 2 | [TBD] | To make |
| CHAR-IDLE | Art (state) | Idle / tablet "not looking" | 2 | [TBD] | To make |
| CHAR-WALK | Art (state) | Walk | 3 | [TBD] | To make |
| CHAR-TAB1 | Art (state) | Tablet, one hand | 3, 5 | [TBD] | To make |
| CHAR-TAB2 | Art (state) | Tablet, two hands, leaning in | 4, 5 | [TBD] | To make |
| PROP-TABLET | Art (prop) | Military rugged tablet | 3, 4, 5 | [TBD] | To make |
| ENV-BASE | Art (environment) | Subway base interior, including the bench | 1–4 | [TBD] | To make |
| UI-TITLE | UI | Game title and start menu | 1, 2 | [TBD] | To make |
| UI-TAB-SMALL | UI | Small tablet window (desktop), bottom right | 3 | [TBD] | To make |
| UI-TAB-FULL | UI | Full tablet interface (desktop) | 4 | [TBD] | To make |
| SFX-STEP | Sound | Footsteps | 3 | `assets/sfx/….ogg` | To make |
| SFX-TAB-OUT | Sound | Cloth rub when the tablet is taken out | 3 | `assets/sfx/….ogg` | To make (low priority in the storyboard) |
| SFX-TAB-BOOT | Sound | Tablet startup "beep" | 3 | `assets/sfx/….ogg` | To make |
| [TBD] | Sound | Fourth sound event | [TBD] | `assets/sfx/….ogg` | [TBD] |
| MUS-MENU | Music | Start-menu loop | 1, 2 | `assets/music/….ogg` | To make |

### Planned for later, not in this slice
From storyboard panels 6–10 and my lab-stealth plan:

| Asset ID | Asset | Panel(s) |
|---|---|---|
| CHAR-STEALTH, CHAR-COVER, CHAR-PEEK, CHAR-DRAW, CHAR-AIM, CHAR-FIRE, CHAR-HURT, CHAR-DEATH, … | Remaining poses in `CHARACTER-SHEET.md` | 6–8 |
| ARMOR-PC | First modular plate carrier | — |
| ENV-LAB | Dim laboratory corridor / chamber | 6 |
| ENV-COVER | Lab workstation / equipment rack used as cover | 6 |
| ENV-DOOR | Doorway into the next chamber | 6 |
| ENEMY-MECH | Hovering scout robot (the mechanical monster) | 6 |
| VFX-SCAN | Scout robot scan beam / cone | 6 |
| UI-DETECT | Detection / alert indicator | 6 |
| PROP-TERMINAL | Lab terminal / console | — |
| SFX-ROBOT-HUM, SFX-SCAN, SFX-ALERT, SFX-INTERACT | Robot hover loop, scan pulse, detection alert, console / door interaction | 6 |
| MUS-BOSS | Boss combat music | 7 |
| SFX-FAIL | Death / failure sound | 8 |
| SFX-EXTRACT | Extraction success sound | 9 |

## Event-to-sound map (this slice)
| Sound | Exact game event that triggers it | How double triggers are prevented |
|---|---|---|
| SFX-STEP | A foot touches the floor during walk | Triggered only from footstep markers in the animation; no parallel timer-based trigger |
| SFX-TAB-OUT | Tablet state changes from "not looking" to "one-handed" or "two-handed" | Fired on the state transition, not on the key press. The short / long Tab press is resolved first, so a long press never fires once as a short press and again as a long press |
| SFX-TAB-BOOT | Same transition as SFX-TAB-OUT (the tablet is taken out) | Same state latch. Switching one-handed ↔ two-handed does not replay it |
| [TBD] | [TBD] | [TBD] |

Rule: sound never decides game state. A missing or muted sound must not change what happens.

## Music behavior
In this slice, music plays only on the start menu.

| Situation | What the music does |
|---|---|
| Start menu | `MUS-MENU` loops; the seam must not be audible |
| Click Start | `MUS-MENU` stops as the camera turns to the over-the-shoulder view. No abrupt hard cut unless it is chosen deliberately and tested |
| Pause | The game has no pause (`CONCEPT.md`) |
| Failure | No music: black screen and failure sound (`CONCEPT.md`); not part of this slice |
| Success (extraction) | No music, sound only (`CONCEPT.md`); not part of this slice |
| End of slice | Nothing to do: the music already stopped after Start |
| Mute | Music and effects muted separately; keys [TBD] |

## Predicted failure cases and how I will check them

### 1 — Character proportions drift between generated poses
- **Risk:** hair length, face shape, coat length, skirt position, boot scale, or body proportions change from pose to pose (including the sitting and tablet poses).
- **Check:** compare every pose against `design/character/turnaround.png`; overlay pose frames at equal character height; reject frames where head height, shoulder width, eye position, coat hem, or leg length visibly drift.
- **Mitigation:** generate from one reference; keep a fixed character prompt / reference image; use reference-conditioning or pose-control tools later if needed.

### 2 — The dark character disappears against the subway base
- **Risk:** the coat, skirt, tights, and boots are all near-black and may merge into a dark, cool-toned environment.
- **Check:** capture gameplay at the actual viewport size in the darkest part of the base; convert the screenshot to grayscale and inspect the silhouette; test both still and moving.
- **Mitigation:** keep environment values separate from the character silhouette; use controlled cool edge lighting or practical lights where needed; keep the white shirt and exposed face as high-value anchors.

### 3 — Tablet sounds fire twice
- **Risk:** the short / long Tab press logic fires the take-out sounds once on key down and again when the press resolves, or a continuous state check fires them every frame.
- **Check:** log state transitions and count sound events for one short press, one long press, rapid repeated presses, and a held key.
- **Mitigation:** trigger sounds on state transitions, not continuous conditions; use a state enum; reset only when the state really changes.

### 4 — The menu music loop clicks at the seam
- **Risk:** the generated music has a mismatched waveform or a reverb tail at the loop boundary.
- **Check:** loop the track for several minutes with headphones; listen at the seam with no other sounds.
- **Mitigation:** edit the loop points; use a short crossfade; regenerate or trim the music if the seam is still obvious.

### 5 — Coat / skirt / concealed holster / tablet clip badly in 3D
- **Risk:** the long coat, skirt, right-waist holster, and the tablet in the hands occupy the same space during movement.
- **Check:** test the idle, walk, sit, stand-up, one-handed, and two-handed animations (and later crouch-walk, run, take cover, draw, aim); inspect front, side, three-quarter, and back views.
- **Mitigation:** keep the holster close to the right hip under the coat; add suitable cloth / bone weighting or simplified cloth behavior; adjust coat collision or animation shape keys if needed.

### 6 — Modular armor destroys the base silhouette
- **Risk:** a plate carrier is too large or intersects the coat, and the character loses the intended school-tactical look.
- **Check:** compare equipped and unequipped silhouettes; verify the coat, skirt, and head stay readable.
- **Mitigation:** build armor as a separate mesh around the approved base model; keep each armor item's size and thickness inside a defined equipment envelope.

## Implementation constraints
- The character becomes a 3D model for Godot.
- The base character and equipment are modular.
- The ballistic vest is never permanently merged into the base character.
- The right-side handgun holster is part of the base outfit but stays hidden under the coat.
- The runtime rotates the 3D model instead of flipping asymmetric character art.
- Generated assets follow the approved matte, dark anime concept-art direction.

## Open decisions
- Final character name.
- Exact character height.
- Final gameplay camera distance / viewport size.
- Final collision capsule dimensions.
- Final palette of the subway base environment.
- The fourth sound event for the slice.
- Mute keys.
- Whether the first modular plate carrier can be equipped in this slice.
- Final menu music track and exact loop length.
- Exact scout robot design (later scenes).

---
## Revision history
<!-- Append here; do not rewrite version 1 above. -->
- **2026-10-07 — Following the storyboard revision:** the seat in ENV-BASE changes from "bench" to to be decided (a chair, a sofa, or something else), and CHAR-SIT becomes "sitting on the seat". UI-TAB-FULL now serves panels 4–5 (panel 5 is now the gameplay view with the tablet filling the screen). Panel 2 shows a status bar at the top left; it is a placeholder for now, and whether it needs a UI asset will be decided later.
- **2026-10-08 — Base greybox:** the `ENV-BASE` greybox is in `godot/base.tscn`: a 16 × 10 m room with a 3 m interior height, a floor, four walls, and a ceiling; a 6-step staircase leads to a 1.2 m platform (an invisible sloped collision box sits over the steps); two cool-colored ceiling lights; the test chair stands against the back wall. Claude built the greybox from CSG basic shapes. As the professor confirmed, assets Claude builds in code also count as generated assets, so it is in the `SOURCES.md` asset log (ENV-BASE-01).
- **2026-10-09 — Terminal sound effects:** the slice's four sound events are now the tablet terminal's four UI sounds. `SFX-TAB-BOOT` is replaced by `SFX-TERMINAL-POWER-ON`; `SFX-STEP` and `SFX-TAB-OUT` move to "planned for later". The generation process (including the rejected versions) is recorded in the `SOURCES.md` asset log and in `FRICTIONAL.md`; this entry records only the final use.

  | Asset ID | Category | Asset | Storyboard panel | Planned path | Status |
  |---|---|---|---|---|---|
  | SFX-TERMINAL-POWER-ON | Sound | Terminal power on: one clear "di" beep with short radio static / squelch texture | 3 | `assets/sfx/….ogg` | Accepted (`design/sfx_sound/sfx_power_on.flac`, not yet converted to OGG) |
  | SFX-TERMINAL-POWER-OFF | Sound | Terminal power off: the same sound family as power on, with a falling pitch | [to be confirmed] | `assets/sfx/….ogg` | Accepted (`design/sfx_sound/sfx_power_off.flac`, not yet converted to OGG) |
  | SFX-TERMINAL-CURSOR | Sound | Button press (`sfx_botton_press`): one low, short, rounded "doo" | [to be confirmed: 4–5] | `assets/sfx/….ogg` | Accepted (`design/sfx_sound/sfx_botton_press.flac`, not yet converted to OGG) |
  | SFX-TERMINAL-ERROR | Sound | Error: one short, higher-pitched, attention-getting "di" | [to be confirmed: 4–5] | `assets/sfx/….ogg` | Still being generated, not final |

  Event-to-sound map (replaces the SFX-STEP / SFX-TAB-OUT / SFX-TAB-BOOT rows of version 1):

  | Asset ID | Gameplay event that triggers it | What it sounds like | How double-triggering is prevented |
  |---|---|---|---|
  | SFX-TERMINAL-POWER-ON | Picking up the tablet at any time (from "not looking" to one-handed or two-handed) | One power-on sound | A new sound effect cuts off (interrupts) the previous one instead of playing on top of it. How one input plays exactly one sound will be filled in once the logic is written [to be confirmed] |
  | SFX-TERMINAL-POWER-OFF | Putting the tablet away at any time (back to "not looking") | One power-off sound | A new sound effect cuts off (interrupts) the previous one instead of playing on top of it. How one input plays exactly one sound will be filled in once the logic is written [to be confirmed] |
  | SFX-TERMINAL-CURSOR | Left mouse button on the tablet | One low, short button sound | A new sound effect cuts off (interrupts) the previous one instead of playing on top of it. How one input plays exactly one sound will be filled in once the logic is written [to be confirmed] |
  | SFX-TERMINAL-ERROR | Right mouse button on the tablet | One short, high warning "di" | A new sound effect cuts off (interrupts) the previous one instead of playing on top of it. How one input plays exactly one sound will be filled in once the logic is written [to be confirmed] |

  Version 1's predicted failure case 3 ("Tablet sounds fire twice") still applies: what it tests is whether the game code fires more than once for one input, which is a different thing from the multiple pulses / tremolo inside the Error audio during generation. All four sounds belong to the tablet; none of them is connected to the game yet.
- **2026-10-15 — Assignment 3: brief for three 3D assets**

  **Order, recorded honestly:** the chair (2026-10-07) and the tablet (2026-10-12) are first versions made for this assignment before this brief existed; Claude built both through the Blender MCP. This brief was written on 2026-10-15. On the same day, at my request, the tablet's triangle count was reduced and the third asset (two weapon crates) was made. So this brief is not a prediction written before any modelling, and some numbers below are measured values.

  **Common rules:** 1 Blender unit = 1 metre; Blender is Z-up; `.glb` files are exported with +Y Up. Each asset has its own folder (`design/item_resource/<asset>/`) holding its `.blend` and `.glb`, is modelled around the world origin, and has rotation and scale applied before export. Reference: **the character is 1.6 m tall**. **Furniture grid: 1 cell = 0.1 m** (my decision on 2026-10-15, for a grid-aligned furniture system); furniture length and width must be whole multiples of 0.1 m, and parts that stick out (handles and similar) count toward the footprint. Course limits: at most 6 basic shapes, at most 500 triangles, and flat-colour materials per asset.

  | | ENV-SEAT (chair) | PROP-TABLET (rugged military tablet) | CRATE-LONG "large crate" / CRATE-CUBE "small crate" (military weapon crates, cuboid / cube) |
  |---|---|---|---|
  | What it is in the game | The chair the character sits on in the start menu (panels 1–2); for real use, no longer just a test | The military tablet the character carries; held in the hand in panels 3–5 (core gameplay) | A kind of furniture: a storage crate the player will be able to build, and it holds items (small crate `small_box` storage grid 10 × 10, large crate `big_box` storage grid 20 × 10, length × width). Military weapon-crate style, opens and closes with open / close animations |
  | Where it appears | `base.tscn`, against the back wall | In the character's hands | In the subway base, built and placed by the player (the building system comes later) |
  | Size (width × depth × height, m) | 0.44 × 0.42 × 0.90, seat height 0.45 | 0.242 × 0.028 × 0.162 (built standing up; 0.028 is the thickness) | My requirement: one cuboid and one cube, the long crate twice the length of the cube. Large crate 1.0 × 0.5 × 0.4 (footprint 10 × 5 cells); small crate 0.5 × 0.5 × 0.5 (5 × 5 cells). Sizes include the handles and latches |
  | Why that size | A normal chair seat is 0.45 m, for a 1.6 m character. Whether the knees line up with the seat can only be checked once the character model is in | About an 8-inch rugged tablet (reference images `design/pad/tablet-ref-01..04.png` in the Assignment 2 folder); held with both hands by a 1.6 m character | The 0.5 m small crate sets the grid unit (1 cell = 0.1 m); the large crate is twice its length. The top is 0.4–0.5 m high, a little above the knee of a 1.6 m character |
  | Origin | Bottom centre; sits on the floor | Geometric centre. **Kept on purpose**: it does not get in the way of attaching it to the hand (my decision on 2026-10-15). Placed on a floor it sinks halfway; that is a known trade-off | Body: bottom centre, sits on the floor. Lid: origin on the back hinge, rotates about X |
  | Look | Block chair: seat, four legs, backrest slats, stretchers; matte dark grey | Dark green shell + black corner bumpers and strips + one large black screen (slightly glossy), so front and back are easy to tell apart (my request on 2026-10-12) | Military green (following the military green / dark direction I set for the tablet) matte shell, dark handles and latches (one handle on each end, two latches on the front); the body is hollow, so the inside shows when the lid is open. **My hand edit on 2026-10-15:** the latches raised to sit half on the lid and half on the body (so they read as latches that lock the lid), the end handles moved up (lower centre of gravity when carried); Claude rebuilt the large crate the same way |
  | Animation | None | None | `open`: lid from 0° to 100°; `close`: from 100° back to 0°. 15 frames each (24 fps, about 0.6 s) |
  | Triangle budget | ≤ 500 (first version 108, second version 72) | ≤ 500 (2026-10-12 version 804 → 2026-10-15 version 388) | ≤ 500 each (measured 88 each; still 88 in the second version) |
  | Shape count | Second version on 2026-10-15: 6 (seat, 4 legs, one backrest board; the two stretchers removed and the two backrest slats merged) | 21 boxes, **over 6**. I decided on 2026-10-15 to keep it as it is (I am happy with this version) | 6 (body, lid, 2 handles, 2 latches) |
  | Files | `design/item_resource/chair/chair.blend`, `chair.glb`; copied to `godot/assets/furniture/chair.glb` and used in `base.tscn` | `design/item_resource/tablet/tablet.blend`, `tablet.glb`; the 2026-10-12 first version `Pad_model.blend` is in the same folder | `design/item_resource/crate_long/`, `design/item_resource/crate_cube/` |
  | Build code | `tools/blender/build_chair.py` | `tools/blender/build_tablet.py` | `tools/blender/build_crate_long.py`, `build_crate_cube.py` |

  **Predicted failures and how I check them (A3):**
  1. **Over the course limits.** Too many shapes or triangles (the chair and the tablet are already over on shapes). Check: turn on Scene Statistics in Blender's status bar for the triangle count; count the `box(...)` calls in `build_*.py`.
  2. **Wrong origin, so the asset floats or sinks into the floor.** The chair's first version floated 6 cm (fixed on 2026-10-07); the tablet's origin is in the centre, so it sinks halfway, on purpose. Check: place it on a floor at y = 0 in Godot; a headless script prints the lowest y of the bounding box.
  3. **Lying on its side after export, or a scale that is not 1.** Blender is Z-up and Godot is Y-up. Check: a headless script prints the node scale and the bounding box; the height must be on Y and the scale 1, 1, 1.
  4. **Colours lost on export, or impossible to tell apart under the base's cool lighting.** The tablet's dark green and black are close; the military-green crates may blend into the dark walls. Check: look at each from the front, the back, and below under the lights in `base.tscn`.
  5. **Claude builds something more complex than asked.** The tablet's first version is the example: I asked for "a greybox blocked out with cubes" and got 21 bevelled parts and 804 triangles. Check: after every build Claude reports the shape count and triangles before I look at it.
  6. **The crate's open / close animation does not reach Godot, or the lid turns about the wrong axis.** Check: a headless script lists the AnimationPlayer's animations, plays `open` / `close` to the last frame and prints the lid's rotation; then I watch in the editor that the lid opens about the back hinge and does not pass through the body.
  7. **Furniture off the 0.1 m grid.** Handles or latches stick out and make the footprint bigger than whole cells (the first crates did: 0.56 × 0.515 and 1.26 × 0.515). Check: the headless script prints the bounding box; length and width must be whole multiples of 0.1. The second crate version on 2026-10-15 moved the handles and latches inside the footprint. When the lid is open it swings out behind the crate; that is not counted in the footprint for now.
- **2026-10-15 — Computer desks (project assets beyond the three A3 assets):** computer desks I asked for, tied to the game's computer gameplay. On the 0.1 m grid: the straight desk `computer_desk` takes 15 × 5 cells (1.5 × 0.5 m); the L-shaped desk `computer_desk_l` takes 15 × 10 cells (a 15 × 5 main desk along the back, and a 5 × 5 return coming forward from the right end, so that side is 10 cells in total). Desktop height 0.7 m (my choice), the computer-desk feature is a monitor riser along the back of the desktop (my choice), dark-grey metal desktop with dark legs and riser (my choice). To stay within 6 shapes, the L-shaped desk uses side panels instead of legs at its two ends. Files in `design/item_resource/computer_desk/` and `computer_desk_l/`, code in `tools/blender/build_computer_desk*.py`, asset log rows COMPUTER-DESK-01 / COMPUTER-DESK-L-01.
