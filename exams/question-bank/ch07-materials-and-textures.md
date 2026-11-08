# Chapter 7: Materials and textures

## MA-ch07.1

A student reads that in physically based rendering a surface is described by separate properties, one of which is albedo (also called base colour). Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Albedo and base colour are two names for the colour a surface reflects diffusely before lighting.
- [ ] B. For a bare metal, the base colour tints the reflections.
- [ ] C. Albedo sets how blurred the reflections are.
- [ ] D. Shadows painted into an albedo texture are called baked lighting and double up with the engine's own lighting.
- [ ] E. Albedo is the finished on-screen colour of a pixel after lights and shadows.

**Key:** A=T B=T C=F D=T E=F

**Why:**

- A: Albedo is the intrinsic diffuse colour, and the renderer applies lighting on top of it.
- B: A metal has little diffuse colour, so its base colour supplies the tint of its reflections.
- C: Blur of reflections is set by roughness, not albedo.
- D: Baked lighting is shading precomputed into the image, so it stacks with runtime lighting and looks double-shaded.
- E: The on-screen colour also depends on light colour, light direction, shadows and reflections.

**Source:** Albedo and baked lighting

## MA-ch07.2

A developer tells a coding agent: "Make the hull shinier." The hull material has a weathered-wood albedo, metallic 0 and roughness 0.8. Check each statement that is true about the terms. Each statement is worth 1 point (5 points total).

- [ ] A. Lowering roughness makes reflections sharper and highlights tighter, which reads as shinier.
- [ ] B. In an engine that exposes smoothness instead of roughness, shinier means a lower smoothness value.
- [ ] C. Brightening the albedo texture is a gloss change, because lighter surfaces reflect sharper images.
- [ ] D. "Shinier" is an imprecise word, because glossy paint (metallic 0, low roughness) and polished metal (metallic near 1, low roughness) are different setups.
- [ ] E. Raising the emission colour is the exact term-level change for shine, because emission adds highlights.

**Key:** A=T B=F C=F D=T E=F

**Why:**

- A: Roughness is the blur of reflections, so a lower value gives a sharper highlight.
- B: Smoothness is roughly the inverse of roughness, so shinier means a higher smoothness.
- C: Albedo changes the base colour, not the sharpness of reflections.
- D: A precise prompt names roughness and metallic instead of the vague word shinier.
- E: Emission is light a surface gives off by itself, which makes it glow rather than reflect.

**Source:** Shinier versus roughness, metallic and specular

## MA-ch07.3

In the metallic-roughness material model, each surface has a metallic value between 0 and 1. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Values between 0 and 1 stand for transitions such as rust, dirt or chipped paint on a metal.
- [ ] B. Specular is the reflection strength of a non-metal, which is a different control from metallic.
- [ ] C. A bare metal with a pure black albedo still shows bright, naturally coloured reflections.
- [ ] D. A dielectric is a non-metal such as plastic, wood or skin, and it sits near metallic 0.
- [ ] E. Metallic controls how blurred reflections are, so metallic 1 gives the blurriest reflections.

**Key:** A=T B=T C=F D=T E=F

**Why:**

- A: A real point is metal or not, so in-between values stand for mixed or partly covered areas.
- B: Specular scales reflection on non-metals, while metallic switches the kind of material.
- C: A metal takes its reflection tint from the base colour, so a black albedo gives almost no reflection.
- D: Dielectric is the term for a non-metal, and metallic 0 selects that behaviour.
- E: Reflection blur is roughness, not metallic.

**Source:** Metallic and dielectric

## MA-ch07.4

A technical artist sets up three surfaces in the metallic-roughness model. Rubber ball: metallic 0, roughness 0.9. Chrome sphere: metallic 1, roughness 0.05. Glossy plastic toy: metallic 0, roughness 0.2. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Setting the rubber ball's metallic to 1 would tint its reflections by its albedo but leave them blurred.
- [ ] B. The plastic toy's highlights are tinted by its albedo, as a metal's reflections are.
- [ ] C. The chrome sphere shows a sharp, mirror-like reflection.
- [ ] D. The rubber ball shows sharp reflections, because a roughness of 0.9 means a smooth surface.
- [ ] E. Raising the chrome sphere's roughness would make its reflection sharper.

