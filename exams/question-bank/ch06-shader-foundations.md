# Chapter 6: Shader foundations

## MA-ch06.1

A renderer draws two opaque triangles. Triangle 1 covers 300 screen pixels. Triangle 2, drawn later and nearer, covers 100 of the same pixels. Rasterization turns each triangle into fragments. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Fragments carry values interpolated from the vertices, such as texture coordinates and depth.
- [ ] B. A fragment is a candidate for a pixel's colour, produced by rasterization for each screen position a triangle covers.
- [ ] C. In the overlap, each pixel gets two fragments, and with opaque surfaces the depth test lets the nearer one win.
- [ ] D. A fragment is a vertex that the vertex shader has moved to its final screen position.
- [ ] E. A fragment is a finished pixel that has passed the depth test and shows in the final image.

**Key:** A=T B=T C=T D=F E=F

**Why:**

- A: Interpolation fills in values between corners.
- B: Rasterization emits one fragment per covered position.
- C: The other fragment is wasted work (overdraw).
- D: A vertex is a corner point; fragments come from rasterization.
- E: A fragment can still be rejected by depth test or discard, or be blended.

**Source:** What a fragment is

## MA-ch06.2

A sprite is drawn on a quad that covers 64 x 64 screen pixels; most of the texture is transparent. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. The vertex shader runs once per vertex and the fragment shader once per fragment.
- [ ] B. The quad has four vertices, and its fragment count follows how many pixels it covers.
- [ ] C. Tinting just the visible artwork is vertex-stage work, since the vertex shader sees the whole sprite.
- [ ] D. Drawing the sprite larger gives more vertices, because vertex count follows screen coverage.
- [ ] E. Transparent texels inside the quad skip the fragment shader.

**Key:** A=T B=T C=F D=F E=F

**Why:**

- A: The two stages run on different units of work.
- B: Vertex count follows the mesh; fragment count follows screen coverage.
- C: Telling artwork from empty texels needs the texture, sampled per fragment.
- D: Vertex count stays at four; fragments increase.
- E: They still produce fragments and run the shader, with alpha 0.

**Source:** Fragment versus vertex counts

## MA-ch06.3

Two programmable stages of the graphics pipeline are the vertex shader and the fragment shader. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. The vertex shader runs once per vertex and typically outputs a clip-space position plus data to pass on.
- [ ] B. Moving a triangle's corners to bend a flat mesh is vertex-stage work.
- [ ] C. Sampling a texture to choose a covered pixel's colour is fragment-stage work.
- [ ] D. For a mesh covering much of the screen, the vertex shader runs far more often than the fragment shader.
- [ ] E. The fragment shader runs once per vertex and outputs the final position of each vertex.

**Key:** A=T B=T C=T D=F E=F

**Why:**

- A: It places corners and hands values onward.
- B: Geometry is changed by changing vertices.
- C: Per-pixel colour decisions belong to the fragment stage.
- D: Fragments outnumber vertices on large objects.
- E: The fragment shader runs per fragment and outputs a colour.

**Source:** Vertex shader versus fragment shader

## MA-ch06.4

A uniform is a value supplied from outside the shader, the same for each invocation in one draw. A varying (interpolant) is output by the vertex stage and interpolated for the fragment stage. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Changing a uniform's value from game code forces the shader to be recompiled.
- [ ] B. A fragment shader can assign a new value to a uniform for later fragments to read.
- [ ] C. An enemy's health ratio set by game code is a natural varying.
- [ ] D. A gradient from 0 at the left of a quad to 1 at the right comes from a varying, interpolated across the triangle.
- [ ] E. A uniform is the channel through which game code hands a per-draw value to a shader.

**Key:** A=F B=F C=F D=T E=T

**Why:**

- A: A uniform is uploaded as data; the program does not change.
- B: Uniforms are read-only inside the shader.
- C: It comes from game code and is the same for the draw, so it is a uniform.
- D: Interpolating corner values gives each fragment its own value.
- E: Each fragment of that draw sees the same value.

**Source:** Uniform versus varying

## MA-ch06.5

A camera scrolls across a 4000 x 1080 background sprite on a 1920 x 1080 screen. A vignette darkens the edges of what the player sees. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A vignette computed from the sprite's UV stays at the display edges as the camera scrolls.
- [ ] B. Screen coordinates scroll with the background, so the top-left display pixel has a new coordinate each frame.
- [ ] C. Screen space is the 3D coordinate system of the scene with the camera at the origin.
- [ ] D. A vignette that hugs the display edges uses the pixel's screen position (SCREEN_UV in Godot).
- [ ] E. UV is a coordinate on the textured surface, normalised from 0 to 1 across it.

