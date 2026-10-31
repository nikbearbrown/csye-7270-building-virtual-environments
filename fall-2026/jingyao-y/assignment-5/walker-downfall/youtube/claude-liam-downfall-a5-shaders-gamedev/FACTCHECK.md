# Fact check

- Fire color statement is copied verbatim from CHANGE-BRIEF and shader line 17.
- The controlled fire samples match all seven original predictions; no prediction was fitted after capture.
- hint_range stores 2.0 and renders the predicted (210,255,67) center.
- TIME advances 2/1/4/0 seconds across 120 fixed-60-fps frames at scales 1/.5/2/0. These are simulation intervals, not real-time FPS.
- Fire endpoint: 181 physics steps / 3.016667 game seconds. The 180-frame counter example is explicitly hypothetical.
- Hint texture samples are 64/128/192 and 137/188/225 on both installed adapters, with two retained runs each.
- Corrected DX normal differs from GL by at most 1/2 RGB8 levels under review/raking lights. The map is very flat; normal differences are not overstated.
- Shared shader edit changes both panels; A-only tint leaves B pixel-identical. The source is restored byte for byte.
- The 48-line generated shader is not used by game materials. Its material bindings are supplied separately in the BoxMesh render.
- The GDI capture failed; the subsequent DXGI same-frame capture succeeded and matches both sampled fire points.
- The parallel regression is 69/73, resolving to baseline 70/73 after an isolated timing repeat; the three old failing suites remain.
- No human-only playtest, complete-game walkthrough or Inspector mouse session is claimed. The demonstration is bounded to A5.
