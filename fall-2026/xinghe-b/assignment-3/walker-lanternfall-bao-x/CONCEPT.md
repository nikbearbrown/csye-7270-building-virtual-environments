# Lanternfall — Concept

`walker-lanternfall-bao-x` · Bao Xing · CSYE 7270 Assignment 2 · **v1 written 2026-09-28, before any generation**

> Frozen at tag `design-v1`. Later changes go under **Revisions** at the bottom; nothing above that line is rewritten.

## In two sentences

A lamp-headed courier is trapped in a fog-bound midnight market, and the light on his shoulders is his only weapon. Keep moving, grow the light, and survive three minutes until the fog lifts.

## Core loop

1. **Move** — the only thing the player does moment to moment (WASD / arrows / left stick).
2. **Weapons fire on their own** — the Beam shoots along the direction of travel; Lamp-Moths orbit the courier.
3. **Enemies break into lamp-oil gems**; walking near a gem pulls it into the satchel.
4. **A full oil gauge levels you up**: the run pauses and you pick 1 of 3 upgrade cards.
5. **The fog thickens** every 30 seconds — more moths, then fog-wraiths.
6. **Both weapons at level 3 → the Sunflare Lighthouse card appears**; taking it fuses them into one pulsing burst of light.
7. **Survive 3:00 to win, or lose all HP** — either way, R starts a fresh run instantly.

## Design pillars

1. **Light is power.** Everything that helps you is warm light; everything that hurts you is cool fog. Growing stronger literally makes the screen brighter around you.
2. **Feet, not fingers.** Movement is the only verb. Every real decision lives in the level-up cards: which weapon, which branch, when to take the evolution.
3. **Readable in silence.** Every event that has a sound also has a visual: hit flash, knockback, gem flight, pause-and-cards, banner, result panel. Sound adds feeling, never information you need.
4. **Three-minute runs.** A run is short, a loss costs nothing, retry is one key. The player should always want "one more".

## Systems in this slice

| System | Details |
|---|---|
| Beam | Starts at level 1. Branches: **Quick Wick** (fire 25 % faster) or **Long Wick** (+1 pierce). Max level 3. |
| Lamp-Moths | Unlocked by a card (2 moths). Branches: **Another Wing** (+1 moth) or **Wider Flight** (larger orbit). Max level 3. |
| Passives | Light Boots (speed), Magnet Satchel (pickup range), Thick Glass (max HP). Two levels each. |
| Evolution | Beam 3 + Moths 3 → **Sunflare Lighthouse**: both weapons are replaced by a radial light burst every 2 s; the courier's colours brighten; the music gains a layer. |
| Enemies | **Moth** — fast, fragile, 1 damage. **Fog-wraith** — slow, tough, 2 damage. |
| Pacing | Spawn density rises in six 30-second steps. |
| Health | 10 HP, 0.8 s of invulnerability after each hit, with knockback. |

## Art direction

- **View:** 3/4 top-down; camera follows the courier inside a bounded market square.
- **Form:** flat-vector shapes with a thick dark outline, reduced to small pixel sprites (courier 32 × 32) and locked to fixed palettes so every frame matches.
- **Warm vs cool:** the courier, his weapons and pickups use the warm character palette; enemies and the ground use the cool fog palette.
- **Value rule:** player and pickups are the brightest things on screen, enemies are mid-value, the ground is darkest. Readability is checked with muted play.

Character palette: `#F2B84B` lamp gold · `#FFF1C9` glow cream · `#2E3A59` coat navy · `#8A5A3C` satchel brown · `#14121C` outline ink.
Environment palette: `#0E1020` night · `#1F2540` deep fog · `#3B4A6B` mid fog · `#6E7FA3` light fog · `#C7D0E0` mist · `#F2B84B` lantern gold · `#B5523B` stall red · `#14121C` ink.

## Audio direction

- **Good events** (kill, pickup, level-up, evolution, win) are soft, warm and glassy — bells, chimes, small pops.
- **Harm** (hurt, lose) is dull, low and muffled — a thud, a guttering flame.
- **No harsh high transients**, because kills and pickups happen many times a minute; frequent sounds are short and throttled so they never machine-gun.

## Music: when it plays, changes and stops

