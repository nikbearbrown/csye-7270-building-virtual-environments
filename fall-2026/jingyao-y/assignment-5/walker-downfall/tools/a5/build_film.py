"""Author the A5 film from exact shader excerpts and measured engine evidence."""
from pathlib import Path
import json
import argparse
import hashlib
import math
import subprocess
from film_layout import apply_layout
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
REEL = ROOT / "youtube/claude-liam-downfall-a5-shaders-gamedev"
TITLE = "Downfall: Fire, Texture and Shader Evidence"
EVIDENCE = ROOT / "evidence/a5/use-it"
EXCERPTS = {"B02": ("shaders/burning_bottle_fire.gdshader", 1, 6),
            "B04": ("shaders/burning_bottle_fire.gdshader", 17, 18),
            "B06": ("entities/fire_flame.gd", 40, 43),
            "B08": ("shaders/hint_experiment.gdshader", 4, 9),
            "B10": ("shaders/cargo_panel.gdshader", 3, 5),
            "B12": ("shaders/cargo_panel.gdshader", 16, 21),
            "B14": ("materials/cargo_panel_mild.tres", 10, 17),
            "B16": ("shaders/standard_generated.gdshader", 41, 47)}

def graphic(pattern, props, event):
    return {"type": "GRAPHIC", "class": "SHOW", "source": "remotion", "motion": "reveal",
            "show": [{"at": "0", "event": event}], "remotion": {"pattern": pattern, "props": props}}

def code(bid, title, notes):
    path, start, end = EXCERPTS[bid]
    text = "\n".join((ROOT/path).read_text(encoding="utf-8").splitlines()[start-1:end])
    return graphic("GodotDevWorkbench", {"mode": "code", "title": title, "project": "downfall-godot",
        "path": "res://" + path, "source": f"{path}:{start}-{end}", "code": text, "startLine": start,
        "codeFontSize": 40 if bid in ("B04", "B06") else 25, "notes": [{"label": a, "value": b} for a, b in notes],
        "cues": [{"at": 1.0, "line": start, "label": title}, {"at": 6.0, "line": end, "label": notes[-1][1]}]},
        f"Read source lines {start}-{end}, then follow their consequence in the next beat")

def media(bid, event, motion=False):
    return {"type": "GAMEPLAY" if motion else "GRAPHIC", "class": "SHOW", "source": "capture" if motion else "image",
            "evidence_media": f"media/{bid}.mp4", "show": [{"at": "0", "event": event}]}

