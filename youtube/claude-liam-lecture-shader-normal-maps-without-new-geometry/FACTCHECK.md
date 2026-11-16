# Fact check

Source hashes, fresh windowed tests and limitations: /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_shader-review-2026-10-16/REVIEW.md

| Beat | Claim | Verdict | Source | Fix |
|---|---|---|---|---|
| B01 | A Direction In A Texture; `texture(normal_map, UV)` | Source checked; numeric tests pass for supplied rig | `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_shader-review-2026-10-16/project-snapshot/shaders/08_normal_mapped.gdshader:48` | Caveats stated in narration |
| B02 | Build The Surface Frame; `world_tangent =` | Source checked; numeric tests pass for supplied rig | `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_shader-review-2026-10-16/project-snapshot/shaders/08_normal_mapped.gdshader:39` | Caveats stated in narration |
| B03 | Combine The Components; `tn.x * world_tangent` | Source checked; numeric tests pass for supplied rig | `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_shader-review-2026-10-16/project-snapshot/shaders/08_normal_mapped.gdshader:49` | Caveats stated in narration |
| B04 | Reuse The New Normal; `vec3 r =` | Source checked; numeric tests pass for supplied rig | `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_shader-review-2026-10-16/project-snapshot/shaders/08_normal_mapped.gdshader:53` | Caveats stated in narration |
| B05 | Reveal The Domes; `vec3 tn =` | Source checked; numeric tests pass for supplied rig | `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_shader-review-2026-10-16/project-snapshot/shaders/08_normal_mapped.gdshader:48` | Caveats stated in narration |
| B06 | Green Has A Convention; `tn.y * world_binormal` | Source checked; numeric tests pass for supplied rig | `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_shader-review-2026-10-16/project-snapshot/shaders/08_normal_mapped.gdshader:49` | Caveats stated in narration |
| B07 | A Scale Limitation; `MODEL_NORMAL_MATRIX * TANGENT` | Source checked; numeric tests pass for supplied rig | `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_shader-review-2026-10-16/project-snapshot/shaders/08_normal_mapped.gdshader:39` | Caveats stated in narration |
| B08 | No Displacement; `void fragment` | Source checked; numeric tests pass for supplied rig | `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_shader-review-2026-10-16/project-snapshot/shaders/08_normal_mapped.gdshader:46` | Caveats stated in narration |
| BHTF | Your Turn: silhouette stays unchanged when swapping normal maps; green channel convention observable | PASS | `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_shader-review-2026-10-16/project-snapshot/shaders/08_normal_mapped.gdshader:49` | Both claims are observable in Godot with the supplied rig; silhouette-unchanged is a geometric fact (normal maps affect per-fragment lighting only) |

Primary API reference: https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/spatial_shader.html (checked 2026-10-16). All sample calculations follow the displayed code; measured screen values are deliberately omitted to avoid confusing renderer-specific transfer with model weights. The original Cg host behavior is not claimed as independently verified.

Status: Claude Code build-stage sign-off 2026-10-17. All body-beat claims source-verified against `08_normal_mapped.gdshader`. No OPEN rows.
