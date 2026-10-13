from pathlib import Path
import json,collections
R=Path(__file__).resolve().parent
c=json.loads((R/'content.json').read_text());s=json.loads((R/'beat_sheet.json').read_text())
rows=c['body']; counts=collections.Counter(b['lane'] for b in s['beats'])
shot=['# Shot list','', '| Beat | About | Lane picked | Runner-up | Why this one wins | Motion |','|---|---|---|---|---|---|']
for b in rows:shot.append('| '+' | '.join(str(b[k]).replace('|','/') for k in ['id','topic','lane','runner_up','why','motion'])+' |')
shot+=['','All body beats are SHOW. Act titles and the mandated identity/terms cards are CARD. No HOLD and no open media requests.','', '## Real-tool evidence','All capture beats use BrowserCapture, rung 1. App captures set frame=app and carry no invented URL. Web captures show the exact public address. Code beats use the registered ClaudeCodeBeat, displaying executed source excerpts; they do not portray a historical Claude session. Shell beats are recorded local output on CCPlainShell, not a Claude Code transcript.','', 'Library searches and renderability checks: evidence/library-search.json. Shader-specific diagram misses were resolved with eleven literal Scene subclasses in scenes.py. No unrelated generic scene was selected from a keyword hit. Show Tell isometric alternatives were auditioned for the pipeline, ownership, transport, and experiment beats; each decision appears above.','', 'The first and closing three beats follow lecture/SKILL.md. Each act has a FormACard title. Bookend labels contain no film ordinal or total.']
(R/'SHOTLIST.md').write_text('\n'.join(shot)+'\n')
links={
'language':'https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/shading_language.html',
'canvas':'https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/canvas_item_shader.html',
'spatial':'https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/spatial_shader.html',
'intro':'https://docs.godotengine.org/en/stable/tutorials/shaders/introduction_to_shaders.html',
'migration':'https://docs.godotengine.org/en/stable/tutorials/shaders/converting_glsl_to_godot_shaders.html',
'first2d':'https://docs.godotengine.org/en/stable/tutorials/shaders/your_first_shader/your_first_2d_shader.html',
'first3d':'https://docs.godotengine.org/en/stable/tutorials/shaders/your_first_shader/your_first_3d_shader.html',
'visual':'https://docs.godotengine.org/en/stable/tutorials/shaders/visual_shaders.html',
'compute':'https://docs.godotengine.org/en/stable/tutorials/shaders/compute_shaders.html',
'book':'https://thebookofshaders.com/',
'community':'https://godotshaders.com/'}
(R/'SOURCES.md').write_text('''# Sources and provenance

Reviewed 13 October 2026. User's pasted transcript is preserved verbatim in sources/user-transcript.txt; its creator, exact video title, and URL were not provided. No attribution has been invented. The user's learning-path notes are preserved in sources/request-notes.md. Narration is an original teaching rewrite, not the transcript read aloud.

Course context: ../../book.md and ../../modules/06-shader-foundations/lesson.md. These orient the course credit and verification emphasis; this film does not claim to adapt that entire separate module or teach the full assignment.

## Primary references
'''+'\n'.join(f'- [{k}]({v})' for k,v in links.items())+'''

## Executed evidence
- Godot 4.7.2.stable.official.ed1daf0bf, OpenGL 4.1 Metal / Compatibility, Apple M4 Pro. Actual stdout/stderr: evidence/godot-run.log. Twenty positive shader files, with actual GPU-rendered SubViewport captures at 3840×2160.
- godot/lab.gd is a deterministic teaching harness, not human gameplay. It sets material values, renders, and reads selected pixels. It does not establish real-time performance.
- evidence/negative-type.log is a real, deliberately invalid assignment. The small negative program exits normally after Godot logs the shader failure. Never interpret exit code alone as validity.
- evidence/godot-first-attempt.log preserves the initial switch failures. Adding explicit default breaks corrected both examples; the clean run overwrote only the canonical positive log, not the preserved first attempt.
- verify_evidence.py performs 24 pixel checks with 2/255 tolerance and checks diagnostics. Report and numeric samples are in evidence/verification.txt and evidence/pixel-checks.json.
- captures/godot-editor.png is a native editor screenshot obtained through computer use. It shows preview.tscn with ColorRect and its Material field. Do not claim the screenshot shows expanded uniform controls.
- capture_docs.py captured public pages at 1600×900 CSS and DPR 2.4. The URL/date/status manifest is evidence/web-captures.json. Godot Shaders returned HTTP 454 while rendering the actual homepage and gallery; the captured pixels were inspected. Do not claim an authenticated session or a successful HTTP 200 for that site.
- Godot and browser source captures were visually inspected on evidence/capture-contact-sheet.jpg; the final cube camera framing was enlarged afterward and inspected separately.
- evidence/sha256.json identifies the source and capture files. Regenerate it after any evidence change.

## Asset rights and provenance
The shader code, test harness, checker texture and conceptual drawings were authored for this lesson. Public documentation and homepage captures are short contextual teaching references, not republication of full articles or redistribution of community shader code. No community shader was downloaded or incorporated. The Professor Bear opening portrait comes from the approved local library, selected by slug seed: professor-bear-1x1-93.png. No paid generation, cloned third-party voice, or stock imagery is used. Liam uses the skill's local Kokoro am_onyx voice in stage two.

## Corrections to the supplied material
- A fragment is a candidate contribution, not invariably a one-to-one final pixel. No promised invocation order or absolute ban on reading stored texture data.
- Vertex displacement changes rendering, not scene transforms or collision geometry.
- TIME is an engine clock, not an elapsed-damage timer; no claim that it increases forever without rollover or ignores time scale.
- Alpha transparency alone is not a glass material or refraction.
- Matrix constructor vectors are columns. mat2(vec2(1,2),vec2(3,4)) has rows (1,3) and (2,4).
- vec2 c.xx is valid; assigning three components into vec2 is not. Do not mix .x and .r naming families in one swizzle.
- Separate ShaderMaterials can share one Shader. Copying the shader code is unnecessary for independent values.
- hint_range is an Inspector hint, not runtime clamping. The executed harness stores 7.0.
- Current checked stable documentation permits per-instance uniforms in canvas_item and spatial; avoid promising the feature for every old Godot release.
- Explicit breaks are retained in every terminating switch case in the tested examples. Fallthrough is demonstrated deliberately, without crashing anything.
- Loops are supported; termination and bounded work are required. No infinite loop is executed.
- Five shader types named in the user notes are examples, not an exhaustive current count.
- Compute requires a RenderingDevice renderer; the Compatibility shader lab does not claim a compute test.
''')
facts=['# Fact check — Gate F','', 'Status: factual review and executed shader evidence complete. Film audio and rendered-frame gates remain stage-two work.','', '| # | Beat | Claim / teaching target | Verdict | Source | Fix / scope |','|---|---|---|---|---|---|']
for i,b in enumerate(rows,1):
 source='User transcript; '
 if b['lane']=='code' and (R/'godot/shaders'/f"{b['asset']}.gdshader").exists():source+='godot/shaders/'+b['asset']+'.gdshader; evidence/godot-run.log'
 elif b['lane']=='capture' and not b['asset'].startswith('docs-'):source+='captures/'+b['asset']+'.png; godot/lab.gd'
 elif b['lane']=='shell':source+='evidence/'+('negative-type.log' if b['asset']=='negative' else 'verification.txt')
 else:source+='[stable reference]('+links['canvas' if b['act']<2 else 'language']+')'
 if b['asset'].startswith('docs-'):source='User learning-path notes; ['+b['asset'][5:]+']('+links[b['asset'][5:]]+'); actual page capture'
 verdict='Verified'
 scope='Constructed teaching example; not a general performance claim.'
 if b['id']=='B09':scope='Conceptual rendering/physics distinction; not an executed collision simulation.'
 if b['id']=='B19':scope='Columns (1,2),(3,4); M·(1,0)=(1,2); local pixel encoding (0.25,0.5,0) passed.'
 if b['id']=='B23':source='godot/lab.gd; CHECK hint_range stores 7.0 in evidence/godot-run.log';scope='Inspector hints do not enforce runtime bounds.'
 if b['id']=='B26':scope='Tested canvas_item instance tint locally; spatial support cross-checked in stable reference.'
 if b['id']=='B35':scope='Only terminating for/while examples executed; no GPU-hang demonstration.'
 if b['id']=='B41':scope='Homepage inspected despite HTTP 454; no assertion of universal code compatibility or licensing.'
 if b['id']=='B43':scope='Documented alternative, not executed in the Compatibility lab.'
 facts.append(f"| {i} | {b['id']} | {b['topic']} | {verdict} | {source} | {scope} |")