def author():
    REEL.mkdir(parents=True, exist_ok=True)
    beats = []
    def add(bid, narration, shot, **kw):
        beats.append({"beat_id":bid, "act": "BODY", "narration_text": narration, "voice":"am_onyx", "engine":"kokoro",
                      "estimated_duration_s":max(10, len(narration.split())/2.4), "shot":shot, **kw})
    add("B00", "Hello. Liam, in for Bear. This is Downfall's shader assignment: a burning bottle driven by game state, a rusty cargo panel lit by the scene, and experiments that check what their pixels actually mean. The useful question is whether the rendered result follows the prediction.",
        graphic("ClaudeComposerAsk", {"greeting":"Hej, Liam", "topic":"GODOT GAMEDEV · ASSIGNMENT 5", "segment":"Fire, Texture and Evidence", "command":"Please use Walker to convert my game design document about Downfall's burning bottles and cargo panels into a shader demonstration with predictions, real engine results and failure checks.", "runningText":"following the shader evidence…", "folderLabel":"@NikBearBrown", "modelLabel":"Claude", "output":["Fire and texture shaders", "Controlled values and rendered results", "Failures kept alongside passes"]}, "Composer opens on the A5 demonstration prompt"), act="ASK")
    add("B01", "A shader changes appearance. The game owns the state. The pixels follow rules. Measure the result. Three small programs make those rules visible in Downfall, and controlled comparisons check that they hold.", graphic("BrutalistHesitantWriter", {"text":"A shader changes gameplay.\nThe game owns the state.\nThe pixels follow rules.\nMeasure the result.","triggerWords":"gameplay", "replacementWords":"appearance", "seed":"downfall-a5-20261030", "fontSize":140, "lineSpacing":1.35, "charMs":36, "mistakeRate":0, "hesitateWithin":0,"hesitateBetween":0}, "The writer changes gameplay to appearance"), lead_silence_s=0.8)
    add("B02", "Start with the kind of program. Spatial means a three-dimensional surface, with Godot's surface outputs available in fragment. Unshaded makes this fire independent of scene lights. Forward Plus and Direct Three D twelve are the renderer and driver, separate choices. Albedo would default to white; vertex COLOR is not an automatically sampled color texture.", code("B02", "A Surface Program", [("Shader type", "spatial: a 3D surface"),("Fire response", "unshaded + additive blend")]))
    add("B03", "Here is the resulting flame over the city. This is an appearance layer over the existing hazard. The background remains visible through the additive shape. Writing an explicit fire color gives this yellow center; simply forwarding a plain quad's white vertex color would not produce the same result. This controlled view uses Linear tone mapping.", media("B03", "The real city and the controlled r=1 flame"))
    add("B04", "This is the required color statement, unchanged. Remaining fire mixes red embers toward yellow heat and multiplies by intensity. Alpha is a separate decision: the shape and remaining fraction determine coverage. Fragment evaluates that shape across the surface. Moving its nonlinear shape calculation to four corner vertices would change the interpolated outline.", code("B04", "Color And Coverage", [("Color", "mix red → yellow, then × 0.6"),("Coverage", "shape × remaining, explicitly clamped")]))
    add("B05", "Now compare the three controlled values. At the center, full fire measures two ten, two ten, sixty seven. Half fire is one fifty eight, one twenty one, sixty seven. Zero returns the original background. Those are the values predicted before capture. Setting two produces a green channel of two fifty five: the Inspector range did not clamp the program's input.", media("B05", "r=1, 0.5, 0 and 2 appear in order with their measured center samples"))
    add("B06", "The CPU connection is four lines. After the hazard updates, this driver checks whether simulation is active, divides remaining duration by the cached initial duration, clamps the ratio, and writes the material parameter. It has no second damage timer. Every fire owns a material, while all of those materials share the same Shader resource.", code("B06", "State Enters Through A Uniform", [("Input", "lasting / initial_lasting"),("Pause", "Skip the uniform update")]))
    add("B07", "Watch the bottle land, then the flame appear above its ground mark. The thrower keeps making new fires instead of restarting one shared color. During the pause, the lifetime value holds while the visual flicker can continue. Nine fires were recorded in this run. The explosive slug keeps a warning and burst; it does not acquire a flame mesh.", media("B07", "Bottle flight, repeated fires and their unchanged ground Decals", True))
    add("B08", "A texture hint can change the numbers. These two samplers read exactly the same three pixels. The first declares source color and the other reads raw data. Both use nearest filtering and disable repetition, so texture filtering cannot explain the difference. The Boolean switches between the two paths without adding a correction factor.", code("B08", "One Texture, Two Interpretations", [("Color path", "source_color: decode sRGB"),("Data path", "No source_color")]))
    add("B09", "The top row returns sixty four, one twenty eight, and one ninety two. The lower row is visibly brighter: one thirty seven, one eighty eight, and two twenty five. The original prediction matches every center sample exactly. Missing the first decode leaves the raw values to be encoded again for display. This is why an albedo hint belongs on the sampler.", media("B09", "The six real hint-experiment samples and the upper/lower gray panels"))
    add("B10", "Cargo needs three different kinds of texture. Albedo is color. Roughness is scalar data. The normal map is encoded direction data. Only albedo gets source color. All three repeat and use the same filtering. The normal sample goes through Godot's normal-map path, rather than being decoded as a color or assigned directly to NORMAL.", code("B10", "Color And Data Stay Separate", [("albedo", "sRGB color"),("roughness / normal", "Data; no source_color")]))
    add("B11", "The normal comparison uses the same light and the same panel position. Raw Direct X reverses the green direction. Flipping its Y import setting makes it agree with the Open G L version within two display levels. The source map is very flat, so the visual difference is subtle. Raking light reveals it more clearly than the review light.", media("B11", "GL, raw DX and Y-corrected DX under review and raking light"))
    add("B12", "Here the surface stays lit. One scaled UV feeds all three textures, so a rust patch and its normal detail keep the same size. Roughness is clamped after scaling because the control reaches two. Normal strength goes to NORMAL MAP DEPTH. The shader writes no alpha and no metallic value, keeping the panel opaque and nonmetallic.", code("B12", "Four Controls, One UV", [("Surface", "UV scale + tint"),("Response", "Roughness + normal strength")]))
    add("B13", "The scan makes the trade-offs visible. Small UV scale magnifies a small part of the sheet; eight repeats make the rust look much finer. Black tint hides most diffuse detail. Roughness two clips much of this map to fully rough. Normal strength two changes the raking light slightly, but cannot invent large dents that are absent from the texture.", media("B13", "Minimum, default and maximum settings across the four cargo controls"))
    add("B14", "These values live on a material instance. The Shader holds declarations and defaults; a ShaderMaterial holds the current overrides and texture bindings. Two boxes can therefore use one program with different responses. Sharing the material itself would share the override too. The experiment changes the common program first, then changes only the first material's tint.", code("B14", "The Material Holds The Overrides", [("A", "roughness 0.65 / normal 0.35"),("B", "roughness 1.35 / normal 1.2")]))
    add("B15", "First both panels respond when the shared shader's color statement changes. After restoring it, changing only A's tint alters the left panel; the right panel stays identical. This separates program sharing from value sharing. The actual base uses those two independent materials on crate stacks. Under its A C E S lighting, the weathered stack is darker.", media("B15", "Baseline → common shader edit → restored → A-only parameter edit → actual base"))
    add("B16", "Godot's generated version reaches the same surface outputs with more general controls. It chooses a roughness channel, scales the sample, then assigns the normal texture and its depth. Its color sampler also declares source color, and its normal sampler does not. Saving the Shader alone does not save the converted material's texture bindings and current values.", code("B16", "Compare The Generated Program", [("Generated shader", "48 lines; separate comparison resource"),("Runtime", "Not referenced by game materials")]))
    add("B17", "This BoxMesh is rendered with that generated program and the three bound textures. It parses and draws, but it is kept out of the game. The hand-written cargo program has fewer controls because it solves a narrower job. The comparison also shows why a generated declaration is not a complete material: the textures and parameter overrides still have to be supplied.", media("B17", "The generated shader's actual BoxMesh rendering"))
    add("B18", "Frame counting would be a different timer. One hundred eighty rendered frames last six seconds at thirty frames per second, three at sixty, and one point two five at one forty four. This driver reads the existing physics state instead. Its measured endpoint is one hundred eighty one physics steps, the same at all three render rates.", graphic("ExecutedData", {"title":"180 Rendered Frames", "mode":"table", "columnLabels":["Frames / second", "Lifetime / seconds"], "rows":[{"label":"30","value":6,"at":1},{"label":"60","value":3,"at":4},{"label":"144","value":1.25,"at":7}], "note":"Actual hazard: 181 physics steps / 3.016667 game seconds"}, "Rows appear as each frame-rate lifetime is explained"))
    add("B19", "Time has its own check. Over one hundred twenty frames at fixed sixty, shader TIME advances two seconds at normal speed, one at half speed, four at double speed, and zero with time scale zero. A normal game menu pauses this hazard through simulation active; it does not set engine time scale to zero. That is why flicker can continue while lifetime color holds.", graphic("ExecutedData", {"title":"Shader TIME Follows Time Scale", "mode":"table", "columnLabels":["time_scale", "TIME advance / seconds"], "rows":[{"label":"1","value":2,"at":1},{"label":"0.5","value":1,"at":4},{"label":"2","value":4,"at":7},{"label":"0","value":0,"at":10}], "note":"120 frames at fixed 60 fps; values decoded from rendered pixels"}, "The four measured time increments appear in narration order"))
    add("B20", "The useful result is a small, testable connection from state to appearance. The fire predictions match. The texture hints change the expected pixels. Separate materials keep separate values. Limits remain visible: the normal texture is subtle, the system capture needed a different Windows path, and the old regression failures remain in the report. Those limits belong beside the successful checks.", graphic("ClaudeVerdictArtifact", {"artifactTitle":"A5 Verdict", "artifactHeading":"What The Evidence Supports", "brandLabel":"@NikBearBrown", "artifactLines":["Fire pixel predictions match.","Texture color hints change sampled values.","One Shader supports independent materials.","Flat normal map and old regression failures remain."]}, "The verdict separates measured results and limitations"), act="VERDICT")
    prompt = "Use Walker to change one shader parameter in my game. Predict one pixel or visible change, keep the game state unchanged, and test the prediction before accepting the result."
    add("B21", prompt + " Start with one controlled change, so a failure has somewhere specific to point. Compare the program, the material value, and the final pixel before changing your prediction. Liam, in for Bear.", graphic("ClaudeComposerAsk", {"greeting":"Your turn.","topic":"ONE CHANGE · ONE PREDICTION", "segment":"Make The Result Testable", "command":prompt, "runningText":"paste this into Claude…", "folderLabel":"@NikBearBrown", "modelLabel":"Claude", "output":["Choose one parameter.","Write the prediction first.","Keep the observed failure if it fails."]}, "The viewer's bounded experiment is typed and read aloud"), act="HANDOFF")
    add("B22", "", graphic("ClaudeTitleOutro", {"title":TITLE,"slug":REEL.name}, "Exact title, regular mascot and stock jingle"), act="OUTRO", audio_policy="silence", actual_duration_s=7.0)
    sheet={"metadata":{"title":TITLE,"slug":REEL.name,"topic":"GODOT GAMEDEV · A5 SHADERS", "kind":"godot-gamedev", "mode":"walker","brand":"claude-liam", "engine":"kokoro", "voice":"am_onyx","voice_kokoro":"am_onyx", "palette":"claude","aspect_ratio":"16:9","captions":False,"channel":"@NikBearBrown","folderLabel":"@NikBearBrown","game":{"name":"downfall-godot","engine_version":"Godot 4.7.2","revision":"A5 source hashes in gamedev-evidence.json"}},"beats":beats}
    apply_layout(sheet)
    (REEL/"beat_sheet.json").write_text(json.dumps(sheet,indent=2)+"\n",encoding="utf-8")
    print(REEL)

