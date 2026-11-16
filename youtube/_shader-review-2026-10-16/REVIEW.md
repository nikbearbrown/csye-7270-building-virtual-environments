# Shader review — 2026-10-16

Verdict: all sixteen shaders are suitable for these teaching films, with the scope and caveats below. They are educational, manually lit materials; this is not certification as general production PBR materials.

## Evidence from this review

An isolated project snapshot preserves the source shaders, scripts, textures and verifier. `source-hashes.json` identifies the reviewed inputs. The original project and its earlier evidence were not overwritten.

Installed engine: Godot 4.7.2.stable.official.ed1daf0bf. Fresh windowed rendering on Forward+ and Compatibility: **134 checks passed per renderer, zero failed (268 total)**. Eight engine logs contain no ERROR, SCRIPT ERROR, SHADER ERROR, or failed-check lines. Logs sit beside this report. The inherited harness exits zero even when a numeric assertion fails, so results were checked from SUMMARY and failure lines, not exit status alone.

The checks cover the supplied sphere/torus rig and test textures, named pixel predictions, selected image comparisons, shader equivalence, displacement silhouettes, UV transformations and four blend variants. They do not establish arbitrary imported-mesh behavior, nonuniform-scale tangent correctness, all edge cases, performance, or Maya/CgFX host fidelity.

Visual review: `shader-contact-sheet.jpg` covers fourteen primary shader outputs; `variants.jpg` covers UV manipulation and the four rendering techniques. All were inspected. The diagnostic TIME square in numeric-test images is instrumentation, not part of the intended film. Separate clean demonstrations were recorded by `project-snapshot/tools/film_capture.gd` into `captures/`; capture labels state actual inputs. These are offline fixed-step demonstrations, not frame-rate benchmarks.

## Findings the narration must preserve

- **00:** explicit POSITION transformation is a teaching choice; most Godot materials can use the default transform. Unshaded output has no built-in scene lighting.
- **01 / 02:** executable shader bodies are identical. Keep separate films only with distinct objectives: normal/varying data flow, then Lambert's angular model.
- **03:** source-color 0.15 is approximately 0.0196 linear in Forward+. The shader comment and inherited series plan's unconditional “1 + 0.15 = 1.15” claim is not correct for that renderer/input path. Films avoid that claim. A constant ambient term does not compute occlusion or bounced-light geometry.
- **04:** this is an artistic Fresnel-inspired rim, not a complete Fresnel reflectance equation. Positive exponents are used in demos; the exposed zero exponent at a zero base is not a portable teaching example.
- **05:** a Phong lobe and manually specified light are not traced reflections or a physical roughness model.
- **06 / 11:** comments claiming Godot always defaults to clamp contradict the project's measured repeat test. The film says `repeat_enable` explicitly requests repetition, without asserting a universal default. No original shader arithmetic was changed.
- **07:** the rim loses the diffuse-plus-ambient factor, deliberately preserving the source. It can glow on the dark side. R masks rim; G masks highlight.
- **08 / 11 / 12 / 15:** the inherited tangent transformation applies MODEL_NORMAL_MATRIX to tangent/binormal as well as normal. Suitable for these uniformly scaled fixtures; not a general tangent-frame solution under nonuniform scaling. Normal textures are read as data, not source colors; compressed two-channel normal textures were not tested.
- **09:** environment reflection is rim-weighted and vanishes at a camera-facing normal. The separate Phong highlight can still appear there. The cubemap is stored imagery, not a scene ray trace.
- **10:** vertex deformation keeps both the original normal and the eye vector computed from the original vertex. These are intentional source-port limitations; they must not be presented as fully corrected deformed lighting. Zero offset is motionless; demo overrides it.
- **11:** positive scale two tiles more, rather than zooming in. All three maps share the transformed UV; their tangent frame stays on the mesh. Mirroring/rotation needs further normal-map treatment.
- **12:** variants are alternatives, not four passes. Godot scissor discards below 0.3; original Cg comparison discarded at equality too. The source's unspecified blend-function default remains a host-behavior assumption.
- **13:** R selects first color, B second, G third. The shader does not normalize arbitrary weight sums.
- **14:** artistic layered contributions; Fresnel offset is added before lighting multiplication, so it is not an unconditional final reflection floor. Cubemap contrast is componentwise exponentiation, not physical reflectance.
- **15:** different channel packing: R highlight, B reflection. Green flip defaults true for the supplied DirectX-style map. Hemisphere ambient uses clamp(n.y,0,1), not (n.y+1)/2. Wrap/tint controls do not simulate internal scattering; reflection has no Fresnel multiplier here.

## Sources and preservation

Original source provenance remains in `shader_lessons_godot/SOURCES.md`: converted from Eat 3D lesson files with author credit Luiz; no redistribution license was found. This review and local film preparation do not publish or push those sources. Existing source comments were left intact so other work is not silently changed; corrections are explicit in this report and the film narration.

Reference checked: https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/spatial_shader.html (2026-10-16). The installed engine and reproduced output are the version-specific execution evidence.
