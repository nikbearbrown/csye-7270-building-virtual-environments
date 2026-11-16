# Collision Shapes, Layers, and Masks in Godot

## BOPEN · Opening

CSYE seventy-two seventy, Building Virtual Environments. Collision Shapes, Layers, and Masks in Godot. Choose boundaries and filtering that match the intended interaction.

## BIDEA · Opening

Hallo. This is Liam, in for Bear. A visible wall can have the wrong boundary, and a correctly drawn pickup can scan the wrong category. We will separate geometry, body roles, and filtering so each failure has a test.

## BDEFS · Opening

Shape. Geometry used for contact. Body. A collision object with a role. Layer. A membership category. Mask. Categories the object scans.

## BACT1 · Geometry and Body Roles

Geometry and Body Roles.

## B14 · Geometry and Body Roles

Artwork is not collision geometry. A rectangle gives crisp platformer edges; a capsule gives smoother rounded contacts. Resize the shape resource instead of scaling the physics node. Keep collision shapes as direct children of their body.

## B10 · Geometry and Body Roles

A static body resists impacts. It can represent a wall or provide conveyor velocity without moving its geometry. A platform following a path belongs on an animatable body, with its movement synchronized to physics.

## B11 · Geometry and Body Roles

A rigid body asks the solver to calculate motion. Forces sustain a push; an impulse produces a one-time change. For this isolated example, mass two and impulse one hundred twenty predict a velocity change of sixty.

## B12 · Geometry and Body Roles

A character body gives your code collision and sliding helpers. It does not supply your game's gravity or friction policy. Set velocity in pixels per second, then call move and slide once in the physics callback.

## BACT2 · Who Can Interact?

Who Can Interact?

## B15 · Who Can Interact?

Name categories before assigning bits: world, one-way platforms, player, enemy, pickup, hazard, and debris. The player scans world and platforms. The coin scans player. Debris scans world. This table makes deliberate exclusions visible.

## B16 · Who Can Interact?

The layer-value methods take one-based layer numbers. Layer three corresponds to bit value four. A raw mask combines bits; the Inspector displays named categories. Keep one constants file synchronized with the project layer names.

## B17 · Who Can Interact?

Our coin detected the player even though the player did not scan pickups. Removing the area's mask prevented detection. That is a directed area query. Do not turn it into a universal rule that every body pair needs reciprocal masks.

## B18 · Who Can Interact?

Two nodes can share the same Shape resource. Resize that shared resource and both boundaries change. Duplicate the resource when you need one independent boundary. This is resource ownership, separate from whether the nodes were instanced separately.

## BT11 · Who Can Interact?

This door has a narrow solid panel inside a larger approach sensor. The sensor can notice the player before the player reaches the panel. Detection requests an interaction; it does not automatically authorize opening. The locked setting remains a separate gameplay rule.

## BACT3 · Tiles and One-Way Surfaces

Tiles and One-Way Surfaces.

## B32 · Tiles and One-Way Surfaces

A TileSet owns tile collision polygons and their physics categories. TileMapLayer places cells and builds the bodies. A stateful block is often easier as its own scene; repeated terrain suits tiles. Keep their responsibilities distinct.

## B33 · Tiles and One-Way Surfaces

This collision touched cell three, zero. The body's resource identifier mapped to quadrant zero, zero. Physics chunking groups compatible tile geometry, so the body identifier does not uniquely identify the struck cell. Disabling chunking changes that tradeoff.

## B34 · Tiles and One-Way Surfaces

Probe slightly into the hit surface, against its outward normal. Convert that world point into the tile layer's local coordinates, then map it to a cell. The probe distance is example-specific; test transformed layers and contacts near cell boundaries.

## B35 · Tiles and One-Way Surfaces

The checked four point seven shape reference exposes a one-way direction. The default points down in two D coordinates. This is a body collision feature, not an area's overlap policy. Test tilted platforms rather than assuming older tutorial behavior.

## B36 · Tiles and One-Way Surfaces

Separate one-way surfaces onto their own layer, then temporarily stop scanning it. A short physics timer is a simple drop-through policy. Before restoring collision in a real game, ensure the character has cleared the platform and handle overlapping requests.

## BACT4 · Diagnose the Boundary

Diagnose the Boundary.

## B38 · Diagnose the Boundary

Speed divided by tick rate estimates travel per tick. It is not a collision theorem. Our character's swept movement detected a four-pixel floor across a requested three-hundred-pixel displacement. Method, shape, direction, and backend all matter.

## B39 · Diagnose the Boundary

For fast rigid bodies, continuous collision detection can reduce tunneling. Two D provides ray and shape modes; three D exposes its own settings. Also consider thicker collision geometry and a higher physics rate. None is a universal prevention guarantee.

## B43 · Diagnose the Boundary

A missed coin suggests filtering. An offset boundary suggests scale or a shared resource. A wrong tile suggests contact lookup. A slope flicker suggests movement order or snap. Treat each as a hypothesis, then change one variable and rerun.

## B47 · Diagnose the Boundary

The same responsibilities transfer to three D nodes. Start with boxes, spheres, or capsules. Convex shapes suit movable objects; a few convex pieces can approximate a complex outline. Concave triangle collision is generally for static environments and costs more.

## B48 · Diagnose the Boundary

Review generated code against the chosen release. Godot three's kinematic body, instance method, and movement signature differ from Godot four. Check annotation, await, signal connection, scene-change, and one-based collision APIs too. Confident syntax is not evidence.

## B50 · Diagnose the Boundary

Make the interaction matrix a deliverable. Add the new object, name the categories it scans, and explain one interaction you excluded. If crates should block the player, update both the design and the relevant filtering; our debris deliberately does not.

## BVDT · Closing

Let's recap with Claude. For CSYE seventy-two seventy, Building Virtual Environments. Choose geometry and body roles independently of artwork. Named layers and masks express an interaction policy. Tiles and one-way surfaces need deliberate contact rules. Diagnose a failed boundary with a controlled test.

## BHTF · Closing

Help me build a Godot four collision test room. Include a character, a solid floor, a one-way platform, a pickup area, and rigid debris. Give every object named layers and masks in an interaction matrix. Predict the result of clearing the pickup mask and test it. Explain how you would identify a struck tile cell and verify drop-through clearance.

## BOUT · Closing

Collision Shapes, Layers, and Masks in Godot. At Nik Bear Brown.
