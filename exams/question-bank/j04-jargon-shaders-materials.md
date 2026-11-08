# Jargon test: shaders and materials

## MA-jargon.31

A student must tell an agent which shader stage to edit. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A vertex shader runs once per vertex and decides where that vertex ends up on screen.
- [ ] B. Tinting every pixel of a surface by distance to the player is a job for the fragment shader.
- [ ] C. Making a flag wave by moving its mesh points is a job for the vertex shader.
- [ ] D. A fragment shader runs once per covered pixel (fragment) and decides its colour.
- [ ] E. A fragment shader runs once per vertex of the mesh.

**Key:** A=T B=T C=T D=T E=F

**Why:**

- A: The vertex stage outputs the position of each vertex.
- B: Per-pixel colour is fragment work.
- C: Displacing vertices changes the shape, which is vertex work.
- D: The fragment stage outputs colour per fragment.
- E: Per-vertex execution describes the vertex shader.

**Source:** Vertex versus fragment shader

## MA-jargon.32

A student asks for a pulsing glow driven from a script. Check each statement that is true about shader inputs. Each statement is worth 1 point (5 points total).

- [ ] A. A varying is set once from the script for the whole mesh.
- [ ] B. A varying is a value passed from the vertex stage to the fragment stage, interpolated across the surface.
- [ ] C. A uniform is calculated separately for each fragment.
- [ ] D. A script changes a shader's glow strength by setting a uniform each frame.
- [ ] E. A uniform is a value set from game code that is the same for every vertex and fragment in a draw.

**Key:** A=F B=T C=F D=T E=T

**Why:**

- A: That describes a uniform.
- B: Varyings carry per-vertex data to the fragment stage with interpolation.
- C: Per-fragment values are computed in the shader, not set as uniforms.
- D: Script-driven parameters are uniforms.
- E: Uniforms are constant across a draw call.

**Source:** Uniform and varying

## MA-jargon.33

A texture looks stretched on a model. Check each statement that is true about UVs. Each statement is worth 1 point (5 points total).

- [ ] A. A stretched texture means the image file is too small to use.
- [ ] B. UV coordinates store the direction in which the surface faces.
- [ ] C. UV stands for the ultraviolet value of a pixel.
- [ ] D. UV coordinates store a colour for each point on a surface.
- [ ] E. UV unwrapping flattens a 3D mesh into 2D so it can be painted.

**Key:** A=F B=F C=F D=F E=T

**Why:**

- A: Stretching usually comes from an uneven UV layout, not from the image.
- B: Surface direction is stored by the normal.
- C: U and V are the names of the two texture axes.
- D: UVs are 2D lookup coordinates; colour comes from the texture they look up.
- E: Unwrapping produces the UV layout.

**Source:** UV coordinates

## MA-jargon.34

An artist says a flat wall should look like rough brick without adding polygons. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A normal map stores a surface direction per pixel so lighting reacts as if there were bumps.
- [ ] B. A normal map moves the vertices outward to add real geometry.
- [ ] C. A normal map changes the colour of the surface.
- [ ] D. A normal map is a good way to make a flat wall light up as if it had brick grooves.
- [ ] E. A normal map fakes surface detail in lighting without changing the mesh's shape or silhouette.

**Key:** A=T B=F C=F D=T E=T

**Why:**

- A: The colours in a normal map encode directions.
- B: Moving vertices is displacement, which a normal map does not do.
- C: Colour belongs to albedo.
- D: Face-on detail is a typical use.
- E: The silhouette stays flat because no geometry moves.

**Source:** Normal map

## MA-jargon.35

A material has parameters an agent can set. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Emission is light that the surface gives off by itself.
- [ ] B. Metallic says how much the surface behaves like a metal.
- [ ] C. Roughness controls how sharp or blurry reflections and highlights are.
- [ ] D. Roughness controls how bright the surface is lit.
- [ ] E. Albedo is the base colour of the surface, before lighting.

**Key:** A=T B=T C=T D=F E=T

**Why:**

- A: An emissive surface appears to glow.
- B: Metallic switches between non-metal and metal reflection behaviour.
- C: A low roughness gives a mirror-like highlight; a high roughness spreads it out.
- D: Brightness comes from lights and emission; roughness shapes the highlight.
- E: Albedo is colour without light or shadow.

**Source:** Albedo, roughness, metallic and emission

## MA-jargon.36

A student must pick the exact material word for a described look. Check each statement in which the term fits the description. Each statement is worth 1 point (5 points total).

- [ ] A. "A matte red plastic ball" suggests setting its albedo to a red colour.
- [ ] B. "Polished steel with sharp reflections" suggests high metallic and low roughness.
- [ ] C. "A mirror" suggests high roughness.
- [ ] D. "A neon sign that lights its own surface" suggests an emission value above zero.
- [ ] E. "Dry chalk with no visible shine" suggests low metallic and high roughness.

**Key:** A=T B=T C=F D=T E=T

**Why:**

- A: Albedo supplies the base colour.
- B: Metals with sharp reflections have high metallic and low roughness.
- C: A mirror has very low roughness.
- D: Self-lit surfaces use emission.
- E: Chalk is a rough non-metal.

**Source:** Pick the precise material term

