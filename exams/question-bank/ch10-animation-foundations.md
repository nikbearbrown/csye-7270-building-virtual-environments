# Chapter 10: Animation foundations

## MA-ch10.1

A 2D developer gets one PNG holding a regular grid of equal-sized drawings of a character in successive poses. Check each statement that is true about the exact names. Each statement is worth 1 point (5 points total).

- [ ] A. The PNG is itself an animation clip, because it records the order and timing of its frames.
- [ ] B. A tilemap is the same thing as a sprite sheet, because both cut one image into a grid.
- [ ] C. A texture atlas packs images of different sizes into one texture and keeps a table of their rectangles.
- [ ] D. The file is a sprite sheet, and showing its cells in sequence at a chosen rate is frame-by-frame animation.
- [ ] E. A tilemap holds the poses of one character to play in sequence.

**Key:** A=F B=F C=T D=T E=F

**Why:**

- A: An image holds pixels only; order, timing and looping come from animation data that refers to it.
- B: A sprite sheet's cells are poses to play in sequence, whereas a tilemap's tiles build a level.
- C: An atlas is a general packing of many images with a lookup table.
- D: A sprite sheet stores the poses of an animation in one image, and playing them in sequence is frame-by-frame animation.
- E: A tilemap places reusable tiles on a level grid; poses to play in sequence belong to a sprite sheet.

**Source:** Sprite sheet, atlas and tilemap

## MA-ch10.2

Team 1 animates a hero with a sprite sheet of hand-drawn walk frames. Team 2 animates a 2D cutout character: separate body-part images attached to a skeleton, with a walk clip that rotates and moves the bones. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Team 2's clip stores a table of image rectangles for each pose.
- [ ] B. Team 1's version needs a skeleton, because bones position each drawn frame.
- [ ] C. Team 2's animation changes bone transforms, and the attached parts follow.
- [ ] D. Team 1's animation changes which image is shown from one frame to the next.
- [ ] E. Team 2's walk clip stores a full image for each pose, packed with the bone data.

**Key:** A=F B=F C=T D=T E=F

**Why:**

- A: A rig-based clip stores bone transform keys; a table of rectangles belongs to an atlas.
- B: Frame-by-frame animation has no skeleton, since each frame is a complete picture.
- C: Moving a bone carries the parts attached to it.
- D: Frame-by-frame animation swaps whole drawings.
- E: A skeletal clip holds transform keys, and the part images are the same in every pose.

**Source:** What is stored: sprite sheet versus rig

## MA-ch10.3

A sprite sheet is a regular grid of equal cells with no gaps, numbered from 0, left to right and row by row from the top-left. A developer tells a coding agent to "play the run animation from the sheet". Check each statement that is true about the grid terms. Each statement is worth 1 point (5 points total).

- [ ] A. Frame index is counted from 1 in column-by-column order.
- [ ] B. The agent has to be told the grid layout, as columns and rows or as a cell size, because pixels do not mark frame boundaries.
- [ ] C. Frame rate of a sprite animation is how many drawn cells are shown per second.
- [ ] D. A wrong guess of columns and rows raises an error.
- [ ] E. The image file records which cells belong to the run animation.

**Key:** A=F B=T C=T D=F E=F

**Why:**

- A: Frame index names a cell by its position, counted from 0 row by row in this layout.
- B: Columns, rows or cell size are the grid metadata the image lacks.
- C: The animation's own rate counts drawn frames per second, apart from the rendering rate.
- D: A wrong grid divides the image anyway, so nothing fails.
- E: A plain image has no record of animation names.

**Source:** Sprite sheet grid terms

## MA-ch10.4

A studio has a 3D walk clip authored for Character X's skeleton. Character Y has a different mesh and different limb lengths but a skeleton whose bones correspond one for one. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Different limb lengths can make retargeted feet slide or float, which IK often corrects.
- [ ] B. A sprite-sheet walk drawn for X can be retargeted to Y by mapping bone names to cells.
- [ ] C. A humanoid clip needs a custom mapping to drive a four-legged skeleton.
- [ ] D. Characters that share one skeleton can share clips, since a clip stores bone motion.
- [ ] E. Retargeting maps a source skeleton's motion onto a target skeleton by pairing bones.

**Key:** A=T B=F C=T D=T E=T

**Why:**

