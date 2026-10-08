# Components of the slice, and where the film shows each

| Component | Lives in | What enters | What changes | What the player sees | Beat |
|---|---|---|---|---|---|
| World orchestrator | `scripts/world.gd` | input, meter signals | `is_inverted`, geometry groups, room visibility | the room becomes the other room | B08 |
| Gravity inversion | `scripts/player.gd` | `_gravity_dir` | `up_direction` | he falls upward and stands on the ceiling | B09 |
| Meters | `scripts/meters.gd` | contact cost | `recognition`, `days_left` | nights counter tears; relic dots fill | B07 |
| Relics | `scripts/contact_point.gd` | proximity + key edge | `_ever_touched`, cooldown | the light goes out; the box plays | B07 |
| Audio | `scripts/audio.gd` | signals only | nothing in game state | nine sounds, two scores, ducking, hush | B13, B18 |
| HUD | `scripts/hud.gd` | meter signals | labels, cues, frost | nights, relics found, key prompts | B14 |
| Child | `Child` + `CHILD_POSES` | recognition | which of three poses | she turns further toward the room | B07 |
| World-dependent solids | `solid_in_memory` / `solid_in_truth` | flip | collision layers | his shelf blocks the memory only | B05 |
| Floor gaps | `FloorSeg0–3`, `LostAbove` | position | a night spent | he falls, and is set down again | B14 |
| Automated check | `tests/test_sound_triggers.gd` | scripted input | counters only | 13 assertions | B19 |

**Not built, and shown as such:** the self-correcting hallway and the cellar door
(storyboard panels 5 and 6) appear only as drawings, labelled *a later night*.
