# Chapter 2: Game art and sound assets

## MA-ch02.1

A developer wants the vocabulary for 2D art straight before instructing a coding agent. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Resolution is the pixel dimensions of an image, written as width by height.
- [ ] B. Texture and sprite are synonyms for one thing.
- [ ] C. A sprite is a 2D image, or one frame of one, drawn as an object in the game scene.
- [ ] D. Aspect ratio is the total pixel count of an image.
- [ ] E. A texture is image data applied to a surface or drawn, and a sprite is drawn using a texture.

**Key:** A=T B=F C=T D=F E=T

**Why:**

- A: A 32 by 48 image has a resolution of 32 by 48 pixels.
- B: The two words name different things.
- C: A sprite is a drawn 2D object.
- D: Aspect ratio is the proportion of width to height.
- E: Texture names the image data and sprite names the thing drawn from it.

**Source:** Sprite, texture, resolution, aspect ratio

## MA-ch02.2

An image generator returns a nearly square picture, and the game uses a wide 16:9 viewport. Check each statement that is true about placing it. Each statement is worth 1 point (5 points total).

- [ ] A. A 16:9 viewport and a nearly square picture have the same aspect ratio.
- [ ] B. Enlarging a low-resolution picture by interpolation adds real detail that was missing.
- [ ] C. Scaling it uniformly to fit keeps the aspect ratio and leaves unused space on one axis.
- [ ] D. Stretching the picture to the viewport size distorts it because the aspect ratios differ.
- [ ] E. Interpolation estimates new pixel values from neighbouring pixels.

**Key:** A=F B=F C=T D=T E=T

**Why:**

- A: 16:9 is much wider than near-square.
- B: Interpolation creates pixels but not information.
- C: Uniform scaling keeps the shape, so one dimension does not fill the viewport.
- D: Non-uniform scaling changes the proportions.
- E: The new values are guesses based on nearby pixels.

**Source:** Aspect ratio and scaling

## MA-ch02.3

A developer asks an image generator for a character sprite "on a transparent background" and gets hero.jpg. In the engine the sprite sits inside a white rectangle. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Lowering the sprite node's opacity makes just the white rectangle transparent.
- [ ] B. JPEG has no alpha channel, so it does not hold transparency.
- [ ] C. Removing a background by colour key can leave light fringe pixels along the edge.
- [ ] D. A white background painted into the pixels counts as transparency.
- [ ] E. An alpha channel stores opacity for each pixel.

**Key:** A=F B=T C=T D=F E=T

**Why:**

- A: Node opacity fades the whole image, character and background.
- B: PNG stores alpha and JPEG does not.
- C: Anti-aliased edge pixels blend the character with the old background.
- D: Painted white is colour content, not an alpha value.
- E: Alpha is the extra channel for opacity.

**Source:** Alpha channel, transparency

## MA-ch02.4

A 32 x 32 pixel-art sprite looks crisp at its original size but looks blurry when shown at four times its size in the game. Check each statement that is true about texture filtering. Each statement is worth 1 point (5 points total).

- [ ] A. Linear filtering blends neighbouring texels when a texture is enlarged, which softens hard edges.
- [ ] B. Nearest filtering takes the colour of the single closest texel, so enlarged pixel art keeps hard edges.
- [ ] C. The instruction "make it sharper" names the setting that should be changed.
- [ ] D. A filter set on one sprite applies to that sprite, while a project default applies to sprites that do not set their own.
- [ ] E. Regenerating the sprite at a higher resolution fixes the blur while linear filtering stays on.

**Key:** A=T B=T C=F D=T E=F

**Why:**

- A: Linear interpolates between neighbouring texels.
- B: Nearest samples one texel per screen pixel.
- C: "Sharper" names a result, not the filter setting.
- D: Scope follows where the setting is placed.
- E: The cause is the sampling mode, not the source size.

**Source:** Nearest versus linear filtering

## MA-ch02.5

A pixel-art game is drawn in a 640 x 360 viewport with nearest filtering and scaled up to fill the window. Check each statement that is true about scaling. Each statement is worth 1 point (5 points total).

