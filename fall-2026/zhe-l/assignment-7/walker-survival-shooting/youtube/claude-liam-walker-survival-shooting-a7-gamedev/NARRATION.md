# Narration script and prompts

Narrator: Liam (in for Bear), local Kokoro `am_onyx`, speed 1.0, 0.35 s lead-in and 0.7 s tail per beat. No paid TTS, no cloud model.

Image/voice prompts: none beyond the TTS text below. No image or music generation was used for this film; all images are engine captures, the game's own sprite sheet, or cards drawn with PIL. No living artist, brand style or existing music is referenced.

Walker prompt shown (suggested, reconstructed for the film): "Please use Walker to convert my game design document about a subway survival shooter into a Godot game. Assignment 7: add two animations - a looping pixel head, and a one-handed tablet raise."

Your Turn prompt read aloud: "Please use Walker to add a put-back animation to my tablet state machine, with a phase table first."

## B00 (0.0 s, 12.1 s)

It starts with a prompt like this one. Please use Walker to convert my game design document about a subway survival shooter into a Godot game. For Assignment Seven, that game gets two animations.

## B01 (12.1 s, 14.4 s)

So what got built? Two clips. A pixel head that breathes, sorry, blinks, in the tablet's taskbar. And a one-handed tablet raise, keyed in Blender. This teardown explains how each clip plays, who owns the bones, and what the tests can, and cannot, prove.

## B02 (26.5 s, 15.3 s)

Two routes. The pixel head is a Sprite2D, driven by an AnimationPlayer frame track. Eight keys, and it loops. The raise is an imported 3D rig, keyed in Blender and exported as a G L B. It is a committing action, with startup, active, and recovery.

## B03 (41.8 s, 27.8 s)

Here is the sheet. Four hundred forty-eight by fifty-six pixels. H frames eight, V frames one, so each cell is fifty-six by fifty-six. One track points at Sprite2D, colon frame. It keys frame zero to seven, every quarter second, in discrete steps, looping linear over two seconds. Frame seven wraps straight back to zero. No duplicate across the seam. The sheet is AI generated, with the Codex and OpenAI image tool, and Claude drew the blink.

## B04 (69.6 s, 8.8 s)

And this is what that track does in the engine. A fixture capture across one wrap: the blink, the one-pixel rise, and then the loop starts again.

## B05 (78.4 s, 15.2 s)

Question one. What is a clip? Here, a clip is a named Animation resource. A length, a step, a loop mode, and tracks that must resolve to real nodes or real bones. The read-back tests check exactly that. Thirty-seven passes for the head. Twenty-five for the raise.

## B06 (93.7 s, 19.7 s)

The raise is designed in frames. Thirty frames per second, frames zero to twenty. Startup, zero to six: the hand reaches and grips. Active, seven to fifteen: lift, then turn toward the face. Recovery, sixteen to twenty: arrive, overshoot eight millimetres, settle. And the tablet bone is keyed on exactly those boundaries. Zero, seven, sixteen, twenty.

## B07 (113.4 s, 12.8 s)

Question four. What does designing feel in frames mean? The table is also the rules. During the raise, you cannot walk, run, or jump. On frame nineteen the screen is dark. On frame twenty it lights, and becomes clickable.

## B08 (126.2 s, 12.3 s)

Here are the boundary frames from the r2 fixture, with the player camera turned around to face her. The hand reaches, grips the top edge, lifts, turns, and arrives. The screen lights on movie frame fifty-four.

## B09 (138.6 s, 17.1 s)

Question two. What does one authority mean? The character's AnimationTree, a state machine, is the only thing that poses the skeleton. The tablet hangs from a BoneAttachment3D on the tablet bone. So the tree also owns where the tablet is. It reads the hold state. It never writes game state.

## B10 (155.7 s, 15.8 s)

So here is the whole tablet set. Four states: on the hip, raising one-handed, holding one-handed, and holding two-handed. Ten transitions. Only the raise is a keyed animation. Every other move is a point two second cross-fade. And the two-handed pose is still a placeholder.

## B11 (171.4 s, 30.3 s)

Now the running game. This is a scripted-input capture: Tab presses sent with parse input event, and the player camera turned to face her. First, one uninterrupted raise: reach, grip, lift, turn, settle, and the screen lights. Then the interrupts, one in each phase. In startup, in active, and in recovery, a second press cancels the clip right away. A short press blends back to the hip. A long press blends to two hands. Then the rest of the set: back to the waist, and one hand to two hands and back. Every one of those is a point two second cross-fade.

## B13 (201.8 s, 11.2 s)

Question three. What are the two clocks? The clip advances on the process clock. The game reads it on the physics clock, one physics frame later. Before revision one, that gap was two frames.

## B14 (212.9 s, 17.0 s)

Revision one. Start the raise on the press frame itself. The screen now lights on movie frame fifty-four, not fifty-five. Revision two came from playing. The stowed tablet felt wrong, so the tablet was re-posed upright in Blender, and the arm no longer reaches out straight to grab it. Both were kept.

## B15 (230.0 s, 18.8 s)

What the tests prove. Read-backs, a state machine test, and edge tests that interrupt one frame before, on, and after every boundary. Mutations make them fail: a renamed track, a loop mode set to none, a frame key past the sheet. What a headless run cannot prove is whether the motion looks good. That was judged by eye, in the running game.

## B16 (248.8 s, 23.5 s)

Agent errors that were caught. The baseline counts included the summary line, so fifty-six and twenty-five became fifty-five and twenty-four. The head's property check was too weak, and the rename mutation exposed it. And the preview logged before the tree updated, so the r0 and r1 labels are one frame early. Claude's reading that the overshoot got flattened was accepted. Its worry about the back view was rejected, because the camera orbits freely.

## B17 (272.3 s, 19.9 s)

Verdict. Built: two clips, a four-state machine, and eleven passing test suites, at source version four two d six c c zero d. Not measured: whether hand and tablet separate during a cross-fade. Placeholder: the two-handed pose. The human posed the end pose and the stowed pose, and judged the motion. Claude derived the in-betweens, wired the tree, and wrote the tests.

## B18 (292.2 s, 18.5 s)

Your turn. Try a prompt like this. Please use Walker to add a put-back animation to my tablet state machine, with a phase table first. Before you run it, predict the frame where the screen goes dark, then check it with an edge test. Next on this list: a two-handed raise, a put-back, a jump, and walking while raising. I'm Liam, in for Bear. Thanks for watching.

## B19 (310.7 s, 5.8 s)

Walker Survival Shooting: Two Animations, One Authority. At Nik Bear Brown.
