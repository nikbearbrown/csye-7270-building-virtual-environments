# Chapter 4: Scenes, collision and physics

## MA-ch04.1

A designer wants a coin that adds to the score when the player touches it while the player walks straight through. The developer asks a coding agent for 'a coin collider' in a 2D Godot game. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. 'Collider' is used for solid shapes and detection regions alike, so the word leaves the role open.
- [ ] B. A detection region works from the pixels of its sprite and needs no collision shape.
- [ ] C. An Area2D reports overlaps and does not block the body that enters it.
- [ ] D. 'A trigger area on the coin that removes it when the player enters, without blocking' names the role, the event and the non-blocking requirement.
- [ ] E. An Area2D pushes the player back slightly on contact.

**Key:** A=T B=F C=T D=T E=F

**Why:**

- A: The agent might build a solid body that stops the player.
- B: Detection reads the collision shape; the sprite is only a drawing.
- C: An area is a detection region that reports overlap and applies no response.
- D: Each element of the behaviour is named.
- E: Pushing back is a solid body's response, not an area's.

**Source:** Collider versus trigger

## MA-ch04.2

Engines use the word 'collision' for two jobs: a solid collider and a trigger. Check each statement that is true about the two terms. Each statement is worth 1 point (5 points total).

- [ ] A. A trigger reports that something entered but not that something left.
- [ ] B. Layers and masks do not affect which objects a trigger detects.
- [ ] C. A solid collider produces a collision response such as blocking, while a trigger just reports an overlap.
- [ ] D. Switching a solid collider to a trigger keeps it blocking the player and adds enter events.
- [ ] E. In Unity one collider can be solid and a trigger at the same time.

**Key:** A=F B=F C=T D=F E=F

**Why:**

- A: Triggers report leaving as well, for example body_exited in Godot.
- B: Layers and masks still decide what a trigger can detect.
- C: Response is the difference between the two.
- D: A trigger lets other colliders pass through it.
- E: A collider is either solid or a trigger, so blocking and sensing need two colliders.

**Source:** Collider versus trigger

## MA-ch04.3

A developer writes: 'Add a wall on the right edge of the room that detects when the player touches it.' The agent adds an Area2D, and the player walks out through the wall. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. The word 'wall' guarantees that the agent builds a blocking body.
- [ ] B. A wall that blocks needs a solid body such as a StaticBody2D with a collision shape.
- [ ] C. The word 'detects' asks for a detection region, while 'blocks' asks for a solid body.
- [ ] D. In Unity, enabling Is Trigger on the wall's collider makes the wall block more firmly.
- [ ] E. Adding layers to the area's mask makes the area block the player.

**Key:** A=F B=T C=T D=F E=F

**Why:**

- A: The agent built what was literally written, so the brief should say the player must be stopped.
- B: A static body supplies the blocking and a child area can supply the touch event.
- C: The instruction named only the detection role.
- D: A trigger collider lets other bodies pass through.
- E: A mask chooses what is scanned and gives no blocking.

**Source:** Collider versus trigger, say it to the agent

## MA-ch04.4

Godot's 2D physics has several node types, and the type decides who moves the body and who handles contact. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A CharacterBody2D is simulated like a RigidBody2D, so gravity needs no code.
- [ ] B. A RigidBody2D is moved by the physics simulation, so it is driven with forces or impulses.
- [ ] C. An Area2D detects overlapping bodies, can change gravity or damping inside it, and does not block.
- [ ] D. A StaticBody2D is a fixed obstacle that other bodies collide with.
- [ ] E. A CharacterBody2D detects collisions and leaves the response to code.

**Key:** A=F B=T C=T D=T E=T

**Why:**

- A: A character body has collision detection but no physics simulation.
- B: A rigid body is a dynamic body owned by the simulation.
- C: Detection and influence are the jobs of an area.
- D: Static bodies suit walls and floors.
- E: The response comes from move_and_slide or move_and_collide.

**Source:** Godot physics body types

## MA-ch04.5

