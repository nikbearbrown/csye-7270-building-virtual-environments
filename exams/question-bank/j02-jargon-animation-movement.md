# Jargon test: animation movement

## MA-jargon.11

A student describes how a door should open to a coding agent. Check each statement that is true about the terms. Each statement is worth 1 point (5 points total).

- [ ] A. Easing changes the final value that the animation ends on.
- [ ] B. A keyframe is a stored value (such as a rotation) at a specific moment on the timeline.
- [ ] C. Interpolation is the calculation of the in-between values between two keyframes.
- [ ] D. A keyframe is the computed in-between frame that the engine draws between two poses.
- [ ] E. Easing changes the frame rate at which the engine draws the scene.

**Key:** A=F B=T C=T D=F E=F

**Why:**

- A: Easing leaves the start and end values alone.
- B: Keyframes are the authored anchor values.
- C: The engine fills the gaps between keyframes by interpolating.
- D: In-betweens are produced by interpolation; they are not keyframes.
- E: Easing shapes the speed curve of one animated value; it does not change how often frames are drawn.

**Source:** Keyframe, interpolation and easing

## MA-jargon.12

A designer asks for a button that "eases in" or "eases out" when it appears. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Ease-in starts slowly and speeds up.
- [ ] B. Linear interpolation changes the value at a constant rate.
- [ ] C. Ease-out starts quickly and slows down toward the end.
- [ ] D. Ease-in-out is slow at both the start and the end, and quicker in the middle.
- [ ] E. Ease-out means the animation plays backward after it finishes.

**Key:** A=T B=T C=T D=T E=F

**Why:**

- A: Ease-in accelerates from rest.
- B: Linear means a straight line from start to end.
- C: Ease-out decelerates into the final value.
- D: Ease-in-out combines both.
- E: Direction of playback is a separate setting from easing.

**Source:** Easing curves

## MA-jargon.13

A developer wants a UI panel to slide in using code instead of an authored clip. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A tween is the better tool for a short one-off effect, such as a pop-up scaling in.
- [ ] B. A tween needs a rig before it can move a node.
- [ ] C. A tween is a code-driven interpolation of a property from a start value to an end value over a set time.
- [ ] D. A tween usually takes an easing type and a duration as settings.
- [ ] E. A tween is another name for a keyframe stored in an animation clip.

**Key:** A=T B=F C=T D=T E=F

**Why:**

- A: Quick procedural effects are a good fit for tweens.
- B: A tween can animate any property, such as position or scale, with no skeleton involved.
- C: Tweens are created in code and animate a property over time.
- D: Duration and easing are the usual parameters.
- E: Keyframes are authored data in a clip; a tween is a runtime process.

**Source:** Tween versus authored clip

## MA-jargon.14

A rigged character needs to blend and switch motions. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A blend tree decides when the character is allowed to die.
- [ ] B. A state machine holds states and the transitions that move between them when conditions are met.
- [ ] C. A state machine blends clips by weight and has no concept of transitions.
- [ ] D. A blend tree is the right tool to switch from the idle clip to a death clip when health reaches zero.
- [ ] E. A blend tree mixes several clips together according to one or more parameters, such as speed.

**Key:** A=F B=T C=F D=F E=T

**Why:**

- A: Life and death are game logic; the animation system only shows the result.
- B: States such as idle and jump are linked by transitions with conditions.
- C: Transitions are the core idea of a state machine.
- D: A one-time switch on a condition is a state machine transition; a blend tree mixes clips by a parameter.
- E: A blend tree outputs a weighted mix of clips driven by parameters.

**Source:** Blend tree versus state machine

## MA-jargon.15

An artist hands over a 3D character. Check each statement that is true about the skeleton terms. Each statement is worth 1 point (5 points total).

- [ ] A. Skinning weights say which texture is applied to each bone.
- [ ] B. A bone is a vertex that is hidden from the renderer.
- [ ] C. A rig is a skeleton of bones together with the setup that lets the mesh follow them.
- [ ] D. A rig is a texture that stores the colour of the character's skin.
- [ ] E. A bone is a transform in the skeleton hierarchy that can be rotated to pose the character.

**Key:** A=F B=F C=T D=F E=T

**Why:**

- A: Skinning weights say how strongly each vertex follows each bone.
- B: A bone is not a vertex; it is a joint transform.
- C: A rig is the skeleton plus the binding of mesh to skeleton.
- D: Skin colour comes from textures; the rig is structural.
- E: Bones form a parent-child hierarchy and are posed by transforms.

**Source:** Rig, bone and skinning