| Moment | Music |
|---|---|
| Title menu | Silent (the fog is quiet until you step in). |
| Run starts / restarts | Night-market loop starts from the top; a second "Sunflare" layer runs silently in sync. |
| Level-up cards | Loop ducks by 6 dB so the choice feels like a held breath. |
| Pause | Loop keeps playing, muffled (low-pass) and 10 dB quieter. |
| Sunflare evolution | The Sunflare layer fades in over 2 s. |
| Lose | Loop fades out over 0.5 s, then the lose stinger. |
| Win (3:00) | Loop fades out over 1 s, then the win stinger. |

Mute: **M** all audio, **9** music only, **0** effects only. The game is fully playable muted.

## Semester goal (outside this slice)

More weapons and evolution recipes, a boss at the end of the fog, between-run progression, saving, and more than one market map.

## Starting point and tools

- Started from a **blank Godot 4.7.2 project**. The Lamp-Head Courier is carried over from my Assignment 1, [walker-jumpman-bao-x](https://github.com/yanxlh/walker-jumpman-bao-x), which extended [nikbearbrown/walker-jumpman](https://github.com/nikbearbrown/walker-jumpman).
- This concept was worked out in a brainstorming session with Claude; the Walker `/gdd` skill was not used. The choices of genre, weapons, branching upgrades, evolution rule, theme, scope and local models were mine.

## Revisions

### R1 · 2026-09-29 · Beam aims at the nearest enemy (was: along the direction of travel)

- **Observed:** with the greybox build, scripted bots died in 22–98 s at level 1–3 with 4–15 kills. Firing along the direction of travel means that fleeing — the natural survival move — points the Beam *away* from the enemies chasing you. Aiming and dodging were the same input, which contradicts pillar 2 ("feet, not fingers").
- **Tried:** A — tuning only (slower moths, 15 HP, slower first wave): still dead by 77–156 s, level ≤ 4, ≤ 22 kills. B — Beam targets the nearest enemy, tuning unchanged: 107 s / 141 s / **won at 3:00**, level 7–11, 169–296 kills. Raw numbers: `evidence/balance-probe-before-aim.txt`, `evidence/balance-probe-after-aim.txt`.
- **Decision (Bao):** B. The Beam now flies toward the nearest enemy; with no enemy on screen it uses the last movement direction. The courier's **facing still follows horizontal movement** exactly as the character sheet says; only the projectile's direction changed.
- **Verified by:** `test_gameplay.gd::beam-aims-nearest` (an enemy above the standing courier dies, a farther one to the right does not).

### R2 · 2026-09-29 · 2D pixel art, and fewer poses (Bao's direction)

- **Observed:** the first ART-PC-01 batch (FLUX.1-schnell, "flat vector" prompt; seeds 11, 23, 37) came out as a shaded, 3D-looking illustration. After seeing it I decided: "不用3d就是2d像素游戏，然后不用太多动作" — this is a 2D pixel-art game, and the courier does not need many actions.
- **Change:** art direction is now **2D pixel art**: every sprite is prompted as a pixel-art game sprite (hard-edged pixels, flat colour, 1-px dark outline, no gradients or 3D shading) and still reduced to its game size and locked to the palettes. The map stays top-down with side-view sprites. The courier's pose set drops to the rubric minimum of **10** (see CHARACTER-SHEET R2).
- **Evidence:** the rejected batch and the reason are in ASSET-LOG (ART-PC-01) and `gen/rejected/ART-PC-01-contact.png`.

### R3 · 2026-09-29 · Every level needs more XP (Bao's request after the first play)

- **Asked:** "每升一次等级后续所需要的经验会增加".
- **Found:** the table already rose (3, 5, 7, … 40) but stopped at 40 from level 13 on.
- **Change:** the table is kept for levels 1–12; after that each step is one bigger than the last (46, 53, 61, 70, …; level 30 needs 301). The HUD now shows `XP have/need` next to the level so the rising cost is visible, including with sound off.
- **Verified by:** `test_logic.gd::prog-xp-need-always-increases` (failed on the plateau, passes now) and `test_gameplay.gd::hud-shows-xp-need`.

### R4 · 2026-09-29 · A fuller market, tougher monsters over time, more cards (Bao's requests after the first play)

- **Map** — "整体地图再丰富一点材料": the arena becomes two market streets — stalls and noodle carts facing each other, lantern posts between them (with a soft pool of light), crates beside stalls, puddles and fallen leaves on the cobbles, and a clear plaza around the spawn. All decoration: nothing collides. Five new generated props (CHANGE-BRIEF R4); the environment palette gains the satchel brown `#8A5A3C` for wood.
- **Monsters over time** — "随着时间增加怪兽的血量也随时间按比例增加": a monster's HP is its base HP × (1 + 0.5 × whole minutes survived) at the moment it spawns (×1.5 from 1:00, ×2 from 2:00, ×2.5 at 3:00). A continuous curve was tried first: it made every moth need two Beam hits from the first second, and scripted bots died in 36–84 s; stepped per minute, a gem-collecting bot evolved at ~1:30 and survived 3:00 in 2 of 3 runs (`evidence/balance-probe-after-hp-growth.txt`).
- **New cards** — "增加伤害和增加武器的攻击速度，人物吸取经验的范围，人物移动速度": **Hotter Flame** (+20% damage for every weapon) and **Quick Hands** (+12% attack speed for every weapon: Beam cooldown, moth spin and hit rate, Sunflare period), 5 levels each; **Magnet Satchel** (pickup range) and **Light Boots** (move speed, now +12 px/s per level) go from 2 to 5 levels. Cards show the level they would reach, e.g. "Quick Hands (4/5)".
- **Verified by:** `test_gameplay.gd::enemy-hp-grows-with-time`, `damage-card-scales-weapons`, `haste-card-shortens-beam-cooldown`, `map-*`; `test_logic.gd::prog-new-passives-offered`, `prog-passive-caps`, `prog-damage-mult`, `prog-attack-rate-mult`, `prog-card-title-shows-level`.

### R5 · 2026-09-29 · Solid props (Bao: "路灯这些有阻挡效果")

- Lantern posts, stalls, noodle carts and crates now **block the courier**; the courier slides along their edges instead of sticking. The box is each sprite's opaque area inset by 2 px (a post blocks only at its pole), so what you bump into is what you see. Puddles and leaves stay walk-over decals.
- **Enemies are not blocked** — moths fly over the stalls and fog-wraiths drift through them. This keeps the lore, avoids enemies jamming behind posts, and means props can corner you rather than shelter you.
- **Verified by:** `test_gameplay.gd::map-has-solids`, `props-block-the-courier`, `courier-slides-along-props`, `decals-do-not-block`, `enemies-pass-through-props`.

### R6 · 2026-09-29 · A broken-up market (Bao: "整体地图应该破碎一点")

- The two tidy streets of R4 are replaced by **14 scattered clusters** with alleys between them: ragged rows of stalls and carts with gaps and a slight bend, lantern corners around wet squares, abandoned crate piles, lone stalls with a lamp — plus stray posts and crates. Overview: [design/map-overview.png](design/map-overview.png).
- Solid props never overlap (the R4 layout had 6 crates overlapping stalls); layout and collision use fixed boxes measured from the sprites, so the map is identical with or without textures loaded.
- **Verified by:** `test_gameplay.gd::map-is-broken-up` (stall/cart rows spread over 9 of 18 bands; the street layout had 4), `props-do-not-overlap`, `solid-boxes-match-sprites`, `map-layout-deterministic`.

### R7 · 2026-10-02 · Art references in words, and one visual or audio choice per pillar

- **References (words, no artists):**
  1. a brass oil lamp and paper-lantern light at night — small, warm, hard-edged light sources;
  2. wet cobblestones under fog — cool blue-grey, low contrast, the darkest values on screen;
  3. a late-night street market of wooden stalls, cloth awnings, noodle carts and crates — worn wood, an old town, quiet and slightly eerie.
- **One choice per pillar:**
  1. *Light is power* — warm gold for everything that helps, cool fog for everything that hurts; the Sunflare brightens the courier's coat and adds a music layer.
  2. *Feet, not fingers* — the card screen freezes the field and ducks the music by 6 dB, so the one real decision has no time pressure.
  3. *Readable in silence* — every sound has a visual twin (hit flash and knockback, gem flight, cards, banner, result panel), and the HUD prints MUSIC/SFX on/off.
  4. *Three-minute runs* — the result panel shows "R / Y" to retry or play again; R stops the stinger and restarts the music from the top at once.
