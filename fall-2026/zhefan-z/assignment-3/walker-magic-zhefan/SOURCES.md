# Sources

> Started 2026-10-01; updated through the Assignment 2 slice (2026-10-07). Every tool and model used to make assets for this project, with accepted and rejected outputs and every edit. Anything still marked TODO is unknown to the author and is listed in `TODO.md`.

## Generation tools

| Tool | Version | Source | License | Used for |
|---|---|---|---|---|
| Google Gemini (Gemini web app, image generation) | Google Gemini app, model shown in the app: Gemini 3.8 Flash | https://gemini.google.com | Google Terms of Service and Generative AI Additional Terms | Every generated image: mage, wolf, FX, cave tiles and background. See **Generated images** below. |
| ComfyUI | v0.38.1 (commit `20ca544ee0436721d8eb5f544665e490609f72c8`) | https://github.com/comfyanonymous/ComfyUI | GPL-3.0 | Running Stable Audio Open locally |
| Stable Audio Open 1.0 | `model.safetensors` at commit `f21265c1e2710b3bd2386596943f0007f55f802e` (sha256 `7b20458a…66b57e`) | https://huggingface.co/stabilityai/stable-audio-open-1.0 | Stability AI Community License (last updated July 5, 2024) — gated; accepted by the author on Hugging Face | Sound effects |
| T5-base text encoder (for Stable Audio Open) | `model.safetensors` at commit `a9723ea7f1b39c1eae772870f3b547bf6ef7e6c1` (sha256 `a9090354…c8f5b4`) | https://huggingface.co/google-t5/t5-base | Apache-2.0 | Text conditioning for Stable Audio Open, as in ComfyUI's official audio example (https://comfyanonymous.github.io/ComfyUI_examples/audio/) |
| Google Gemini (Gemini web app, music generation: Lyria) | Google Gemini app, model shown in the app: Gemini 3.8 Flash; music generation in the app (Lyria); the Lyria version was not shown in the app | https://gemini.google.com | Google Terms of Service and Generative AI Additional Terms | MUS-LOOP source track `Beneath_the_Unlit_Stone.mp3`. See **Music** below. |
| Suno (free plan) | v4.5-all and V6 Preview | https://suno.com | Suno Terms of Service (free plan: non-commercial) | **Rejected** for MUS-LOOP; nothing used. See **Music** below. |

## Generated images (Google Gemini)

Accepted images stay full size; rejected ones are kept only as 256 px-wide thumbnails in the group's `rejected/` folder.

- **`*-thumb.png`:** thumbnail from a screenshot of the Gemini output; original download not kept. Claude made these in claude.ai from screenshots the author had shared there; the author put them in the repo. This covers all 13 `.png` thumbnails: CHAR-CAST v1, v2, v4 · CHAR-RUN v1, v2 · ENEMY-WOLF-DOWN v2 · WOLF-R1 run v0, run v1, lunge v1, down v1, derived · ENV-TILES v1 · ENV-BG v2.
- **`*-thumb.jpg`:** made from the original downloaded file (CHAR-REF v1, v3 · CHAR-RUN-PASSING v0).

