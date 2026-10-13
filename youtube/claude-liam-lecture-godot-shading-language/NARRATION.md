# Godot Shading Language

## BOPEN · Opening

CSYE seventy-two seventy, Building Virtual Environments. Godot Shading Language. Learn to turn coordinates and material inputs into effects you can predict and test.

## BIDEA · Opening

Hallo. This is Liam, in for Bear, for CSYE seventy-two seventy, Building Virtual Environments. Shaders compute from their inputs. Once you can predict those inputs, the language starts to make sense.

## BDEFS · Opening

Five terms. G P U: the processor doing parallel graphics work. A vertex is a geometry point. A fragment is a candidate contribution to a pixel. A material describes a surface. U V coordinates address a texture.

## BACT1 · A Program for the Surface

A Program for the Surface.

## B01 · A Program for the Surface

Start with the rendering pipeline. The vertex function works on geometry. Rasterization turns triangles into covered fragments. The fragment function computes surface values. That is our map: inputs, a calculation, then a visible result.

## B02 · A Program for the Surface

Godot uses its own shading language, closely related to G L S L. Save it as dot G D shader. Shader type selects the context. Canvas item serves two D; spatial serves three D.

## B02A · A Program for the Surface

Other shader contexts include particles, sky, and fog. Not every context exposes the same processor functions or built-ins. Older Godot three tutorials use dot shader files. In Godot, vertex and fragment replace the usual G L S L main entry point.

## B03 · A Program for the Surface

Select a drawable node, open Material, and assign a ShaderMaterial. That material holds a Shader resource. Here the real editor shows our ColorRect with the material attached. Open its shader to edit the program.

## B04 · A Program for the Surface

This is a complete first shader. Void means the function returns no ordinary value. Instead, it writes COLOR. Four components specify red, green, blue, and opacity. One in the last component means fully opaque.

## B05 · A Program for the Surface

Every covered fragment receives the same four numbers, so the whole rectangle becomes pink. This output came from Godot. No texture coordinates appear in the calculation, so there is no reason for one part to differ.

## B06 · A Program for the Surface

For a three D material, write ALBEDO for the base color. The lighting system uses it along with properties such as roughness and the surface normal. ALBEDO is a three-component vector; opacity has its own output.

## B06A · A Program for the Surface

In a spatial shader, ALPHA controls opacity. This small example writes zero point three. Defining light lets you customize lighting where that processor is supported; you do not need an empty light function in every shader.

## B07 · A Program for the Surface

Here is the rendered cube. Writing ALPHA as zero point three makes a transparent surface. That alone does not create physically convincing glass. Refraction, lighting, and transparency sorting are separate questions.

## BACT2 · Coordinates, Not Memory

Coordinates, Not Memory.

## B08 · Coordinates, Not Memory

Now coordinates. In a two D vertex function, VERTEX gives a local position. Add twenty to its horizontal component and the drawn geometry shifts right. Use twenty point zero because that component is a float.

## B09 · Coordinates, Not Memory

Before it moves, predict what happens to the collider. The drawn square shifts; the collision outline stays put. A shader changes rendering. It does not move the node or rewrite your physics shape.

## B10 · Coordinates, Not Memory

TIME is an engine clock. Feeding it into sine makes the offset oscillate. Each frame recomputes the offset from the supplied time. We are not accumulating the previous frame’s vertex position.

## B11 · Coordinates, Not Memory

A clock value of zero, then a quarter turn, then a half turn produces zero offset, maximum offset, then zero again. For an event like damage, drive your own uniform from game state instead of treating TIME as an event timer.

## B12 · Coordinates, Not Memory

UV gives texture coordinates for the current point. This example places U into red and V into green. Blue stays zero. We are turning an invisible coordinate field into something we can inspect.

## B13 · Coordinates, Not Memory

On this rectangle, the upper left is dark. Move right and red increases. Move down and green increases. The lower right combines both. The gradient is many invocations applying one rule to different inputs.

## B14 · Coordinates, Not Memory

Do not picture a paintbrush remembering the last pixel. Each fragment has local inputs and local work. Other pixels can be read through appropriate textures, but you cannot rely on the neighboring invocation having already finished.

## BACT3 · Types You Can See

Types You Can See.

## B15 · Types You Can See

Types make the calculation explicit. Bool holds true or false. Int holds an integer. Float holds a real-valued approximation. Statements end in semicolons. Convert an integer deliberately when a calculation needs a float.

## B16 · Types You Can See

Here is a deliberate failure: assigning the integer literal five directly to a float. Godot reports a type error. Five point zero or an explicit float conversion fixes it. Read the shader diagnostics, not just the process exit status.

## B17 · Types You Can See

A vector groups components. These four numbers can be addressed as X, Y, Z, W, or as red, green, blue, alpha. The names change with your interpretation; the underlying four values do not.

## B18 · Types You Can See

Swizzling selects and reorders components. B G R reverses the three color channels. X X copies the first component into a two-component vector. Match the result’s size, and never mix naming families inside one swizzle.

## B19 · Types You Can See

A matrix constructor takes columns. Put one and two in the first column, three and four in the second. Multiplying by the first basis vector selects that first column: one, two. It does not select the first row.

## B20 · Types You Can See

Here is that calculation in shader code. Matrix indexing also starts with the column. The result is divided by four only to fit this color demonstration. The colored output is a diagnostic encoding, not a new matrix rule.

## B21 · Types You Can See

An array stores several values of the same type. Its first index is zero. These three weights live at indices zero, one, and two. Index one selects zero point three. Keep every access inside the array’s bounds.

## BACT4 · Who Owns the Value?

Who Owns the Value?.

## B22 · Who Owns the Value?

Now make the material adjustable. A uniform supplies a value shared by the invocations using that material. Source color gives a color control; hint range gives a numeric control. The shader reads those values while it runs.

