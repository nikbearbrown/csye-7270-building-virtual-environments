# FRICTIONAL — Assignment 5

My Assignment 3 log is in `../assignment-3/FRICTIONAL.md`.

## Entries

<!-- One entry per work session, newest last. Copy the block below. -->

### 2026-10-28 to 2026-10-29 — The tablet on the character, the raise / lower animation, the two-handed tablet camera, and the A5 test wrapper and baseline

- **Date and what I was working on:** 2026-10-28 and 2026-10-29. Preparing the tablet logic for A5: attaching the tablet model to the character, placing it on the hip or in the hand by the `TabletHold` state, and making the screen findable from code on its own. Then starting A5: adding `scripts/run-test.sh` and recording the baseline. The humanoid body, the player brain, the intent and the tablet's three states were written in earlier sessions (2026-10-23 to 2026-10-27); this is their first upload.
- **I tried / expected:** The tablet sits under `Visual`; on the hip when "not looking at the screen", in the hand for one-handed / two-handed (I set the positions in the editor); every character has its own tablet; the screen is a separate Screen mesh in `tablet.glb` whose material can be changed on its own.
- **What happened:** `tablet.glb` has no separate Screen mesh: `build_tablet.py` joins every part into one `PROP_Tablet`, and the screen is only its surface 1, with its own material. Claude first wrote code that found the screen by material name; I pointed out that this is a detection that only needs to run once and proposed a very thin plane in front of the screen instead. `Screen` is now a 0.18 × 0.108 m QuadMesh 1 mm in front of the model's screen. A headless check showed that the two tablets' `Screen` nodes are separate, but the material in the prefab is **one object shared by both** (it printed `true`). With the tablet in both hands, where it appeared on screen depended on the view pitch before raising it; Claude made the camera level while the tablet is held in both hands. The first version was still 11.9° off (the eye offset turned with the pivot); after the fix it was 3.8° off at a pitch of 0. I then asked to look down at the tablet slightly, and the default became -20°; after I adjusted the slot, the tablet measured 0.7° off the centre of the view, 0.10 m from the eye, with 2.2° between the screen's facing and the line of sight. The raise / lower move took 0.367 / 0.350 / 0.354 s at 30 / 60 / 144 fps (set to 0.35 s). Known issue: moving straight from the hip to the two-handed slot passes through the body. `run-test.sh` on `a3_asset_check.gd` at 60 fps: 55 PASS, 0 FAIL, exit 0; run once with a test file that does not exist: exit 1.
- **What I did:** Built the prefab `tablet_device.tscn` (`Model` + `Screen`) in the editor, added three slots under `Visual` (`TabletHipSlot` on the left hip, `TabletOneHandSlot` on the left, `TabletTwoHandSlot` in front of the eyes) and positioned them myself; fixed the Screen plane being turned 180° around Z; renamed `human model` to `human_model`; moved `TabletDevice` under `Visual`; asked for the camera to look down slightly while the tablet is held in both hands; asked for a small black box (`UpMarker`) to confirm the tablet's orientation. Decided for A5: the screen glows in ONE_HAND and TWO_HAND and not in NONE; the glow colour is `#E6F7F7` (it looks like the image of a modern night-vision device); each tablet gets its own material copy through the material's Local To Scene; the second shader goes on the crates as wear.
- **What Claude or another person contributed:** Claude Code (Claude Opus 5.5) wrote the tablet position and move code in `humanoid.gd`, the camera-levelling code in `player_controller.gd`, and `tablet_device.gd`; added `UpMarker` to the scene at my request; ran all the headless checks above; wrote `scripts/run-test.sh` from the assignment's template (two changes: it detects the project folder, and prefers `godot_console`); ran the baseline; and translated the uploaded scripts' comments into English.
- **What I understand now / still do not understand:**
- **Evidence and next step:** `walker-survival-shooting/godot/characters/human/humanoid/humanoid.gd`, `humanoid.tscn`, `godot/characters/human/player/player_controller.gd`, `godot/items/tablet/tablet_device.tscn`; `walker-survival-shooting/scripts/run-test.sh`; baseline log `walker-survival-shooting/logs/a3_asset_check_60fps.log`. Next: write and commit the A5 section of CHANGE-BRIEF, then write the screen-glow shader.

---

## GitHub pushes

| Date | Commit note |
|---|---|
| 2026-10-29 | Start Assignment 5: the Godot project as the A5 starting point (character body / brain and tablet logic), `scripts/run-test.sh`, and the 60 fps baseline (a3_asset_check: 55 PASS) |
