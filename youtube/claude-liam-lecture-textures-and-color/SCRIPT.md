# Script: Textures and Color

**What this is.** The words Liam will say in *Textures and Color*, beat by beat, each with the picture it gets. This is the layout stage: nothing is voiced, captured or rendered yet.

**Why.** So the whole film can be read, and changed, before anyone builds it. A change to a line is cheap now and expensive after the audio and the 4K render.

**Found.** 47 beats, 1907 words, about **10:52** at Liam's measured pace (0.34 s per word, median of 57 shipped films). Preferred band 9 to 11.5 minutes, ceiling 15. Body lanes: capture 27, manim 7, remotion 4, editor 3.

**If it runs long.** Cut, in this order: the tween beat (B26), the brighten beat (B13), the alpha-hole beat (B12), the gray pair (B14, B15), then the from-code beat (B36): each extends an idea another beat already carries. The dissolve build (B19 to B25), the two-renderer reveal (B27 to B31) and the hint rules (B33 to B39) stay: they are the film.

**How to read it.** Blockquotes are the spoken words, exactly as they will be sent to the voice. Numbers are written as words because the voice engine reads them better that way; the screen shows the real figures. Letters in an acronym are spaced for the same reason. "Picture" is what is on screen; "Motion" is the thing the voice can point at.

## Act map

| Act | Title | Beats | Words | About |
|---|---|---|---|---|
| I | Reading a Texture | 7 | 270 | ~1:32 |
| II | Color Is Math | 9 | 330 | ~1:52 |
| III | Noise as a Mask | 10 | 373 | ~2:07 |
| IV | Two Ways to Count Light | 6 | 245 | ~1:23 |
| V | Hint Colors, Not Masks | 9 | 370 | ~2:06 |

## Opening

### BOPEN · identity card · 29 words · ~10 s

> Textures and Color. Learn how a shader reads a texture, how to do math on color, and why the color you type is not always the color you see.

*Picture.* Portrait of Professor Bear (random square portrait, seeded by the film slug), the title "Textures and Color", and the line "How a shader reads images, and why colors shift".

### BIDEA · the question · 37 words · ~13 s

> Hallo. This is Liam, in for Bear. Most people picture a texture as a picture pasted onto a shape. A shader never pastes anything. For every pixel, it looks a color up in a table, by address.

*Picture.* The hesitant writer types: "A texture is a picture
pasted onto a shape." then deletes "pasted onto a shape" and types "looked up by address".

### BDEFS · terms · 76 words · ~26 s

> Six terms. A shader is a small program the graphics card runs to decide how something is drawn. U V is a point's address on a shape, from zero to one across and down. A texture is an image a shader can read by address. A channel is one of red, green, blue or alpha. Alpha is how visible a pixel is: zero invisible, one solid. And the renderer is the part of Godot that draws.

*Picture.* "Terms In This Lecture": **Shader** — a small program the graphics card runs to decide how something is drawn; **UV** — a point's address on the shape: 0 to 1 across, 0 to 1 down; **Texture** — an image a shader can read by address; **Channel** — one of red, green, blue or alpha; **Alpha** — how visible a pixel is: 0 invisible, 1 solid; **Renderer** — the part of Godot that draws

## Act I: Reading a Texture

### B01 · 44 words · ~15 s

> Watch this sprite burn away. One number drives it, and a picture of soft clouds decides where it burns first. By the end of this film you will build that effect, and know why the colors you pick can look different in another renderer.

*Picture.* Act title 'Reading a Texture' (serif 40) top-left. A real Godot render in a framed window on the cream stage: the teal test sprite sits whole, then burns away from the edges in, a yellow-orange-red rim around every hole, while a thin 0 to 1 strip under the window carries a marker labelled 'progress' that rides from 0 to 1 with the burn.

*Motion.* The sprite burns away as the progress marker rides from 0 to 1.

*Lane.* capture · `ShaderLab` · runner-up: manim drawing of a sprite dissolving

