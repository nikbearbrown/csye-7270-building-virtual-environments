# RIFF — gameplay observations (capture/run-01)

Riffs are on what the capture shows, inspected frame by frame (and against the frame log) before writing. Scripted input, not a human playtest; how the clips read in play was judged by the author in the running game (TUNING.md, TEST-REPORT.md "Human checks").

| Artifact + frames | Visible observation | Interpretation and source | Narration (beat) | Next experiment |
|---|---|---|---|---|
| run-01 0–20 | the mage idles at x 60; both cave walls glow orange and the glow breathes; embers drift up | the flicker clip on two PointLight2D nodes (`cave_lights.tscn`), embers (`embers.tscn`) | B03, B24 | — |
| run-01 20–117 | the run: four cells (contact, down, passing, up) at 6, 6, 6, 7 ticks, then 5, 6, 6, 7 per loop | a discrete frame track at 0.1 s keys; the clip wraps on the tick it reaches 0.4 s (`player.tscn` 97–100) | B03, B11 | in-betweens for the planted foot (FRICTIONAL.md "Still open") |
| run-01 118–152 | D released: IDLE; D again: RUN from cell 0 at 153 | `_set_state()` plays the clip from 0 on a state change | B03 | — |
| run-01 301–346 | Space: RISE 301, FALL 323; the landing tick 346 shows RUN, cell 0 | the same rule after a jump (edges check "run → jump → land → run") | B03, B13 | — |
| run-01 880–932 | the wolf switches to the rig on the tick it sees the mage (880), crouches, then stretches and dashes left (911); ghosts appear every 3 ticks, up to 6 alive (926); the dash ends short of the mage, who stepped back | the lunge clip from frame 0 on GROWL entry; LUNGE 22 ticks at 220 px/s; afterimage every 3 LUNGE ticks (`wolf.tscn` 256–258) | B04, B25 | — |
| run-01 933–970 | the wolf settles (overshoot then neutral); one tick of PATROL (969) and a new growl at clip frame 0 (970) as the mage runs past | the second alignment fix (`process_physics_priority = -1`) holding in play | B04, B18 | — |
| run-01 970–1022 | during the growl the wolf turns to face the mage, now on its right; the rig mirrors; it lunges right and hits her at 1009 (hurt image, HP 4) | `_face_target()` each GROWL tick; Facing.scale.x mirrors the whole rig (F5 avoided: Facing and Rig are separate nodes) | B04 | — |
| run-01 1528–1549 | the click at 1530: the fireball leaves the staff on growl tick 2 and hits on tick 21; the wolf flashes and goes straight to recovery at clip frame 53; no dash | the growl cancel (`wolf.gd` 158–162) and the first alignment fix | B05, B18 | a later click, around growl tick 12, to see the window's edge in play (growl_window.png) |
| run-01 1549–1584 | the hitbox never arms; the mage steps out of sight; PATROL at 1584 | `monitoring` false on every frame (frame log) | B05 | — |
