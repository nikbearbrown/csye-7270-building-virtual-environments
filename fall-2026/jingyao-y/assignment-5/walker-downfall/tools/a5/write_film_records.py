"""Write the film's source, shot and build records from its current beat sheet."""
from pathlib import Path
import hashlib
import json

ROOT=Path(__file__).resolve().parents[2]
REEL=ROOT/"youtube/claude-liam-downfall-a5-shaders-gamedev"
sheet=json.loads((REEL/"beat_sheet.json").read_text(encoding="utf-8"))
beats=sheet["beats"]
def write(name,text):(REEL/name).write_text(text.strip()+"\n",encoding="utf-8")
write("COMPONENTS.md","# A5 components\n\n"+"\n".join(f"- {b['beat_id']}: {b['shot'].get('remotion',{}).get('pattern','Real engine evidence')} — {b['shot']['show'][0]['event']}" for b in beats))
time=0;rows=[]
for b in beats:
    duration=b.get("actual_duration_s",b.get("estimated_duration_s",0))
    rows.append(f"| {b['beat_id']} | {time:.2f}–{time+duration:.2f} s | {b['shot']['show'][0]['event']} |")
    time+=duration
write("SHOTLIST.md","# Shot list\n\nMeasured narration is the clock. Source action is cut at normal speed. The exact conformed timeline is written by the compiler.\n\n| Beat | Approximate span | Visible sequence |\n|---|---|---|\n"+"\n".join(rows))
write("FACTCHECK.md", """# Fact check

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
""")
write("SOURCES.md", """# Film sources

All code excerpts come directly from the source files and line ranges in gamedev-evidence.json. The game is Godot 4.7.2, Forward+ / D3D12. Source hashes identify the measured snapshot; its development checkout includes pre-existing working-tree changes.

Engine images come from evidence/a5/use-it, hint-experiment and normal-map-check. Their measurement JSON files retain renderer/adapter/settings. Native gameplay frames are 3840×2160 at fixed 30 fps. The final B07 intervals are recorded in media-provenance.json; they are cut without speed changes. Game audio is muted beneath Kokoro narration. Still comparisons keep the actual rendered pixels; they are not redrawn as simulated game output.

Cargo textures: https://polyhaven.com/a/rusty_metal_sheet, CC0: https://polyhaven.com/license. Technical sources: Godot's stable shading-language, spatial-shader and Movie Maker documentation. Measured behavior is distinguished from documentation defaults.

The local Brutalist godot-gamedev and riff workflows provide the teaching structure and reusable scenes. Voice: local Kokoro am_onyx, Liam in for Bear, not a voice clone. The regular title/handle/mascot outro uses the toolkit's stock jingle. The opening prompt is a suggested demonstration prompt, not a historical transcript.
""")
write("RIFF.md", """# Evidence-led commentary

| Artifact | Visible observation | Interpretation / limit |
|---|---|---|
| Controlled fire images | Yellow → orange/red → unchanged background | Uniform controls appearance; Linear is required for this numeric comparison |
| Native city take | Bottle flight, new flames over Decals, slug warning/burst without a flame | Confirms the recorded cases, not every possible camera or encounter |
| Hint panels | Raw path is brighter | The missing sRGB decode changes the displayed values |
| Normal same-place comparisons | Corrected DX aligns with GL within 1/2 levels | A flat source limits the visible difference |
| Uniform sweep | Repetition density, tint and highlight response change | Large UV scale repeats conspicuously; strong roughness clips data variation |
| Shared program / A-only value | Both panels change, then only A changes | Program resource and material overrides have separate ownership |
| Generated shader BoxMesh | Textured, lit surface renders | Saving code alone does not save material bindings |

Next experiment: alter one parameter, write a prediction first, and compare one controlled region before accepting it. No claim about fun or accessibility follows from these captures.
""")
write("PROMPTS.md", "# Prompts\n\nThe opening prompt is a suggested demonstration prompt. The Your Turn prompt is a bounded viewer exercise.\n\n"+"\n\n".join(b["shot"]["remotion"]["props"]["command"] for b in beats if b["shot"].get("remotion",{}).get("pattern")=="ClaudeComposerAsk"))
write("BUILD-PROMPT.md", """# Rebuild the A5 film

Use the delivered A5 project and the local Brutalist toolkit. Preserve existing films and source. Set PYTHONUTF8=1 and use the interpreter with kokoro-onnx installed. Never publish.

1. Review TEST-REPORT and the measurement JSON files. Recheck shader hashes and code line ranges.
2. Run tools/a5/build_film.py author only for a new build; it resets the authored sheet. Do not overwrite an already measured sheet accidentally.
3. Generate audio with runtime/scripts/generate_audio_kokoro.py REEL. Use the existing am_onyx voice. Run tools/a5/attach_outro.py to bind the shipped channel jingle and its full duration; never synthesize over it.
4. Run tools/a5/make_film_media.py against the retained captures. Re-record native 4K gameplay if missing. Do not upscale recorded gameplay or retime actions.
5. Render a pilot using runtime/scripts/remotion_scenes.py REEL --only B04, inspect it, then render remaining established scenes with that wrapper.
6. Write records with tools/a5/write_film_records.py, then tools/a5/build_film.py ledger. Run art godot-gamedev --check REEL --game PROJECT.
7. Run art final REEL --height 2160 --fps 30 --out REEL/exports/landscape. Retain normal audio, paperwork, frame and source gates.
8. Inspect the actual master at 2 fps plus each beat near 15/50/85 percent, including source at reading size, motion order, audio and the silent regular outro. Record defects and fixes in _qc/REPORT.md. Do not call a probe alone visual QC.
9. Refresh the source inventory after final artifacts are created and rerun the game-development checker. Verify the exported file's SHA-256 against its receipt. Keep the previous films and failed-attempt records.
""")
write("CHECKS-REPORT.md", """# Teaching checks

23 SHOW beats, zero unresolved PUNTs. Framework: shader/state separation before examples. Worked example: required color statement and measured pixels. Falsifiability: mutations, out-of-range value, raw color path and regression failures. Scaffolded task: one parameter, one prediction, one check. Bookends: composer → hesitant overview → body → verdict → Your Turn → locked title outro. Every code excerpt is immediately followed by its actual engine result.

The negative space on the two-line color excerpt emphasizes the exact statement; it uses enlarged type after the pilot review. Stills are evidence comparisons; gameplay action uses the native take at its original simulation speed.
""")
write("BUILD-LOG.md", """# Build log

The first code pilot was inspected and the short color/driver excerpts were enlarged for reading. An initial system capture was flat; DXGI with a correctly sized borderless client recovered matching samples. Desktop window dimensions clamp below 4K, so native gameplay was rendered in a 3840×2160 SubViewport rather than upscaling the window capture. The first PNG take was stopped for slow encoding and replaced with quality-97 JPEG frames; numeric calibration remains lossless PNG. Source code and final clip hashes are retained separately.

The toolkit documentation refers to scripts/type_check.py and a kerning skill, but neither exists in this installed toolkit. The available final-export gates remain enabled. Actual frame inspection and the recorded type review are required; a missing checker is not reported as an automated pass. No human approval signatures are fabricated.
""")
print("Wrote film records")
