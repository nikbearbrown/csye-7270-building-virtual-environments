# Character sheet — <mage name>

> Draft v1 — written before any generation. Pose images in this version are my own hand sketches;
> generated poses are added later as a revision, and judged against this sheet.
> Items marked *PROPOSED* came from Claude and still need my confirmation.

- **Concept in one sentence:** a cute young fire mage with white twin tails and red eyes, carrying the only warm light into a dark cave.
- **Viewport:** 640×360 base resolution, integer-scaled (3× for 1080p, 6× for 4K). Pixel art, nearest-neighbor filter.
- **On-screen size:** about 64 px tall including the hat (about 18% of screen height); body without the hat about 52 px.
- **Proportions:** slender, girlish figure, not chibi. Head-to-body ratio about 1:3.5 (head about 15 px), long legs relative to torso.
- **Silhouette at on-screen size:** `design/character/silhouette.png` — idle pose filled solid black at 64 px, placed on the actual cave background.
- **Reference:** `design/character/turnaround.png` — front, side, three-quarter and back at the same height, with a height bar.

## Appearance
- White twin tails reaching the waist, tied with small red bows and hanging clear of her back; large red eyes with a highlight pixel; light blush and a small mouth. Cute but not chibi.
- View: body in side view, face turned slightly toward the camera (three-quarter face), so both eyes read in every facing.
- *PROPOSED* Details: high collar on the capelet, wide sleeves with gold cuffs, gold hem trim, red ribbon tail trailing from the hat, staff crystal wrapped by a curled branch.
- (v1 idea of an eyepatch dropped before generation: it made the face less cute and hid one red eye.)
- Staff held in the right hand: dark wood shaft, red crystal at the tip. The crystal is where fireballs spawn and where the heal glow centers.
- *PROPOSED* Hat: tall witch hat whose tip bends backward, wide slightly drooping brim, red ribbon band with a small ember charm.
- *PROPOSED* Outfit: short capelet over a knee-length belted tunic, belt with small pouches, short boots.

## Orientation
- Drawn facing **right** only. Facing left is `flip_h` at runtime.
- The design is left-right symmetric enough that flipping has no visible side effect. The staff-tip marker is mirrored in code so fireballs still leave the crystal.
- Facing follows movement; the mage turns toward the cursor at the moment she casts.

## Poses (10)
| # | Pose | Game state | Playback |
|---|---|---|---|
| 1 | Turnaround (front, side, three-quarter, back, height bar) | reference | — |
| 2 | Idle | standing; also held during the heal channel | loop |
| 3 | Run — contact | moving | loop |
| 4 | Run — passing | moving | loop |
| 5 | Rising | jump, going up | once |
| 6 | Falling | jump, coming down | once |
| 7 | Cast | fireball released from the crystal | once |
| 8 | Hurt | took damage (held ~0.3 s with knockback, then blinks during 1 s invulnerability) | once |
| 9 | Fail | fell into a pit or ran out of HP | once |
| 10 | Victory | boss defeated, exit reached | loop |

Images: `design/character/poses/01-turnaround.png` … `10-victory.png`.

## Collision overlay
`design/character/collision.png` — every pose at 64 px with the collision rectangle drawn over it.
- Shape: rectangle about 14×44 px, from the feet to the chin, centered on the body.
- Outside the shape: hat, twin tails and staff. Only the body can be hurt. This is fair to the player because hair and hat are the parts that swing furthest in the run and jump poses; a hit on a hair tip would feel unearned.
- The rectangle does not change between poses, so the hurtbox never jumps when the animation changes.

## Palette (*PROPOSED*, to be checked against the cave background)
| Use | Hex |
|---|---|
| Hair | #E8E6F0 |
| Eyes, ribbon, staff crystal | #D62839 |
| Hat, capelet | #3A40A0 |
| Trim, ember charm | #D4A63A |
| Tunic, boots | #6B5A4E |
| Skin | #F5DCCD |

Outline #1A1420 and one shade/highlight step per color (e.g. blush #F2A0A8) are derived from these six and are not separate key colors.

