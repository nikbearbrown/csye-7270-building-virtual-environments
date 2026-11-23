# Capture record

## Fixture strips (reused, made by the user before this film; not gameplay)
- captures/tablet_raise/r2-front (B08), r1-front + r2-front grab frames (B14), captures/pixel_head/r0 (B04). Labelled FIXTURE on screen. r0 and r0-front were read but not shown (r0/r1 labels are one frame early, see TUNING r1).

## New scripted-input capture (play-01)
- Copy: `git archive 42d6cc0d` of the game package's godot/ extracted to <film-work>/a7/game/; `--headless --import` exit 0. The course repository was not modified and the user's Godot editor was not opened or closed.
- Script: <film-work>/a7/capture-tools/tablet_capture.gd (+ tablet_capture.tscn), kept outside the copy; a runtime copy was placed in the copy's film_capture/ folder. Copy included here as capture-tools/tablet_capture.gd.
- It loads base.tscn, turns the player camera 180 degrees around the character (as tablet_raise_preview.gd --front does), and sends Tab through Input.parse_input_event (InputEventKey keycode and physical_keycode KEY_TAB). Short press = released before 0.4 s; long press = held 0.4 s (player_controller.gd).
- Run: Godot 4.7.2-stable console, windowed, Forward+ / D3D12, Movie Maker 30 fps (`--write-movie`, `--fixed-fps 30`); output folder created first. Windows display scaling made the frames 2048 x 1152; ffmpeg lanczos scaled them to 1920 x 1080, libx264 crf 18.
- Result: play-01.mp4, 26.37 s, 791 frames. SHA-256 c5a0529e118f7b1052c365baf06355cb7324ef990911f1ede3f14c0f0c81ea81.

## Known issues in the capture
1. After the first two-hand hold the character turns to the camera direction, so from about 14.1 s the camera shows her back; the label says so.
2. In the two-hand state the game uses its first-person view; only the tablet is visible, no hands.
3. In the first ~7 s the camera yaw drifts slowly (cause not investigated).
4. A small dark rectangle near the head is level art / UI, not an artefact of the capture.

## Timeline (from the engine log)
```
# play-01.mp4 timeline (30 fps; time = movie frame / 30). Scripted input, not a playtest.
# time_s	frame	event
0.000	0	start: character at waist idle (tablet on hip), front view
0.000	0	  [engine] hold=NONE state=hip clip_pos=0.0000 fading_from= lit=false raising=false
1.000	30	1. Tab down (short press): uninterrupted one-hand raise
1.067	32	1. Tab up -> SHORT: raise_1h starts
1.100	33	  [engine] hold=ONE_HAND state=raise_1h clip_pos=0.0000 fading_from= lit=false raising=true
1.767	53	  [engine] hold=ONE_HAND state=hold_1h clip_pos=0.0000 fading_from= lit=false raising=true
3.333	100	2. Tab down (short press): put back to waist
3.400	102	2. Tab up -> SHORT: one-hand -> waist (hold_1h -> hip, 0.2 s blend)
3.433	103	  [engine] hold=NONE state=hip clip_pos=0.0000 fading_from=hold_1h lit=false raising=false
5.000	150	3a. Tab down: raise again
5.067	152	3a. Tab up -> SHORT: raise_1h starts
5.100	153	  [engine] hold=ONE_HAND state=raise_1h clip_pos=0.0000 fading_from= lit=false raising=true
5.133	154	3a. Tab down: interrupt in ANTICIPATION
5.200	156	3a. Tab up -> SHORT at raise clip ~frame 4 (anticipation): put back to waist
5.233	157	  [engine] hold=NONE state=hip clip_pos=0.0000 fading_from=raise_1h lit=false raising=false
7.000	210	3b. Tab down: raise again
7.067	212	3b. Tab up -> SHORT: raise_1h starts
7.100	213	  [engine] hold=ONE_HAND state=raise_1h clip_pos=0.0000 fading_from= lit=false raising=true
7.333	220	3b. Tab down: interrupt in ACTIVE
7.400	222	3b. Tab up -> SHORT at raise clip ~frame 10 (active): put back to waist
7.433	223	  [engine] hold=NONE state=hip clip_pos=0.0000 fading_from=raise_1h lit=false raising=false
9.000	270	3c. Tab down: raise again
9.067	272	3c. Tab up -> SHORT: raise_1h starts
9.100	273	  [engine] hold=ONE_HAND state=raise_1h clip_pos=0.0000 fading_from= lit=false raising=true
9.633	289	3c. Tab down: interrupt in RECOVERY
9.700	291	3c. Tab up -> SHORT at raise clip ~frame 19 (recovery): put back to waist
9.733	292	  [engine] hold=NONE state=hip clip_pos=0.0000 fading_from=raise_1h lit=false raising=false
11.333	340	3d. Tab down: raise again
11.400	342	3d. Tab up -> SHORT: raise_1h starts
11.433	343	3d. Tab down and HOLD: long press will fire 0.4 s later
11.433	343	  [engine] hold=ONE_HAND state=raise_1h clip_pos=0.0000 fading_from= lit=false raising=true
11.833	355	3d. (expected) LONG fires at raise clip ~frame 13 (active): raise -> two-hand
11.867	356	  [engine] hold=TWO_HAND state=hold_2h clip_pos=0.0000 fading_from=raise_1h lit=false raising=false
12.167	365	3d. Tab up (long press already counted)
14.000	420	4a. Tab down (short press): two-hand -> one-hand
14.067	422	4a. Tab up -> SHORT: hold_2h -> hold_1h
14.100	423	  [engine] hold=ONE_HAND state=hold_1h clip_pos=0.0000 fading_from=hold_2h lit=false raising=false
16.000	480	4b. Tab down and HOLD: one-hand -> two-hand
16.433	493	  [engine] hold=TWO_HAND state=hold_2h clip_pos=0.0000 fading_from=hold_1h lit=false raising=false
16.667	500	4b. Tab up (LONG fired ~0.4 s after down)
18.667	560	4c. Tab down and HOLD: two-hand -> waist
19.100	573	  [engine] hold=NONE state=hip clip_pos=0.0000 fading_from=hold_2h lit=false raising=false
19.333	580	4c. Tab up (LONG fired ~0.4 s after down): hold_2h -> hip
21.333	640	4d. Tab down and HOLD: waist -> two-hand directly
21.767	653	  [engine] hold=TWO_HAND state=hold_2h clip_pos=0.0000 fading_from=hip lit=false raising=false
22.000	660	4d. Tab up (LONG fired ~0.4 s after down): hip -> hold_2h
24.000	720	4e. Tab down and HOLD: two-hand -> waist
24.433	733	  [engine] hold=NONE state=hip clip_pos=0.0000 fading_from=hold_2h lit=false raising=false
24.667	740	4e. Tab up (LONG fired): hold_2h -> hip
26.333	790	end

```
