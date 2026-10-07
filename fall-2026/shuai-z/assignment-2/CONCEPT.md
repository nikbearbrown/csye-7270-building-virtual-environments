# CONCEPT — walker-rudy

> Draft v4, 2026-10-01. Written in English with Claude Code from my answers to a design intake. The design decisions are mine. Changes between drafts are logged in FRICTIONAL.md.

## The game in two sentences

You play Rudy, a cheerful chibi boy with medium-length, center-parted blond hair that leans toward light brown, green eyes and a grey robe with a large hood worn down, who crosses a medieval countryside to reach the teleport circle at the end of each level. He runs, jumps and stomps goblins; with a sword and shield or a magic staff he can also fight and block, until a hit knocks the gear away.

## Core loop

- **Repeat:** cross a short stretch of cliffs, spikes and monsters to the next safe ground.
- **Decide:**
  - Avoid or fight: jump past an enemy, stomp it, or (with gear) cut it down or shoot it.
  - Block a shot from the front, or step out of its path. Blocking does not protect against touching an enemy.
  - When hurt, take a risky detour for a health pack, or stay on the safe line. Hearts carry into the next level, so a heart regained now still counts later. At full health a pack does nothing; golden packs in later levels will raise the maximum.
  - Carry the sword or the staff. The sword defeats a goblin in one hit, but only up close. The staff fires one bolt per press from a distance, and needs two to defeat a goblin. You can hold only one; picking up the other swaps it.
- **Risk:** any hit (an enemy, a shot, spikes) knocks the gear away first, and costs one of three hearts after that. Falling off a cliff is instant death. At zero hearts Rudy restarts from the last checkpoint. A short invulnerability after each hit keeps one mistake from turning into three.

## Design pillars

| Pillar | Experience it protects | A visual or sound choice that honors it |
|---|---|---|
| **P1 — Your gear is your plan** | Picking the sword or the staff changes how you deal with what is ahead | Each form has its own silhouette at game size: a short sword with a shield, or a long staff with a magic barrier. Each attack has its own sound: a light steel swish or a soft magic chime |
| **P2 — Read every threat** | It is always obvious when an enemy is attacking, and from where | Every enemy attack has a clear, readable pose, and its projectile stands out from the painted background. Each shot plays the enemy's ordinary attack sound with no extra warning, because enemies fire slowly enough to react to |
| **P3 — It stings, then you try again** | A mistake costs something, but never makes you want to quit | On a hit, the gear visibly drops away and Rudy flashes while invulnerable. The hurt sound is short, and the music dips instead of stopping |
| **P4 — A journey into another world** | The world feels bigger than the path you are on, and worth crossing | A castle on the far horizon, on a slow parallax layer behind the fields, and a folk theme led by lute and recorder |

## Art direction

Characters are chibi (2–3 heads tall) in clean anime cel shading, with fine, even linework inside a bold dark outer outline that is added in-engine, and flat, neutral lighting, so the same sprites work under any level's light and still stand out. Backgrounds are painterly and detailed, with watercolor and gouache texture, careful natural light and a muted, warm, low-saturation palette; the world should feel grounded and real rather than bright and effects-heavy, and the play space stays free of busy scenes of village life. The split serves the pillars: flat, outlined characters and attacks read at once against the soft painted world (P2), while the painted fields and the distant castle make the world feel larger than the path (P4).

- **Materials:** ripe wheat and meadow grass, weathered fieldstone, old timber, worn wool and linen; a stone castle far away.
- **Light:** a clear autumn afternoon with low, warm sun, long soft shadows and a little haze in the distance.
- **Era and mood:** the late-medieval European countryside at harvest time, where golden wheat meets green meadow; quiet, warm and unhurried.

**Known risk:** Rudy's blond hair and grey robe could disappear against yellow wheat and grey stone. The robe stays grey; the outer outline keeps him visible. The silhouette and palette checks in the character sheet must test him against the actual Level 1 background.

## Audio direction

The music should feel like a light, unhurried country adventure with a faraway flavor. It uses a small folk ensemble (plucked lute-like strings, wooden flute or recorder, fiddle, frame drum) at a gently bouncing mid tempo, in a major or modal key, with no vocals. Sound effects are soft and warm rather than harsh: a padded stomp, a light sword swish, a gentle magic chime for the staff, a wooden knock when the shield blocks and a soft hum when the barrier does, a short non-vocal hurt cue, and a bright shimmer at the teleport circle. Every sound event also has a visual cue, so the game still reads with the sound muted.

| Moment | Music |
|---|---|
| Normal play | One loop plays continuously through the level |
| Hurt | Dips briefly under the hurt sound, then returns |
| Death (cliff or zero hearts) | Dips during the respawn and carries on; it does not restart from the top |
| Pause | Drops to a low volume until play resumes |
| Teleport circle reached | Fades out under the arrival shimmer; the level ends in quiet |

## Level 1 — Harvest Fields

A forgiving level of about 30 seconds on a clear autumn afternoon, in the wheat fields outside a village, with a castle far away. On the way are cliffs, spikes, patrolling goblins, and a stationary mushroom monster, rooted in the ground, that aims at Rudy and puffs balls of spores at him. Both enemies can be stomped. The only gear in this level is the sword and shield: the shield blocks the spores from the front, but they cannot be cut down. A waystone in the middle of the level is the checkpoint, and there is no health pack. The level ends at the teleport circle, and a "Level complete" card looks down on the road ahead to the castle. Later levels (not designed yet) add the staff, golden health packs, and enemies that cannot be stomped.

## Open questions

None at the moment. The ranged monster (draft v2's open question) is the mushroom monster.

## Revisions after design-v1

- **2026-10-01, Rudy's look, after his reference was generated:** he is about 3.4 heads tall rather than 2–3. His robe has a thin pale trim along the hood edge, the front opening, the cuffs and the hem. See CHARACTER-SHEET.md, revision 2.
- **2026-10-02, falling and zero hearts, after the greybox playtests:** a fall off a cliff is no longer instant death. It costs one heart and sends Rudy back to the last checkpoint with the hearts he has left. At zero hearts, by a hit or a fall, he no longer restarts from the last checkpoint: the level starts over from the opening, as if the game had just begun. See CHANGE-BRIEF.md.
- **2026-10-03, the hurt sound, after it was generated:** the hurt cue is a short cry (SFX-HURT, 0.2 s), not a non-vocal sound. I chose the take that sounds like a character crying out when hurt. This replaces "a short non-vocal hurt cue" in the audio direction; the hurt sound stays short, as P3 asks. The slice also has six sound effects instead of ten: the fall plays the hurt sound, the waystone lights up in silence, and the spore and block sounds are cut with the mushroom. See CHANGE-BRIEF.md.
- **2026-10-04, the mushroom cut:** Level 1 in the slice has no mushroom monster, so no spores and no blocking; its threats are the cliffs, the spikes and the goblins. The section above keeps it as designed. See CHANGE-BRIEF.md, build step 4 cut.
- **2026-10-03, the title:** the game is called *Walker Rudy*, after the repository. The title shows over the opening of Level 1 with "Level 1 · Harvest Fields" under it, in the engine's default font, as on the end card (STORYBOARD.md panel 1). I chose both.