**Key:** A=F B=F C=F D=T E=T

**Why:**

- A: It darkens the image's own edges and slides with the scroll.
- B: A screen coordinate names a fixed place in the output image.
- C: That describes view space; screen space is 2D.
- D: Screen space is tied to the display.
- E: UV belongs to the image.

**Source:** UV versus screen space

## MA-ch06.6

Blending combines a new fragment's colour with the framebuffer: result = new x alpha + old x (1 - alpha). Alpha testing keeps or discards a fragment by a threshold. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Alpha testing gives smooth, partially transparent edges on a cut-out.
- [ ] B. With blending, a half-transparent red over blue gives a mix of both, weighted by alpha.
- [ ] C. Alpha testing has two-state transparency (kept or dropped) and no order dependence.
- [ ] D. Blending gives the same result whichever translucent layer is drawn first.
- [ ] E. A window pane that shows the scene dimly is better made with alpha testing.

**Key:** A=F B=T C=T D=F E=F

**Why:**

- A: A tested fragment is kept in full or dropped, so edges are hard.
- B: Blending is a weighted mix.
- C: Nothing is blended.
- D: Blending is order-dependent, so translucent objects are sorted.
- E: Partial opacity needs blending.

**Source:** Alpha blending versus alpha test

## MA-ch06.7

Godot has a 2D shader type (canvas_item) and a 3D shader type (spatial). Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Setting ROUGHNESS in a canvas_item shader gives a sprite a glossy physically based look.
- [ ] B. The shader type follows what is drawn: canvas_item for 2D elements, spatial for 3D objects.
- [ ] C. A canvas_item fragment function writes the pixel's final colour, starting from the texture colour.
- [ ] D. A spatial fragment function sets material properties (ALBEDO, ROUGHNESS, METALLIC) and the engine's lighting makes the final colour.
- [ ] E. A spatial shader is assigned to a 2D sprite to give it 3D-style shading.

**Key:** A=F B=T C=T D=T E=F

**Why:**

- A: There is no ROUGHNESS in a canvas_item shader.
- B: The type matches the kind of object.
- C: The 2D fragment decides the drawn colour itself.
- D: The renderer does the shading.
- E: 2D sprites use canvas_item shaders.

**Source:** 2D canvas shader versus 3D spatial shader

## MA-ch06.8

A shader colour is four floats (red, green, blue, alpha) normally from 0.0 to 1.0. A pixel has the colour (0.2, 0.4, 0.6, 1.0). Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. mix(colour, white, 0.25) moves the colour 25 percent of the way toward white.
- [ ] B. Alpha 0.0 is fully transparent.
- [ ] C. Writing 8-bit numbers (255, 128, 0) into float channels gives orange.
- [ ] D. In an 8-bit image 255 corresponds to 1.0, so (255, 128, 0) is about (1.0, 0.5, 0.0).
- [ ] E. Multiplying the red, green and blue channels by white, (1, 1, 1), turns the pixel white.

**Key:** A=T B=T C=F D=T E=F

**Why:**

- A: mix interpolates between two values.
- B: Alpha is the opacity channel.
- C: They clamp to full intensity, giving yellow.
- D: 8-bit values are divided by 255.
- E: Multiplying by 1 leaves each channel unchanged.

**Source:** Colour as RGBA from 0 to 1

## MA-ch06.9

A developer asks a coding agent for a white flash on a multi-coloured sprite when it is hit. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Setting the colour multiplier (modulate in Godot) to white pushes the artwork to white.
- [ ] B. A shader can not do this, so a white copy of the texture is swapped in.
- [ ] C. "In the fragment shader, mix the output colour toward white by a 0-to-1 uniform flash_amount, keep alpha, driven by the script" names stage, operation, control, constraint and driver.
- [ ] D. "Change the vertex positions" sends the agent to the stage that moves corners and does not recolour the artwork.
- [ ] E. Leaving out alpha is harmless: transparent surroundings stay transparent.

**Key:** A=F B=F C=T D=T E=F

**Why:**

