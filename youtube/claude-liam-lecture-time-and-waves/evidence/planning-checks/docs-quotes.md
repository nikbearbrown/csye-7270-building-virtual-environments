# Godot 4.7 documentation: the passages this film relies on

**What this is.** The exact words of the Godot 4.7 documentation (docs.godotengine.org/en/stable) that `FACTCHECK.md` cites, copied from the live pages on 2026-10-13 (page text saved and searched; nothing paraphrased inside the quotation marks).
**Why.** The brief asks for the docs pages to be fetched and quoted, so a reviewer can check each docs row without opening twelve pages.
**Found.** Every docs claim in the film is backed by one of these passages. Two pieces of the film are NOT in the docs and rest on runs instead: that `TIME` and `Time.get_ticks_msec()` have different zeros (both pages say "since the engine started"), and what the roll-over does to a pulse (the setting's page says only that animations "may appear to restart"). Both were measured (`gd/logs/`).

Page addresses are under `https://docs.godotengine.org/en/stable/`.

## TIME, PI, TAU (`tutorials/shaders/shader_reference/canvas_item_shader.html`, section "Global built-ins")

> "Global built-ins are available everywhere, including custom functions."

> `in float TIME` · "Global time since the engine has started, in seconds. It repeats after every 3,600 seconds (which can be changed with the rollover setting). It's affected by time_scale but not by pausing. If you need a TIME variable that is not affected by time scale, add your own global shader uniform and update it each frame."

> `in float PI` · "A PI constant (3.141592). The ratio of a circle's circumference to its diameter and the number of radians in a half turn."

> `in float TAU` · "A TAU constant (6.283185). Equivalent to PI * 2 and the number of radians in a full turn."

> (Built-ins) "Values marked as in are read-only."

> (Opening paragraph) "CanvasItem shaders contain fewer built-in variables and functionality than Spatial shaders, but they maintain the same basic structure with vertex, fragment, and light processor functions."

> (Vertex built-ins) `inout vec2 UV` · "Normalized texture coordinates. Range from 0.0 to 1.0."

## Why a shader needs a clock (`tutorials/shaders/introduction_to_shaders.html`)

> "Shaders are a special kind of program that runs on Graphics Processing Units (GPUs)."

> "Because of their parallel nature, though, shaders don't process information the way a typical program does. Shader code runs on each vertex or pixel in isolation. You cannot store data between frames either."

> "The fragment() function runs for every pixel covered by the mesh."

## Built-in functions (`tutorials/shaders/shader_reference/shader_functions.html`)

> `sin(angle)` · "Returns the trigonometric sine of angle." / angle: "The quantity, in radians, of which to return the sine."

> `fract(x)` · "Returns the fractional part of x. This is calculated as x - floor(x)."

> `abs(x)` · "Returns the absolute value of x. Returns x if x is positive, otherwise returns -1 * x."

> `mix(a, b, c)` · "Performs a linear interpolation between a and b using c to weight between them. Computed as a * (1 - c) + b * c."

> `step(a, b)` · "Generates a step function by comparing b to a. Equivalent to if (b < a) { return 0.0; } else { return 1.0; }."

> `distance(a, b)` · "Returns the distance between the two points a and b. i.e., length(b - a);"

> `texture(s, p)` · "Retrieves texels from a texture. Samples texels from the texture bound to s at texture coordinate p."

## Uniforms (`tutorials/shaders/shader_reference/shading_language.html`)

> "Passing values to shaders is possible with uniforms, which are defined in the global scope of the shader, outside of functions. When a shader is later assigned to a material, the uniforms will appear as editable parameters in the material's inspector. Uniforms can't be written from within the shader."

> (Hint table) `hint_range(min, max[, step])` · "Restricted to values in a range (with min/max/step)." · sampler2D `repeat[_enable, _disable]` · "Enabled texture repeating."

> (Per-instance uniforms) "Per-instance uniforms are available in both canvas_item (2D) and spatial (3D) shaders." · "Sometimes, you want to modify a parameter on each node using the material." · "There is a practical maximum limit of 16 instance uniforms per shader."

> (Setting uniforms from code) "The first argument to set_shader_parameter() is the name of the uniform in the shader. It must match exactly to the name of the uniform in the shader or else it will not be recognized."

## ShaderMaterial and CanvasItem (`classes/class_shadermaterial.html`, `classes/class_canvasitem.html`)

> ShaderMaterial `set_shader_parameter(param, value)` · "Changes the value set for this material of a uniform in the shader." · "Note: param is case-sensitive and must match the name of the uniform in the code exactly (not the capitalized name in the inspector)." · "Note: Changes to the shader uniform will be effective on all instances using this ShaderMaterial. To prevent this, use per-instance uniforms with CanvasItem.set_instance_shader_parameter(), GeometryInstance3D.set_instance_shader_parameter() or duplicate the ShaderMaterial resource using Resource.duplicate(). Per-instance uniforms allow for better shader reuse and are therefore faster, so they should be preferred over duplicating the ShaderMaterial when possible."

> CanvasItem `set_instance_shader_parameter(name, value)` · "Set the value of a shader uniform for this instance only (per-instance uniform). See also ShaderMaterial.set_shader_parameter() to assign a uniform on all instances using the same ShaderMaterial." · "Note: For a shader uniform to be assignable on a per-instance basis, it must be defined with instance uniform ... rather than uniform ... in the shader code."

## Curves (`classes/class_curvetexture.html`, `classes/class_curve.html`)

> CurveTexture · "A 1D texture where pixel brightness corresponds to points on a unit Curve resource, either in grayscale or in red." · "This visual representation simplifies the task of saving curves as image files." · property `curve`: "The Curve that is rendered onto the texture. Should be a unit Curve." · property `width` (default 256): "The width of the texture (in pixels). Higher values make it possible to represent high-frequency data better (such as sudden direction changes), at the cost of increased generation time and memory usage." · `TEXTURE_MODE_RGB` "Store the curve equally across the red, green and blue channels." · `TEXTURE_MODE_RED` "Store the curve only in the red channel."

> Curve · "This resource describes a mathematical curve by defining a set of points and tangents at each point. By default, it ranges between 0 and 1 on the X and Y axes, but these ranges can be changed." · "Please note that many resources and nodes assume they are given unit curves. A unit curve is a curve whose domain (the X axis) is between 0 and 1."

## Time, pausing, delta, tweens (`classes/class_engine.html`, `class_time.html`, `class_scenetree.html`, `class_node.html`, `class_tween.html`)

> Engine `time_scale` (default 1.0) · "The speed multiplier at which the in-game clock updates, compared to real time. For example, if set to 2.0 the game runs twice as fast, and if set to 0.5 the game runs half as fast." · "This value affects Timer, SceneTreeTimer, and all other simulations that make use of delta time (such as Node._process() and Node._physics_process())."

> Time `get_ticks_msec()` · "Returns the amount of time passed in milliseconds since the engine started."

> SceneTree `paused` · "If true, the scene tree is considered paused. This causes the following behavior: 2D and 3D physics will be stopped, as well as collision detection and related signals. Depending on each node's Node.process_mode, their Node._process(), Node._physics_process() and Node._input() callback methods may not called anymore."

> Node `_process(delta)` · "Called on each idle frame, prior to rendering, and after physics ticks have been processed. delta is the time between frames in seconds." · "Note: When --fixed-fps is enabled or the engine is running in Movie Maker mode (see MovieWriter), process delta will always be the same for every frame, regardless of how much time the frame took to render."

> Tween · "Tweens are mostly useful for animations requiring a numerical property to be interpolated over a range of values."

## The roll-over setting (`classes/class_projectsettings.html`)

> `rendering/limits/time/time_rollover_secs` = 3600 · "Maximum time (in seconds) before the TIME shader built-in variable rolls over. The TIME variable increments by delta each frame, and when it exceeds this value, it rolls over to 0.0. Since large floating-point values are less precise than small floating-point values, this should be set as low as possible to maximize the precision of the TIME built-in variable in shaders. This is especially important on mobile platforms where precision in shaders is significantly reduced. However, if this is set too low, shader animations may appear to restart from the beginning while the project is running. On desktop platforms, values below 4096 are recommended, ideally below 2048. On mobile platforms, values below 64 are recommended, ideally below 32."
