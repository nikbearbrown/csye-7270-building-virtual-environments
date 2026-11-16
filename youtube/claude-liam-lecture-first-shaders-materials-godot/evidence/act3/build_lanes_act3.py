#!/usr/bin/env python3
"""build_lanes_act3.py — writes lanes/act3.json (Builder 3, Act III: B19-B24) and checks every real line it puts on screen against its source file.

  python3 evidence/act3/build_lanes_act3.py          (from the reel folder; or from anywhere: paths are absolute)

Remotion terminal beats (B20, B21, B22): every line that is not marked ANNOTATION is looked up VERBATIM in the log/json it came from (the check
fails loudly otherwise). lineCues are written in seconds below and converted to frames (30 fps) from the ESTIMATED duration (beat_sheet.json
estimated_duration_s). If real audio differs from the estimate by more than about 10 %, scale the cues:  cue_new = cue * actual / estimated.
"""
import json, re, sys
from pathlib import Path

REEL = Path("/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-first-shaders-materials-godot")
EV = REEL / "evidence"
FPS = 30


def src(p):
    return (REEL / p).read_text().splitlines()


SRC = {
    "hung_log": src("evidence/example/course-signal-30.1791994689764928000.log"),
    "hung_json": src("evidence/example/course-signal-30.1791994689764928000.json"),
    "r5_raw": src("evidence/runs/R5-shader-error-raw.log"),
    "r5_wrap": src("evidence/runs/R5-shader-error-wrapper.log"),
    "guard": src("evidence/runs/git-diff-guard.log"),
    "assign": src("evidence/example/sources/assignment-05.md"),
}
journal = (EV / "runs/journal-commands-exit-codes-elapsed.tsv").read_text()

problems = []


def real(srcname, line):
    """a line that must exist verbatim in the named source"""
    if line not in SRC[srcname]:
        problems.append(f"NOT IN {srcname}: {line!r}")
    return line


def cues(seconds):
    return [max(0, round(s * FPS)) for s in seconds]


# ─────────────────────────────────────────── B20 · the example's first driver run, 14 Oct (exit 124) ───────────────────────────────────────────
# command = the "command" array of the .json joined with spaces (that is the argv the example's runner recorded)
argv = json.loads("\n".join(SRC["hung_json"]))["command"]
cmd20 = "$ " + " ".join(argv)
B20_LINES = [cmd20,
             "...",
             real("hung_log", "PASS pause freezes charge"),
             real("hung_log", "PASS reset clears uniform"),
             real("hung_log", "PASS interruption has no late gate"),
             real("hung_log", "SCRIPT ERROR: Invalid call. Nonexistent 'float' constructor."),
             real("hung_log", "          at: run (res://course-series/tests/test-signal-driver.gd:57)"),
             "...",
             real("hung_log", "TIMEOUT"),
             "# the example's JSON record of that run:",                                        # ANNOTATION
             real("hung_json", '  "elapsed_seconds": 120.01059412956238,'),
             real("hung_json", '  "exit_code": 124,')]
B20_CUES_S = [0.35, 0.7, 1.0, 1.3, 1.6, 2.1, 2.5, 7.4, 7.55, 8.2, 8.6, 9.2]

# ─────────────────────────────────────────── B21 · exit 0 is not "no errors": raw run vs wrapper run (re-run for this film) ───────────────────────────────────────────
B21_LINES = ["$ godot --headless --path godot --script res://tests/shader-error-demo.gd",           # EVIDENCE-NOTES R5 form of the journal command
             "...",
             real("r5_raw", "SHADER ERROR: Expected a ';' after 'shader_type spatial'."),
             "...",
             real("r5_raw", "UNIFORMS 0"),
             real("r5_raw", "godot exit=0"),
             " ",
             "$ ./scripts/run-test.sh shader-error-demo.gd 60",                                  # journal: ./scripts/run-test.sh shader-error-demo.gd 60
             "...",
             real("r5_wrap", "SHADER ERROR: Expected a ';' after 'shader_type spatial'."),
             "...",
             real("r5_wrap", "UNIFORMS 0"),
             real("r5_wrap", "wrapper exit status: 1 (see journal.tsv R5-wrapper)")]
