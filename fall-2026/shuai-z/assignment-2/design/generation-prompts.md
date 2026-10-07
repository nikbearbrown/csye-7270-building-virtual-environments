# Generation prompts — v2

> Claude Code drafted these from CHARACTER-SHEET.md, STORYBOARD.md and CHANGE-BRIEF.md.
>
> - **v1** (2026-09-30) is preserved at the `design-v1` tag.
> - **v2** (2026-10-01) follows the accepted reference CHAR-REF-07: no prompt names the character any more (see SOURCES.md), every pose attaches CHAR-REF-07, and the proportions and robe trim follow that image.
> - **Audio** (2026-10-01): the sound-effect and music prompts at the end, drafted from CONCEPT.md's audio direction and CHANGE-BRIEF.md's event-to-sound map.
> - **Run redo** (2026-10-02): a new CHAR-RUN-B and CHAR-SWORD-RUN-B, after the step 2a playtest (see "Run redo" under Rudy).
>
> The asset log records the exact prompt actually used for each output.

## How to use them

1. **The reference is done.** CHAR-REF-07 (`generated/accepted/CHAR-REF-07.jpg`) is accepted; see ASSET-LOG.md. Judge every new image with `python3 design/tools/check_against_sheet.py IMAGE --views POSE -o generated/checks/ID-check.png`.
2. **Every pose is an edit of the reference.** Attach CHAR-REF-07 (the full-size file) and describe only the change of pose. Consistency comes from the reference image, not from repeating the text.
3. **Enemies and props match the reference's style.** Attach CHAR-REF-07 as a style reference, and say that it shows a different character.
4. **Save every output under its ID and a number**, such as `CHAR-REF-01.png`, in `_raw/`. That is a local working folder of full-size downloads, kept out of git. Then:
   - an accepted output is copied unchanged to `generated/accepted/`;
   - a rejected output goes in `generated/rejected/` as a small thumbnail or on a contact sheet, as the assignment asks;
   - the edited, game-ready version goes into the Godot project.

   All three are committed.
5. **Record for each output:** the model name and version exactly as the tool shows them, the date, the exact prompt, the attached images, and the size or aspect ratio. Hosted chat tools do not expose a seed, so write "seed: not available".
6. If an image comes back with a visible watermark, note it in the asset log, and check the tool's terms before cropping it out.
7. Never add the name of an artist, a studio, a game or a franchise to any prompt.
8. The bold outer outline is added in-engine at game size, so the generated outline only has to be fine and even.
9. Do not name the character in a prompt; say "the boy".

## Shared style blocks

These are already written out in full inside each prompt below. They are listed here so that every prompt can be checked against the same wording.

**Sprite style** (characters, enemies, props, hazards):

```text
Style: a 2D game sprite in anime style. Clean cel shading with exactly two tones per color (a flat base and one flat shadow), a fine dark-brown outline of even weight, and flat, neutral front lighting: no rim light, no glow, no cast shadow, no gradients. One figure, centered, with empty margin around it. Background: one plain, flat, solid steel-blue color (#4F7CAA) filling the whole image, with no floor, no shadow, no other objects and no text.
```

**Background style** (the parallax layers):

```text
Style: a painterly, hand-painted 2D game background, like a high-quality TV anime background: detailed watercolor and gouache textures, soft natural light, a muted natural palette with low saturation and warm earthy tones, atmospheric depth, subtle film grain. A grounded, believable late-medieval European countryside in autumn, on a clear afternoon. No characters, no animals, no text.
```

## Rudy

### CHAR-REF — done: CHAR-REF-07 accepted

The v1 prompt below was turn 1 of the Gemini chat. It is kept here as the record; it still names the character, which v2 prompts no longer do.