- [ ] A. Switching to linear filtering removes the uneven widths with no other change to the look.
- [ ] B. A non-integer scale is harmless to pixel art as long as nearest filtering is on.
- [ ] C. At a non-integer scale with nearest filtering, pixels show uneven widths.
- [ ] D. At an integer scale each source pixel becomes a whole-number block of screen pixels.
- [ ] E. Integer scaling needs linear filtering to look right.

**Key:** A=F B=F C=T D=T E=F

**Why:**

- A: Linear filtering hides the unevenness by blurring everything.
- B: Nearest filtering makes the unevenness visible.
- C: Some source pixels cover more screen pixels than others.
- D: A scale of 2 makes each pixel a 2 by 2 block.
- E: Integer scaling pairs with nearest filtering.

**Source:** Integer scaling of pixel art

## MA-ch02.6

A developer chooses among a sprite sheet, a texture atlas, a tileset and a tilemap. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A tileset is a library of reusable tiles, and a tilemap is the level grid whose cells reference them.
- [ ] B. A sprite sheet and a tileset can both be one PNG in a grid and differ in how the engine uses the cells.
- [ ] C. A sprite sheet is one image holding the frames of an animation, often in equal grid cells.
- [ ] D. An atlas packs many separate images, often of different sizes, into one texture with a record of each rectangle.
- [ ] E. A tilemap is the image file of tile artwork, and a tileset is the painted level layout.

**Key:** A=T B=T C=T D=T E=F

**Why:**

- A: The tileset supplies the pieces and the tilemap places them.
- B: Sheet cells are played as frames, and tileset cells are placed on a map.
- C: The engine slices a sheet into frames played in order.
- D: An atlas is a packing of many images into one texture.
- E: The two terms are swapped.

**Source:** Sprite sheet, atlas, tileset, tilemap

## MA-ch02.7

A designer tells a coding agent "make me a cave tilemap" and wants to paint rooms with 16 x 16 tiles for floor, wall, ceiling and corners. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. The reusable tile artwork is a tileset, and a tilemap is the painted grid.
- [ ] B. The wording could be met by one fixed picture of a finished room.
- [ ] C. The tile size can be left out, because the engine infers it from the image.
- [ ] D. A precise request gives the tile size, the tile types, the edge-matching rule and the file format.
- [ ] E. "Cave tilemap" is a precise request because it fixes tile size and edge rules.

**Key:** A=T B=T C=F D=T E=F

**Why:**

- A: Tileset names the library and tilemap names the layout.
- B: A fixed picture matches the words but cannot be rearranged.
- C: The engine is told the size of one tile to cut the image.
- D: Each item removes a guess.
- E: The phrase leaves out size, types and edge rules.

**Source:** Tileset or tilemap in an instruction

## MA-ch02.8

An image generator is asked for a four-frame walk cycle in one row and returns one 800 x 200 image. The developer slices it into 4 columns and 1 row. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Equal slicing assumes the figures are spaced evenly in the image.
- [ ] B. Frames of one cycle share a baseline and a scale so that they play as one motion.
- [ ] C. Equal slicing centres each figure in its cell.
- [ ] D. Playback speed is set in the engine on the animation, not stored in the image.
- [ ] E. A frame count of 4 shows that the figures are poses of one character.

**Key:** A=T B=T C=F D=T E=F

**Why:**

- A: Slicing cuts at fixed positions.
- B: A shifting baseline makes the animation bob.
- C: Unevenly spaced figures are cut apart or shifted.
- D: Frames per second is an animation setting.
- E: A count says how many cells, not who is drawn.

**Source:** Sprite sheet frame layout

## MA-ch02.9

An interviewer asks why packing 64 separate sprite images into one atlas can make a 2D game run better. Check each statement that is true about a sound answer. Each statement is worth 1 point (5 points total).

- [ ] A. Padding between packed sprites prevents colour bleed when filtering samples near an edge.
- [ ] B. Packing sprites into an atlas changes their drawn size.
- [ ] C. An atlas stores fewer pixels than the separate images it replaces.
- [ ] D. Sprites that share one texture can be batched into fewer draw calls.
- [ ] E. An atlas reduces texture switches rather than reducing the number of pixels stored.

