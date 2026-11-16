#!/usr/bin/env python3
"""build_lanes_act10.py — writes lanes/act10.json (Builder 3, Act X: B69-B74) and checks every real line / number it puts on screen against its source.

  python3 evidence/act10/build_lanes_act10.py        (paths are absolute; run from anywhere)

Checks: B71's commands, comment fragments and template lines against evidence/example/sources/assignment-05.md; B73's code lines against the frozen
signal.gdshader / surface.gdshader; B72's rubric numbers against the assignment's rubric tables and their sums; B69's predicted swatch against
controlled-predictions.json; B74's panel value against captures/lab/states.jsonl (charge / 0.6). Remotion cues are in seconds here (converted at 30 fps
from the ESTIMATED duration); if real audio differs by more than about 10 %, scale them: cue_new = cue * actual / estimated.
"""
import json, re, sys
from pathlib import Path

REEL = Path("/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-first-shaders-materials-godot")
FPS = 30
A = (REEL / "evidence/example/sources/assignment-05.md").read_text()
A_LINES = A.splitlines()
A_PLAIN = A.replace("`", "")          # backticks dropped, as on screen
problems = []


def need_line(line):
    if line not in A_LINES:
        problems.append(f"assignment lacks the line: {line!r}")
    return line


def need_frag(frag):
    if frag not in A_PLAIN:
        problems.append(f"assignment lacks the fragment: {frag!r}")
    return frag


def cues(sec):
    return [max(0, round(s * FPS)) for s in sec]


# ───────────────────────── B71 · clean clone and submit (documented, not run) ─────────────────────────
B71_LINES = ["# " + need_frag("Clone the a5 tag into a fresh folder."),
             "$ " + need_line("godot --headless --path godot --import"),
             "$ " + need_line("./scripts/run-test.sh <existing_test>.gd 60"),
             "# " + need_frag("Confirm the counts match TEST-REPORT.md and no log contains SHADER ERROR."),
             " ",
             "# " + need_frag("Submit a source ZIP of that same GitHub revision,") + " ...",
             "# ... " + need_frag("together with SUBMISSION.md:"),
             need_line("Git tag and submitted commit SHA:"),
             "...",
             need_line("Final film SHA-256:")]
B71_CUES_S = [0.4, 2.3, 3.1, 4.9, 0, 8.1, 9.2, 10.0, 10.4, 10.8]

# ───────────────────────── B72 · rubric ─────────────────────────
ru = {"Implementation and explanation": 60, "Frictional": 10, "GitHub version posting": 10, "Relative Quartile": 20}
for k, v in ru.items():
    if not re.search(rf"\|\s*{re.escape(k)}[^|]*\|\s*{v}\s*\|", A):
        problems.append(f"rubric row not found: {k} = {v}")
split = {"Specification and context": 8, "Shader from code": 12, "Textured shader and materials": 14, "The language": 10, "Verification": 8, "Brutalist explainer": 8}
for k, v in split.items():
    if not re.search(rf"\|\s*{re.escape(k)}[^|]*\|\s*{v}\s*\|", A):
        problems.append(f"60-point row not found: {k} = {v}")
if sum(ru.values()) != 100 or sum(split.values()) != 60:
    problems.append(f"sums wrong: {sum(ru.values())} / {sum(split.values())}")

# ───────────────────────── B73 · real shader lines ─────────────────────────
sig = (REEL / "evidence/example/sources/signal.gdshader").read_text().split("\n")
sur = (REEL / "evidence/example/sources/surface.gdshader").read_text().split("\n")
for want, got in (("\tALBEDO = mix(base, active_color.rgb, activation);", sig[9]), ("uniform float activation : hint_range(0.0, 1.0) = 0.0;", sig[2]),
                  ("uniform sampler2D color_map : source_color, filter_nearest;", sur[2]), ("uniform sampler2D roughness_map : filter_nearest;", sur[3])):
    if want != got:
        problems.append(f"shader line mismatch: {want!r} vs {got!r}")