- A: Proportions change where feet land, so contact is re-solved with IK.
- B: A sprite sheet has no bones and shows drawings of one character.
- C: Without corresponding bones there is nothing to pair, so a manual mapping is needed.
- D: A clip addresses bones by name or path, not pixels.
- E: Retargeting pairs source bones with target bones so motion transfers.

**Source:** Retargeting

## MA-ch10.5

A character has a walk clip and a run clip, and the designer wants a smooth change as speed rises. Check each statement that is true about the exact terms. Each statement is worth 1 point (5 points total).

- [ ] A. A blend space is a way to mix several clips by one or two parameters such as speed.
- [ ] B. Mixing the pixels of two sprite frames gives a ghosted double image, not an in-between pose.
- [ ] C. A blend weight of 0.5 sets the playback speed to half.
- [ ] D. Blending combines two poses by interpolating each bone's transform, weighted by a blend value.
- [ ] E. Cutout rigs have no bones, so their poses are not blended like 3D ones.

**Key:** A=T B=T C=F D=T E=F

**Why:**

- A: A blend space maps parameter values to blends of clips.
- B: A cross-fade overlays both drawings and does not draw the pose between them.
- C: The blend weight mixes poses; playback speed is a separate setting.
- D: Skeletal poses are bone transforms, which interpolate per bone.
- E: A 2D skeleton is still a skeleton, so its poses blend per bone.

**Source:** Blending and blend space

## MA-ch10.6

An art lead compares a sprite sheet drawn at a fixed pixel size with a skeletal 3D character drawn from its mesh, on 1080p and 4K screens. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A 3D character is drawn from its mesh at screen resolution, so its sharpness is not locked to a fixed frame size.
- [ ] B. A cutout rig built from bitmap parts is resolution independent.
- [ ] C. Nearest-neighbour filtering keeps magnified pixels crisp and blocky.
- [ ] D. Real detail at 4K for a sprite comes from scaling the frames up with linear filtering.
- [ ] E. Linear filtering blends neighbouring pixels, so a magnified sprite looks blurry.

**Key:** A=T B=F C=T D=F E=T

**Why:**

- A: Geometry is rasterised for the current screen each frame.
- B: The parts are bitmaps with a fixed pixel size, so enlarging them softens them.
- C: Nearest-neighbour picks the closest texel, so edges stay hard.
- D: Scaling cannot invent detail; frames have to be redrawn or exported larger.
- E: Linear filtering averages neighbours, which softens edges.

**Source:** Resolution and filtering

## MA-ch10.7

An animator wants a cartoon character to squash flat on landing and show a drawn smear on a punch, and a 3D character must bend an elbow without pinching. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Skinning with vertex weights splits one mesh into rigid pieces at a joint.
- [ ] B. Hand-drawn frames can take a squash or smear shape, because each frame is an independent picture.
- [ ] C. Rigid cutout parts rotating about a joint stay joined at the edges.
- [ ] D. A skinned mesh takes the silhouette of a hand-drawn frame because bones move vertices.
- [ ] E. A rig changes the pose of one set of art, so an unmodelled shape such as a smear needs extra tools such as blend shapes.

**Key:** A=F B=T C=F D=F E=T

**Why:**

- A: Skinning blends bone influence on shared vertices, giving a smooth bend.
- B: Frame-by-frame work is free-form.
- C: Rigid pieces do not stay joined at their edges when they rotate.
- D: The silhouette is limited by the mesh, weights and bone motion.
- E: A rig changes pose, not the underlying shapes.

**Source:** Fixed look versus deformation

## MA-ch10.8

A producer lists four animation methods: frame-by-frame, cutout, procedural and tweening. Check each statement that is true about the exact names. Each statement is worth 1 point (5 points total).

- [ ] A. Tweening is the name for animation drawn frame by frame.
- [ ] B. Procedural animation is computed at runtime from rules, physics or targets.
- [ ] C. Frame-by-frame animation uses a skeleton with about one bone per drawn piece.
- [ ] D. Procedural animation is a fixed recording keyed on a timeline.
- [ ] E. Cutout animation redraws the whole figure for each pose.

**Key:** A=F B=T C=F D=F E=F

**Why:**

- A: A tween computes in-between values of a property between endpoints.
- B: Procedural motion responds to conditions, so it can differ per playback.
- C: Frame-by-frame swaps whole drawings and has no skeleton.
- D: Keys on a timeline describe authored animation.
- E: Cutout reuses separate pieces such as limbs and a head.

