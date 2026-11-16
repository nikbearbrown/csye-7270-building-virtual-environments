# Fact check

Source hashes, fresh windowed tests and limitations: /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_shader-review-2026-10-16/REVIEW.md

| Beat | Claim | Verdict | Source | Fix |
|---|---|---|---|---|
| B01 | A View-Dependent Spot; `normalize(eye_vector)` | Source checked; numeric tests pass for supplied rig | `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_shader-review-2026-10-16/project-snapshot/shaders/05_phong.gdshader:39` | Caveats stated in narration |
| B02 | Mirror The Direction; `-reflect(e, n)` | Source checked; numeric tests pass for supplied rig | `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_shader-review-2026-10-16/project-snapshot/shaders/05_phong.gdshader:40` | Caveats stated in narration |
| B03 | Compare With Light; `dot(r, l)` | Source checked; numeric tests pass for supplied rig | `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_shader-review-2026-10-16/project-snapshot/shaders/05_phong.gdshader:42` | Caveats stated in narration |
| B04 | Control The Width; `specular_power` | Source checked; numeric tests pass for supplied rig | `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_shader-review-2026-10-16/project-snapshot/shaders/05_phong.gdshader:23` | Caveats stated in narration |
| B05 | Color The Highlight; `specular_color` | Source checked; numeric tests pass for supplied rig | `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_shader-review-2026-10-16/project-snapshot/shaders/05_phong.gdshader:24` | Caveats stated in narration |
| B06 | Keep Terms Separate; `ALBEDO =` | Source checked; numeric tests pass for supplied rig | `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_shader-review-2026-10-16/project-snapshot/shaders/05_phong.gdshader:46` | Caveats stated in narration |
| B07 | No Scene Query; `uniform vec3 light_direction` | Source checked; numeric tests pass for supplied rig | `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_shader-review-2026-10-16/project-snapshot/shaders/05_phong.gdshader:20` | Caveats stated in narration |
| B08 | Know What It Teaches; `vec3 specular` | Source checked; numeric tests pass for supplied rig | `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_shader-review-2026-10-16/project-snapshot/shaders/05_phong.gdshader:24` | Caveats stated in narration |
| BHTF | Your Turn uses specular_power values 8 and 100 | PASS | `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_shader-review-2026-10-16/project-snapshot/shaders/05_phong.gdshader:23` | Both lie within `hint_range(0.1, 100.0, 0.01)`; suggested as practical comparison points |

Primary API reference: https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/spatial_shader.html (checked 2026-10-16). All sample calculations follow the displayed code; measured screen values are deliberately omitted to avoid confusing renderer-specific transfer with model weights. The original Cg host behavior is not claimed as independently verified.

Status: Claude Code build-stage sign-off 2026-10-17. All body-beat claims source-verified against `05_phong.gdshader` SHA 54630bc4. No OPEN rows.