```text
A character turnaround sheet of one boy, Rudy, shown four times side by side at exactly the same height and scale, standing in a relaxed neutral pose with his arms at his sides: front view, three-quarter view, side view facing right, and back view.
Rudy is a cheerful boy drawn in chibi proportions, exactly 2.5 heads tall (his head is 40% of his height). Medium-length blond hair with a light-brown tint (browner than golden blond), parted in the middle with curtain bangs framing his face, covering his ears and ending at the nape, drawn with visible strands and texture rather than a flat fill; one cowlick curling up from the crown. Large green eyes and a small, friendly smile. A plain knee-length slate-grey mage robe with long sleeves and a large hood; the hood is down, lying across his shoulders and upper back. A brown leather belt and brown leather boots. No hat, no jewelry, no emblem, no weapon.
Style: a 2D game sprite in anime style. Clean cel shading with exactly two tones per color (a flat base and one flat shadow), a fine dark-brown outline of even weight, and flat, neutral front lighting: no rim light, no glow, no cast shadow, no gradients. Background: one plain, flat, solid steel-blue color (#4F7CAA) filling the whole image, with no floor, no shadow, no other objects and no text.
Wide image, 16:9.
```

### Pose edits (attach CHAR-REF-07)

Paste this template and replace `[POSE]` with one line from the table:

```text
Use the attached image as the exact character reference: draw the same boy, with the same proportions, face, center-parted light-brown hair with its strands and cowlick, green eyes, slate-grey robe with the large hood down and the thin pale trim along the hood edge, the front opening, the cuffs and the hem, brown belt and boots, colors and outline. Draw only one figure: the boy in side view facing right, [POSE]. Keep the same cel-shaded style, flat neutral lighting and the same plain, solid steel-blue background (#4F7CAA). Change nothing except the pose. Square image.
```

| ID | `[POSE]` |
|---|---|
| CHAR-IDLE | standing relaxed, with his weight slightly forward and a cheerful look |
| CHAR-RUN-A | running, contact pose: the front foot just touching the ground, the back leg stretched out behind him, body leaning forward, arms swinging opposite to the legs |
| CHAR-RUN-B | running, passing pose: the supporting leg straight under his body, the other knee bent and lifted as it passes, body leaning forward |
| CHAR-RISE | jumping upward: knees tucked, arms raised, hair and robe pulled downward by the upward motion |
| CHAR-FALL | falling: legs stretched down, ready to land, arms out for balance, hair and robe lifted by the fall |
| CHAR-HURT | hurt: recoiling from a hit coming from the right, leaning back, eyes squeezed shut, arms flung out |
| CHAR-DEFEAT | defeated: sitting on the ground with his legs out, dizzy, eyes shut, a small sad smile |
| CHAR-RESPAWN | getting back up: one knee on the ground, pushing himself up with a determined smile |
| CHAR-CELEBRATE | celebrating: a small hop with one fist raised high and a big happy smile |

### Sword form

**CHAR-SWORD-IDLE** (attach CHAR-REF-07). This image becomes the reference for the sword form.

```text
Use the attached image as the exact character reference: the same boy, with the same proportions, face, hair and cowlick, eyes, grey robe with the large hood down and its pale trim, belt, boots, colors and outline. Draw only one figure: the boy in side view facing right, in a ready stance, holding a short, plain, straight steel sword in one hand with the blade pointing forward and down, and a small round wooden shield with a plain iron rim and no emblem on the other arm. Keep the same cel-shaded style, flat neutral lighting and the same plain, solid steel-blue background (#4F7CAA). Square image.
```

**Slash and block** (attach CHAR-SWORD-IDLE). Paste this template and replace `[POSE]`:

```text
Use the attached image as the exact reference for the character, the sword and the shield. Draw only one figure: the boy in side view facing right, [POSE]. Keep the same style, colors, outline, lighting and the same plain, solid steel-blue background (#4F7CAA). Change nothing except the pose. Square image.
```

| ID | `[POSE]` |
|---|---|
| CHAR-SWORD-SLASH | mid-slash, swinging the sword in a wide horizontal arc in front of him, body twisted into the swing, the shield pulled in close |
| CHAR-SWORD-BLOCK | blocking: the shield raised in front of him toward the right, body braced, knees bent, the sword held back |

**Sword-form movement**: CHAR-SWORD-RUN-A, -RUN-B, -RISE and -FALL. Attach the default pose first and CHAR-SWORD-IDLE second.

```text
Keep exactly the pose, body and background of the first attached image. Add the sword and shield exactly as they look in the second attached image, held naturally for this pose. Change nothing else.
```

### Run redo: CHAR-RUN-B, the other contact pose (after the step 2a playtest)

