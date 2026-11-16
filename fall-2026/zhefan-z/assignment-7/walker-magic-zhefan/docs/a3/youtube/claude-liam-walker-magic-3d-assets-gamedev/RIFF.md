# RIFF — walker-magic Assignment 3 gamedev film

| Artifact + time range | Visible observation | Interpretation and its source | Narration | Suggested next experiment |
|---|---|---|---|---|
| run-01 0.0–2.0 s (B16) | The saved camera: dark #0F1119 background, floor to the horizon, mage, rock, crystal, chest left to right, all on the floor with shadows | The scene fixes took effect (prop_room.tscn lines 16–18, 40) | "Here it is running, at native 4K, with a scripted camera. The props stand on the floor beside a 1.45-metre mage." | Put the camera at the 2D game's eye height and compare the props' screen size with the 64 px sprite |
| run-01 2.0–6.5 s | The camera swings right; the mage keeps facing it; at ~6 s the chest's unlit right end fills the lower right | Y-billboard (line 40); one light from the front-left | "As the camera swings behind them, she keeps facing us" | — |
| run-01 7.5–12.0 s | From behind, rock and chest almost black; the crystal stays blue; the mage still shows her front | One DirectionalLight3D and no ambient beyond the dark background; the crystal's emission; billboarding | "a flat sprite always shows her front — and with one light from the front, the rock and the chest go almost black, while the crystal keeps its blue." | Add the planned torch beside the chest and look from behind again |
| B06 look renders | First build: three separate rounded stones; Revision 1: one mass | FRICTIONAL.md, TEST-REPORT.md cycle 1 | "it read as three dice … Revision 1 fits with factors of exactly one" | — |
| B14 my screenshots | Grey background, floor edges, the mage as a line from above | TEST-REPORT.md HUMAN CHECK (the author's observations) | "the background was Godot's default grey, the floor's edges showed, and from the side the mage became a thin line" | — |

Observations are from viewing the frames listed in CAPTURE.md and the images themselves; the interpretations name their source. The footage is a scripted camera, not a human look; the human look is the author's (TEST-REPORT.md).
