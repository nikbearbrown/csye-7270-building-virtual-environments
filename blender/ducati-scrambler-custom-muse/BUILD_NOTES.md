# BUILD_NOTES.md — ducati-scrambler-custom-muse

## Subject
Green Ducati custom (scrambler/cafe-racer). Reference: 13 photos in
`~/workspace/user/media_library/image/` (hero: `a0/a0082119...jpg`, full
right-side 3/4 view with correct "DUCATI" tank script) plus a turnaround
sheet. Real-world scale ~2.1 m long, ~1.1 m tall.

## Dimensions used (meters, Blender units)
- Wheelbase: 1.44 (rear axle x=-0.72, front axle x=+0.72)
- Front wheel: tire outer radius 0.33 (torus R=0.27 + tube 0.06), rim r=0.19
- Rear wheel: tire outer radius 0.345 (torus R=0.28 + tube 0.065), rim r=0.20
- Axle height: 0.33 (front), 0.345 (rear)
- Fuel tank: ellipsoid 0.74 x 0.35 x 0.30, center (0.14, 0, 0.865), teardrop-shaped
- Seat: 0.46 long, center (-0.30, 0, 0.845)
- Handlebar: y +/-0.34, z 1.045
- Overall (audited): 2.10 x 0.82 x 1.15 m (x=length, y=width, z=height)

## Mesh / material counts (from audit_blend.py, not invented)
- Mesh objects: 140 (v2; v1 was 94)
- Triangles (evaluated): 19,206 (v2; v1 was 14,032)
- Materials: 14 (v2; v1 was 12 — added RedShock, ClutchBadge)
- Overall (audited): 2.10 x 0.82 x 1.06 m (x=length, y=width, z=height)
- Textures: DUCATI script decal (PIL-drawn, packed in .blend)
- .blend: 2.4 MB · .glb: 1.4 MB (both under limits)

## Method
Fully procedural Blender Python (bpy), Blender 4.2.0 headless (EEVEE-Next).
No sculpting, no imported meshes. Every part is a primitive (torus, cylinder,
sphere, tube, curve) shaped in code:
- Wheels: torus tire + 78 instanced knobby tread blocks + 20 spokes + hub +
  brake disc (front: gold, drilled via boolean holes)
- Trellis frame: cylinders between 3D node pairs
- Tank: UV sphere, non-uniform scale, vertex-level teardrop shaping, subsurf
- DUCATI script: drawn with PIL (DejaVu Sans, letter-spaced) on transparent PNG,
  applied as a shrinkwrapped decal plane on each tank flank. The reference
  close-ups have garbled AI-generated lettering, so the script was redrawn
  clean rather than traced.
- Exhaust: bezier curve tube (VECTOR handles) + tapered cone muffler
- Headlight: cylinder bucket + chrome torus rim + lens + grille (2 torus rings
  + 7 bar tubes)
- Fenders: cylinder arcs cut by vertex-angle selection
- Chain: instanced links along a path; sprockets: cylinders with teeth

## Comparison rounds (render -> side-by-side vs reference -> harsh judge -> fix)
1. Initial build. Killed mid-render: tank rendered white (metallic 0.85 washing
   out under studio lights), exhaust too fat/chrome, seat pink, fender/headlight
   oversized, mirrors lollipops.
2. Fixes applied (green metallic 0.25, darker leather, slimmer rerouted exhaust,
   smaller fender/headlight/mirrors, teardrop tank). Blocked by the invisible-tank
   bug (see below).
3. Tank bug fixed (rebuilt tank object). First clean full render. Judged vs hero:
   tank too small/high, exhaust arced through the bike, muffler a white rocket,
   seat too orange, headlight a black blob.
4. Tank enlarged/lowered, fender rebuilt with angle-cut code, exhaust rerouted
   lower, seat darkened, headlight rim enlarged. Fender cut had a select-all bug
   (deleted everything); fixed with deselect-first.
5. Hero color pass: tank to deep green, rims silver->already, fork lowers chrome
   (reference shows chrome sliders), exhaust VECTOR handles to kill bezier
   overshoot, studio lights softened (900->650 key) to stop washout.
6. Muffler realigned to pipe axis, tank darkened further.
7. (final v1) Full 8-view render + .blend save + .glb export.

### The invisible-tank bug
The fuel tank (healthy mesh: 610 verts, 640 polys, outward normals, correct
bounds/location) rendered as a faint ghost while every other part rendered fine.
Ruled out: material, mesh data, custom normals, subsurf, decals, duplicate
objects. A fresh sphere at the same location with the same material rendered
fine, so the tank object was rebuilt from scratch (same shaping code, which an
isolated test proved innocent). Root cause of the original object's state was
never isolated; the rebuild rendered correctly and the shaping was re-applied
to it. Noted here so the mystery is on the record.