In the game, CHAR-RUN-A and CHAR-RUN-B-02 both have the same leg behind him, so the two-frame run looks like hopping on one foot. The new CHAR-RUN-B is the other contact pose: the same stride with the legs and arms swapped, so the two frames alternate legs. It is an edit of the accepted run frame, which keeps its size, lean and framing.

New chat. Attach `generated/accepted/CHAR-RUN-A-01.jpg` first and CHAR-REF-07 second:

```text
Edit the first attached image, which shows this boy running in side view facing right, in the contact pose. Use the second attached image as the exact character reference. Draw the next step of the same run: the same contact pose with the legs and arms swapped. The leg that is stretched out behind him now becomes the front leg, its foot just touching the ground in front of him, and the front leg now stretches out behind him. The arms swing the other way too: the arm that reaches forward now swings back, and the arm that is back now swings forward. Keep the same forward lean, stride length, size and position in the frame, and keep him facing right. Keep the same cel-shaded style, flat neutral lighting and the same plain, solid steel-blue background (#4F7CAA). Change nothing except the legs and arms. Square image.
```

If the legs come back unchanged, a second turn: "The legs are still the same as in the first image. The boot that is behind him in the first image must now be in front, touching the ground, and the front boot must be behind him."

**Then CHAR-SWORD-RUN-B:** a new chat with the sword-form movement prompt above, unchanged, attaching the new CHAR-RUN-B first and CHAR-SWORD-IDLE-01 second.

**Outcome (2026-10-02):** dropped. The new sword-form run frame came back with the same legs as CHAR-SWORD-RUN-A, so CHAR-RUN-B-02 and CHAR-SWORD-RUN-B-01 stay as they are. See FRICTIONAL.md and ASSET-LOG.md.

## Environment

### ENV-SKY-CASTLE — far parallax layer (new image)

```text
A wide panoramic far background for a side-scrolling game, seen at eye level. A clear autumn afternoon sky with a few soft clouds and low, warm sunlight. Low, hazy blue-green hills along the lower third. A grey stone castle, small and far away on a hill in the right third, softened by haze. Nothing in the foreground: the lowest part of the image is distant hills only, so that a field layer can sit in front of it.
Style: a painterly, hand-painted 2D game background, like a high-quality TV anime background: detailed watercolor and gouache textures, soft natural light, a muted natural palette with low saturation and warm earthy tones, atmospheric depth, subtle film grain. A grounded, believable late-medieval European countryside in autumn. No characters, no animals, no text.
The widest aspect ratio available (21:9 if possible, otherwise 16:9), at the largest size.
```

### ENV-FIELDS — middle layer (new image)

```text
A middle-ground layer for a side-scrolling game, seen straight from the side at eye level: rolling golden-yellow wheat fields meeting a green meadow, with a few small trees and a low wooden fence far behind. No buildings, no people, no busy village scenes. Even detail across the whole width, so that it can repeat horizontally. The fields fill only the lower half of the image; above them the image is one flat, solid pale blue (#CFE0E6) with no clouds and no detail, so that it can be cut away.
Style: a painterly, hand-painted 2D game background, like a high-quality TV anime background: detailed watercolor and gouache textures, soft natural light, a muted natural palette with low saturation and warm earthy tones, subtle film grain. Late-medieval European countryside in autumn, clear afternoon. No characters, no animals, no text.
The widest aspect ratio available, at the largest size.
```

### ENV-GROUND — ground strip (new image), then the cliff edge (edit)

```text
A side-view ground strip for a 2D platformer: packed earth with a band of short grass and a few wheat stalks along the top, and warm brown soil with small stones below. A straight, level, crisp top edge, and detail spread evenly so that it can repeat from left to right. Painterly hand-painted texture with watercolor and gouache, a muted warm earthy palette, soft natural light. The strip is isolated on one plain, flat, solid steel-blue background (#4F7CAA), with nothing else in the image and no text. Wide image, 16:9.
```

Cliff edge (attach the chosen ENV-GROUND):

```text
The same ground strip, exactly as attached, but ending on the right in a rough, crumbling cliff edge that drops straight down. Keep the same style, colors and plain steel-blue background. Change nothing else.
```

### ENV-SPIKES (new image)