*Capture to record.* C01: Lab sprite (teal test sprite, scale to fit 640x360), lab-shaders/18-dissolve.gdshader; noise_tex = NoiseTexture2D (FastNoiseLite seed 7, frequency 0.02, 256 x 256: the Lab's 'noise' kind); ramp_tex = GradientTexture1D (#8A2A12, #F08A2C, #F7D46B, 256 wide); `--animate progress:0.05:0,0.97:1` (fractions of the beat), 30 fps, Forward+, scripted sweep (label it). Verified frames: evidence/planning-checks/png/plus-a3-18-dissolve-*.png (sprite 23,512 px whole at 0; 0 px at 1).

### B02 · 39 words · ~13 s

> First, the table. A texture is a grid of colors, and every entry has an address: U V, zero to one across, zero to one down. Hand the table an address, and it hands back the color stored there.

*Picture.* A 6-by-6 grid of cells: the cream letter F on teal (the film's tiny table), with a one-cell teal margin. Beside it a swatch box with four numbers under it, and under the grid an address readout '(u, v)'. A terracotta dot (the address) starts at the top-left cell, a thin line runs from the dot to the swatch, the swatch takes that cell's color and the four numbers fill in (0.98, 0.98, 0.96, 1.0). Labels: 'texture', 'address', 'color'.

*Motion.* The address dot hops from cell to cell and, each time, the swatch changes to that entry's color.

*Lane.* manim · `B02_LookupTable` · runner-up: ShaderLab with a Lab render

### B03 · 38 words · ~13 s

> In code, the lookup is one function: texture, then the table's name, then the address. It returns a color. Fragment runs once for each pixel, so every pixel asks with its own address, and the shape fills in.

*Picture.* Code card at left (the four-line lookup shader); at right a real Godot window: a plain Color Rect that now shows the 8-by-8 teal and cream checker picture. A terracotta ring moves to one cream cell and then one teal cell, each with its address as a readout.

*Motion.* The ring hops to a cell, and its address and color are read out.

*Lane.* capture · `ShaderLab` · runner-up: LectureCodeTrace alone

*Capture to record.* C02: Lab rect 360x360 logical, lab-shaders/01-lookup.gdshader, --tex tex=checker, still PNG at 4K. Verified probes: (0.06, 0.06) = (0.980, 0.977, 0.961) cream; (0.19, 0.06) = (0.372, 0.639, 0.569) teal.

### B04 · 43 words · ~15 s

> Where does the table come from? A uniform of type sampler two D is a slot you fill from outside. Any texture fits: a small picture, a gradient, noise. It stretches across the shape, because the address always runs from zero to one.

*Picture.* Code card at left with the uniform line highlighted. At right the same real Godot window shows three tables in turn with no change to the code: the small cream F on teal (smeared, because it is tiny), the red-green gradient, the grey noise. A caption under the window says 'same code'.

*Motion.* The window's picture changes from table to table while the code stays put.

*Lane.* capture · `ShaderLab` · runner-up: manim: a slot with three tables plugging in

*Capture to record.* C03: three Lab stills of lab-shaders/01-lookup.gdshader on a 360x360 rect, joined with ffmpeg, one third of the clip each: tex = tiny_f (the 6x6 F, default filter: smeared), gradient, noise (Lab kinds). Verified: F centre probes (0.25, 0.25) cream, (0.0833, 0.0833) teal; the F at (0.15, 0.25) blends to (0.608, 0.769, 0.722).

### B05 · 41 words · ~14 s

> That small picture came out smeared. An address can land between two entries, and by default the graphics card blends the four nearest. Add filter nearest, and it takes the closest entry only: crisp blocks, which is what pixel art wants.

*Picture.* Code card at left with the hint highlighted. At right two real panels of the small F table side by side: on the left the smeared default, on the right the crisp blocks after the hint. Panel labels 'default' and 'filter_nearest'.

*Motion.* The right panel snaps from smeared to crisp blocks next to the unchanged left one.

*Lane.* capture · `ShaderLab` · runner-up: ShaderLab with one panel and a toggle

*Capture to record.* C04: two Lab renders of the 6x6 F table on 360x360 rects, side by side (ffmpeg hstack): left lab-shaders/01-lookup.gdshader, right lab-shaders/02-nearest.gdshader; right panel revealed at 40 % of the beat. Verified at (0.15, 0.25): linear (0.608, 0.769, 0.722) blend, nearest (0.372, 0.639, 0.569) the closest entry.

### B06 · 32 words · ~11 s

> Because it is a lookup, you can ask for any address you like. Ask for one minus the horizontal address, and the picture flips. The table never changed. Only where you looked.

*Picture.* Code card at left with the address line highlighted. At right two real panels: the F table as it is, then, beside it, the same table flipped left to right (the F's stem moves from left to right). Labels 'same table' and 'new address'.

*Motion.* The F's stem jumps from the left side to the right side as the new address is applied.

*Lane.* capture · `ShaderLab` · runner-up: manim: a flipped grid

*Capture to record.* C05: two Lab renders of the F table (filter_nearest) on 360x360 rects, hstack: left lab-shaders/02-nearest.gdshader, right lab-shaders/03-flip.gdshader; right panel revealed at 40 %. Verified: stem texel (0.25, 0.4167) cream in the original and teal when flipped; (0.75, 0.4167) teal in the original and cream when flipped.

### B07 · 33 words · ~11 s

> Ask for twice the address, and half the lookups fall off the end of the table. With repeat disable, the edge entries stretch outward. With repeat enable, the table starts over, and tiles.

*Picture.* Code card at left (repeat enable). At right two real panels of the F table asked for twice the address: on the left with repeat disabled a half-size F in the top-left corner with the edge entries smeared out to the right and downward; on the right with repeat enabled a two-by-two tiling of F. Labels 'repeat_disable' and 'repeat_enable'.

*Motion.* The left panel streaks outward; the right panel tiles.

*Lane.* capture · `ShaderLab` · runner-up: manim: a table with an arrow running off its edge

*Capture to record.* C06: two Lab renders of the F table on 360x360 rects, hstack: left lab-shaders/04-repeat-off.gdshader (revealed at 25 %), right lab-shaders/05-repeat-on.gdshader (revealed at 65 %). Verified probes (0.625, 0.2083) and (0.125, 0.625): repeat off = teal, teal; repeat on = cream, cream.

## Act II: Color Is Math

### B08 · 41 words · ~14 s

> What comes back from a lookup is a vec four: four numbers, each from zero to one. Red, green, blue, and alpha. Orange is one, one half, zero, one. A color is only numbers, so you can do arithmetic on it.

*Picture.* Act title 'Color Is Math' (serif 40) top-left. A large orange swatch (1.0, 0.5, 0.0, 1.0) with four labelled bars beside it, R G B A, each an outline track with a terracotta dot at its value. A label 'vec4: a bundle of four numbers'. The G bar slides up to 0.9 and the swatch turns yellow-orange; the B bar slides to 0.4 and it pales.

*Motion.* Sliding one bar changes the swatch: the color is nothing but the four numbers.

*Lane.* manim · `B08_FourNumbers` · runner-up: ShaderLab

### B09 · 38 words · ~13 s

> A sprite brings a table of its own, named texture, in capitals. Before your code runs, color already holds that lookup, multiplied by the node's modulate. Overwrite color with a plain lookup, and the modulate is thrown away.

*Picture.* Code card at left (COLOR = texture(TEXTURE, UV)). At right two real panels of the four-patch picture on a sprite whose modulate is 50 % gray: on the left an empty fragment (the picture is darker), on the right the plain lookup (the picture is full bright). Labels 'empty: keeps modulate' and 'plain lookup: drops it'.

*Motion.* The right panel jumps to full brightness as the plain lookup throws the modulate away.

*Lane.* capture · `ShaderLab` · runner-up: manim: COLOR box with two inputs multiplied

*Capture to record.* C07: two Lab renders of the swatch picture on a Sprite2D at fit scale with modulate #808080, hstack: left lab-shaders/06-empty.gdshader (revealed at 20 %), right lab-shaders/07-own-texture.gdshader (revealed at 62 %); label 'scripted'. Verified (rose patch): left (0.451, 0.176, 0.275), right (0.902, 0.349, 0.549) (the picture untouched is the same as the right).

### B10 · 35 words · ~12 s

> Multiply the color by a tint. A channel times one stays, times a half it halves. This tint keeps all the red, most of the green, and half the blue, so the picture turns warm.

*Picture.* Code card at left (a tint color multiplied into COLOR.rgb). At right the real four-patch picture, untouched, then the shader is switched on and every patch warms: the rose deepens, the sky patch turns slate. A readout '1.0, 0.7, 0.5' (the tint) appears.

*Motion.* The picture turns warm the moment the tint is switched on.

*Lane.* capture · `ShaderLab` · runner-up: manim: a bar of each channel shrinking

*Capture to record.* C08: Lab sprite (swatches kind: rose, leaf, sky, sand), shader lab-shaders/08-tint.gdshader switched on with `--material-at` at 25 % of the beat, 30 fps, Forward+, label 'scripted'. Verified patch centres: rose (0.902, 0.349, 0.549) -> (0.902, 0.243, 0.275); leaf (0.400, 0.651, 0.349) -> (0.400, 0.455, 0.176); sky (0.400, 0.502, 0.851) -> (0.400, 0.353, 0.427); sand (0.878, 0.690, 0.290) -> (0.878, 0.482, 0.145).

### B11 · 31 words · ~10 s

> One minus the color flips it. Zero becomes one, one becomes zero, and a half stays put. Do it to red, green and blue, and every patch turns into its opposite.

*Picture.* Code card at left (COLOR.rgb = 1.0 - COLOR.rgb). At right the real four-patch picture, untouched, then switched: rose becomes green, leaf becomes purple, sky becomes brown, sand becomes blue. A readout '0.90 → 0.10' on the rose patch.

*Motion.* Every patch flips to its opposite the moment the shader switches on.

*Lane.* capture · `ShaderLab` · runner-up: manim: a channel bar flipping

*Capture to record.* C09: Lab sprite (swatches), lab-shaders/09-invert.gdshader switched on with `--material-at` at 25 % of the beat, 30 fps, Forward+, 'scripted'. Verified: rose (0.902, 0.349, 0.549) -> (0.098, 0.651, 0.451); leaf -> (0.600, 0.349, 0.651); sky -> (0.600, 0.498, 0.149); sand -> (0.122, 0.310, 0.710).

### B12 · 34 words · ~12 s

> Careful with the fourth number. Flip alpha too, and the sprite turns see-through, while the empty space around it becomes a solid white card. Alpha is a channel like the others: only a number.

*Picture.* Code card at left (COLOR = vec4(1.0) - COLOR). At right the real teal test sprite on the stage, then switched: the sprite becomes a see-through hole and the empty square around it becomes a solid white card. Readouts 'alpha 1→0' on the sprite and 'alpha 0→1' on the card.

*Motion.* The sprite punches out as a hole in a white card the moment the shader switches on.

*Lane.* capture · `ShaderLab` · runner-up: manim: alpha bar flipping

*Capture to record.* C10: Lab sprite (the teal test sprite with eyes), lab-shaders/10-invert-all.gdshader switched on with `--material-at` at 25 % of the beat, 30 fps, Forward+, 'scripted'. Verified: centre of the sprite = the stage color (0.851, 0.835, 0.792) (alpha 0); a transparent corner = (1.0, 1.0, 1.0) (alpha 1). GATE V note: pale card on a pale stage.

### B13 · 36 words · ~12 s

> Add instead of multiply, and the picture brightens. Add a ramp that grows to one, and every patch ends in flat white. Ordinary two-D drawing cuts every number off at one, so the extra is lost.

*Picture.* Code card at left (COLOR.rgb += UV.x). At right the real four-patch picture, untouched, then switched: the left edge is only a little brighter and the right edge is flat white, every patch ending in the same white. A ring on the flat white area and a readout 'cut at 1'.

*Motion.* The picture washes out toward flat white from left to right when the shader switches on.

*Lane.* capture · `ShaderLab` · runner-up: manim: a bar growing past 1 and stopping

*Capture to record.* C11: Lab sprite (swatches), lab-shaders/11-brighten.gdshader switched on with `--material-at` at 25 % of the beat, 30 fps, Forward+, 'scripted'. Verified: rose patch (UV.x about 0.25) (1.0, 0.596, 0.796); leaf patch (UV.x about 0.75) (1.0, 1.0, 1.0). A separate script check (verify-clamp.gd): a shader writing 1.5, 1.2, 0.5 reads back 1.0, 1.0, 0.502 with HDR 2D off and 1.5, 1.2, 0.5 with it on.

### B14 · 32 words · ~11 s

> To make gray, give red, green and blue the same number. The crude way copies one channel. Copy red, and the rose turns bright, while the leaf and the sky turn dark.

*Picture.* Code card at left (gray = COLOR.r, then vec3(gray)). At right the real four-patch picture, untouched, then switched to gray: rose and sand turn light gray, leaf and sky turn a much darker gray. Readouts on three patches: 0.90, 0.40, 0.40.

*Motion.* Three of the patches jump to very different grays the moment the shader switches on.

*Lane.* capture · `ShaderLab` · runner-up: manim: three bars and their grays

*Capture to record.* C12: Lab sprite (swatches), lab-shaders/12-gray-red.gdshader switched on with `--material-at` at 25 % of the beat, 30 fps, Forward+, 'scripted'. Verified gray values: rose 0.902, leaf 0.400, sky 0.400, sand 0.878.

### B15 · 40 words · ~14 s

> Better: weigh the channels by how bright each looks to the eye. About twenty-one percent red, seventy-two percent green, seven percent blue. Dot multiplies and adds them up. Now the rose, the leaf and the sky land on close grays.

*Picture.* Code card at left (gray = dot(COLOR.rgb, vec3(0.2126, 0.7152, 0.0722))). At right two real panels of the four-patch picture in gray: on the left the crude red-channel version, on the right the weighted one where the rose, the leaf and the sky land on close grays and sand stays lightest. Readouts 0.48, 0.58, 0.51 on the weighted panel.

*Motion.* The right panel's three patches settle at nearly the same gray while the left panel's do not.

*Lane.* capture · `ShaderLab` · runner-up: manim: a bar of weights

*Capture to record.* C13: two Lab renders of the swatch picture, hstack: left lab-shaders/12-gray-red.gdshader, right lab-shaders/13-gray-weighted.gdshader, both switched on with `--material-at` at 12 %; right panel revealed at 40 %. Verified weighted grays: rose 0.482, leaf 0.577, sky 0.506, sand 0.702. The weights follow Rec. 709: derived from the primaries in evidence/planning-checks/derive-bt709-weights.py; Godot's Color.get_luminance() returns the same three weights.

### B16 · 43 words · ~15 s

> Mix blends two colors by an amount from zero to one. Here it blends the picture with its own gray: zero is all color, one is all gray. The amount can be one number for everything, or a different number at every pixel.

*Picture.* Code card at left (an amount uniform; mix of the color and its gray). At right the real four-patch picture draining of its color as the amount sweeps from 0 to 1, a thin 0 to 1 strip under the window with a marker riding the amount.

*Motion.* The picture drains from full color to gray while the amount marker rides from 0 to 1.

*Lane.* capture · `ShaderLab` · runner-up: ShaderLab stills at three amounts

*Capture to record.* C14: Lab sprite (swatches), lab-shaders/14-mix.gdshader, `--animate amount:0.1:0,0.85:1`, 30 fps, Forward+, 'scripted'. Verified patch centres: amount 0.0 the picture untouched; amount 0.5 rose (0.690, 0.416, 0.514), leaf (0.486, 0.612, 0.463), sky (0.451, 0.502, 0.678), sand (0.788, 0.694, 0.494); amount 1.0 the weighted grays (0.482, 0.577, 0.506, 0.702).

## Act III: Noise as a Mask

### B17 · 42 words · ~14 s

> Not every texture is a picture. This one is noise: soft clouds made of numbers, one from zero to one at every pixel. Read each number as an amount of teal, and you have a mask: how much of something to show.

*Picture.* Act title 'Noise as a Mask' (serif 40) top-left. Code card at left (COLOR.a = the noise value). At right a real Godot window: a teal Color Rect whose opacity follows the noise, so soft teal clouds fade into the stage. Three readouts on three spots: 0.08 (nearly nothing), 0.50, 0.91 (nearly solid teal).

*Motion.* Readouts land on three spots of the clouds, low, middle and high.

*Lane.* capture · `ShaderLab` · runner-up: manim: a grey picture turning into numbers

*Capture to record.* C15: Lab rect 360x360 logical with the node color #5FA391 (a ColorRect color, not a shader literal), lab-shaders/15-noise-mask.gdshader, noise_tex = NoiseTexture2D (FastNoiseLite seed 7, frequency 0.02, 256 x 256), still PNG at 4K. Verified noise values at (0.363, 0.454) = 0.082, (0.181, 0.606) = 0.502, (0.637, 0.698) = 0.906; the picture is a normalized noise: min 0.0, max 1.0.

### B18 · 46 words · ~16 s

> You do not draw it. In the Inspector, open the slot's menu and choose Noise Texture two D under New. Click it, then open its Noise slot the same way, and choose Fast Noise Lite. Godot generates the clouds, at the size and seed you choose.

*Picture.* Five real frames of the Godot editor's Inspector (a scripted editor session) for a Sprite2D whose shader has a Noise Tex slot, joined by slow cross-dissolves: the slot empty; the slot's menu open, a heading New above bare class names, NoiseTexture2D ringed; inside the NoiseTexture2D, its Noise slot's menu open (heading New, FastNoiseLite) with FastNoiseLite ringed; the NoiseTexture2D view with FastNoiseLite in its Noise slot and Width and Height ringed (this view has no preview); then the FastNoiseLite itself, where the grey clouds preview appears, with Seed ringed. One terracotta ring on the row or entry being named.

*Motion.* The ring moves entry to entry as the voice names each step: the slot, NoiseTexture2D, FastNoiseLite, the size, the seed and the clouds.

*Lane.* editor · `ShaderLab` · runner-up: GodotDevWorkbench (labelled reconstruction)

*Capture to record.* E1 (DONE by script, 2026-10-13, editor driver; README 2.7): five full frames from `_godot-shaders-series/editor-capture/png/1920x1080/textures-and-color/` (native 3456x1944 twins beside them in png/3456x1944/): textures-and-color_E1-1a_noise_tex-slot-empty, E1-1b_noise_tex-dropdown-open, E1-2c_noise-dropdown-open, E1-3a_NoiseTexture2D-width-height-noise-FastNoiseLite, E1-3b_inside-FastNoiseLite-preview-clouds. Join them with ffmpeg cross-dissolves at 0.2, 0.58, 0.74 and 0.9 of the beat (the voice's 'Click it' falls inside 45 to 55 %, so the click state E1-2b, the NoiseTexture2D with its Noise empty, is a spare and is not shown); ring boxes are fractions of the whole 1920x1080 frame (no crop). Real labels: the slot's menu has a Search box, a heading New, 19 bare class names (NoiseTexture2D last), then Quick Load... and Load...; inside the NoiseTexture2D the Noise slot's menu is the heading New, FastNoiseLite, Quick Load..., Load...; the NoiseTexture2D view lists Width, Height, Generate Mipmaps, Noise, Color Ramp, Seamless, Invert, In 3D Space, As Normal Map, Normalize and has NO preview; the grey clouds are in the FastNoiseLite view (preview with a 3D button, Noise Type, Seed, Frequency, Offset). No pointer is visible (Movie Maker records the window only): the clicks are the driver's, so the label says scripted editor session.

### B19 · 31 words · ~10 s

> Now cut with it. Step compares each number with a threshold: below it, zero; at or above it, one. Slide the threshold up, and the clouds shrink into blobs that disappear.

*Picture.* Code card at left (COLOR.a = step(threshold, n)). At right the teal Color Rect: at threshold 0 solid teal, then as the threshold sweeps up the cloud edges turn hard and the teal shrinks into blobs and disappears. A thin 0 to 1 strip under the window with a marker riding the threshold.

*Motion.* The teal shrinks into hard-edged blobs and vanishes as the threshold marker rides from 0 to 1.

*Lane.* capture · `ShaderLab` · runner-up: manim: a number line with a threshold

*Capture to record.* C16: Lab rect 360x360 logical with node color #5FA391, lab-shaders/16-step-cut.gdshader, noise_tex = the same NoiseTexture2D, `--animate threshold:0.1:0,0.97:1`, 30 fps, Forward+, 'scripted'. Verified teal share of the frame: threshold 0.25 = 92.2 %, 0.5 = 51.6 %, 0.75 = 8.4 % (plus-analysis.txt).

### B20 · 37 words · ~13 s

> Use that cut on a sprite. If a pixel's noise is below the threshold, discard it, and the background shows through. Call the threshold progress. As it climbs from zero to one, the sprite is eaten away.

*Picture.* Code card at left (if the noise is below progress, discard). At right the real teal test sprite on the stage: ragged holes open in the shape of the clouds and grow until the sprite is gone, with the stage showing through every hole. A 0 to 1 strip under the window with a marker riding progress.

*Motion.* Holes open and grow in the shape of the clouds as the progress marker rides from 0 to 1.

*Lane.* capture · `ShaderLab` · runner-up: manim: a sprite with holes appearing

*Capture to record.* C17: Lab sprite (teal test sprite, fit scale), lab-shaders/17-dissolve-cut.gdshader, noise_tex = the same NoiseTexture2D, `--animate progress:0.1:0,0.97:1`, 30 fps, Forward+, 'scripted'. Verified sprite pixels left (of 23,512): progress 0.25 = 90.0 %, 0.5 = 46.0 %, 0.75 = 8.7 %, 1.0 = 0 (plus-analysis.txt).

### B21 · 35 words · ~12 s

> To make it burn, color the pixels that are about to go. They sit right above the threshold: a thin band of noise values, a tenth wide. Everything in that band is next to disappear.

*Picture.* A horizontal strip of noise values from 0 to 1 drawn in light-to-mid grays with end labels '0' and '1'. A terracotta marker 'threshold' sits on the strip with a bracket just to its right marking a band one tenth wide, labelled 'band: a strip of noise values, a tenth wide'. Below the strip a row of twelve pixel cells, each holding a noise value: cells whose value is below the marker are drawn as empty outlines, cells inside the band glow yellow-orange-red, cells beyond stay teal. The marker slides right; the band moves with it and cells burn, then vanish, in order.

*Motion.* The marker slides right and the band right behind it lights up the pixels that are next to go.

*Lane.* manim · `B21_Band` · runner-up: ShaderLab

### B22 · 45 words · ~15 s

> What color? Look it up in a second table: a ramp from dark red through orange to yellow. The nearer a pixel is to the edge, the hotter it is, and the further along the ramp you read. The address is a number you computed.

*Picture.* Left, a real Lab crop of the burning edge (a zoomed still of the dissolve at progress 0.5 with a thick yellow-to-dark-red rim); at the bottom the real burn ramp as a horizontal strip labelled 'ramp: a smooth run of colors', end labels '0' and '1' (dark red at 0, yellow at 1). Three sample pixels on the edge crop are boxed in terracotta; from each a thin line runs down to an address on the strip: the pixel nearest the hole to 1.0 (yellow), a middle one to 0.5 (orange), the outermost to 0.0 (dark red), each with a readout 'heat 1.0 / 0.5 / 0.0'.

*Motion.* Lines run from three pixels on the edge to three addresses on the ramp, the nearest pixel to the hottest end.

*Lane.* manim · `B22_RampLookup` · runner-up: ShaderLab with the ramp strip

### B23 · 28 words · ~10 s

> Here is the whole shader. Noise decides who goes first. Progress is the dial. The ramp colors the edge. Twelve lines of code, and the sprite burns away.

*Picture.* The full dissolve shader at left (twelve lines of code); at right the real sprite burning away with its yellow-to-red rim as progress sweeps from 0 to 1, a 0 to 1 strip under the window carrying a marker. The highlight walks through the code as the voice names noise, progress and the ramp.

*Motion.* The highlight walks the code while the sprite burns away.

*Lane.* capture · `ShaderLab` · runner-up: LectureCodeTrace alone

*Capture to record.* C18: Lab sprite (teal test sprite, fit scale), lab-shaders/18-dissolve.gdshader, noise_tex = NoiseTexture2D (seed 7, frequency 0.02, 256), ramp_tex = GradientTexture1D (#8A2A12, #F08A2C, #F7D46B), `--animate progress:0.1:0,0.97:1`, 30 fps, Forward+, 'scripted'. Verified (sprite 23,512 px): progress 0 whole, 0.25 = 20,391 sprite px + 2,371 burning, 0.5 = 8,815 + 4,132, 0.75 = 921 + 1,655, 1.0 = none.

### B24 · 35 words · ~12 s

> Now swap the table. Put a left to right gradient where the noise was, and the same shader wipes instead of dissolves. Nothing in the code changed. A mask is only a table of amounts.

*Picture.* The same dissolve shader at left with the noise slot highlighted. At right the real sprite: a straight burning edge sweeps across it from left to right, leaving the right part intact until it arrives. A caption 'gradient, not noise'.

*Motion.* A straight burning edge travels left to right across the sprite.

*Lane.* capture · `ShaderLab` · runner-up: ShaderLab with the noise sweep next to it

*Capture to record.* C19: Lab sprite (teal test sprite, fit scale), lab-shaders/18-dissolve.gdshader, noise_tex = the Lab's 'gradient' kind (its red channel runs 0 -> 1 left to right), ramp_tex as C18, `--animate progress:0.1:0.15,0.97:0.85`, 30 fps, Forward+, 'scripted'. Verified left edge of what is left at progress 0.35 / 0.5 / 0.65 = x 258 / 306 / 353 of 640.

### B25 · 41 words · ~14 s

> Check the ends. At zero the sprite should be untouched. The first version of this shader failed that: some pixels already burned, because at zero the band covered the darkest clouds. The fix: start the threshold a band's width below zero.

*Picture.* The fixed shader at left with the cut line highlighted. At right two real panels of the sprite at progress 0: on the left the first version, with a few specks of burning already on it, ringed in terracotta with a readout '160 pixels burning'; on the right the fixed version, perfectly clean. Labels 'first version' and 'fixed'.

*Motion.* The ring lands on the specks in the left panel while the right panel stays clean.

*Lane.* capture · `ShaderLab` · runner-up: manim: a band hanging off the noise range

*Capture to record.* C20: two Lab renders of the sprite at progress 0, hstack: left lab-shaders/19-dissolve-first-try.gdshader, right lab-shaders/18-dissolve.gdshader (same noise and ramp as C18); right revealed at 60 %. Verified: first version 160 burning pixels in three specks (boxes in the 640x360 frame: (341,129)-(348,137), (271,160)-(291,175), (287,185)-(308,205)); fixed version 0. At progress 1 both are empty.

### B26 · 33 words · ~11 s

> To drive it from the game, tween progress. One trap: a tween needs a starting value, so set progress from code first. Skip that, and Godot answers that the property does not exist.

*Picture.* A three-line GDScript card at left (set progress to 0.0; create a tween; tween the shader parameter progress to 1.0 over two seconds). At right the real sprite burning away over two seconds. A caption under the window quotes the real error that line one prevents.

*Motion.* The sprite burns away over two seconds once the tween lines run.

*Lane.* capture · `ShaderLab` · runner-up: ShaderLab with only the error text

*Capture to record.* C21: scene with a Sprite2D 'Sprite' using lab-shaders/18-dissolve.gdshader (noise and ramp as C18); the scene script runs `start_tween` through `--call-at` at 25 % of the beat: set_shader_parameter("progress", 0.0) then a Tween to 1.0 over 2.0 s; 30 fps, Forward+. Verified in run-10 (verify-tween-progress.gd): with the first line progress 0.4998 at 0.5 s, sprite gone by 1.2 s; without it the console prints 'The tweened property "shader_parameter/progress" does not exist' and nothing moves.

## Act IV: Two Ways to Count Light

### B27 · 45 words · ~15 s

> Now the part that surprises people. Here is one three-D shader, run in two renderers. It blends two grays, point two and point eight, halfway. You would expect point five. On this Mac, Forward Plus reads point six in the middle. Compatibility reads point five.

*Picture.* Act title 'Two Ways to Count Light' (serif 40) top-left. Code card at left (a spatial unshaded shader that mixes two source-color grays by UV.x). At right two real horizontal gray strips stacked, the same shader in two renderers: top labelled 'Forward+', bottom 'Compatibility'. A readout at the middle of the top strip '0.60', then at the middle of the bottom strip '0.50'.

*Motion.* The two strips differ visibly at the middle, and the readouts land top then bottom.

*Lane.* capture · `ShaderLab` · runner-up: LectureEvidenceTable with the two numbers

*Capture to record.* C22: two Lab renders of lab-shaders/20-blend-3d.gdshader (quad3d, 1280x360 logical each), vstack: top --renderer forward_plus, bottom --renderer gl_compatibility; stills. Verified at the middle (0.5, 0.5): Forward+ 0.600, Mobile 0.600, Compatibility 0.502; at 0.1: 0.329 / 0.333 / 0.259; at 0.9: 0.765 / 0.765 / 0.741. GATE T note: the 0.2 gray end is dark; strips are tall, so they are not text-shaped.

### B28 · 32 words · ~11 s

> Neither renderer is broken. A pixel probe measures one thing: what this renderer drew for this shader. And a test that runs without a window has no pixels to read at all.

*Picture.* A left-to-right chain of four outline boxes: 'numbers you typed', 'shader math', 'the renderer', 'pixel on screen'. A terracotta token travels the chain. A magnifier (a circle and a handle) lands on the last box with the label 'probe: reads one pixel's color'. Under the chain a second, shorter chain 'no window' leads to a box 'no pixels' that is struck through, labelled 'null'.

*Motion.* The token travels the chain and the magnifier lands at its end; the lower chain stops at an empty box.

*Lane.* manim · `B28_Probe` · runner-up: LectureEvidenceTable

### B29 · 46 words · ~16 s

> Why do they differ? There are two ways to count brightness. A color picker's numbers are spaced for the eye: that is s R G B. Light adds up in a straight line: that is linear. The two agree at zero and one, and disagree between.

*Picture.* Axes: the horizontal axis 'typed number (sRGB: the scale color pickers use)' from 0 to 1, the vertical 'light (linear: numbers that add up like light)' from 0 to 1. A dashed diagonal marked 'if the two agreed'. The real sRGB curve is drawn from (0, 0) to (1, 1), bending under the diagonal. Rings on the two ends where it meets the diagonal. A dot slides along the curve to x = 0.5 and drops a dashed line to y = 0.21 with the label '0.5 typed = 0.21 light'.

*Motion.* The curve draws itself under the diagonal; a dot rides it and drops to 0.21 at 0.5.

*Lane.* manim · `B29_TwoScales` · runner-up: ShaderLab

### B30 · 35 words · ~12 s

> Blend point two and point eight halfway. Average the typed numbers, and you get point five. Convert to light, average there, and convert back, and you get point six. Same two colors, two different answers.

*Picture.* The same axes and curve. Two dots on the curve at typed 0.2 and 0.8 (light 0.03 and 0.60) joined by a thin chord. Path A: a dashed vertical from typed 0.5 marks the average of the typed numbers, a marker on the horizontal axis labelled '0.5'. Path B: a dashed horizontal at light 0.32 (the average of the two lights) runs to the curve and drops to the horizontal axis at '0.6'. Both markers stay on the axis, labelled 'average the typed numbers' and 'average the light'.

*Motion.* Two dashed paths trace to two different markers on the axis, 0.5 and 0.6.

*Lane.* manim · `B30_TwoMidpoints` · runner-up: ShaderLab

### B31 · 40 words · ~14 s

> Forward Plus and Mobile work in light, and convert to s R G B only to show the picture. In this test, Compatibility blends the numbers as typed. That is why one reads point six and the other point five.

*Picture.* A three-row table, one row ringed as each renderer is named, the third column carrying the real measured pixel and the fourth saying where each renderer is the default (desktop, mobile devices, web), which defines Mobile where it is first spoken.

*Motion.* The ring steps down the rows with the voice.

*Lane.* remotion · `LectureEvidenceTable` · runner-up: manim

### B32 · 47 words · ~16 s

> In two-D, the default is different. Every renderer blends the typed numbers, and all three read point five. Turn on the project setting H D R two D, which works in light and keeps numbers past one for glow, and Forward Plus and Mobile read point six.

*Picture.* A two-row table, the default row ringed first, then the HDR 2D row.

*Motion.* The ring moves from the first row to the second.

*Lane.* remotion · `LectureEvidenceTable` · runner-up: ShaderLab with the HDR 2D project setting

## Act V: Hint Colors, Not Masks

### B33 · 45 words · ~15 s

> The fix is a hint: source color, written after a color's name. Godot's docs say where it matters. Required in Forward Plus and Mobile, and in two-D when H D R two D is on. Optional in Compatibility, and in two-D when it is off.

*Picture.* Act title 'Hint Colors, Not Masks' (serif 40) top-left. The real Godot 4.7 'Using source_color' section in a browser window; the camera pushes in on the paragraph that says where the hint is required and where it is optional, and a terracotta ring marks that paragraph.

*Motion.* The camera pushes in on the paragraph the voice is reading.

*Lane.* remotion · `BrowserCapture` · runner-up: ShaderLab: a hint line in code

### B34 · 43 words · ~15 s

> What does it do? It tells the engine the numbers are s R G B, so red, green and blue are converted to light before your math. Alpha stays a plain amount. And the Inspector shows a color picker, not four number boxes.

*Picture.* Code card at left (two vec4 uniforms with the same numbers, one with source color, one without). At right a real still of the Inspector's Shader Parameters group from a scripted editor session: Picked is a color swatch (a click on it opens the picker), Typed is four number boxes x, y, z, w (0.2, 0.4, 0.6, 1.0). A terracotta ring on the swatch, then on the four boxes.

*Motion.* The ring moves from the color swatch to the four number boxes.

*Lane.* editor · `ShaderLab` · runner-up: ShaderLab video of a Lab render with the same values

*Capture to record.* E2 (DONE by script, 2026-10-13): `_godot-shaders-series/editor-capture/png/3456x1944/textures-and-color/textures-and-color_E2_picked-swatch-and-typed-four-boxes.png` (the 1920x1080 twin is in png/1920x1080/). Crop the Inspector from the native frame: the rectangle x 1275 to 1915, y 195 to 555 in 1920x1080 coordinates, times 1.8 for the native file (1152 x 648 px, 16:9); save as editor-picker.png (a still). The ring boxes below are fractions of that crop. Real labels: group Shader Parameters; Picked is an EditorPropertyColor (swatch, `source_color` vec4); Typed is four number boxes labelled x y z w. No pointer is visible; the clip is a scripted editor session. Type-level check: evidence/planning-checks/run-4-inspector-types.log (Color against Vector4).

### B35 · 48 words · ~16 s

> Leave the hint off, and the engine takes typed numbers for light. In Forward Plus with H D R two D on, a color typed as point two, point four, point six comes out near point five, point seven, point eight. Washed out. Plain nodes need no hint.

*Picture.* Code card at left (the hinted flat-color shader; the voice says the third patch has the same line without the hint). At right three real steel-blue patches: a Color Rect, a hinted shader patch, and an unhinted shader patch that is visibly lighter. Readouts under them: 'node color', 'hinted', 'no hint', then the numbers 0.20 0.40 0.60 under the first two and about 0.48 0.66 0.80 under the third.

*Motion.* The third patch is visibly paler than the other two, and its numbers land under it.

*Lane.* capture · `ShaderLab` · runner-up: manim: three swatches

*Capture to record.* C23: custom scene (reference script evidence/planning-checks/verify-patches.gd): three 96x140 patches on the stage at 320x180 logical, scaled to 4K: a ColorRect with color (0.2, 0.4, 0.6); a ColorRect with lab-shaders/23-patch-hinted.gdshader; a ColorRect with lab-shaders/24-patch-plain.gdshader; Viewport.use_hdr_2d = true, --rendering-method forward_plus; PNG converted from linear to what the screen shows. Verified centres: node (0.1999, 0.3999, 0.5998), hinted (0.1999, 0.3999, 0.5998), plain (0.4845, 0.6651, 0.7975) (an 8-bit capture reads 0.48, 0.66, 0.80). With HDR 2D off, or in Compatibility, all three are (0.2, 0.4, 0.6).

### B36 · 36 words · ~12 s

> Setting a color from code works the same way. Pass the color exactly as you picked it, and let the hint convert it. Convert it yourself first, and it converts twice: that blue turns almost navy.

*Picture.* A two-line GDScript card at left (set the tint to the color as picked; set it to color.srgb_to_linear()). At right two real patches: steel blue for the first line, a dark navy for the second. Labels 'as picked' and 'converted first'.

*Motion.* The second patch is far darker than the first.

*Lane.* capture · `ShaderLab` · runner-up: ShaderLab stills

*Capture to record.* C24: custom scene as C23 with two patches using lab-shaders/23-patch-hinted.gdshader and HDR 2D on: the first with tint = Color(0.2, 0.4, 0.6), the second with tint = Color(0.2, 0.4, 0.6).srgb_to_linear() = (0.0331, 0.1328, 0.3184). Verified (runner_plus, HDR 2D, Forward+): (0.196, 0.396, 0.596) against (0.031, 0.129, 0.318). Also on an unshaded 3D quad in Forward+ (run-12 g): (0.200, 0.400, 0.600) against (0.031, 0.133, 0.318).

### B37 · 36 words · ~12 s

> Textures follow the rule. A color texture gets the hint. Without it, in Forward Plus, the picture comes out lighter, the same washed out look. In Compatibility it makes no difference, so the mistake can hide.

*Picture.* Code card at left (a spatial unshaded shader that shows a texture, with the hint). At right a two-by-two grid of real renders of the four-patch picture: top row Forward+ (hinted: true colors; not hinted: pale, washed out), bottom row Compatibility (both true). Labels 'hint' and 'no hint' above the columns, 'Forward+' and 'Compatibility' beside the rows.

*Motion.* Only one cell of four is pale: the Forward+ render without the hint.

*Lane.* capture · `ShaderLab` · runner-up: manim: a texture passing through two scales

*Capture to record.* C25: four Lab renders of the swatches texture (quad3d, tex = picture) joined with ffmpeg xstack as a 2x2: lab-shaders/25-swatch-hinted.gdshader and 26-swatch-plain.gdshader, each in forward_plus and in gl_compatibility; stills. Verified (rose patch): Forward+ hinted (0.902, 0.349, 0.549), plain (0.957, 0.624, 0.765); Compatibility hinted and plain (0.902, 0.349, 0.549). Mobile matches Forward+ (plain 0.957, 0.627, 0.769).

### B38 · 37 words · ~13 s

> A mask must not have the hint. Hint a mask in Forward Plus, and every number in it shifts. A threshold of one half then cuts about three quarters of the way across the ramp, not halfway.

*Picture.* Code card at left (the mask shader with the hint, cutting at 0.5). At right two real horizontal strips of the same gray ramp cut at one half: the top one without the hint switches colors at the middle, the bottom one with the hint switches about three quarters of the way across. Readouts 'no hint 0.50' and 'hint 0.74' (where each strip switches), with a terracotta ring on each switch.

*Motion.* The ring jumps from the middle of the top strip to three quarters of the way across the bottom one.

*Lane.* capture · `ShaderLab` · runner-up: manim: two number lines with a cut

*Capture to record.* C26: two Lab renders of the gray ramp (the 256-wide ramp_grey texture: value = x / 255) on a 3D unshaded quad, Forward+, vstack: top lab-shaders/27-mask-plain.gdshader, bottom lab-shaders/28-mask-hinted.gdshader (both with source-color cream and teal uniforms); stills. Verified: no hint flips cream -> teal between x = 0.50 and 0.51; hint flips between 0.73 and 0.74. In Compatibility both flip near 0.50. In HDR 2D (canvas_item) the same shift (run-6).

### B39 · 43 words · ~15 s

> So the rule is short. Hint every color you give a shader, uniform or texture. Never hint a mask. And if you ship on more than one renderer, look at each, because a number read from one may not hold in the others.

*Picture.* A four-row table, the answer column ringed row by row as each kind is named.

*Motion.* The ring steps down the four kinds.

*Lane.* remotion · `LectureEvidenceTable` · runner-up: manim

### B40 · 45 words · ~15 s

> To change a project's renderer, open Project Settings, then Rendering, Renderer. Set Rendering Method to forward plus, mobile or G L compatibility, then Save and Restart. Look at your colors in each renderer you ship on, because the same shader can show a different pixel.

*Picture.* Three real frames of the Godot editor's Project Settings dialog (a scripted editor session), joined by cross-dissolves: Rendering, Renderer open, with the Renderer entry in the left tree and then the Rendering Method row (forward_plus) ringed; the Rendering Method menu open, its three entries forward_plus, mobile, gl_compatibility ringed; then the dialog's note 'Changed settings will be applied to the editor after restarting.' with the Save & Restart button ringed.

*Motion.* The ring moves from the Renderer page to the Rendering Method row, to the three entries, to Save & Restart as the voice names each.

*Lane.* editor · `ShaderLab` · runner-up: GodotDevWorkbench (labelled reconstruction)

*Capture to record.* E3 (replaced; DONE by script, 2026-10-13, README section 11): three full frames from `_godot-shaders-series/editor-capture/png/1920x1080/renderer-path/` (native twins in png/3456x1944/renderer-path/): renderer-path_R1-C_Project-Settings_Rendering-Renderer_menu-closed, R1-D_Project-Settings_Rendering-Method_menu-open, R1-E_Project-Settings_restart-note. Cross-dissolve at 0.34 and 0.56 of the beat; ring boxes are fractions of the whole 1920x1080 frame (no crop). Real labels: dialog 'Project Settings (project.godot)'; left tree Rendering > Renderer (a second page named Rendering sits under Internationalization: not that one); rows 'Rendering Method' (forward_plus), 'Rendering Method.web', 'Rendering Method.mobile'; the dropdown lists forward_plus, mobile, gl_compatibility; after a change the note reads 'Changed settings will be applied to the editor after restarting.' with the buttons Save & Restart and X. Save & Restart was never pressed, so the film says nothing about what follows. The frames show the scratch project name, and the editor draws its own menu bar inside the window (Use Embedded Menu on): label the clip 'scripted editor session'. NOT used: the title-bar renderer name (hidden by default in 4.7.2; shown only after Editor > Editor Settings > Interface > Editor > Appearance > Show Renderer Selector, frames R3-A, R3-B and the OFF-vs-ON composite).

### B41 · 37 words · ~13 s

> Back to the burn. Its ramp is a color texture, so it carries the hint. Its noise is a mask, so it does not. Check those two lines whenever an AI hands you a shader like this.

*Picture.* The finished dissolve shader at left; the ramp_tex line highlighted with 'a color: hinted', then the noise_tex line with 'a mask: no hint'. At right the real sprite burning away again.

*Motion.* The highlight lands on the ramp line, then the noise line, while the sprite burns.

*Lane.* capture · `ShaderLab` · runner-up: LectureCodeTrace alone

*Capture to record.* C18 reused (the same capture as B23).

## Closing

### BVDT · recap · 83 words · ~28 s

> Let's recap with Claude. A texture is a table you look up by address. A color is four numbers, so you can tint it, flip it, gray it and mix it. A noise texture is a mask: compare it with a threshold, and a sprite dissolves. The number you type is not always the color you see: there are two scales. Hint every color with source color, and never hint a mask. A number read from one renderer may not hold in another.

*Picture.* The recap card: A texture is a table you look up by address. / A color is four numbers, so you can tint it, flip it, gray it and mix it. / A noise texture is a mask: compare it with a threshold, and a sprite dissolves. / The number you type is not always the color you see: there are two scales. / Hint every color with source color, and never hint a mask. / A number read from one renderer may not hold in another.

### BHTF · your turn · 87 words · ~30 s

> Your turn. Paste this into Claude: Write a Godot canvas item shader that dissolves a sprite. A noise texture decides which pixels go first, a float uniform called progress from zero to one is the dial, and a ramp texture colors the burning edge. Mark which texture needs the source color hint, and say why. Then check two things yourself. At progress zero, is the sprite untouched, and at one, is it gone? And does the ramp carry the source color hint, while the noise does not?

*Prompt shown and read in full:* Write a Godot canvas item shader that dissolves a sprite. A noise texture decides which pixels go first, a float uniform called progress from zero to one is the dial, and a ramp texture colors the burning edge. Mark which texture needs the source color hint, and say why.

*Two checks:* Check: at progress zero the sprite is untouched, and at one it is gone. · Check: the ramp has the source color hint and the noise does not.

### BOUT · outro · 7 words · ~4 s

> Textures and Color. At Nik Bear Brown.

*Picture.* The locked channel outro card: exact title, handle, one mascot. Followed by a one-second silent tail.

