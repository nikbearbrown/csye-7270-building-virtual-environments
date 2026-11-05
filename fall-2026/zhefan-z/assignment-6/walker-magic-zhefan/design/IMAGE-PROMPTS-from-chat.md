# Image prompts — drafted by Claude in claude.ai, sent by me in the Gemini app

> Collected on 2026-10-07 from my claude.ai chat. Each prompt below was drafted by Claude from my decisions.
> I must confirm each one was sent unchanged; where I edited or skipped a prompt, I mark it. Model shown in the app: Gemini 3.8 Flash.

## Chat 1 — character (CHAR-*)

### CHAR-REF v1
```
Pixel art character reference sheet for a 2D side-scrolling game. One original character shown four times at exactly the same height: front view, side view facing right, three-quarter view, back view. Solid flat bright green background (#00FF00), no shadows on the background, no text.

Character: a cute young fire mage girl with slender, girlish proportions (about 3.5 heads tall, NOT chibi). Long white twin tails reaching her waist, tied with small red bows. Large red eyes, light blush. Tall indigo witch hat whose tip bends backward, wide slightly drooping brim, red ribbon band with a small gold ember charm and a red ribbon tail hanging from the back. Short indigo capelet with a high collar, wide sleeves with gold cuffs, knee-length gray-brown belted tunic with gold hem trim, small belt pouches, dark stockings, short brown boots. She holds a dark wooden staff in her right hand, about shoulder height, topped with a diamond-shaped red crystal wrapped by a curled branch.

Clean pixel art, 1 px dark outline, limited palette: white #E8E6F0, red #D62839, indigo #3A40A0, gold #D4A63A, gray-brown #6B5A4E, skin #F5DCCD.
```

### CHAR-REF v2 (edit of v1)
```
Keep everything the same, but: she holds the staff in her RIGHT hand in every view, and make the staff shaft noticeably thicker and the eyes slightly larger so they read at small size.
```

### CHAR-REF v3 (edit of v2)
```
Edit only the staff position. Keep the character, pose, colors, proportions and background exactly the same.

The staff must be in her RIGHT hand in every view. Describe it by where it appears in the image:
- Front view (1st figure): the staff is on the LEFT side of the image.
- Side view facing right (2nd figure): the staff is held in the hand closest to the viewer, in front of her body.
- Three-quarter view (3rd figure): the staff is on the LEFT side of the image, held in the hand closest to the viewer.
- Back view (4th figure): the staff is on the RIGHT side of the image.

Keep the thicker staff shaft from the last version.
```

### Setup message (CHAR-REF v2 + 9 pose sketches uploaded, no generation)
```
I'm uploading 10 images for a game character project. Do not generate anything yet, just confirm you understand.

Image 1: my character reference sheet (the side view, 2nd figure, is the standard for everything).
Images 2–10: rough pose sketches, in this order: idle, run contact, run passing, rising, falling, cast, hurt, fail, victory. Use the sketches ONLY for body pose; ignore their faces, the eyepatch and their colors.

For every pose I ask for later: the exact character from image 1, side view facing right, face turned slightly toward the viewer, same proportions, outfit, colors, white twin tails with red bows, thick staff in the hand closest to the viewer. One full-body figure, centered, solid flat bright green background (#00FF00), no text, no ground shadow.
```

### CHAR-IDLE v1
```
One correction: the tunic is mid-thigh length, exactly as in the reference sheet, not knee-length. Match the reference sheet whenever the text and the image disagree.

Now draw the idle pose (sketch #02 Idle).
```

### CHAR-RUN v1 (rejected)
```
Now draw run contact and run passing side by side, both figures exactly the same size.
```
(An earlier draft of this prompt said: "...Both figures exactly the same size and on the same ground line, same face angle as the idle you just drew." — mark which one was sent.)