```text
A short row of five sharp iron spikes set in a weathered wooden base, seen from the side, clearly dangerous.
Style: a 2D game sprite in anime style. Clean cel shading with exactly two tones per color, a fine dark-brown outline of even weight, flat, neutral front lighting, no glow, no cast shadow, no gradients. Centered, with empty margin. Background: one plain, flat, solid steel-blue color (#4F7CAA), with no floor, no other objects and no text. Square image.
```

### ENV-WAYSTONE — dark (new image), then lit (edit)

```text
A waist-high, weathered standing stone used as a checkpoint, seen from the side, with one simple invented rune carved into its face; the rune is dark. A little moss at its base.
Style: a 2D game sprite in anime style. Clean cel shading with exactly two tones per color, a fine dark-brown outline of even weight, flat, neutral front lighting, no glow, no cast shadow, no gradients. Centered, with empty margin. Background: one plain, flat, solid steel-blue color (#4F7CAA), with no floor, no other objects and no text. Square image.
```

Lit (attach the chosen dark stone):

```text
The same stone, exactly as attached, but the carved rune now glows soft white-blue and gives off a faint glow. Change nothing else.
```

### ENV-PORTAL (new image)

```text
A magic teleport circle drawn on the ground, seen from a low side angle so that it looks like a flat ellipse: rings of simple invented runes and plain geometric lines glowing a soft gold-white, with faint motes of light rising from it. No stars, no letters, no real-world symbols.
Style: a 2D game sprite in anime style, with clean cel shading and a fine dark-brown outline where there are solid edges; the circle itself may glow. Centered, with empty margin. Background: one plain, flat, solid steel-blue color (#4F7CAA), with nothing else in the image and no text. Wide image, 16:9.
```

### ENV-ENDCARD — the "Level complete" card (new image)

```text
A high, elevated view looking down over a late-medieval European countryside in autumn: a dirt road winds from the bottom left of the image, between golden wheat fields and green meadows, all the way to a grey stone castle small on the far horizon. Near the start of the road, a faint, softly glowing magic circle lies on the ground. No characters, no animals, no text. Leave calm sky at the top for a title to sit on.
Style: a painterly, hand-painted 2D game background, like a high-quality TV anime background: detailed watercolor and gouache textures, soft natural light, a muted natural palette with low saturation and warm earthy tones, atmospheric depth, subtle film grain. A clear autumn afternoon.
16:9, at the largest size.
```

## Props, enemies and UI

### PROP-SWORDSHIELD (attach CHAR-SWORD-IDLE)

```text
Draw only the sword and shield from the attached image, unchanged in shape and color, as a floating game pickup: the short straight sword crossed over the small round wooden shield, with a faint warm glow around them. No character. Same cel-shaded style and dark-brown outline, on the same plain, solid steel-blue background (#4F7CAA). Square image.
```

### ENEMY-GOBLIN (attach CHAR-REF-07 as a style reference)

```text
Match the art style of the attached image exactly (the same cel shading, outline weight, flat lighting and plain steel-blue background), but draw a different character: a small goblin enemy in the same chibi proportions, 2 heads tall and a little shorter than the boy in the reference. Grey-green skin, long pointed ears, a big nose, a mischievous grin, a ragged brown cloth tunic, bare feet, no weapon. One figure, side view facing right, mid-walk. Square image.
```

Second walk frame (attach the chosen goblin):

```text
The same goblin, exactly as attached, in the other walking pose, with the other leg forward. Change nothing else.
```

Squashed (attach the chosen goblin):

```text
The same goblin, exactly as attached, squashed flat by a stomp from above, dizzy. Change nothing else.
```

### ENEMY-MUSHROOM (attach CHAR-REF-07 as a style reference)

The mushroom must not resemble any existing game's mushroom: it has no feet, and its cap is not red with white spots.

```text
Match the art style of the attached image exactly (the same cel shading, outline weight, flat lighting and plain steel-blue background), but draw a different character: a stationary mushroom monster rooted in the ground, with no legs and no feet. A squat, lumpy, pale stem with two small dark eyes and a round mouth, under a wide, drooping, rust-orange autumn cap with a few darker ochre speckles. Grumpy rather than cute, about two-thirds as tall as the boy in the reference. One figure, side view facing right. Square image.
```