facts+=['','No externally sourced benchmark numbers, frame-rate claims, historical quotations, or fabricated interface output. Syntax is corroborated primarily by the retained source and actual local rendering. BVDT only recaps previously established claims; BHTF is a proposed learner task, not a claim of a historical Claude session.']
(R/'FACTCHECK.md').write_text('\n'.join(facts)+'\n')
(R/'PROMPTS.md').write_text('''# Prompts
No image or video generation prompts. All visual evidence is captured from the local Godot lab or public references; concept animation is authored in scenes.py. No paid media requests and no missing pantry assets.

BHTF is the suggested learner prompt, exactly as narrated and stored in beat_sheet.json. It is not portrayed as a prompt submitted to Claude in this production session.
''')
(R/'CAPTURE.md').write_text(f'''# Capture protocol
Native engine: /Applications/Godot.app/Contents/MacOS/Godot
Version: 4.7.2.stable.official.ed1daf0bf
Renderer: Compatibility / OpenGL 4.1 Metal / Apple M4 Pro.

From books/:
```bash
/Applications/Godot.app/Contents/MacOS/Godot --path {R}/godot -- --capture > {R}/evidence/godot-run.log 2>&1
/Applications/Godot.app/Contents/MacOS/Godot --path {R}/godot --script res://negative.gd > {R}/evidence/negative-type.log 2>&1
python3 {R}/verify_evidence.py
```

This is a shader teaching harness. Scripted parameters and actual viewport readbacks, not human play or a real-time speed measurement. Local GPU rendering is used, not the headless dummy renderer. The test does not alter an existing student game. The fixed source and image hashes are in evidence/sha256.json.

Native editor capture: opened only this lab in Godot; selected preview.tscn, 2D, ColorRect, and its Material field; captured through cua. No editor preferences were changed. Browser screenshots and exact URL/status records are retained separately. Concept diagrams are labeled and are not engine screenshots.
''')
(R/'README.md').write_text('''# Godot Shading Language
CSYE 7270 Building Virtual Environments · Liam, in for Bear · @NikBearBrown

**Status: lecture authored and evidence checked; audio and final film are not rendered.**

- NARRATION.md: every spoken line.
- ACTS.md and SHOTLIST.md: coverage and visual decisions.
- beat_sheet.json and make_sheet.py: executable film plan.
- scenes.py: eleven authored Manim scenes; other beats use registered Remotion components.
- godot/: 20 working shader examples, a capture harness, and an editor preview scene.
- FACTCHECK.md, SOURCES.md, evidence/: review and reproducible results.
- BUILD-PROMPT.md: stage-two instructions for the 4K master.

## Try the tint effect
Open godot/project.godot in Godot. Open preview.tscn, select ColorRect, expand its ShaderMaterial and Shader Parameters. Change amount among 0, 0.5 and 1; tint changes the target color. The source is shaders/flash.gdshader. The program preserves incoming alpha. To exercise all examples and regenerate evidence, use CAPTURE.md. The default main scene is a scripted capture lab, not an interactive game.

The negative.gd test is deliberately invalid and separate from the main scene. It exists to demonstrate why diagnostics matter. No nonterminating shader is included.

## Learning links
'''+ '\n'.join(f'- [{k}]({v})' for k,v in links.items())+'\n')
(R/'CHECKS-REPORT.md').write_text(f'''# Preparation checks

58 beats: 46 body SHOW beats, 6 act-title CARD beats, 6 required opening/closing beats. No HOLD and no unresolved PUNT. Lane histogram: {dict(counts)}.

Teaching arc: framework B01 before the first example; worked examples B04–B07 and B36–B37; falsifiability B16 and B33; scaffolded task BHTF with two independent checks; mandated lecture bookends present; source/evidence references in FACTCHECK.md.

Evidence: 20 positive shader files rendered without SHADER ERROR; 24 pixel assertions pass. The invalid type test is rejected by the compiler. Real source captures were visually inspected. Source author/URL for the pasted transcript remains unspecified and is not invented.

Structural checks: literal scene classes resolve, registered Remotion patterns resolve, narration is present, BHTF command matches narration, no numbered-video metadata. Static scene checker results are in evidence/static-scene-checks.json. Local schema validation and source checks are recorded in evidence/package-validation.json.

Not yet run: TTS, word alignment, low-resolution film-scene stills, Gate B pixel layout, Gate V frame review, Gate T typography, sharpness, audio/listening review, final bookend verification and final-master duration/dimensions. Those cannot pass before rendering. No blank gate result is called a PASS.
''')
(R/'BUILD-LOG.md').write_text('''# Build log — 13 October 2026

Applied the local lecture skill, Liam / am_onyx, and the two-stage film rule from books/CLAUDE.md. Stage one stops after authored narration, scene code and captured evidence. Estimated narration: about 12 minutes; final duration follows measured audio, not the estimate. No TTS or film render started.

Read the complete supplied transcript. Coverage and the one prerequisite reorder are in ACTS.md. The course's existing unrelated files had modifications when this work began and were preserved. All new course work is inside this new reel. Captures were copied into the toolkit's per-reel public asset folder for Remotion; library searches added normal miss records to the toolkit.

Evidence: tested Godot 4.7.2 Compatibility on Apple M4 Pro. Initial switch examples failed with a default branch lacking an explicit break; retained that failed log, corrected the examples and reran. First negative test quit before forcing use of the material, so it produced no shader diagnostic; revised the negative harness to draw and await frames. The retained negative log now contains the real type error. No false success was used in narration.

The initial cube capture was too small for teaching. Enlarged the cube in the same actual render harness and recaptured. Source imagery is evidence, not a substitute for final film QA. The community site rendered content with status 454; preserved the status honestly.

Source corrections include column-major matrices, swizzle sizes, material versus shader ownership, hint versus runtime clamp, fragment versus final pixel, rendering versus physics, and transparent material versus glass.

No paid generation, publication, staging, Git commit or push. No human review signature created. Next: BUILD-PROMPT.md.
''')
print('Wrote coverage, shot list, fact check, sourcing, capture protocol and build records.')