**Source:** Cutout, procedural, tween and frame-by-frame

## MA-ch10.9

An animator keys a door's rotation to 0 degrees at 0.0 s and to 90 degrees at 1.0 s and sets nothing else. Check each statement that is true about the terms. Each statement is worth 1 point (5 points total).

- [ ] A. The clip stores one value for each rendered frame.
- [ ] B. Interpolation computes the values between keys, so the door shows intermediate angles.
- [ ] C. Linear interpolation gives 60 degrees at 0.5 s.
- [ ] D. A keyframe is an authored value at a chosen time.
- [ ] E. A display with a higher refresh rate needs the clip re-authored with more keys.

**Key:** A=F B=T C=F D=T E=F

**Why:**

- A: The clip stores two keys; the engine computes values for frames.
- B: Interpolation fills in the in-betweens.
- C: Linear interpolation halfway between 0 and 90 gives 45 degrees.
- D: A key is a value pinned to a time.
- E: Values are sampled from time, so any display rate works with the same keys.

**Source:** Keyframe and interpolation

## MA-ch10.10

A menu panel slides from x = 0 to x = 300 over 0.5 s, once linear and once with ease-out. Check each statement that is true about the terms. Each statement is worth 1 point (5 points total).

- [ ] A. Easing shapes the speed profile of the interpolation.
- [ ] B. Ease-out starts fast and slows toward the end.
- [ ] C. An ease-out finishes sooner than the linear version because it covers more distance early.
- [ ] D. Easing changes the start value, the end value or the duration.
- [ ] E. Ease-in starts fast and slows down.

**Key:** A=T B=T C=F D=F E=F

**Why:**

- A: Easing is the curve that decides how speed varies.
- B: Ease-out decelerates into the end.
- C: Both versions finish at the same time.
- D: Easing keeps the endpoints and the duration.
- E: Ease-in starts slowly and speeds up; ease-out is the one that slows.

**Source:** Easing

## MA-ch10.11

A developer sets up a door with an animation player node and animation clips. Check each statement that is true about the terms. Each statement is worth 1 point (5 points total).

- [ ] A. The animation player plays clips: it advances time, applies values and handles looping and speed.
- [ ] B. A clip is data: tracks bound to targets, with keys along time.
- [ ] C. A track whose target was renamed or moved reports a loud error that stops the game.
- [ ] D. A timeline is the time axis on which keys sit, and the playhead marks the current time.
- [ ] E. A clip animates one property of one object, so a door needs one clip per property.

**Key:** A=T B=T C=F D=T E=F

**Why:**

- A: The player applies a clip's values to its targets over time.
- B: A clip does nothing until something plays it.
- C: Tracks refer to targets by path or name, so a changed path can leave a track pointing at nothing without failing loudly.
- D: Scrubbing moves the playhead to preview values.
- E: A clip commonly holds many tracks.

**Source:** Clip, track, timeline and animation player

## MA-ch10.12

A producer says a character "needs a rig". Check each statement that is true about the exact names. Each statement is worth 1 point (5 points total).

- [ ] A. Skinning binds mesh vertices to bones so the mesh follows them.
- [ ] B. A skeleton holds structure and pose, and a walk comes from a clip, code or a solver.
- [ ] C. A rig is the full posable setup: skeleton, skin binding and often controls such as IK handles.
- [ ] D. A skeleton (armature) is a hierarchy of bones where moving a parent bone moves its children.
- [ ] E. The skeleton is geometry that is drawn as the body in the final game.

**Key:** A=T B=T C=T D=T E=F

**Why:**

- A: Skinning ties vertices to bones with weights.
- B: A skeleton holds structure and pose; motion comes from clips, code or solvers.
- C: Rig names the whole setup that makes a character posable.
- D: Bones are parented so a shoulder rotation carries the arm.
- E: Bones are not drawn by default; the mesh is.

**Source:** Skeleton, armature, rig and skinning

## MA-ch10.13

Under linear blend skinning, a vertex near an elbow has weight 0.75 for the upper-arm bone and 0.25 for the forearm bone. Check each statement that is true about the terms. Each statement is worth 1 point (5 points total).

