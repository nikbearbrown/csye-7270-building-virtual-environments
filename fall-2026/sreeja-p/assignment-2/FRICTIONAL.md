# FRICTIONAL — Assignment 2

## Entries

<!-- One entry per work session, newest last. Copy the block below. -->

### YYYY-MM-DD — <what I was working on>

- **Date and what I was working on:**
- **I tried / expected:**
- **What happened:**
- **What I did:**
- **What Claude or another person contributed:**
- **What I understand now / still do not understand:**
- **Evidence and next step:**

### 2026-10-01 — choosing the game and writing the design docs before generating

- **Date and what I was working on:** 2026-10-01. I chose this semester's game and wrote the design docs before generating anything.
- **I tried / expected:** I started from my Assignment 1 firefighter game, expecting to swap the firefighter for generated art and add sound and music.
- **What happened:**
  - Claude checked the A1 code. The firefighter is drawn entirely in code (`player.gd`, `_draw()`), and the game has no audio, so all three generated categories (art, sound, music) are new work.
  - I could not push to the class repo directly (no write access), so I forked it.
- **What I did:**
  - Decided the concept: a ninja firefighter named **Extinguisho**, with a yellow helmet, a mostly red heat suit, and ninja touches.
  - Decided his movement and face: kung-fu-style jump and landing poses, and a deadpan, grumpy face that turns comic-book devastated when fire touches him.
  - Decided the sound: exaggerated, funny sound effects and urgent music, because he has limited time to save the victims.
  - Picked the tools: Gemini and ChatGPT for images, Suno for music, Audacity for editing.
  - Picked the name from Claude's list and reviewed the drafts.
- **What Claude or another person contributed:** Claude Code:
  - read the A1 code;
  - drafted CONCEPT, CHARACTER-SHEET, CHANGE-BRIEF, and SOURCES from my notes and the game code;
  - suggested name options;
  - flagged two risks: the red suit and yellow helmet against the fire colors, and face readability at about 32 px;
  - set up the fork and copied the A1 game at commit `b2f7945`.
- **What I understand now / still do not understand:**
  - Claude cannot produce art that counts as generated.
  - Audacity edits audio but does not generate it.
  - The class repo ignores WAV files, so game audio will be OGG.
  - Still open: the final look (three candidates in the character sheet), the palette, the storyboard pictures, and whether the kung-fu stance plays in-game.
- **Evidence and next step:** this push's commits. Next: STORYBOARD.md, committed with the other docs before the first generation.

### 2026-10-02 — storyboard sketches in ChatGPT

- **Date and what I was working on:** 2026-10-02. Generating the six storyboard panel sketches.
- **I tried / expected:** one rough pencil sketch per panel from ChatGPT (Plus, Instant mode), using a base style prompt and then one prompt per panel. I expected each image to match its panel's shot, angle, and action.
- **What happened:**
  - **Panel 1** matched except the character's size (large in the foreground, not "small at the far left").
  - **Panel 3, attempt 1:** he carried the person in his arms. That contradicts my game, where a rescued survivor rides as a head in the bag on his back. My prompt never mentioned the bag.
  - **Rescue strip:** when I pasted the three rescue prompts in one message, ChatGPT returned one wide strip of three square frames, not three 16:9 images.
  - **Panel 6:** the bag holds two people and a dog instead of one person and one dog.
  - **Order:** I generated panel 1 before the storyboard text was committed. The text was written 2026-10-01; the image was saved at 10:20 and the storyboard committed at 10:22 on 2026-10-02. Panels 2–6 came after the commit.
