# STORYBOARD.md — six panels across the slice

**Written 2026-10-03, before any art or sound effect has been generated.**

## What these panels are, and what they are not

**The level already exists.** It was built for Assignment 1 and it already
divides itself into six signposted sections — the label text below is read out
of `godot/levels/first_steps.json`, not invented for this document:

| | label in the level | label drawn at x | section runs to |
|---|---|---|---|
| 01 | `GET MOVING` | 33 | 474 |
| 02 | `MIND THE GAP` | 474 | 862 |
| 03 | `PICK A ROAD` | 862 | 1544 |
| 04 | `SOMETHING PATROLS` | 1544 | 2100 |
| 05 | `CONTESTED LANDINGS` | 2100 | 2700 |
| 06 | `LAST STAND` | 2700 | 3072 (level width) |

The x values are the label draw positions in the level file; a section runs
from its own label to the next one.

So the panels are **retrospective about gameplay and forward-looking about
appearance**. What happens in each one is already decided and testable; what it
*looks and sounds like* is the thing this assignment changes, and that is the
column every panel below actually commits to. Labelling it the other way round —
pretending the storyboard designed the level — would be the easiest sentence to
write and the only dishonest one in the file.

A storyboard for a level that already runs is still worth drawing, for one
reason: it is the only artefact that puts **pose, sound and background in the
same frame**. The character sheet specifies poses in isolation and the change
brief specifies wiring in isolation. Neither of them can catch "the scarf reads
fine on the test background and disappears here".

## The hand-drawn sketches

**Drawn 2026-10-03.** Seven frames in pen on one sheet, photographed as
`design/storyboard/sheet-2026-10-03.jpg` and cropped into
`design/storyboard/panel-01.jpg` … `panel-06.jpg`, plus
`panel-06-death.jpg` for the death variant of panel 06.

The sheet's own numbering is not this document's. The frames were drawn in the
order they came to hand; the mapping is recorded here rather than renumbered on
the paper, because the paper is the evidence:

| frame on the sheet | panel |
|---|---|
| 1 | 01 `GET MOVING` |
| 2 | 04 `SOMETHING PATROLS` |
| 3 | 03 `PICK A ROAD` |
| 4 | 02 `MIND THE GAP` |
| 5 | 05 `CONTESTED LANDINGS` |
| 6 | 06 `LAST STAND` |
| 7 | 06, death variant |

What a sketch has to show, and it is a low bar on purpose — the point is the
composition, not the draughtsmanship:

- the character, at roughly its real size relative to the platform
- which pose from `CHARACTER-SHEET.md` section 5 it is in
- where the camera edge is
- the one thing in the frame the player is supposed to be looking at

---

## Panel 01 — `GET MOVING`

| | |
|---|---|
| Sketch | `design/storyboard/panel-01.jpg` — drawn 2026-10-03 (sheet frame 1) |
| Where | x 0 – 474, the long opening platform; spawn is (64, 320) |
| In frame | the character, the 48 × 16 step at x 160, the single fixed spike at x 320, the label `01 / GET MOVING` and `Read the landing. Then jump.` |
| Poses | **P1 Idle**, then **P2 Run**, then **P3 Rising** |
| Sound | music loop enters here (`MUS-B-01` or `-02`); `SFX-JUMP` on the first jump |
| Pillar | 4 — readable at 18 × 28. This is the first frame anyone sees the character in. |

**What the panel has to prove.** That the character reads at all. The opening
platform is dark slate and the sky above it is cream, so this single frame
contains both of the backgrounds from `CHARACTER-SHEET.md` section 3 — body at
1.12:1 against the platform, visor at 1.32:1 against the sky. **If the scarf is
not doing its job, this is where it shows**, before any complication.

---

## Panel 02 — `MIND THE GAP`