- [ ] A. Vertex weights are one number per bone for the whole mesh.
- [ ] B. Vertex weights are normally kept so that they sum to 1.
- [ ] C. Vertex weights are stored per vertex, so each vertex has its own mix of bone influences.
- [ ] D. Painting vertex weights changes the keys stored in the animation clip.
- [ ] E. A weight of 1 for one bone leaves the vertex halfway between two bones.

**Key:** A=F B=T C=T D=F E=F

**Why:**

- A: Weights vary vertex by vertex.
- B: Normalised weights keep the blended result on the scale of bone motion.
- C: Weight is influence at a vertex.
- D: Weights belong to the skin binding; clip keys are separate.
- E: With the whole weight on one bone the vertex copies that bone.

**Source:** Vertex weights and skinning

## MA-ch10.14

A character walks down uneven stairs, and the walk clip keys the hip, knee and ankle rotations of each leg. Check each statement that is true about the terms. Each statement is worth 1 point (5 points total).

- [ ] A. Forward kinematics computes the foot position from the joint rotations down a chain.
- [ ] B. An IK target beyond the chain's length is reached by lengthening the bones.
- [ ] C. Inverse kinematics takes a target for the end of a chain, such as a foot, and solves the joint rotations.
- [ ] D. Forward kinematics starts from the target position and works back to the hip rotation.
- [ ] E. Adding IK to the legs usually means layering it over the clip, which still drives the rest of the pose.

**Key:** A=T B=F C=T D=F E=T

**Why:**

- A: FK goes from rotations to end position.
- B: Rotation does not lengthen bones, so a far target is only approached with the chain extended.
- C: IK goes from a target position to joint angles.
- D: That describes IK; forward kinematics starts from joint rotations.
- E: IK adjusts the legs on top of the authored animation.

**Source:** Forward versus inverse kinematics

## MA-ch10.15

A walk clip's root bone travels 1.2 m forward in each 1.0 s loop. A developer tells a coding agent "make the character walk forward when I press up". Check each statement that is true about the terms. Each statement is worth 1 point (5 points total).

- [ ] A. In-place animation poses the limbs and leaves travel to code or physics.
- [ ] B. Code can set a different speed with root motion without feet sliding.
- [ ] C. Root motion means the clip plays in place so the root bone stays at the origin.
- [ ] D. Root motion applies the root bone's movement in the clip to the character's position in the world.
- [ ] E. If root motion moves the character and code also moves the body, the distance is covered twice.

**Key:** A=T B=F C=F D=T E=T

**Why:**

- A: An in-place clip has no root translation to extract.
- B: The feet are planted for the distance the clip covers, so another speed slides them.
- C: That is the in-place definition, the opposite of root motion.
- D: Root motion hands movement authority to the clip.
- E: Two sources of forward movement add up.

**Source:** Root motion versus in-place animation

## MA-ch10.16

A hand-drawn run cycle has 8 frames at 12 frames per second in a looping clip, and frame 8 is an exact copy of frame 1. Check each statement that is true about the loop terms. Each statement is worth 1 point (5 points total).

- [ ] A. The loop seam is the point where the last frame leads back to the first.
- [ ] B. A seamless loop needs a last frame that is an exact copy of the first.
- [ ] C. A duplicated end frame shows two different poses in a row.
- [ ] D. Removing the duplicate leaves 8 distinct frames in the cycle.
- [ ] E. Ping-pong mode (forward, then backward) is a good substitute for a run cycle.

**Key:** A=T B=F C=F D=F E=F

**Why:**

- A: The seam is where one pass ends and the next begins.
- B: The pose after the last frame has to lead naturally into the first, not duplicate it.
- C: A duplicate shows the same pose twice in a row, which reads as a stall.
- D: Removing one of the 8 leaves 7 distinct frames.
- E: Running played backward steps the wrong way, so ping-pong does not suit a run.

**Source:** Loop seam and loop mode

## MA-ch10.17

Script 1 turns a fan blade 3 degrees on every drawn frame. Script 2 turns it 180 degrees per second multiplied by delta time. Check each statement that is true about the terms. Each statement is worth 1 point (5 points total).

- [ ] A. Delta time is the time since the previous frame.
- [ ] B. Script 2 is frame-rate independent because it scales a per-second rate by elapsed time.
- [ ] C. A playback speed scale of 2 makes a clip take twice as long to finish.
- [ ] D. Frame-rate independence means results do not depend on the number of frames drawn.
- [ ] E. Frame-rate independence is reached by scaling with elapsed time, not by locking the rate.