## MA-jargon.16

A walking character slides across the ground in the game, and a student must name the cause and the fix. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. If a clip uses root motion and the script also moves the body, the character travels half the distance.
- [ ] B. Root motion uses the movement baked into the animation to move the character's root in the game.
- [ ] C. An in-place clip is unsuitable for a character that moves through the world.
- [ ] D. An in-place animation moves the character's root through the world by itself.
- [ ] E. Root motion means the camera is attached to the character's root bone.

**Key:** A=F B=T C=F D=F E=F

**Why:**

- A: Two sources of motion add together, so the character travels the distance twice.
- B: With root motion the animation drives the character's travel.
- C: In-place clips are the usual choice for code-driven movement.
- D: An in-place clip runs on the spot; game code supplies the movement.
- E: Root motion concerns who moves the character, not the camera.

**Source:** Root motion versus in-place

## MA-jargon.17

A character's foot must land on uneven stairs and a hand must grip a rail. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. FK starts from a target position and solves backward for the joint angles.
- [ ] B. Forward kinematics (FK) sets the rotation of each joint from the parent down and the end position results from those rotations.
- [ ] C. IK and FK are two names for the same technique.
- [ ] D. Inverse kinematics (IK) works out the joint angles needed to put the end of a chain, such as a foot, at a target position.
- [ ] E. IK is a good fit for planting a foot on a step whose height is only known at run time.

**Key:** A=F B=T C=F D=T E=T

**Why:**

- A: That description is IK.
- B: FK poses by rotating each joint in order along the chain.
- C: They solve in opposite directions.
- D: IK solves from the goal back to the joint angles.
- E: Foot placement on varied ground is a classic IK use.

**Source:** IK versus FK

## MA-jargon.18

A 2D game uses a sprite sheet for its hero. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Frame rate for a sprite animation is how many frames are shown per second.
- [ ] B. A sprite sheet is one image holding many frames laid out in a grid.
- [ ] C. Halving the frame rate makes the same animation play at twice the speed.
- [ ] D. Slicing a sprite sheet needs the number of bones in the skeleton.
- [ ] E. A sprite sheet stores bones and skinning weights.

**Key:** A=T B=T C=F D=F E=F

**Why:**

- A: Frame rate is frames per second.
- B: Many frames share one texture.
- C: Fewer frames per second makes the animation slower.
- D: Slicing needs the grid layout (cell size or columns and rows); sprite sheets have no bones.
- E: Bones belong to rigs, not to sprite sheets.

**Source:** Sprite sheet and frame rate

## MA-jargon.19

A student rewrites the vague prompt "animate the character walking". Check each rewrite that uses the exact terms for a 3D rigged character correctly. Each statement is worth 1 point (5 points total).

- [ ] A. "Play the walk clip from the rig, looping, in place, and move the body in script at the speed value."
- [ ] B. "Cut the walk clip into a 4 by 2 grid and show each cell for 100 ms."
- [ ] C. "Give the walk clip a frame rate of 12 and a sprite sheet of 8 bones."
- [ ] D. "Rotate the walk of the rig by tweening its UV."
- [ ] E. "Add a blend tree on the speed parameter that mixes the idle, walk and run clips."

**Key:** A=T B=F C=F D=F E=T

**Why:**

- A: This names the clip, loop mode, root handling and who moves the body.
- B: Cutting into a grid describes a sprite sheet, not a rigged clip.
- C: A sprite sheet has frames, not bones; the terms are mixed up.
- D: UV is a texture coordinate and is not a thing to rotate to make a walk.
- E: Blending clips by a parameter is the tool for idle, walk and run.

**Source:** Rewrite a vague animation prompt

## MA-jargon.20

A prompt says: "Animate the rig with a sprite sheet and key the bones every frame at 24 bones per second." Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. "Bones per second" is a standard unit of animation speed.
- [ ] B. "24 bones per second" is the wrong unit; speed of playback is frames per second.
- [ ] C. The prompt is correct because a sprite sheet and a rig mean the same thing.
- [ ] D. "Sprite sheet" is the wrong word for a rig; a rig is animated with clips of bone transforms.
- [ ] E. "Key the bones" is acceptable, since a keyframe stores a bone's transform at a time.

**Key:** A=F B=T C=F D=T E=T

**Why:**

- A: There is no such unit.
- B: Playback speed is frames per second.
- C: They are different animation methods.
- D: Sprite sheets are flat image frames; rigs use bone transforms.
- E: Keying a bone means storing its transform at a given time.

**Source:** Spot the wrong word in an animation prompt

