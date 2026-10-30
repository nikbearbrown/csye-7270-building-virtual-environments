# source_color mutation — 2026-10-30

Who: the student removed `source_color` from `albedo_tex` in
`shaders/cargo_panel.gdshader` by hand and restored it by hand. No agent edited
the shader. Claude Code ran the test and compared the files.

| Run | Shader | Command | Exit | Result |
|---|---|---|---|---|
| before | as committed in f099d98 | `./scripts/run-test.sh test_materials.gd 60` (fresh A5 cache, `logs/fresh_cache/`) | 0 | 120 PASS |
| mutated | line 3 without `source_color, ` (`source-color-removed.diff`) | same | **1** | `FAIL cargo_panel.gdshader albedo_tex hints …`, `RESULT FAIL, 1 failure(s)` (`source-color-removed.log`) |
| restored | byte-identical to f099d98 (SHA-256 `916a00df69680581ec864af1bbc7d899e3792fc651e4a276315423b51cb9a277`, `cmp`) | not rerun, at the student's instruction | — | — |

Only the source-text hint check caught the mutation. `get_shader_uniform_list()`
reports all three samplers as `Texture2D` with or without `source_color`, so the
uniform-list checks still passed. The restored file was not retested; it is the
same bytes as the file that passed 120/120 in the fresh-cache run.