| | |
|---|---|
| Sketch | `design/storyboard/panel-02.jpg` — drawn 2026-10-03 (sheet frame 4) |
| Where | x 474 – 862; gaps at 448–512 and 736–784, a raised 48 × 32 block at x 576 |
| In frame | the character airborne over a gap, both platform edges, the label `02 / MIND THE GAP` |
| Poses | **P3 Rising** into **P4 Falling** |
| Sound | music; `SFX-JUMP` |
| Pillar | 1 — every failure teaches. A missed gap is the cheapest lesson in the level. |

**What the panel has to prove.** That rising and falling are distinguishable
*against the sky*, where the visor contributes almost nothing (1.32:1) and only
the `shade` outline and the scarf are carrying the silhouette. The scarf's
direction is the tell: below-and-behind rising, above-and-behind falling.

---

## Panel 03 — `PICK A ROAD`

| | |
|---|---|
| Sketch | `design/storyboard/panel-03.jpg` — drawn 2026-10-03 (sheet frame 3) |
| Where | x 862 – 1544, the fork |
| In frame | **both roads at once** — the high planks at y 224 and y 200, the low floor at y 320 with three pop-up traps (spikes at x 1160, 1296, 1432), the slime patrolling the high road between x 1356 and 1424, and both labels: `HIGH ROAD - GUARDED` and `LOW ROAD - IT BITES` |
| Poses | **P1 Idle** at the decision point; the branch is not drawn |
| Sound | music only — deliberately |
| Pillar | 3 — choose the risk |

**What the panel has to prove.** That the choice is legible *before* it is made.
This is the one panel where the character is standing still and the composition
has to carry everything, so it is the panel most likely to fail on background
clarity rather than on the character.

**The one thing the player should be looking at** is not the character — it is
the two labels. That is worth drawing explicitly, because it is the only panel
in the slice where that is true.

---

## Panel 04 — `SOMETHING PATROLS`

| | |
|---|---|
| Sketch | `design/storyboard/panel-04.jpg` — drawn 2026-10-03 (sheet frame 2) |
| Where | x 1544 – 2100 |
| In frame | the character mid-swing, a slime patrolling x 1580 – 1690, a flying horse at y 268 patrolling x 1700 – 1820, the label `One slash is enough. Touching one is not.` |
| Poses | **P6 Attack windup** (4 ticks) and **P7 Attack live** (9 ticks) |
| Sound | music; `SFX-SLASH` on the transition into windup |
| Pillar | 1 and 3 |

**What the panel has to prove, and it is the hardest one.** The sword is **not
generated** — `CHANGE-BRIEF.md` C2 keeps it code-drawn so it cannot drift from
the kill hitbox. So the sketch must show the generated *body* committing to a
swing with a code-drawn blade over it, and the two must look like one action.

The live window is 9 ticks — 150 ms. If windup and live are not distinguishable
as still images, the player cannot learn the timing, and the only thing left
teaching it is `SFX-SLASH`. That is a real dependency between an art decision
and a sound decision, and this panel is where it is visible.

---

## Panel 05 — `CONTESTED LANDINGS`

| | |
|---|---|
| Sketch | `design/storyboard/panel-05.jpg` — drawn 2026-10-03 (sheet frame 5) |
| Where | x 2100 – 2700, four 128 px platforms with 64 px gaps |
| In frame | the character dashing across a gap, a horse holding the gap at y 268, a slime on the far platform, the label `The horses hold the gaps.` |
| Poses | **P5 Dash** (10 ticks, 167 ms) |
| Sound | music; this is the loudest, busiest stretch |
| Pillar | 2 and 3 |

**What the panel has to prove.** That the dash reads as a *committed*,
horizontal, non-invincible move. The dash is the only pose with no vertical
lean and a fully extended scarf, and it is the one the player spends once per
airborne period — so it has to look like a decision, not like fast running.

---

## Panel 06 — `LAST STAND`, and the trap