**Key:** A=T B=F C=T D=F E=F

**Why:**

- A: Metallic changes the tint of the reflection, and the high roughness keeps it blurred.
- B: Highlights on a non-metal are not tinted by albedo; they keep the colour of the light.
- C: Metallic 1 with low roughness gives a mirror-like reflection.
- D: High roughness means blurred reflections, which is the opposite of smooth.
- E: More roughness spreads the reflection out, making it blurrier.

**Source:** Roughness, metallic and specular compared

## MA-ch07.5

A brick wall has a height map (greyscale, white high, black low) and a tangent-space normal map (a mostly purple-blue image). Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Displacement moves vertices and so changes the silhouette, while normal and bump maps change shading alone.
- [ ] B. Both maps can make a flat surface shade as if it had bumps without adding triangles.
- [ ] C. A height map used for bump mapping gives slopes between neighbouring texels, from which a shading normal is derived.
- [ ] D. A normal map changes the silhouette of the wall at a grazing angle, like real geometry.
- [ ] E. A normal map stores a surface direction in each texel, with red, green and blue encoding the x, y and z of a vector.

**Key:** A=T B=T C=T D=F E=T

**Why:**

- A: Displacement needs enough vertices to move, and it changes the actual shape.
- B: Normal mapping and bump mapping both fake relief in the lighting without extra geometry.
- C: Bump mapping derives slope from the height difference between neighbouring texels.
- D: The outline stays flat because the geometry is unchanged.
- E: A normal map is an image of per-texel directions encoded in colour channels.

**Source:** Normal map versus height and bump map

## MA-ch07.6

A developer downloads a floor pack with floor_albedo.png, floor_normal.png, floor_roughness.png and floor_ao.png, and tells a coding agent: "Put the wood floor texture on the floor mesh." Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. The prompt is imprecise because it does not name the map types, so the agent may fill a slot with the wrong image.
- [ ] B. The word "texture" names which of the four images goes in which material slot.
- [ ] C. A greyscale roughness image placed in the albedo slot still acts as roughness, because the engine reads its contents.
- [ ] D. A better prompt assigns the albedo map to albedo, the normal map to normal, the roughness map to roughness and the AO map to ambient occlusion.
- [ ] E. A normal map placed in the albedo slot tints the floor purple-blue instead of adding bumps.

**Key:** A=T B=F C=F D=T E=T

**Why:**

- A: Albedo map, normal map, roughness map and AO map are different terms for different slots.
- B: Texture is a general word for image data and does not name a slot.
- C: The engine uses the slot, not the content, to decide how an image is used.
- D: Naming each map type and its slot removes the ambiguity.
- E: The slot decides the meaning, so a normal map read as colour just paints colour.

**Source:** Naming map types and slots to an agent

## MA-ch07.7

A tangent-space normal map stores a direction in each texel, decoded per channel as n = 2c − 1 on a 0 to 1 scale. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Tangent space and world space name the same coordinate frame.
- [ ] B. Tangent space means the vectors are relative to the surface, with x along U, y along V and z along the surface normal.
- [ ] C. A tangent-space map has to be re-baked each time the object rotates in the scene.
- [ ] D. A normal map looks mostly purple-blue because most texels point near straight out of the surface.
- [ ] E. A texel decoding to (0, 0, 1) points straight out of the surface and shades as flat.

**Key:** A=F B=T C=F D=T E=T

**Why:**

- A: World space is shared by the scene, while tangent space follows each surface.
- B: Tangent space is a frame attached to the surface itself.
- C: Because vectors are relative to the surface, the map survives rotation and deformation.
- D: Most texels are close to the unperturbed direction, so the image is dominated by one colour.
- E: (0, 0, 1) is the unperturbed normal, which encodes as the purple-blue colour.

**Source:** Tangent space and normal decoding

## MA-ch07.8

