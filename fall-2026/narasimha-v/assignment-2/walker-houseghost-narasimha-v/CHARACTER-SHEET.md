# Character sheet — the Ghost (nameless by design)

> **STATUS 2026-10-01:** the visual concept described below (the oversized-sweater candidate) is a working draft. Four candidate looks are under discussion — Sweater Kid, Pajama Boy, Slicker, Outline — and the final one will be chosen and committed here **before the first generation**. The name rule, pose list, collision, palette discipline, and consistency rules stand regardless of which look wins.

- **Concept in one sentence:** a boy of about ten in an oversized hand-me-down sweater and socks, translucent and cold in the living world, solid and warm only in the house he remembers — he looks alive exclusively in the world that is gone.
- **The name rule:** the boy has no name anywhere in the game's text or UI until the player finds it — the name is a relic, scratched under a floorboard in the memory-house, and the child speaking it aloud is what completes "being seen" (the endgame, not the slice). Hidden answer on record: **Hollis** — one letter from "Hollow," which is the point; swappable until it first appears on screen. All documents refer to him as "the ghost" or "the boy."
- **Silhouette at on-screen size:** design/character/silhouette.png — target ~96 px tall in a 1920×1080 viewport. The read comes from three shapes: the too-big sweater (wide, slumped rectangle), the thin sock-footed legs, the slightly tilted head. No cape, no sheet, no chains — a kid, not a costume.
- **Orientation:** right-facing drawn, left flipped at runtime. Vertical: the upright world and inverted world use the same frames rotated 180° by the engine; the art is drawn gravity-agnostic (sweater hem and hair drift AWAY from current gravity, drawn as separate layered elements so the drift direction is runtime-correct in both worlds).
- **Reference:** design/character/turnaround.png — front, side, three-quarter, back at the same height with height bar. (Counts as one pose.)

## The two-state rule (the slice's generated-art requirement)

Every pose exists in **two palettes from one linework**: GHOST state (upright world — translucent, cold blue-white #AFC8D8 at ~60% opacity, soft edge) and REMEMBERED state (inverted world — solid, warm skin and mustard sweater, lamplit). State swap is the character's most important visual beat.

## Poses (12, each labeled with its game state)

1. **Turnaround reference** — proportions contract (one pose)
2. **Idle drift** (loop) — upright world; hovering a few pixels off the floor, slow bob
3. **Walk contact** (loop key) — inverted world; real footsteps, he only walks where he was alive
4. **Walk passing** (loop key) — inverted world
5. **Flip transition** (single) — tucked roll, sweater flaring, used for the 180° world turn
6. **Reach / kind contact** (single) — arm extended, fingers almost touching; the game's core verb
7. **Scare pose** (single) — both arms out, mouth open; deliberately childish, a kid playing monster — the scary option should look a little heartbreaking
8. **Noticed / freeze** (single) — head snapped toward the viewer, shoulders up; plays when the child looks at him
9. **Searching / peering** (loop) — leaning around a corner in the memory-house
10. **Dispersed / hurt** (single) — form scattering like breath on glass; Hollow contact or scare backfire
11. **Hide / curl** (single) — knees up, head down; recovery state after dispersal
12. **Fully seen / goodbye** (single) — standing straight, waving, small smile; reserved for the game's ending, when the child speaks the found name aloud

## Supporting cast (design rules; full sheets are semester work)

- **The child (half-sibling, ~6):** the only saturated thing in the upright house — a bright yellow raincoat (#E9C846 family) she refuses to take off indoors; round silhouette, mismatched socks, a one-eared stuffed rabbit. She notices the ghost in reflections (mirrors, kettles, dark windows) before she ever sees him directly.
- **The father:** tall, pressed cardigan, reading glasses on a cord, always mid-task (a box, a mug) so his never-facing-the-camera rule reads as natural. One wrong detail: a worn leather pouch on his belt — the salt. Nobody asks.
- **The wife:** warm but faded, like a photo left in the sun; forever unpacking picture frames whose photos we never quite see; hums the music-box lullaby without knowing why.
- **The Hollow (identity unrevealed):** one silhouette, two readings. At distance: too tall, arms too long, hair drifting as if underwater, a face like frosted glass. Every element must reinterpret as motherly once the truth lands — the arms were reaching, the hair is how he last saw her, the glass face is his memory refusing her. No design element may be scary in a way that can't later be read as love.

Loop/once noted per pose above. A mirrored copy counts as nothing; walk contact and walk passing are the two genuine keys of one cycle.

## Collision overlay

design/character/collision.png — one capsule, 40×80 px at game scale, centered on the torso, identical in both gravity states (rotated with the character). The sweater hem and drifting hair extend up to 12 px beyond the capsule and never collide: art that moves with the "wind" of the wrong world is readable as atmosphere, and letting it pass through walls is fair because nothing the player must dodge ever uses those pixels.

## Palette

| Use | Hex |
|---|---|
| Ghost-state body/glow | #AFC8D8 (at ~60% opacity) |
| Ghost-state outline | #5F7684 |
| Remembered skin | #E8C4A0 |
| Remembered sweater | #C98F2D (mustard — reads against both the blue upright rooms and the amber memory rooms because it sits between them) |
| Remembered shorts/socks | #4A3B32 |
| Accent (eyes, music box key) | #F2E6C9 |

Checked against environments: the ghost-state blue must never appear in upright-world wall colors (walls stay brown/gray); the sweater mustard must never appear in memory-world furniture (furniture stays deep amber/wood). These two exclusions are environment-palette rules, not just character rules.

## Consistency rules (what every generated frame is judged against)

- Head = 1/3 of total height; sweater hem at mid-thigh; same three-shape silhouette in every pose
- Eyes: two dark ovals, no whites, same vertical position relative to head in every frame
- Outline: uniform weight, no outline on the glow edge in ghost state
- The sweater's drift direction must oppose current gravity in every frame
- One reference image generates all poses; any frame that drifts in proportion from the turnaround is rejected regardless of how good it looks alone