**Key:** A=T B=F C=F D=T E=T

**Why:**

- A: Without padding, sampling can read a neighbour sprite's pixels.
- B: An atlas changes where pixels are stored, not how large the sprite is drawn.
- C: Padding and unused space can make an atlas larger.
- D: No texture switch is needed between them.
- E: The gain is fewer state changes.

**Source:** Atlas, batching, draw call, padding

## MA-ch02.10

A developer will repeat a 256 x 256 grass image over a large ground plane. Check each statement that is true about seamless textures. Each statement is worth 1 point (5 points total).

- [ ] A. An image that looks good as a single picture is therefore seamless.
- [ ] B. With repeat mode the image tiles, and with clamp mode the edge pixels stretch.
- [ ] C. Placing copies side by side tests whether a texture is seamless.
- [ ] D. A seamless (tileable) texture has opposite edges that match, so copies show no visible join.
- [ ] E. A seamless texture shows no visible repetition over a large area.

**Key:** A=F B=T C=T D=T E=F

**Why:**

- A: One view says nothing about how the edges meet their copies.
- B: Repeat and clamp are the two wrap behaviours.
- C: A seam is the join between copies.
- D: Seamlessness is a property of the image's edge content.
- E: Distinctive features recurring at a regular spacing still form a pattern.

**Source:** Seamless textures, repeat versus clamp

## MA-ch02.11

A pixel-art game restricts its art to a 16-colour palette, and a script counts the distinct colours in a generated enemy sprite. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A script can count distinct colours and test each against the palette.
- [ ] B. Anti-aliased edges add in-between colours that are not in the palette.
- [ ] C. An image generator guarantees it will respect a request for these 16 colours.
- [ ] D. An indexed-colour image stores a palette plus an index per pixel, so editing palette entries recolours the sprite.
- [ ] E. A palette is a fixed set of colours the art draws from, and sharing one helps assets look consistent.

**Key:** A=T B=T C=F D=T E=T

**Why:**

- A: The test is exact and can be automated.
- B: Blended edge pixels are extra colours.
- C: Generators approximate such constraints, so the result is checked.
- D: The index data stays the same when palette entries change.
- E: A shared palette gives visual consistency.

**Source:** Palette, indexed colour

## MA-ch02.12

In Godot, an imported PNG has import settings stored in a small file beside it. A developer asks an agent to "make the sprite crisp". Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Mipmaps are pre-shrunk copies of a texture used when it is drawn smaller.
- [ ] B. The settings file records the import choices for that image and belongs in version control with the asset.
- [ ] C. Lossless compression is the recommended mode for pixel art, because VRAM compression shows artifacts in 2D.
- [ ] D. Mipmaps sharpen a sprite that is drawn at its native size.
- [ ] E. "Make the sprite crisp" names the import settings to change.

**Key:** A=T B=T C=T D=F E=F

**Why:**

- A: They help with minified drawing.
- B: A clone without it falls back to default import settings.
- C: Compression artifacts are visible on small 2D images.
- D: Mipmaps add memory and do not sharpen.
- E: The phrase names a result, so the agent may change the wrong setting.

**Source:** Import settings, compression, mipmaps

## MA-ch02.13

A sound effect is stored as uncompressed PCM audio with a sample rate, a bit depth and a number of channels. Check each statement that is true about these terms. Each statement is worth 1 point (5 points total).

- [ ] A. Sample rate is the number of samples taken per second.
- [ ] B. The highest frequency a sample rate can represent is half of it, which is the Nyquist limit.
- [ ] C. Raising the sample rate makes the sound louder.
- [ ] D. Stereo has one channel and mono has two.
- [ ] E. Bit depth sets the number of samples taken per second.

**Key:** A=T B=T C=F D=F E=F

**Why:**

- A: Sample rate is how finely time is sampled.
- B: A signal above half the rate cannot be represented correctly.
- C: Sample rate does not set loudness.
- D: Stereo has two channels and mono has one.
- E: Bit depth is the precision of each sample's level; samples per second is the sample rate.

