# Assignment 5 — Frictional Notes

The original predictions stayed in place. Earlier assignment write-ups are archived under a5/archive/pre-final-documents/.

## Observation → decision

- R3: subtracting 1/60 from 3.0 leaves a small positive residual after 180 steps. I kept gameplay timing and documented 181 steps / 3.016667 game seconds.
- R1: at 30 fps two physics steps may precede one process observation. Birth remains 1.0; the first process value may be 0.994444.
- Cargo: the final hall uses two crate_stack props, while their clasp surfaces retain the original material.
- Normals: the source averages about 1 degree tilt. I kept it and did not claim an obvious A/B normal difference.
- Lighting: the raking-light comparison exposes small differences; the review and ACES game setups remain distinct.
- System capture: GDI returned a flat frame. DXGI worked after fixing the borderless client dimensions before capture; both sampled points then matched.
- Regression load: the parallel market test exceeded 3 seconds. The isolated repeat passed; neither threshold nor expectation changed.

## Tool-count audit

The first audit counted every top-level tool_use occurrence, including duplicate messages inside api-request-blob records: 62, 76, 148 and 20. Counting distinct tool-use IDs gives **35, 44, 97 and 20**, including handback. evidence/a5/session-audit.json retains both counts and the reports.

| Session | Distinct calls | Report | Assessment |
|---|---|---|---|
| session-1 | 35 | about 32 of 40 | understated |
| session-2a | 44 | 43 before handback, 44 including it | matches |
| session-2b | 97 | 96 before handback, 97 including it | matches; 148 included duplicate snapshots |
| session-3 | 20 | audit count 20 | matches |

I therefore do not repeat the earlier conclusion that all first three counts were wrong. The implementation session did break its command allowlist: its report names tail and chained cd/grep/head/echo use. Correct counting does not erase that breach. Its full record is 1,577,697 bytes and stays local; the annotated course excerpt retains the prompt, tool index and report.

## Step 4 history

Codex first drafted notes while export was unavailable, then generated the 48-line shader through the real editor's native conversion actions. It revised the voice and translated the notes to English at my request. Export records were temporarily removed; the final evidence restores the program, logs, two earlier notes and the English draft. The current notes cite actual generated lines and completed pixel/TIME measurements.

Desktop control returned Computer Use native pipe is unavailable. I later requested scripting for the remaining work. No mouse-click session is claimed. Original export logs retain editor shutdown/resource-cleanup errors.

## Assistance

The initial CHANGE-BRIEF, its predictions and answers, and its read-only background
probe were also completed with Codex. The retained conversation establishes that
history; the later implementation guides do not replace that provenance.

Codex completed the three custom shaders, mutations and exact restoration, conversion export, language-note drafts, final verification tools, measurements, documentation, film and delivery preparation. The driver and main new tests came from the retained Claude implementation session. Existing gameplay formulas and old test expectations were preserved. The required fire color statement and material interface stayed exactly as supplied.

