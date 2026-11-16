# Scenes, Collision, and Physics in Godot

## BOPEN · Opening

CSYE seventy-two seventy, Building Virtual Environments. Scenes, Collision, and Physics in Godot. Learn to organize objects, control interactions, and test motion.

## BIDEA · Opening

Hallo. This is Liam, in for Bear, for CSYE seventy-two seventy, Building Virtual Environments. A game object has three different responsibilities. Separating organization, collision, and motion gives us a better way to find bugs.

## BDEFS · Opening

Five terms. A node provides a capability. An instance is a live copy of a saved scene. A shape defines collision geometry. Velocity is movement rate with a direction. A tick is one physics update step.

## BACT1 · Compose a Game

Compose a Game.

## B01 · Compose a Game

A scene organizes an object. Collision defines its boundary and filtering. A movement policy decides what happens over time. Keep those responsibilities separate, and a missing pickup becomes a testable question instead of a mysterious physics bug.

## B02 · Compose a Game

This lab ran in Godot four point seven point two. Match your documentation and project settings to the installed engine. A saved version is reproducible context; calling something the latest release is a claim that soon expires.

## B03 · Compose a Game

A scene is a reusable node tree, usually saved as a text scene file. One root owns this small example. A complete level, a player, a coin, and a menu can each be scenes.

## B04 · Compose a Game

Node itself has no position. Two D and three D spatial nodes provide transforms. Here a child keeps its local offset when its parent moves. Top-level settings and different node types can change that relationship.

## B05 · Compose a Game

PackedScene holds a saved definition. Instantiate creates a live copy. These two copies have different positions, while resources inside them may still be shared. Independent nodes do not automatically mean independent materials or shapes.

## B06 · Compose a Game

A level has a player and coins: composition. An inherited scene specializes a base scene: a variant relationship. Prefer exported settings over repeatedly exposing editable children. Reuse should preserve a clear boundary around the object.

## B07 · Compose a Game

Let the level connect a coin's collected signal to the score update. The coin reports what happened without locating a distant parent. Unique names help inside a scene; persistent state can live in an autoload.

## B08 · Compose a Game

A question block remembers whether it was used, so give it a small scene and an explicit state. Animate its visual child for a cosmetic bump. If the solid surface must push something, use an animatable body.

## B09 · Compose a Game

Keep actors, blocks, levels, interface, and layer definitions organized by responsibility. Test scenes in isolation. When editing text scenes, preserve resource references and existing identifiers; letting the engine save a PackedScene avoids hand-copying node identifiers.

## BACT2 · Decide What Interacts

Decide What Interacts.

## B10 · Decide What Interacts

A static body resists impacts. It can represent a wall or provide conveyor velocity without moving its geometry. A platform following a path belongs on an animatable body, with its movement synchronized to physics.

## B11 · Decide What Interacts

A rigid body asks the solver to calculate motion. Forces sustain a push; an impulse produces a one-time change. For this isolated example, mass two and impulse one hundred twenty predict a velocity change of sixty.

## B12 · Decide What Interacts

A character body gives your code collision and sliding helpers. It does not supply your game's gravity or friction policy. Set velocity in pixels per second, then call move and slide once in the physics callback.

## B13 · Decide What Interacts

An area detects overlaps without blocking the player. It can also change local gravity or damping. Body-entered is for bodies; area-entered is for areas. Detection needs monitoring and a mask that includes the target's layer.

## B14 · Decide What Interacts

Artwork is not collision geometry. A rectangle gives crisp platformer edges; a capsule gives smoother rounded contacts. Resize the shape resource instead of scaling the physics node. Keep collision shapes as direct children of their body.

## B15 · Decide What Interacts

Name categories before assigning bits: world, one-way platforms, player, enemy, pickup, hazard, and debris. The player scans world and platforms. The coin scans player. Debris scans world. This table makes deliberate exclusions visible.

## B16 · Decide What Interacts

The layer-value methods take one-based layer numbers. Layer three corresponds to bit value four. A raw mask combines bits; the Inspector displays named categories. Keep one constants file synchronized with the project layer names.

## B17 · Decide What Interacts

Our coin detected the player even though the player did not scan pickups. Removing the area's mask prevented detection. That is a directed area query. Do not turn it into a universal rule that every body pair needs reciprocal masks.

## B18 · Decide What Interacts

Two nodes can share the same Shape resource. Resize that shared resource and both boundaries change. Duplicate the resource when you need one independent boundary. This is resource ownership, separate from whether the nodes were instanced separately.

## BACT3 · Design the Motion

Design the Motion.

## B19 · Design the Motion

Move and slide consumes the velocity property and applies the timestep internally. Move and collide takes a displacement, often velocity times delta. Mixing these contracts is a common source of tiny movement or wildly incorrect speed.

