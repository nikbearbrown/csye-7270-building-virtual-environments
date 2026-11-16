# Character Motion and Rigid-Body Physics in Godot

## BOPEN · Opening

CSYE seventy-two seventy, Building Virtual Environments. Character Motion and Rigid-Body Physics in Godot. Design motion, let the solver work, and measure the result.

## BIDEA · Opening

Hallo. This is Liam, in for Bear. A character jump is a movement policy you design. A falling crate asks the solver to handle motion. Mixing those responsibilities makes both harder to tune. We will choose an owner for every motion.

## BDEFS · Opening

Velocity. Movement rate and direction. Acceleration. Change in velocity over time. Tick. One physics update step. Impulse. A one-time momentum change.

## BACT1 · Who Owns the Motion?

Who Owns the Motion?

## B01 · Who Owns the Motion?

A scene organizes an object. Collision defines its boundary and filtering. A movement policy decides what happens over time. Keep those responsibilities separate, and a missing pickup becomes a testable question instead of a mysterious physics bug.

## B19 · Who Owns the Motion?

Move and slide consumes the velocity property and applies the timestep internally. Move and collide takes a displacement, often velocity times delta. Mixing these contracts is a common source of tiny movement or wildly incorrect speed.

## B10 · Who Owns the Motion?

A static body resists impacts. It can represent a wall or provide conveyor velocity without moving its geometry. A platform following a path belongs on an animatable body, with its movement synchronized to physics.

## B12 · Who Owns the Motion?

A character body gives your code collision and sliding helpers. It does not supply your game's gravity or friction policy. Set velocity in pixels per second, then call move and slide once in the physics callback.

## BACT2 · Design a Character Jump

Design a Character Jump.

## B20 · Design a Character Jump

Choose jump height and time to the apex. Under constant upward-phase acceleration, gravity is twice the height divided by time squared. Initial upward speed is gravity times apex time. Godot's downward-positive axis makes jump velocity negative.

## B21 · Design a Character Jump

The reference controller computes rise gravity from those design values. It increases gravity while falling and clamps fall speed. That creates a deliberate game feel. These parameters describe a policy, not an attempt at a universal realistic jump.

## B22 · Design a Character Jump

Horizontal speed approaches a target rather than jumping instantly. Ground acceleration, braking, and air acceleration are separate choices. Multiply acceleration by delta when updating velocity; keep the final movement call responsible for displacement.

## B23 · Design a Character Jump

Coyote time permits a jump shortly after leaving a ledge. Jump buffering remembers a recent press before landing. They are different timer windows. Consume both when a jump starts so a held permission cannot launch another jump.

## B24 · Design a Character Jump

Releasing jump early reduces upward speed for a shorter hop. A stomp bounce sets a new upward velocity. If you author gravity yourself, area gravity overrides do not automatically replace that policy; decide how local gravity should contribute.

## B25 · Design a Character Jump

Up direction and the maximum floor angle classify surfaces. Floor snap helps follow downward slopes; grounded and floating modes serve different movement styles. Read floor state after movement for the current result, or deliberately use the previous result for coyote time.

## B27 · Design a Character Jump

The continuous formula is a design target. A fixed-step controller samples it. Here the measured apex is slightly above seventy-two pixels, within the declared ten-percent tolerance. Plot the measured samples before changing parameters to chase a feeling.

## BACT3 · Let the Solver Work

Let the Solver Work.

## B11 · Let the Solver Work

A rigid body asks the solver to calculate motion. Forces sustain a push; an impulse produces a one-time change. For this isolated example, mass two and impulse one hundred twenty predict a velocity change of sixty.

## BP01 · Let the Solver Work

A force acts over time. An impulse represents a one-time momentum change. With the same impulse, doubling mass halves the ideal velocity change. Do not repeatedly apply a jump impulse every rendered frame; that changes the intended event into repeated pushes.

## BP02 · Let the Solver Work

A rigid body can collide even when your script receives no contact signal. For body entered reporting, enable contact monitoring and allow enough reported contacts. Our crate fixture sets both and observes a floor contact. Reporting and physical response are separate concerns.

