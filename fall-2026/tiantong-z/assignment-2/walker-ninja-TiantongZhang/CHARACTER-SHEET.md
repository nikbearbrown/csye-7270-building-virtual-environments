# CHARACTER-SHEET.md — the generation spec for the player character

**Written 2026-10-03, before any image has been generated.** Every number in
this file was measured out of the shipped build (`godot/features/player/player.gd`,
`godot/features/player/tuning.gd`, `godot/game/session.gd`) rather than chosen
to look reasonable, and the measurements are reproducible: each section names
the file and the lines it came from.

**Ordering, stated honestly.** This sheet is written *after* the music was
generated (2026-10-01, `ASSET-LOG.md`) and *before* any art or sound effect was.
The music therefore ran ahead of its spec and the art does not. That is recorded
in `FRICTIONAL.md` rather than hidden by backdating a file.

---

## 1. The subject

An original cyber-ninja built for Assignment 1 and carried forward: deep navy
plate, a light-blue visor slit that reads the facing direction, a purple scarf
that trails behind travel, and a steel blade slung across the back. Near-future
industrial — brushed metal and matte fabric under flat overhead light with no
visible source. Not cyberpunk-neon, no glow, no bloom.

Nothing about this character is traced from or prompted against an existing
commercial character, an artist's name or a brand. `CONCEPT.md` section "What
this replaces, and what it credits" carries that history, including the
reference that was dropped on rights grounds before anything was drawn.

---

## 2. The constraint that outranks everything

The character occupies an **18 x 28 px collider on a 640 x 360 logical
viewport** (`player.gd:46-50` — `RectangleShape2D.size = Vector2(18, 28)`,
`CollisionShape2D.position = Vector2(0, -14)`). The node's `position` is the
point **between the feet**; the box spans x in [-9, +9] and y in [-28, 0].

That is pillar 4 of `CONCEPT.md` — "readable at 18 by 28 pixels" — and it is the
reason this sheet leads with contrast and silhouette instead of with detail.
**A pose is judged at game size and as a solid-black silhouette before anyone
looks at its detail.** A frame that only works zoomed in has failed.

### Cell size and anchor