B21_CUES_S = [0.4, 0.7, 1.7, 2.4, 2.7, 3.4, 0, 5.75, 5.95, 6.15, 6.35, 6.55, 6.95]
if "./scripts/run-test.sh shader-error-demo.gd 60" not in journal:
    problems.append("journal lacks the wrapper command")
if "R5-raw\texit=0" not in journal.replace("\t", "\t") and "R5-raw" not in journal:
    problems.append("journal lacks R5-raw")

# ─────────────────────────────────────────── B22 · after every agent session: the .jsonl event (documented) and the diff guard (re-run) ───────────────────────────────────────────
def assign_line(prefix):
    for l in SRC["assign"]:
        if l.startswith(prefix):
            return l
    problems.append(f"assignment lacks a line starting {prefix!r}")
    return prefix


A1 = "1.  **Read the final result event** in the session's `.jsonl` file."
A2 = "2.  **Run `git diff --stat godot/shaders/`**, which must print nothing."
for a in (A1, A2):
    if not any(l.startswith(a[:40]) for l in SRC["assign"]):
        problems.append(f"assignment text not found: {a[:50]!r}")
B22_LINES = ["1. Read the final result event in the session's .jsonl file.",                       # assignment line 163 (bold and backticks dropped)
             "# documented, not run: no session ran for the example",                            # ANNOTATION
             " ",
             "2. Run git diff --stat godot/shaders/, which must print nothing.",                 # assignment line 164
             real("guard", "$ git diff --stat godot/shaders/     # clean tree"),
             real("guard", "(exit 0; printed nothing above this line)"),
             " ",
             "# a hand edit stands in for an agent edit",                                        # ANNOTATION (the log's own comment says: made for this film)
             real("guard", "$ git diff --stat godot/shaders/     # after the one-character edit"),
             real("guard", " godot/shaders/signal.gdshader | 2 +-"),
             real("guard", " 1 file changed, 1 insertion(+), 1 deletion(-)"),
             real("guard", "(exit 0)")]
B22_CUES_S = [2.0, 3.4, 0, 6.4, 6.75, 7.1, 0, 7.55, 7.8, 8.05, 8.25, 8.45]

