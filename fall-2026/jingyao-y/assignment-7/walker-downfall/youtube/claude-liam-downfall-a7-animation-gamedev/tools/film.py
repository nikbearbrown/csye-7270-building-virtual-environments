"""Author the A7 animation film (beat sheet + source ledger) from exact excerpts.

    python tools/film.py author   # writes beat_sheet.json (resets measured fields!)
    python tools/film.py ledger   # writes gamedev-evidence.json (after media exist)

Every code excerpt is read from the game folder at the given line range; the
checker (art godot-gamedev --check) compares it with the file again.
"""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess

REEL = Path(__file__).resolve().parents[1]
GAME = REEL.parents[1]
TITLE = "Downfall: A Breath, A Sword Wave and Frames"
NOTE = "Source notes — not Inspector values"

# beat -> (path, start, end, title, notes, font)
EXCERPTS = {
    "B03": ("animations/npc_idle.tscn", 7, 20, "Q1 · A Clip Is A List Of Keys",
            [("Track", ".:frame on the Sprite3D itself"), ("Keys", "t 0, 1/3, 2/3, 1 s → cells 0, 1, 2, 3\nupdate 1 = discrete · loop_mode 1 = LOOP_LINEAR")], 22),
    "B05": ("animations/npc_idle.tscn", 28, 36, "The Sheet Is A Grid Of Numbers",
            [("Slicing", "hframes 4 × vframes 1 (default)\n256×64 sheet → four 64×64 cells"), ("Read-back", "every key < hframes·vframes = 4")], 34),
    "B07": ("tests/a7_readback.gd", 36, 38, "A Missing Property Fails Silently",
            [("Branch", "ordinary track: is the subname a member?"), ("Limit", "true for a method too: proves the track\npoints at something real, not the right thing")], 32),
    "B09": ("world/continuous_world_map.gd", 2719, 2729, "Q2 · One Authority: Seek, Don't Write",
            [("Before", "figure.frame = rng… (a second writer)"), ("After", "the same draw, one seek of the figure's\nown clip; its AnimationPlayer owns frame")], 25),
    "B11": ("entities/player.gd", 362, 376, "The State Machine Owns The Rig",
            [("Writes", "Billboard.visible, Rig.scale.x, the sprite's\nvisible — never keyed by any clip"), ("Calls", "play, seek on the rig's AnimationPlayer")], 21),
    "B13": ("entities/player.gd", 380, 388, "Q3 · Two Clocks, One Tick",
            [("Clock", "callback_mode_process = MANUAL\nadvance(delta × r) on the physics tick"), ("Gameplay", "frame 6 read from wave_frame,\nnever from the clip")], 28),
    "B15": ("animations/lappland_wave_rig.tscn", 108, 116, "Q4 · Feel Is Designed In Frames",
            [("Phase table", "startup 6 · active 4 · recovery 10\nat 30 fps, step 1/30"), ("Keys", "frames 0, 6, 10, 20 → 0, 0.2, 0.333, 0.667 s")], 28),
    "B17": ("entities/player.gd", 318, 331, "The State Table In Code",
            [("States", "READY · STARTUP · ACTIVE · RECOVERY"), ("Interrupts", "dodge / loss of control → READY\na swing in RECOVERY cuts it")], 22),
    "B19": ("tests/test_wave_edges.gd", 198, 203, "Edges: One Frame Before, On, After",
            [("Cases", "f5/6/7 · f9/10/11 · f19/20/21 at r = 1"), ("Rule", "before f6: no wave, charge kept\nfrom f6: the wave is out")], 22),
}

