# RIFF — walker-magic Assignment 5 gamedev film

| Artifact | Visible observation | Interpretation and its source | Narration | Suggested next experiment |
|---|---|---|---|---|
| hurt_tint_i0.0 / 0.5 / 1.0 (B05) | The mage keeps her blue hat and pale hair at 0; at 0.5 she is half red, the hair pink; at 1 a flat red silhouette, transparent pixels still transparent | Line 7 mixes COLOR toward red by intensity and leaves alpha (CHANGE-BRIEF.md §2); the two x.5 channels one lower (TEST-REPORT.md) | "At one half, four of the six channels match the prediction exactly…" | More x.5 cases to test the rounding (B26) |
| hurt_tint_grey_i2.0 (B08) | The mage looks like a colour negative: the hair dark, the hat yellow-olive | 2 × 127.5 − stored, unclamped (TEST-REPORT.md) | "exactly the unclamped prediction" | — |
| rock_compare_default (B10) | Left rock warm grey-brown; right rock paler and cooler with mottled frost; the top stones identical on both | frost_amount 0.65 on low-roughness areas; Rock_Top keeps its imported material (revision 2026-10-27) | "a pale frost where the roughness map is low" | — |
| rock_one_material_changed / after_shader_edit (B11) | First: only the left rock's relief flattens; second: both rocks darker | One value in one material vs one line of the shader (TEST-REPORT.md measurements) | "Values live in the material; the code lives in the shader." | — |
| hint_quads (B13) | Left quad 64/128/192; right quad visibly lighter, 137/188/225 | sRGB decode vs data (CHANGE-BRIEF.md §3) | "Same bytes; the hint decides what they mean." | — |
| frost_amount sweep (B17) | 0: no frost; 0.65: frost layer; 1.0: near-white block | Threshold sweep at line 33 (rock_frost.gdshader) | "a white crust buries the rock's detail" | Sweep the planned ice_roughness uniform (B29) |
| interface sweep (B19) | base_tint black: dark rock with white frost; roughness 0: sharp highlight; frost_color black: soot | TEST-REPORT.md observations | "nothing broke the render" | — |

Observations are from viewing the captures themselves at their enlargement; the interpretations name their source. The look judgments are the author's (TEST-REPORT.md, translated there from Chinese).
