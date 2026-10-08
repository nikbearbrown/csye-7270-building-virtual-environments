# Character sheet — the Ghost (nameless by design)

> **Revision 2026-10-06.** This sheet now describes the design that was accepted after the generation sessions of 2026-10-02 (asset-log rows CHAR-REF-01 to 07). The earlier "School Picture Boy" specification was rejected once it was rendered; that decision and its reasoning are kept in FRICTIONAL.md and the asset log rather than erased, per the assignment's instruction to add revisions rather than rewrite the record.

- **Concept in one sentence:** a boy of about eight, drowned-looking and grey, in a ruined knitted sweater and dungarees, who appears in the living world as something the house has not finished letting go of, and in the remembered world as an ordinary dirty child who was alive here.
- **The name rule:** the boy has no name anywhere in the game's text or interface until the player finds it. The name is a relic scratched under a floorboard in the memory-house, and the child speaking it aloud is what completes "being seen" — the endgame, not this slice. Hidden answer on record: **Hollis**, one letter from "Hollow", swappable until it first appears on screen. All documents call him "the ghost" or "the boy".

## Design

**Body.** Child proportions: head roughly one third of total height, narrow shoulders held slightly too high, thin arms hanging loose and a little away from the body. He never stands straight; the head tilts, the shoulders are uneven. He reads as being held up rather than standing.

**Face.** Hollow cheeks, grey skin with a faint blue tint at the lips and under the eyes. Eyes too large and too dark for the face, with very small pupils. The mouth is slightly open, as if he has been about to speak for a very long time. In every view, including profile and back views, the head is turned toward the viewer.

**Hair.** Long, badly overgrown, uncut for years. Heavy wet strands hang over the eyes and past the jaw, stuck to the forehead and cheeks, dripping. One eye is usually more visible than the other.

**Clothes — every element is evidence, not decoration.**

| Item | What it tells the player |
|---|---|
| Dark green hand-knitted sweater, far too big, soaked dark from the chest down with a visible wet line | Where did the water come from, if he ran away? |
| Cuffs and hem unravelling badly, long threads hanging | Time has passed; nobody mended it |
| Denim dungaree shorts, one shoulder strap unbuckled and hanging | A child dressed by someone, or undressed by something |
| Trousers caked with dry grey dust at the knees and shins | He has been somewhere underground — the cellar the father keeps checking |
| Bare feet, pale and dirty, dust on the soles | He never put shoes on; he never left |

## The two states (the slice's generated-art requirement)

One character, two static images. The game swaps the image when the world turns over; no animation, per the 2026-10-02 assignment update. Motion in the slice is engine code only — a slow vertical drift, the 180° world rotation, fades.

| | REMEMBERED — normal world | GHOST — inverted world |
|---|---|---|
| Colour | Drained to pale cold grey and washed blue | Full warm colour, lamplit |
| Edge | Soft, translucent, dissolving | Solid, outlined |
| Legs | Dissolve into drifting mist below the knee | Whole, feet visible |
| Hair and threads | Drift upward, against gravity | Hang normally |
| Contact | Hovers, no shadow, feet never touch the floor | Grounded |
| File | `godot/assets/art/char_ghost.png` | `godot/assets/art/char_remembered.png` |

The contrast is the point: he looks alive only in the world that is gone.

## Orientation

Side profile facing **right** is the drawn view, which is the view a side-scrolling player sees. Left is produced by flipping the sprite horizontally at runtime (`flip_h`), never by generating a second image. Vertically, the same images are used in both worlds; the engine rotates the world root 180°, so no upside-down art is generated either.

## Silhouette test

`design/character/silhouette.png` — the front view filled solid black and scaled to its real on-screen height of **96 px** (33 × 96). `design/character/silhouette-test-card.png` shows that size beside a 3× enlargement.

Result: the shape reads at game size. The hair mass is the dominant silhouette element, the body stays narrow beneath it, and the ragged sweater hem and hanging threads break the outline so the figure never becomes a solid blob. Facial detail is lost at this size, which is expected and acceptable — the character is identified by hair mass and posture, not by face.

## Poses (14, one static image per game state)

Generated and in the slice:

1. **Turnaround reference** — front, side, three-quarter, back at one height (counts as one pose); `design/character/model-sheet-8-views.png`
2. **Idle drift, ghost** — inverted world, hovering, legs dissolving into mist; `godot/assets/art/char_ghost.png`
3. **Idle, remembered** — normal world, solid and grounded; `godot/assets/art/char_remembered.png`
4. **Walk: contact** — right leg forward, heel down, arms opposite; `char_walk_1.png`
5. **Walk: passing** — legs together, torso lifted; `char_walk_2.png`
6. **Walk: contact mirrored** — left leg forward, arms swapped; `char_walk_3.png`
7. **Walk: passing, second** — legs together, opposite leg lifting; `char_walk_4.png`
8. **Ghost high angle** — looked down on; from the model sheet
9. **Ghost low angle** — looked up at; from the model sheet
10. **Ghost close-up** — head and shoulders, for the moment of being noticed; from the model sheet
11. **Ghost floating, arms limp** — the drifting full body; from the model sheet

Specified and not yet generated (semester work beyond this slice):

12. **Reach / kind contact** — arm extended, fingers almost touching: the core verb
13. **Scare pose** — arms out, mouth open; deliberately childish, a boy playing monster
14. **Fully seen / goodbye** — standing straight, small wave; reserved for the ending


A mirrored copy counts as nothing, and minor variations of one pose count once. Left-facing movement is the right-facing art flipped at runtime, never a separate generation.

## Collision overlay

`design/character/collision.png` — the capsule drawn over four poses at the same scale, with the floor line marked.

One capsule, **52 x 250 px**, centred 125 px above the feet, identical in every pose and in both states. The sprite is 320 px tall, so the capsule covers the torso and legs and stops short of the hair.

**Revision 2026-10-06:** this was specified as 40 x 80 px before the art existed, which turned out to cover only the shins of a 320 px sprite. The mismatch was found while drawing this overlay and corrected in `Player.tscn` rather than papered over in the document.

Art outside the capsule and why it is fair: the hair mass, the hanging sweater threads, and, in the GHOST state, the mist the legs dissolve into all extend beyond the capsule and never collide. In the ghost state the capsule's base sits where his feet would be if he were standing, not where the mist ends, so footing is consistent between states even though the art is not. Art that drifts against gravity reads as atmosphere, and letting it pass through walls is fair because nothing the player must dodge ever occupies those pixels; the capsule is never wider than the body, so a generous shape can only work in the player's favour.

## Palette

Sampled from the accepted assets rather than specified in advance, so the sheet matches what is actually in the game.

| Use | Hex |
|---|---|
| Sweater, remembered | `#303020` |
| Dungarees / denim | `#303030` |
| Dust and skin, remembered | `#504030` |
| Ghost body, cold grey | `#404050` |
| Ghost mist highlight | `#707080` |
| Upright room walls | `#303030` / `#404040` |
| Memory room, amber and wood | `#302010` / `#402010` |

**Readability rules checked against the environments:** the upright room is cold blue-grey with no green, so the sweater separates him from the wall in the remembered state; the memory room is amber and wood with no green or cold blue, so the ghost's cold grey separates him there. Green belongs to the character alone and appears nowhere in either room; the child's yellow raincoat (`#E9C846`) belongs to her alone and appears on no one else.

## Consistency rules (what every generated image is judged against)

- Head roughly one third of total height; narrow body beneath a heavy hair mass
- Eyes large and dark with small pupils, same vertical position relative to the head in every image
- Mouth slightly open in every image; never smiling, never neutral-closed
- The head is turned toward the viewer in every view, including profile and back
- The costume never changes between poses or states — sweater, dungarees with one strap unbuckled, dusty trousers, bare feet. Only its rendering changes: warm and solid in REMEMBERED, pale and dissolving in GHOST
- Hair and loose threads drift away from current gravity
- One reference image generates all poses; any image that drifts in proportion from the model sheet is rejected regardless of how good it looks alone

## Supporting cast (design rules; full sheets are semester work)

- **The child (half-sibling, about six):** the only saturated thing in the upright house — a bright yellow raincoat she refuses to take off indoors, round silhouette, mismatched socks, a one-eared stuffed rabbit. She notices the ghost in reflections before she ever sees him directly.
- **The father:** tall, pressed cardigan, reading glasses on a cord, always mid-task so his never-facing-the-camera rule reads as natural. One wrong detail: a worn leather pouch on his belt, which is salt. Nobody asks.
- **The wife:** warm but faded, forever unpacking picture frames whose photographs we never quite see; hums the music-box lullaby without knowing why.
- **The Hollow (identity unrevealed):** one silhouette, two readings. At a distance: too tall, arms too long, hair drifting as if underwater, a face like frosted glass. Every element must reinterpret as motherly once the truth lands. No element may be frightening in a way that cannot later be read as love.