## B20 · Design the Motion

Choose jump height and time to the apex. Under constant upward-phase acceleration, gravity is twice the height divided by time squared. Initial upward speed is gravity times apex time. Godot's downward-positive axis makes jump velocity negative.

## B21 · Design the Motion

The reference controller computes rise gravity from those design values. It increases gravity while falling and clamps fall speed. That creates a deliberate game feel. These parameters describe a policy, not an attempt at a universal realistic jump.

## B22 · Design the Motion

Horizontal speed approaches a target rather than jumping instantly. Ground acceleration, braking, and air acceleration are separate choices. Multiply acceleration by delta when updating velocity; keep the final movement call responsible for displacement.

## B23 · Design the Motion

Coyote time permits a jump shortly after leaving a ledge. Jump buffering remembers a recent press before landing. They are different timer windows. Consume both when a jump starts so a held permission cannot launch another jump.

## B24 · Design the Motion

Releasing jump early reduces upward speed for a shorter hop. A stomp bounce sets a new upward velocity. If you author gravity yourself, area gravity overrides do not automatically replace that policy; decide how local gravity should contribute.

## B25 · Design the Motion

Up direction and the maximum floor angle classify surfaces. Floor snap helps follow downward slopes; grounded and floating modes serve different movement styles. Read floor state after movement for the current result, or deliberately use the previous result for coyote time.

## B26 · Design the Motion

Move an animatable platform on physics ticks and test inherited velocity when the character leaves. Characters can affect other bodies, but a deliberate crate-pushing policy may use impulses. That policy only runs when the character actually collides with the crate.

## B27 · Design the Motion

The continuous formula is a design target. A fixed-step controller samples it. Here the measured apex is slightly above seventy-two pixels, within the declared ten-percent tolerance. Plot the measured samples before changing parameters to chase a feeling.

## BACT4 · Turn Contact into Gameplay

Turn Contact into Gameplay.

## B28 · Turn Contact into Gameplay

Physics overlap callbacks can run while queries are being flushed. Defer changes such as disabling a shape or monitoring. The coin sets a synchronous claimed flag first, then schedules the physics change and emits its value.

## B29 · Turn Contact into Gameplay

We invoked the collection path again after the first award. The count remained one. Deferring monitoring alone leaves a window before that change applies. A small immediate latch makes the gameplay promise explicit.

## B30 · Turn Contact into Gameplay

A falling player above an enemy can suggest a stomp, but comparing origins alone is a heuristic. Feet-aligned pivots help interpretation. A top sensor or contact-normal test, plus side and corner tests, makes the intended rule clearer.

## B31 · Turn Contact into Gameplay

This example uses a separate top sensor for a falling player's stomp. A side sensor requests damage. The defeated latch prevents repeated events, and sensor changes are deferred. Simultaneous corner contacts still need an explicit priority policy.

## B32 · Turn Contact into Gameplay

A TileSet owns tile collision polygons and their physics categories. TileMapLayer places cells and builds the bodies. A stateful block is often easier as its own scene; repeated terrain suits tiles. Keep their responsibilities distinct.

## B33 · Turn Contact into Gameplay

This collision touched cell three, zero. The body's resource identifier mapped to quadrant zero, zero. Physics chunking groups compatible tile geometry, so the body identifier does not uniquely identify the struck cell. Disabling chunking changes that tradeoff.

## B34 · Turn Contact into Gameplay

Probe slightly into the hit surface, against its outward normal. Convert that world point into the tile layer's local coordinates, then map it to a cell. The probe distance is example-specific; test transformed layers and contacts near cell boundaries.

## B35 · Turn Contact into Gameplay

The checked four point seven shape reference exposes a one-way direction. The default points down in two D coordinates. This is a body collision feature, not an area's overlap policy. Test tilted platforms rather than assuming older tutorial behavior.

## B36 · Turn Contact into Gameplay

Separate one-way surfaces onto their own layer, then temporarily stop scanning it. A short physics timer is a simple drop-through policy. Before restoring collision in a real game, ensure the character has cleared the platform and handle overlapping requests.

## BACT5 · Make Time and Tests Explicit

Make Time and Tests Explicit.

## B37 · Make Time and Tests Explicit

Physics ticks and rendered frames are different clocks. The default physics rate is sixty ticks per second. Run collision-based motion in physics callbacks and use delta. Correctly scaled render-frame motion still does not give the same collision scheduling.

## B38 · Make Time and Tests Explicit

Speed divided by tick rate estimates travel per tick. It is not a collision theorem. Our character's swept movement detected a four-pixel floor across a requested three-hundred-pixel displacement. Method, shape, direction, and backend all matter.

## B39 · Make Time and Tests Explicit

For fast rigid bodies, continuous collision detection can reduce tunneling. Two D provides ray and shape modes; three D exposes its own settings. Also consider thicker collision geometry and a higher physics rate. None is a universal prevention guarantee.