**Key:** A=T B=T C=F D=T E=T

**Why:**

- A: Delta time is the frame-to-frame interval, not the total elapsed time.
- B: A rate times delta time gives the same motion per second.
- C: A speed scale of 2 plays twice as fast, so it finishes in half the time.
- D: The result depends on time, not frames.
- E: Scaling by elapsed time makes results independent of the frame rate.

**Source:** Delta time and frame-rate independence

## MA-ch10.18

A sword swing clip lasts 0.6 s. The hitbox is on from 0.20 s to 0.35 s. Option 1 starts a code timer when the swing begins. Option 2 puts animation events (a method-call track) on the clip. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A cancelled clip fires the events that lie past the point where it stopped.
- [ ] B. An animation event calls a function when playback passes its keyed time.
- [ ] C. Events live in clip time, so they stay aligned when playback speed changes.
- [ ] D. A code timer counts real time, so it drifts from a clip played at 1.5 times speed.
- [ ] E. If the swing is cancelled early, the event turns the hitbox off by itself.

**Key:** A=F B=T C=T D=T E=F

**Why:**

- A: Keys past the cancel point are never reached, so they do not fire.
- B: A method track is a function call keyed on the timeline.
- C: Clip time scales with playback speed.
- D: A timer has its own clock, apart from clip speed.
- E: An event that was never reached does not run, so cleanup also has to happen on cancel.

**Source:** Animation event and method track

## MA-ch10.19

A project has one file, hero.png. A developer types "animate the character walking" without saying what kind of art it holds. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. An agent that assumes a rig may rotate bone nodes that do not exist.
- [ ] B. The word "walking" fixes the frame count and the order of the cells.
- [ ] C. The word "walking" names neither a sprite sheet nor a rig, so the agent has to guess the method.
- [ ] D. A precise version says hero.png is a 6 by 1 sprite sheet of 64 by 64 frames played as a looping walk at 10 frames per second.
- [ ] E. Loop mode and speed are settings the agent would otherwise choose.

**Key:** A=T B=F C=T D=T E=T

**Why:**

- A: Skeletal techniques on flat frames target things that do not exist.
- B: Frame count belongs to the art, not the verb.
- C: Sprite-sheet and rig animation are built differently, and the sentence names neither.
- D: It names the art type, grid, frame size, loop and rate.
- E: Looping and speed are not implied by the word walking.

**Source:** Vague versus precise animation prompt

## MA-ch10.20

A character must reach for a cup the player can place anywhere on a table. The project has one authored reach clip keyed to reach straight ahead. A developer says "play a reach animation toward the cup". Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Inverse kinematics on the arm chain, with the cup's position as target, is the exact request.
- [ ] B. Forward kinematics makes the hand go to the cup because it starts from the target.
- [ ] C. A pole or hint names the elbow direction, since a target alone leaves it open.
- [ ] D. The authored clip reaches the place it was keyed for.
- [ ] E. A blend space between authored reaches stays inside the range of those clips.

**Key:** A=T B=F C=T D=T E=T

**Why:**

- A: IK solves joint rotations from a target position.
- B: FK computes the hand position from rotations; it takes no target.
- C: Many joint configurations reach the same point.
- D: Keyed rotations are fixed data.
- E: A blend space interpolates between authored poses, so it stays inside their range.

**Source:** Inverse kinematics prompt

## MA-ch10.21

A pause panel slides in over 0.25 s and a designer wants to scrub and retime it. A health bar eases from its current width to a new width, unknown in advance, on each hit. Check each statement that is true about the terms. Each statement is worth 1 point (5 points total).

- [ ] A. A tween takes a texture and a mesh.
- [ ] B. The health bar suits a tween created in code, because its end value exists at runtime.
- [ ] C. A tween has no easing setting and moves at constant speed.
- [ ] D. A tween is authored as keys in the scene so a designer can scrub it.
- [ ] E. The panel suits an authored clip, which is stored with the scene and editable on a timeline.

**Key:** A=F B=T C=F D=F E=T

**Why:**

- A: A tween takes a duration and an easing curve.
- B: A tween moves from the current value to a target given when it is created.
- C: Tweens normally accept an easing curve.
- D: A tween is created and run from code.
- E: A clip is made ahead of time.