Check: the hat/capelet indigo must stay at least one value step brighter than the darkest cave tone, and the hair must be the brightest shape on screen. Fireball and heal glow are warm; enemy art stays cool.

## Consistency rules (every frame is judged against these)
- Same height (64 px with hat), head-to-body ratio 1:3.5 as in the turnaround; reject any frame that drifts toward chibi proportions.
- Eye line at the same height in every standing pose; both eyes visible, same size and highlight position.
- Twin tails always reach the waist; they may swing but not change length.
- Staff length and crystal size fixed; always in the right hand.
- 1 px outline in #1A1420; no extra outline colors.
- Only palette colors above; no new hues introduced by the model.
- Hat shape and bend direction identical in every pose.

## Open
- Name, hat and outfit confirmation.

## Revision 1 — 2026-10-01 (after reference generation)
- Tunic length: accepted at mid-thigh instead of knee-length. The generated reference (CHAR-REF v2) drew it shorter; at 64 px the shorter tunic shows more leg and makes the run and jump poses easier to read, so I kept it.
- Staff thickness: shaft made thicker in v2 after the 64 px check showed the v1 staff breaking into loose pixels.

## Revision 2 — 2026-10-06 (sheet images produced after generation)
- `design/character/silhouette.png` and `design/character/collision.png` were produced after generation, from the cleaned sprites in `assets/sprites/mage/` (script: `tools/sheet_images.py`), not before generation as the Draft v1 header implies.
- Silhouette: idle filled solid black at 64 px on the actual cave background (1x, 640x360), standing on the ground tiles at three screen positions. Cave L* behind the silhouette (median): 5.5 at x=128, 8.2 at x=320, 17.3 at x=512. The shape reads in all three; it is weakest at x=128, against the darkest part of the cave.
- Collision: every pose at 64 px with the 14x44 rectangle at canvas x 24–38, y 23–67 (feet to chin, centred on the body column x=31), identical in every pose. Idle's chin is 0.2 px from the rectangle top; cast, hurt and win 0.4 px above it; rise (crouched) and fail (kneeling) about 7 px below it, so in those two poses the rectangle top overlaps the head.
- Pose count: run_contact (legs at their widest stride, front heel down) and run_passing (legs together under the body, one foot planted) are two distinct key poses with different silhouettes, not minor variations of one pose, so the sheet keeps 10 poses. The slice shows run_contact for the run state; run_passing is kept on the sheet as the second key pose of the stride.

## Revision 3 — 2026-10-06 (palette revision 1, after the 64 px cave-background check)
- Reason: predicted failure 3 (CHANGE-BRIEF) was observed on the cave-tone row of the contact sheet. The cave's darkest tones measure L* 4.7 (5th percentile) and 8.7 (median); the outline #1A1420 is L* 7.4, so the stockings, boots and hat brim, which had mapped to the outline colour, disappeared.
- Skin ramp: base #F5DCCD with shade #E0B8A6 (replaces the derived shade; the light step is dropped because it read as white on the face). Skin-toned pixels may only use skin, never gold or hair.
- Indigo shade lifted from #201973 (L* 16.7) to #261E8A (L* 20.7); the hat brim now uses it, about one value step above the darkest cave tone.
- Stockings and boots one step lighter: stockings from the outline colour to the tunic shade #4D3931 (L* 25.9); boots from the tunic shade to the tunic base #6B5A4E (L* 39.6), the boot colour in the palette table above.
- Staff head: solid #D62839 crystal with one highlight pixel inside a solid wood branch, no dithering. Eyes: a 2x2 #D62839 eye in the open-eye poses (idle, run_contact, run_passing, rise, fall, cast); hurt, fail and win keep closed eyes.
- Frame sizes, canvas and anchors unchanged. Before/after: `design/checks/mage-palette-revision1-before-after.png`; per-pixel details in `assets/sprites/EDIT-LOG.md`.
- Known limitation, collision: the fixed 14x44 rectangle covers part of the head in RISE (crouched) and FAIL (kneeling), where the chin sits about 7 px below the rectangle top (see `design/character/collision.png`). Accepted, because RISE lasts only a moment and FAIL appears only after the run has ended.