### CHAR-RUN v2 (rejected; the model edited the reference sheet)
```
Not quite. Please redraw both running frames with these fixes:
- Hold the staff the same way in both frames: one hand only (the hand closest to the viewer), staff tilted slightly forward, not across the body. The whole staff must stay inside the image with a margin around it.
- Run passing (right figure): the supporting foot is flat on the ground, directly under the body; only the other leg is lifted. Both figures' feet touch the same ground level.
- Twin tails the same length as the reference, red bows visible in both frames.
- No ground line, no shadow. Leave empty green space around both figures.
```

### CHAR-RUN-CONTACT v3 (idle uploaded as base)
```
Do not edit the reference sheet. Use THIS image (the idle sprite I just uploaded) as the base and create a new image with exactly ONE figure.

Change only the legs and arms into a running pose, run contact (sketch #03): front leg reaching forward with the heel touching the ground, back leg pushing off behind, body leaning slightly forward. She holds the staff in one hand only (the hand closest to the viewer), tilted slightly forward, the whole staff inside the image.

Keep everything else identical to the uploaded idle sprite: size, head, hat, hair, outfit, colors, face angle. Same solid green background, no ground line, no shadow.
```

### CHAR-RUN-PASSING v1
```
Again use the idle sprite as the base and create a new image with exactly ONE figure: run passing (sketch #04). The supporting leg is straight under the body with the foot flat on the ground; the other leg passes under the body with the knee bent and the foot lifted behind. Body leaning slightly forward, twin tails flowing back like in the run contact frame you just drew, staff held the same way as in that frame. Keep size, head, hat, outfit, colors and face angle identical. Same green background, no ground line, no shadow.
```

### CHAR-RISE v1
```
Again use the idle sprite as the base and create a new image with exactly ONE figure: rising (sketch #05). She is jumping upward: knees tucked up, staff raised a little in the hand closest to the viewer, twin tails hanging down below her because she is moving up. Keep size, head, hat, outfit, colors and face angle identical. Same green background, no ground line, no shadow.
```

### CHAR-FALL v1
```
Again use the idle sprite as the base and create a new image with exactly ONE figure: falling (sketch #06). She is coming down after a jump: legs extended downward and slightly apart, ready to land, the arm without the staff stretched out for balance, twin tails and the hat ribbon flowing UPWARD above her shoulders because she is falling. Keep size, head, hat, outfit, colors and face angle identical. Same green background, no ground line, no shadow.
```

### CHAR-CAST v1 (rejected)
```
Again use the idle sprite as the base and create a new image with exactly ONE figure: cast (sketch #07). She thrusts the staff forward, held almost horizontally at shoulder height in the hand closest to the viewer, the red crystal pointing forward with a small bright glow around it. Wide stance, body leaning slightly into the cast, twin tails swinging back. Do NOT draw a fireball or any projectile, only the glow on the crystal. The whole staff must stay inside the image. Keep size, head, hat, outfit, colors and face angle identical. Same green background, no ground line, no shadow.
```

### CHAR-CAST v2 (rejected; design changed to a raised staff)
```
Change of plan for the cast pose. Use the idle sprite as the base and create a new image with exactly ONE figure: she raises the staff up diagonally in front of her, so the red crystal is held above and slightly in front of her head, glowing brightly. The other hand is open, palm out, near her chest. Focused expression, feet slightly apart, body a little tense. The staff head looks exactly like the reference (same curled branch, same diamond crystal). Do NOT draw a fireball. The whole staff stays inside the image. Keep size, head, hat, outfit, colors and face angle identical. Same green background, no ground line, no shadow.
```

### CHAR-CAST v3 (accepted)
```
The staff is not raised enough. Redraw the cast pose:
- She raises the staff high with BOTH hands, arms stretched up and forward, so her hands and the staff are in front of the hat brim, never overlapping the hat.
- The staff stands upright in front of her face, and the red crystal is held higher than the tip of her hat.
- Her upper body leans back slightly, the hat tilting back a little with it.
- The crystal glows with a small RED-ORANGE light, not yellow or green.
- The staff head looks exactly like the reference (same curled branch, same diamond crystal). No fireball.
Keep size, hair, outfit, colors and face angle identical. Same green background, no ground line, no shadow.
```

