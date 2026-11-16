# Signal Garden asset sources

- `claude-mascot.glb`: byte-identical copy of this repository's `assets/claude-3d/claude_mascot.glb`, imported inside the Godot root. Original Blender source stays there. Its original proportions derive from Bear's Brutalist ClaudeMascotScene; see the original asset README. No new model generation is claimed.
- `gate-color.png`: 64×64 RGB stripes authored by `scripts/garden-textures.py`; albedo/color role.
- `gate-roughness.png`: 64×64 RGB grayscale stripes from the same script; red-channel roughness/data role, values 102 and 216. It is not a normal map. No image model, third-party texture or paid service was used.
- Particles: original low-poly SphereMesh resources in the two effect scenes; no sprite texture. Colors are vertex colors on unshaded materials.
- Motion: new Godot AnimationLibrary generated from readable keys in `mascot-rig.gd`, acting on the existing rig. This does not bake or replace the Blender actions. Four clips, not all 18 historical 2D poses.
- Audio: original sine waves made by `sound.gd` with a 10 ms attack and 40 ms release for event tones; 110 Hz, 2-second ambient loop. Temporary test assets, not Assignment 2 art/music. No sample library or recorded person.

The original mascot's rights and brand attribution remain as documented in the parent repo. This file does not grant new rights to third-party character branding.