Unity sorts colliders as static (a collider with no Rigidbody), dynamic (a Rigidbody with Is Kinematic off) and kinematic (a Rigidbody with Is Kinematic on). An elevator is moved by code each physics step. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A static collider is a collider that has a Rigidbody and is moved by code.
- [ ] B. A dynamic body is moved by the physics engine in response to gravity, forces and collisions.
- [ ] C. A kinematic body is moved by code and not by forces, and it can push dynamic bodies in its path.
- [ ] D. The elevator should be dynamic, because dynamic bodies are the ones moved by code.
- [ ] E. In Godot, a StaticBody2D plays the kinematic role for a platform moved by code or animation.

**Key:** A=F B=T C=T D=F E=F

**Why:**

- A: A static collider has no Rigidbody.
- B: Dynamic bodies respond to the simulation.
- C: Kinematic motion comes from outside the simulation, yet the body still acts on others.
- D: Dynamic means the simulation owns the motion; code-driven motion is kinematic.
- E: The Godot node for a code or animation driven platform is an AnimatableBody2D.

**Source:** Static, kinematic and dynamic bodies

## MA-ch04.6

An agent builds a 2D platformer player as a CharacterBody2D. In _physics_process it adds gravity to the velocity, sets horizontal velocity from input and calls move_and_slide(). Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A CharacterBody2D is simulated by the engine in the same way as a RigidBody2D.
- [ ] B. The movement belongs in _physics_process, which runs at the fixed physics rate, not in the per-frame callback.
- [ ] C. Overwriting a RigidBody2D's position each frame is the recommended way to move it.
- [ ] D. The gravity line is needed because a character body is not simulated; the code supplies it.
- [ ] E. Velocity should be multiplied by delta again before move_and_slide() is called.

**Key:** A=F B=T C=F D=T E=F

**Why:**

- A: A character body is code-driven; a rigid body is simulated.
- B: Collision movement runs in the fixed-rate physics callback.
- C: Rigid bodies are driven with forces or impulses.
- D: Nothing pulls a character body down unless the code changes its velocity.
- E: move_and_slide() applies the time step itself.

**Source:** Character body movement

## MA-ch04.7

In Godot every collision object has a collision layer and a collision mask. Check each statement that is true about the two terms. Each statement is worth 1 point (5 points total).

- [ ] A. Layer and mask are one setting seen from two sides.
- [ ] B. Changing an object's layer also changes which layers it scans.
- [ ] C. The mask is the set of layers an object scans for contacts.
- [ ] D. The layer is the set of layers an object appears in.
- [ ] E. Object A detects object B when B's layer is among the layers in A's mask.

**Key:** A=F B=F C=T D=T E=T

**Why:**

- A: They are two independent fields.
- B: Layer and mask change separately.
- C: Mask says what an object looks for.
- D: Layer says where an object can be found.
- E: Detection runs from the scanner's mask to the other object's layer.

**Source:** Collision layers versus masks

## MA-ch04.8

In the Godot editor collision layers are numbered, while in scripts collision_layer and collision_mask hold a bitmask integer. Check each statement that is true about the terms. Each statement is worth 1 point (5 points total).

- [ ] A. A mask value of 0 scans the full range of layers.
- [ ] B. Values of several layers are multiplied together to form the mask.
- [ ] C. Writing a layer number where a bit value is expected can select the wrong layer.
- [ ] D. A bitmask is an integer in which each layer has its own bit.
- [ ] E. Layer 3 has the value 3 in a script, the same number the editor shows.

**Key:** A=F B=F C=T D=T E=F

**Why:**

- A: A mask of 0 scans no layers.
- B: Values add, since each layer is a separate bit.
- C: A number mistaken for a bit value points at a different layer.
- D: A bitmask packs the layers into one integer.
- E: The script value for layer 3 is 4.

**Source:** Layer numbers versus bit values

## MA-ch04.9

Enemies should bounce off walls and the player but pass through one another. The developer tells the agent only: 'make the enemies not collide with each other'. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. In Unity, unticking the World/Enemy pair makes enemies pass through each other.
- [ ] B. In Unity the matching change is to untick the Enemy/Enemy pair in the layer collision matrix.
- [ ] C. Disabling the enemies' collision shapes meets the request.
- [ ] D. A precise instruction puts enemies on their own layer and sets their mask to scan the wall and player layers but not the enemy layer.
- [ ] E. Making enemies heavier meets the request, because mass decides whether contact is detected.

**Key:** A=F B=T C=F D=T E=F

**Why:**