A wooden crate has an ambient occlusion (AO) texture that is white where light reaches freely and dark in creases. Assume the engine applies the AO texture to ambient light, as Godot and Unity do by default. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. An AO texture and screen-space ambient occlusion (SSAO) are the same effect.
- [ ] B. The AO texture is a shadow cast by the directional light, so it moves when the light rotates.
- [ ] C. An AO texture that dims just ambient light does not darken direct light from a directional light.
- [ ] D. An AO texture holds data rather than colour, so it is imported as linear, not sRGB.
- [ ] E. AO approximates how much ambient light reaches each point, so creases receive less of it.

**Key:** A=F B=F C=T D=T E=T

**Why:**

- A: AO texture is authored per material, while SSAO is computed from screen depth each frame.
- B: AO is a fixed map of occlusion, not a shadow tied to a light.
- C: Ambient occlusion modulates ambient light, so direct light is unaffected.
- D: A greyscale occlusion value is a number to use as stored, so it is data.
- E: Occlusion is the fraction of ambient light blocked by nearby surfaces.

**Source:** Ambient occlusion

## MA-ch07.9

A designer gives a lamp mesh an emission colour so that it appears to glow. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Emission is another name for a brighter albedo.
- [ ] B. To light nearby surfaces, the scene needs a light source or a global illumination feature that treats emissive surfaces as lights.
- [ ] C. Emission adds colour to the final appearance without needing scene lighting, so the lamp glows in a dark room.
- [ ] D. Emission values above 1.0 are meaningless on a modern display pipeline.
- [ ] E. In a basic real-time renderer without global illumination, an emissive mesh lights nearby walls like a point light.

**Key:** A=F B=T C=T D=F E=F

**Why:**

- A: Albedo is reflected diffuse colour and needs light, while emission does not.
- B: Only a light or a global illumination method makes the glow illuminate neighbours.
- C: Emission is light a surface gives off by itself.
- D: High dynamic range values above 1.0 are used for bright glow and bloom.
- E: Emission changes the lamp's own appearance but does not light other objects by default.

**Source:** Emission versus albedo

## MA-ch07.10

PBR (physically based rendering) is the usual way modern engines describe materials. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. PBR needs a photorealistic art style, so stylised games use a different material system.
- [ ] B. Energy conservation means a surface does not reflect more light than it receives, so rougher highlights are wider and dimmer.
- [ ] C. PBR does not require ray tracing; it works in ordinary rasterizing renderers.
- [ ] D. PBR describes a surface with base colour, roughness and metallic, which stay meaningful under different lighting.
- [ ] E. The metallic workflow and the specular workflow are two ways of parameterising a PBR material.

**Key:** A=F B=T C=T D=T E=T

**Why:**

- A: PBR is a description of surfaces and light, and stylised games can use it too.
- B: Spreading the same energy over a wider highlight makes each point dimmer.
- C: PBR is a material model, separate from the choice of rendering algorithm.
- D: The parameters describe the surface itself, not one particular lighting setup.
- E: Both workflows express physically based surfaces with different parameter sets.

**Source:** PBR and energy conservation

## MA-ch07.11

A material pack has albedo, normal map, roughness, ambient occlusion and emission colour images. A colour texture is stored in sRGB and decoded to linear before lighting; a data texture holds numbers used as stored. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. The normal map, roughness and ambient occlusion images are colour textures and are flagged as sRGB like albedo.
- [ ] B. A data texture is another name for a texture with an alpha channel.
- [ ] C. Emission colour is authored like albedo and is treated as sRGB.
- [ ] D. Albedo is a colour texture and is imported as sRGB.
- [ ] E. Linear means the stored number goes into the shading maths as it is.

**Key:** A=F B=F C=T D=T E=T

**Why:**

- A: Those three hold numbers or vectors, so they are data textures and are read as linear.
- B: A data texture is defined by its content being numbers, not by having alpha.
- C: Emission colour is a colour and follows the colour path.
- D: Albedo is authored as colour for human vision and decoded to linear.
- E: Linear values are used directly in lighting calculations.

**Source:** Colour textures versus data textures

## MA-ch07.12

