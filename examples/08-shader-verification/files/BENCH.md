# Failure-flash visual bench

This is a human visual check. Headless Godot validates the scene and uniforms,
but its dummy renderer cannot establish what the shader actually draws.

1. Import `godot/project.godot` in Godot, then open
   `res://tests/flash_bench.tscn`. Run that scene or use the editor's 2D view.
2. Confirm the background is `#f6f3ec` and the three copies are labelled
   `flash_amount 0.0`, `0.5`, and `1.0`.
3. Take a screenshot without rescaling or color correction. Sample a pixel well
   inside the body and one well inside an eye on each copy (avoid edges).
4. Run the CPU reference table with:

   ```sh
   godot --headless --path godot --script res://tests/flash_model.gd --fixed-fps 60
   ```

5. Compare the sampled RGB hex values with `FLASH_MODEL_COLORS` in its output.
   Allow one step per channel at `0.5`: a half-way value such as 82.5 can round
   to 82 or 83. (Human review addition.)
   Alpha cannot be established from a screenshot against an opaque background;
   inspect the clear area around Clawd separately if alpha evidence is needed.

Expected model values:

| Source | 0.0 | 0.5 | 1.0 |
| --- | --- | --- | --- |
| body `#dd775b` | `#dd775b` | `#815653` | `#25354a` |
| eyes `#000000` | `#000000` | `#131b25` | `#25354a` |

A mismatch means the rendered shader path does not implement CLAUDE.md rule 4
for these code-drawn rectangles. It does not, by itself, identify whether the
cause is shader input (`COLOR` versus a texture sample), material placement,
renderer behavior, screenshot color management, or pixel sampling. Preserve the
screenshot and sampled coordinates before changing the implementation.