- **What I did:**
  - Rejected the arms-carry rescue because it doesn't match the game.
  - Decided the rescue is funnier if he doesn't care: he grabs the survivor and recklessly tosses them into his bag.
  - Then split the rescue into three beats with different faces: 3a grab (serious), 3b throw (couldn't care less, yawning), 3c in the bag (serious again).
  - Moved the person inside the window for 3a.
  - Kept the strip only as a reference and regenerated each beat as its own 16:9 image, one message each.
  - Accepted panel 6 with the bag mismatch noted.
- **What Claude or another person contributed:** Claude Code:
  - wrote the base and panel prompts and the revised prompts from my changes;
  - pointed out from the code that rescue uses the bag;
  - flagged the strip's frame shape and the panel 6 mismatch;
  - resized and filed the images;
  - recorded the prompts and the asset log.
  
  ChatGPT generated every sketch. The rescue redesign and every accept or reject decision were mine.
- **What I understand now / still do not understand:**
  - One message gives one image, so each frame needs its own message saying "single 16:9 image."
  - A prompt has to describe the game's actual mechanic, or the model fills in a default.
  - Still open: the three rescue beats could become the three frames of the in-game rescue animation (pose 9), which the character sheet needs to reflect.
  - **Still open: the ninja-ness doesn't come through strongly enough.** Looking at the six panels together, he reads mostly as a regular firefighter. The ninja signals are only the face wrap, the headband tails, the stance in panel 2, and the kick in panel 6; the rest is standard firefighter gear. My concept depends on "every move is a kata", so the ninja side has to be pushed harder when I design the character's look. I have not decided how yet.
- **Evidence and next step:**
  - Prompts are verbatim in STORYBOARD.md, "Revision 2026-10-02"; asset log rows SB-01 … SB-06 are in SOURCES.md; rejected thumbnails are in `walker-ninja-firefighter-joe/rejected/`.
  - Next: generate the character's three candidate looks and pick one.

### 2026-10-02 — character look exploration

- **Date and what I was working on:** 2026-10-02. Exploring Extinguisho's look in ChatGPT (Plus, Instant mode), in a new chat separate from the storyboard.
- **I tried / expected:** to push the ninja side harder by combining ancient ninja / kung-fu style with firefighter gear. I expected a few clear options to choose from.
- **What happened:**
  - **CHAR-EXPLORE-01:** a concept sheet with four looks (A Shinobi Smoke-Eater, B Shaolin Fire Monk, C Samurai Fireguard, D Kung-fu Master in Turnout), each with poses.
  - **CHAR-EXPLORE-02:** three builds of A (lean, heavy, balanced). They still looked cartoonish, on a gray background.
  - **CHAR-EXPLORE-03:** three realism levels with soot and ash. They came back crusty and battle-worn on cream, and the red suit and yellow helmet still read under the grime. He was posed in a three-quarter turn instead of the side view I asked for.
- **What I did:**
  - Chose look A, then A3's balanced athletic build.
  - Asked for him to be more muscular and strong, more realistic instead of comic-book, crusty and ashy, with his deadpan, grumpy mood in the prompt, on a white/cream background.
  - Picked three poses I liked from the four-look sheet: A's dashing lunge, B's low palm-forward stance, and D's wide pushing stance.
- **What Claude or another person contributed:** Claude Code:
  - suggested the four look options and the pose options;
  - wrote the prompts from my choices;
  - warned that realistic detail may not read at the sprite's ~32 px size and that it departs from the comic-book art direction in CONCEPT.md;
  - recorded the iterations.
  
  ChatGPT generated the images. Choosing A, A3, the realistic and crusty direction, and the poses were my decisions.
- **What I understand now / still do not understand:**
  - Asking for several variations side by side makes it easier to judge one change at a time (build, then realism).
  - Still open: which realism level (R1–R3) to use; whether realistic detail survives at game size; and the CHAR-EXPLORE-01 prompt still needs to be copied into the log.
- **Evidence and next step:**
  - Prompts are in CHARACTER-SHEET.md, "Revision 2026-10-02"; asset log rows CHAR-EXPLORE-01 … 03 are in SOURCES.md; thumbnails are in `design/character/explore/`.
  - Next: pick R1, R2, or R3, then test it at game size.
- **Update, same session:**
  - The R2 and R3 body, ash, and hand skin looked realistic, but all three faces still looked cartoonish. I asked for R2 and R3 combined with a fully realistic face (CHAR-EXPLORE-04). It came back realistic, with a stern face.
  - Claude then shrank it to the real 32 px game size. The silhouette and headband still read, but the soot turns the red suit muddy and the yellow helmet into a few dull pixels, and the face is not visible at all (`design/character/size-test/`).
  - So the realistic version works as the master reference and for close-ups. How to make the in-game sprite frames is still my decision to make.
- **Update, later the same day:**
  - **Turnaround (CHAR-REF-01):** generated from the realistic image, with front, side, three-quarter, and back views and a height bar. The "side" view was nearly three-quarter.
  - **True side profile (CHAR-REF-02):** asked for separately, because every in-game pose is seen from the side. It came back as a real profile and is now the reference image I attach to every pose prompt.
  - **Expression sheet (CHAR-EXPR-01):** grumpy, bored, serious, devastated. Grumpy and serious looked almost the same, bored had no yawn, and devastated was too subtle.
  - **My decision:** add both hands on his head for devastated. Claude pointed out this also matters in the game, because at 32 px only body language shows, so the burned pose gets the same gesture.
  - Asked for a revised sheet (CHAR-EXPR-02). The pose prompts are written and logged in CHARACTER-SHEET.md; poses are next.
  - **CHAR-EXPR-02 result:** bored now yawns behind his hand, and devastated clutches his smoking helmet with both hands, both as I wanted. But grumpy still doesn't look grumpy; it looks sleepy.
  - I'm letting it be for now and will revisit, because grumpy is his default face in most poses. Claude suggested asking for an active glare with a hard brow instead of droopy eyelids; that prompt tweak is logged in CHARACTER-SHEET.md.
- **Update, sprite approach (provisional):**
  - **The question:** the realistic look is muddy at game size. Should I (A) shrink it as it is, or (B) first make one brighter, cleaner, game-readable version of the same character and make every pose from it?
  - **Honestly:** I didn't yet understand what sprite frames are or how A or B would look in play. I chose B because Claude recommended it, as a test, not out of my own taste yet. If it doesn't read in the game, I'll switch to A or explore other options. I want to come back and review this decision.
  - Sent the B prompt (CHAR-REF-03, verbatim in CHARACTER-SHEET.md, "Sprite approach"). Claude wrote it; ChatGPT generated the image; the result isn't checked yet.
  - Also downloaded both expression sheets: v1 kept as a reject thumbnail, v2 as `design/character/expressions.png`.
- **Update, CHAR-REF-03 result and character size:**
  - **Got:** the same character, with brighter red and yellow, lighter soot, and a clean outline.
  - **First test, 32 px:** B's helmet and suit kept their colors better than A's, but **neither one looked like my character to me.** That made me ask whether the in-game character is supposed to look like the generated images. Claude checked the assignment: yes, the in-game appearance must be the generated art and meet the character sheet. The art is fine; the character is just too small.
  - **Claude's correction:** the 32 px test was harsher than the real game, which shows him at about 64 px. Claude mocked up the real 1280×720 window at 64 px and at 128 px.
  - **Decided:**
    - He needs to be **bigger** in the game. I'll pick the exact size when we put him in the game and I can see it.
    - **B**, because it's brighter and better, and at the bigger size it stands out from the flames more than A.
  - **Human / Claude / model:** ChatGPT generated CHAR-REF-03; Claude wrote the prompt and made the size mock-ups; noticing the mismatch, choosing B, and making him bigger were my decisions.
  - **Still unresolved:** the exact size, and how much the level (platforms, jumps, fire) has to change to fit a bigger character.

### 2026-10-05 — pose 1 (idle)

- **Date and what I was working on:** generated pose 1 on Saturday 2026-10-03; downloaded and checked it with Claude on 2026-10-05.
- **I tried / expected:** the CHAR-IDLE prompt from CHARACTER-SHEET.md (verbatim there), sent in ChatGPT with `side-profile-game.png` attached. I expected his low kung-fu ready stance in a true side profile, the same character as the reference.
- **What happened:**
  - The gear, colors, and grumpy face all match the reference, and the stance reads strongly as kung fu.
  - But his chest and hips turn toward the camera (about three-quarter), even though the prompt said "TRUE SIDE PROFILE… chest not turned toward the camera." That's predicted failure F1, and the same drift as the turnaround's side view.
- **What I did:** not decided yet: accept with the note, or regenerate with a stronger side-view instruction.
- **Also, the assignment changed:** it now says animation is not required; each state can be one static image that the game swaps in. My 12 single-pose plan already fits this.
- **What Claude or another person contributed:** Claude wrote the pose prompt from my pose picks, checked the result against the reference, and pointed out the three-quarter drift. ChatGPT generated the image. The pose choice was mine; the accept/regenerate decision is mine to make.
- **What I understand now / still do not understand:** writing "true side profile" in the prompt doesn't guarantee it; the model drifts toward three-quarter for dynamic poses. Still open: whether three-quarter is acceptable in my side-view game.
- **Evidence and next step:** CHARACTER-SHEET.md, "CHAR-IDLE — pose 1"; asset log row CHAR-IDLE in SOURCES.md. Next: decide on pose 1, then pose 2 (run).
- **Update, decision on pose 1:**
  - I realized we already had a standing pose that is a true side profile: `side-profile-game.png`. That becomes **idle**. Claude added that its narrow shape fits the collision box, which matters for the pose on screen most.
  - I kept pose 1 anyway, as **respawn / ready** (CHAR-RESPAWN, storyboard panel 5): he snaps back into his stance after a retry.
  - I'm still generating the other planned poses (2–12).
  - The CHARACTER-SHEET entry heading was renamed to "Pose 1, sent as CHAR-IDLE, now CHAR-RESPAWN"; the original "what I wanted" text is kept as written.
- **Update, pose 2 (run):**
  - **Tried:** because pose 1 drifted to three-quarter, Claude suggested one more header sentence: "His body is turned fully sideways… only one eye is visible."
  - **My mistake:** I sent only the header and forgot the "Pose:" line. It came back as a calm walk. At first Claude and I judged it as "a walk, not the dash we asked for"; my screenshot of the chat then showed the dash was never asked for.
  - **What it did show:** the new sentence works. It's a true side profile.
  - **Decided:** replace it with a real run. I attached the walk image itself and asked ChatGPT to edit only the pose, to keep the side view. It came back as a low ninja dash in true side view, and I accepted it.
  - **Human / Claude / model:** Claude wrote the header sentence and the edit prompt; ChatGPT generated both images; noticing that the walk wasn't what I wanted, and replacing it, were my decisions.
  - **What I understand now:** editing an existing good image keeps its view better than starting again from the reference. Still unresolved: the wide run pose sticks out far past the collision box.
- **Update, poses 3 and 4:**
  - Attached `side-profile-game.png` for both, with the revised header.
  - **Pose 3 (crane stance, jump crouch):** usable on the first try. Judged against the reference: same gear and colors, side view with only a very slight chest turn. Accepted.
  - **Pose 4 (flying kick, rising):** the kick itself reads well, but it drifted back to **three-quarter**, with the chest facing the camera, and the body stayed upright instead of horizontal. So the "fully sideways" sentence helps for standing poses but not reliably for big action poses. Decision pending.
  - **Pose 4b:** I attached the drifted image and asked ChatGPT to change only the camera angle (Claude wrote the edit prompt). It came back mostly side-on: the tank and axe are back on his left side, with only a little chest showing from his spread arms. I accepted 4b; the first try is a reject thumbnail. This is the second time editing an image fixed the view where a new prompt didn't.
  - **Pose 5 (falling):** usable on the first try: cross-legged, arms folded, calm, true side profile. Accepted. It carries *Too cool to care* well; he's falling and couldn't care less.
  - **Pose 6 (landing):** the pose and side view were right, but the dust puff from my own planned prompt came back as a cream-brown cloud that would leave a messy edge when the background is removed. I asked for an edit removing the dust (6b) and accepted it.
  - **Pose 7 (hose), planned change:** Claude checked the game code: the game already draws the water stream itself (`session.gd`). So I agreed to drop "water blasting out" from the prompt; the pose shows him holding the nozzle with no water.
  - **Pose 7 result:** the stance and side view were right, but **I noticed the hose ran off the left edge of the image.** Cut out for the game, it would end in mid-air behind him. I asked for the hose to stay in frame and connect to his tank. Claude wrote that edit prompt; the result (7b) has the hose looping from the nozzle to the bottom of the tank, and I accepted it.
  - **Pose 8 (rescue grab):** Claude pointed out that the game draws the survivors (a person and a dog), so I agreed to leave the person out of the image. It came back in true side view, but the hand is a fist, so it reads more like a punch, and an extra thigh pouch appeared. Claude suggested an edit; **I accepted it as is.**
- **Update, design change: the toss goes up.**
  - **What happened:** pose 9 (toss) came back as asked: a sideways toss over the shoulder, mid-yawn, true side view.
  - **What I decided:** looking at it, I changed the design. The toss should be **exaggerated and go upward**: he launches the survivor sky-high without looking, and they fall into the bag. It's funnier and pushes *Too cool to care*.
  - **What Claude did:** wrote the edit prompt (9b) from my idea, and pointed out that the image can only show his throw. The survivor's flight up and drop into the bag has to be drawn by the game, which is a small, optional code addition for the build.
  - **Docs updated** as dated revisions, with the originals kept: STORYBOARD.md (panel 3b's sketch still shows the old sideways toss) and CHANGE-BRIEF.md.
  - **Still unresolved:** whether there's time to code the survivor's upward arc. Without it, the survivor simply appears in the bag, as in A1.
  - **9b result:** arm flung up overhead, yawn kept, extra pouch gone, true side view. Accepted.
  - **Pose 10 skipped (my decision):** "walking away with a dazed person in the bag" can't be one image. His art has no bag, and a baked-in person would be wrong for the dog. The set still has 12 poses plus the turnaround.
- **Update, pose 11 (burned):**
  - **Before sending:** Claude suggested two prompt changes, which I agreed to: heavy soot instead of "scorched black head to toe" (so he's still recognizable), and thin dark smoke instead of a cloud (so the background removal stays clean).
  - **Result:** the hands-on-helmet horror came back in side view, but the smoke touched the top edge.
  - **Front view?** I asked whether the burned pose was supposed to be front-facing. Claude checked: only the storyboard close-up and the expression portrait face the camera; the in-game pose was always side view. I kept side view.
  - **Edit attempt:** shorten the smoke. Both versions ChatGPT offered fixed the smoke but turned him three-quarter. I rejected them.
  - **Hand edit instead:** Claude faded the top rows of try 1 into the background with a short script, so the smoke fades out. Side view kept; logged as an edit.
  - **What I understand now:** an edit can fix one thing and break another (the view), so every edit has to be rechecked against the reference.


### 2026-10-06 — pose 12 (celebrate)

- **Date and what I was working on:** 2026-10-06. Finishing the last pose, then putting Extinguisho into the game for the first time.
- **I tried / expected:** pose 12 as a deadpan kung-fu bow for the end of the level (panel 6).
- **What happened:**
  - **Try 1** (2026-10-05) came back as an upright salute with palms together: no bow, nearly the same shape as idle.
  - I asked twice in the same chat to edit it into a bow. Both times ChatGPT returned an error and no image. The chat had become very long.
  - **Try 2:** I started a **new chat**, attached `side-profile-game.png`, and sent Claude's prompt with the bow written into the pose line. It came back as a clear forward bow, side view, matching gear.
- **What I did:** rejected try 1 (thumbnail kept), accepted 12b. Its palms are together rather than fist-in-palm, which I judged minor because it still reads as a bow and differs from idle at game size.
- **What Claude or another person contributed:** Claude wrote the 12b prompt and checked the result against the reference. ChatGPT generated both images. Rejecting try 1, starting a new chat, and accepting 12b were my decisions.
- **What I understand now / still do not understand:** a very long chat can stop working; a new chat with the reference attached and the full prompt worked on the first try.
- **Evidence and next step:** CHARACTER-SHEET.md, "Pose 12"; SOURCES rows CHAR-BOW. Next: play the game with the new character and judge size, box, and colors.


### 2026-10-06 — Extinguisho in the game: step 1 and playtest 1

- **Date and what I was working on:** 2026-10-06. First time the generated character is in the game.
- **I tried / expected:** Claude's step 1: one generated image per movement state (idle, run, jump crouch, rising, falling, landing), 64 px tall in the game, collision box 20×40. I expected to judge his size, the box, and his colors.
- **Decisions before the build (mine):**
  - **Collision box A (20×40)** instead of a 58 px tall box. Claude's overlay showed the crouching poses are only 41–49 px tall, so a tall box would kill him by flames that never visibly touch him; with A his helmet can stick out above the box, which only forgives.
  - Size 64 px and the palette: accepted for now, to judge in the game.
  - Hide the empty rescue bag until the first rescue (Claude suggested; I agreed).
- **What happened (my playtest):** the run and the flying kick look fine. But: the intro text was hidden behind him; nothing happened to him when the fire got him; the jump flashed too many poses (crane, kick, meditating fall) in a short time; hosing looked like he was peeing on the fire; the bag sat near his knees; and there was no grab, toss, or fall into the bag. Details and causes are in TEST-REPORT.md, "Playtest 1".
- **What I decided:** the jump should be the kick and then the landing pose. Claude proposed keeping the meditating fall only for walking off a ledge, so it is still used; I agreed. Everything else goes into step 2.
- **What Claude or another person contributed:** Claude wrote the code (`player.gd`, one line in `session.gd`), the background-removal script (`tools/make_sprites.py`), ran the tests (41/41 pass), and explained each cause. The playtest observations are mine.
- **What I understand now / still do not understand:** passing tests didn't show any of these problems; only playing did. Still open: whether 64 px is the right size.
- **Evidence and next step:** TEST-REPORT.md, "Playtest 1". Next: step 2 (action poses, rescue toss, hose nozzle, bag position).


### 2026-10-06 — step 2, playtest 2 (slower), and the background

- **I tried / expected:** step 2 fixed everything from playtest 1. Playing it, the toss was nice and funny, but the movement and pose changes felt like too much, and I still didn't see the burned pose or the landing.
- **What happened:** Claude checked: burned did show, but only 0.55 s, and it is dark and subtle at game size (predicted failure F3); the landing showed only 0.13 s. When I asked to slow him down (run speed 160 → 120), the tests showed the burning-street jump became impossible.
- **What I decided:** option A from Claude's tested options: speed 120 with a floatier jump (64 px, 0.8 s in the air), which kept the level beatable. Landing and burned hold longer. For ENV-BG I accepted the image, and asked that the other game elements stay visible on it; Claude recolored the ledges and level text.
- **What Claude or another person contributed:** Claude wrote the code and test changes, tested speed/gravity options, and found the hidden bow (the end card covered it) in a screenshot. ChatGPT generated ENV-BG. The slowdown, option A, and accepting ENV-BG were my decisions.
- **What I understand now / still do not understand:** slowing the run changes the level too, because jump distance depends on speed; the tests caught it before I played. Still open: whether burned reads well enough on the dark background, and the exact ENV-BG prompt for the log.
- **Evidence and next step:** TEST-REPORT.md, step 2, Playtest 2, ENV-BG; SOURCES row ENV-BG. Next: playtest 3, then sounds and mute.


### 2026-10-07 — finishing the character sheet

- **Date and what I was working on:** 2026-10-07. The required character-sheet parts that were still missing: silhouette at game size, collision overlay, palette hex values, consistency check.
- **What happened:** Claude made them from the exact in-game images with a script (`tools/make_sheet_extras.py`), so they show what the game draws. The silhouette was first drawn on the dark backdrop, where black shapes were hard to judge, so it moved to a plain light background (the test is about shape). I looked at all three images before committing.
- **What they showed:** every state has its own shape at 64 px; the upright poses (idle, burned, toss, bow) differ only by arms and head. The 20×40 box sits on the torso and legs in every pose. The palette check confirmed predicted failure F2: next to the fire the red suit and yellow helmet nearly vanish and the dark outline carries him; on the dark backdrop the yellow and red carry him. No recolor needed.
- **What Claude or another person contributed:** Claude wrote the script, measured the contrast ratios, and wrote the sheet section from my earlier decisions (option A box, 64 px size, palette option A). I reviewed the images and the text and approved them.
- **Still unresolved:** the 64 px size is "to confirm" in my next playtest.
- **Evidence:** CHARACTER-SHEET.md, "Revision 2026-10-07"; `design/character/silhouette.png`, `collision.png`, `palette.png`; `evidence/screens-web/`.

---

## GitHub pushes

| Date | Commit note |
|---|---|
| 2026-10-01 | Add concept, character sheet, change brief, and sources before generation |
| 2026-10-02 | Add storyboard text: six panels, shots, angles, and motion |
| 2026-10-02 | Add storyboard sketches, prompt log, and rejected thumbnails |
| 2026-10-05 | Add character reference, poses 1-9 and 11, and prompt logs with rejects |
| 2026-10-06 | Add action poses, slower run, and ENV-BG backdrop; verify 41/41 tests |
| 2026-10-07 | Add silhouette, collision overlay, and palette from in-game art; finish character sheet |
