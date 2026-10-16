# Prompts and script — Walker Survival Shooting: First Props in Blender

## Reconstructed opening prompt (B00)
Illustrative reconstruction written for this film. It is **not** a saved session or a historical transcript.

```text
Please use Walker to convert my game design document about a third-person extraction shooter, where a survivor lives in a subway base and carries a rugged military tablet, into its first 3D props: a start-menu chair, the tablet and weapon crates, built in Blender through the MCP and checked in Godot.
```

## Your Turn prompt (B22)

```text
Please use Walker on my Godot project. Read my CHANGE-BRIEF and tests/a3_asset_check.gd. Add one check that plays each crate's open animation where it stands in base.tscn and tests whether the open lid passes through the back wall. Predict which crates fail before you run it, and do not move anything to make it pass.
```

## The designer's prompts shown in the film
Shown in B04, B05 and B07, in English translation, exactly as the game's SOURCES.md asset log gives them
(rows PROP-TABLET-01 and CRATE-LONG-02; the B07 quote is shortened with an ellipsis). The originals were
typed in Chinese. No model was run for the film except Kokoro for the narration.

## Narration script (Kokoro am_onyx, exact text sent to TTS)

**B00 · ASK**

Hola, this is Liam, in for Bear. The prompt on screen is a reconstruction for this film, not a saved session. It asks Walker to turn the design document for a subway extraction shooter into its first 3D props. At source revision b, three, seven, oh, six, two, six, the answer is three assets, in Blender and in a Godot scene, and a check script.

**B01 · BLUF**

I directed and Claude built my game's first 3D props. Claude wrote the Blender code; I made the decisions and one edit by hand. The checks prove the sizes, not the looks.

**B02 · CONCEPT**

The game first. You live in a subway base, carry a rugged military tablet, go out to fight monsters, and extract. This assignment needed three props for that base. A chair for the character to sit on in the start menu. The tablet itself, the core of play. And weapon crates: furniture the player will build to store items. Every footprint sits on a grid, where one cell is ten centimetres.

**B03 · ROUTE**

How they were made. Most of it went through the Blender MCP: Claude Code ran Python inside my open Blender, and looked at the viewport to check. Three later steps ran as headless scripts instead. And one honest detail: the brief was written after the chair and the tablet existed, so some of its numbers are measurements, not predictions.

**B04 · PROMPT**

Here is a real prompt, translated from my Chinese. Make me a tablet from the reference images. Block it out with cubes; a greybox is enough. And here is what Claude built: twenty-one bevelled boxes, eight hundred and four triangles. That is not a greybox. It is the first thing Claude got wrong: it built more than I asked for.

**B05 · REVISE**

I kept the shape, but front and back were hard to tell apart, so I asked for a dark green and black shell with one large black screen. Claude rebuilt it with three materials. Then the course limit bit: five hundred triangles. Keeping bevels only on the body and the four corner bumpers brought it to three hundred and eighty-eight. It is still twenty-one shapes, over the limit of six. I decided to keep it.

**B06 · REVISE**

The chair went the other way. Version one was nine boxes, with stretchers and two backrest slats. To meet the six-shape limit, I asked Claude to change it: the stretchers went, and the slats merged into one board. Same size, seventy-two triangles. That rebuild ran as a headless script, so there is no viewport capture of it. On the right is the chair in Godot.

**B07 · REVISE**

The crates taught me the grid. I asked for one cube and one crate twice as long, in military green. The first version's handles stuck out, so the small crate covered zero point five six by zero point five one five metres, off any clean grid. I set the rule, one cell is zero point one, and Claude moved the hardware inside the footprint. Now it is exactly five by five cells.

**B08 · HAND EDIT**

And this is my own screenshot, from my Blender in Simplified Chinese. Edit Mode, the small crate, one latch selected; the sidebar shows its median point. My edit: I raised both latches so each sits half on the lid and half on the body, so it reads as a latch that locks the lid. And I moved the handles up, so the centre of gravity is lower when it is carried.

**B09 · CHECK**

Then the checking. Claude measured my edit: the right latch had been stretched ten centimetres deep, into the box. I fixed it and told Claude not to measure again, and Claude wrote fixed into the records. It was not: the fix never reached the saved file. My second fix, a copy of the left latch, worked, and a hidden duplicate was deleted. Six millimetres of asymmetry remain, and I kept them.

