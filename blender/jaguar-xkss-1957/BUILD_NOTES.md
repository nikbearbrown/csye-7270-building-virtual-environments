# Jaguar XKSS (1957 / Jaguar Classic continuation) - Blender build

Built by Grok Bot in Blender 4.2.3 (headless, Cycles CPU) from 7 reference photos (refs/).

## Files
- `xkss.blend` - final model + studio + 4 fixed comparison cameras (= `xkss_r8.blend`)
- `xkss_r1.blend` ... `xkss_r8.blend` - milestone saves, one per round (same cameras in every round)
- `xkss.glb` - car only (modifiers applied at viewport subdivision; flat PBR colours, no procedural panel lines)
- `gallery/` - 1600 px renders: side, front, rear34 (matching the reference angles) and hero 3/4 front
- `compare/rN_{side,front,rear34}_compare.jpg` - reference left, render right, every round
- `analysis/r*_overlay.jpg` - 50% blends of render over reference used to fit the profile
- `build_xkss.py` - the whole build (`blender -b -P build_xkss.py -- --round N --res 640 --samples 10`)
- `compare.py`, `PROGRESS.md` (what changed each round and why)

## Dimensions used (sources: Jaguar media, Wikipedia, Ultimatecarpage)
| | spec | model |
|---|---|---|
| Length | 3990 mm | 3780 mm body (X -2.035 .. +1.745) + ~90 mm bumperettes |
| Width | 1660 mm | 1664 mm (front wings 0.832 half-width) |
| Height | 1120 mm | 1065 mm to screen top |
| Wheelbase | 2300 mm | 2300 mm |
| Track F / R | 1270 / 1219 mm | 1270 / 1220 mm |
| Tyre | 6.50-16 | r 318 mm (measured off the side photo), 16 in rim |
Length is ~5% short of the published figure: the side profile was traced from the photo and the overhangs only partly corrected for perspective; I kept the photo's proportions over the spec number.

## Method
- Body = ONE lofted quad mesh (~148 stations x 118 points) generated from smooth (PCHIP) profile tables traced off the side photo on a 50 px grid (wheelbase-calibrated, 1.846 mm/px) plus front-view widths/crowns. Cockpit tub, wheel arches, grille mouth and headlamp holes are cut from the same mesh with boundaries snapped to ellipses/circles; Subdivision (2 at render) + 3 mm Solidify. Panel gaps are shallow shader creases (bump + darken).
- Side and front cameras were solved from reference pixels (hub centres, headlamp spacing) so overlays register; rear 3/4 estimated from the near/far wheel-size ratio.
- Parts are ray-cast onto the body: deep headlamp nacelles w/ chrome bezels + lenses, sidelamps, oval grille with mesh, split bumperettes, rear bumper blades, red tail lamps, XKSS plate, 24 bonnet louvres, 112 rivets, bonnet latch + leather strap, perforated heat shield + twin side exhausts, wraparound framed screen + side screens, tan seats/tunnel/dash with gauges, wood-rim RHD wheel, folded black hood with tan piping, chrome luggage rack, fuel cap, disc wheels with perforation ring and 3-ear spinners.

## Counts (final)
- 293 mesh objects in the car (incl. 112 instanced rivets)
- ~361k triangles at viewport subdivision (what the GLB carries); ~1.2M at render subdivision (estimate: body level 2)

## Honest limitations
- Front: the bonnet reads too bright/white at the reference's grazing camera angle and the wing crowns above the headlamps are softer than the photo's distinct humps; the "frog-eye" chrome lamp rings look more prominent than the real recessed nacelles.
- Surface flow is a parametric loft, not hand-sculpted: no subtle S-curve under the doors, no sharp feature crease at the rear wing seam, haunches slightly less voluminous than the photos.
- Wheels: perforations are dark inset discs, not real holes; no tread pattern; spinner simplified.
- Interior, hood bundle and rack are simplified; no Jaguar script badge on the bonnet; no wipers.
- Exhaust heat shield sits a little proud/low compared to the photo.
- Studio is generic (white block walls, striped floor); paint is a touch lighter/flatter than the photos.
- GLB has flat materials only.