- A: That change would let enemies pass through walls.
- B: That pair controls enemy-enemy contact.
- C: It also removes contact with walls and the player.
- D: Layers and masks pick which pairs interact.
- E: Mass affects the response, not detection.

**Source:** Layers and masks, say it to the agent

## MA-ch04.10

An icy floor should let the player slide, and a rubber ball should bounce. A designer tells an agent 'make the floor slippery and the ball bouncy'. Check each statement that is true about the terms. Each statement is worth 1 point (5 points total).

- [ ] A. Slippery maps to low friction and bouncy maps to high bounce, both set on a physics material.
- [ ] B. Friction and bounce are separate properties of a contact.
- [ ] C. A round collider is what makes a ball rebound.
- [ ] D. Lowering a body's mass is how to raise its bounce.
- [ ] E. A glossy render material is what makes the player slide.

**Key:** A=T B=T C=F D=F E=F

**Why:**

- A: A physics material holds surface properties such as friction and bounce.
- B: A slippery floor can have no bounce at all.
- C: Rebound comes from the bounce value of the contact, not from the outline.
- D: Mass sets how hard a body is to accelerate and is a separate property.
- E: A render material changes only how the surface is drawn.

**Source:** Physics material

## MA-ch04.11

A raycast asks the physics world what is the first thing hit by a ray from an origin in a direction for a given length. Check each statement that is true about the term. Each statement is worth 1 point (5 points total).

- [ ] A. By default Godot's ray query does not report Area nodes.
- [ ] B. A hitscan weapon, whose shot lands instantly, is usually built on a raycast.
- [ ] C. A basic ray query reports the nearest hit along its path.
- [ ] D. A ray has width, so it reports objects in a narrow cone around the line.
- [ ] E. A ray from an enemy's eyes to the player tests line of sight.

**Key:** A=T B=T C=T D=F E=T

**Why:**

- A: Areas are reported only if the query asks for them.
- B: The shot is an instant line test along the aim direction.
- C: The result describes a single first hit.
- D: A ray is an infinitely thin line.
- E: If the first hit is the player, nothing solid is in between.

**Source:** Raycast

## MA-ch04.12

A bomb should damage the enemies within 3 metres in any direction. Check each statement that is true about a shape query (overlap query) and a raycast. Each statement is worth 1 point (5 points total).

- [ ] A. A shape query returns the objects that overlap a given shape, such as a sphere.
- [ ] B. A ray covers a line, not a region.
- [ ] C. A shape query finds trigger regions and does not report solid bodies.
- [ ] D. One ray from the bomb finds the enemies in the whole area around it.
- [ ] E. A ray is used to ask who is near, and a shape query to ask what stands between two points.

**Key:** A=T B=T C=F D=F E=F

**Why:**

- A: A shape query tests a region at this moment.
- B: A ray is a single line.
- C: Shape queries test colliders in general, solid bodies included.
- D: A 3 metre region needs a shape query or many rays.
- E: The roles are swapped: a shape query finds who is near and a ray checks what is in between.

**Source:** Overlap query versus raycast

## MA-ch04.13

A small, fast bullet passes through a thin wall now and then, with continuous collision detection off. Check each statement that is true about the terms. Each statement is worth 1 point (5 points total).

- [ ] A. Tunnelling happens because a fast body's layer stops being recognised by the wall's mask.
- [ ] B. Tunnelling is a fast body passing through a thin obstacle because overlap is tested at discrete positions instead of along the path.
- [ ] C. A thicker wall can reduce tunnelling, but a fast enough body can still skip it.
- [ ] D. Continuous collision detection costs more per body, so it suits fast, small bodies.
- [ ] E. Continuous collision detection tests the path swept during a step.

**Key:** A=F B=T C=T D=T E=T

**Why:**

- A: Layers do not depend on speed.
- B: Nothing checks the space between two tested positions.
- C: Wall thickness helps, but skipping depends on the step distance.
- D: The extra cost is why it is switched on selectively.
- E: It tests the swept path, not only the end position.

**Source:** Tunnelling and continuous collision detection

## MA-ch04.14

A developer asks an agent for a crate knocked away by an explosion, a rocket that speeds up while its engine burns, and a paddle that moves at 300 px/s while a key is held. Check each statement that is true about force, impulse and velocity. Each statement is worth 1 point (5 points total).

