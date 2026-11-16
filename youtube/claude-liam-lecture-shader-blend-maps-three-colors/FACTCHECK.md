# Fact check

Source hashes, fresh windowed tests and limitations: /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_shader-review-2026-10-16/REVIEW.md

| Beat | Claim | Verdict | Source | Fix |
|---|---|---|---|---|
| B01 | Read Weights; `texture(blend_map, UV)` | Source checked; numeric tests pass for supplied rig | `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_shader-review-2026-10-16/project-snapshot/shaders/13_blended.gdshader:44` | Caveats stated in narration |
| B02 | Map Channels Explicitly; `vec3 final_color` | Source checked; numeric tests pass for supplied rig | `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_shader-review-2026-10-16/project-snapshot/shaders/13_blended.gdshader:45` | Caveats stated in narration |
| B03 | Use Pure Regions; `shader_color * blend.r` | Source checked; numeric tests pass for supplied rig | `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_shader-review-2026-10-16/project-snapshot/shaders/13_blended.gdshader:45` | Caveats stated in narration |
| B04 | Mix The Boundaries; `vec3 final_color` | Source checked; numeric tests pass for supplied rig | `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_shader-review-2026-10-16/project-snapshot/shaders/13_blended.gdshader:45` | Caveats stated in narration |
| B05 | Change One Paint; `uniform vec3 shader_color` | Source checked; numeric tests pass for supplied rig | `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_shader-review-2026-10-16/project-snapshot/shaders/13_blended.gdshader:18` | Caveats stated in narration |
| B06 | Light After Mixing; `ALBEDO =` | Source checked; numeric tests pass for supplied rig | `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_shader-review-2026-10-16/project-snapshot/shaders/13_blended.gdshader:52` | Caveats stated in narration |
| B07 | Avoid Color Conversion; `uniform sampler2D blend_map` | Source checked; numeric tests pass for supplied rig | `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_shader-review-2026-10-16/project-snapshot/shaders/13_blended.gdshader:26` | Caveats stated in narration |
| B08 | Check The Contract; `vec3 final_color` | Source checked; numeric tests pass for supplied rig | `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_shader-review-2026-10-16/project-snapshot/shaders/13_blended.gdshader:45` | Caveats stated in narration |

Primary API reference: https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/spatial_shader.html (checked 2026-10-16). All sample calculations follow the displayed code; measured screen values are deliberately omitted to avoid confusing renderer-specific transfer with model weights. The original Cg host behavior is not claimed as independently verified.