### CHAR-CAST v4 (rejected; returned identical to v3)
```
Closer, but the staff still points forward. Redraw the cast pose:
- She holds the staff perfectly VERTICAL, raised straight up above her head with both hands, like lifting a lantern. The staff is not tilted forward or backward at all.
- The red crystal is directly above the tip of her hat.
- Her hands are on the shaft above her head, clear of the hat brim.
- The crystal glows RED-ORANGE only. No yellow or green glow anywhere.
- No fireball. Same staff head as the reference.
Keep size, hair, outfit, colors and face angle identical. Same green background, no ground line, no shadow.
```

### CHAR-WIN v1
```
Use the idle sprite as the base and create a new image with exactly ONE figure: victory pose. She stands on the ground, relaxed and proud: the staff rests diagonally on her shoulder, held near its lower end by the hand closest to the viewer. Her other hand makes a V sign (peace sign) raised beside her face, palm facing the viewer so both fingers are clearly visible. Big happy smile, eyes slightly closed. The whole staff stays inside the image. Do NOT draw sparkles or effects. Keep size, hat, outfit, colors and face angle identical. Same green background, no ground line, no shadow.
```

### CHAR-HURT v1
```
Use the idle sprite as the base and create a new image with exactly ONE figure: hurt (sketch #08). She is knocked back by a hit from the front: upper body bent backward, head tilted back, eyes squeezed shut, one foot lifted off the ground, the staff tilting backward in her hand, twin tails swinging forward. Do NOT draw impact lines or effects. Keep size, hat, outfit, colors and face angle identical. Same green background, no ground line, no shadow.
```

### CHAR-FAIL v1
```
Use the idle sprite as the base and create a new image with exactly ONE figure: fail (sketch #09). She has collapsed: kneeling on both knees, upper body slumped forward, head down, eyes closed, sad. The staff has fallen out of her hand and lies flat on the ground in front of her. Her hat has slipped down over her eyes a little. Keep size, hat, outfit and colors identical. Same green background, no ground line, no shadow.
```

## Environment (same chat as the character, CHAR-IDLE-v1 uploaded as a style reference)

### ENV-BG v1 (accepted; v2 was a variant the app produced with cave paintings)
```
Using the same pixel art style as this character, draw a wide 16:9 background for a 2D side-scrolling game: the inside of a dark underground cave. Damp limestone walls, stalactites hanging from the ceiling, faint distant rock layers, cold desaturated slate blue and gray-brown tones, mostly in deep shadow. Low contrast and darker than the character so she stays the brightest thing on screen. No characters, no floor in the foreground, no text, no light sources.
```

### ENV-TILES v1 (rejected)
```
Same pixel art style. Draw a horizontal strip of cave ground tiles for a 2D platformer, side view: the top surface is a walkable rocky ledge with a lighter edge highlight, the body below is darker rock. The strip must tile seamlessly left-to-right. Also draw, separately on the right, a left edge piece and a right edge piece that end the ground cleanly where a pit begins, with a clear lighter rim so the edge is easy to see. Slate gray and gray-brown, a little lighter than the background. Solid flat bright green background (#00FF00), no text.
```

### ENV-TILES v2 (accepted, cropped)
```
Redraw the ground tiles with these fixes:
- NO cave paintings, drawings or symbols anywhere. Plain rock texture only.
- The main strip must tile seamlessly: its left edge and right edge must match exactly, with the same rock pattern and the same brightness, so it can repeat without a visible seam.
- Keep the walkable top ledge with the lighter rim, and keep the two separate edge pieces on the right.
- Uniform dark slate rock below the ledge, no bright patches.
Same solid flat bright green background (#00FF00).
```