Attack (attach the chosen mushroom):

```text
The same mushroom monster, exactly as attached, attacking: the cap squeezes down and the mouth opens wide, puffing one ball of violet spores toward the right. Change nothing else.
```

Squashed (attach the chosen mushroom):

```text
The same mushroom monster, exactly as attached, squashed flat by a stomp from above, its cap crumpled. Change nothing else.
```

### FX-SPORE (new image)

```text
A single small, round ball of dusky violet spores, slightly brighter at the core, with a soft, dusty edge: a projectile for a 2D game. Clean cel shading with a fine dark-brown outline; it may glow softly. Centered, with empty margin, on one plain, flat, solid steel-blue background (#4F7CAA), with nothing else in the image. Square image.
```

### UI-HEART (new image)

```text
Two small heart icons for a game's health display, side by side: a full heart in warm red, and an empty heart drawn as an outline only. Clean cel shading with exactly two tones, a fine dark-brown outline, flat lighting. On one plain, flat, solid steel-blue background (#4F7CAA), with nothing else and no text. Wide image.
```

## Sound effects

Drafted 2026-10-01 from CONCEPT.md's audio direction and CHANGE-BRIEF.md's event-to-sound map, and written to work in any text-to-sound-effect tool. I generated SFX-JUMP in Adobe Firefly (Generate sound effects) and, from SFX-STOMP on, generate them in ElevenLabs' sound effects; both on free plans, and each prompt gives four takes.

On 2026-10-02 the list was cut to six sounds (CHANGE-BRIEF.md, revisions): SFX-JUMP, SFX-STOMP, SFX-HURT, SFX-PORTAL, SFX-SLASH and SFX-PICKUP. The four cut rows are kept below for the record and are not generated.

### How to use them

