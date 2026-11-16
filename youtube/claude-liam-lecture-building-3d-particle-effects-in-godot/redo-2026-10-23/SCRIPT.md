## BOPEN

Particle Systems and VFX in Godot. Building 3D Particle Effects in Godot. Connect motion, meshes, and materials, then test particles from several angles.

## BIDEA

Hallo. This is Liam, in for Bear. Does a particle effect become three-dimensional just because its node says Three D? We will build the missing draw setup and inspect what survives a moving camera.

## BDEFS

Mesh. The geometry drawn for a particle. Material. A resource for behavior or appearance. Camera. The view through which the scene is seen. Axis. One direction in a coordinate system.

## B01

This is the three-dimensional test stage. The floor and the one-meter reference stay fixed while we change the effect. We are using Godot’s Compatibility renderer. The camera will move so depth has to survive more than one flattering angle.

## B02

Add G P U Particles Three D. Set Amount to sixty-four. Set Lifetime to two seconds. There is no visible result yet. A particle node needs both a simulation resource and something to draw.

## B03

Create a Particle Process Material. This is the behavior resource. It can give particles velocity and gravity, but it is not the surface material that will color a sphere or draw a soft image.

## B04

Assign a small sphere to Draw Pass One, with a standard surface material. Now the particle positions have visible geometry. This is the separate draw decision: the process material moves particles, and the mesh gives each one a shape.

## B05

Launch upward with positive Y, using a speed range from three to five. Gravity points downward at negative six. That differs from our two-dimensional canvas convention. Watch the spheres rise, slow, and return toward the floor.

## B06

Orbit the editor camera. The particles occupy a volume, and the spheres keep their shape as our viewpoint changes. The camera motion is scripted for this recording; the scene and its particle simulation are running in the real editor.

## B07

Here is a staged drawing fault. Remove Draw Pass One. The emission and process resource still exist, but the spheres disappear. More amount or more speed would not repair a missing draw mesh.

## B08

Restore the sphere and the picture returns. Save this checkpoint. When an effect is missing, separate three questions: are particles being emitted, are they moving where expected, and does the draw setup make them visible?

## B09

Change the emission shape from a point to a box. The particles are now born across a region, instead of sharing one exact source. The box controls birth positions; it does not replace the launch direction.

## B10

Compare a sphere-shaped emission volume with the box, then restore the box. Shape changes where the effect begins. Keep speed, lifetime, and gravity fixed during this comparison so that one visible difference has one explanation.

## B11

Reverse the launch direction for a moment. Negative Y sends the initial motion down toward the floor. Restore positive Y. A direction is only meaningful in the coordinate system of this scene, not from the word up in our notes.

## B12

Set gravity to zero. The particles keep traveling along their launch motion. Restore negative six and the path bends back down. Gravity changes the velocity over time; it is not another name for the initial speed.

## B13

Set a controlled scale range, from four tenths to one. The same sphere mesh now produces varied sizes. The one-meter reference makes that choice visible in scene units. Variation should support a readable effect, rather than conceal a weak silhouette.

## B14

Assign a hot-to-cool color ramp in the process material. The spheres stay white because their draw material is not using particle vertex colors yet. This is a deliberately staged connection fault between simulation data and appearance.

## B15

Enable Vertex Color Use As Albedo in the sphere’s material. Now the same particle color data reaches the visible mesh. The process ramp and the draw material have to agree about which data becomes the picture.

## B16

The ramp ends at zero alpha, but an opaque material does not show that fade. Switch transparency to Alpha. The spheres now fade as they age. Color, transparency mode, and particle lifetime are related choices with different jobs.

## B17

Duplicate the emitter as Smoke, then make its process material unique. Put the two sources beside each other. We will keep their different visual jobs visible while changing the smoke’s drawing and motion.

## B18

Replace the smoke’s sphere with a quad and our procedural soft-dot texture. Its material is unshaded and uses alpha transparency. This is a flat image placed in three dimensions; it will need a deliberate camera-facing setup.

## B19

Orbit with billboarding off and the flat cards turn away from us. Enable particle billboarding and Keep Scale. The cards face the camera while preserving the particle size. This repairs the view-dependent silhouette without turning each card into a sphere.

## B20

Give the smoke a slow upward speed, narrow spread, and zero gravity. Replace the hot ramp with a muted smoke ramp. The two effects now share a particle model but communicate different material behavior.

## B21

Attach the growth curve and increase the smoke’s scale. New particles start small and expand as they rise. A curve expresses a change over age, while the random scale range supplies variation between individual particles.

## B22

Compare additive blending with ordinary alpha blending. Additive smoke brightens the background, which changes its visual meaning. Restore alpha for this plume. Choose a blend mode for what the effect represents, then inspect it in the lighting where it will be used.

## B23

Orbit both results together. Mesh particles remain small solid forms; the smoke remains soft camera-facing imagery. Neither drawing method is universally better. The visible job and camera distance determine which one earns its cost.

## B24

Move the original emitter with local coordinates off. New particles appear at the moving source, while older particles stay in world space. This is the behavior needed for a trail left behind an object.

## B25

Turn local coordinates on and the existing cloud follows the source. Turn them off again. Both behaviors are useful, but they tell different stories: an attached aura moves with its owner, while a trail records where that owner has been.

## B26

Shrink the visibility box, then restore a box that covers the measured motion. The box is a culling bound, not a wall for the particles. Inspect it from the camera angles the game can actually reach.

## B27

Duplicate Smoke as Shared Smoke without making its process material unique. Change the duplicate’s launch speed and both plumes change. That is a shared resource doing exactly what sharing means; the mistake is expecting independent behavior.

## B28

Make the duplicate’s process material unique, then reduce only its speed. Its original partner keeps the faster setting. Keep intentional texture sharing, but separate the behavior resource that needs an independent edit.

## B29

For the collision experiment, put the emitter above the floor and aim it down. Add a particle collision box that matches the floor’s top. A visible floor mesh alone does not establish particle collision.

## B30

Enable rigid collision in the particle process material and give it a visible bounce. Now compare the floor contact with collision disabled, then restore collision. This box setup is supported by the renderer used for this recorded test.

## B31

Orbit the contact area. The particle collision box affects the visual simulation; it does not award damage or change the game’s rules. Keep gameplay decisions in gameplay code, even when a particle bounce helps sell the event.

## B32

Keep renderer requirements with the effect. This box example does not establish support for signed-distance-field collision, trails, or every GPU feature. A clean offline capture is also not a frame-time measurement on the target device.

## B33

Save the stage and separate mesh and smoke scenes. The useful result includes the draw setup, motion resource, coordinate choice, and bounds. Those choices can now be tested together when the effects enter a real game.

## BVDT

Let's recap with Claude. A 3D emitter needs behavior and a draw mesh. Emission shape, velocity, and gravity have separate jobs. Vertex color and transparency connect particle data to appearance. Billboards keep soft images readable as the camera moves. Coordinate space, bounds, and resource ownership need deliberate choices. Visual collision does not replace gameplay rules.

## BHTF

Create mesh sparks and soft smoke from the same launch behavior. Predict what changes when the camera moves, then test both effects from several angles and preserve a revision.

## BSIGN

This is Liam, in for Bear. Keep the version that survives the test.

## BOUT

Building 3D Particle Effects in Godot. At Nik Bear Brown.