## v2 refinement pass (2026-10-19) — "keep refining toward close-looking"
Bear judged v1 a clean stylized asset but not a close likeness. Fixes, in
priority order:
1. PROPORTIONS: lowered the body mass (tank center 0.865->0.80, seat
   0.845->0.80), wheelbase 1.42->1.44 m, wheels 0.33->0.32 radius. Wheels kept
   near reference size (650 mm OD); the "oversized" read came from the body
   sitting too high, not the wheels being too big.
2. TANK: rebuilt longer (0.84 span), lower, flatter top line, tail tucking under
   the seat nose, sitting down into the frame.
3. TRELLIS: tube radius 0.016->0.0125 (25 mm), frame narrowed (y +/-0.075),
   18 tube runs (was 11) with triangulated bays wrapping the engine; top rails
   run from the steering head back just under the tank's top edge.
4. ENGINE: L-twin — crankcase + two finned cylinders (front near-vertical,
   rear laid back 42 deg), 9-fin stacks per cylinder, round clutch cover +
   badge, left-side cover. Fills the frame; no more dead air.
5. EXHAUST: headers per cylinder (0.016 r) into a collector, rising mid-pipe,
   substantial tapered muffler (115 mm max dia) with torus end-cap ring, dark
   outlet, 6 rivet dots, frame mounting bracket.
6. DECAL: root-caused the v1 invisible-decal bug — decal planes were rotated
   68 deg instead of 90 deg, slicing into the tank. Fixed to exactly +/-90 deg,
   subdivided planes + PROJECT shrinkwrap, simplified alpha material using
   Blender 4.2's surface_render_method. Verified rendering in test.
7. FRONT END: corrected fork geometry for the lower steering head, front brake
   line (bezier), round instrument with glass face; longer chrome sliders per
   the new fork close-up refs.
8. RED rear shock coil-over (prominent in references), repositioned taillight.

### The transform_apply bug (root-caused this pass)
Blender 4.2's `bpy.ops.object.transform_apply(scale=True)` ALSO bakes the
object's location into the vertices (object ends at origin). The tank/seat
shaping code assumed local coords, so the tank got crushed into the engine
(world z 0.36-0.48 instead of ~0.80) and the seat taper/rotation used wrong
pivots. This also explains v1's "tank too small" (it was being squashed).
Fix: never transform_apply positioned parts — shape in local coords, bake
dimensions into vertices, set `location` only. Tank and seat rewritten to
this pattern.

### Render engine note
EEVEE-Next cannot initialize headless here (no libEGL.so.1 after the VM
restart; Xvfb/GLX path also requires it). Switched all renders to Cycles
(CPU, 64-96 samples + OpenImageDenoise). Slower but robust; arguably better
for likeness judgment.

### v2 checkpoint assessment (harsh, from compare_side.png)
Shipped as a coherent v2. What still falls short vs the hero:
1. Tank is too long/tubular; the reference tank is shorter, more bulbous,
   with a distinct front hump. Mine reads "torpedo", ref reads "teardrop".
2. DUCATI script too small, too upright, too far back; reference script is
   larger, italic, sitting forward on the flank.
3. Reference has a prominent WHITE front fender hugging the tire; mine is
   dark and undersized (missed detail — the 39/ close-up confirms white).
4. Stance still slightly tall/narrow vs the reference's low wide muscle.
5. Exhaust headers still read chunky where they cross the engine; reference
   headers are slimmer and tuck tighter.
6. Engine cases still boxy; reference has more sculpted castings.
These are Round 3 targets, not v2 blockers.

## Known limitations (harsh)
1. Tank green is close but not the hero's near-black deep green; bright studio
   lighting lifts it. A moodier light rig would match better.
2. The DUCATI decal is a flat white script; the reference has a slightly
   metallic/raised badge look. Shrinkwrap on a 4-vertex plane does not hug the
   tank curvature perfectly at glancing angles.
3. Exhaust muffler is a simple tapered cone; the reference has visible weld
   seams, a riveted end cap, and a mounting bracket.
4. No cables, hoses, brake lines, or wiring; the cockpit (clocks, switches) is
   minimal. The reference has rich small details here.
5. Spokes are straight cylinders; the reference has slightly crossed lacing.
6. Overall it reads as a clean stylized game asset, not a photoreal replica.
   Silhouette and identity features (green tank + script, brown seat, knobbies,
   gold disc, high pipe, grilled light, trellis, number plate) all present.

## Files
- `scripts/build_ducati.py` — the full procedural build (renders, saves .blend, exports .glb)
- `ducati-scrambler-custom.blend` — Blender 4.2+ scene (2 MB)
- `ducati-scrambler-custom.glb` — glTF 2.0 export (1 MB, with packed DUCATI decal texture)
- `renders/` — 8 views, 1400x1050 PNG
- `compare/` — reference-vs-render side-by-sides
- `textures/ducati_decal.png` — PIL-drawn DUCATI script (also packed in .blend)