A roughness map with a uniform mid-grey of 0.50 is wrongly imported as an sRGB colour texture, so the renderer applies the sRGB-to-linear decode. That decode turns 0.50 into about 0.22. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. The right fix is to multiply the roughness in the shader by a constant.
- [ ] B. The error is invisible, because the decoded number is the same mid-grey.
- [ ] C. Importing the roughness map as linear data uses the authored number unchanged.
- [ ] D. The surface is shaded with a roughness of about 0.22 instead of 0.50, so it looks glossier than intended.
- [ ] E. A mid-grey albedo wrongly treated as linear data comes out lighter than intended.

**Key:** A=F B=F C=T D=T E=T

**Why:**

- A: The cause is the colour-space flag, and the fix is to change the import setting.
- B: The decode changes the number, so the result differs.
- C: Linear import means no decode happens to the stored value.
- D: A smaller roughness means sharper reflections, so the surface looks glossier.
- E: Colour left undecoded skips the sRGB-to-linear step, so it ends up brighter than authored.

**Source:** sRGB versus linear decoding

## MA-ch07.13

A tiled checker floor shimmers far from the camera. A coding agent turns on mipmaps, a chain of precomputed half-size copies of the texture. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Enabling mipmaps replaces the full-size level, so close-up detail is lost.
- [ ] B. Mipmaps make the texture sharper when the camera is very close, because extra levels add detail.
- [ ] C. Magnification, where one texel covers many pixels, is not what mipmaps address; minification is.
- [ ] D. For distant floor where many texels fall in one pixel, the GPU reads a smaller pre-averaged level, which reduces shimmer.
- [ ] E. The mip chain adds about one third to the memory of the texture.

**Key:** A=F B=F C=T D=T E=T

**Why:**

- A: The base level remains and is used up close.
- B: Extra levels are smaller than the base, so they add no detail close up.
- C: Mipmaps help minification, which is many texels per pixel.
- D: Pre-averaged levels avoid aliasing when many texels map to one pixel.
- E: Each level is a quarter of the previous one, so the chain sums to about a third more.

**Source:** Mipmaps and minification

## MA-ch07.14

A 2048 by 2048 albedo texture is a small PNG on disk, but takes far more video memory when kept as plain RGBA8. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Block-compressed textures stay compressed in video memory, and the GPU decodes them while sampling.
- [ ] B. File compression such as PNG and GPU block compression are two different things.
- [ ] C. Block-compressed GPU formats are lossless, so quality is identical to the PNG.
- [ ] D. A PNG's size on disk says little about video memory use, because the GPU samples it uncompressed unless it is imported in a GPU format.
- [ ] E. A normal map can use the same compression settings as an albedo texture with no concern for artefacts.

**Key:** A=T B=T C=F D=T E=F

**Why:**

- A: GPU hardware reads the compressed blocks directly.
- B: PNG is a storage format, while block compression is a GPU format that stays compressed in memory.
- C: Block compression is lossy and trades quality for memory.
- D: Disk compression is undone on load, so file size does not predict GPU memory.
- E: Normal maps are sensitive to compression artefacts and usually need a format chosen for vectors.

**Source:** Block compression and video memory

## MA-ch07.15

A texture is sampled when a pixel maps to a spot between texel centres or covers many texels. Engines offer nearest, bilinear, trilinear and anisotropic filtering. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Trilinear filtering blends the four nearest texels in a single mip level.
- [ ] B. Bilinear filtering blends the four closest texels of one mip level.
- [ ] C. Anisotropic filtering mainly blends between mip levels.
- [ ] D. Nearest filtering takes the single closest texel, giving hard blocky edges that suit pixel art.
- [ ] E. Anisotropic filtering improves surfaces seen at shallow angles, such as a floor stretching away.

**Key:** A=F B=T C=F D=T E=T

**Why:**

- A: That description is bilinear; trilinear also blends between two mip levels.
- B: Bilinear is a blend of a 2 by 2 neighbourhood.
- C: Anisotropic filtering takes extra samples along the stretched direction of the pixel's footprint.
- D: Nearest (point) sampling does no blending.
- E: Shallow viewing angles stretch the footprint, which anisotropic filtering handles.

**Source:** Texture filtering modes

## MA-ch07.16