**Source:** Clip versus tween

## MA-ch10.22

A studio picks sprite-sheet animation for a pixel-art platformer and rig-based animation for a 3D game with twelve characters on one humanoid body. Check each statement that is true about the terms. Each statement is worth 1 point (5 points total).

- [ ] A. Characters that share a skeleton need separate clips for each body.
- [ ] B. A sprite sheet holds drawn images in a grid plus data on which to show and when.
- [ ] C. A rig-based character holds a skeleton, art bound to it and clips of bone transforms.
- [ ] D. A rig-based clip changes the displayed image from frame to frame.
- [ ] E. Drawn frames transfer between characters by retargeting.

**Key:** A=F B=T C=T D=F E=F

**Why:**

- A: A shared skeleton lets clips be reused and mixed.
- B: A sprite sheet is images plus timing data.
- C: A rig is skeleton, binding and bone-transform clips.
- D: Changing the displayed image describes frame-by-frame; a rig changes bone transforms.
- E: Drawn frames belong to one character and do not retarget.

**Source:** Sprite sheet versus rig choice

## MA-ch10.23

A developer tells a coding agent "animate the walk", and the agent has to know the art type. Check each statement that is true about exact rewrites. Each statement is worth 1 point (5 points total).

- [ ] A. A sprite-sheet rewrite names the bones and the skeleton.
- [ ] B. A sprite-sheet rewrite names the bones to rotate.
- [ ] C. Slicing a sheet with the wrong grid is one plausible wrong build from a guess.
- [ ] D. A rig rewrite names the columns and rows of the sheet.
- [ ] E. A rig rewrite names the skeleton or model, the walk clip, its loop mode and whether motion is in place or uses root motion.

**Key:** A=F B=F C=T D=F E=T

**Why:**

- A: A sheet has grid, cells, rate and loop; a skeleton belongs to a rig.
- B: A sheet has no bones.
- C: A wrong grid cuts the image into the wrong cells.
- D: Columns and rows belong to a sheet, not a rig.
- E: Those are the settings a rig clip needs.

**Source:** Rewrite of the animate-the-walk prompt

## MA-ch10.24

A door rotates from 0 to 90 degrees over 1 second. Check each statement that is true about telling a keyframe, interpolation and easing apart. Each statement is worth 1 point (5 points total).

- [ ] A. Reaching 45 degrees at 0.5 s is interpolation.
- [ ] B. Keyframe is the name for the computed value between two endpoints.
- [ ] C. 0 degrees at 0.0 s and 90 degrees at 1.0 s are keyframes.
- [ ] D. Easing is the name for the authored value at a chosen time.
- [ ] E. Slow in, slow out is keyframing.

**Key:** A=T B=F C=T D=F E=F

**Why:**

- A: Interpolation computes in-between values.
- B: That describes interpolation.
- C: A keyframe is an authored value at a time.
- D: That describes a keyframe.
- E: Slow in, slow out is easing.

**Source:** Keyframe, interpolation and easing

## MA-ch10.25

A tester reports that when the character raises an arm, the skin near the shoulder stretches toward the neck and the armpit collapses. Check each statement that is true about the terms. Each statement is worth 1 point (5 points total).

- [ ] A. The animation clip's keys are the likely cause.
- [ ] B. The symptom points first at vertex weights, which set how much each bone influences a vertex.
- [ ] C. Deleting the walk clip is a fitting fix.
- [ ] D. Shoulder vertices following the neck bone point to a clip that was keyed wrongly.
- [ ] E. A precise report names the bones, the vertex group affected and the pose.

**Key:** A=F B=T C=F D=F E=T

**Why:**

- A: The keys move bones correctly; the skin is the problem.
- B: Weights decide how skin follows bones.
- C: Weight painting corrects influence; the clip is not the cause.
- D: Wrong or too many bone influences make vertices follow the wrong bone.
- E: Naming bone, vertex group and pose lets an artist reproduce it.

**Source:** Diagnosing a skinning fault

## MA-ch10.26

A walk clip makes the feet hover above some steps and sink into others on uneven stairs. Check each statement that is true about the terms. Each statement is worth 1 point (5 points total).