## Wolf, round 1 (same long chat; abandoned because of context bleed)

### WOLF-R1 run
```
Same pixel art style. Draw one cave wolf for a 2D side-scrolling game, side view facing right, running. Lean body, cool gray-blue fur, glowing cyan eyes, clearly an enemy but not gory. Its shoulder reaches about the character's waist height. One figure only, solid flat bright green background (#00FF00), no text, no ground, no shadow.
```

### WOLF-R1 lunge
```
Use this wolf as the base and create a new image with ONE figure: the same wolf lunging forward to attack, body stretched out low, front legs reaching forward, mouth open showing teeth, ears back. Keep size, colors, the cyan eyes and the style identical. Same green background, no ground, no shadow.
```

### WOLF-R1 down
```
Use the first wolf (the running one) as the base and create a new image with ONE figure: the same wolf defeated, lying on its side on the ground, legs limp, eyes closed. Not bloody, no wounds. Keep size, colors and pixel art style identical. Solid flat bright green background (#00FF00), no ground, no shadow.
```

## Chat 2 — wolf, round 2 (new chat, text only, nothing uploaded)

### ENEMY-WOLF-RUN v2 (accepted)
```
Pixel art sprite for a 2D side-scrolling game: a cave wolf enemy, side view facing right, running at full speed. Lean body, cool gray-blue fur with lighter gray highlights, glowing cyan eyes, pointed ears, bushy tail. Clean anime-style pixel art with a 1 px dark navy outline, flat cel shading with one shadow and one highlight tone, limited palette. Clearly an enemy, but not gory. One figure only, centered with empty space around it, solid flat bright green background (#00FF00), no text, no ground, no shadow, no other characters.
```

### ENEMY-WOLF-LUNGE v2 (accepted)
```
Use the wolf you just drew as the base and create a new image with ONE figure: the same wolf lunging forward to attack, body stretched out long and low, front legs reaching far forward, back legs extended behind, mouth open showing teeth, ears flat back. Keep size, colors, cyan eyes, outline and style identical. Same green background, no ground, no shadow, no other characters.
```

### ENEMY-WOLF-DOWN v2 (rejected; legs unchanged)
```
Do NOT reuse the running or lunging pose. Draw the same wolf (same fur colors, cyan eyes, outline, size and style) defeated: lying flat on its side on the ground, its back at the top and belly toward the viewer, all four legs limp and stretched out sideways, head resting down, eyes closed. Not bloody, no wounds. One figure only, same solid flat bright green background (#00FF00), no ground, no shadow, no other characters.
```

### ENEMY-WOLF-DOWN v3 (accepted, partial)
```
Pixel art sprite for a 2D side-scrolling game: a defeated cave wolf collapsed on the ground, side view, head toward the right. Its belly is pressed flat against the ground, all four legs splayed out flat and limp, chin resting on the ground, ears drooping, eyes closed, tail lying flat behind it. The whole body is low and horizontal, much lower than a standing wolf. Lean wolf with cool gray-blue fur and lighter gray highlights, spiky fur on the back. Clean pixel art with a dark navy outline, flat cel shading with one shadow and one highlight tone. Not bloody, no wounds. One figure only, centered, solid flat bright green background (#00FF00), no text, no ground line, no shadow, no other characters.
```
(Check: was this sent in a new chat, or in the same wolf chat? The result kept the lunge pose, which suggests the same chat.)

## Chat 3 — FX (new chat)

### FX-FIREBALL-BURST v1 (accepted)
```
Pixel art sprite sheet for a 2D side-scrolling game, two separate small images side by side: on the left, a fireball projectile flying to the right, a round bright yellow-white core inside orange flames with a short flame trail behind it; on the right, a small fire burst explosion for when it hits, orange and red flames spreading out from the center. Clean pixel art with a dark outline, warm colors only: no green, no yellow-green. Solid flat bright green background (#00FF00), no text, no other objects.
```