- [ ] A. Setting a body's velocity and applying an impulse are the same operation.
- [ ] B. An impulse is an instantaneous change of momentum applied once.
- [ ] C. An impulse is a faster force that changes position directly.
- [ ] D. A force acts over time and produces acceleration.
- [ ] E. The rocket's engine is modelled as one impulse at launch.

**Key:** A=F B=T C=F D=T E=F

**Why:**

- A: Setting velocity replaces the motion, while an impulse adds to it.
- B: The explosion knock-back is a one-time impulse.
- C: Both change velocity and not position directly.
- D: Constant force means steady acceleration.
- E: Sustained thrust needs a force applied over time.

**Source:** Force, impulse and velocity

## MA-ch04.15

A designer asks an agent to 'move the platform right at 100 pixels per second' and to 'teleport the player to the checkpoint'. The player is a CharacterBody2D. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A velocity of (100, 0) and a velocity of (-100, 0) are the same velocity.
- [ ] B. A CharacterBody2D has no velocity property.
- [ ] C. Writing a body's position directly is a teleport that skips collision handling along the path.
- [ ] D. Writing position runs the same collision handling as move_and_slide().
- [ ] E. Velocity has a speed and a direction; speed is its size.

**Key:** A=F B=F C=T D=F E=T

**Why:**

- A: They have equal speed but opposite directions.
- B: move_and_slide() reads and updates a velocity property on a character body.
- C: A teleport has no sweep and no response, so a destination in a wall can embed the player.
- D: Only the move functions run collision handling.
- E: Velocity is a vector; speed is its magnitude.

**Source:** Velocity versus position

## MA-ch04.16

Collision handling has two stages: detection and response. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A body's bounciness belongs to detection.
- [ ] B. A trigger applies a blocking response after it detects an overlap.
- [ ] C. move_and_slide() stops at the first contact and returns the details, while move_and_collide() applies a sliding response.
- [ ] D. Detection finds that and where two shapes overlap, and response decides what then happens.
- [ ] E. For a RigidBody2D the developer writes the code that stops it at a wall.

**Key:** A=F B=F C=F D=T E=F

**Why:**

- A: Bounce shapes the response, the speed returned after contact.
- B: A trigger detects and applies no response.
- C: The functions are swapped: move_and_collide() stops and reports, move_and_slide() slides.
- D: The two stages are separate.
- E: The simulation supplies the response for rigid bodies.

**Source:** Collision detection versus collision response

## MA-ch04.17

A game renders at 30, 60 and 144 frames per second on three machines, and its physics runs on a fixed time step. Check each statement that is true about the terms. Each statement is worth 1 point (5 points total).

- [ ] A. The per-frame callback runs at a variable rate.
- [ ] B. A fixed time step advances the physics simulation in equal increments of game time.
- [ ] C. The engine may run zero, one or several physics steps for one rendered frame.
- [ ] D. Multiplying by delta in the per-frame callback makes collision results the same on the three machines.
- [ ] E. A variable time step gives the same jump arc on the three machines.

**Key:** A=T B=T C=T D=F E=F

**Why:**

- A: It runs once per rendered frame, and frame times vary.
- B: The step size is constant regardless of frame rate.
- C: Physics catches up or waits to keep its own clock steady.
- D: Delta fixes speed but not collision tests, jump arcs or contact timing.
- E: Different step sizes give different integration results.

**Source:** Fixed time step

## MA-ch04.18

A melee game team uses three terms: hitbox, hurtbox and body collider. Check each statement that is true about the melee convention. Each statement is worth 1 point (5 points total).

- [ ] A. A body collider is the solid shape that blocks movement.
- [ ] B. The sword carries the hurtbox and the enemy carries the hitbox.
- [ ] C. Hitboxes and hurtboxes are normally solid colliders.
- [ ] D. A hitbox is a region that deals damage during an attack.
- [ ] E. A hurtbox is a region on a character that receives damage.

**Key:** A=T B=F C=F D=T E=T

**Why:**

- A: Blocking is the body collider's job.
- B: The roles are swapped: the sword carries the hitbox.
- C: Both are detection regions that report overlap and do not block.
- D: The hitbox is the attacking region.
- E: The hurtbox is the receiving region.