- A: Multiplying by white leaves colours unchanged.
- B: A fragment shader can mix toward white with no extra texture.
- C: It is a precise instruction.
- D: Recolouring pixels is fragment work.
- E: An opaque white output turns the surroundings into a white box.

**Source:** Hit flash wording

## MA-ch06.10

A flag is a flat quad with 4 vertices. A developer asks for a ripple in the wind. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Vertex displacement by a sine of time moves just the four corners, so a subdivided mesh is needed for a wave.
- [ ] B. A continuous ripple can read the engine's global time, since it has no start event.
- [ ] C. Offsetting the sampling coordinate by a sine of position and time in the fragment shader ripples the picture on the same quad.
- [ ] D. In the UV-offset approach the fragment shader moves the quad's vertices.
- [ ] E. The vertex approach changes the flag's outline, and the UV-offset approach keeps the rectangle.

**Key:** A=T B=T C=T D=F E=T

**Why:**

- A: Detail follows vertex count.
- B: Only event-triggered effects need a value from game code.
- C: Distorting UV shifts which texel each pixel shows.
- D: Fragment shaders decide colour, not vertex positions.
- E: Moved vertices change the rasterized shape.

**Source:** Vertex versus fragment for a ripple

## MA-ch06.11

A developer asks for a 0.4 s flash starting at the hit. The agent writes flash = 1.0 - clamp(TIME / 0.4, 0.0, 1.0), where TIME is engine time since start. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. TIME restarts at each hit, so repeated hits flash correctly.
- [ ] B. TIME is a uniform that game code sets when the hit happens.
- [ ] C. The shader sees a hit because it runs each time a frame is drawn.
- [ ] D. TIME counts from engine start, not from the hit.
- [ ] E. Dividing TIME by a larger number fixes the restart problem.

**Key:** A=F B=F C=F D=T E=F

**Why:**

- A: It is not reset.
- B: TIME is supplied by the engine as a global clock.
- C: Events reach a shader through uniforms, textures or vertex data.
- D: Global time is not reset by events.
- E: The clock still starts at engine start.

**Source:** Time as a uniform

## MA-ch06.12

A developer asks for a one-pixel white outline around the opaque shapes of a 64 x 64 texel sprite. Each fragment invocation runs independently. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A fragment can not read the final colour a neighbouring fragment computed in the same draw.
- [ ] B. The outline samples the sprite's alpha at neighbouring offsets of 1/64 in UV, and colours a transparent fragment white when a neighbour is opaque.
- [ ] C. Outline pixels outside the quad appear without padding, because fragments exist everywhere.
- [ ] D. A vertex shader makes the outline by moving each pixel one step outward.
- [ ] E. A fragment shader can create new fragments beyond the quad's edge.

**Key:** A=T B=T C=F D=F E=F

**Why:**

- A: Invocations are independent.
- B: One texel is 1/64 in UV here.
- C: Fragments exist only where geometry covers the screen.
- D: The vertex stage handles vertices, not pixels.
- E: Rasterization decides which fragments exist.

**Source:** Neighbour sampling and texel

## MA-ch06.13

A developer asks for a dissolve: holes follow a noise pattern as a uniform called dissolve goes from 0 to 1. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Discarded pixels fade out gradually, so hole edges are smooth.
- [ ] B. A smooth alpha fade is independent of draw order.
- [ ] C. A discarded fragment writes nothing, so the pixel keeps what was drawn there.
- [ ] D. Comparing a noise sample with the dissolve uniform and discarding fragments below it gives sharp-edged holes.
- [ ] E. Discard has no performance cost.

**Key:** A=F B=F C=T D=T E=F

**Why:**

- A: Discard is all or nothing; smooth edges need partial alpha and blending.
- B: Partial alpha is blended, and blending depends on order.
- C: Discard drops the fragment.
- D: The keep-or-discard decision is per fragment.
- E: It can defeat depth optimisations on some GPUs.

**Source:** Dissolve with discard

## MA-ch06.14

A developer wants requests to land in the right shader stage. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Turning the whole level black-and-white on death is fragment-stage work.
- [ ] B. Squash and stretch of a mesh on landing is fragment-stage work.
- [ ] C. Swaying grass tips is vertex-stage work when each blade is a mesh with displaceable vertices.
- [ ] D. A palette swap is vertex-stage work because the palette belongs to the whole object.
- [ ] E. Horizontal scanlines over the screen are vertex-stage work because lines are geometry.

