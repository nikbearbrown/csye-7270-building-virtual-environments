# Fact check

Source hashes, fresh windowed tests and limitations: /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_shader-review-2026-10-16/REVIEW.md

| Beat | Claim | Verdict | Source | Fix |
|---|---|---|---|---|
| B01 | Start With The Normal; `flip_green ?` | Source checked; numeric tests pass for supplied rig | `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_shader-review-2026-10-16/project-snapshot/shaders/15_uber.gdshader:59` | Caveats stated in narration |
| B02 | Recheck Packed Channels; `specular_map.r` | Source checked; numeric tests pass for supplied rig | `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_shader-review-2026-10-16/project-snapshot/shaders/15_uber.gdshader:74` | Caveats stated in narration |
| B03 | Ambient By Orientation; `vec3 ambient =` | Source checked; numeric tests pass for supplied rig | `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_shader-review-2026-10-16/project-snapshot/shaders/15_uber.gdshader:70` | Caveats stated in narration |
| B04 | Broaden The Light; `vec3 lambert =` | Source checked; numeric tests pass for supplied rig | `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_shader-review-2026-10-16/project-snapshot/shaders/15_uber.gdshader:72` | Caveats stated in narration |
| B05 | Watch The Terminator; `subsurface_spread` | Source checked; numeric tests pass for supplied rig | `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_shader-review-2026-10-16/project-snapshot/shaders/15_uber.gdshader:34` | Caveats stated in narration |
| B06 | Keep Reflections Separate; `reflection_intensity * specular_map.b` | Source checked; numeric tests pass for supplied rig | `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_shader-review-2026-10-16/project-snapshot/shaders/15_uber.gdshader:78` | Caveats stated in narration |
| B07 | Read Every Addition; `vec3 total_spec` | Source checked; numeric tests pass for supplied rig | `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_shader-review-2026-10-16/project-snapshot/shaders/15_uber.gdshader:78` | Caveats stated in narration |
| B08 | A Combined Model Has Limits; `ALBEDO =` | Source checked; numeric tests pass for supplied rig | `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_shader-review-2026-10-16/project-snapshot/shaders/15_uber.gdshader:80` | Caveats stated in narration |

Primary API reference: https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/spatial_shader.html (checked 2026-10-16). All sample calculations follow the displayed code; measured screen values are deliberately omitted to avoid confusing renderer-specific transfer with model weights. The original Cg host behavior is not claimed as independently verified.