**Source:** Hitbox, hurtbox and body collider

## MA-ch04.19

A developer briefs an agent on a sword swing that should damage a given enemy once. Check each statement that is true about the setup. Each statement is worth 1 point (5 points total).

- [ ] A. The hitbox should be active during the frames of the swing in which the blade can hurt.
- [ ] B. The sword's hitbox mask should scan the player's own layer so it detects the wielder.
- [ ] C. Once-per-swing damage is automatic because an overlap is a single event.
- [ ] D. The hurtbox can sit on a layer separate from the body collider's layer.
- [ ] E. A constantly active hitbox is fine, because overlap is just detection.

**Key:** A=T B=F C=F D=T E=F

**Why:**

- A: The active frames limit when damage can occur.
- B: The mask should scan the enemies' hurtbox layer and not the player's own.
- C: Overlap lasts several steps, so the swing needs a record of targets already hit.
- D: Separate layers let masks choose which shape is scanned.
- E: An always-on hitbox would damage things outside the attack.

**Source:** Hitbox and hurtbox setup

## MA-ch04.20

A platformer has ledges the player can jump up through from below, then stand on. In Godot 2D this is a collision shape with one-way collision enabled. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A one-way platform is a solid collider that blocks from one side, normally the top.
- [ ] B. A one-way platform is a trigger that lifts the player onto it.
- [ ] C. A ledge on a layer that the player's mask does not scan behaves the same as a one-way platform.
- [ ] D. One-way collision works on a shape that belongs to an Area2D.
- [ ] E. Dropping through can be done by briefly turning off collision with that ledge.

**Key:** A=T B=F C=F D=F E=T

**Why:**

- A: It is solid from one direction and open from the other.
- B: Triggers neither block nor lift.
- C: The player would also pass through from above and not stand on it.
- D: One-way collision has no effect under an Area2D.
- E: A short pause lets the player fall past it.

**Source:** One-way platform

## MA-ch04.21

Lava should hurt the player every 0.5 s while the player stands in it. The agent built an Area2D whose body_entered handler subtracts 1 health, and the player loses health only once. Check each statement that is true about the terms. Each statement is worth 1 point (5 points total).

- [ ] A. An event reports a change, while a query reports the current state.
- [ ] B. body_exited fires repeatedly while the player stays inside.
- [ ] C. A timer that asks which bodies currently overlap the lava gives repeated damage.
- [ ] D. body_entered is an enter event that fires once when an overlap begins.
- [ ] E. Making the lava's shape bigger produces repeated enter events.

**Key:** A=T B=F C=T D=T E=F

**Why:**

- A: Which bodies overlap now is a query, not an event.
- B: An exit event fires once when the player leaves.
- C: Polling the overlap list repeats the check while the overlap lasts.
- D: Standing still inside produces no further enter events.
- E: Size does not change the fact that entry is a single event.

**Source:** Enter events versus current overlaps

## MA-ch04.22

A player is invulnerable for 3 seconds. An enemy that was already overlapping the player when invulnerability ends does not hurt the player until it leaves and re-enters. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Making the detection shape larger fixes the missed damage.
- [ ] B. A fix is to query the current overlapping bodies when invulnerability ends.
- [ ] C. An enter handler is a query of the current overlaps.
- [ ] D. No new enter event fires when invulnerability ends, so the earlier overlap stays unreported.
- [ ] E. Godot's body_entered signal also works as a stay event.

**Key:** A=F B=T C=F D=T E=F

**Why:**

- A: Shape size does not create a new event.
- B: A query reads the current state.
- C: A handler reacts to an event and does not read the current state.
- D: An enter event is a change, and nothing changed.
- E: body_entered fires once at the start of an overlap.

**Source:** Enter events versus current overlaps

## MA-ch04.23

Three engines name the same idea differently: a region that reports objects inside it without blocking them. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. In Godot this is an Area2D or Area3D.
- [ ] B. In the three engines the region detects through its drawn mesh or sprite.
- [ ] C. In Unreal this is a collision component whose response to the other object's type is Overlap.
- [ ] D. In Godot an area detects a body when the body's layer is among the layers in the area's mask.
- [ ] E. In Unity this is a collider with Is Trigger enabled.

**Key:** A=T B=F C=T D=T E=T

**Why:**