**Key:** A=T B=F C=T D=F E=F

**Why:**

- A: It recolours each pixel.
- B: It changes geometry, so it is vertex-stage or transform work.
- C: Swaying displaces vertex positions.
- D: The colour looked up per pixel is fragment-stage.
- E: A pattern in screen position is computed per fragment.

**Source:** Choosing the shader stage

## MA-ch06.15

A developer tells a coding agent: "Use a shader to shrink the boss to half size so the player can slip under its attacks." The boss has a collision shape separate from its sprite. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A shader changes how the boss is drawn, not the size or position of its collision shape.
- [ ] B. Physics queries read the pixels the shader outputs to decide overlaps.
- [ ] C. Vertex positions changed in a shader update the node's transform.
- [ ] D. Discarding the lower half of the fragments shrinks the collision shape to match.
- [ ] E. Shrinking the visual in a shader also shrinks the hit area.

**Key:** A=T B=F C=F D=F E=F

**Why:**

- A: Rendering and physics are separate systems.
- B: Collision is computed from shapes.
- C: Shader output stays on the GPU.
- D: Discard changes only what is displayed.
- E: The hit area needs a change in game code.

**Source:** Shaders versus gameplay

## MA-ch06.16

An interviewer asks why shaders run on the GPU and what they can not do. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A shader can read a variable of a game script directly if it is a number.
- [ ] B. A frame limited by game logic and draw preparation is GPU-bound.
- [ ] C. Moving a calculation from a script into a fragment shader is faster because the GPU is faster than the CPU.
- [ ] D. A GPU runs the same small program over many vertices or fragments in parallel.
- [ ] E. Data a shader needs, such as the player's position, arrives through uniforms or textures set from the CPU side.

**Key:** A=F B=F C=F D=T E=T

**Why:**

- A: Values are passed in as uniforms.
- B: That is CPU-bound.
- C: A fragment shader runs per pixel, so cost can grow.
- D: That is what GPUs are built for.
- E: Shaders have no access to game objects.

**Source:** GPU versus CPU work

## MA-ch06.17

A simplified chain: vertex data, vertex shader, mapping to the screen, rasterization, fragment shader, depth and stencil tests plus blending, framebuffer. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. The fragment shader runs before rasterization to decide which pixels a triangle covers.
- [ ] B. The vertex shader and the fragment shader are programmable stages.
- [ ] C. Rasterization is fixed-function: configured, not programmed.
- [ ] D. Blending happens before the fragment shader.
- [ ] E. The vertex shader's output is already in screen pixels.

**Key:** A=F B=T C=T D=F E=F

**Why:**

- A: It runs on fragments rasterization produced.
- B: Developers write both in a shader language.
- C: Developers do not write it.
- D: Blending uses the shader's output colour, so it comes after.
- E: It typically outputs clip-space positions that are converted later.

**Source:** Programmable versus fixed-function stages

## MA-ch06.18

A 1920 x 1080 screen has 2,073,600 pixels. A full-screen translucent fog sprite and a full-screen translucent glow sprite are drawn, then the UI. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. The two layers together cost 4,147,200 fragment-shader runs per frame.
- [ ] B. Rendering the fog at half the width and half the height cuts its fragment count to a quarter.
- [ ] C. The GPU skips low-alpha fragments, so the glow costs about its visible part.
- [ ] D. Making the fog layer's fragment shader simpler lowers its cost though the pixel count is unchanged.
- [ ] E. Overdraw means the same screen pixel is shaded by more than one fragment in a frame.

**Key:** A=T B=T C=F D=T E=T

**Why:**

- A: 2 x 2,073,600.
- B: 960 x 540 is a quarter of the pixels.
- C: Low alpha does not stop the shader running.
- D: Cost is shader work times fragment count.
- E: Here each pixel gets at least two.

**Source:** Overdraw and fragment cost

## MA-ch06.19

A fragment shader reads a texture with texture(tex, uv). The texture is a 16 x 16 pixel-art icon on a quad covering 128 x 128 screen pixels. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Linear filtering keeps enlarged texels crisp.
- [ ] B. A uv of (1.25, 0.5) has no colour to return, so the pixel is left undrawn.
- [ ] C. A texel is one pixel of the texture image.
- [ ] D. Nearest filtering returns a single texel's colour, keeps blocks crisp and suits pixel art.
- [ ] E. UV counts texels, so the centre of the icon is at uv (8, 8).

