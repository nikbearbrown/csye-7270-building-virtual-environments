# Futurama-toy Enterprise: build notes (Grok Bot)

A generic, toy-style take on the classic starship Enterprise, in the style of the Planet Express ship toy: glossy pale grey-blue vinyl, cream trim, red accents. No registry number, logos or insignia.

## Sources
- **Style target:** a Grok Bot concept image approved by Professor Bear (`compare/concept_grok_bot.jpg`): "You definitely recognize the Enterprise, but it's not the Enterprise."
- **Layout and proportions:** Professor Bear's blueprint images (orthographic sheet and outboard profile), then made rounder, fatter and more compact.

## Measurements
Model units, X forward (nose at +X), Z up, saucer centred at the origin.
- Blueprint ratios (orthographic sheet, top view): saucer diameter 1.0; nacelles about 1.26 saucer diameters long, at ±0.38 saucer diameters off the centreline; secondary hull front about 0.3 saucer diameters behind the saucer centre.
- Concept image, measured in round 5 assuming a camera about 62° off the nose: nacelle front at x ≈ -1.0 and spacing ±0.7; hull front at x ≈ -0.5; nacelle length about 1.3-1.5; hull radius ≈ 0.3; nacelle radius ≈ 0.18. That is much more compact and much fatter than the blueprint, and the round 5 rebuild followed the concept.
- Final (round 9): saucer radius 1.0, top height 0.32, bottom height 0.24 (superellipse exponents 1.9 and 2.1); red bumper torus, minor radius 0.062, plus a lower band of 0.034; bridge dome radius 0.335. Secondary hull lathed, 1.34 long, max radius 0.335, centre z -0.70, front x -0.52. Nacelles radius 0.18, length 1.46, front x -1.0, y ±0.72, z +0.25, red caps radius 0.195. Pylon chord half-width 0.15 and half-thickness 0.075.

## Rounds
| Round | Change |
|---|---|
| r1 | First full parametric layout from the blueprint ratios. Readable, but the colours were pastel and washed out (AgX), the nacelles too thin and long, and the horizon line showed. |
| r2 | Standard view transform with slate colours; shadow-catcher ground composited on a studio-grey gradient; fatter, shorter nacelles; bigger dome. |
| r3 | Stepped cream deflector housing with a dark dish, spokes and a cone; colours and lights toned down to the concept. |
| r4 | Thicker saucer, nacelles shortened again, pylons moved. Hero camera tests. |
| r5 | Sizes and positions re-measured off the concept: the whole ship became much more compact (hull moved forward under the saucer, slimmer hull and nacelles). The biggest single improvement. |
| r6 | Hull lowered so it reads below the saucer, bigger bridge dome. |
| r7 | Double red bumper band, smaller bridge core, rivets on the pylon piping, eye-level 45 mm hero camera. |
| r8 | Flatter, more lens-like saucer top; portholes moved in from the rim; less fill light. |
| r9 | Narrower pylons (the top view showed them as wide plates); nacelles slightly longer. Final. |

## Scores (Grok Bot, judged by overall look and feel against the concept)
- Hero three-quarter: 6/10
- Side: 5/10, top: 5/10, front: 5/10 (layout only; the blueprints are a different, non-toy style)
- Close-ups (bridge, nacelle, deflector): 6/10
- Overall: about 6/10

## Stats
266 mesh objects (GLB, curves converted), 155,640 triangles, 6 materials, 3.57 x 2.11 x 1.74 units. Blender 4.2.3, Cycles CPU, 64 samples, Open Image Denoise. The `.blend` is about 1.2 MB and the `.glb` about 2.8 MB.

## Limitations
- The saucer is thinner and flatter-topped than the concept, so it is less inflated-looking.
- The secondary hull is smaller and less prominent than the concept's big pod, and it is mostly hidden under the saucer in the top view.
- The pylons and neck are simple lofted beams with cream piping, not the concept's framed panels and wedge neck.
- The bumper lights look like small stuck-on tiles.
- Only one view (the hero) can be compared directly, because the concept is a single image.
- There are no panel lines, and small parts sit on the surfaces as separate objects.
- The GLB has flat colours only.