- A: An area is Godot's non-blocking detection region.
- B: Detection uses collision shapes, not drawings.
- C: Overlap is Unreal's non-blocking response.
- D: Layer says where an object appears and mask says what is scanned.
- E: Is Trigger turns a collider into a detection region.

**Source:** Trigger across engines

## MA-ch04.24

A developer tells an agent: 'only let the player jump when touching the ground'. The player is a CharacterBody2D. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Floor, wall and ceiling are different classes of contact surface.
- [ ] B. is_on_floor() reflects the result of the most recent move_and_slide() call.
- [ ] C. An Area2D at the feet detects solid ground when its mask scans the ground's layer.
- [ ] D. is_on_floor() is a plain overlap test that is true when the body is inside a floor shape.
- [ ] E. An empty ray result from the feet means the player stands on the ground.

**Key:** A=T B=T C=T D=F E=F

**Why:**

- A: 'Touching' is ambiguous, so the brief should say the contact must be a floor.
- B: It is updated by the movement call and is not live.
- C: Areas report only bodies on layers in their mask.
- D: It classifies contact by surface direction and is not an overlap test.
- E: An empty result means the ray hit nothing within its length.

**Source:** Ground check, say it to the agent

## MA-ch04.25

A developer swaps a character's sprite for a larger drawing, and afterwards the arms poke into walls. Check each statement that is true about the terms. Each statement is worth 1 point (5 points total).

- [ ] A. A debug view that draws collision shapes at runtime exposes the mismatch.
- [ ] B. Replacing the sprite resizes the collision shape.
- [ ] C. Capsule shapes are costly to test and so are avoided for characters.
- [ ] D. The physics engine reads collision shapes, not the picture.
- [ ] E. The engine leaves the transparent pixels of a sprite out of the collision.

**Key:** A=T B=F C=F D=T E=F

**Why:**

- A: Seeing the shape over the art shows where they disagree.
- B: The shape is a separate node and keeps its size.
- C: Primitives such as capsules are cheap to test.
- D: Collision comes from shapes.
- E: Transparency is a rendering property and does not affect collision.

**Source:** Collision shape versus art

## MA-ch04.26

A developer gives an agent: 'Add a collider to the shield pickup so that the player can collide with it and get the shield.' Check each statement that is true about wording the request with exact terms. Each statement is worth 1 point (5 points total).

- [ ] A. 'Walk through it and collect it' asks for a detection region.
- [ ] B. 'It should not block movement' is a useful clause in the brief.
- [ ] C. A sprite alone is enough for a detection region to find the player.
- [ ] D. 'Stop the player at it' asks for a solid body.
- [ ] E. A good observable result is that the player passes through and the shield state is set once.

**Key:** A=T B=T C=F D=T E=T

**Why:**

- A: A pickup is an area or trigger.
- B: The word 'collide' alone leaves blocking open.
- C: A detection region needs a collision shape.
- D: Blocking is a solid body's response.
- E: The result can be checked in a test.

**Source:** Say it to the agent: collider versus trigger

## MA-ch04.27

A teammate says 'collider, trigger and raycast are all just ways of finding out that two things touched'. Check each statement that is true in correction. Each statement is worth 1 point (5 points total).

- [ ] A. A raycast blocks things in its path.
- [ ] B. Collider, trigger and raycast are three names for one detection tool.
- [ ] C. Walls and floors are fitting uses of a solid collider.
- [ ] D. A pickup or damage zone is a fitting use of a raycast.
- [ ] E. A raycast is a query along a line, not a body in the world.

**Key:** A=F B=F C=T D=F E=T

**Why:**

- A: A ray does not block, push or notify.
- B: They differ in what they do and what they return.
- C: A collider produces a response such as blocking.
- D: A pickup or damage zone is a trigger; a ray suits line of sight or a hitscan shot.
- E: A ray asks a question at one moment.

**Source:** Collider, trigger and raycast

## MA-ch04.28

A 2D game has walls, a player, enemies, bullets and coins, and each kind of object must interact with only some of the others. Check each statement that is true about layers and masks in Godot. Each statement is worth 1 point (5 points total).

