# RIFF — the judgments the narration makes, and what each rests on

| Beat | Judgment | Rests on | Limit |
|---|---|---|---|
| B01 | "No model generated these props." | build scripts use only Blender primitives; every generator and library off in `get_addon_status`; no generator/library call in the session | a claim about this session's calls, not about every file Blender ever opened |
| B06 | "Exported like this, Godot would receive a scaled node." | glTF node transforms; the unit-scale check exists for this reason | not demonstrated by exporting the unapplied crate |
| B11 | "It cannot show whether they look right." | what the suite measures (AABB, node scale, counts, names) | — |
| B13 | the gate "blocks only where it should" | `collider-fit`; the block take; Bao: "灯臂下面可以通过" | one approach direction filmed |
| B14 | "One thing Claude got wrong" | A3-R0's sentence vs the fixed camera at 7e117ce | found by Claude while preparing the human check, not by a test |
| B16 | colour shift and z-fighting are acceptable limits | Bao's own words after his look | one viewer only |
| B18 | "How they look is Bao's judgment." | the assignment's human check; B16 | — |

Observations the film reports from viewing the media (not from tests): the two lanterns stay separate from the post
from the front and behind (look renders); the barrel's base and the crate's underside show through each other from
below (look render, and Bao in the room); Godot draws EmberGlass and OilGlow pale yellow against Blender's pale
orange preview (orbit captures).