**Source:** Sample rate, bit depth, channels

## MA-ch02.14

A model generates an 8-bar music track at a steady tempo in 4/4 time to loop behind a level. Check each statement that is true about looping. Each statement is worth 1 point (5 points total).

- [ ] A. A fade-out baked into the end of the file is harmless in a loop.
- [ ] B. A sharp jump between the last and first sample can be heard as a click.
- [ ] C. A track that sounds smooth played once will loop seamlessly.
- [ ] D. Cutting the loop at a bar line keeps the rhythm unbroken across the join.
- [ ] E. The loop point is the position where the track fades out before repeating.

**Key:** A=F B=T C=F D=T E=F

**Why:**

- A: The fade makes a dip and then a jump back up at the join.
- B: A discontinuity in the waveform is audible.
- C: A single play does not test the join.
- D: A loop that ends mid-bar shifts the beat on each repeat.
- E: A loop point is where playback jumps back to, and a fade-out at that point would be audible.

**Source:** Audio loops

## MA-ch02.15

A developer chooses file formats and playback behaviour for a coin-pickup effect and a three-minute background track. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A one-shot plays once per trigger, and a loop repeats until stopped.
- [ ] B. Lossless audio such as WAV or FLAC keeps the samples, and lossy audio such as Ogg Vorbis or MP3 discards detail permanently.
- [ ] C. FLAC is a lossy format because it is compressed.
- [ ] D. Re-encoding a lossy file to another lossy format loses no further detail at the same bit rate.
- [ ] E. The original uncompressed audio can be rebuilt in full from a lossy file.

**Key:** A=T B=T C=F D=F E=F

**Why:**

- A: One-shot and loop are playback behaviours.
- B: Lossy encoding trades information for size.
- C: Compressed does not mean lossy.
- D: Each lossy generation discards more detail.
- E: The discarded detail is gone.

**Source:** Lossless versus lossy; one-shot versus loop

## MA-ch02.16

A game routes sound effects to a bus named SFX and music to a bus named Music, and both feed a Master bus. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A bus is a channel that audio is routed through before output, and its volume and effects apply to the sources routed to it.
- [ ] B. A bus at 0 dB is silent.
- [ ] C. Clipping happens when summed sounds pass the digital maximum, which causes distortion.
- [ ] D. A change of about 6 dB roughly doubles or halves the amplitude.
- [ ] E. A bus at 0 dB passes the signal with no change in level.

**Key:** A=T B=F C=T D=T E=T

**Why:**

- A: Buses group sources for shared control.
- B: Silence is a very large negative decibel value.
- C: Simultaneous sounds add, and the sum can exceed the limit.
- D: The decibel scale is logarithmic.
- E: 0 dB is unity gain.

**Source:** Audio buses, decibels, clipping

## MA-ch02.17

A coin sound is played by one audio player limited to a single simultaneous voice. Three quick pickups produce one clipped blip. A developer says "make the coin sound better". Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. With a limit of one voice, a new play request cuts off the sound still playing.
- [ ] B. "Make the coin sound better" names the voice limit as the problem.
- [ ] C. Raising polyphony cuts off overlapping copies of the sound sooner.
- [ ] D. Making the file louder fixes the cut-off.
- [ ] E. Polyphony is the number of voices that can sound at the same time.

**Key:** A=T B=F C=F D=F E=T

**Why:**

- A: Exceeding the limit drops the earlier sound.
- B: The phrase names no problem.
- C: More voices lets overlapping plays sound together instead of cutting each other off.
- D: Loudness is unrelated to cut-off.
- E: Polyphony counts simultaneous voices.

**Source:** Polyphony

## MA-ch02.18

A studio reviews sprites from an image generator for a pixel-art game. Check each statement that is true about pixel art. Each statement is worth 1 point (5 points total).