| | |
|---|---|
| Sketch | `design/storyboard/panel-06.jpg` and `panel-06-death.jpg` — drawn 2026-10-03 (sheet frames 6 and 7) |
| Where | x 2700 – 3072; trap triggers at x 2704, spike at x 2800; finish at (3030, 264) |
| In frame | **the moment of the trap**: the character past the trigger, the spike part-way through its 15-tick rise, the finish visible beyond it |
| Poses | **P2 Run**, and the alternate **P8 Death** |
| Sound | `SFX-TRAP` **on the trigger crossing, not on the contact**; `SFX-DEATH` only if it lands |
| Pillar | 2 — the floor is not safe |

**What the panel has to prove, and it is the whole argument of the assignment.**
The player has 96 px of run-up between the trigger at 2704 and the spike at 2800
— 87 px to their leading edge — and 15 ticks of visible rise. The hazard is
already fair on visuals alone; that was established in Assignment 1 and it is
not being changed.

So the sound here cannot make the game *more* fair. It can only make the warning
**arrive sooner than the eye finds it**, or it can be masked by a 124 bpm bed
with pulsing bass and add nothing. `CONCEPT.md` revision 1.1 predicted the
masking in advance and `CHANGE-BRIEF.md` C4 carries the check: a human playtest
of this exact section at full music level.

**This panel is drawn twice** — once at the trigger crossing and once at P8, the
death pose, because P8 does not exist in the build today (`CHANGE-BRIEF.md` C3)
and this is the only place in the storyboard where it can be specified against a
real background.

---

## What the six panels cover between them

| | P1 | P2 | P3 | P4 | P5 | P6 | P7 | P8 |
|---|---|---|---|---|---|---|---|---|
| 01 | ● | ● | ● | | | | | |
| 02 | | | ● | ● | | | | |
| 03 | ● | | | | | | | |
| 04 | | | | | | ● | ● | |
| 05 | | | | | ● | | | |
| 06 | | ● | | | | | | ● |

All eight required poses appear in at least one panel. The three optional poses
(P9 air jump, P10 attack recovery, P11 celebrate) appear in none, which is
consistent with them being the slack in `CHANGE-BRIEF.md` section 2 — if they
are dropped, no panel loses anything.

Both backgrounds appear: cream sky in every panel, dark slate platform in every
panel, and panel 03 is the only one showing the high planks and the low floor
simultaneously.

---

# What the drawings settled, 2026-10-03

## Three things that are now specified and were not before

**1. The death pose, P8, is prone and face-down.** Sheet frame 7 draws the
character flat on the ground, face down, head pointing the way it was
travelling, limbs collapsed. That is a specification — `CHARACTER-SHEET.md`
section 5 only said "the pose the player sees while the retry ticks", and
`CHANGE-BRIEF.md` C3 only said it must be keyed off `session.state`. Prone and
face-down is also the right answer for the reason the panel exists: it is the
one silhouette in the game that is **wider than it is tall**, so it cannot be
confused with any other pose even at 5 mm.

**2. The death frame carries text.** Frame 7 is lettered `You Died.` The build
already prints text on death — `session.gd:516` sets `death_reason` to
"Missed the landing" / "It got you" / "Watch the spikes", drawn by
`hud.gd:47`. So the drawing is asking for a **second**, larger line above the
existing one, not a replacement.

That is a real decision and it is being taken the other way: **the existing
`death_reason` stays and no `You Died.` line is added.** Pillar 1 is "every
failure teaches", and "Watch the spikes" teaches something that "You Died."
does not — the player already knows they died. The drawing is kept as drawn
because it is the record of what was wanted; this paragraph is the record of
why it was not done.

**3. The swing arc is drawn, and it is already in the code.** Frame 2 puts
motion strokes above the blade. `player.gd:344-351` already draws a translucent
wedge, and **only while `attack_phase() >= 2`** — so the bright sweep marks
exactly the ticks that can kill. The sketch and the build agree without either
having been changed to match, which is the best outcome available for a
retrospective panel.

## Where the drawings depart from the appendix, and what is being done about it

