from pathlib import Path
import json,collections,hashlib
R=Path(__file__).resolve().parent;T=R.parents[2]/'brutalist.art';B=R.parents[2]
C=json.loads((R/'content.json').read_text());S=json.loads((R/'beat_sheet.json').read_text());E=json.loads((R/'evidence/physics-results.json').read_text());web=json.loads((R/'evidence/web-captures.json').read_text());counts=collections.Counter(x['lane'] for x in S['beats'])
(R/'SHOTLIST.md').write_text('# Shot decisions\n\nEvery body beat is SHOW. Conceptual diagrams are labeled; engine output and documentation are actual captures. No photographic HOLD, no generated media, no fictional app session. Each body topic was searched against the scene library (evidence/library-per-beat.json); registered components were checked before use.\n\n| Beat | About | Lane picked | Runner-up | Why this wins | Motion |\n|---|---|---|---|---|---|\n'+'\n'.join('| '+' | '.join([x['id'],x['topic'],x['lane'],x['runner_up'],x['why'],x['motion']])+' |' for x in C['body'])+'\n\n## Tool evidence rungs\n\n- BrowserCapture: real official public documentation and native Godot viewport output (rung 1). Camera targets the relevant property or result, with transitions outside 45–55%.\n- ClaudeCodeBeat: executed GDScript and actual saved scene excerpts (rung 2); conventions are an authored document, not executed code. No invented compiler output. Exact excerpt source ranges are in evidence/excerpt-map.json.\n- CCPlainShell: real local logs, no fictional shell or agent conversation.\n- Manim: deliberately labeled conceptual geometry or plots of actual JSON measurements. Show Tell isometric handoffs were auditioned for B01/B07; precise scene relationships and callback direction teach more directly here. There is no isometric quota.\n- No Claude Code or Codex session is claimed; the learner composer prompt is explicitly a prompt to paste.\n')
refs={
0:'sources/research-notes.txt Parts 1–2; sources/overview.txt; docs-scenes.txt; godot/actor.tscn; evidence/physics-results.json',
1:'research Parts 3–4; overview collision section; docs-physics.txt, docs-rigid.txt; layers.gd; both physics result JSON files',
2:'research Part 5; overview movement section; docs-character.txt; godot/player.gd; engine trajectory and supplemental timer tests',
3:'research Parts 6–7; docs-oneway.txt; official TileMapLayer 4.7 reference; coin.gd, enemy.gd, tile_hit.gd; both result JSON files',
4:'research Parts 8–9; docs-physics.txt, docs-problems.txt, docs-interpolation.txt; thin-floor sweep and jump measurements',
5:'research Parts 10–12; overview 3D/exercise; docs-jolt.txt, docs-geometry.txt, docs-migration.txt; CONVENTIONS.md; supplemental debris tests'}
corrections='''## Material corrections

| Source claim | Decision and evidence |
|---|---|
| Physics is deterministic | Corrected. The official physics introduction explicitly disclaims determinism. Fixed ticks are a scheduling choice, not a cross-device replay guarantee. |
| speed / ticks < thickness guarantees no tunneling | Rejected as a theorem. Retained as a travel-distance diagnostic. The local swept CharacterBody test hit a 4 px floor across 300 px displacement. CCD is a mitigation, not a guarantee. |
| Jolt only through GDExtension; GodotPhysics always default | Corrected using the checked official Jolt page: integrated since 4.4; new projects default to Jolt in this reference. Inspect existing project settings. |
| Every lower Node inherits transforms | Narrowed to spatial/CanvasItem transform relationships with top-level exceptions. The lab verifies a Node2D parent/child case only. |
| CharacterBody cannot push rigid bodies | Corrected: it can affect bodies in its path. A chosen impulse policy is explicit code and requires actual collision filtering. This lab does not claim a complete push-mechanics test. |
| Deferred monitoring guarantees one award | Added an immediate claimed latch, tested with a repeated call. Deferred physics mutation and gameplay idempotence are separate concerns. |
| Origins alone reliably decide stomps | Treated as a heuristic. The companion shows a top/side sensor design, tested for one defeated event and bounce; corner ordering remains a game policy to test. |
| Scalar local/default gravity ratio | Not prescribed: loses vector direction and has a zero-default edge case. Explain intentional integration of local gravity instead. |
| Moving in _process always creates frame-dependent displacement | Narrowed: correct delta scaling can preserve speed, but collision scheduling differs; use _physics_process for this lab's collision motion. |
| Every scene must run alone; no agent can see gameplay | Labeled project policies, not universal engine facts. Suitable fixtures and actual tool access govern what can be tested. |
| Jolt 4.7 migration details | Corroborated by the live full page: plane-distance sign, soft-body mass/stiffness, Area3D soft-body overlaps. B46A shows the official record. |
| Tile RID maps to a cell | Reproduced local counterexample: requested/contact cell (3,0), RID quadrant (0,0). Official 4.7 TileMapLayer reference supports this distinction. |

## Algebra and numeric checks

For h=72 px and t=0.38 s: g=2h/t²=997.2299168975 px/s², vy0=-g*t=-378.9473684211 px/s. Continuous height at the apex is 72 px. The measured discrete controller apex is 75.2320251464844 px; a ±10% rubric is [64.8,79.2]. This is a selected grading tolerance, not a Godot standard. Impulse 120 with mass 2 predicts Δv=60; observed first sampled vx≈59.8002 includes step damping. Shape/ray CCD enumerations were read from the installed engine. No statistical generalization is claimed from these small experiments.

## Limits

32 tested cases, not 32 exhaustive features. Tests cover isolated mask behavior, repeat-event latches, instance transforms, a sampled jump, one rigid impulse/contact setup, a tile contact, a long swept movement, property/enumeration checks, shape-resource ownership, selected timer branches, platform displacement, and debris creation/impulse. Platform carrying/leaving velocity, drop-through clearance, tilted one-way play, side/top corner priority, cross-device behavior, and control feel remain outside this evidence. The film says so. No existing course reference game was supplied or audited.

'''
(R/'FACTCHECK.md').write_text('# Claim review — 14 October 2026\n\n'+corrections+'## Per-beat record\n\n| # | Beat | Claim / topic | Verdict | Source | Fix / limit |\n|---|---|---|---|---|---|\n'+'\n'.join(f"| {i+1} | {x['id']} | {x['topic']} | {'Executed evidence' if x['lane'] in ['shell','code'] and x['asset'] not in ['conventions','migration_excerpt'] else 'Documentation / labeled model'} | {refs[x['act']]} | Apply corrections and limits above; do not infer whole-game correctness. |" for i,x in enumerate(C['body']))+'\n')
(R/'SOURCES.md').write_text('# Sources and provenance\n\n## Supplied source material\n\n'+f'- {R}/sources/research-notes.txt — full research attachment, originally /Users/bear/.codex/attachments/590e6154-14b6-4954-a47c-edd5c85d51fc/Pasted text.txt.\n- {R}/sources/overview.txt — full shorter attachment, originally /Users/bear/.codex/attachments/b79d6ca9-a2bb-4fe0-a9f8-996759b21c31/Pasted text.txt.\n- User message in this chat — Scenes / Collision Architecture / Physics Engines overview; distinct claims mapped in ACTS.md.\n\n## Official references checked and captured\n\n'+'\n'.join(f"- [{x['title']}]({x['resolved_url']}) — HTTP {x['status']}, 14 October 2026; {R}/sources/docs-{x['name']}.txt and {R}/captures/docs-{x['name']}.png." for x in web)+'\n- [TileMapLayer 4.7](https://docs.godotengine.org/en/4.7/classes/class_tilemaplayer.html) — quadrant size and RID lookup, independently checked through web tool; also reproduced locally.\n- [Area2D 4.7](https://docs.godotengine.org/en/4.7/classes/class_area2d.html) — overlap filtering/signals, checked through web tool and local experiment.\n\n## Original evidence\n\n'+f'Engine: /Applications/Godot.app/Contents/MacOS/Godot, reported 4.7.2.stable.official.ed1daf0bf; Compatibility/OpenGL 4.1 Metal on Apple M4 Pro. All gameplay captures are authored isolated experiments rendered by the actual engine into a native 3840×2160 SubViewport. They are not screenshots of an existing class reference game and not a human playtest. Actual logs, JSON results and source hashes live in {R}/evidence/.\n\nCode snippets preserve executed source and record ranges in excerpt-map.json; code excerpts may combine separately identified lines. Source conventions are authored guidance, not a historical repository record. Conceptual Manim scenes are clearly labeled. No generated media, third-party gameplay art, or recreated app results. Documentation retains its real visual appearance and attribution.\n\n## Lineage retained from supplied notes\n\nThe notes name Glenn Fiedler’s fixed-timestep explanation, Ericson’s collision text, Catto/Box2D, Pittman’s jump parameterization, Thorson’s platformer physics article, Monteiro’s platformer taxonomy, and Swink’s Game Feel. These are retained as source-provided further reading; no additional quotation or unverified finding is attributed to them. Rapier is mentioned only as source-provided optional research, not a verified determinism recommendation.\n')
(R/'PROMPTS.md').write_text('# Prompts\n\nNo paid or generated-media prompts. Liam narration uses local Kokoro am_onyx in the render stage.\n\n## Learner prompt\n\n'+S['beats'][-2]['narration_text']+'\n\nChecks: coin awards once and disabling its mask prevents detection; declared jump tolerance passes, with platform carrying tested separately.\n')
(R/'CHECKS-REPORT.md').write_text(f'''# Preparation checks

Status: stage-one layout prepared; final film gates have not run.

- {sum(b['proof_gate']=='SHOW' for b in S['beats'])} SHOW; 0 HOLD; 0 PUNT; {sum(b['proof_gate']=='CARD' for b in S['beats'])} CARD (identity, definitions, act dividers).
- Framework B01 before examples; worked example across B15–B18 and B19–B29; falsifiability B33/B38; scaffolded task BHTF; required opening and closing sequences present.
- Lane histogram (information, not quota): {dict(counts)}.
- 32 local physics/logic checks pass. Six native engine captures and twelve documentation captures inspected as a contact sheet; tile contact also inspected at full detail. Capture QA does not certify film layout.
- Python parses; registered compositions checked; every body has a runner-up, visual intent, motion, and source. Static Manim checker and beat lint results are in evidence/.
- Runtime validate_project / validate_approvals must pass. No fabricated human approval records.
- Legacy schema's CARD exclusion conflicts with the current mandated lecture BOPEN contract; leave shared schema unchanged, use current runtime validation, and document the mismatch.

Not run: TTS, audio listening/transcription, Manim frame render, Remotion film stills, Gate A render, Gate B/V/T, final assembly, final master inspection, bookend gate. All belong to stage two. No MP4 or measured film runtime is claimed.

Visual review must inspect math at 15/50/85%, all body stills, capture zooms, code density and timing. Do not equate static checks with a rendered-frame pass.
''')
(R/'README.md').write_text(f'''# {C['title']}

A CSYE 7270 Building Virtual Environments lecture prepared for Liam in for Bear, @NikBearBrown. Six acts, {len(S['beats'])} beats, 2,275 words, estimated 14 minutes 45 seconds before audio measurement. No audio or film master has been rendered.

Read {R}/NARRATION.md and {R}/BUILD-PROMPT.md. The latter is the self-contained render handoff.

The separate lab is at {R}/godot/project.godot. It is a collection of scripted experiments, not a finished platformer. Run commands and evidence limits are in CAPTURE.md and FACTCHECK.md. All 32 local checks passed; human control-feel testing and complete moving-platform behavior remain outside that evidence.

Layout: ACTS.md, SHOTLIST.md, FACTCHECK.md, content.json, make_sheet.py, beat_sheet.json, scenes.py. Source scripts and exact evidence travel with the lecture. No changes were made to other course films or a course reference game.
''')
(R/'CAPTURE.md').write_text(f'''# Reproduce the evidence

Commands may run from {B}; every project path is explicit.

```bash
/Applications/Godot.app/Contents/MacOS/Godot --headless --path {R}/godot --editor --import --quit
/Applications/Godot.app/Contents/MacOS/Godot --headless --path {R}/godot --quit-after 600
/Applications/Godot.app/Contents/MacOS/Godot --path {R}/godot --quit-after 600
/Applications/Godot.app/Contents/MacOS/Godot --headless --path {R}/godot --script res://supplemental.gd
python3 {R}/capture_docs.py
python3 {R}/extract_excerpts.py
python3 {R}/verify_evidence.py
```

Capture stdout/stderr into the corresponding evidence logs when rerunning. The rendered main run creates six 3840×2160 viewport PNGs and physics-results.json; headless mode skips PNG capture. Supplemental creates supplemental-results.json. Do not overwrite the final rendered result JSON with headless results and still call it rendered evidence. Preserve earlier failed logs when fixing a problem.

Scripted setups and direct test calls are explicitly identified. No hidden teleport was used to claim normal gameplay; respawn itself is an isolated function test. None of these captures is a normal-input walkthrough or human playtest.
''')
print('Documentation written')
