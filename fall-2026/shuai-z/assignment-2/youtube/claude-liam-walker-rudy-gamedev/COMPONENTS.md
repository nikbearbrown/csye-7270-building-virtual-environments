# COMPONENTS — Walker Rudy, Wired In.

The game folder `game/` at `3b7aa1c`: 114 authored files (`.uid` identifiers and `.godot/` excluded by the contract), every one assigned to a component in `gamedev-evidence.json`.

| Component | Files | Beats | What it does |
| --- | ---: | --- | --- |
| `app-flow` | 4 | B02, B04, B06, B07, B26, B27, B28, B29, B31, B32, B34, B35 | Main (app/main.gd) runs Level 1's states TITLE → PLAYING → DYING → COMPLETE: Enter on the title, the kill line and the fall, the respawn at a checkpoint or the start-over, the teleport circle and the end card. SystemKeys reads Esc, M and N while paused. project.godot holds the input map, the autoloads and the physics layer names. |
| `rudy-controller` | 2 | B08, B09, B10, B11, B12, B17, B22, B24, B25 | Rudy (CharacterBody2D): run, turn on the spot, jump with separate rise/fall gravity, stomp bounce, the sword swing and its timed hitbox, take_hit (gear first, then hearts), invulnerability, knockback and modes. |
| `rudy-art` | 36 | B12, B13, B14, B15, B16, B16R, B17, B18, B19 | Rudy's sixteen generated frames on one canvas, chosen by pose ID (rudy.gd _pick_pose → rudy_look.gd), with the matting record in frames.json; the outline shader and its material that add the 4 px outer line to Rudy, goblins and spikes. |
| `level` | 14 | B05 | Level 1's layout scene and its painted layers: the far sky/castle layer at 0.0218 of the camera, the repeated fields at 0.4, the ground blocks that size their own collision and draw the tiles and cliff pieces (env.json). |
| `hazards-checkpoints` | 15 | B05, B17, B26, B27, B29, B34, B35 | Spikes (a hurt box narrower and lower than the art), the waystone checkpoint (lights once, halo and ring drawn by code) and the teleport circle (column of light drawn by code); props.json gives their art origins. |
| `goblin` | 8 | B05, B20, B21, B22, B23, B28 | The goblin Area2D: patrol, a 40×118 box queried every tick, stomp versus hit decided by STOMP_MARGIN, reset after a death; two walk frames and a squashed frame. |
| `sword-pickup` | 5 | B05, B22, B23, B24, B25, B28 | The sword-and-shield pickup (taken once, hidden, reset after a death) and FlyingGear, the picture thrown off when a hit knocks the gear away. |
| `audio` | 17 | B04, B10, B11, B17, B21, B26, B30, B31, B32, B33, B34 | Sfx, the one entry point for six sounds (one player each, counted per ID), and Music, the looping theme with named dips (deepest wins), ramps and the fade-out; the Music and SFX buses. |
| `hud` | 9 | B04, B06, B07, B09, B29, B31, B33, B34, B35 | The HUD: title over the opening, hearts, the debug line (F1), the black fade, 'Paused' and the end card. |
| `tests` | 4 | B36, B37 | 141 headless checks (tests/checks.gd) and the project's own screenshot/mix capture tool (tests/capture.gd). Both use test-only teleports to set up cases; the film's footage comes from a separate input-only driver. |

## Code → result pairs

| Code beat | Source | Result beat | Observed |
| --- | --- | --- | --- |
| B06 | `app/main.gd:98–110` | B07 | Enter at frame 77; the title fades and the hearts fade in; Rudy starts running at frame 85 on the same screen. |
| B08 | `content/rudy/rudy.gd:203–215` | B09 | Debug line shows x 300 through both taps (frames 82 and 104); the run starts at frame 125. |
| B10 | `content/rudy/rudy.gd:217–227` | B11 | Jump in place at frame 158 plays one SFX-JUMP; the key held 90 ticks from frame 195 gives one takeoff and one sound (driver check). |
| B12 | `content/rudy/rudy.gd:297–309` | B13 | Debug line reads CHAR-RISE after takeoff at frame 272 and CHAR-FALL from the top of the arc; he clears SpikesA. |
| B16 | `content/rudy/frames/frames.json:108–117` | B16R | game/content/rudy/frames/CHAR-HURT.png at its 410×386 canvas, enlarged 4× on a dark backing: transparent background, the figure from CHAR-HURT-02 scaled ×0.1816, soles at the 205,370 origin; no outline pixels in the file. |
| B18 | `systems/art/outline.gdshader:31–41` | B19 | Engine frames at 4K, Rudy at x 664 over the wheat: with width 8 the dark line separates hair from wheat; with width 0 the hair and the wheat run together. |
| B20 | `content/goblin/goblin.gd:100–109` | B21 | Frame 165: Rudy's capsule lands on GoblinA's 40×118 box from above; the squashed frame shows, he bounces; one SFX-STOMP. |
| B22 | `content/rudy/rudy.gd:239–247` | B23 | Frame 237: slash pressed with GoblinB 115 px ahead; the hitbox shows in front of Rudy and GoblinB is squashed; one SFX-SLASH. |
| B24 | `content/rudy/rudy.gd:134–146` | B25 | Frame 243: GoblinB touches Rudy in the sword form; FlyingGear spins up and fades; hearts stay at 2; SFX-HURT. |
| B26 | `app/main.gd:116–124` | B27 | Frame 362 the waystone lights (ring, halo); frame 393 he crosses the kill line (hearts 2 → 1, SFX-HURT); frame 432 he is back in control at x 4120. |
| B28 | `app/main.gd:125–135` | B29 | Frame 490: GoblinB takes the last heart (CHAR-DEFEAT); after the fade Rudy is at x 300 with 3 hearts and the waystone is dark (driver check). |
| B30 | `systems/audio/music.gd:95–103` | B31 | Frames 313–375: tree paused, 'Paused' over a dimmed screen; log music_db −12.0 while paused, 0.0 after. |
| B32 | `app/system_keys.gd:18–29` | B33 | Frame 408 M mutes the Music bus; the jump at 427 is audible. Frame 499 N mutes SFX; the jump at 518 is silent and the debug line's jump count rises. |
| B34 | `app/main.gd:184–195` | B35 | Frame 452 the circle is reached (SFX-PORTAL, music fades); the end card shows at 522; Enter at 582 reloads straight into play. |
| B36 | `tests/checks.gd:1328–1339` | B37 | Recorded output of the checks on an isolated copy of game/ at 3b7aa1c: 141 PASS lines, 'all checks passed', exit 0; the muted-route line reports 733 ticks at x 7118.076 both ways. |

## Exclusions

- `.DS_Store`: macOS Finder metadata, gitignored; not part of the game.

## Not shown as code, and why

- `level_1.tscn`, `main.tscn`, `project.godot`: shown as reconstructed scene trees with their real positions and names (B04, B05), not as excerpts.
- `backdrop.gd`, `ground_segment.gd`, `hearts.gd`, `hud.gd`, `spikes.gd`, `waystone.gd`, `portal.gd`, `sword_pickup.gd`, `flying_gear.gd`, `rudy_look.gd`, `sfx.gd`: their behaviour is shown in play and named in narration or source notes; the film excerpts the lines that decide state.
- `tests/capture.gd`: the project's own screenshot/mix tool; it teleports Rudy, so none of its output is used as gameplay footage.
- Texture, audio and `.import` files: inventoried and hashed; the film shows the generated art in play and one asset's full trace (CHAR-HURT).