| | value | derived from |
|---|---|---|
| Cell | **32 x 32 px** | drawn extents below, rounded up to a power of two |
| Anchor (the node's `position`) | **(20, 30)** from the cell's top-left | leaves 3 px under the feet and 20 px of scarf room behind |

Measured drawn extents of the **body and scarf together** (`player.gd:300-336`):
x in [-19, +9], y in [-28, -9]; the scarf reaches x = -19 airborne (`trail = 15`
plus a 4 px tip) and flutters +/-3 px. Those fit the cell with margin.

### What is *not* generated: the sword

**The blade stays code-drawn, in both its sheathed and its swung form, and the
generated sprite is body-plus-scarf only.**

This is not a shortcut, it is a correctness requirement. The swung blade is
drawn from `ATTACK_PIVOT (5, -18)`, `attack_angle()` and
`tuning.attack_reach = 30` — *the same three numbers the kill hitbox is built
from* (`player.gd:8-10`, `player.gd:122-123`, and the comment at `player.gd:4-7`:
the blade the player sees and the blade that kills cannot drift apart). Baking
the blade into a static image severs that link: the picture would stop tracking
the hitbox the moment anyone touched the tuning, and the failure would be
silent.

Measured, the swept blade covers x in [-12, +37], y in [-50, +3]. Generating
that as pixels would also force the cell from 32 x 32 to 56 x 56 for three
frames.

**Consequence for generation:** every attack pose below is prompted and judged
**without a sword**, as an arm and shoulder committing to a swing. The steel
colours stay in the palette anyway, because the code draws them over the sprite
and they must not clash.

---

## 3. Palette

Nine colours are in the shipped build. **Eight are kept.** `steel_dark #2a3246`
is dropped: at this scale it is the one-pixel grip, and `shade` carries it.

| role | hex | where it is in the build |
|---|---|---|
| plate | `#1f3a6e` | torso, helm, chest wedge, forward shoulder |
| shade | `#16233d` | legs, rear shoulder, crest — and the 1 px outline |
| visor | `#7fe3ff` | the slit, 6 x 2 px, set forward of centre |
| glint | `#d8f7ff` | 2 x 2 px at the slit's leading edge |
| scarf | `#8a5cf0` | the trail and the belt sash |
| scarf_tip | `#6a3fbf` | the trail's far end |
| steel | `#4a5468` | blade (code-drawn) |
| steel_edge | `#9aa7bd` | blade highlight (code-drawn) |

### The contrast problem, measured

WCAG relative-luminance contrast against the two backgrounds the character
actually stands on — sky `#f6f3ec` and platform `#25354a`
(`session.gd:552` platform ink, `session.gd:558` sky):

| colour | vs sky | vs platform | **worst case** |
|---|---|---|---|
| plate `#1f3a6e` | 10.03 | **1.12** | 1.12 |
| shade `#16233d` | 14.12 | **1.26** | 1.26 |
| visor `#7fe3ff` | **1.32** | 8.50 | 1.32 |
| glint `#d8f7ff` | **1.02** | 11.07 | 1.02 |
| **scarf `#8a5cf0`** | 3.89 | 2.89 | **2.89** |
| scarf_tip `#6a3fbf` | 6.16 | 1.82 | 1.82 |
| steel `#4a5468` | 6.87 | 1.64 | 1.64 |
| steel_edge `#9aa7bd` | 2.19 | 5.12 | 2.19 |

**The body is effectively invisible against the platforms it stands on.** Plate
against platform is 1.12:1 — that is not "low contrast", that is the same
brightness. The visor is the mirror image: it carries the character against
slate at 8.50:1 and vanishes into the sky at 1.32:1.

> **CORRECTION, 2026-10-04 — the sentence above overstates its case, and it is
> left standing so the overstatement is visible.** The colour arithmetic is
> right; the claim about the *game* is not. Platforms in this level sit at
> y 320 with height 64, and the character's body spans 28 px above its feet, so
> standing on the floor it occupies y 292–320 while the platform occupies
> 320–384. **The body essentially never overlaps a platform**, and the 1.12:1
> case I called the crisis barely occurs. What is behind the character almost
> always is the backdrop — 10.03:1 against the cream sky.
>
> I found this only when the dungeon decision forced me to ask what is actually
> behind the character, which is the question I should have asked before
> putting a contrast table in a specification. A measured number in a table is
> not the same as a measured claim about the game.
>
> **It matters now because it has become true.** `CONCEPT.md` revision 1.3
> replaces the cream sky with a dungeon wall, so the backdrop drops from 10.03
> to 1.60 — worse than the figure above, and happening constantly rather than
> almost never. Section 3b carries the numbers that now govern.

Three things follow, and they are binding on every prompt below:

1. **The scarf is the silhouette.** It is the only colour above 2.5:1 against
   *both* backgrounds, so it is the one element guaranteed to read wherever the
   player is. It must be present, unoccluded and clearly separated from the body
   in every single pose, including the ones where the character is not moving.
2. **The 1 px outline is `shade`, and it is non-negotiable.** Against the cream
   sky it is the strongest colour on the sheet (14.12:1); against slate it does
   nothing, which is exactly where the scarf and visor take over. No pose ships
   without the outline. — **Superseded 2026-10-04: the outline is now
   `steel_edge`. See section 3b.**
3. **Neither the visor nor the scarf alone is sufficient**, so a pose may not
   trade one for the other for the sake of a nicer composition.

These are the numbers a generated frame is checked against. They are not a
preference.

---

## 3b. The dungeon palette — governing from 2026-10-04

`CONCEPT.md` revision 1.3 replaced the cream sky with a stone wall. Section 3's
table above is kept because it is the record of what the build looked like when
the sheet was written; **this table is the one a generated pose is checked
against.**

Backdrop `#1b1620`, platform stone `#25354a` (unchanged), lit platform edge
`#c89a5a`.

| colour | vs wall `#1b1620` | vs stone `#25354a` |
|---|---|---|
| plate `#1f3a6e` | **1.60** | 1.12 |
| shade `#16233d` | **1.14** | 1.26 |
| visor `#7fe3ff` | 12.12 | 8.50 |
| glint `#d8f7ff` | 15.79 | 11.07 |
| scarf `#8a5cf0` | 4.12 | 2.89 |
| scarf_tip `#6a3fbf` | 2.60 | 1.82 |
| steel `#4a5468` | 2.33 | 1.64 |
| **steel_edge `#9aa7bd`** | **7.31** | 5.12 |

**The rim is `steel_edge`, not `shade`.** Against the wall, `shade` is 1.14:1 —
the dark shading that used to separate the character from a bright sky now
separates it from nothing. `steel_edge` is 7.31:1 against the wall **and 4.57:1
against the plate it outlines**, so it works from both sides, and it costs no
new colour because it is already one of the eight.

**The scarf is still the silhouette's last line of defence** — 4.12:1 against the
wall, better than it ever managed against the old backgrounds. Rule 1 of
section 3 is unchanged and now easier to satisfy.

**`shade` keeps its other job.** It is still the interior shading — legs, rear
shoulder, crest — where it reads against `plate` rather than against the
background. Only the *outline* changed colour.

**Checked in the build, not only on paper.** The rim was implemented in
`player.gd` and the backdrop in `session.gd`, and the result was rendered and
inspected at 8× in `evidence/screens/`. The first torch glow used four nested
discs and showed visible ring banding in the render that the code did not
suggest; it is sixteen now. That is the kind of thing only a screenshot finds.

## 3c. Value separation — governing from 2026-10-05

`CONCEPT.md` revision 1.4 rebuilt the code-drawn character so the head, torso,
arms and legs are separable. The generated sprite inherits that structure, and
the rule it inherits is **not** "draw gaps between the limbs".

**At 18 × 28 a gap does not survive.** A 1 px rim closes any gap narrow enough
to fit on this body. Separation is by **value**, three steps, every part in
exactly one:

| | role | parts |
|---|---|---|
| `shade` `#16233d` | the **far** side of the body | far arm, far leg, recessed abdomen, jawline, neck |
| `plate` `#1f3a6e` | the **near** side | chest, near arm, near leg |
| `steel` `#4a5468` | the **extremities** | gauntlets and boots only |

`steel` now does double duty — blade *and* extremities — so the whole structure
costs **no new colour**. The palette is still the eight of section 3.

**Limb widths: 4 px legs, 3 px arms.** Narrower than that and there is nothing
left inside for the value step to happen in.

**The 2 px neck is mandatory.** It is the single reason the head reads as a
head rather than as the top of the torso, and it is the cheapest part on the
figure.

### The rim is directional, not an outline

**1 px toward the character's back and 1 px up. Nothing on the front or the
underside.** Section 3b's `steel_edge` `#9aa7bd` is unchanged as the colour;
what changed is where it goes.

An all-sides rim costs a part 2 px of width, so a 3 px arm would keep 1 px of
armour. Rendered, that figure was grey pipework with a hint of navy down the
middle. A directional rim costs **0 px** of width and still breaks the
silhouette against the wall, because the light in a dungeon comes from a torch
above and behind rather than from everywhere.

**Consequence for generation:** a prompt that asks for "1 pixel dark outline"
is now wrong on two counts — the colour is light, and it is on two sides. The
skeleton in section 4 is superseded by the one below.

### Superseding the section 4 prompt skeleton

> pixel art sprite, side view, small humanoid ninja in deep navy segmented
> plate armour, horizontal light-blue visor slit across the helm, short neck
> separating helm from chest, long purple scarf trailing behind, far arm and
> far leg in a darker navy than the near arm and near leg, pale steel
> gauntlets and boots, pale rim light along the back and the top of the
> figure, limited palette of eight colours, flat dungeon torchlight from above
> and behind, no gradients, no glow, no text, plain background

Still no artist name, no character name, no franchise, no "in the style of",
and the palette is still given as hex values rather than as adjectives.

## 4. The reference image comes first

`CONCEPT.md` revision 1.2 commits to this: **one reference image, then every
pose derived from it.** Consistency across poses comes from the reference, not
from repeating the prompt text — which direction A's four rewordings in
`ASSET-LOG.md` already demonstrated in audio, where changing the sentence
changed nothing that mattered.

**REF-01** is a standing side reference at a workable size (not at 32 x 32),
from which the poses are derived and then reduced.

Prompt skeleton, to be logged verbatim in `ASSET-LOG.md` when it is run:

> pixel art sprite, side view, small humanoid ninja in deep navy segmented
> plate armour, horizontal light-blue visor slit across the helm, long purple
> scarf trailing behind, limited palette of eight colours, 1 pixel dark
> outline, flat overhead lighting, no gradients, no glow, no text, plain
> background

No artist name, no character name, no franchise, no "in the style of". The
palette is given as hex values, not as adjectives.

---

## 5. Poses

Every pose below corresponds to a state **the running code can already
distinguish**, so each one can be swapped in by reading a variable rather than
by inventing a new state machine. The condition column is the literal test.

### Required (8)

| # | Pose | Condition in code | What the frame has to say |
|---|---|---|---|
| P1 | Idle | `is_on_floor()` and `absf(velocity.x) <= 8.0` | standing, scarf settled, visor forward |
| P2 | Run | `is_on_floor()` and `absf(velocity.x) > 8.0` | one contact pose; scarf streams back, body leans forward, **arms counter the legs** |
| P3 | Rising | `not is_on_floor()` and `velocity.y < 0` | **bent far knee** — shin and boot lifted together at full height, not a shortened shin — scarf below and behind |
| P4 | Falling | `not is_on_floor()` and `velocity.y >= 0` | legs reaching, scarf above and behind |
| P5 | Dash | `dash_ticks_left > 0` | horizontal, scarf fully extended, no vertical lean |
| P6 | Attack windup | `attack_phase() == 1` | **4 ticks (67 ms)** — arm up and back, body coiled, *no sword* |
| P7 | Attack live | `attack_phase() == 2` | **9 ticks (150 ms)** — arm committed through the sweep, *no sword* |
| P8 | Death | `session.state == State.DYING` | **0.55 s** — the pose the player sees while the retry ticks |

### Optional, in this order if time allows (3)

| # | Pose | Condition in code | Why it is lower priority |
|---|---|---|---|
| P9 | Air jump | `not is_on_floor()` and `air_jumps_left == 0` and `velocity.y < 0` | distinguishable from P3, but P3 covers it legibly |
| P10 | Attack recovery | `attack_phase() == 3` | **3 ticks (50 ms)** — barely visible; P7 can hold |
| P11 | Celebrate | `session.state == State.COMPLETE` | the results screen already communicates this |

Tick budgets are from `tuning.gd`: `attack_ticks = 16`, `attack_windup_ticks = 4`,
`attack_active_ticks = 9`, therefore recovery = 3, at 60 Hz fixed physics.
`dash_ticks = 10` (167 ms). The 0.55 s retry is `session.gd:479`.

### Facing: only one direction is generated

`player.gd:239-251` mirrors every drawn primitive about the body centre
(`_mrect` flips `x` to `-(x + w)`; `_mpoly` reverses the winding and negates
`x`). The sprite is therefore generated **facing right only**, and the left
facing is a horizontal flip of the same texture at runtime. Generating both
would risk two characters that do not match, for no gain.

This also means the visor's forward offset and the glint must stay
**asymmetric** — they are what makes facing readable from the head alone at
this size, and a symmetric helm would destroy the flip's usefulness.

### Two of these poses do not exist yet in the build

`session.gd:477-492` sets `player.enabled = false` on both death and goal, and
the sprite simply **freezes on whatever frame it was on**. There is no death
pose and no celebrate pose today — the reaction is the overlay and the sound, at
the session level, not the character.

So P8 and P11 are **new wiring**, not a texture swap for something that already
has a slot. That belongs in `CHANGE-BRIEF.md` as scope, and it is the reason P8
is in the required set while P11 is not: a frozen mid-air frame at the moment of
death is the single worst-reading state the game currently has, and P11's slot
is already covered by the results screen.

---

## 6. How a generated pose is accepted or rejected

In this order. A pose that fails an earlier check is rejected without the later
ones being run — the rejection and its reason go in `ASSET-LOG.md`.

1. **Silhouette.** Fill every non-transparent pixel solid black, place it on
   the dungeon wall and on the lit platform edge at 1x game size. **A
   silhouette test cannot see the value separation of section 3c** — that is
   the point of running it first and separately: the shape has to work before
   the three-step scheme is allowed to carry anything. If the pose is not identifiable against P1,
   it fails. (Pillar 4.)
2. **Scale.** Viewed at 1x on a 640 x 360 viewport, not zoomed. Detail that
   disappears here is detail that should not have been drawn.
3. **Contrast.** The scarf is unoccluded and reads on slate; the **directional
   rim of section 3c** is present along the back and the top; the visor is
   asymmetric and forward.
4. **Palette.** Exactly the eight colours of section 3 / 3b, no anti-aliased
   intermediates. A generator that returns 40 colours is re-quantised, and the
   re-quantisation is recorded as an edit in `ASSET-LOG.md`, not left implied.
5. **Anchor.** Feet land on (20, 30) in the cell; the character does not drift
   vertically between poses when they are flipped through in sequence.
6. **Consistency with REF-01.** Same proportions, same plate segmentation, same
   scarf length. A pose that is a different character is rejected however good
   it is.

---

## 7. What this sheet deliberately does not specify

- **Facial detail.** There is none — the visor is the face, and at 18 x 28 any
  feature behind it is one ambiguous pixel.
- **Per-frame animation.** Each state is one static image. The run's stride tell
  is currently a `sin(tick * 0.7)` 2 px offset, scissoring the legs and
  counter-swinging the arms (`_body_parts`); whether
  that stays as code motion under a static sprite or is dropped is a
  `CHANGE-BRIEF.md` decision, not an art one.
- **The enemies.** Slimes and flying horses are out of scope for this sheet. If
  they are generated at all they get their own section, and they inherit the
  contrast rule of section 3 unchanged — more so, because a hazard that cannot
  be seen against the platform it patrols is a fairness bug, not a style
  problem.

---

## 8. Open

- **REF-01 has not been generated.** Nothing in section 5 can be judged until it
  exists.
- **The generator is not chosen.** It should be one that records a seed, so the
  art log can reproduce the request *and* the output — which Suno could not do
  for the music, and which `ASSET-LOG.md` already names as the reason to prefer
  a seeded tool for everything after the music.