# ───────────────────────── B69 / B74 · numbers ─────────────────────────
cp = json.loads((REEL / "evidence/example/controlled-predictions.json").read_text())
row = [r for r in cp["rows"] if r["activation"] == 0.5 and r["stripe"] == "dark"][0]
if row["predicted_display_rgb8_compatibility"] != [48, 105, 74]:
    problems.append("predicted swatch (48,105,74) not in controlled-predictions.json")
states = [json.loads(l) for l in (REEL / "captures/lab/states.jsonl").read_text().splitlines()]
s609 = [s for s in states if s["frame"] == 609][0]
if f"{s609['charge'] / 0.6:.3f}" != "0.944":
    problems.append(f"lab frame 609 charge/0.6 = {s609['charge'] / 0.6:.3f}, not 0.944")

lanes = {
    "B69": {
        "lane": "manim", "class": "B69_OneFilm",
        "visual_intent": "Act title 'Ship It, and How It's Graded' (serif 40) top-left. A grey path with five stops; a terracotta dot travels along it and each stop gets a picture and a one-to-three-word label as the voice names it: 'your game' (the REAL pad crop of captures/lab/lab_000300.png), 'four answers' (four ticked circles), 'captures' (the REAL pad capture at activation 0.5 beside a swatch of the predicted colour 48, 105, 74), 'tests, mutations' (a terminal icon and a cross), 'the limits' (an eye). Then three outline chips land under the path: 'scripted input', 'reconstruction', 'held frame'. The tag 'instructor example \u00b7 A. I.-written' lands with the capture (the 0.5 pad capture is the example's own).",
        "motion_claim": "The dot walks the film's contents in the order the voice lists them; the three labels land when the voice says label.",
        "show": [{"at": 0.06, "event": "stop 1: your game (real pad crop)"}, {"at": 0.22, "event": "stop 2: four answers"}, {"at": 0.4, "event": "stop 3: captures + predicted swatch"}, {"at": 0.58, "event": "stop 4: tests, mutations"}, {"at": 0.69, "event": "stop 5: the limits"}, {"at": 0.81, "event": "chip: scripted input"}, {"at": 0.87, "event": "chip: reconstruction"}, {"at": 0.89, "event": "chip: held frame"}],
        "runner_up": "CONSIDERED, not rendered: Remotion LibraryIconRow of five line icons",
        "why": "The sentence is a list in time; a path with a travelling dot makes the order the motion, and two of the five stops are real pictures (the pad, a capture) rather than icons. Chips are the assignment's own three label kinds.",
        "sparse": True, "sparse_reason": "A thin row of small pictures on cream with the voice carrying the explanation; only underfill/clustered are waived."},
    "B70": {
        "lane": "manim", "class": "B70_Repository",
        "visual_intent": "Isometric: a low-walled kraft box (the repository) with the GitHub logo chip beside it. Eight items listed down the left (shaders, scenes, driver, materials, textures, tests, wrapper, documents, logs), each dropping a white file-cube into the box as it is named (a terracotta dot moves down the list). Then four outline icons each crossed by a prohibition mark: cache, credentials, audio and video, over 25 MB. The list and the refusals leave; a commit chain of five nodes appears along the bottom with alternating chips (Professor Bear portrait = you, Claude mark = agent) and labels shader, draft, review, change, check; a terracotta dot reads along the chain; a tag 'a5' hangs on a string from the last commit.",
        "motion_claim": "Each named item drops into the repository; the refusals are crossed out; the commits line up in the order the work happened; the tag is hung on the final commit.",
        "show": [{"at": 0.02, "event": "GitHub chip"}, {"at": 0.09, "event": "shaders drops in"}, {"at": 0.3, "event": "tests drops in"}, {"at": 0.38, "event": "documents, logs"}, {"at": 0.43, "event": "cache refused"}, {"at": 0.48, "event": "credentials refused"}, {"at": 0.54, "event": "audio, video refused"}, {"at": 0.6, "event": "over 25 MB refused"}, {"at": 0.67, "event": "list leaves, commit chain grows"}, {"at": 0.8, "event": "reader dot along the chain"}, {"at": 0.9, "event": "a5 tag on a string"}],
        "runner_up": "CONSIDERED, not rendered: Remotion CCPlainShell with the real output of git ls-files",
        "why": "The sentence is an arrangement (things in a box, things kept out, an order of commits, a tag); the iso box and the tag on a string are the show-tell kit's own vocabulary. A git ls-files listing would show the example's file names, but the beat teaches what a student posts. The chain is a drawing of the assignment's commit order (shader, agent draft, your review, agent change, your check), not the example's history.",
        "sparse": True, "sparse_reason": "Small iso box and a chain on cream; the voice carries the list; only underfill/clustered are waived."},
    "B71": {
        "lane": "remotion", "pattern": "CCPlainShell",
        "props": {"title": "documented, not run", "lines": B71_LINES, "lineCues": cues(B71_CUES_S),
                  "rings": [{"line": 7, "cue": round(10.15 * FPS)}, {"line": 9, "cue": round(10.95 * FPS)}],
                  "fontSize": 34, "windowMargin": 96, "durationSeconds": "__AUDIO__"},
        "visual_intent": "A plain terminal titled 'documented, not run', no output anywhere: the assignment's sentence 'Clone the a5 tag into a fresh folder.' as a comment; `godot --headless --path godot --import`; `./scripts/run-test.sh <existing_test>.gd 60`; the comment 'Confirm the counts match TEST-REPORT.md and no log contains SHADER ERROR.'; the submission sentence as two comment lines; then two real lines of the SUBMISSION.md template ('Git tag and submitted commit SHA:' and 'Final film SHA-256:', ringed) with a cut mark between them.",
        "motion_claim": "The two commands land with the voice; the two template fields that name the commit and the checksum are ringed last.",
        "show": [{"at": 0.03, "event": "clone comment"}, {"at": 0.17, "event": "import command"}, {"at": 0.23, "event": "run-test command"}, {"at": 0.36, "event": "confirm-the-counts comment"}, {"at": 0.59, "event": "submit comments"}, {"at": 0.75, "event": "commit SHA field (ringed)"}, {"at": 0.85, "event": "film SHA-256 field (ringed)"}],
        "runner_up": "CONSIDERED, not rendered: Manim: Menlo commands on cream with a drawn checklist",
        "why": "Commands belong on the terminal skin, shown without output because nothing was run (title says so). The assignment's two code blocks are used verbatim; its prose is quoted as comments. The assignment gives no clone command, so none is invented. The template lines are plain bright text so the midpoint frame (the two commands) carries type GATE T can read.",
        "sparse": False},
    "B72": {
        "lane": "manim", "class": "B72_Rubric",
        "visual_intent": "'100 points' (serif 40) over a vertical grade column that grows from the bottom in four grey segments, each with its number and a label: 60 implementation, 10 honest log, 10 GitHub = Canvas, 20 relative. Then the 60 becomes the whole column (everything else fades, a brace and the numeral 60 appear) and splits from the top into six pieces as the voice says them: 8 specification, 12 shader from code, 14 textures, materials, 10 the language, 8 verification, 8 the film.",
        "motion_claim": "The column fills 60, 10, 10, 20; the 60 splits into 8, 12, 14, 10, 8, 8 on the voice.",
        "show": [{"at": 0.1, "event": "60 grows"}, {"at": 0.3, "event": "10 (log)"}, {"at": 0.41, "event": "10 (GitHub)"}, {"at": 0.57, "event": "20 (relative)"}, {"at": 0.71, "event": "the 60 becomes the column; brace + 60"}, {"at": 0.78, "event": "8 specification"}, {"at": 0.81, "event": "12 shader from code"}, {"at": 0.84, "event": "14 textures, materials"}, {"at": 0.89, "event": "10 the language"}, {"at": 0.93, "event": "8 verification"}, {"at": 0.95, "event": "8 the film"}],
        "runner_up": "CONSIDERED, not rendered: Remotion chart (horizontal stacked bar)",
        "why": "A part-to-whole that then splits is a column that splits; heights are proportional to points (a 14 is taller than an 8). Labels are the rubric rows' own names shortened to one to three words; the numbers are the assignment's and sum to 100 and to 60 (checked by the lane builder).",
        "sparse": True, "sparse_reason": "One column and its labels on cream; the voice carries the explanation; only underfill/clustered are waived."},
    "B73": {
        "lane": "manim", "class": "B73_Explain",
        "visual_intent": "Top: 'late work', ten grey cells (100 per cent in tens), the last cell drops out leaving a dashed outline, '−10% a day'. Then three challenge cards, each a label over REAL lines of the example's shaders (Menlo size 24, real line numbers): 'change a line, predict' over signal.gdshader line 10; 'set a uniform, predict a pixel' over signal.gdshader line 3; 'point to the line that makes data' over surface.gdshader lines 3-4, line 4 (the sampler with no source_color) ringed and labelled 'no hint: data'. Tag 'instructor example · A. I.-written' bottom right.",
        "motion_claim": "A cell falls away on 'ten percent'; each card lands as its ask is spoken; the ring lands on the one line without a hint.",
        "show": [{"at": 0.08, "event": "late work: a cell drops out, -10% a day"}, {"at": 0.35, "event": "card 1 lands"}, {"at": 0.55, "event": "card 2 lands"}, {"at": 0.73, "event": "card 3 lands"}, {"at": 0.82, "event": "line 4 ringed, 'no hint: data'"}],
        "runner_up": "CONSIDERED, not rendered: Remotion CCPlainShell showing the three lines as a terminal",
        "why": "The three asks are three pictures a viewer should recognise on a test day: a line, a uniform, a sampler line. Real lines on outlined code cards with the asked-about line ringed teach the 'point to the line' skill directly. The lane plan named surface line 3; the line that makes the texture read as DATA is line 4 (no source_color), so lines 3-4 are shown and line 4 is ringed (see the factcheck).",
        "sparse": False},
    "B74": {
        "lane": "manim", "class": "B74_Integrity",
        "visual_intent": "Two stamps (double circles) land and are ringed as the voice says authorship (a page icon inside) and verification (a tick inside), each with a one-word label. A brace over both with the label 'course A. I. policy'; a drawn play button labelled 'policy video'. Then all of that leaves and the REAL lab panel (a crop of captures/lab/lab_000609.png, an earlier take of the lab's panel) lands, framed, tagged 'scripted input' and 'earlier take, 14 Oct': only its line 'Render and play still need checking.' (present in both takes of the panel script) is ringed, with an eye labelled 'your eyes'. The panel is never described as the final script's output.",
        "motion_claim": "Two stamps are pressed, the policy brace and video land, then the real panel arrives and its last line is ringed with the eye.",
        "show": [{"at": 0.1, "event": "authorship stamp pressed and ringed"}, {"at": 0.27, "event": "verification stamp pressed and ringed"}, {"at": 0.52, "event": "course A. I. policy brace"}, {"at": 0.65, "event": "policy video play button"}, {"at": 0.73, "event": "the real panel replaces the stamps, tags scripted input + earlier take, 14 Oct"}, {"at": 0.88, "event": "ring: Render and play still need checking. + eye"}],
        "runner_up": "CONSIDERED, not rendered: Remotion ProfessorBearPortrait with a stamp animation",
        "why": "Integrity is two things being falsely claimed; two stamps that are pressed (and ringed) are the picture, and the real panel is the last picture because it is the film's own statement of what headless proves and what it cannot. The panel is a real capture of an EARLIER take of the lab's verification panel (the frozen verification.gd prints other words), so it is tagged 'earlier take, 14 Oct', and only the line that is in both takes is ringed. It lands after the clip midpoint, framed in grey.",
        "sparse": True, "sparse_reason": "A few large marks on cream, then one real capture; the voice carries the explanation; only underfill/clustered are waived."},
}

if problems:
    print("PROBLEMS:")
    for p in problems:
        print("  ", p)
    sys.exit(1)
out = REEL / "lanes" / "act10.json"
order = ["B69", "B70", "B71", "B72", "B73", "B74"]
out.write_text(json.dumps({k: lanes[k] for k in order}, indent=1, ensure_ascii=False) + "\n")
print("wrote", out)
print("verified: B71 lines vs assignment, B72 rubric rows and sums (60+10+10+20=100; 8+12+14+10+8+8=60), B73 shader lines, B69 swatch, B74 panel value 0.944")