## B23 · Who Owns the Value?

An enum hint names integer choices. A range hint guides the Inspector, but it does not enforce a runtime bound. Our local test stored seven in a parameter whose suggested range was zero to one. Clamp when the effect requires it.

## B24 · Who Owns the Value?

Predict what happens when two nodes share this ShaderMaterial and we change its tint. Both become orange. The value belongs to the shared material resource, so duplicating a node does not automatically give it independent parameters.

## B25 · Who Owns the Value?

One fix is a separate material resource. The two materials can still share the same shader program. Here only one tint changes. You need different parameter storage, not another copy of the shader’s source code.

## B26 · Who Owns the Value?

Another option is an instance uniform, supported for canvas item and spatial shaders in the stable reference checked here. Set it on each drawable node. The material stays shared while the tint varies. Check support in your project’s version.

## B27 · Who Owns the Value?

A sampler binds a texture. Texture reads sample that image at supplied coordinates. Here image tex is the input and UV is the address. Use source color for color textures; a data map has a different role.

## B28 · Who Owns the Value?

This checkerboard is a real texture sample. On a Sprite, sampling TEXTURE directly reads the texture alone. Incoming COLOR already includes the normal texture and vertex-color contribution. Choose deliberately, or your effect can discard tint and modulation.

## BACT5 · Passing Values, Choosing Paths

Passing Values, Choosing Paths.

## B29 · Passing Values, Choosing Paths

A varying carries data between stages. Here the vertex function writes horizontal from U. The fragment function reads it. This is stage-to-stage transport, not a variable storing yesterday’s frame or a neighbor’s output.

## B30 · Passing Values, Choosing Paths

The endpoints carry zero and one. Between them, rasterization interpolates the value. Halfway across this flat rectangle, the value is about one half. That is why a few vertex values can create a smooth fragment gradient.

## B31 · Passing Values, Choosing Paths

Ordinary conditionals work inside the shader. This example chooses dark on the left and light on the right by comparing U with one half. The decision is local to each invocation, so different fragments take different branches.

## B32 · Passing Values, Choosing Paths

A switch selects an integer case. Here mode one produces one quarter. Break stops execution from continuing into later cases. Include explicit breaks in the demonstrated version, including the default branch.

## B33 · Passing Values, Choosing Paths

Remove the first two breaks and mode one keeps going: one quarter, then three quarters, then one tenth. The captured outputs differ. The language accepted the program; the control flow still changed the meaning.

## B34 · Passing Values, Choosing Paths

A loop needs a clear stopping condition and progress toward it. This one visits three weights, advances its index, and adds them to one. Keeping the bound small also keeps the work per fragment understandable.

## B35 · Passing Values, Choosing Paths

Watch the index: zero, one, two, then stop at three. A while loop also needs progress. A missing increment can hang rendering. We inspect that failure in a trace; we do not freeze the editor to prove it.

## BACT6 · Build, Verify, Keep Learning

Build, Verify, Keep Learning.

## B36 · Build, Verify, Keep Learning

Put the pieces together. Preserve incoming COLOR, blend its RGB toward a tint, and keep its alpha. Clamp the amount between zero and one. That makes the input contract explicit even when game code sends an unexpected value.

## B37 · Build, Verify, Keep Learning

Before looking, predict three settings. Zero should preserve the base. One should reach the tint. One half should lie between them. These are the actual rendered samples. Transparent artwork needs a separate alpha check too.

## B38 · Build, Verify, Keep Learning

A parser check is useful, but a rendered image answers a different question. Our test inspects shader errors and selected pixels. It does not prove performance on every device or whether this color communicates danger well in your game.

## B39 · Build, Verify, Keep Learning

Use the stable documentation for first two D and first three D shaders. Then keep the language reference nearby. If you know G L S L, use the migration guide. Match documentation to your installed release.

## B40 · Build, Verify, Keep Learning

The Book of Shaders teaches the mathematical habits: coordinate fields, shaping functions, patterns, and noise. Its examples use plain G L S L. Translate the entry points and inputs into Godot rather than pasting every example unchanged.

## B41 · Build, Verify, Keep Learning

Godot Shaders is a community library. Choose a small effect, check its Godot version and license, and change one parameter at a time. Predict the visible difference before running it. Reading a shader is active experimentation.

## B42 · Build, Verify, Keep Learning

Visual Shaders offer a graph editor for building these programs. Nodes change the authoring interface; they do not remove the need to understand coordinates, types, and data flow. Use the form that helps you inspect the calculation.

## B43 · Build, Verify, Keep Learning

Compute shaders use raw G L S L through RenderingDevice. They are a separate low-level path for general GPU work. The official tutorial requires a RenderingDevice renderer, such as Forward Plus or Mobile, rather than Compatibility.

## B44 · Build, Verify, Keep Learning

Keep one loop: predict a visible change, alter one input, run the engine, and compare the result. If the result surprises you, inspect the type, coordinates, and ownership of that input before adding more code.

## BVDT · Closing

Let's recap with Claude. For CSYE seventy-two seventy, Building Virtual Environments. Choose the shader type and the output for its stage. Compute from coordinates and inputs, not the previous pixel. Match scalar types, vector sizes, and matrix columns. Know whether a value belongs to a material or an instance. Pass varyings deliberately and keep control flow bounded. Predict, render, compare, then judge the effect in context.

## BHTF · Closing

Help me build a Godot canvas item tint shader. Preserve incoming alpha and expose a color plus an amount from zero to one. Predict the output at zero, one half, and one. Explain how two objects can have independent amounts. Give me the shader, a minimal test scene, and checks that distinguish parsing from rendered appearance.

## BOUT · Closing

Godot Shading Language. At Nik Bear Brown.