N = {}  # narration
N["B00"] = "Jambo. This is Liam, in for Bear. Today it's Downfall, the walker-downfall Godot game, and its Assignment Seven animation work: a breathing loop on every non-player character, made from a sprite sheet, and Lappland's sword wave release, a cutout rig that winds up, sweeps and recovers. We read each clip, then watch what it does."
N["B01"] = "A clip is a list of keys, not a movie. Each track names a node and a property, and holds times and values. Exactly one thing writes to each animated node. And feel is designed in frames, then judged by a person watching it run."
N["B02"] = "Two clips. The loop is npc idle: a Sprite three D sliced four by one, with an Animation Player frame track at twelve frames a second. The committing action is wave release: a two D cutout rig of Lappland, drawn through a SubViewport onto a billboard, keyed at thirty frames a second. Each clip's Animation Player is the one writer of its parts, and the player's state machine drives the rig."
N["B03"] = "Here is the whole loop, as resource text. One value track, path dot colon frame, on the sprite itself. Four keys, at zero, a third, two thirds and one second, with values zero, one, two and three. Update one is discrete, so the frame jumps instead of sweeping. Loop mode one is loop linear, and the length is sixteen twelfths of a second."
N["B04"] = "This is Closure at the base store, in the running game, through a preview fixture that only places the player for framing. Each cell holds for a third of a second, ten capture frames. The last key sits one interval before the end, so the wrap from cell three back to zero takes exactly as long as every other step. The user watched it in the game and said: All fine."
N["B05"] = "Which picture is frame three? That isn't the image's business. The sprite's texture is the sheet, and h frames four, with one row, cuts it into four cells of sixty four pixels. The slicing decides which cell frame three names. The read-back test checks every key against h frames times v frames: nothing above three."
N["B06"] = "Here is the actual sheet with its four cells numbered, and four capture frames, one per key. The picture in each frame is the cell the track named. Nothing in the clip knows it's Closure: the same clip, with another texture, breathes for the squad and the trader."
N["B07"] = "So what if a track names a property that doesn't exist? Godot plays the clip anyway. A track that points at nothing sets nothing, with no error. That's why the read-back resolves every track. For an ordinary track, this line asks whether the node has the named member. Bone and blend shape tracks branch off before it."
N["B08"] = "Mutation one, in its own worktree, from an empty cache: the rig's arm rotation track renamed to rotaton, in the clip only. The read-back exits one, and the line says why: wave release track four, ArmFront has no property rotaton. In the game, that arm would just stop moving. Loop mode flipped to none, and a key set to cell four: also exit one."
N["B09"] = "One authority. Before this change, the field set pieces wrote each figure's frame directly, so the squad wouldn't breathe in step. That was a second writer on a node the Animation Player now owns. The same random draw is kept, but it becomes one seek of the figure's own clip, once it's in the tree. The Animation Player stays the only thing that writes frame."
N["B10"] = "The field squad, in the same fixture run. The structure test read the three figures at a third, a third and two thirds of a second: not all in step. If two things wrote one sprite, whichever ran last in the frame would win, and that depends on node order, not on any design."
N["B11"] = "On the player, the release click starts the rig. The wave state machine writes the billboard's visibility and the rig root's facing, and it is the operator sprite's only visibility writer too, the same place that already hid it for Amiya's shadow skill. No clip keys those properties, so nothing fights it."
N["B12"] = "In the user's strip, frame twenty seven, the click, is still the sprite. On twenty nine, the rig has replaced it, and on fifty the sprite is back. The film's scripted run logs the same swap: sprite hidden while the state is startup, active or recovery, shown again in ready."
N["B13"] = "Two clocks. An Animation Player can advance on the process tick or the physics tick. Gameplay reads the active window on the physics tick, so this rig runs in manual mode. Each physics tick that isn't frozen by hitstop, the same delta, times the attack speed rate, advances both the state machine's time and the clip. Frame six fires the wave from the state machine's own count, never from the clip."
N["B14"] = "The structure test, through real input, records every tick. At rate one, active opens after twelve unfrozen ticks, recovery after twenty, ready after forty, and four hitstop ticks freeze both clocks together. At rate one and a half: eight, fourteen and twenty seven. Every tick, clip position equals the state machine's time, within a ten thousandth of a second. The NPC loop runs on the process tick, and nothing reads it."
N["B15"] = "Feel is designed in frames. The phase table says six startup frames, four active, ten recovery, at thirty frames a second, with a step of one thirtieth. So the arm's keys sit at zero, point two, a third, and two thirds of a second: frames zero, six, ten and twenty. Transition two eases into the sweep, and point five eases out through recovery."
N["B16"] = "Here's the rig alone, in a fixture with nothing but a grey floor, stepped one thirtieth of a second per frame. The blades wind back through startup, swing through the active frames, and settle by frame twenty. The parts are cut unchanged from Lappland's combat sheet. Only their pivots move."
N["B17"] = "The state table in code: four states, the clip each one plays, and three transitions, at frames six, ten and twenty. A dodge or loss of control in any state goes back to ready, and a swing in recovery cuts it short. The structure test checks this table against the brief, and against the rig's own animation library."
N["B18"] = "The user's Movie Maker capture, read at each boundary. Frame twenty nine is the first startup frame, two of them hitstop. Thirty six is the last startup frame. On thirty seven, the charge mark is gone, and the wave leaves. Forty one starts recovery, and on fifty the sprite is back. The user's verdict: I saw the record, everything is nice, we did a good job. Then: keep r zero, no revision."
N["B19"] = "The edges. For each boundary, a real dodge arrives one frame before it, on it, and one frame after. Before frame six: no wave, and the charge is kept. On or after six, the wave is already out. The test asserts exactly that: nine cases, thirty nine checks."
N["B20"] = "A scripted input capture of the same rule in the running game: a real click, then a real dodge event, timed by reading the state. First, a full release. Then a dodge in startup: no wave, and the charge is kept. A dodge on the first active frame: the wave is already out. A dodge in recovery cuts the settle. Between takes, a ground click walks her back, and the charge is refilled as a fixture."
N["B21"] = "What the tests proved. Read-backs: fifty five checks on the loop, a hundred thirty six on the rig. The pins: sixteen before the change, five failing exactly where the brief predicted, then re-pinned one suite per commit. Structure, fifty one. Edges, thirty nine. All four mutations behaved: three exit one, and a fresh cache passes. The whole suite: ninety three of a hundred and three before, ninety nine of a hundred and eight after. None of it draws a single frame."
N["B22"] = "What only a person could check, and who did what. The user judged the seam, the action in play with interrupts in combat, while searching and standing still, and the contrast on light and dark ground. Claude wrote the brief, every prediction, the reviews and the records. Delegated agent sessions built the clips, the state machine and the tests. The art is fan art made with gpt sol six point one, and its terms were not supplied."
N["B23"] = "The verdict. Both clips are resources, every track resolves, one writer owns each animated node, and the wave leaves on the same physics tick that advances the clip. Mistakes caught: the planning session found test changes the brief had missed, including a pin the agent failed to mark, and the rig session found the brief's wrong sheet grid. Claude's strip reading flagged an early hit flash and a possible facing problem. The user kept r zero, so there is no observation driven revision. Still untested: death, stuns and leaving mid release. Next step: give the startup a readable wind up, prediction first."
PROMPT = "Use Walker to change one number in my phase table. Predict what the frame strip will show at each boundary, rebuild the keys from the table, capture before and after, and let me give the verdict in the running game."
N["B24"] = PROMPT + " Change the table, not the keys, and let the change flow down. Liam, in for Bear."