- [ ] A. Hip height is adjusted so both feet can reach their targets.
- [ ] B. A good instruction names the texture of the stairs and the sprite frame rate.
- [ ] C. The keyed rotations know nothing about the stair surface, so the foot goes where the keys put it.
- [ ] D. Finding the ground under a foot with a ray cast and using it as the IK target is a fitting fix.
- [ ] E. IK replaces the walk clip for the legs.

**Key:** A=T B=F C=T D=T E=F

**Why:**

- A: Hip height lets the legs reach.
- B: Chain, pole and blend weight are the terms for an IK setup.
- C: Forward kinematics follows the keys, not the ground.
- D: A cast finds the surface and IK reaches it.
- E: IK is layered on top of the clip.

**Source:** Foot placement with IK

## MA-ch10.27

A developer tells a coding agent "make the character walk forward at 3 metres per second using the walk clip", and the clip's root bone travels 1.2 m per 1.0 s loop. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Ignoring root motion and moving at 3 m/s makes the feet slide, since the clip plants them for 1.2 m per loop.
- [ ] B. Choosing one authority for movement is a fitting rewrite.
- [ ] C. Applying root motion and also moving the body at 3 m/s causes double movement.
- [ ] D. An in-place clip with code-set speed needs no matching of playback speed.
- [ ] E. Root motion lets code set the speed freely.

**Key:** A=T B=T C=T D=F E=F

**Why:**

- A: The feet were authored for another speed.
- B: One source of movement keeps the result predictable.
- C: Two sources of forward movement add.
- D: Matching playback speed to travel speed prevents sliding.
- E: Root motion gives the clip the authority over speed.

**Source:** Root motion rewrite

## MA-ch10.28

A script moves a platform 2 units each time a frame is drawn, and it is much faster on a 144 frames per second monitor than on a 60 one. Check each statement that is true about the terms. Each statement is worth 1 point (5 points total).

- [ ] A. Defining speed in units per second and multiplying by delta time fixes it.
- [ ] B. The movement is tied to the number of frames drawn.
- [ ] C. A fixed physics step is an engine alternative.
- [ ] D. Per-frame increments are frame-rate independent.
- [ ] E. A sprite sheet's frame rate is the rendering rate.

**Key:** A=T B=T C=T D=F E=F

**Why:**

- A: Per-second rates scaled by elapsed time are frame-rate independent.
- B: A per-frame increment scales with frames.
- C: The fixed step runs at a constant interval.
- D: Per-frame increments depend on frame rate.
- E: The animation's own rate is separate from the rendering rate.

**Source:** Frame-rate independence rewrite

## MA-ch10.29

A designer wants the hitbox on during part of a sword swing and a whoosh at its start. Check each statement that is true about the terms. Each statement is worth 1 point (5 points total).

- [ ] A. An animation event or method track is a function call keyed at a time on the clip.
- [ ] B. A precise instruction names the clip, the times, the functions and what happens on cancel.
- [ ] C. Events keep the timing in code, so retiming the clip leaves them where they were.
- [ ] D. A code timer follows clip playback speed on its own.
- [ ] E. A cancelled clip fires the keys that lie past the point where it stopped.

**Key:** A=T B=T C=F D=F E=F

**Why:**

- A: Events are keyed calls.
- B: Those are the details the agent would otherwise guess.
- C: Event timing travels with the clip.
- D: A code timer runs on its own clock, apart from clip playback speed.
- E: Keys past the cancel point are not reached, so they do not fire.

**Source:** Animation event instruction

## MA-ch10.30

Playtesters say a run cycle hitches once per loop, and switching from walk to run pops. Check each statement that is true about the terms. Each statement is worth 1 point (5 points total).

- [ ] A. A rig can cross-fade or blend bone transforms over a short time to hide a pop.
- [ ] B. A sprite sheet blends frames into a true in-between pose.
- [ ] C. A pop on switching is an instant cut between two different poses.
- [ ] D. A sprite-sheet fix switches at a matching point in the cycle or adds transition frames.
- [ ] E. A hitch at the loop seam comes from a pop between walk and run.

**Key:** A=T B=F C=T D=T E=F

**Why:**

- A: Skeletal poses interpolate per bone.
- B: Mixing pixels gives a ghost, not a pose.
- C: A pop is a jump between poses.
- D: Matching phase or extra frames hide the cut.
- E: A seam hitch comes from a last frame that duplicates the first.

**Source:** Loops, blending and clip switching