## B26 · Let the Solver Work

Move an animatable platform on physics ticks and test inherited velocity when the character leaves. Characters can affect other bodies, but a deliberate crate-pushing policy may use impulses. That policy only runs when the character actually collides with the crate.

## B49 · Let the Solver Work

To teach simulation alongside character kinematics, add debris or a crate. Spawn a rigid body, apply one impulse, let it sleep when settled, and remove it when no longer needed. Keep its layer policy separate from the player's.

## B51 · Let the Solver Work

Build a test room with a player, floor, falling crate, moving platform, and collectible. Verify landing, contact, platform carrying, and a nonblocking pickup. Then remove the pickup mask and predict the failure. Our captured crate is one tested piece of that exercise.

## BACT4 · Time, Presentation, and Evidence

Time, Presentation, and Evidence.

## B37 · Time, Presentation, and Evidence

Physics ticks and rendered frames are different clocks. The default physics rate is sixty ticks per second. Run collision-based motion in physics callbacks and use delta. Correctly scaled render-frame motion still does not give the same collision scheduling.

## B38 · Time, Presentation, and Evidence

Speed divided by tick rate estimates travel per tick. It is not a collision theorem. Our character's swept movement detected a four-pixel floor across a requested three-hundred-pixel displacement. Method, shape, direction, and backend all matter.

## B39 · Time, Presentation, and Evidence

For fast rigid bodies, continuous collision detection can reduce tunneling. Two D provides ray and shape modes; three D exposes its own settings. Also consider thicker collision geometry and a higher physics rate. None is a universal prevention guarantee.

## B40 · Time, Presentation, and Evidence

Interpolation draws intermediate poses between physics states. It smooths presentation without simulating extra contacts. Temporarily testing at ten ticks per second makes mistakes obvious. Restore the intended rate and test pixel snapping and camera behavior together.

## B41 · Time, Presentation, and Evidence

A respawn is a discontinuity. Set the new position, clear unwanted velocity, then reset physics interpolation. For a rigid body, change the simulated state through its integration callback. Frequent transform writes can fight the solver.

## B42 · Time, Presentation, and Evidence

A fixed timestep improves consistency, but it is not a promise of identical physics across runs, devices, or backends. Grade documented structure and behavior within tolerances. Exact replay requirements need a separate determinism design and validation plan.

## B44 · Time, Presentation, and Evidence

The lab ran real physics checks and captured real engine output. Those records cover specific setups. They do not prove good controls, all corner contacts, cross-device stability, or moving-platform behavior. Read diagnostics as well as the process exit code.

## B45 · Time, Presentation, and Evidence

For this jump, ten percent means a band around the design height. A point inside the band passes this measurement; it does not validate every movement rule. Keep structural checks, numerical checks, and a human playtest as separate evidence.

## B46 · Time, Presentation, and Evidence

Godot's two D and three D physics are separate systems. Jolt is now built into Godot and is the default for new projects in the checked documentation. Existing projects keep their selected backend; inspect the setting before interpreting behavior.

## B46A · Time, Presentation, and Evidence

The four point seven migration notes change Jolt world-boundary distance signs, soft-body mass and stiffness behavior, and area overlap reporting for soft bodies. These are backend-specific migration checks; they do not rewrite the two D platformer.

## BVDT · Closing

Let's recap with Claude. For CSYE seventy-two seventy, Building Virtual Environments. Choose whether code or the solver owns the motion. A character jump starts with design values and measured behavior. Rigid simulation needs deliberate forces and contact reporting. Fixed ticks, presentation, and numerical evidence answer different questions.

## BHTF · Closing

Help me build a Godot four physics test room with a character jump, a falling rigid crate, and an animatable platform. Choose a jump height and apex time, derive the upward acceleration, then measure the resulting height within a declared tolerance. Use physics callbacks correctly, compare an impulse with a sustained force, and list platform, interpolation, and device checks still requiring a playtest.

## BOUT · Closing

Character Motion and Rigid-Body Physics in Godot. At Nik Bear Brown.