RESULTS = {  # result beat -> visible sequence
    "B04": "FIXTURE preview, real game: Closure breathing at the base store, one cell per 10 capture frames",
    "B06": "The actual NPC sheet with its four cells numbered, beside capture frames one per key",
    "B08": "Mutation m1/m2/m3/m4 recorded output, verbatim from logs/a7_mutations/",
    "B10": "FIXTURE preview, real game: the field squad breathing out of step; structure-test phase line",
    "B12": "The user's r0 frames 28/29 and 49/50 (sprite ↔ rig) with the scripted run's state log",
    "B14": "Recorded output: the structure test's per-tick clock lines at r = 1 and r = 1.5",
    "B16": "FIXTURE capture: the rig alone, one design frame per capture frame, frames 0–20",
    "B18": "The user's r0 strip at each phase boundary beside the phase table",
    "B20": "Scripted-input capture: full release, then a real dodge in startup, active and recovery",
}
MOTION = {"B04", "B10", "B16", "B20"}
ORDER = [f"B{i:02}" for i in range(26)]
ID = {k: k for k in ORDER}


def excerpt(bid):
    path, start, end = EXCERPTS[bid][:3]
    return "\n".join((GAME / path).read_text(encoding="utf-8").splitlines()[start - 1:end])


def graphic(pattern, props, event):
    return {"type": "GRAPHIC", "class": "SHOW", "source": "remotion", "motion": "reveal",
            "show": [{"at": "0", "event": event}], "remotion": {"pattern": pattern, "props": props}}