**Workflow change:** the mage and the first wolf round shared one long Gemini chat, and earlier images started leaking into new ones (the mage's head in a wolf frame, cave paintings in the tiles). From the wolf onward, each asset group got its own Gemini chat to stop this context bleed.

### Mage — `design/character/generated/` (chat 1, shared)

| Asset | Status | File | Notes |
|---|---|---|---|
| CHAR-REF v1 | rejected | `rejected/CHAR-REF-v1-thumb.jpg` | Staff broke into loose pixels at 64 px (see CHARACTER-SHEET Revision 1). Prompt: see **Image prompts** → CHAR-REF v1. |
| CHAR-REF v2 | **accepted** | `CHAR-REF-v2.jpg` | Mid-thigh tunic and thicker staff accepted in Revision 1. Prompt: see **Image prompts** → CHAR-REF v2 (edit of v1). |
| CHAR-REF v3 | rejected | `rejected/CHAR-REF-v3-thumb.jpg` | Unchanged from v2. Prompt: see **Image prompts** → CHAR-REF v3 (edit of v2). |
| CHAR-IDLE v1 | **accepted** | `CHAR-IDLE-v1.jpg` | Prompt: see **Image prompts** → CHAR-IDLE v1 (after the setup message). |
| CHAR-RUN-CONTACT attempt 1 | rejected | `rejected/CHAR-RUN-v1-thumb.png` | Two frames side by side, staff cut off, floating foot, ground line. Prompt: see **Image prompts** → CHAR-RUN v1. |
| CHAR-RUN-CONTACT attempt 2 | rejected | `rejected/CHAR-RUN-v2-thumb.png` | Model edited the reference sheet instead of drawing a new pose. Prompt: see **Image prompts** → CHAR-RUN v2. |
| CHAR-RUN-CONTACT v3 | **accepted** | `CHAR-RUN-CONTACT-v3.jpg` | Prompt: see **Image prompts** → CHAR-RUN-CONTACT v3. |
| CHAR-RUN-PASSING v0 | rejected | `rejected/CHAR-RUN-PASSING-v0-thumb.jpg` | See notes. Prompt: an extra version Gemini returned for the **Image prompts** → CHAR-RUN-PASSING v1 prompt. |
| CHAR-RUN-PASSING v1 | **accepted** | `CHAR-RUN-PASSING-v1.png` | Screenshot; see notes. Prompt: see **Image prompts** → CHAR-RUN-PASSING v1. |
| CHAR-RISE v1 | **accepted** | `CHAR-RISE-v1.jpg` | Staff not raised as the prompt asked, but consistent with IDLE. Prompt: see **Image prompts** → CHAR-RISE v1. |
| CHAR-FALL v1 | **accepted** | `CHAR-FALL-v1.jpg` | Prompt: see **Image prompts** → CHAR-FALL v1. |
| CHAR-CAST v1 | rejected | `rejected/CHAR-CAST-v1-thumb.png` | The staff was thrust forward horizontally and passed across her body; the staff head changed shape. The author also realised that a forward-pointing cast pose does not fit mouse aiming in any direction, so the cast design was changed to a raised staff. Prompt: see **Image prompts** → CHAR-CAST v1. |
| CHAR-CAST v2 | rejected | `rejected/CHAR-CAST-v2-thumb.png` | The staff was not raised at all, so the cast barely differed from idle; the crystal glow was yellow-green, too close to the green screen. Prompt: see **Image prompts** → CHAR-CAST v2. |
| CHAR-CAST v3 | **accepted** | `CHAR-CAST-v3.jpg` | File originally named CAST-v1. Yellow-green crystal glow removed in cleanup; glow added in Godot. Prompt: see **Image prompts** → CHAR-CAST v3. |
| CHAR-CAST v4 | rejected | `rejected/CHAR-CAST-v4-thumb.png` | Identical to v3: the model returned the image unchanged, so the author stopped iterating and accepted v3. Prompt: see **Image prompts** → CHAR-CAST v4. |
| CHAR-HURT v1 | **accepted** | `CHAR-HURT-v1.jpg` | Prompt: see **Image prompts** → CHAR-HURT v1. |
| CHAR-FAIL v1 | **accepted** | `CHAR-FAIL-v1.jpg` | Prompt: see **Image prompts** → CHAR-FAIL v1. |
| CHAR-WIN v1 | **accepted** | `CHAR-WIN-v1.jpg` | Prompt: see **Image prompts** → CHAR-WIN v1. |

### Wolf — `design/character/generated/`

Round 1 (chat 1, shared with the mage) was abandoned because the long chat mixed earlier images into new ones. The wolf was restarted in a new, text-only chat (chat 2), and every accepted wolf frame comes from that chat.

| Asset | Status | File | Notes |
|---|---|---|---|
| Round 1 run v0 | rejected | `rejected/WOLF-R1-RUN-v0-bleed-thumb.png` | The mage's head leaked into the wolf. Prompt: see **Image prompts** → WOLF-R1 run; v0 is the downloaded original from that prompt, which differed from what the chat showed. |
| Round 1 run v1 | rejected | `rejected/WOLF-R1-RUN-v1-thumb.png` | Screenshot. Abandoned with round 1. Prompt: see **Image prompts** → WOLF-R1 run (the same prompt as v0; v1 is what the chat showed). |
| Round 1 lunge v1 | rejected | `rejected/WOLF-R1-LUNGE-v1-thumb.png` | Abandoned with round 1. Prompt: see **Image prompts** → WOLF-R1 lunge. |
| Round 1 down v1 | rejected | `rejected/WOLF-R1-DOWN-v1-thumb.png` | Abandoned with round 1. Prompt: see **Image prompts** → WOLF-R1 down. |
| Round 1 frame derived from down v1 | rejected | `rejected/WOLF-R1-DERIVED-thumb.png` | Legs still in the running pose. Prompt: the text-only **Image prompts** → ENEMY-WOLF-RUN v2 prompt, sent by mistake in the old long chat, so the model edited the previous image. |
| ENEMY-WOLF-RUN v2 | **accepted** | `ENEMY-WOLF-RUN-v2.jpg` | Chat 2. Prompt: see **Image prompts** → ENEMY-WOLF-RUN v2. |
| ENEMY-WOLF-LUNGE v2 | **accepted** | `ENEMY-WOLF-LUNGE-v2.jpg` | Chat 2. Prompt: see **Image prompts** → ENEMY-WOLF-LUNGE v2. |
| ENEMY-WOLF-DOWN v2 | rejected | `rejected/ENEMY-WOLF-DOWN-v2-thumb.png` | Chat 2. Legs still in the running pose. Prompt: see **Image prompts** → ENEMY-WOLF-DOWN v2. |
| ENEMY-WOLF-DOWN v3 | **accepted** (partially achieved) | `ENEMY-WOLF-DOWN-v3.jpg` | Listed under Chat 2; the author does not remember which chat it was sent in. Eyes closed, head and ears down; legs unchanged. The defeat motion is handled in the engine: white flash, tilt, cool blue-gray particles. Prompt: see **Image prompts** → ENEMY-WOLF-DOWN v3. |

### FX — `design/character/generated/`

| Asset | Status | File | Notes |
|---|---|---|---|
| FX-FIREBALL-BURST v1 | **accepted** (first try) | `FX-FIREBALL-BURST-v1.jpg` | The downloaded original has semi-transparent ghost blobs and dark fragments along the top; only the fireball and the burst are cropped out in cleanup. Prompt: see **Image prompts** → FX-FIREBALL-BURST v1. |

### Environment — `design/environment/generated/`

| Asset | Status | File | Notes |
|---|---|---|---|
| ENV-TILES v1 | rejected | `rejected/ENV-TILES-v1-thumb.png` | Visible seams when tiled; cave paintings leaked in from the background chat. Prompt: see **Image prompts** → ENV-TILES v1. |
| ENV-TILES v2 | **accepted** | `ENV-TILES-v2.jpg` | Only the uniform dark rock is used as the repeating tile, plus the two end pieces; the brighter wall on the left is discarded. Prompt: see **Image prompts** → ENV-TILES v2. |
| ENV-BG v1 | **accepted** | `ENV-BG-v1.jpg` | Framed composition, fixed to the camera. Prompt: see **Image prompts** → ENV-BG v1. |
| ENV-BG v2 | rejected | `rejected/ENV-BG-v2-thumb.png` | Cave paintings add warm colors, against pillar 2 ("your fire is the only warmth"). Prompt: see **Image prompts** → ENV-BG v1; v2 is a second version Gemini returned for that prompt. |

## Image prompts (Google Gemini app)

Every prompt below is recorded as: **prompt drafted by Claude, sent by me in the Gemini app** (model shown in the app: Gemini 3.8 Flash). Copied verbatim from `design/IMAGE-PROMPTS-from-chat.md` (collected 2026-10-07 from the author's claude.ai chat); headings demoted one level.

**Author checks (answered by the author, 2026-10-07).** The checks below were carried over from that file; the parenthetical questions inside the verbatim copy are left as they were collected.
1. **Sent unchanged:** all image prompts in the file were sent unchanged.
2. **CHAR-RUN v1:** the author does not remember which of the two drafts was sent; both are kept below.
3. **ENEMY-WOLF-DOWN v3:** the author does not remember which chat it was sent in (it is listed under Chat 2 because that is where the file places it).
4. **Images without their own prompt:**
   - **CHAR-RUN-PASSING v0:** an extra version Gemini returned for the CHAR-RUN-PASSING v1 prompt.
   - **WOLF-R1 run v0:** the downloaded original from the WOLF-R1 run prompt, which differed from what the chat showed (v1 is the screenshot of what the chat showed).
   - **WOLF-R1 derived frame:** the text-only ENEMY-WOLF-RUN v2 prompt was sent by mistake in the old long chat, so the model edited the previous image.
   - **ENV-BG v2:** a second version Gemini returned for the ENV-BG prompt.

### Chat 1 — character (CHAR-*)

#### CHAR-REF v1
```
Pixel art character reference sheet for a 2D side-scrolling game. One original character shown four times at exactly the same height: front view, side view facing right, three-quarter view, back view. Solid flat bright green background (#00FF00), no shadows on the background, no text.

Character: a cute young fire mage girl with slender, girlish proportions (about 3.5 heads tall, NOT chibi). Long white twin tails reaching her waist, tied with small red bows. Large red eyes, light blush. Tall indigo witch hat whose tip bends backward, wide slightly drooping brim, red ribbon band with a small gold ember charm and a red ribbon tail hanging from the back. Short indigo capelet with a high collar, wide sleeves with gold cuffs, knee-length gray-brown belted tunic with gold hem trim, small belt pouches, dark stockings, short brown boots. She holds a dark wooden staff in her right hand, about shoulder height, topped with a diamond-shaped red crystal wrapped by a curled branch.

Clean pixel art, 1 px dark outline, limited palette: white #E8E6F0, red #D62839, indigo #3A40A0, gold #D4A63A, gray-brown #6B5A4E, skin #F5DCCD.
```

#### CHAR-REF v2 (edit of v1)
```
Keep everything the same, but: she holds the staff in her RIGHT hand in every view, and make the staff shaft noticeably thicker and the eyes slightly larger so they read at small size.
```

#### CHAR-REF v3 (edit of v2)
```
Edit only the staff position. Keep the character, pose, colors, proportions and background exactly the same.

The staff must be in her RIGHT hand in every view. Describe it by where it appears in the image:
- Front view (1st figure): the staff is on the LEFT side of the image.
- Side view facing right (2nd figure): the staff is held in the hand closest to the viewer, in front of her body.
- Three-quarter view (3rd figure): the staff is on the LEFT side of the image, held in the hand closest to the viewer.
- Back view (4th figure): the staff is on the RIGHT side of the image.

Keep the thicker staff shaft from the last version.
```

#### Setup message (CHAR-REF v2 + 9 pose sketches uploaded, no generation)
```
I'm uploading 10 images for a game character project. Do not generate anything yet, just confirm you understand.

Image 1: my character reference sheet (the side view, 2nd figure, is the standard for everything).
Images 2–10: rough pose sketches, in this order: idle, run contact, run passing, rising, falling, cast, hurt, fail, victory. Use the sketches ONLY for body pose; ignore their faces, the eyepatch and their colors.

For every pose I ask for later: the exact character from image 1, side view facing right, face turned slightly toward the viewer, same proportions, outfit, colors, white twin tails with red bows, thick staff in the hand closest to the viewer. One full-body figure, centered, solid flat bright green background (#00FF00), no text, no ground shadow.
```

#### CHAR-IDLE v1
```
One correction: the tunic is mid-thigh length, exactly as in the reference sheet, not knee-length. Match the reference sheet whenever the text and the image disagree.

Now draw the idle pose (sketch #02 Idle).
```

#### CHAR-RUN v1 (rejected)
```
Now draw run contact and run passing side by side, both figures exactly the same size.
```
(An earlier draft of this prompt said: "...Both figures exactly the same size and on the same ground line, same face angle as the idle you just drew." — mark which one was sent.)

#### CHAR-RUN v2 (rejected; the model edited the reference sheet)
```
Not quite. Please redraw both running frames with these fixes:
- Hold the staff the same way in both frames: one hand only (the hand closest to the viewer), staff tilted slightly forward, not across the body. The whole staff must stay inside the image with a margin around it.
- Run passing (right figure): the supporting foot is flat on the ground, directly under the body; only the other leg is lifted. Both figures' feet touch the same ground level.
- Twin tails the same length as the reference, red bows visible in both frames.
- No ground line, no shadow. Leave empty green space around both figures.
```

#### CHAR-RUN-CONTACT v3 (idle uploaded as base)
```
Do not edit the reference sheet. Use THIS image (the idle sprite I just uploaded) as the base and create a new image with exactly ONE figure.

Change only the legs and arms into a running pose, run contact (sketch #03): front leg reaching forward with the heel touching the ground, back leg pushing off behind, body leaning slightly forward. She holds the staff in one hand only (the hand closest to the viewer), tilted slightly forward, the whole staff inside the image.

Keep everything else identical to the uploaded idle sprite: size, head, hat, hair, outfit, colors, face angle. Same solid green background, no ground line, no shadow.
```

#### CHAR-RUN-PASSING v1
```
Again use the idle sprite as the base and create a new image with exactly ONE figure: run passing (sketch #04). The supporting leg is straight under the body with the foot flat on the ground; the other leg passes under the body with the knee bent and the foot lifted behind. Body leaning slightly forward, twin tails flowing back like in the run contact frame you just drew, staff held the same way as in that frame. Keep size, head, hat, outfit, colors and face angle identical. Same green background, no ground line, no shadow.
```

#### CHAR-RISE v1
```
Again use the idle sprite as the base and create a new image with exactly ONE figure: rising (sketch #05). She is jumping upward: knees tucked up, staff raised a little in the hand closest to the viewer, twin tails hanging down below her because she is moving up. Keep size, head, hat, outfit, colors and face angle identical. Same green background, no ground line, no shadow.
```

#### CHAR-FALL v1
```
Again use the idle sprite as the base and create a new image with exactly ONE figure: falling (sketch #06). She is coming down after a jump: legs extended downward and slightly apart, ready to land, the arm without the staff stretched out for balance, twin tails and the hat ribbon flowing UPWARD above her shoulders because she is falling. Keep size, head, hat, outfit, colors and face angle identical. Same green background, no ground line, no shadow.
```

#### CHAR-CAST v1 (rejected)
```
Again use the idle sprite as the base and create a new image with exactly ONE figure: cast (sketch #07). She thrusts the staff forward, held almost horizontally at shoulder height in the hand closest to the viewer, the red crystal pointing forward with a small bright glow around it. Wide stance, body leaning slightly into the cast, twin tails swinging back. Do NOT draw a fireball or any projectile, only the glow on the crystal. The whole staff must stay inside the image. Keep size, head, hat, outfit, colors and face angle identical. Same green background, no ground line, no shadow.
```

#### CHAR-CAST v2 (rejected; design changed to a raised staff)
```
Change of plan for the cast pose. Use the idle sprite as the base and create a new image with exactly ONE figure: she raises the staff up diagonally in front of her, so the red crystal is held above and slightly in front of her head, glowing brightly. The other hand is open, palm out, near her chest. Focused expression, feet slightly apart, body a little tense. The staff head looks exactly like the reference (same curled branch, same diamond crystal). Do NOT draw a fireball. The whole staff stays inside the image. Keep size, head, hat, outfit, colors and face angle identical. Same green background, no ground line, no shadow.
```

#### CHAR-CAST v3 (accepted)
```
The staff is not raised enough. Redraw the cast pose:
- She raises the staff high with BOTH hands, arms stretched up and forward, so her hands and the staff are in front of the hat brim, never overlapping the hat.
- The staff stands upright in front of her face, and the red crystal is held higher than the tip of her hat.
- Her upper body leans back slightly, the hat tilting back a little with it.
- The crystal glows with a small RED-ORANGE light, not yellow or green.
- The staff head looks exactly like the reference (same curled branch, same diamond crystal). No fireball.
Keep size, hair, outfit, colors and face angle identical. Same green background, no ground line, no shadow.
```

#### CHAR-CAST v4 (rejected; returned identical to v3)
```
Closer, but the staff still points forward. Redraw the cast pose:
- She holds the staff perfectly VERTICAL, raised straight up above her head with both hands, like lifting a lantern. The staff is not tilted forward or backward at all.
- The red crystal is directly above the tip of her hat.
- Her hands are on the shaft above her head, clear of the hat brim.
- The crystal glows RED-ORANGE only. No yellow or green glow anywhere.
- No fireball. Same staff head as the reference.
Keep size, hair, outfit, colors and face angle identical. Same green background, no ground line, no shadow.
```

#### CHAR-WIN v1
```
Use the idle sprite as the base and create a new image with exactly ONE figure: victory pose. She stands on the ground, relaxed and proud: the staff rests diagonally on her shoulder, held near its lower end by the hand closest to the viewer. Her other hand makes a V sign (peace sign) raised beside her face, palm facing the viewer so both fingers are clearly visible. Big happy smile, eyes slightly closed. The whole staff stays inside the image. Do NOT draw sparkles or effects. Keep size, hat, outfit, colors and face angle identical. Same green background, no ground line, no shadow.
```

#### CHAR-HURT v1
```
Use the idle sprite as the base and create a new image with exactly ONE figure: hurt (sketch #08). She is knocked back by a hit from the front: upper body bent backward, head tilted back, eyes squeezed shut, one foot lifted off the ground, the staff tilting backward in her hand, twin tails swinging forward. Do NOT draw impact lines or effects. Keep size, hat, outfit, colors and face angle identical. Same green background, no ground line, no shadow.
```

#### CHAR-FAIL v1
```
Use the idle sprite as the base and create a new image with exactly ONE figure: fail (sketch #09). She has collapsed: kneeling on both knees, upper body slumped forward, head down, eyes closed, sad. The staff has fallen out of her hand and lies flat on the ground in front of her. Her hat has slipped down over her eyes a little. Keep size, hat, outfit and colors identical. Same green background, no ground line, no shadow.
```

### Environment (same chat as the character, CHAR-IDLE-v1 uploaded as a style reference)

#### ENV-BG v1 (accepted; v2 was a variant the app produced with cave paintings)
```
Using the same pixel art style as this character, draw a wide 16:9 background for a 2D side-scrolling game: the inside of a dark underground cave. Damp limestone walls, stalactites hanging from the ceiling, faint distant rock layers, cold desaturated slate blue and gray-brown tones, mostly in deep shadow. Low contrast and darker than the character so she stays the brightest thing on screen. No characters, no floor in the foreground, no text, no light sources.
```

#### ENV-TILES v1 (rejected)
```
Same pixel art style. Draw a horizontal strip of cave ground tiles for a 2D platformer, side view: the top surface is a walkable rocky ledge with a lighter edge highlight, the body below is darker rock. The strip must tile seamlessly left-to-right. Also draw, separately on the right, a left edge piece and a right edge piece that end the ground cleanly where a pit begins, with a clear lighter rim so the edge is easy to see. Slate gray and gray-brown, a little lighter than the background. Solid flat bright green background (#00FF00), no text.
```

#### ENV-TILES v2 (accepted, cropped)
```
Redraw the ground tiles with these fixes:
- NO cave paintings, drawings or symbols anywhere. Plain rock texture only.
- The main strip must tile seamlessly: its left edge and right edge must match exactly, with the same rock pattern and the same brightness, so it can repeat without a visible seam.
- Keep the walkable top ledge with the lighter rim, and keep the two separate edge pieces on the right.
- Uniform dark slate rock below the ledge, no bright patches.
Same solid flat bright green background (#00FF00).
```

### Wolf, round 1 (same long chat; abandoned because of context bleed)

#### WOLF-R1 run
```
Same pixel art style. Draw one cave wolf for a 2D side-scrolling game, side view facing right, running. Lean body, cool gray-blue fur, glowing cyan eyes, clearly an enemy but not gory. Its shoulder reaches about the character's waist height. One figure only, solid flat bright green background (#00FF00), no text, no ground, no shadow.
```

#### WOLF-R1 lunge
```
Use this wolf as the base and create a new image with ONE figure: the same wolf lunging forward to attack, body stretched out low, front legs reaching forward, mouth open showing teeth, ears back. Keep size, colors, the cyan eyes and the style identical. Same green background, no ground, no shadow.
```

#### WOLF-R1 down
```
Use the first wolf (the running one) as the base and create a new image with ONE figure: the same wolf defeated, lying on its side on the ground, legs limp, eyes closed. Not bloody, no wounds. Keep size, colors and pixel art style identical. Solid flat bright green background (#00FF00), no ground, no shadow.
```

### Chat 2 — wolf, round 2 (new chat, text only, nothing uploaded)

#### ENEMY-WOLF-RUN v2 (accepted)
```
Pixel art sprite for a 2D side-scrolling game: a cave wolf enemy, side view facing right, running at full speed. Lean body, cool gray-blue fur with lighter gray highlights, glowing cyan eyes, pointed ears, bushy tail. Clean anime-style pixel art with a 1 px dark navy outline, flat cel shading with one shadow and one highlight tone, limited palette. Clearly an enemy, but not gory. One figure only, centered with empty space around it, solid flat bright green background (#00FF00), no text, no ground, no shadow, no other characters.
```

#### ENEMY-WOLF-LUNGE v2 (accepted)
```
Use the wolf you just drew as the base and create a new image with ONE figure: the same wolf lunging forward to attack, body stretched out long and low, front legs reaching far forward, back legs extended behind, mouth open showing teeth, ears flat back. Keep size, colors, cyan eyes, outline and style identical. Same green background, no ground, no shadow, no other characters.
```

#### ENEMY-WOLF-DOWN v2 (rejected; legs unchanged)
```
Do NOT reuse the running or lunging pose. Draw the same wolf (same fur colors, cyan eyes, outline, size and style) defeated: lying flat on its side on the ground, its back at the top and belly toward the viewer, all four legs limp and stretched out sideways, head resting down, eyes closed. Not bloody, no wounds. One figure only, same solid flat bright green background (#00FF00), no ground, no shadow, no other characters.
```

#### ENEMY-WOLF-DOWN v3 (accepted, partial)
```
Pixel art sprite for a 2D side-scrolling game: a defeated cave wolf collapsed on the ground, side view, head toward the right. Its belly is pressed flat against the ground, all four legs splayed out flat and limp, chin resting on the ground, ears drooping, eyes closed, tail lying flat behind it. The whole body is low and horizontal, much lower than a standing wolf. Lean wolf with cool gray-blue fur and lighter gray highlights, spiky fur on the back. Clean pixel art with a dark navy outline, flat cel shading with one shadow and one highlight tone. Not bloody, no wounds. One figure only, centered, solid flat bright green background (#00FF00), no text, no ground line, no shadow, no other characters.
```
(Check: was this sent in a new chat, or in the same wolf chat? The result kept the lunge pose, which suggests the same chat.)

### Chat 3 — FX (new chat)

#### FX-FIREBALL-BURST v1 (accepted)
```
Pixel art sprite sheet for a 2D side-scrolling game, two separate small images side by side: on the left, a fireball projectile flying to the right, a round bright yellow-white core inside orange flames with a short flame trail behind it; on the right, a small fire burst explosion for when it hits, orange and red flames spreading out from the center. Clean pixel art with a dark outline, warm colors only: no green, no yellow-green. Solid flat bright green background (#00FF00), no text, no other objects.
```

## Sound effects (Stable Audio Open 1.0)

Generation: ComfyUI, 3 variants per sound with fixed seeds 1, 2, 3; prompts, settings and hashes in `design/audio/sfx-gen-log.md`. The first run clipped in 10 of 18 files and was regenerated at -6 dB with the same seeds (content unchanged). Raw WAVs stay outside the repo in `E:\7270\tools\sfx_raw\`.

Picks are the author's, after listening. Reason for every pick: it matches the on-screen action better and reads more clearly; the other seeds fit the action less well or were less clear.

| Sound | Picked | Rejected | Edits (`tools/trim_sfx.py`) | In the slice |
|---|---|---|---|---|
| SFX-CAST | seed 3 | seeds 1, 2 | trim leading silence, cut to 0.4 s, 10 ms fade-out, level match | `assets/audio/sfx/SFX-CAST.ogg` |
| SFX-WOLF-DOWN | seed 1 | seeds 2, 3 | trim, cut to 0.6 s, 10 ms fade-out, level match | `assets/audio/sfx/SFX-WOLF-DOWN.ogg` |
| SFX-HURT | seed 3 | seeds 1, 2 | trim, cut to 0.3 s, 10 ms fade-out, level match | `assets/audio/sfx/SFX-HURT.ogg` |
| SFX-FAIL | seed 2 | seeds 1, 3 | trim, cut to 1.0 s, 250 ms fade-out (sustained tone; stays shorter than the 1.2 s reload), level match | `assets/audio/sfx/SFX-FAIL.ogg` |
| SFX-CLEAR | seed 3 | seeds 1, 2 | trim, cut to 1.2 s, 10 ms fade-out, level match | `assets/audio/sfx/SFX-CLEAR.ogg` |
| SFX-HEAL | seed 3 (pre-pick) | — | not exported: heal is out of the slice (CHANGE-BRIEF Revision 2); pre-picked for the full game | — |

Common edits for every exported sound: onset = first 2 ms window above -45 dBFS with 5 ms kept before it, 2 ms fade-in so the cut cannot click, raised-cosine fade-out, levels matched on the loudest 50 ms window (short-window RMS) to one shared target of -15.75 dBFS with peaks at most -1 dBFS, OGG Vorbis q6 (FFmpeg libvorbis). Per-file numbers (onset, cut points, gain, peak, hashes): `assets/audio/EDIT-LOG.md`.

## Music (Google Gemini, Lyria)

- **Rejected first attempt: Suno.** 4 tracks were generated on the free plan. The two V6 Preview tracks were paid previews, and the free account had 0 downloads available, so no Suno track could be used without paying; the author switched to Google Gemini instead. Nothing from Suno is in the project. (CHANGE-BRIEF's "Generation tools" planned Suno; this is the change.)
- **Accepted: Google Gemini, Lyria.** Track `Beneath_the_Unlit_Stone.mp3` (MP3, 44.1 kHz stereo, 181.37 s, sha256 `6401e27055558127282bf15341158276146278e15ad0d0e9c0ee36a7d2248430`), kept outside the repo in `E:\7270\tools\music_raw\` and never committed. Google Gemini app, model shown in the app: Gemini 3.8 Flash; music generation in the app (Lyria); the Lyria version was not shown in the app.
- **Prompt** (drafted by Claude, sent by the author in the Gemini app, unchanged): "Create an instrumental music track for a 2D pixel-art game set in a dark underground cave. Dark fantasy exploration: low hollow percussion, sustained low strings, soft distant crystal chimes, tense and lonely, slow steady tempo, consistent rhythm all the way through so it can loop. No vocals."
- **SynthID:** audio generated by Lyria in the Gemini app carries Google's inaudible SynthID watermark; MUS-LOOP, cut from it, should be treated as carrying it too.
- **Loop:** 60.886 s to 115.510 s (12 bars at about 52.7 bpm), points suggested by Claude's waveform analysis in chat and confirmed by the author's listening: in a 3x repeat preview the seams at 0:54.6 and 1:49.2 sound clean, no click and no rhythmic hiccup. Edits (`tools/make_music_loop.py`): both points snapped to the nearest rising zero crossing (60.886485 s and 115.510363 s, shifts under 0.5 ms); the loop's last 50 ms crossfaded (equal-power) into the 50 ms just before the loop start; exported as OGG Vorbis q6 to `assets/audio/music/MUS-LOOP.ogg` (54.624 s), with looping enabled on import in Godot. No gain applied to the file; the engine's Music bus is set to -8 dB so the music sits under the sound effects (confirmed by the author in playtest 5: it sits well under the effects). Per-edit numbers: `assets/audio/MUSIC-EDIT-LOG.md`.

## Code-drawn and code-made (not generated by a model)

| Asset | Where | Why |
|---|---|---|
| ENV-EXIT: tall opening of pale daylight | `features/exit/exit.gd` | The optional generated exit was not made. Its brightest pixel (L* 89.0) stays below the hair (L* 91.7), so the hair remains the brightest shape (pillar 3). |
| UI-HEART: 7x6 px HP hearts | `ui/hud.gd` | Optional UI asset; drawn in code. |
| UI-CROSSHAIR: 9x9 px pale cross | `ui/crosshair.gd` | Optional UI asset; neutral colours so the fire stays the only warm thing on screen. |
| Dark fill in the pit | `game/main.tscn` (`PitDark`, #08090C) | Without it the cave background showed through the gap and the pit did not read as dark (storyboard P4). |
| HUD text, PAUSED and CLEARED screens | `ui/hud.gd` | Godot's built-in font (known limitation: smooth, not pixel). |
| White hit flash on the wolf | `features/wolf/flash.gdshader` | Engine effect. |
| Placeholder tones | `audio/placeholder_tones.gd` | Fallback only, used if an OGG is missing; none is used in the current slice. |

## Runtime

| Tool | Version | Source | License |
|---|---|---|---|
| PyTorch | 2.11.0+cu128 | https://pytorch.org · https://download.pytorch.org/whl/cu128 | BSD-3-Clause |
| torchvision | 0.26.0+cu128 | https://github.com/pytorch/vision | BSD-3-Clause |
| torchaudio | 2.11.0+cu128 | https://github.com/pytorch/audio | BSD-2-Clause |
| Python | 3.12.7 | https://www.python.org | PSF-2.0 |
| uv | 0.11.19 | https://github.com/astral-sh/uv | MIT or Apache-2.0 |
| Godot Engine | 4.7.2-stable | https://godotengine.org | MIT |
| Pillow | 12.3.0 | https://python-pillow.org | MIT-CMU |
| NumPy | 2.5.2 | https://numpy.org | BSD-3-Clause (with bundled 0BSD/MIT/Zlib parts) |
| SciPy | 1.18.1 | https://scipy.org | BSD-3-Clause |
| PyAV | 19.0.0 | https://github.com/PyAV-Org/PyAV | BSD-3-Clause |
| FFmpeg | 9.0.2 (gyan.dev full build, via WinGet) | https://ffmpeg.org | GPL-3.0 build (includes libvorbis, BSD-3-Clause) |

Project scripts: `tools/clean_sprites.py` (sprite cleanup, settings in `tools/sprites.json`, log in `assets/sprites/EDIT-LOG.md`), `tools/sheet_images.py` (silhouette and collision check images), `tools/gen_sfx.py` (sound generation, prompts in `tools/sfx_prompts.json`, log in `design/audio/sfx-gen-log.md`), `tools/trim_sfx.py` (SFX trim and export, log in `assets/audio/EDIT-LOG.md`) and `tools/make_music_loop.py` (music loop). All run with the ComfyUI venv; the two audio scripts also use FFmpeg.

Hardware: NVIDIA GeForce RTX 5060 Laptop GPU (8 GB), Windows 11.

## Notes

- **SynthID:** images made with Google Gemini carry an invisible SynthID watermark embedded in the pixels. Google designs it to survive common edits such as resizing and cropping, so the CHAR-REF images and their thumbnails should be treated as carrying it.
- **Stable Audio Open attribution:** the Community License (§IV.a) requires that anything distributed with or made from the model keeps the notice "This Stability AI Model is licensed under the Stability AI Community License, Copyright © Stability AI Ltd. All Rights Reserved" and shows "Powered by Stability AI". You own the generated outputs (§IV.c.iii). Commercial use is allowed only for revenue under US $1M and requires registering at https://stability.ai/community-license. This project is coursework (non-commercial).
- **CHAR-RUN-PASSING v1 is a screenshot:** `CHAR-RUN-PASSING-v1.png` (900×1024) is a screenshot of the accepted Gemini output; the original download was lost. Screenshot pixels, not the original file, so it may differ slightly in resolution and color from the other frames.
- **CHAR-RUN-PASSING v0 (rejected):** wide stride, gray ground band, and too similar to RUN-CONTACT for a 2-frame loop. Commit `2a90b0b` mistakenly added this image at full size as `CHAR-RUN-PASSING-v1.jpg`; it was removed in the next commit and replaced by the v0 thumbnail.
- **Run loop:** RUN-CONTACT v3 + RUN-PASSING v1, chosen after comparing loop previews. After the assignment was revised (no animation required), the slice shows RUN-CONTACT v3 for the run state; RUN-PASSING v1 stays on the sheet as the second key pose (CHARACTER-SHEET Revision 2).
- **CHAR-RUN-PASSING v1:** hat about 5% smaller than in the other frames, and less forward lean than RUN-CONTACT v3. During cleanup, scale by head height and re-check the run loop in the engine.
- Model weights and the ComfyUI install live in `E:\7270\tools\`, outside this repo, and are not committed.

## Original commit SHAs

Author and committer of the imported commits were rewritten to `zhefan-z <noreply>` for the course repo, to follow the fall-2026 rule "no IDs and no full names"; author and commit dates and file contents are unchanged. The originals are the permanent record in zhef-z/walker-magic-zhefan, frozen at `920d969`.

| Course-repo SHA | Original SHA (zhef-z/walker-magic-zhefan) | Author date | Commit |
|---|---|---|---|
| `7371b257cbca6b7e6b049153d7f3f00d1866153d` | `6697b805420ac46b925d17fd4dbc00330fae239f` | 2026-10-01T17:00:58-04:00 | Add concept, storyboard, character sheet and change brief before any generation |
| `26668d6661269f00a2297c2bf60b4b0e6a1c8b17` | `c4fabafbb31f2e1b475b77b84912d5aad0e6274b` | 2026-10-01T18:07:05-04:00 | Add CHAR-REF v1-v3, idle and run contact from Gemini, Revision 1, SOURCES draft |
| `24e8c629ceaeb35c539673c2f05741c2514025f6` | `2a90b0bafe44c3fd41c684d3845936dcea670278` | 2026-10-01T18:16:12-04:00 | Add CHAR-RUN-PASSING v1 from Gemini |
| `a40b5346b8441d436a1d530121ecd429fce51d7c` | `95b9bb85b7412649d8fb18f87a902c7aa5f3e42c` | 2026-10-01T18:33:03-04:00 | Add remaining accepted Gemini poses, fix passing frame (v1 screenshot, v0 rejected) |
| `7f195585fca2767d5362c1c3b9a0f9b6ef35d2df` | `a67239c4c44aadf1a008cc18af99f37058abe596` | 2026-10-03T03:14:11-04:00 | WIP checkpoint: sprite cleanup, SFX generation scripts, SOURCES and rejected thumbnails |
| `511fcbf19080690aed407b888e266ff047f38aec` | `920d96914fa34e3682cafa236fdaf5a04cb6c662` | 2026-10-06T15:43:40-04:00 | Add FRICTIONAL pointer to the course-repo log |