1. **One prompt, one sound.** Paste the shared block and then the line for the sound. If the tool has a duration setting, set it to the upper end of the target length; if it has a prompt-strength setting, keep it high.
2. **Make three or four takes of each sound** (one prompt gives four in both tools) and keep the best. Save every take as `ID-NN` (for example `SFX-JUMP-01.wav`) in `_raw/`, and follow step 4 of *How to use them* above for accepted and rejected takes.
3. **Record for each take:** the model name and version, the date, the exact prompt, the duration and any other settings, and the seed if the tool shows one. Firefly's page shows no model name, but each WAV's Content Credentials do: its XMP chunk links to a manifest that names the model and version.
4. **Game-ready version:** trim the silence at the start (the sound must begin on the event's frame), trim or fade the tail, convert to mono, normalize the peak to about −1 dBFS, and export as WAV. `design/tools/prepare_sfx.py` does this from the accepted take, with each sound's cut points in its `CUTS` table, and keeps the take's Content Credentials link. The edits go in the asset log.
5. **Listen in context.** Jump and slash play many times a minute, so they must not tire the ear; play each one ten times in a row before accepting it.
6. Never add the name of a game, a franchise, a studio or a composer to any prompt.

### Shared block

```text
A single short sound effect for a cozy 2D fantasy platformer. Soft, warm and rounded rather than harsh or loud. Clean and close, dry with almost no reverb, no music, no voice, no background noise, no other sounds.
```

### Prompts

| ID | Target length | Prompt (after the shared block) |
|---|---|---|
| SFX-JUMP | 0.2–0.35 s | `A quick, light jump: a soft upward whoosh of air with a little flutter of a cloth robe. Gentle and springy, not cartoonish.` |
| SFX-STOMP | 0.25–0.4 s | `A padded stomp: a soft, cushioned thump of small boots landing on top of a small creature, with a tiny squishy pop. Satisfying but gentle, no crunch, no bones.` |
| SFX-PICKUP | 0.5–0.8 s | `Picking up a sword and a wooden shield: a light metallic shing of a short blade, followed by a bright, rising two-note pluck on a lute-like string. Rewarding and cheerful.` |
| SFX-HURT | 0.3–0.5 s | `A short, non-vocal hurt sound: a soft muffled thud followed by a quick falling pluck on a wooden string instrument. It stings a little but stays soft. No voice, no groan, no scream.` |
| SFX-PORTAL | 2–3 s | `Arriving at a magic teleport circle: a bright, airy shimmer that swells upward, made of soft glassy bell tones and sparkling high chimes, then rings out and fades to silence. Wondrous and calm, a sense of completion, not a fanfare.` |
| SFX-SLASH | 0.2–0.3 s | `A light sword swish: a quick, airy swipe of a short steel blade cutting through the air. Thin and clean, no clang, no impact.` |
| SFX-SPORE | **cut** (0.3–0.5 s) | `A mushroom creature puffing out a ball of spores: a soft, dusty puff of air, like squeezing a small pouch of powder, with a faint low wobble. Clearly an attack, but not alarming.` |
| SFX-BLOCK | **cut** (0.2–0.35 s) | `A ball of soft spores hitting a small wooden shield: a hollow wooden knock with a little dusty puff as it bursts. Short and solid, no metal ring.` |
| SFX-FALL | **cut** (0.8–1.2 s) | `Falling off a cliff: a soft, descending whistle of wind that drifts away and fades out, with no impact at the end. Gentle, a little comic, not scary.` |
| SFX-CHECKPOINT | **cut** (1–1.5 s) | `An old standing stone waking up as a checkpoint: a low, warm hum of resonant stone, with a gentle chime blooming on top, then a soft fade. Reassuring and calm.` |

If a take keeps adding music or a voice, add `Only the sound effect.` at the end of the prompt. If the hurt sound keeps coming back with a voice, drop the word "hurt" and describe only the thud and the pluck.

## Music

### MUS-LOOP — the Level 1 theme

One track loops for the whole level, from the title through play (CHANGE-BRIEF.md, music behavior). The level takes about 30 seconds, so a 60–90 second loop plays about once and does not wear out when the player retries.

**In a text-to-music tool with a style field** (turn on *instrumental*, and leave the lyrics empty):

```text
instrumental folk, medieval countryside, warm and unhurried adventure, plucked lute, wooden recorder, fiddle, frame drum, gently bouncing, 104 BPM, D mixolydian, no vocals
```

**In a tool that takes a full description:**

```text
An instrumental loop for a cozy 2D fantasy platformer level set in late-medieval farmland at harvest time, on a warm autumn afternoon with a castle on the far horizon. A small folk ensemble: a plucked lute-like string instrument plays the steady rhythm, a wooden recorder carries a simple, singable melody, a fiddle answers it and adds a soft counter-line, and a frame drum keeps a light, bouncing beat. Gently bouncing mid tempo at 104 BPM in 4/4, in D mixolydian, so it feels cheerful with a slightly faraway, old-world flavor. Light, unhurried and adventurous, warm rather than epic: no orchestra, no choir, no electronic sounds, no vocals. Steady energy all the way through, with no big intro, no build-up and no ending, so that it can loop.
```

**How to use it:**

1. Make several takes, and keep the one with the clearest melody and the steadiest tempo. The recorder melody must not compete with the sound effects; if it is busy or very high, ask for `a calmer, simpler melody`.
2. Many tools add an intro and an ending anyway. Choose a stretch of 16 or 32 bars in the middle (about 37 or 74 s at 104 BPM), cut it at bar lines on zero crossings, and check that the last bar leads back into the first. This is predicted failure 4 in CHANGE-BRIEF.md.
3. Export as OGG Vorbis, stereo, with the peak about −1 dBFS and the loudness around −16 LUFS, so the sound effects sit on top. In Godot, turn on Loop in the import settings, then listen to at least three repetitions.
4. Record the model and version, the date, both prompts, the settings, the take chosen, and the start and end of the cut in the asset log.
5. If the tool changes the tempo or key on its own, write down what it chose; only the loop length depends on the BPM.

**Used (2026-10-04):** the style-field prompt, unchanged, in Suno v6 mini on the free plan. The song came back at about 105 BPM in D major and repeats every 24 bars, so the loop is 24 bars (54.87 s), cut by `design/tools/prepare_music.py` with a one-beat crossfade at the seam; it is mono because I exported my recording as mono, and it sits at −19.2 LUFS, since −16 LUFS would have passed the −1 dBFS peak. See `generated/logs/2026-10-04-suno-MUS-LOOP.md`.