- [ ] A. Pixel art means an image with a retro colour scheme.
- [ ] B. Pixel art is authored at low resolution on a grid, with each pixel placed deliberately.
- [ ] C. Pixel art is shown at an integer scale with nearest filtering so each art pixel stays a crisp block.
- [ ] D. A generated image can look like pixel art while lacking a true pixel grid.
- [ ] E. A smoothed, JPEG-compressed picture becomes clean pixel art when shrunk with linear filtering.

**Key:** A=F B=T C=T D=T E=F

**Why:**

- A: The term describes how the image is built.
- B: Control over each pixel defines the style.
- C: Uneven scaling or blending would destroy the pixel shapes.
- D: Blocky look does not guarantee the pixels sit on a grid.
- E: Shrinking blends the artifacts and does not restore a grid.

**Source:** Pixel art

## MA-ch02.19

A developer ships a game with an AI-generated sprite and an AI-generated music track. Check each statement that is true about licensing and provenance. Each statement is worth 1 point (5 points total).

- [ ] A. Provenance is the record of an asset's origin: tool and version, prompt and settings, terms, references and edits.
- [ ] B. An unrecorded reference image can leave its licence doubt attached to the result.
- [ ] C. A tool's terms can restrict use, for example to non-commercial work.
- [ ] D. A provenance record helps regenerate or replace an asset later.
- [ ] E. Writing the prompt gives the developer full copyright in the output.

**Key:** A=T B=T C=T D=T E=F

**Why:**

- A: Provenance is the evidence trail for an asset.
- B: A result derived from an unknown reference inherits the doubt.
- C: Some services carry non-commercial terms.
- D: Recorded settings make an asset reproducible.
- E: Ownership of output depends on the terms and the jurisdiction.

**Source:** Licence and provenance

## MA-ch02.20

A developer tells an image generator and a coding agent: "Make me a cool pixel-art enemy with a walk animation, plus a jump sound and some background music that I can ship." Check each statement that is true about making this precise. Each statement is worth 1 point (5 points total).

- [ ] A. "That I can ship" is a licensing requirement that a provenance record supports.
- [ ] B. "Background music" does not say whether it loops, and "looping track cut on a bar boundary" does.
- [ ] C. "Pixel-art" becomes precise when the size in the viewport and the palette are stated.
- [ ] D. "Cool" tells the generator the viewpoint and the on-screen size.
- [ ] E. "Walk animation" is imprecise, and "four-frame walk cycle as a sprite sheet in equal cells" is precise.

**Key:** A=T B=T C=T D=F E=T

**Why:**

- A: Shipping needs terms and origin to be known.
- B: Loop and one-shot are different playback behaviours.
- C: Size and palette remove guesses.
- D: "Cool" names a taste, not a viewpoint or size.
- E: The precise phrase fixes frame count and layout.

**Source:** Rewriting a vague asset request

## MA-ch02.21

Pixel art looks crisp in an image viewer but smeared when enlarged in the running game. Check each statement that is true about causes and checks. Each statement is worth 1 point (5 points total).

- [ ] A. Changing the filter mode edits the PNG file.
- [ ] B. Texture filtering applies when the texture is sampled at draw time.
- [ ] C. Import settings apply when the source file is converted for the engine.
- [ ] D. Checking at several window sizes tests the effect of scale.
- [ ] E. A JPEG-compressed source with blocky artifacts becomes clean pixel art once nearest filtering is chosen.

**Key:** A=F B=T C=T D=T E=F

**Why:**

- A: The filter is an engine setting, not a change to the image.
- B: Filtering happens when pixels are drawn.
- C: Import happens before the game runs.
- D: Non-integer scales show uneven pixels.
- E: Filtering cannot repair a source that is not on a pixel grid.

**Source:** Blurry pixel art diagnosis

## MA-ch02.22

A game has an eight-frame walking character and a cave level built from forty reusable wall and floor pieces. Check each statement that is true about which term fits. Each statement is worth 1 point (5 points total).

- [ ] A. The cave pieces are a tileset that is painted into a tilemap.
- [ ] B. The eight-frame character is described with a sprite sheet.
- [ ] C. The cells of a tileset are played in order as frames.
- [ ] D. The walking character is described with a tilemap.
- [ ] E. A texture atlas is chosen mainly to reduce texture switches and draw calls.

