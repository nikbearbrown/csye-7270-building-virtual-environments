# Character sheet — the Ghost (nameless by design)

> **STATUS 2026-10-02 — LOOK LOCKED: the School Picture Boy.** Chosen over four earlier candidates (Sweater Kid, Pajama Boy, Slicker, Outline — see FRICTIONAL) and committed before the first generation. The 2026-10-01 sweater draft below this note is superseded where it conflicts; the name rule, pose list, collision, palette discipline, and consistency rules carry over.

- **Concept in one sentence:** a boy of about ten dressed for picture day — collared shirt buttoned one button wrong, clip-on tie, combed hair fighting a cowlick — who appears in the living world as the faded school photograph the town kept, and in the remembered world as the real kid no photo captured.
- **The two looks of one boy:**
  - **GHOST state (upright world):** the walking photograph — desaturated sepia-blue tones, soft paper-grain wear, tie straight, hair combed; legs dissolve into mist below the knee, no shadow, drifting slightly off the floor. The photo treatment says who he is to the world; the mist and missing shadow say what he is.
  - **REMEMBERED state (inverted world):** full warm color, tie yanked loose, shirt untucked, grass-stained knees, the cowlick winning; feet planted, real shadow. An ordinary kid, which is the point.
  - Story hook: the wife's endlessly unpacked picture frames hold his school photo — the relic the recognition arc converges on.
- **The name rule:** the boy has no name anywhere in the game's text or UI until the player finds it — the name is a relic, scratched under a floorboard in the memory-house, and the child speaking it aloud is what completes "being seen" (the endgame, not the slice). Hidden answer on record: **Hollis** — one letter from "Hollow," which is the point; swappable until it first appears on screen. All documents refer to him as "the ghost" or "the boy."
- **Silhouette at on-screen size:** design/character/silhouette.png — target ~96 px tall in a 1920×1080 viewport. The read comes from three shapes: the collared-shirt torso with the small tie notch, thin shorts-and-socks legs (ghost state: legs end in a mist taper instead), the slightly tilted head with one cowlick spike. No cape, no sheet, no chains — a kid, not a costume.
- **Orientation:** right-facing drawn, left flipped at runtime. Vertical: the upright world and inverted world use the same images rotated 180° by the engine; the art is drawn gravity-agnostic (hair and tie drift AWAY from current gravity, drawn as separate layered elements so the drift direction is runtime-correct in both worlds).
- **Reference:** design/character/turnaround.png — front, side, three-quarter, back at the same height with height bar. (Counts as one pose.)

## The two-state rule (the slice's generated-art requirement)

Every pose exists in **two renders from one linework**: GHOST state (upright world — faded-photograph treatment: desaturated sepia-blue, paper-grain, ~60% opacity, mist below the knee, no shadow) and REMEMBERED state (inverted world — solid, full warm color, lamplit, grounded with a shadow). State swap is the character's most important visual beat. Production note: generate the REMEMBERED render; the GHOST render may be derived from it by logged edits (desaturate, grain, fade, mist) or by image-to-image from the same reference — whichever holds consistency better, recorded per asset-log row.

## Poses (11 — one static image per game state; the game swaps the image on state change. Animation not required per the 2026-10-02 assignment update; any motion is engine code (tweens, rotation, fade), not generated frames.)

1. **Turnaround reference** — proportions contract (counts as one pose)
2. **Idle drift** — upright world; hovering a few pixels off the floor (engine tween bobs the static image)
3. **Walk** — one representative stride, inverted world; he only walks where he was alive
4. **Flip transition** — tucked roll, sweater flaring; shown during the engine's 180° world turn
5. **Reach / kind contact** — arm extended, fingers almost touching; the game's core verb
6. **Scare pose** — both arms out, mouth open; deliberately childish, a kid playing monster — the scary option should look a little heartbreaking
7. **Noticed / freeze** — head snapped toward the viewer, shoulders up; shown when the child looks at him
8. **Searching / peering** — leaning around a corner in the memory-house
9. **Dispersed / hurt** — form scattering like breath on glass; Hollow contact or scare backfire
10. **Hide / curl** — knees up, head down; recovery state after dispersal
11. **Fully seen / goodbye** — standing straight, waving, small smile; reserved for the game's ending, when the child speaks the found name aloud

## Supporting cast (design rules; full sheets are semester work)

- **The child (half-sibling, ~6):** the only saturated thing in the upright house — a bright yellow raincoat (#E9C846 family) she refuses to take off indoors; round silhouette, mismatched socks, a one-eared stuffed rabbit. She notices the ghost in reflections (mirrors, kettles, dark windows) before she ever sees him directly.
- **The father:** tall, pressed cardigan, reading glasses on a cord, always mid-task (a box, a mug) so his never-facing-the-camera rule reads as natural. One wrong detail: a worn leather pouch on his belt — the salt. Nobody asks.
- **The wife:** warm but faded, like a photo left in the sun; forever unpacking picture frames whose photos we never quite see; hums the music-box lullaby without knowing why.
- **The Hollow (identity unrevealed):** one silhouette, two readings. At distance: too tall, arms too long, hair drifting as if underwater, a face like frosted glass. Every element must reinterpret as motherly once the truth lands — the arms were reaching, the hair is how he last saw her, the glass face is his memory refusing her. No design element may be scary in a way that can't later be read as love.

A mirrored copy counts as nothing, and minor variations of one pose count once. Every pose is a single static image judged against the turnaround.

## Collision overlay

design/character/collision.png — one capsule, 40×80 px at game scale, centered on the torso, identical in both gravity states (rotated with the character). The drifting hair and tie extend up to 12 px beyond the capsule and never collide; in GHOST state the mist taper below the knee is also outside the capsule, so the capsule's base sits where his feet would be, not where the mist ends. Art that moves with the "wind" of the wrong world reads as atmosphere, and letting it pass through walls is fair because nothing the player must dodge ever uses those pixels.

## Palette

| Use | Hex |
|---|---|
| Ghost-state photo paper / shirt | #C8CBC4 (desaturated, at ~60% opacity) |
| Ghost-state sepia shadow + mist edge | #8A8374 |
| Remembered skin | #E8C4A0 |
| Remembered shirt | #DCD6C4 (off-white; reads against both the cold upright rooms and the amber memory rooms) |
| Remembered tie | #8C3B2E (oxblood — the one saturated note on him, and the eye's anchor at 96 px) |
| Remembered shorts / grass stain | #4A3B32 / #6B7A42 |

Checked against environments: the ghost-state desaturated grey must never appear in upright-world wall colors (walls stay brown/blue-grey); the tie's oxblood must never appear in memory-world furniture (furniture stays deep amber/wood), so the tie stays the character's unique accent. The child's yellow raincoat (#E9C846) is reserved for her alone and never appears on him in either state.

## Consistency rules (what every generated pose image is judged against)

- Head = 1/3 of total height; shirt hem at hip, shorts at mid-thigh; same three-shape silhouette in every pose
- Eyes: two dark ovals, no whites, same vertical position relative to head in every pose
- The costume never changes between poses or states: collared shirt (one button wrong), clip-on tie, grey shorts, socks. Only its condition changes — tie straight and hair combed in GHOST state, tie loose, shirt untucked, grass-stained and cowlick up in REMEMBERED state
- Outline: uniform weight; no hard outline on the mist taper in ghost state
- Hair and tie drift away from current gravity in every pose
- One reference image generates all poses; any pose that drifts in proportion from the turnaround is rejected regardless of how good it looks alone
