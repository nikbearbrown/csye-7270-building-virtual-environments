# Fact check

Source hashes, fresh windowed tests and limitations: /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_shader-review-2026-10-16/REVIEW.md

| Beat | Claim | Verdict | Source | Fix |
|---|---|---|---|---|
| B01 | Two Jobs; `shader_type` | Source checked; numeric tests pass for supplied rig | `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_shader-review-2026-10-16/project-snapshot/shaders/00_super_simple.gdshader:18` | Caveats stated in narration |
| B02 | Place The Mesh; `POSITION =` | Source checked; numeric tests pass for supplied rig | `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_shader-review-2026-10-16/project-snapshot/shaders/00_super_simple.gdshader:24` | Caveats stated in narration |
| B03 | Homogeneous Position; `vec4(VERTEX` | Source checked; numeric tests pass for supplied rig | `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_shader-review-2026-10-16/project-snapshot/shaders/00_super_simple.gdshader:24` | Caveats stated in narration |
| B04 | Choose A Color; `ALBEDO =` | Source checked; numeric tests pass for supplied rig | `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_shader-review-2026-10-16/project-snapshot/shaders/00_super_simple.gdshader:28` | Caveats stated in narration |
| B05 | Change One Input; `uniform vec3 shader_color` | Source checked; numeric tests pass for supplied rig | `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_shader-review-2026-10-16/project-snapshot/shaders/00_super_simple.gdshader:21` | Caveats stated in narration |
| B06 | No Hidden Lamp; `render_mode unshaded` | Source checked; numeric tests pass for supplied rig | `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_shader-review-2026-10-16/project-snapshot/shaders/00_super_simple.gdshader:19` | Caveats stated in narration |
| B07 | The Color Contract; `source_color` | Source checked; numeric tests pass for supplied rig | `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_shader-review-2026-10-16/project-snapshot/shaders/00_super_simple.gdshader:21` | Caveats stated in narration |
| B08 | A Useful Baseline; `void vertex` | Source checked; numeric tests pass for supplied rig | `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_shader-review-2026-10-16/project-snapshot/shaders/00_super_simple.gdshader:23` | Caveats stated in narration |

Primary API reference: https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/spatial_shader.html (checked 2026-10-16). All sample calculations follow the displayed code; measured screen values are deliberately omitted to avoid confusing renderer-specific transfer with model weights. The original Cg host behavior is not claimed as independently verified.

Status: 8 claims checked against actual shader source (`00_super_simple.gdshader`) and 268 passing numerical tests in the review evidence record (`_shader-review-2026-10-16/`); signed by the build agent 2026-10-16 (no human sign-off yet). All PASS rows trace to a named source line.
