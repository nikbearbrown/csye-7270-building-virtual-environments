# Build notes — planet-express-ship-muse

## What this is

A procedural Blender model of the Planet Express ship (Futurama), built from
5 reference photos of a physical model kit (teal hull, red cheatline stripe,
cream trim, wraparound cockpit glass, porthole row, tail fin with circular
PLANET EXPRESS logo, glowing rear thruster cluster, roof dome + periscope +
antenna, tricycle landing gear). It is an interpretive reconstruction, not a
scan. No part of the reference kit was traced or photogrammetry-processed.

## Method

- Fully scripted with Blender's Python API (`bpy`), run headless. No hand
  modeling, no sculpting.
- Hull: lathed from a Catmull-Rom-interpolated profile (13 control rings,
  110 sampled rings, 64 segments), nose toward +Y, slight nose droop.
- Red cheatline stripe, cream spine trim and tail-base trim: bands projected
  onto the hull surface along the hull normal.
- Cockpit: dark frame patch + glass patch + three mullions, all hull-following
  grid patches.
- Portholes: 8 (4 per side) — cream torus rings + dark glass discs placed on
  the hull by surface normal.
- Tail fin: extruded polygon; the PLANET EXPRESS roundel is a 1024px texture
  generated with Pillow (red planet, rocket, arc text), applied as decals on
  both sides of the fin.
- Engine: cream pod rings + dark face + 19 glowing thruster cells (1 center,
  6 inner, 12 outer) + cream rim torus.
- Details: roof dome + glass, periscope, antenna with glowing tip, 14 rivets
  along the spine trim, side strakes with red tip lights, side vents, hatches,
  tricycle landing gear with a nose ski-blade.
- Renders: Blender 4.2.3 LTS, EEVEE, 64 samples, 3-point studio lighting.

## Audit (measured from the .blend, not estimated)

- Mesh objects: 96
- Triangles: 51,416 (evaluated, modifiers applied)
- Materials: 11 (Cream, DarkGlass, DarkMetal, DarkTeal, Glass, HullTeal,
  LogoMat, MetalGray, StripeRed, ThrusterGlow, TipGlow)
- Bounding box: X 5.54 × Y 7.62 × Z 4.60 (Blender units; nose +Y, up +Z)
- `planet-express-ship.blend`: 5.0 MB (logo texture packed)
- `planet-express-ship.glb`: 1.5 MB, 96 meshes, 11 materials, 1 embedded
  texture (the fin logo). Flat PBR colours otherwise.

## Comparison rounds

1 render-vs-reference comparison round from matched cameras (side, rear,
front three-quarter), after the single scripted build pass. No geometry was
changed as a result of the round; the findings below are recorded as known
limitations instead.

## Known limitations

- The red cheatline reads salmon-pink under the studio lighting; the
  reference stripe is a deeper red.
- The cream spine trim on the hull top renders as a broad pale sheet and
  looks draped rather than paneled.
- Hull reads slightly blimp-like; the reference kit has a sharper teardrop
  with a more pinched tail.
- Landing-gear stance is simplified; the reference kit sits on a display
  stand, so the gear is partly interpretive.
- The fin logo is a flat decal, not raised paint.
- No interior; cockpit glass is opaque dark glazing.
