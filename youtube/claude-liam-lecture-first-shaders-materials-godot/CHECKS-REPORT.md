# CHECKS-REPORT.md — PROOF GATE (written 2026-10-16, layout stage)

Beats: 81 · measured runtime 1011 s (16.8 min) · PROOF GATE classes {'CARD': 2, 'SHOW': 79}.
A lane histogram is information, never a quota.

## Lane histogram
- manim: 69
- bookend: 6
- remotion · CCPlainShell: 6

## Runtime by act
- Opening: 44 s
- I · Two Shaders and Their Materials: 94 s
- II · Predict Before You Write: 126 s
- III · Give the Agent Rules: 67 s
- IV · The Shader From Code: 114 s
- V · A Shader That Reads Textures: 56 s
- VI · Textures Are Information: 111 s
- VII · Read the Language: 107 s
- VIII · What the Agent Gets Wrong: 41 s
- IX · Check What You See: 129 s
- X · Ship It, and How It's Graded: 84 s
- Closing: 39 s

## Whole-sheet teaching-arc checklist (nopunt)
- [x] FRAMEWORK beat before the worked example — Act II (B09-B18) presents what the change brief commits to (state, specification, colour line, measurable rules, controlled inputs, the hint-experiment predictions, material plan, predicted failures); Acts IV-IX run the example against exactly those fields.
- [x] WORKED EXAMPLE — Acts IV-IX walk the instructor example (labelled as such) through the wrapper, the driver, the mutations, the textured shader and two materials, the hint experiment in two renderers, the normal-map calibration, the audit and the human checks, each with a real log or a real engine capture.
- [x] FALSIFIABILITY / edge-case beat — B33-B34 (mutations: a deleted semicolon and a renamed uniform; the driver test still passes), B48 (deleting source_color), B62-B64 (the colour shortfall, the renderer, hint range does not clamp), B56-B58 (what the agent gets wrong).
- [x] SCAFFOLDED viewer task — BHTF: a paste-able prompt and two checks the viewer runs.
- [x] Bookends — BOPEN (narrated portrait/title), BIDEA (writer), BDEFS (terms) and BVDT, BHTF, BOUT (channel outro); no composer cold open, by the lecture skill's own spine.
- [ ] No source, no verdict — every body beat that asserts a number or a named result carries an on-screen artifact: verify per beat at the stills pass (open items are listed in BUILD-LOG.md).

## Open items
See BUILD-LOG.md.
