# PROMPTS.md — the generation pack, ready to paste

Everything still to be generated, in the order to generate it, with the exact
text to send and where to put what comes back.

**Nothing in this file is a decision.** Every prompt is derived from
`CHARACTER-SHEET.md` (palette, poses, acceptance order) and `CONCEPT.md`
(style, setting, audio direction). If a prompt here disagrees with those, they
win and this file is stale.

---

## 0. Before anything

### The rules this assignment imposes, restated so they are in front of you

- **No named artist.** No "in the style of …".
- **No copyrighted character, franchise or brand.** Not in the prompt, not as
  a reference image.
- **No existing music or recordings**, and no stem-splitting of commercial
  tracks.
- **No voice cloning.**
- **Never paste an API key into anything that gets committed.**

### The tool requirement

**It has to record a seed.** This has been a stated preference since
`CHARACTER-SHEET.md` section 8 and became binding on 2026-10-04, when Suno
turned out to expose no seed and the music became reproducible as a *request*
but not as an *output*.

Candidates that satisfy it: **Stable Audio Open** for the sound effects (built
for foley, and its training set is CC0 / CC-BY / CC Sampling+ from Freesound
and the Free Music Archive, which is a rights story worth having in
`SOURCES.md`); any Stable-Diffusion-family UI for the art, which exposes a seed
by default.

### What to record for every single generation, kept or not

Straight into `ASSET-LOG.md`:

| | |
|---|---|
| Asset ID | the one in this file |
| Model **and version** | e.g. `stable-audio-open-1.0` |
| Where run | the URL or the local tool |
| Licence / terms | what the tool's own terms page says, not what you assume |
| **Seed** | the number |
| Prompt | **verbatim as the tool recorded it**, not as you meant it |
| Settings | steps, CFG, sampler, duration |
| Outcome | kept / rejected, and against which pillar or sheet item |
| Edits | everything you did to it afterwards |

The music section had to be rebuilt from a screenshot because the first version
recorded what I *meant* to send. Don't repeat it — screenshot the tool's own
history as you go, into `design/rejected/`.

---

## 1. Art — `REF-01` first, then eight poses

### Why the reference comes first

`CONCEPT.md` revision 1.2: **one reference image, then every pose derived from
it.** Consistency comes from the reference, not from repeating the prompt text
— which direction A's four rewordings already demonstrated in audio, where
changing the sentence changed nothing that mattered.

### The constraints every prompt below inherits

| | |
|---|---|
| Cell | **32 × 32 px**, character anchored at **(20, 30)** from the top-left |
| Facing | **right only** — the engine mirrors for left, and generating both risks two characters |
| Palette | exactly the eight below |
| Rim | **light, on the back and the top only** — not a dark outline, not all four sides |
| **No sword** | the blade stays code-drawn, because it and the kill hitbox come from the same three numbers |

```
plate       #1f3a6e   near-side armour: chest, near arm, near leg
shade       #16233d   far side, recessed abdomen, jawline, neck
visor       #7fe3ff   the slit
glint       #d8f7ff   the slit's leading edge
scarf       #8a5cf0   scarf and belt sash
scarf_tip   #6a3fbf   the scarf's far end
steel       #4a5468   gauntlets and boots
steel_edge  #9aa7bd   the rim light
```

### `CHAR-REF-01` — the reference

Generate this at a workable size (512 px or larger), **not** at 32 × 32. It is
reduced afterwards.

> pixel art character reference, side view facing right, standing, small
> humanoid ninja in deep navy segmented plate armour, horizontal light-blue
> visor slit across the helm, short neck clearly separating helm from chest,
> chest wider than the waist, long purple scarf trailing behind, two arms and
> two legs clearly separated, far arm and far leg painted a darker navy than
> the near arm and near leg, pale steel gauntlets and boots, pale rim light
> along the back and the top edge of the figure only, limited palette of eight
> colours, hard edges, no gradients, no glow, no text, no weapon, plain flat
> background, dungeon torchlight from above and behind

Generate **four**, pick one, log the other three as rejections with the reason.

### The eight required poses, derived from `CHAR-REF-01`

Use the chosen reference as an image input (img2img / reference / IP-adapter —
whatever the tool calls it) at a strength that keeps the character and changes
the pose. Append the pose line to the reference prompt; keep everything else
identical, **including the seed where the tool lets you**.

| ID | pose line to append | what it has to say |
|---|---|---|
| `CHAR-P1` | `standing still, weight even, scarf settled, visor forward` | the baseline everything is judged against |
| `CHAR-P2` | `mid-stride running, body leaning forward, scarf streaming back, arms swinging opposite to the legs` | one contact pose, not a cycle |
| `CHAR-P3` | `airborne rising, far knee bent and lifted, scarf below and behind` | **must differ from P4 by the scarf's direction** |
| `CHAR-P4` | `airborne falling, legs reaching down, scarf above and behind` | ditto |
| `CHAR-P5` | `horizontal air dash, body level with no vertical lean, scarf fully extended straight back` | has to look like a decision, not fast running |
| `CHAR-P6` | `arm raised up and back, body coiled, about to strike, empty hand` | 4 ticks on screen — **67 ms** |
| `CHAR-P7` | `arm swept down and forward through a strike, body committed, empty hand` | 9 ticks — **150 ms**; must be tellable from P6 as a still |
| `CHAR-P8` | `lying face down flat on the ground, head forward, limbs collapsed, seen from the side` | **0.55 s**; the only pose wider than it is tall |