**B10 · CODE**

Into Godot. This is my scene file, base dot T S C N. Each asset is one instance of its imported G L B, placed with a transform. The chair, the two crates, and the tablet. There is no scaling: ones on the diagonal. The y value, zero point two five, is the top of the floor slab. The tablet's row holds a tilt, because I lifted and tilted it to see it better.

**B11 · RESULT**

And here is what those lines produce, rendered by Godot at native four K through my asset camera. The chair, the tablet floating beside the large crate, and the small crate. They read as what they are at a glance, but that was my check, not the script's. The light is cool and dim; I moved one light myself so the assets could be seen.

**B12 · CODE**

Now the check script, which Claude wrote. It compares every imported asset with my brief. This table is the contract: a file, an expected size in metres, the expected lowest point, and a triangle budget of five hundred. Notice the tablet: its lowest point is minus zero point zero eight one, because I kept its origin in the centre on purpose, so it can be attached to a hand later.

**B13 · RESULT**

Here is the headless output beside the brief. Godot is y up, so the height moves to the middle number, but every size matches within two millimetres. The small crate is off by six thousandths of a millimetre. Triangles: seventy-two, three hundred and eighty-eight, and eighty-eight each. This is recorded output from a fresh export of the submitted revision, not a number typed in by hand.

**B14 · CODE**

The crates have to open. These lines find each crate's animation player, play open, jump to its last frame, and read the lid's rotation. It must be minus one hundred degrees. Then close, and it must be back at zero. The lid's origin sits on the back hinge, so it swings about the x axis.

**B15 · RESULT**

This is the same animation in the scene, rendered at four K. My capture script plays each crate's own imported open animation, then close; nothing else moves. Fifteen frames each, a little over half a second. The headless check only proves the end angles. The test report adds what it misses: the open lid swings about eight centimetres behind the footprint, so against a wall it would pass through.

**B16 · CODE**

Placement checks. The floor top is read from the floor node itself, not from an asset. Every floor item must rest on it, and every crate and desk needs footprint edges on the ten-centimetre grid. The chair is not grid-checked, because it is zero point four four by zero point four two. And this comment is history: the tablet used to be checked against the crate lid.

**B17 · RESULT**

The result: every bottom at zero point two five, every grid edge clean, no overlaps. Fifty-five passes, zero failures, exit code zero. An earlier run failed: after I lifted the tablet into the air, the lid check broke. The check changed because the placement changed, and the failing log is kept in the repository.

**B18 · LIMITS**

What the script cannot show: whether an asset looks right, reads as what it is, or suits the style. That was my own look. I recognised all of them at a glance, looked from behind and below, and found no missing faces. What I cannot confirm yet is the scale against a person, because there is no character model. Nobody else has looked at the scene.

**B19 · ERRORS**

What Claude got wrong. It overbuilt the tablet. Its first brief draft marked my own decisions as Claude's choices, or left them blank. Its first crates were off the grid. It overwrote a test chair file by accident, and the re-export came out the same size. And the worst one: it wrote fixed for the latch without measuring, and that went into a push. The next upload corrected it.

**B20 · CREDITS**

Who did what. I made every decision: the three assets, the colours, the grid, the latch, and every accept. Claude Code wrote and ran all the Blender Python, placed the assets, wrote the check, and drafted the documents. This film shows source revision b, three, seven, oh, six, two, six. The next step: a character model to settle the scale, the first gameplay in the game, and a design for the tablet's interaction.

**B21 · VERDICT**

Verdict. Built: three assets plus two desks, in Blender and in a Godot scene, with a check that passes fifty-five times. Limits: the tablet is over the shape limit by my choice, the scale next to a person is unknown, and one latch is six millimetres off. The judgement was mine; the code was Claude's. The checks prove numbers, not looks.

**B22 · HANDOFF**

Your turn. Paste this into Claude. Please use Walker on my Godot project. Read my change brief and my asset check script. Add one check that plays each crate's open animation where it stands in base dot T S C N and tests whether the open lid passes through the back wall. Predict which crates fail before you run it, and do not move anything to make it pass. The prediction is the point: write down which crate you expect to fail before the log tells you. And keep the scene as it is; you want to learn what the lid does, not hide it. Liam, in for Bear.

**B23 · OUTRO**

Walker Survival Shooting: First Props in Blender. At Nik Bear Brown.