## B40 · Make Time and Tests Explicit

Interpolation draws intermediate poses between physics states. It smooths presentation without simulating extra contacts. Temporarily testing at ten ticks per second makes mistakes obvious. Restore the intended rate and test pixel snapping and camera behavior together.

## B41 · Make Time and Tests Explicit

A respawn is a discontinuity. Set the new position, clear unwanted velocity, then reset physics interpolation. For a rigid body, change the simulated state through its integration callback. Frequent transform writes can fight the solver.

## B42 · Make Time and Tests Explicit

A fixed timestep improves consistency, but it is not a promise of identical physics across runs, devices, or backends. Grade documented structure and behavior within tolerances. Exact replay requirements need a separate determinism design and validation plan.

## B43 · Make Time and Tests Explicit

A missed coin suggests filtering. An offset boundary suggests scale or a shared resource. A wrong tile suggests contact lookup. A slope flicker suggests movement order or snap. Treat each as a hypothesis, then change one variable and rerun.

## B44 · Make Time and Tests Explicit

The lab ran real physics checks and captured real engine output. Those records cover specific setups. They do not prove good controls, all corner contacts, cross-device stability, or moving-platform behavior. Read diagnostics as well as the process exit code.

## B45 · Make Time and Tests Explicit

For this jump, ten percent means a band around the design height. A point inside the band passes this measurement; it does not validate every movement rule. Keep structural checks, numerical checks, and a human playtest as separate evidence.

## BACT6 · Transfer and Verify

Transfer and Verify.

## B46 · Transfer and Verify

Godot's two D and three D physics are separate systems. Jolt is now built into Godot and is the default for new projects in the checked documentation. Existing projects keep their selected backend; inspect the setting before interpreting behavior.

## B46A · Transfer and Verify

The four point seven migration notes change Jolt world-boundary distance signs, soft-body mass and stiffness behavior, and area overlap reporting for soft bodies. These are backend-specific migration checks; they do not rewrite the two D platformer.

## B47 · Transfer and Verify

The same responsibilities transfer to three D nodes. Start with boxes, spheres, or capsules. Convex shapes suit movable objects; a few convex pieces can approximate a complex outline. Concave triangle collision is generally for static environments and costs more.

## B48 · Transfer and Verify

Review generated code against the chosen release. Godot three's kinematic body, instance method, and movement signature differ from Godot four. Check annotation, await, signal connection, scene-change, and one-based collision APIs too. Confident syntax is not evidence.

## B49 · Transfer and Verify

To teach simulation alongside character kinematics, add debris or a crate. Spawn a rigid body, apply one impulse, let it sleep when settled, and remove it when no longer needed. Keep its layer policy separate from the player's.

## B50 · Transfer and Verify

Make the interaction matrix a deliverable. Add the new object, name the categories it scans, and explain one interaction you excluded. If crates should block the player, update both the design and the relevant filtering; our debris deliberately does not.

## B51 · Transfer and Verify

Build a test room with a player, floor, falling crate, moving platform, and collectible. Verify landing, contact, platform carrying, and a nonblocking pickup. Then remove the pickup mask and predict the failure. Our captured crate is one tested piece of that exercise.

## B52 · Transfer and Verify

Write the engine version, scene boundaries, named layers, movement callback, and test commands into the repository conventions. These are project policies, not universal laws. Require the agent to report what ran and what still needs a playtest.

## B53 · Transfer and Verify

Before an agent extends reference code, inspect the seed for old APIs, scaled collision nodes, hard-coded parent paths, and movement outside physics callbacks. Static searches are leads. A clean search does not prove behavior, and we have not audited an unseen course game.

## B54 · Transfer and Verify

Use the documentation matching your engine, beginning with nodes and scenes, physics introduction, and the character-body reference. Keep the runnable lab beside those pages. Predict an outcome, run one controlled test, and use the evidence to revise your explanation.

## BVDT · Closing

Let's recap with Claude. For CSYE seventy-two seventy, Building Virtual Environments. Compose reusable scenes with clear ownership. Choose body types, boundaries, and filtering deliberately. Design character motion and measure the result. Turn contacts into gameplay with explicit state and signals. Separate physics ticks, presentation, and evidence limits. Pin the version and test the interaction you intend.

## BHTF · Closing

Help me build a Godot four test room with a character, floor, rigid crate, moving platform, and coin. State the engine version. Provide reusable scenes, a named collision matrix, and physics-tick movement. Predict what changes when the coin mask is cleared. Test the jump against a declared height tolerance, prevent duplicate collection, and distinguish automated evidence from checks that need a human playtest.

## BOUT · Closing

Scenes, Collision, and Physics in Godot. At Nik Bear Brown.