**Key:** A=F B=F C=T D=T E=F

**Why:**

- A: Linear filtering blends neighbouring texels and blurs the blocks.
- B: The wrap mode decides which texel comes back.
- C: Texel names the texture's own pixel.
- D: Each texel appears as an 8 x 8 block here.
- E: UV is normalised, so the centre is (0.5, 0.5).

**Source:** Texel and filtering

## MA-ch06.20

A hit flash fades from 1.0 to 0.0. Version A lowers it by 1/12 on each rendered frame. Version B sets it to 1.0 - elapsed_seconds / 0.4, with elapsed_seconds accumulated from the time each frame took. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Counting frames gives frame-rate independence.
- [ ] B. Frame-rate independent means the effect lasts the same number of seconds at 30 and 144 frames per second.
- [ ] C. Accumulating delta time (seconds since the previous frame) gives frame-rate independence, as in Version B.
- [ ] D. Version A lasts longer at 144 frames per second than at 30.
- [ ] E. Version A lasts 0.4 s at 30 frames per second.

**Key:** A=F B=T C=T D=F E=T

**Why:**

- A: A frame count changes duration with frame rate.
- B: Duration is in seconds.
- C: Elapsed time is measured in seconds.
- D: Twelve frames are shorter at a higher rate.
- E: 12 frames / 30 per second.

**Source:** Frame-rate independence

## MA-ch06.21

An interviewer asks how a fragment differs from a pixel. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Fragment and pixel are two names for the same thing.
- [ ] B. A pixel is the final element of the output image, and several fragments can compete for one pixel.
- [ ] C. Blending combines a fragment's colour with the colour already in the framebuffer.
- [ ] D. The fragment count follows the number of vertices in the mesh.
- [ ] E. A fragment becomes the pixel's colour if it survives the depth test, the stencil test and discard.

**Key:** A=F B=T C=T D=F E=T

**Why:**

- A: They differ in meaning and count.
- B: Competing fragments are overdraw.
- C: Blending is the final combining step.
- D: It follows screen coverage.
- E: Rejected fragments are wasted work.

**Source:** Fragment versus pixel

## MA-ch06.22

A developer sends prompts to a coding agent that confuse fragment, pixel and vertex. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. "Edit the fragment shader to squash and stretch the mesh" names the right stage.
- [ ] B. Flash, tint and dissolve are vertex-stage effects.
- [ ] C. "Per-vertex" and "per-fragment" are the same level of detail on a large quad.
- [ ] D. Pixel and fragment can be swapped in a prompt without changing meaning.
- [ ] E. "Edit the vertex shader to tint the sprite's artwork on hit" names the wrong stage; tint is fragment work.

**Key:** A=F B=F C=F D=F E=T

**Why:**

- A: Shape changes are vertex-stage.
- B: They are per-pixel fragment effects.
- C: A quad has few vertices but many fragments.
- D: They differ, and the agent may edit the wrong stage.
- E: Colour per pixel is fragment-stage.

**Source:** Wrong word in a prompt

## MA-ch06.23

A developer tells a coding agent: "Add a shader to the player so it looks hurt." The player is a multi-coloured 2D sprite with transparent areas. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Preserving alpha keeps transparent texels transparent, and at 0 the sprite looks as before.
- [ ] B. A float uniform from 0 to 1 sets how far the colour is mixed toward the target.
- [ ] C. A uniform set on a material shared by several sprites tints just the hit sprite.
- [ ] D. A vertex shader that wobbles the mesh is a safe reading of the vague wording.
- [ ] E. Naming the shader kind (canvas_item) and the stage (fragment) removes ambiguity.

**Key:** A=T B=T C=F D=F E=T

**Why:**

- A: Alpha and the zero case are stated.
- B: It is the control that game code drives.
- C: A shared material changes all users.
- D: It does not recolour the sprite.
- E: The change is to colour, not geometry.

**Source:** Precise hurt-tint instruction

## MA-ch06.24

Data and cost across the vertex and fragment stages. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A per-pixel keep-or-discard dissolve decision is vertex-stage work.
- [ ] B. Scanlines use the fragment's screen-space position, since the pattern varies per output pixel regardless of mesh UV.
- [ ] C. The vertex stage runs once per vertex and passes interpolated values, such as UV, to the fragment stage.
- [ ] D. A waving flag on a mesh with many vertices is vertex-stage work, limited by the vertex count.
- [ ] E. For a large on-screen object, fragment work greatly outnumbers vertex work.