A floor uses a seamless brick texture at UV scale 1, stretched once across the floor. A developer asks a coding agent: "make the bricks smaller." Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Texel density is the number of texels in the image file.
- [ ] B. A UV scale of 4 repeats the texture four times across the width, so bricks look four times smaller.
- [ ] C. A UV scale of 4 makes the floor mesh four times as large.
- [ ] D. A seamless texture and a repeat wrap mode are needed for tiling to look right.
- [ ] E. Clamp wrap mode repeats the texture, while repeat wrap mode smears the edge texels.

**Key:** A=F B=T C=F D=T E=F

**Why:**

- A: Texel density is texels per unit of surface, such as per metre.
- B: Scaling UVs up makes the image repeat, shrinking each copy.
- C: UV scale changes the mapping, not the geometry.
- D: Seamless edges hide the joins, and repeat mode wraps the coordinates.
- E: The two are swapped; clamp smears edge texels and repeat tiles.

**Source:** Tiling, UV scale and texel density

## MA-ch07.17

A forest has three tree meshes. All three use the same bark shader program, but each tree's material has a different bark texture and tint value. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. One bark texture can be referenced by several materials.
- [ ] B. The scene has three materials that point at the same shader.
- [ ] C. A shader is the program that computes how a surface is drawn, and a material bundles a shader with its values and textures.
- [ ] D. Sharing one shader means the three trees share one material.
- [ ] E. A texture is a kind of material, so there are three shaders, one per texture.

**Key:** A=T B=T C=T D=F E=F

**Why:**

- A: Textures are shared resources that many materials can use.
- B: Three parameter sets mean three materials sharing one program.
- C: The shader is code; the material holds its parameters and texture bindings.
- D: Materials with different values are different materials even with one shader.
- E: A texture is image data a material reads, not a type of material.

**Source:** Material, shader and texture

## MA-ch07.18

Twenty enemies share one material resource. A developer tells a coding agent: "make the enemy that was just hit turn red." The agent changes the colour on the shared material, and all twenty enemies turn red. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A material instance inherits from a parent material and overrides parameter values, reusing the parent's shader.
- [ ] B. Editing a shared material changes each object that references it.
- [ ] C. A per-object material copy compiles a brand-new shader program for each enemy.
- [ ] D. Each node that references a shared material keeps a private copy of it.
- [ ] E. Giving the hit enemy its own material copy or instance, or a per-instance parameter, limits the change to that enemy.

**Key:** A=T B=T C=F D=F E=T

**Why:**

- A: An instance overrides parameters only, so no new shader is needed.
- B: A material is a shared resource, and a reference points at the one resource.
- C: A copy shares the shader program and differs in values.
- D: A reference is not a copy, so edits show up for every referencing node.
- E: A per-object copy or per-instance parameter isolates the change.

**Source:** Shared material versus material instance

## MA-ch07.19

An artist packs sixteen small prop textures into one large texture atlas and changes each prop's UV coordinates to address its own cell. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. The atlas makes each prop's texture sharper, since it is part of a larger image.
- [ ] B. A texture atlas is the same as a mipmap chain.
- [ ] C. Props that share the atlas can share one material, which reduces material switches and draw calls.
- [ ] D. With filtering and mipmaps, colour from neighbouring cells can bleed across a border unless the cells are padded.
- [ ] E. Hardware texture repeat can still tile one prop's cell, because the sampler wraps at the cell edge.

**Key:** A=F B=F C=T D=T E=F

**Why:**

- A: Each prop keeps its original resolution.
- B: An atlas holds different images side by side, while a mip chain holds one image at decreasing sizes.
- C: One material and texture can serve many meshes.
- D: Filtering reads texels near the border, so padding (a gutter) is added.
- E: Wrapping happens at the edge of the whole texture, not of a cell.

**Source:** Texture atlas

## MA-ch07.20

Some pipelines pack three greyscale maps into the red, green and blue channels of one image. A common arrangement called ORM puts ambient occlusion in red, roughness in green and metallic in blue. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A packed image holds data rather than colour, so it is read as linear.
- [ ] B. In an engine that uses smoothness, the green channel can be used as it is.
- [ ] C. A packed ORM image fits a different engine's mask-map slot unchanged, because the channel order is standardised.
- [ ] D. Channel packing replaces three texture reads with one that returns three values.
- [ ] E. If the roughness lookup reads the blue channel by mistake, glossiness follows the metallic map.

