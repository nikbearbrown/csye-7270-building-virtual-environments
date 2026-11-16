# Passing Normals to Pixels

## BOPEN

Godot Shader Techniques. Passing Normals to Pixels. Trace a surface normal from the mesh through a varying into fragment lighting.

## BIDEA

Olá. This is Liam, in for Bear. The key correction is that the normal needs a space conversion. We will trace the code, inspect its output, and test where the model stops working.

## BDEFS

Three terms. Normal: A direction perpendicular to the surface. World space: Coordinates shared by objects and lights. Varying: A value passed and interpolated between shader stages.

## B01

The input normal belongs to the mesh's local coordinates. Our light direction is defined in world coordinates. Comparing them directly would compare directions expressed in different reference frames.

## B02

The vertex function multiplies the normal by the model normal matrix. This is a direction transformation, not a position transformation. Translation must not move a normal.

## B03

The varying carries transformed normals toward the fragment stage. Rasterization interpolates their components across each triangle. It does not run the vertex function again for every fragment.

## B04

Interpolation can change a vector's length. Normalize the interpolated normal before using it in a dot product. Otherwise its length would accidentally change the brightness.

## B05

Watch the torus rotate while the light remains fixed in world space. Different surface directions face the light. The normal transformation is what keeps those directions consistent with the scene.

## B06

This uniform stores the direction light travels. Lighting needs the direction toward the light. The minus sign converts between those conventions; removing it illuminates the opposite side.

## B07

The normalized directions meet in a clamped dot product. A surface facing the light gets a positive weight. A surface facing away gets zero. That weight multiplies the surface color.

## B08

Despite its name, the base shader already implements Lambert lighting. Its executable code matches the separate Lambert file. This lesson is about the data path, not a new lighting model.

## BVDT

Let’s recap with Claude. Mesh normals start in local space. The normal matrix carries them to world space. Varyings interpolate across triangles. Normalize before comparing directions. Liam, in for Bear.

## BHTF

Rotate a Godot mesh using this shader. Trace its normal through the vertex function, varying, and fragment function. Explain why the light direction and normal must use the same coordinate space. Check two things: The normal is transformed before the dot product. The interpolated normal is normalized again.

## BOUT

Passing Normals to Pixels. At Nik Bear Brown.