def source_ledger():
    sheet=json.loads((REEL/"beat_sheet.json").read_text(encoding="utf-8"))
    excerpts=[]; files=[];components=[];pairs=[]
    for bid,(path,start,end) in EXCERPTS.items():
        text="\n".join((ROOT/path).read_text(encoding="utf-8").splitlines()[start-1:end])
        excerpts.append({"beat_id":bid,"path":path,"start_line":start,"end_line":end,"text":text})
        cid=bid.lower();components.append({"id":cid,"explanation":next(b["narration_text"] for b in sheet["beats"] if b["beat_id"]==bid),"beat_ids":[bid,f"B{int(bid[1:])+1:02}"],"files":[path]})
        f=next((f for f in files if f["path"]==path),None)
        if f:f["component_ids"].append(cid)
        else:files.append({"path":path,"sha256":hashlib.sha256((ROOT/path).read_bytes()).hexdigest(),"role":"A5 source explained on screen","component_ids":[cid]})
        result=f"B{int(bid[1:])+1:02}";clip=REEL/f"media/{result}.mp4"
        pairs.append({"code_beat":bid,"result_beat":result,"observation":next(b["narration_text"] for b in sheet["beats"] if b["beat_id"]==result),"media":{"path":f"media/{result}.mp4","sha256":hashlib.sha256(clip.read_bytes()).hexdigest()}})
    def attach(path,cid,role):
        component=next(c for c in components if c["id"]==cid)
        if path not in component["files"]:component["files"].append(path)
        record=next((f for f in files if f["path"]==path),None)
        if record:
            if cid not in record["component_ids"]:record["component_ids"].append(cid)
        else:files.append({"path":path,"sha256":hashlib.sha256((ROOT/path).read_bytes()).hexdigest(),"role":role,"component_ids":[cid]})
    associations={
        "b02":["project.godot","evidence/a5/use-it/measurement.json"],
        "b04":["evidence/a5/use-it/measurement.json"],
        "b06":["entities/ground_hazard.gd","entities/molotov.gd","tests/test_fire_shader.gd","evidence/a5/use-it/gameplay.json","evidence/a5/use-it/menu-input.json"],
        "b08":["tests/hint_experiment.tscn","textures/hint_experiment/greys_3x1.png","textures/hint_experiment/greys_3x1.png.import","tests/a5_capture_hint.gd","evidence/a5/hint-experiment/four-runs.json"],
        "b10":["tests/normal_map_check.tscn","tests/normal_map_check.gd","evidence/a5/normal-map-check/measurement.json","textures/cargo_panel/ATTRIBUTION.md"],
        "b12":["tests/material_review.tscn","tests/test_materials.gd"],
        "b14":["materials/cargo_panel_weathered.tres","world/base_map.gd","evidence/a5/use-it/shared-shader.json"],
        "b16":["evidence/a5/step4/generation.json","evidence/a5/step4/validation.json"]}
    for cid,paths in associations.items():
        for path in paths:attach(path,cid,"A5 input, existing integration, fixture or measured receipt explained by this component")
    for cid,bids,paths in [("timing",["B18","B19"],["tools/a5/capture_use_it.gd","tests/test_fire_shader.gd","evidence/a5/use-it/measurement.json"]),("checks",["B20"],["evidence/a5/final-regression/summary.json","evidence/a5/performance-rerun/summary.json","TEST-REPORT.md"])]:
        components.append({"id":cid,"explanation":"Measured A5 timing and verification, including the limits stated in the film.","beat_ids":bids,"files":[]})
        for path in paths:attach(path,cid,"Measured evidence or its executed verification source")
    included={f["path"] for f in files}
    exclusions=[{"path":p.relative_to(ROOT).as_posix(),"reason":"Outside the A5 shader component scope: preserved game, prior assignment, authoring asset or generated evidence/media."} for p in ROOT.rglob("*") if p.is_file() and not any(x in (".godot",".git") for x in p.relative_to(ROOT).parts) and p.suffix!=".uid" and p.relative_to(ROOT).as_posix() not in included]
    # The ledger lists itself as excluded; otherwise its own hash would be recursive.
    path="youtube/"+REEL.name+"/gamedev-evidence.json"
    if not any(e["path"]==path for e in exclusions):exclusions.append({"path":path,"reason":"This source inventory; self-hash would be recursive."})
    (REEL/"gamedev-evidence.json").write_text(json.dumps({"schema_version":1,"teaching_contract":"code-then-result-v1","files":files,"components":components,"excerpts":excerpts,"exclusions":exclusions,"code_result_pairs":pairs},indent=2)+"\n",encoding="utf-8")

if __name__=="__main__":
    parser=argparse.ArgumentParser();parser.add_argument("mode",choices=["author","ledger"]);args=parser.parse_args()
    author() if args.mode=="author" else source_ledger()