**Key:** A=F B=T C=T D=T E=T

**Why:**

- A: It is a per-fragment decision.
- B: Screen position is independent of the mesh.
- C: These are varyings.
- D: Displacement moves vertices.
- E: Fragments follow coverage.

**Source:** Varyings and stage cost

## MA-ch06.25

A game needs a chain-link fence, a ghost, a window pane and a dissolving enemy. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A ghost suits alpha testing because it needs hard edges.
- [ ] B. A chain-link fence suits blending better than alpha testing.
- [ ] C. Blending adds no overdraw or sorting problems.
- [ ] D. Translucent objects drawn with blending are typically sorted far to near.
- [ ] E. Alpha-tested fragments need no sorting.

**Key:** A=F B=F C=F D=T E=T

**Why:**

- A: A ghost needs partial transparency, so blending.
- B: A fence is hard-edged, so alpha test fits.
- C: It adds both.
- D: Blending depends on draw order.
- E: Keep-or-discard does not depend on order.

**Source:** Draw order and alpha

## MA-ch06.26

A sprite shared by several enemies pulses red for 0.4 s when hit. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A uniform set on a shared material changes each object using it.
- [ ] B. Game code computes progress from 0 to 1 from the seconds since the hit and sets the uniform.
- [ ] C. A uniform is the channel through which game events reach the shader.
- [ ] D. A per-object copy of the material or a per-instance parameter pulses just the hit object.
- [ ] E. Global engine time is a good clock for an event-triggered effect.

**Key:** A=T B=T C=T D=T E=F

**Why:**

- A: The material is shared.
- B: This keeps the duration in seconds.
- C: It is set from game code.
- D: Per-instance data separates objects.
- E: It counts from engine start.

**Source:** Uniform, event and shared material

## MA-ch06.27

A textured mesh goes from game code to a changed pixel. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Depth test, stencil test and blending are configurable fixed-function steps after the fragment shader.
- [ ] B. A fragment can run the fragment shader and still be rejected by the depth test, which is wasted work.
- [ ] C. A draw call is the command from the CPU asking the GPU to draw the submitted mesh with its textures and uniforms.
- [ ] D. The vertex shader runs on the CPU.
- [ ] E. The fragment shader is fixed-function and the vertex shader is programmable.

**Key:** A=T B=T C=T D=F E=F

**Why:**

- A: They decide whether and how output is written.
- B: That waste is overdraw.
- C: The CPU prepares and submits.
- D: It runs on the GPU.
- E: Both are programmable.

**Source:** Pipeline walk-through

## MA-ch06.28

A developer asks for a "metallic and shiny" 2D character sprite. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Setting a roughness uniform in a canvas shader makes the sprite respond to physically based lighting.
- [ ] B. A moving highlight band from UV and time, masked by alpha, fakes a shiny look on a sprite.
- [ ] C. Roughness and metallic have no meaning in a 2D canvas shader, so "metallic" is ambiguous in a 2D prompt.
- [ ] D. A normal map is the sprite's colour texture.
- [ ] E. Albedo, roughness, metallic and emission are material properties of a spatial shader, which the engine lights.

**Key:** A=F B=T C=T D=F E=T

**Why:**

- A: 2D drawing has no such model.
- B: It is a 2D approximation.
- C: The agent may invent parameters.
- D: A normal map holds surface directions for lighting.
- E: Spatial fragments set properties.

**Source:** 2D versus 3D shiny wording

## MA-ch06.29

A developer asks for flowing water on a 128 x 128 tile. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Scrolling is made by moving the tile's vertices over time.
- [ ] B. Repeat wrap mode with a seamless texture lets offset UVs run past 0 to 1 without a seam.
- [ ] C. Scrolling adds an offset proportional to time to the UV before sampling.
- [ ] D. Clamp wrap mode makes scrolled water tile seamlessly.
- [ ] E. Linear filtering suits smooth water, and nearest filtering suits crisp pixel art.

**Key:** A=F B=T C=T D=F E=T

**Why:**

- A: It is a UV offset in the fragment stage.
- B: Otherwise edge texels smear under clamp.
- C: Speed is in UV units per second.
- D: Clamp smears the edge texels.
- E: Filter choice follows the look.

**Source:** UV scrolling, wrap and filter