**Key:** A=T B=F C=F D=T E=T

**Why:**

- A: The channels hold numbers, so sRGB decoding would alter them.
- B: Smoothness is the inverse of roughness, so the channel would need inverting.
- C: Channel layouts differ between pipelines, so repacking is often needed.
- D: One sample returns three channels at once.
- E: Reading the wrong channel gives the wrong map's data.

**Source:** Channel-packed textures (ORM)

## MA-ch07.21

An artist tells a coding agent: "Use this photo of a brick wall as the wall's colour texture." The photo was taken in strong sun and has a dark shadow across one third. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. De-lighting removes the baked shadows and highlights from the photo before it is used as albedo.
- [ ] B. Baked lighting means lighting computed by the engine each frame.
- [ ] C. A better prompt asks for the de-lit photo as the albedo map and names separate normal and roughness maps.
- [ ] D. The photo can be used as albedo as it is, because engine lighting replaces the shading.
- [ ] E. "Colour texture" is imprecise, because the precise term for the slot is albedo map.

**Key:** A=T B=F C=T D=F E=T

**Why:**

- A: De-lighting is the cleanup that leaves the intrinsic colour.
- B: Baked lighting is precomputed shading stored in the image.
- C: Naming each map type gives the agent exact slots.
- D: The shadow stays in the image and is added on top of runtime lighting.
- E: Albedo map names the slot and the kind of data.

**Source:** De-lit albedo and the albedo map slot

## MA-ch07.22

A developer tells a coding agent: "Make the ship's hull look like polished steel and shinier." Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A precise rewrite is: metallic 1, roughness 0.1, grey steel base colour, with an environment to reflect.
- [ ] B. Polished steel is described by a non-metal with raised specular and a bright albedo.
- [ ] C. Polished steel implies metallic near 1 with low roughness.
- [ ] D. Emission supplies the reflections that a smooth metal needs.
- [ ] E. A smooth metal needs something to reflect, such as an environment map or reflection probe, or it looks dark.

**Key:** A=T B=F C=T D=F E=T

**Why:**

- A: The rewrite names the exact parameters rather than vague adjectives.
- B: A non-metal is a dielectric and does not look like steel.
- C: A bare metal has metallic near 1, and polish means low roughness.
- D: Emission is the surface's own light, not a reflection.
- E: A metal shows only reflections, so it needs a reflection source.

**Source:** Rewriting a vague material prompt

## MA-ch07.23

An artist asks a coding agent to "add depth to the stone wall with a normal map" and expects the stones to stick out of the wall's outline at a corner. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A normal map imported as sRGB colour is decoded correctly.
- [ ] B. A normal map changes shading and leaves the outline flat, so protruding stones need displacement or real geometry.
- [ ] C. If the green channel convention is flipped, the bumps look inverted.
- [ ] D. A height map and a normal map store the same data in the same format.
- [ ] E. A normal map placed in the albedo slot paints the wall purple-blue instead of adding relief.

**Key:** A=F B=T C=T D=F E=T

**Why:**

- A: A normal map is a data texture and is read as linear.
- B: The silhouette comes from the geometry, which a normal map does not change.
- C: Engines differ in whether green points up or down, so a mismatch inverts the relief.
- D: A height map stores heights, while a normal map stores directions.
- E: The slot decides the meaning, so the vectors are drawn as colour.

**Source:** Normal map limits and setup errors

## MA-ch07.24

A developer wants a precise instruction to a coding agent about texture colour spaces for a material pack. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A wrong colour-space flag raises no error and still looks plausible, so the instruction names the colour space.
- [ ] B. Importing the roughness map as sRGB colour is the correct default.
- [ ] C. Lighting maths is done in linear space.
- [ ] D. A normal map flagged as sRGB leaves its vectors unchanged after decoding.
- [ ] E. "Import albedo and emission as sRGB colour, and import normal, roughness and AO as linear data" uses precise terms.

**Key:** A=T B=F C=T D=F E=T

**Why:**

