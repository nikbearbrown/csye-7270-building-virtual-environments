# walker-3d-lights-and-shadows: capture notes

**What this is.** A real windowed Godot 4.7.2 Movie Maker run of the 3D Lights and Shadows showcase, recorded 2026-10-09 at a fixed 30 fps from a scratch copy. It uses the Forward+ renderer on Metal, with omni, spot and area lights, PCSS shadows and projectors. The source at `/Users/bear/Documents/CoWork/bear-textbooks/books/walker-3d-lights-and-shadows/godot` was not touched. The copy got only the capture autoload and a 1920x1080 window.

## Scripted input
Starting at frame 90, the Right arrow key (`ui_right` = "Next") was tapped every 60 frames, 14 times in total, stepping through all 15 testers. A screenshot was taken 50 frames after each switch. The settings panel (Enable Sun off, Animate Lights on, 4096x4096 shadows) was left at the scene's defaults and was not clicked.

## Files (all 1920x1080, tester name drawn at the bottom)
1. `01-OmniLightNoShadows`
2. `02-OmniLightWithShadows`
3. `03-OmniLightWithPCSSShadows`
4. `04-OmniLightWithProjector`
5. `05-OmniLightAttenuation`
6. `06-SpotLightNoShadows`
7. `07-SpotLightWithShadows`
8. `08-SpotLightWithPCSSShadows`
9. `09-SpotLightWithProjector`
10. `10-SpotLightAngleAttenuation`
11. `11-AreaLightNoShadows`
12. `12-AreaLightWithShadows`
13. `13-AreaLightWithPCSSShadows`
14. `14-AreaLightWithTexture`
15. `15-AreaLightShapes`

Every shot shows the checkered torus and cones under that light, with the scene's settings panel at top left.

`walker-3d-lights-and-shadows-clip.mp4`: 8.0 s, H.264, 30 fps, no audio. Movie frames 90–330: Omni With Shadows, then PCSS Shadows, then Projector, then Attenuation, with the animated lights moving.

**Problems:** none. The project has no sound.