| | appendix says | sheet does | action |
|---|---|---|---|
| Character size | 5.4 × 8.4 mm, true scale | roughly 3× that | **accepted.** The frames still read; forcing a redraw at true scale would cost a day and the contrast question is answered by the real sprite on the real background, not by a pen sketch |
| Pose box | one per panel | only on frame 1 | **accepted.** The poses are legible in the frames |
| The four annotation lines | on every page | not written | **accepted**, because this document carries the same information per panel and in more detail |
| Panel 06 trigger line | dashed, 28.8 mm before the spike | not drawn; the spike is at the character's feet | **noted, not redrawn.** The 96 px run-up is the fairness argument and it is measured in `CHANGE-BRIEF.md` C5 against the level file, which is a stronger record than a pen line |
| Panel 03 | two high planks | one | **accepted.** Both roads are present, which is what the panel is for |

None of these is a reason to redraw. All of them are reasons this document, not
the photographs, is where the specification lives.

## Open

- Nothing in the storyboard. All seven frames are drawn and filed.
- The storyboard's job now is to be checked **against** the generated art: each
  pose, once generated, gets placed on its panel's background at true size and
  judged there (`CHARACTER-SHEET.md` section 6).

---

# Appendix — how the six panels are drawn

Written with the panels, so the method is on the record rather than implied by
six photographs.

## The scale, and why it is not negotiable

**1 game pixel = 0.3 mm.** The frame is therefore **192 x 108 mm**, which is the
640 x 360 viewport at a fixed, checkable ratio.

At that scale the character is **5.4 x 8.4 mm** — about the size of a lowercase
letter. That is uncomfortable to draw and it is the entire point. Pillar 4 is
"readable at 18 by 28 pixels"; a storyboard drawn with a 40 mm hero would
answer a question the game never asks. **The character is not enlarged inside
the frame under any circumstances.**

The detail that cannot be drawn at 5.4 mm goes in a separate **pose box** beside
the frame, at 1.25 mm per pixel (a 32 x 32 cell becomes 40 x 40 mm). Two scales
on one page, each honest about what it is for:

| | scale | answers |
|---|---|---|
| Frame, 192 x 108 mm | 0.3 mm/px | does the character read, and where does the eye go? |
| Pose box, 40 x 40 mm | 1.25 mm/px | what is the pose? |

## Where the character sits in the frame

`session.gd:521` — `camera.position.x = clampf(player.position.x + 100, 320,
level.width - 320)`. The camera leads the player by 100 px, so **the player is
at screen x = 220 of 640 — 66 mm from the left edge** for the whole level,
except where the camera clamps.

It clamps at both ends. At the start (camera pinned to 320) the player is
wherever its world x puts it; at the finish (camera pinned to 2752) the player
walks rightward across a fixed frame. Panels 01 and 06 are the two that show
this, and their player positions below differ from 66 mm accordingly.

Camera y never moves (`session.gd:79`, `453`): the view is always world y 0–360,
so **the ground line is at 96 mm from the top of every frame** and the frame's
vertical contents can be measured once and reused.

## Per-page layout

One A4 **portrait** page per panel, six pages.

```
  +--------------------------------------------------+
  |  PANEL 0n  /  <the level's own label>            |   <- heading
  |                                                  |
  |  +--------------------------------------------+  |
  |  |                                            |  |
  |  |            frame, 192 x 108 mm             |  |   <- ruled, 0.3 mm/px
  |  |                                            |  |
  |  +--------------------------------------------+  |
  |                                                  |
  |  +----------+   pose:  P_                       |
  |  | pose box |   sound: ___                      |   <- 40 x 40 mm
  |  | 40x40 mm |   eye:   ___                      |
  |  +----------+   bg:    sky / slate / both       |
  +--------------------------------------------------+
```

The four lines are the panel's actual content. "eye" is the one thing in the
frame the player is meant to be looking at, and it is circled in the frame too.

## Coordinates

Every value is millimetres from the frame's **top-left corner**, derived from
the level file at 0.3 mm/px. The ground line (world y 320) is at 96 mm in all
six. Platform bodies run from their top edge down past the frame's bottom.

### Panel 01 — camera 320 (clamped), frame = world x 0–640