- A: The result is wrong but not an error, so it is easy to miss.
- B: Roughness is data and is read as linear.
- C: Lighting is computed on linear values, so colour images are decoded first.
- D: Decoding changes the stored values, which tilts the surface directions.
- E: It classifies each map as colour or data and names the encoding.

**Source:** Telling an agent colour versus data

## MA-ch07.25

A mobile game has a long cobblestone road that shimmers in the distance, and the game runs out of video memory on low-end phones. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Running out of video memory is fixed by switching to trilinear filtering.
- [ ] B. Shimmer far away is texture aliasing, which mipmaps address.
- [ ] C. Mipmaps reduce video memory because they are smaller copies.
- [ ] D. Block compression reduces video memory use.
- [ ] E. Anisotropic filtering sharpens a road seen at a shallow angle.

**Key:** A=F B=T C=F D=T E=T

**Why:**

- A: Filtering mode changes the look, not the memory use.
- B: Many texels per pixel cause aliasing, and pre-averaged mip levels fix it.
- C: A mip chain adds memory rather than saving it.
- D: Block formats stay compressed in video memory.
- E: Shallow angles stretch the footprint, which anisotropic filtering handles.

**Source:** Matching mipmaps, filtering and compression to problems

## MA-ch07.26

A game has many enemies that share one mesh and one shader. A coding agent is told: "Make a red version of the enemy material and flash the hit enemy." Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Colour variants are built as material instances that override the colour parameter of one parent material.
- [ ] B. "Make a red version" is ambiguous, because the agent might edit the shared material or create a material instance.
- [ ] C. A per-instance parameter limits the flash to the node that was hit.
- [ ] D. A flash on the hit enemy is done by editing the shared material's flash parameter.
- [ ] E. Four colour variants need four shader programs.

**Key:** A=T B=T C=T D=F E=F

**Why:**

- A: An instance reuses the parent's shader and overrides values.
- B: Naming the intended term (material instance versus editing the shared material) removes the ambiguity.
- C: A per-instance parameter is stored per object.
- D: Editing the shared material changes every enemy that uses it.
- E: Variants differ in parameter values, so one shader program serves them.

**Source:** Material instance in an agent prompt

## MA-ch07.27

A level has a large concrete floor and many small props, each with its own small texture. A developer tells a coding agent: "make the floor texture bigger and put the prop textures together." Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. "Put the prop textures together" is a texture atlas, with UVs remapped to each cell.
- [ ] B. "Bigger" is ambiguous, because it could mean a different UV scale, a higher resolution or a different texel density.
- [ ] C. Texel density is the pixel size of the image file.
- [ ] D. A seamless texture is one with high resolution.
- [ ] E. Bleeding across atlas cells comes from filtering at cell borders.

**Key:** A=T B=T C=F D=F E=T

**Why:**

- A: An atlas packs several textures into one, and each prop gets new UVs.
- B: Tiling scale, resolution and density are different things that "bigger" mixes up.
- C: Texel density is texels per unit of surface.
- D: Seamless means the edges match so tiling shows no joins.
- E: Filtering reads texels across a border, so padding is needed.

**Source:** Tiling, UV scale and atlas terms in a prompt

## MA-ch07.28

A developer reports: "The metal shield is pure black, the crevice ambient occlusion has no effect, and the glowing crystal does not light the cave wall. The textures must be broken." The scene has one directional light, no environment lighting and zero ambient light. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. An emissive crystal does not light the wall without a light or global illumination.
- [ ] B. Emission lights nearby walls by default.
- [ ] C. An AO texture that modulates ambient light has no visible effect when ambient light is zero.
- [ ] D. A metal with nothing to reflect looks black, which is a lighting problem and not a texture problem.
- [ ] E. Regenerating the textures is the right fix for the three symptoms.

**Key:** A=T B=F C=T D=T E=F

**Why:**

- A: Emission affects the surface itself, not its neighbours, unless the renderer treats it as a light.
- B: Lighting neighbours needs a light or global illumination.
- C: Occlusion scales ambient light, and zero ambient leaves nothing to scale.
- D: A metal has no diffuse colour and shows only reflections, so it needs a reflection source.
- E: The causes are in the lighting setup, so new textures would not help.

**Source:** Diagnosing materials under lighting
