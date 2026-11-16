# Fact check

Source hashes, fresh windowed tests and limitations: /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_shader-review-2026-10-16/REVIEW.md

| Beat | Claim | Verdict | Source | Fix |
|---|---|---|---|---|
| B01 | Move Before Projection; `VERTEX = VERTEX` | Source checked; numeric tests pass for supplied rig | `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_shader-review-2026-10-16/project-snapshot/shaders/10_vertex_anim.gdshader:40` | Caveats stated in narration |
| B02 | Build A Phase; `sin(TIME * animation_speed` | Source checked; numeric tests pass for supplied rig | `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_shader-review-2026-10-16/project-snapshot/shaders/10_vertex_anim.gdshader:40` | Caveats stated in narration |
| B03 | Choose Amplitude; `uniform vec3 vert_offset` | Source checked; numeric tests pass for supplied rig | `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_shader-review-2026-10-16/project-snapshot/shaders/10_vertex_anim.gdshader:27` | Caveats stated in narration |
| B04 | The Zero Case; `vec3 vert_offset =` | Source checked; numeric tests pass for supplied rig | `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_shader-review-2026-10-16/project-snapshot/shaders/10_vertex_anim.gdshader:27` | Caveats stated in narration |
| B05 | Grow The Motion; `VERTEX = VERTEX` | Source checked; numeric tests pass for supplied rig | `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_shader-review-2026-10-16/project-snapshot/shaders/10_vertex_anim.gdshader:40` | Caveats stated in narration |
| B06 | Check Operation Order; `vec3 world_pos =` | Source checked; numeric tests pass for supplied rig | `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_shader-review-2026-10-16/project-snapshot/shaders/10_vertex_anim.gdshader:36` | Caveats stated in narration |
| B07 | The Stale Normal; `world_normal =` | Source checked; numeric tests pass for supplied rig | `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_shader-review-2026-10-16/project-snapshot/shaders/10_vertex_anim.gdshader:35` | Caveats stated in narration |
| B08 | Make The Model Honest; `ALBEDO =` | Source checked; numeric tests pass for supplied rig | `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_shader-review-2026-10-16/project-snapshot/shaders/10_vertex_anim.gdshader:54` | Caveats stated in narration |

Primary API reference: https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/spatial_shader.html (checked 2026-10-16). All sample calculations follow the displayed code; measured screen values are deliberately omitted to avoid confusing renderer-specific transfer with model weights. The original Cg host behavior is not claimed as independently verified.