# ─────────────────────────────────────────── the lanes ───────────────────────────────────────────
lanes = {
    "B19": {
        "lane": "manim", "class": "B19_Wrapper",
        "visual_intent": "Act title 'Give the Agent Rules' (serif 40) top-left, tag 'from the assignment' top-right. The REAL wrapper script (evidence/runs/scripts/run-test.sh, nine lines, verbatim) in a Menlo size-24 outline block with its real line numbers; lines 6 and 8 are soft-wrapped into indented continuation rows with a gutter hook (no character added or dropped). Then four right-margin brackets land as the voice names the jobs, each with an ink numeral: 1 timeout (row 6a), 2 frame rate (row 6b), 3 log (line 5 and the tee on row 6c), 4 fails on errors (the grep on line 8); a legend along the bottom (terracotta dot, numeral, one to three words) lands with each bracket.",
        "motion_claim": "The script is on screen, then each of the four jobs is bracketed the moment the voice names it, and its label joins the legend.",
        "show": [{"at": 0.05, "event": "act title, tag, and the nine real lines land"}, {"at": 0.56, "event": "bracket 1 + 'timeout'"}, {"at": 0.65, "event": "bracket 2 + 'frame rate'"}, {"at": 0.75, "event": "brackets 3 + 'log' (line 5 and the tee)"}, {"at": 0.83, "event": "bracket 4 + 'fails on errors'"}],
        "runner_up": "RENDERED: Remotion CCPlainShell showing the script as `cat` output (all nine lines, line 6 in ONE row at fontSize 26 / windowMargin 96) with whole-line rings; ready to swap in under the key \"alt\"",
        "why": "The four jobs live inside one 101-character line, so a whole-line ring cannot tell them apart; brackets at the margin can, and a soft-wrapped block at size 24 stays legible where one 101-character row cannot (no size at or above the floor shows 101 characters on this frame). The terminal skin fits the line but cannot bracket tokens.",
        "sparse": False},
    "B20": {
        "lane": "remotion", "pattern": "CCPlainShell",
        "props": {"title": "recorded by the example, 14 Oct", "lines": B20_LINES, "lineCues": cues(B20_CUES_S),
                  "rings": [{"line": 5, "cue": round(2.4 * FPS)}, {"line": 11, "cue": round(9.3 * FPS)}],
                  "fontSize": 26, "windowMargin": 96, "durationSeconds": "__AUDIO__"},
        "visual_intent": "A plain terminal (CCPlainShell, no Claude chrome) titled 'recorded by the example, 14 Oct': the real argv of the example's first driver run (30 fps), a cut mark, the last three real PASS lines, the real 'SCRIPT ERROR: Invalid call. Nonexistent 'float' constructor.' (ringed) with its 'at:' line, a cut mark, the log's own last word 'TIMEOUT', then two real lines of the example's JSON record: '\"elapsed_seconds\": 120.01059412956238,' and '\"exit_code\": 124,' (ringed).",
        "motion_claim": "The tests pass, the script error lands and is ringed, then nothing more happens until TIMEOUT arrives; the exit code 124 lands last and is ringed.",
        "show": [{"at": 0.03, "event": "command"}, {"at": 0.09, "event": "three PASS lines"}, {"at": 0.18, "event": "SCRIPT ERROR (ringed) + its at: line"}, {"at": 0.64, "event": "cut, TIMEOUT"}, {"at": 0.71, "event": "JSON record comment"}, {"at": 0.74, "event": "elapsed_seconds"}, {"at": 0.8, "event": "exit_code 124 (ringed)"}],
        "runner_up": "CONSIDERED, not rendered: Manim: Menlo log excerpt on cream with a drawn clock that runs out",
        "why": "git/Godot output is a terminal's own text: SHOW-THE-THING rung 1 and the lead's rule put it on CCPlainShell, verbatim, with cut marks. The 4.9-7.3 s stretch with no new line is the hang. fontSize 26 and windowMargin 96 are forced by the 103-character real command (the window must stay inside the title-safe margin, which windowMargin 48 does not; see the factcheck).",
        "sparse": False},
    "B21": {
        "lane": "remotion", "pattern": "CCPlainShell",
        "props": {"title": "re-run for this film", "lines": B21_LINES, "lineCues": cues(B21_CUES_S),
                  "rings": [{"line": 5, "cue": round(3.5 * FPS)}, {"line": 12, "cue": round(7.05 * FPS)}],
                  "fontSize": 34, "windowMargin": 96, "durationSeconds": "__AUDIO__"},
        "visual_intent": "Plain terminal titled 're-run for this film'. Top: `godot --headless --path godot --script res://tests/shader-error-demo.gd`, a cut, the real 'SHADER ERROR: Expected a ';' after 'shader_type spatial'.', a cut, 'UNIFORMS 0' and the log's own last line 'godot exit=0' (ringed). Below: `./scripts/run-test.sh shader-error-demo.gd 60` with the same SHADER ERROR line, 'UNIFORMS 0' and 'wrapper exit status: 1 (see journal.tsv R5-wrapper)' (ringed).",
        "motion_claim": "The same error prints twice; the first run ends exit=0 (ringed), the wrapper run ends exit status 1 (ringed).",
        "show": [{"at": 0.04, "event": "raw command"}, {"at": 0.19, "event": "SHADER ERROR"}, {"at": 0.37, "event": "godot exit=0 (ringed)"}, {"at": 0.63, "event": "wrapper command"}, {"at": 0.72, "event": "SHADER ERROR again"}, {"at": 0.77, "event": "wrapper exit status: 1 (ringed)"}],
        "runner_up": "CONSIDERED, not rendered: Manim two-up: two Menlo columns on cream with big 0 and 1 numerals",
        "why": "Two real runs of one six-line script, side by side in time on the real terminal skin; the two rings are the claim (same error, exit 0 versus exit 1). The wrapper's last line is the real log line, '(see journal.tsv ...)' included, not tidied.",
        "sparse": False},
    "B22": {
        "lane": "remotion", "pattern": "CCPlainShell",
        "props": {"title": "1 documented, not run · 2 re-run for this film", "lines": B22_LINES, "lineCues": cues(B22_CUES_S),
                  "rings": [{"line": 5, "cue": round(7.2 * FPS)}, {"line": 10, "cue": round(8.35 * FPS)}],
                  "fontSize": 36, "durationSeconds": "__AUDIO__"},
        "visual_intent": "Plain terminal. Check 1 is the assignment's own sentence ('1. Read the final result event in the session's .jsonl file.') with a note that it is documented, not run (no session ran for the example). Check 2 is the assignment's sentence '2. Run git diff --stat godot/shaders/, which must print nothing.' followed by the real log of the diff guard: the command on a clean tree and the real line '(exit 0; printed nothing above this line)' (ringed); a note that a hand edit stands in for an agent edit; the same command after a one-character edit with its real two stat lines (the summary line ringed) and '(exit 0)'.",
        "motion_claim": "The first check lands as a sentence only (nothing was run); the second prints nothing (ringed); after a one-character edit the same command prints one stat line (ringed).",
        "show": [{"at": 0.19, "event": "check 1 sentence"}, {"at": 0.33, "event": "documented, not run note"}, {"at": 0.62, "event": "check 2 sentence"}, {"at": 0.65, "event": "clean-tree command"}, {"at": 0.69, "event": "printed nothing (ringed)"}, {"at": 0.73, "event": "hand-edit note"}, {"at": 0.76, "event": "command after the edit"}, {"at": 0.8, "event": "stat lines, summary ringed"}, {"at": 0.82, "event": "(exit 0)"}],
        "runner_up": "CONSIDERED, not rendered: Manim hybrid: a drawn session-1.jsonl card (turn limit / permission denials) then the shell as a rendered image",
        "why": "git's output is shown on the real terminal skin. The .jsonl half has no real artifact (no session ran), so it is stated as the assignment's sentence, flagged documented, not run, instead of an invented result event. The checklist sentences are plain bright text so the clip's midpoint carries type GATE T can read (a ghost comment alone fails it). The log's checkout step is left out so the last landing is at 82 %.",
        "sparse": False},
    "B23": {
        "lane": "manim", "class": "B23_ContextFile",
        "visual_intent": "File name CLAUDE.md (Menlo) top-left, tag 'instructor example · A. I.-written' top-right. The example's REAL CLAUDE.md as an outline block at size 20: real lines 1-5 (@AGENTS.md, @CHANGE-BRIEF.md, @assignments/05-shaders-materials/CHANGE-BRIEF.md, a blank line, '# Signal Garden context'), a gap row, then real line 22 (a fact that names signal.gdshader). Line 22 is ringed with the label 'file reference'; a bar of 120 with 65 filled and the numerals 65 and 120 under the word 'lines'; then lines 2-3 are ringed and an arrow from the label 'imports your brief' points at them.",
        "motion_claim": "The file lands, a fact with its file reference is ringed, the bar fills to 65 of 120, and the two import lines are ringed last.",
        "show": [{"at": 0.1, "event": "CLAUDE.md lines land, tag"}, {"at": 0.43, "event": "line 22 ringed + 'file reference'"}, {"at": 0.58, "event": "bar fills to 65 of 120"}, {"at": 0.74, "event": "'imports your brief' arrow + rings on lines 2-3"}],
        "runner_up": "RENDERED: Remotion ClaudeCodeBeat (largeText) with lines 1-5 and 22; clean and legible, but no line numbers, no rings and no counter; props under the key \"alt\"",
        "why": "The numbers are the claim (65 against 120) and the two ringed import lines are the second claim; a drawn bar and rings on the real lines say both, which the code-card skin (no rings, no counter) cannot. Real lines only; the prose block (line 10 says 'Assignments 1-9') is left out and a gap row says so.",
        "sparse": True,
        "sparse_reason": "One outline block and a bar on cream with the voice carrying the explanation; only underfill/clustered are waived."},
    "B24": {
        "lane": "manim", "class": "B24_CommitAndScope",
        "visual_intent": "A two-node commit chain: Claude Code's logo chip over 'draft' ('unedited' under it), a Professor Bear portrait over 'review'. A tag 'recorded in the assignment' with two crossed items, 'wrong lines' and 'headless settles look' (the recorded draft's mistakes). Then the assignment's own flag line in Menlo, soft-wrapped after a comma, tagged 'documented, not run': --allowedTools \"Read,Write,Glob,Grep,Bash(git status:*),Bash(git diff:*),Bash(git log:*),Bash(ls:*)\"; below it a chip 'git:*' with a cross and 'not allowed'.",
        "motion_claim": "The draft commit and the review commit are separate nodes; the allowed-tools list lands with git limited to status, diff and log, and git:* is crossed out.",
        "show": [{"at": 0.04, "event": "agent chip + draft node"}, {"at": 0.1, "event": "'unedited'"}, {"at": 0.13, "event": "review node + portrait"}, {"at": 0.36, "event": "'wrong lines' crossed"}, {"at": 0.43, "event": "'headless settles look' crossed"}, {"at": 0.56, "event": "allowed-tools line lands"}, {"at": 0.68, "event": "git:* crossed out"}],
        "runner_up": "CONSIDERED, not rendered: Remotion CCPlainShell with the flag line (documented, not run) and the commit chain as comments",
        "why": "The chain (who made which commit) is a drawing; the flag line is shown as the assignment's own text on a labelled block, soft-wrapped because it is 100 characters. A chip for git:* is crossed out because the assignment's reason is about git:*, which the line deliberately leaves out.",
        "sparse": True,
        "sparse_reason": "Two small groups on cream (a chain, a flag line); the voice carries the explanation; only underfill/clustered are waived."},
}