def code(bid):
    path, start, end, title, notes, font = EXCERPTS[bid]
    return graphic("GodotDevWorkbench", {
        "mode": "code", "title": title, "project": "downfall-godot", "path": "res://" + path,
        "source": f"{path}:{start}-{end}", "code": excerpt(bid), "startLine": start, "codeFontSize": font,
        "inspectorLabel": NOTE, "notes": [{"label": a, "value": b} for a, b in notes],
        "cues": [{"at": 1.0, "line": start, "label": title}, {"at": 7.0, "line": end, "label": notes[-1][1].replace("\n", " ")}]},
        f"Godot editor reconstruction: read {path} lines {start}-{end}, then watch the result in the next beat")


def media(bid, event, motion=False):
    return {"type": "GAMEPLAY" if motion else "GRAPHIC", "class": "SHOW", "source": "capture" if motion else "image",
            "evidence_media": f"media/{ID[bid]}.mp4", "show": [{"at": "0", "event": event}]}


def author():
    beats = []

    def add(bid, shot, **kw):
        n = N.get(bid, "")
        beats.append({"beat_id": ID[bid], "film_key": bid, "act": kw.pop("act", "BODY"), "narration_text": n, "voice": "am_onyx",
                      "engine": "kokoro", "estimated_duration_s": max(8, len(n.split()) / 2.5), "shot": shot, **kw})

    add("B00", graphic("ClaudeComposerAsk", {
        "greeting": "Jambo, Liam", "topic": "GODOT GAMEDEV · ASSIGNMENT 7", "segment": "A Breath, A Sword Wave, Frames",
        "command": "Please use Walker to convert my game design document about Downfall's NPCs and Lappland's sword wave into two animations: a looping sprite clip and a committing rig action, with a phase table, read-back tests and one authority per animated node.",
        "runningText": "reading the brief, clips, tests and strips…", "folderLabel": "@NikBearBrown", "modelLabel": "Claude",
        "output": ["npc_idle — Sprite3D frame track, loops", "wave_release — 2D cutout rig, commits (6 / 4 / 10 frames)",
                   "Read-backs, pins, edges, mutations; the user's verdicts"]},
        "Composer opens on the A7 demonstration prompt"), act="ASK")
    add("B01", graphic("BrutalistHesitantWriter", {
        "text": "A clip is a movie.\nEach track: a node, a property, keys.\nOne writer per animated node.\nFeel is designed in frames.",
        "triggerWords": "movie", "replacementWords": "list of keys", "seed": "downfall-a7-20261122",
        "fontSize": 100, "lineSpacing": 1.55, "charMs": 22, "jitter": 10, "mistakeRate": 0, "hesitateWithin": 0,
        "hesitateBetween": 0, "brandLabel": "@NikBearBrown"}, "The writer changes a movie to a list of keys"), lead_silence_s=0.8)
    add("B02", media("B02", "The two clips: routes, nodes, which loops and which commits, and who drives each"))
    for bid in ORDER[3:21]:
        if bid in EXCERPTS:
            add(bid, code(bid))
        else:
            add(bid, media(bid, RESULTS[bid], bid in MOTION))
    add("B21", media("B21", "Recorded test, pin, mutation and suite results; what headless cannot show"))
    add("B22", media("B22", "Human checks in the user's words; who did what; the sheet's source; the filmed commit"))
    add("B23", graphic("ClaudeVerdictArtifact", {
        "artifactTitle": "A7 Verdict", "artifactHeading": "What The Evidence Supports", "brandLabel": "@NikBearBrown",
        "artifactLines": ["Both clips are resources; every track resolves; one writer per animated node; clip and gameplay share the physics tick.",
                          "Caught: missed test changes incl. an unmarked pin (plan session); wrong sheet grid (rig session).",
                          "Claude flagged an early hit flash and facing; the user kept r0 — no observation-driven revision.",
                          "Untested: death, stuns, leaving mid-release. Next: a readable wind-up, prediction first."]},
        "The verdict separates evidence, mistakes and open questions"), act="VERDICT")
    add("B24", graphic("ClaudeComposerAsk", {
        "greeting": "Your turn.", "topic": "ONE NUMBER · ONE PREDICTION", "segment": "Change The Table, Not The Keys",
        "command": PROMPT, "runningText": "paste this into Claude…", "folderLabel": "@NikBearBrown", "modelLabel": "Claude",
        "output": ["Change the phase table.", "Predict each boundary frame.", "The human gives the verdict in play."]},
        "The viewer's bounded experiment is typed and read aloud"), act="HANDOFF")
    add("B25", graphic("ClaudeTitleOutro", {"title": TITLE, "slug": REEL.name}, "Exact title, regular mascot and stock jingle"),
        act="OUTRO", audio_policy="silence", actual_duration_s=7.0)
    sheet = {"metadata": {"title": TITLE, "slug": REEL.name, "topic": "GODOT GAMEDEV · A7 ANIMATION", "kind": "godot-gamedev",
                          "mode": "walker", "brand": "claude-liam", "engine": "kokoro", "voice": "am_onyx", "voice_kokoro": "am_onyx",
                          "palette": "claude", "aspect_ratio": "16:9", "captions": False, "channel": "@NikBearBrown",
                          "folderLabel": "@NikBearBrown",
                          "game": {"name": "downfall-godot (walker-downfall)", "engine_version": "Godot 4.7.2",
                                   "revision": "git HEAD at filming (see gamedev-evidence.json source_revision) + source hashes"}},
             "beats": beats}
    for b in beats:
        assert b["film_key"] == "B25" or b["narration_text"], b["beat_id"]
    (REEL / "beat_sheet.json").write_text(json.dumps(sheet, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(len(beats), "beats")


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


R0 = [f"captures/wave_release/r0/frame000000{n}.png" for n in (27, 29, 36, 37, 40, 41, 49, 50)]
ASSOC = {  # component -> extra files it explains or rests on
    "b03": ["tests/test_npc_idle_readback.gd", "logs/test_npc_idle_readback_60fps.log", "art/field_art.gd", "world/base_map.gd",
            "previews/npc_idle_in_game.gd", "previews/npc_idle_in_game.tscn", "evidence/a7/human-checks.md"],
    "b05": ["art/characters/npc/npc_closure_idle.png", "art/characters/npc/npc_closure_idle.png.import",
            "art/characters/npc/prepare_npc.py", "animations/ATTRIBUTION.md"],
    "b07": ["tests/test_wave_rig_readback.gd", "logs/test_wave_rig_readback_60fps.log", "scripts/a7_mutations.sh"] +
           [f"logs/a7_mutations/{n}" for n in ("summary.txt", "m1.log", "m1.test_wave_rig_readback.log", "m2.log",
                                               "m2.test_npc_idle_readback.log", "m3.log", "m3.test_npc_idle_readback.log",
                                               "m4.log", "m4.test_npc_idle_readback.log", "m4.test_wave_rig_readback.log")],
    "b09": ["tests/test_wave_state_machine.gd"],
    "b11": ["previews/film_wave_dodges.gd", "previews/film_wave_dodges.tscn"] + R0,
    "b13": ["logs/test_wave_state_machine_60fps.log", "tests/a7_probe_headless.gd", "logs/a7_probe_headless_60fps.log"],
    "b15": ["animations/lappland_rig/body.png", "animations/lappland_rig/blade_front.png", "animations/lappland_rig/blade_back.png",
            "tools/a7_cut_rig_parts.py", "previews/wave_rig_turntable.gd", "previews/wave_rig_turntable.tscn"],
    "b17": ["CHANGE-BRIEF.md", "TUNING.md", "previews/wave_release_preview.gd", "previews/wave_release_preview.tscn"],
    "b19": ["logs/test_wave_edges_60fps.log"],
}
EXTRA = [  # non-code components: (id, beats, files, explanation)
    ("overview", ["B02"], ["README.md", "CLAUDE.md", "animations/npc_idle.tscn", "animations/lappland_wave_rig.tscn"],
     "The two clips, their routes and nodes, which loops and which commits, and the authority over each."),
    ("tests", ["B21"], ["TEST-REPORT.md", "tests/test_a7_pins.gd", "logs/test_a7_pins_60fps.log", "logs/test_a7_pins_after_step3_60fps.log",
                        "logs/baseline-before/summary.txt", "logs/baseline-after/summary.txt"],
     "Recorded results of the read-backs, pins, structure and edge tests, mutations and suites, and their headless limits."),
    ("credits", ["B22", "B23"], ["SOURCES.md", "FRICTIONAL.md", "project.godot"],
     "Human checks, who did what, the sheet's source, the filmed revision and the verdict."),
]


def ledger():
    sheet = json.loads((REEL / "beat_sheet.json").read_text(encoding="utf-8"))
    narr = {b["film_key"]: b["narration_text"] for b in sheet["beats"]}
    files, comps, excerpts, pairs = {}, [], [], []

    def attach(path, cid, role):
        rec = files.setdefault(path, {"path": path, "sha256": sha(GAME / path), "role": role, "component_ids": []})
        if cid not in rec["component_ids"]:
            rec["component_ids"].append(cid)
        comp = next(c for c in comps if c["id"] == cid)
        if path not in comp["files"]:
            comp["files"].append(path)

    for bid, (path, start, end, *_rest) in EXCERPTS.items():
        cid = bid.lower()
        result = ORDER[ORDER.index(bid) + 1]
        comps.append({"id": cid, "explanation": narr[bid] + " " + narr[result], "beat_ids": [ID[bid], ID[result]], "files": []})
        attach(path, cid, "A7 source shown verbatim on screen")
        for extra in ASSOC.get(cid, []):
            attach(extra, cid, "Input, fixture, capture or recorded evidence explained by this component")
        excerpts.append({"beat_id": ID[bid], "path": path, "start_line": start, "end_line": end, "text": excerpt(bid)})
        clip = REEL / f"media/{ID[result]}.mp4"
        pairs.append({"code_beat": ID[bid], "result_beat": ID[result], "observation": narr[result],
                      "media": {"path": f"media/{ID[result]}.mp4", "sha256": sha(clip)}})
    for cid, bids, paths, text in EXTRA:
        comps.append({"id": cid, "explanation": text, "beat_ids": [ID[b] for b in bids], "files": []})
        for p in paths:
            attach(p, cid, "Evidence or record shown or cited in this beat")
    inv = sorted(p.relative_to(GAME).as_posix() for p in GAME.rglob("*") if p.is_file()
                 and not any(x in (".godot", ".git") for x in p.relative_to(GAME).parts) and p.suffix != ".uid")
    film = "youtube/" + REEL.name + "/"
    exclusions = []
    for p in inv:
        if p in files:
            continue
        if p.startswith(film):
            reason = "This film's own authoring, capture, media or QC file (not game source)."
            if p == film + "gamedev-evidence.json":
                reason = "This source inventory; self-hash would be recursive."
        else:
            reason = "Outside the A7 animation components: the rest of the game, earlier assignments and films, other tests/logs, art sources or authoring files."
        exclusions.append({"path": p, "reason": reason})
    if not any(e["path"] == film + "gamedev-evidence.json" for e in exclusions):
        exclusions.append({"path": film + "gamedev-evidence.json", "reason": "This source inventory; self-hash would be recursive."})
    data = {"schema_version": 1, "teaching_contract": "code-then-result-v1",
            "source_revision": {"git_commit": subprocess.run(["git", "-C", str(GAME), "log", "-1", "--format=%H"], capture_output=True, text=True).stdout.strip(),
                                "working_tree_note": "Tracked files: " + (subprocess.run(["git", "-C", str(GAME), "status", "--short", "--untracked-files=no", "."], capture_output=True, text=True).stdout.strip() or "no modifications") + ". Untracked: this film folder, the film's preview fixture previews/film_wave_dodges.*, pre-existing .uid sidecars and untracked game files. Hashes below are of the working tree."},
            "files": list(files.values()), "components": comps, "excerpts": excerpts, "exclusions": exclusions,
            "code_result_pairs": pairs}
    (REEL / "gamedev-evidence.json").write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(len(files), "files,", len(exclusions), "exclusions,", len(pairs), "pairs")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["author", "ledger"])
    a = ap.parse_args()
    author() if a.mode == "author" else ledger()
