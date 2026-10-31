# Assignment 5 — Submission

Course folder: [walker-downfall](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/tree/Jingyao_Y/fall-2026/jingyao-y/assignment-5/walker-downfall/).
The final release is identified by the a5 tag.

Open project.godot with Godot 4.7.2 and import before running game/main.tscn.
The renderer is Forward+ with D3D12 on Windows. The complete game source and
assets are included; .godot caches are regenerated. No engine executable is bundled.

Required documents: CHANGE-BRIEF, CLAUDE, LANGUAGE-NOTES, MATERIALS, TEST-REPORT,
FRICTIONAL, SOURCES and README. Prompts, session records and the annotated oversized
session excerpt are under a5/. Test, mutation, pixel and import evidence is under
evidence/a5/. SHA-256 source inventory: evidence/a5/delivery-manifest.json.

The fire tests pass 89/89 at 30, 60 and 144 fps; the material audit passes 120/120.
The original fire predictions match all seven specified RGB samples. The hint
experiment retains two RTX 4060 and two AMD 610M runs. The resolved 73-suite
baseline is 70/73, with the same three pre-existing failing suites; the extra
parallel performance failure and its isolated passing repeat are both retained.
See TEST-REPORT for the limits of these results.

The landscape film is Downfall: Fire, Texture and Shader Evidence. Its 4K master
is included in the Canvas package's film/ folder. Film source records, source/result
pairs, provenance and verification receipts accompany the project. Rendered video,
audio and intermediate media stay outside GitHub under the course media rule.

The Canvas ZIP contains this submission note, the complete walker-downfall project,
the film, and final fresh-clone verification receipts. The verification identifies
the tested GitHub commit and confirms its runtime source hashes; evidence/report
updates after that tested commit do not alter the game or test code.