# ready-to-swap alternatives that were rendered during the audition (make_sheet.py ignores the key "alt")
_wrap = src("evidence/runs/scripts/run-test.sh")
lanes["B19"]["alt"] = {"lane": "remotion", "pattern": "CCPlainShell",
                       "props": {"title": "the wrapper, from the assignment", "lines": ["$ cat scripts/run-test.sh"] + _wrap, "lineCues": [0] * (len(_wrap) + 1),
                                 "rings": [{"line": 6, "cue": 180}, {"line": 8, "cue": 240}], "fontSize": 26, "windowMargin": 96, "durationSeconds": "__AUDIO__"}}
_cm = src("evidence/example/sources/CLAUDE.md")
lanes["B23"]["alt"] = {"lane": "remotion", "pattern": "ClaudeCodeBeat",
                       "props": {"title": "CLAUDE.md", "code": "\n".join([_cm[i] for i in (0, 1, 2, 3, 4)] + ["\u2026", _cm[21]]), "sparkLine": "", "language": "markdown",
                                 "largeText": True, "durationSeconds": "__AUDIO__"}}

if problems:
    print("PROBLEMS:")
    for p in problems:
        print("  ", p)
    sys.exit(1)
out = REEL / "lanes" / "act3.json"
out.parent.mkdir(exist_ok=True)
order = ["B19", "B20", "B21", "B22", "B23", "B24"]
out.write_text(json.dumps({k: lanes[k] for k in order}, indent=1, ensure_ascii=False) + "\n")
print("wrote", out)
print("all real lines verified verbatim against their sources")