**P6 and P7 have no sword in them.** If the model draws one, reject the frame —
a blade in the sprite would stop tracking the hitbox the moment anyone touched
the tuning, and the failure would be silent.

### Save them as

```
design/character/CHAR-REF-01-{a,b,c,d}.png     all four, including rejects
design/character/CHAR-P1.png … CHAR-P8.png     the chosen frames, full size
godot/assets/poses/p1-idle.png … p8-death.png  after scripts/import_pose.py
```

### Then run the importer on each

```bash
python scripts/import_pose.py design/character/CHAR-P1.png --id p1-idle
```

It snaps to the eight colours, places the cell and anchor, and **prints the
acceptance checks from `CHARACTER-SHEET.md` section 6** — palette conformance,
contrast against the dungeon wall and the lit platform edge, the anchor, and a
silhouette render. It does not decide anything; it tells you which rule a frame
breaks.

---

## 2. Sound effects — four, replacing the placeholders

The four in the build are **synthesised by arithmetic**, not generated
(`SOURCES.md` section 4). Replacement is file-for-file: no trigger, assertion,
level or balance changes.

**Keep the durations close.** `sfx-all-four-are-loaded-at-their-synthesised-lengths`
asserts them within ±0.02 s. If a generated effect is a different length, the
honest move is to **update that assertion to the new number and say so in
`CHANGE-BRIEF.md`** — not to delete it, and not to loosen it to a range.

### `SFX-JUMP` → `godot/assets/sfx-jump.ogg` · target **0.11 s**

> short crisp video game jump sound effect, single rising blip, clean synthetic
> tone sweeping upward in pitch, very short, dry, no reverb, no music

### `SFX-SLASH` → `sfx-slash.ogg` · target **0.14 s**

> short sword swing whoosh, sharp air movement passing quickly, bright noisy
> transient falling in pitch, dry, no impact, no reverb, no music

### `SFX-TRAP` → `sfx-trap.ogg` · target **0.26 s** — **the one with a brief**

`CONCEPT.md` revision 1.1 predicted on 2026-10-01 that a 124 bpm bed with
pulsing bass would mask this, and specified the answer in advance: **a moving
pitch, which percussion does not have**, so it is told apart by motion rather
than by level.

> rising metallic alarm sweep, mechanism winding up quickly, inharmonic struck
> metal partials sliding upward in pitch, getting louder towards the end,
> tense, dry, no reverb, no music, no voice

Judge it **over the music**, never on its own — there is a ready-made A/B in
`masking-test.ogg`. The one that sounds best in isolation is not the one that
wins here.

### `SFX-DEATH` → `sfx-death.ogg` · target **0.45 s**

> short low impact thud with a descending tone, muffled body fall, dark,
> final, slight downward pitch glide, dry, no reverb, no music, no voice

### After replacing any of them

```bash
"$GODOT" --headless --path godot --script res://tests/test_game.gd
```

`sfx-trap-fires-on-the-trigger-not-the-contact` still has to report a lead of
at least 15 ticks. It was **35** with the placeholders.

---

## 3. Optional, only if the art goes quickly

| | |
|---|---|
| `CHAR-P9` | `airborne rising after a second jump, both knees tucked` |
| `CHAR-P10` | `arm following through after a strike, lowered, empty hand` |
| `CHAR-P11` | `standing, arms raised, celebrating` |
| **At least one environment asset** | a dungeon wall or floor tile |

The environment one is worth more than P9–P11: it is a second *kind* of
generated art rather than a ninth frame of the first kind.

> seamless tileable pixel art dungeon stone wall texture, dark cold stone
> blocks with staggered mortar joints, very low contrast, quiet and unobtrusive
> background, limited palette, flat lighting, no text, no characters

**It must stay quiet.** `CONCEPT.md` revision 1.3: mortar is 1.18:1 against the
wall and the arches 1.10:1 on purpose, because the strong contrast is spent on
what the player interacts with. A beautiful, busy wall is a failed wall.

---

## 4. Checklist

- [ ] `CHAR-REF-01` × 4 generated, one chosen, three logged as rejections
- [ ] `CHAR-P1` … `CHAR-P8` generated from the chosen reference
- [ ] each run through `scripts/import_pose.py`, each check read
- [ ] `SFX-JUMP` / `SLASH` / `TRAP` / `DEATH` generated
- [ ] `SFX-TRAP` judged **over the music**, not alone
- [ ] suite re-run, 113 checks still passing
- [ ] every generation logged in `ASSET-LOG.md` with **model, version, seed,
      verbatim prompt, settings, outcome, edits**
- [ ] tool history screenshotted into `design/rejected/`
- [ ] the tool's licence terms read and written into `SOURCES.md`
