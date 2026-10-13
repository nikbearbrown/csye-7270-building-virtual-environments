# walker-3d-particles: capture notes

**What this is.** A real windowed Godot 4.7.2 Movie Maker run of the 3D Particles showcase, recorded 2026-10-09 at a fixed 30 fps from a scratch copy. It uses the Forward+ renderer on Metal. The source at `/Users/bear/Documents/CoWork/bear-textbooks/books/walker-3d-particles/godot` was not touched. The copy got only the capture autoload and a 1920x1080 window.

## Scripted input
Starting at frame 90, the Right arrow key (`InputEventKey`, which the scene reads as `ui_right` = "Next") was tapped every 60 frames, 13 times in total, stepping through all 14 particle testers. A screenshot was taken 50 frames after each switch, once the camera had glided over.

## Files (all 1920x1080)
The scene draws each tester's name at the bottom of the frame:
- 01 CPU Particles Force Field
- 02 CPU Particles Explosion
- 03 GPU Particles Fire
- 04 GPU Particles Smoke
- 05 GPU Particles Attractor
- 06 GPU Particles Turbulence
- 07 GPU Particles Collision
- 08 GPU Particles Collision Global Coords
- 09 GPU Particles 3D Foam
- 10 GPU Particles Trails
- 11 GPU Particles Subemitter At End
- 12 GPU Particles Subemitter On Collision
- 13 GPU Particles Collision SDF
- 14 GPU Particles Collision Heightfield

The PNG names use the scene's node names, for example `03-GPUParticlesFire.png`. The node for 01 is named "CPUParticlesForceField", and the on-screen label reads "Cpu Particles Force Field".

`walker-3d-particles-clip.mp4`: 8.0 s, H.264, 30 fps, no audio. Movie frames 90–330: the camera glides from Explosion to Fire to Smoke to Attractor (Next pressed at 0, 2, 4 and 6 s), with the particles animating throughout.

**Problems:** none. The project has no sound.
