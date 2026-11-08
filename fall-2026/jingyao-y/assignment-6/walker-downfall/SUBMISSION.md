# Assignment 6 — Submission

Course folder: [walker-downfall](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/tree/Jingyao_Y/fall-2026/jingyao-y/assignment-6/walker-downfall/).
The final release is identified by the `a6` tag.

Open `project.godot` with Godot 4.7.2 and run `--import` once before running
`game/main.tscn`. The renderer is Forward+ with D3D12 on Windows. The upload is
the game's export whitelist plus `.import`/`.uid` sidecars, every test and
script, the data files the existing suites read, and the A6 work; art sources,
reference sheets and Blender files stay out. `.godot` caches are regenerated.
No engine executable is bundled. On Windows, clone to a short path or set
`git config core.longpaths true` (one film receipt path is long).

**Effects.** Effect A `effects/hit_spark.tscn`: a one-shot burst (Flash,
Sparks, Puff) on every landed operator melee hit, overlapping, freed by its own
timer. Effect B `effects/fire_pit_flames.tscn`: the Sami fire pit's flames and
embers on the GPU with turbulence and preprocess, its `amount_ratio` driven by
the fuel left (`entities/fire_pit.gd`).

**Required documents:** CHANGE-BRIEF, CLAUDE, TUNING, TEST-REPORT, FRICTIONAL,
SOURCES and README. Prompts are under `prompts/`, session records (labelled
excerpts where large) under `sessions/`, frame strips under `captures/`, test,
mutation, GPU and user evidence under `evidence/a6/`, the generated process
shader at `shaders/particles_generated.gdshader`.

**Results** (TEST-REPORT has the limits):

- Configuration tests 165/165 (A) and 123/123 (B); both state tests pass at
  60 fps; mutations M1 (Godot 3 float spelling) fail the config test as
  predicted.
- Tuning: one revision per effect driven by the user's runtime observation,
  both kept by the user (A: Puff quad 0.5 → 1.0; B: Flames quad 0.30 → 0.55);
  partial prediction misses recorded in TUNING.
- Price: headless CPU indistinguishable from the empty-scene control; GPU
  `Update GPU Particles` from the user's Visual Profiler: A 0.14 ms (budget
  0.25), B 0.09 ms (budget 0.15).
- Suites: 78/89 before A6 → 82/93 after in the working folder. Fresh clean
  clone of the final commit: 78/93 in parallel, all four A6 suites passing;
  the extra load failures pass alone except `test_elevation`'s intermittent
  floor-build race (pre-existing). The first fresh clone found four suites
  missing data files; they were added before this release.

**Film.** Brutalist godot-gamedev, walker modifier, Liam (local Kokoro):
`youtube/claude-liam-downfall-a6-particles-gamedev/`. 11:36, 3840×2160, 30 fps.
SHA-256 `33d15797d825922546e397b935e8527bbc7d85f4cda731276e1400df883666a2`;
checker PASS (16 code→result pairs). The user watched and listened to the
final export: "No problems". The 4K master is kept locally; rendered
video, audio and intermediate media are not uploaded to GitHub at the user's
request. Film source records, provenance and the verification receipt are in
the folder.

**Agent use.** Claude Code (Claude Opus 5.5) plus delegated agent sessions in
place of `claude -p` (the CLI is not installed on this machine); FRICTIONAL
separates the agent's work from the user's.
