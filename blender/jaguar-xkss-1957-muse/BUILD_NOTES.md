# BUILD_NOTES — jaguar-xkss-1957-muse

1957 Jaguar XKSS roadster, Sherwood Green. Fully scripted with the Blender Python API (bpy); no sculpting, no textures (flat colours only).

## Audit (measured from the finished .blend, not estimated)

- Mesh objects (car only): 51 (52 incl. ground plane)
- Triangles (evaluated, subdivision applied): 21,242
- Materials used: 15 — Black, Chrome, Dark, Glass, Grille, Ground, Lens, Paint, RedLens, Rim, Rubber, Steel, SteelDark, Tan, Wood
- Model dimensions, metres X×Y×Z (length × width × height): 4.64 × 1.85 × 1.33 — **stylized, not built to real scale**
- Blender version: 4.5.9 LTS
- File sizes: .blend 1.7 MB (limit 100 MB), .glb 0.9 MB

## Real-car reference figures (for comparison only)

The references are Jaguar Classic 2016 continuation press shots of the XKSS in Sherwood Green.
Published real-car figures: wheelbase 2,300 mm, length 3,990 mm, width 1,660 mm,
height 1,120 mm; 16×5.5 in Dunlop solid alloy disc wheels with center-lock hubs
(not wire spokes), 6.50×16 tires. The model does not attempt these dimensions.

## Method

1. Body: a single lofted quad mesh. Twelve stations along the length, each an
   ellipse ring (20 points) with separate top/bottom radii to shape the
   long bonnet, cowl, cockpit region and tapered tail; end caps fanned.
   Subdivision Surface (level 2) + smooth shading.
2. Wheels: cylinders — rubber tire, silver disc rim, chrome center-lock hub.
   Four wheels, no tread, no perforations.
3. Cockpit: thin dark lid floating just above the hull as the opening; tan
   box-built seats, dark dashboard, wood-rim steering torus + column,
   black folded soft-top boot, green headrest fairing.
4. Windshield: wraparound arc panel (12-segment grid), tinted transparent,
   with black A-posts.
5. Details: faired headlamps (chrome ring + lens), oval dark grille, split
   chrome front bumperettes, full-width rear bumper, red tail lamps with
   chrome rings, chrome luggage rack (tube grid) on the rear deck, chrome
   fuel cap, side exhaust pipe + dark heat shield, chrome door handle,
   black leather door strap, stalk mirror.
6. Studio: large ground plane, light-grey world, 1 sun + 3 area lights.
7. Cameras: side, rear 3/4, front 3/4 (comparison set), plus 2 detail
   cameras (front, cockpit). Rendered headless with EEVEE-Next, 1280×720.

## Comparison rounds (5)

- v1: initial loft; body read well but cockpit was a black slab, windshield a dark shard, seats too tall, heat shield oversized.
- v2: cockpit opening thinned to a lid, seats/dash lowered, windshield seal removed, heat shield shrunk and darkened, rims darkened.
- v3: deeper green base colour attempted.
- v4: colour-space correction — bpy colour values are linear, so the green was re-specified in linear terms (the wash-out was a linear-vs-sRGB mistake, not the lighting).
- v5: metallic lowered 0.6 → 0.22 (the white studio was reflecting into mint); final renders.

## Known limitations (honest)

- Stylized subdivision-smoothed body, not true XKSS surfacing; panel gaps, shut lines and the bonnet louvers are absent.
- Interior is box-built; instruments, switches and pedal box omitted.
- Wheels are plain discs: no perforations, no tread, simplified center-lock spinners.
- Brightwork simplified: bumpers, rack and exhaust are plain chrome/steel shapes; no Jaguar script badge, no wipers.
- Glass is a single tinted panel; trim is minimal.
- Colours approximate; judged harshly, the side view is closest, the front is weakest (lamps read flat rather than deeply nacelled).
- GLB carries flat colours only.
