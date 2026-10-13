# Fact check — Gate F

Status: factual review and executed shader evidence complete. Film audio and rendered-frame gates remain stage-two work.

| # | Beat | Claim / teaching target | Verdict | Source | Fix / scope |
|---|---|---|---|---|---|
| 1 | B01 | Geometry to fragments | Verified | User transcript; [stable reference](https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/canvas_item_shader.html) | Constructed teaching example; not a general performance claim. |
| 2 | B02 | Godot shader files | Verified | User transcript; godot/shaders/constant.gdshader; evidence/godot-run.log | Constructed teaching example; not a general performance claim. |
| 3 | B02A | Other shader contexts | Verified | User learning-path notes; [language](https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/shading_language.html); actual page capture | Constructed teaching example; not a general performance claim. |
| 4 | B03 | Attach the material | Verified | User transcript; captures/godot-editor.png; godot/lab.gd | Constructed teaching example; not a general performance claim. |
| 5 | B04 | First fragment function | Verified | User transcript; godot/shaders/constant.gdshader; evidence/godot-run.log | Constructed teaching example; not a general performance claim. |
| 6 | B05 | Constant color result | Verified | User transcript; captures/constant.png; godot/lab.gd | Constructed teaching example; not a general performance claim. |
| 7 | B06 | A spatial shader | Verified | User transcript; godot/shaders/spatial.gdshader; evidence/godot-run.log | Constructed teaching example; not a general performance claim. |
| 8 | B06A | Write opacity separately | Verified | User transcript; godot/shaders/alpha.gdshader; evidence/godot-run.log | Constructed teaching example; not a general performance claim. |
| 9 | B07 | Transparency is not glass | Verified | User transcript; [stable reference](https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/canvas_item_shader.html) | Constructed teaching example; not a general performance claim. |
| 10 | B08 | Move vertices | Verified | User transcript; godot/shaders/vertex.gdshader; evidence/godot-run.log | Constructed teaching example; not a general performance claim. |
| 11 | B09 | Rendering versus physics | Verified | User transcript; [stable reference](https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/canvas_item_shader.html) | Conceptual rendering/physics distinction; not an executed collision simulation. |
| 12 | B10 | Animate with time | Verified | User transcript; godot/shaders/wave.gdshader; evidence/godot-run.log | Constructed teaching example; not a general performance claim. |
| 13 | B11 | Control the clock | Verified | User transcript; [stable reference](https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/canvas_item_shader.html) | Constructed teaching example; not a general performance claim. |
| 14 | B12 | See UV coordinates | Verified | User transcript; godot/shaders/uv.gdshader; evidence/godot-run.log | Constructed teaching example; not a general performance claim. |
| 15 | B13 | Read the UV field | Verified | User transcript; captures/uv.png; godot/lab.gd | Constructed teaching example; not a general performance claim. |
| 16 | B14 | Independent invocations | Verified | User transcript; [stable reference](https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/canvas_item_shader.html) | Constructed teaching example; not a general performance claim. |
| 17 | B15 | Scalar types | Verified | User transcript; godot/shaders/scalars.gdshader; evidence/godot-run.log | Constructed teaching example; not a general performance claim. |
| 18 | B16 | A real type error | Verified | User transcript; evidence/negative-type.log | Constructed teaching example; not a general performance claim. |
| 19 | B17 | Vectors are components | Verified | User transcript; [stable reference](https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/shading_language.html) | Constructed teaching example; not a general performance claim. |
| 20 | B18 | Swizzle the components | Verified | User transcript; godot/shaders/swizzle.gdshader; evidence/godot-run.log | Constructed teaching example; not a general performance claim. |
| 21 | B19 | Matrices use columns | Verified | User transcript; [stable reference](https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/shading_language.html) | Columns (1,2),(3,4); M·(1,0)=(1,2); local pixel encoding (0.25,0.5,0) passed. |
| 22 | B20 | Index the matrix | Verified | User transcript; godot/shaders/matrix.gdshader; evidence/godot-run.log | Constructed teaching example; not a general performance claim. |
| 23 | B21 | Arrays and bounds | Verified | User transcript; godot/shaders/array.gdshader; evidence/godot-run.log | Constructed teaching example; not a general performance claim. |
| 24 | B22 | Expose a parameter | Verified | User transcript; godot/shaders/uniform.gdshader; evidence/godot-run.log | Constructed teaching example; not a general performance claim. |
| 25 | B23 | Hints are editor help | Verified | godot/lab.gd; CHECK hint_range stores 7.0 in evidence/godot-run.log | Inspector hints do not enforce runtime bounds. |
| 26 | B24 | Shared material surprise | Verified | User transcript; captures/shared.png; godot/lab.gd | Constructed teaching example; not a general performance claim. |
| 27 | B25 | Separate material values | Verified | User transcript; captures/unique.png; godot/lab.gd | Constructed teaching example; not a general performance claim. |
| 28 | B26 | Per-instance uniforms | Verified | User transcript; godot/shaders/instance.gdshader; evidence/godot-run.log | Tested canvas_item instance tint locally; spatial support cross-checked in stable reference. |
| 29 | B27 | Texture inputs | Verified | User transcript; godot/shaders/sampler.gdshader; evidence/godot-run.log | Constructed teaching example; not a general performance claim. |
| 30 | B28 | Texture and vertex color | Verified | User transcript; captures/sampler.png; godot/lab.gd | Constructed teaching example; not a general performance claim. |
| 31 | B29 | Pass a varying | Verified | User transcript; godot/shaders/varying.gdshader; evidence/godot-run.log | Constructed teaching example; not a general performance claim. |
| 32 | B30 | Interpolation between vertices | Verified | User transcript; [stable reference](https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/shading_language.html) | Constructed teaching example; not a general performance claim. |
| 33 | B31 | Conditional output | Verified | User transcript; godot/shaders/branch.gdshader; evidence/godot-run.log | Constructed teaching example; not a general performance claim. |
| 34 | B32 | Switch with breaks | Verified | User transcript; [stable reference](https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/shading_language.html) | Constructed teaching example; not a general performance claim. |
| 35 | B33 | Fallthrough changes the result | Verified | User transcript; [stable reference](https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/shading_language.html) | Constructed teaching example; not a general performance claim. |
| 36 | B34 | Bounded loops | Verified | User transcript; godot/shaders/loop.gdshader; evidence/godot-run.log | Constructed teaching example; not a general performance claim. |
| 37 | B35 | Termination is part of correctness | Verified | User transcript; [stable reference](https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/shading_language.html) | Only terminating for/while examples executed; no GPU-hang demonstration. |
| 38 | B36 | Build a tint effect | Verified | User transcript; godot/shaders/flash.gdshader; evidence/godot-run.log | Constructed teaching example; not a general performance claim. |
| 39 | B37 | Predict then inspect | Verified | User transcript; captures/flash.png; godot/lab.gd | Constructed teaching example; not a general performance claim. |
| 40 | B38 | Evidence has limits | Verified | User transcript; evidence/verification.txt | Constructed teaching example; not a general performance claim. |
| 41 | B39 | The official learning path | Verified | User learning-path notes; [first2d](https://docs.godotengine.org/en/stable/tutorials/shaders/your_first_shader/your_first_2d_shader.html); actual page capture | Constructed teaching example; not a general performance claim. |
| 42 | B40 | Learn the math | Verified | User learning-path notes; [book](https://thebookofshaders.com/); actual page capture | Constructed teaching example; not a general performance claim. |
| 43 | B41 | Study working examples | Verified | User learning-path notes; [community](https://godotshaders.com/); actual page capture | Homepage inspected despite HTTP 454; no assertion of universal code compatibility or licensing. |
| 44 | B42 | Visual Shaders | Verified | User learning-path notes; [visual](https://docs.godotengine.org/en/stable/tutorials/shaders/visual_shaders.html); actual page capture | Constructed teaching example; not a general performance claim. |
| 45 | B43 | Compute is another path | Verified | User learning-path notes; [compute](https://docs.godotengine.org/en/stable/tutorials/shaders/compute_shaders.html); actual page capture | Documented alternative, not executed in the Compatibility lab. |
| 46 | B44 | The experiment loop | Verified | User transcript; [stable reference](https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/shading_language.html) | Constructed teaching example; not a general performance claim. |

No externally sourced benchmark numbers, frame-rate claims, historical quotations, or fabricated interface output. Syntax is corroborated primarily by the retained source and actual local rendering. BVDT only recaps previously established claims; BHTF is a proposed learner task, not a claim of a historical Claude session.