**Key:** A=T B=T C=F D=F E=T

**Why:**

- A: The tileset holds pieces and the tilemap places them.
- B: A sheet holds animation frames.
- C: Sheet cells play in order and tileset cells are placed individually.
- D: A tilemap is a level grid, not a character animation.
- E: Packing images into one texture reduces state changes.

**Source:** Choosing sheet, atlas, tileset or tilemap

## MA-ch02.23

A game needs a short coin sound, an ambient loop and a three-minute music piece. Check each statement that is true about formats and playback. Each statement is worth 1 point (5 points total).

- [ ] A. Long music is often a lossy file, to save space, that is streamed.
- [ ] B. A short effect is a one-shot that is triggered by an event and may overlap itself.
- [ ] C. Keeping a lossless master rules out a later re-export.
- [ ] D. An ambient loop should have a fade-out baked into its end.
- [ ] E. Sample rate changes loudness.

**Key:** A=T B=T C=F D=F E=F

**Why:**

- A: Streaming plays from disk rather than loading the whole file.
- B: One-shot describes playback once per trigger.
- C: A lossless master is what allows a later re-export without generation loss.
- D: A fade-out would make a dip at each repeat.
- E: Sample rate sets time resolution and the highest frequency.

**Source:** Audio formats and playback

## MA-ch02.24

A student ships an AI-generated sprite made from a reference picture of unknown source, and a music track from a tool whose terms were not read. Check each statement that is true about provenance. Each statement is worth 1 point (5 points total).

- [ ] A. A provenance record lets a problem be traced after the fact.
- [ ] B. A good log entry lists the tool and version, the prompt and settings, references with licences, the terms and the edits.
- [ ] C. An unknown-source reference stops affecting the result once it is deleted from the project.
- [ ] D. Ownership of generated output follows automatically from writing the prompt.
- [ ] E. Some terms require attribution as a duty.

**Key:** A=T B=T C=F D=F E=T

**Why:**

- A: Recorded origin makes tracing possible.
- B: The log is the evidence trail for the asset.
- C: The uncertainty stays with the generated asset.
- D: Ownership depends on terms and jurisdiction.
- E: Attribution is a condition of use in some licences.

**Source:** Provenance log

## MA-ch02.25

A developer covers a large ground surface with a 256 x 256 texture. Check each statement that is true about repeating textures. Each statement is worth 1 point (5 points total).

- [ ] A. Stretching the texture once across a large plane is tiling.
- [ ] B. Without repeat mode, the edge pixels stretch instead of the image repeating.
- [ ] C. The tiling scale is the number of repeats across a surface.
- [ ] D. An engine repeat setting can make a non-seamless image seamless.
- [ ] E. Distinctive features that recur at a regular spacing show as visible repetition even without a seam.

**Key:** A=F B=T C=T D=F E=T

**Why:**

- A: Stretching is scaling, not repeating.
- B: Clamp mode extends the edge pixels.
- C: The scale decides how finely the texture repeats.
- D: Seamlessness is a property of the image content.
- E: Repeating features form a pattern the eye notices.

**Source:** Tiling scale, repeat, clamp

## MA-ch02.26

A game has music, sound effects, dialogue and interface clicks, with separate sliders for music and effects. Check each statement that is true about the audio design. Each statement is worth 1 point (5 points total).

- [ ] A. Headroom is the loudest level that distortion is allowed to reach.
- [ ] B. Each volume slider sets the volume of its own bus.
- [ ] C. Decibels are a linear, absolute scale.
- [ ] D. Ducking automatically lowers the music bus while dialogue plays and restores it afterwards.
- [ ] E. Separate buses for Music, SFX and Dialogue can each feed the Master bus.

**Key:** A=F B=T C=F D=T E=T

**Why:**

- A: Headroom is the margin kept below the digital maximum so sums do not clip.
- B: Each slider acts on one bus.
- C: Decibels are logarithmic and relative.
- D: Ducking keeps speech intelligible.
- E: Buses give independent control and feed the output.

**Source:** Bus layout, ducking, decibels, headroom