- [ ] A. Detection runs from the scanner's mask to the other object's layer.
- [ ] B. Giving each kind of object its own layer lets masks choose which pairs interact.
- [ ] C. A function that takes layer numbers avoids the bit-value mistakes of writing the integer directly.
- [ ] D. With each object on the default layer and scanning it, each object collides with each other object.
- [ ] E. The default layer already separates walls from enemies.

**Key:** A=T B=T C=T D=T E=F

**Why:**

- A: A scans B only if B's layer is in A's mask.
- B: Separate layers are the first step in the design.
- C: Layer numbers are converted to bits by the function.
- D: That is why the default is unsuitable for selective interaction.
- E: The default puts them on one layer.

**Source:** Layers and masks design

## MA-ch04.29

A jump written in the per-frame callback reaches a different height on a 30 frames-per-second machine than on a 144 frames-per-second machine. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A constant step makes behaviour depend on the frame rate.
- [ ] B. A long variable step lets a fast body travel farther than a thin wall is thick in one step.
- [ ] C. 'Make the movement frame-rate independent' names the callback.
- [ ] D. 'Apply gravity and call move_and_slide() inside _physics_process using the physics delta' names the callback.
- [ ] E. The per-frame callback is the right place for movement that collides.

**Key:** A=F B=T C=F D=T E=F

**Why:**

- A: A constant step makes behaviour reproducible and testable.
- B: Long steps let fast bodies skip thin obstacles.
- C: It states a goal without naming the callback.
- D: It names the callback and the delta to use.
- E: Collision movement belongs in the fixed-rate callback.

**Source:** Fixed time step, say it to the agent

## MA-ch04.30

A bullet is a RigidBody2D that sometimes tunnels through a thin wall. Check each statement that is true about remedies and what each costs. Each statement is worth 1 point (5 points total).

- [ ] A. A hitscan design still needs a physical bullet body.
- [ ] B. A higher physics rate is a remedy that costs more for the whole simulation.
- [ ] C. Continuous collision detection is a remedy that costs more per body.
- [ ] D. Tunnelling is guaranteed for a fast body.
- [ ] E. A raycast from the previous position to the new position is a remedy that needs more code.

**Key:** A=F B=T C=T D=F E=T

**Why:**

- A: Hitscan has no travelling bullet.
- B: More physics steps per second shrink the distance between tested positions, at a cost to the whole simulation.
- C: It tests the swept path of each body.
- D: It depends on where the tested positions fall relative to the wall.
- E: The ray checks the path between positions.

**Source:** Tunnelling remedies

## MA-ch04.31

A developer must brief an agent on a 2D platformer by choosing a body type for each object. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. An elevator moved by code is a kinematic body such as Godot's AnimatableBody2D.
- [ ] B. The player is a character body such as Godot's CharacterBody2D.
- [ ] C. A pushable crate is a static body.
- [ ] D. The level floor is a static body.
- [ ] E. A health pickup is a trigger region such as an Area2D that does not block.

**Key:** A=T B=T C=F D=T E=T

**Why:**

- A: A kinematic body is moved by code or animation and still pushes others.
- B: A character body is code-driven with collision detection and no simulation.
- C: A pushable crate is a dynamic (rigid) body.
- D: A floor is a fixed obstacle.
- E: A pickup detects the player and does not block.

**Source:** Static, kinematic, dynamic and character bodies

## MA-ch04.32

A developer asks for a crate knocked away by an explosion, a rocket that accelerates while its engine burns, and a character that moves at 200 px/s while a key is held. Check each statement that is true about choosing force, impulse or setting velocity. Each statement is worth 1 point (5 points total).

- [ ] A. The rocket's thrust is a force applied on each physics step while the engine burns.
- [ ] B. The explosion knock-back is a force applied on each physics step.
- [ ] C. The 200 px/s character on a character body is moved by setting its velocity.
- [ ] D. Impulse is divided by velocity to give the change in mass.
- [ ] E. Applying an impulse once per rendered frame makes the total push depend on the frame rate.

**Key:** A=T B=F C=T D=F E=T

**Why:**

- A: Sustained thrust is a force over time.
- B: A one-time knock-back is an impulse, not a continuing force.
- C: The code owns a character body's motion, so it sets velocity.
- D: The change in velocity is the impulse divided by mass.
- E: Frames per second differ between machines, so the number of impulses per second differs.

**Source:** Force, impulse and velocity choices