## MA-jargon.37

A student wants a more realistic material set-up. Check each statement that is true about PBR. Each statement is worth 1 point (5 points total).

- [ ] A. PBR is a file format for animated meshes.
- [ ] B. PBR materials respond consistently across different lighting conditions.
- [ ] C. PBR stands for physically based rendering and describes materials with measured-style parameters.
- [ ] D. PBR stands for per-bone rendering.
- [ ] E. A PBR material usually combines albedo, roughness, metallic and normal inputs.

**Key:** A=F B=T C=T D=F E=T

**Why:**

- A: PBR is a shading approach, not a file format.
- B: One set-up looks plausible under varied lights.
- C: PBR models how light interacts with surfaces.
- D: The letters do not stand for that.
- E: These are the common PBR inputs.

**Source:** PBR

## MA-jargon.38

A particle effect and a window need different transparency settings. Check each statement that is true about blend modes. Each statement is worth 1 point (5 points total).

- [ ] A. Alpha blending mixes by opacity, so a half-transparent window shows the scene behind it.
- [ ] B. Multiply blending darkens what is behind it, which suits shadows and tints.
- [ ] C. Additive blending can make a surface darker than the background.
- [ ] D. A blend mode sets how a surface's output colour is combined with the colour already on screen.
- [ ] E. Additive blending adds colour to what is behind it, so fire and glows look brighter.

**Key:** A=T B=T C=F D=T E=T

**Why:**

- A: Alpha is opacity.
- B: Multiplying by a value of 1 or less keeps or darkens.
- C: Adding non-negative colour cannot darken.
- D: The blend mode is the combining rule.
- E: Adding light brightens, so overlapping glows brighten.

**Source:** Blend mode

## MA-jargon.39

A student writes the prompt: "Add a normal map to change the colour of the wall and a fragment shader to move its vertices." Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A normal map is the standard way to set a wall's colour.
- [ ] B. A normal map does not set colour; albedo (base colour) is the right word.
- [ ] C. The prompt is accurate because both stages move vertices.
- [ ] D. The prompt would be accurate if the words "normal map" were replaced with "albedo" and "fragment" with "vertex".
- [ ] E. Moving vertices is vertex shader work, so "fragment shader" is the wrong stage.

**Key:** A=F B=T C=F D=T E=T

**Why:**

- A: A normal map does not store colour.
- B: Colour is albedo; a normal map changes lighting direction.
- C: The fragment stage works on pixels.
- D: With those two changes the sentence uses the terms correctly.
- E: Vertex positions are handled in the vertex stage.

**Source:** Spot the wrong word in a material prompt

## MA-jargon.40

A vague prompt reads "make the sword look cool". Check each rewrite that uses exact shader and material terms correctly. Each statement is worth 1 point (5 points total).

- [ ] A. "Use additive blend mode on the whole opaque blade so it looks like steel."
- [ ] B. "Add a fragment shader that scrolls the UV over time to make a glint pass along the blade."
- [ ] C. "Give the blade a vertex roughness of 0.2 and a UV metallic of 1."
- [ ] D. "Add an emission colour of pale blue to the blade's fuller, at low strength."
- [ ] E. "Set the blade's metallic to 1 and roughness to 0.2, and add a normal map for the engraving."

**Key:** A=F B=T C=F D=T E=T

**Why:**

- A: Additive blending makes a surface glow like light; it is not how steel is shaded.
- B: Scrolling UVs in the fragment stage animates a glint across the texture.
- C: Roughness and metallic are material parameters, not vertex or UV properties.
- D: Emission supplies self-lit colour.
- E: Metallic, roughness and a normal map are used for their meanings.

**Source:** Rewrite a vague shader prompt

## MA-jargon.41

A student confuses related texture maps. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A roughness map stores a roughness value per pixel instead of one value for the whole material.
- [ ] B. A height map stores how high each point is, and displacement can use it to move geometry.
- [ ] C. An emission map stores the metal grade of each pixel.
- [ ] D. An albedo map stores the lighting direction at each pixel.
- [ ] E. An ambient occlusion map darkens creases where ambient light would be blocked.

**Key:** A=T B=T C=F D=F E=T

**Why:**

- A: Maps vary a parameter across the surface.
- B: Height maps can drive displacement or parallax.
- C: Emission maps store self-lit colour, and metal grade is the metallic map.
- D: Albedo stores colour; direction is in the normal map.
- E: Ambient occlusion adds contact shading.

**Source:** Texture map types

## MA-jargon.42

A student wants a shader to respond to a value that changes while the game runs. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Several materials can share one shader with different parameter values.
- [ ] B. Passing time into a shader as a uniform lets it animate a pattern.
- [ ] C. Changing a material parameter requires rewriting the shader code.
- [ ] D. A material is a shader together with the parameter values and textures it uses.
- [ ] E. A shader is a texture file that stores a painted colour.

**Key:** A=T B=T C=F D=T E=F

**Why:**

- A: This is why one shader can serve many looks.
- B: A time uniform is the standard way to animate.
- C: Parameters are exposed so they can change without editing code.
- D: A material packages a shader and its settings.
- E: A shader is a program, not an image.

**Source:** Shader versus material