| | x (mm) | top y (mm) |
|---|---|---|
| **character** (P2 Run) | 42.0 | feet on 91.2 |
| step, 48 px wide | 48.0 – 62.4 | 91.2 |
| fixed spike | 96.0 – 103.2 | 91.2 |
| ground | whole width | 96.0 |

### Panel 02 — camera 548, frame = world x 228–868

| | x (mm) | top y (mm) |
|---|---|---|
| **character** (P3 Rising) | 66.0 | mid-air, above 96.0 |
| gap in the ground | 66.0 – 85.2 | — |
| raised block | 104.4 – 118.8 | 86.4 |
| second gap | 152.4 – 166.8 | — |

### Panel 03 — camera 1140, frame = world x 820–1460

| | x (mm) | top y (mm) |
|---|---|---|
| **character** (P1 Idle, at the decision point) | 66.0 | feet on 96.0 |
| high plank 1 | 85.2 – 121.2 | 67.2 |
| high plank 2 | 156.0 – 186.0 | 60.0 |
| slime, patrolling plank 2 | 160.8 – 181.2 | 60.0 |
| trap spike 1 (low road) | 102.0 – 109.2 | 91.2 |
| trap spike 2 | 142.8 – 150.0 | 91.2 |
| trap spike 3 | 183.6 – 190.8 | 91.2 |

Both labels are drawn in the level and both belong in this panel:
`HIGH ROAD - GUARDED` at x 82.8 mm, y 64.2 mm, and `LOW ROAD - IT BITES` at
x 60.0 mm, y 90.0 mm.

### Panel 04 — camera 1720, frame = world x 1400–2040

| | x (mm) | top y (mm) |
|---|---|---|
| **character** (P6 windup / P7 live) | 66.0 | feet on 96.0 |
| slime, patrol span | 54.0 – 87.0 | 96.0 |
| flying horse, patrol span | 90.0 – 126.0 | 80.4 |

### Panel 05 — camera 2370, frame = world x 2050–2690

| | x (mm) | top y (mm) |
|---|---|---|
| **character** (P5 Dash, over the gap) | 66.0 | mid-air |
| platform | 18.6 – 57.0 | 96.0 |
| platform | 76.2 – 114.6 | 96.0 |
| platform | 133.8 – 172.2 | 96.0 |
| horse holding the first gap | 52.2 – 81.0 | 80.4 |
| slime | 82.2 – 109.2 | 96.0 |
| horse | 109.8 – 138.6 | 80.4 |

### Panel 06 — camera 2752 (clamped), frame = world x 2432–3072

The last screenful is fixed, so the whole ending fits in one frame.

| | x (mm) | top y (mm) |
|---|---|---|
| **character** (P2 Run, just past the trigger) | 89.4 | feet on 96.0 |
| the trigger line (invisible in game — draw it dashed) | 81.6 | — |
| trap spike, part-way up | 110.4 – 117.6 | 91.2 at full height |
| horse | 52.8 – 81.6 | 80.4 |
| slime | 146.4 – 170.4 | 96.0 |
| finish | 179.4 – 186.6 | 79.2 |

The gap between the trigger at 81.6 mm and the spike at 110.4 mm is **28.8 mm**
— that is the 96 px of run-up, drawn to scale. It is the measurement the whole
fairness argument rests on, so this panel is the one where the ruler matters
most.

## Capture

Photograph or scan flat, even light, no shadow across the frame, crop to the
page. `design/storyboard/panel-01.jpg` … `panel-06.jpg`.

## When a panel is finished

1. The frame is 192 x 108 mm, ruled, not eyeballed.
2. The character is at its true 5.4 x 8.4 mm and has **not** been enlarged.
3. The scarf is visible and separated from the body — in the frame, at true
   size, not only in the pose box. If it is not, that is the panel telling you
   something about the pose, not about the drawing.
4. The pose box names a pose ID from section 5.
5. The four lines are filled in, and the "eye" subject is circled in the frame.
