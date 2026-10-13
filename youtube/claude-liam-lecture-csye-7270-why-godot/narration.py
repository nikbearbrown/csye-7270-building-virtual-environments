"""narration.py — every spoken line of the lecture, in beat order. Liam, in for Bear (Kokoro am_onyx).

Film 2 of 3 of "CSYE 7270: Start Here". FOR the course CSYE 7270, so the course is named (metadata.course) in BOPEN and BIDEA only.
Sources: the engines brief researched 2026-10-09 (primary docs and GitHub API figures, dates and quotes in
_conducting-series-evidence/ and the scratchpad brief), the real no-bridge Godot demo (_conducting-series-evidence/godot-evidence/DEMO.md), and the
real command-line runs on Bear's Mac. HONESTY: Bear's premise ("Godot is the natural fit; Unity/Unreal MCP are raw and catching up") is only partly
supported: Godot has NO official MCP; Unity and Unreal DO (beta / experimental). The film says so (Act IV) and bases the case on what is readable
and checkable (Acts II and III).
Rules: "three-D model" for a 3D model, "A. I. model" for an AI model. Numbers spelled out for Kokoro; on-screen text keeps the real spelling.
"""

SLUG = "claude-liam-lecture-csye-7270-why-godot"
TITLE = "Why Godot"
GREETING = "Hola"
SERIES = "CSYE 7270: Start Here"
COURSE = "CSYE 7270"
VIDEO_NUMBER = 2
VIDEO_COUNT = 3
TITLE_LINES = ["Why Godot"]
OPENING_DESCRIPTION = "Why Godot suits an AI agent"

BOPEN = ("C S Y E seven two seven zero, Start Here. Why Godot. "
         "Learn what Godot is, why an A. I. can work in it without special tools, and how it compares with Unity and Unreal.")

ACTS = [
    ("I", "What Godot Is"),
    ("II", "A Scene Is a Text File"),
    ("III", "A Complete Command Line"),
    ("IV", "The Other Two Engines"),
    ("V", "Why It Fits, and What This Proves"),
]

BODY = [
    # ── ACT I · what Godot is ────────────────────────────────────────────────────────────
    ("B01", 0, "Godot is a game engine: the program that runs a game's graphics, physics, input and sound, with an editor to build it in."),
    ("B02", 0, "It is free and open source, under the M I T licence. No account. No fee. No royalty on what you make."),
    ("B03", 0, "A non-profit foundation looks after its name and its money. It does not own the engine. The code belongs to its contributors, and no company can buy it."),
    ("B04", 0, "The current stable version is four point seven point two, released on the eighteenth of August, twenty twenty-six. The Mac download is about one hundred and seventy megabytes. Installed on this Mac, it is three hundred and thirty-seven. One application file."),
    ("B05", 0, "Games are written in G D script, a language built for Godot that reads a lot like Python, or in C sharp. The example games in this course use G D script."),

    # ── ACT II · a scene is a text file ──────────────────────────────────────────────────
    ("B06", 1, "Here is the property that matters most for directing an A. I. A Godot scene is a text file. This is a real one, from a Pong game. Every object in the game is a few plain lines: its name, its type, its settings."),
    ("B07", 1, "The scripts are text. The project's settings are text. On this Mac, the file command reports every script and scene file in a real Godot project as plain text."),
    ("B08", 1, "That means an A. I. needs no special bridge to read your game. It reads a file, like any other. It edits a file, like any other. And your version history shows exactly what changed."),
    ("B09", 1, "Here is a real run. A fresh Claude Code agent was given a small Pong project and one job: add a label to the scene by editing its text. It could read, edit, write a file, and run Godot. That was all."),
    ("B10", 1, "It read the scene. It inserted three lines. It wrote a small check script. And it ran Godot with no window. Twenty-three seconds, from request to report."),
    ("B11", 1, "Its own check printed pass. That means little: the agent wrote the check. So a second check, written outside the project, ran as well. All twenty-one original nodes still there. Scripts still attached. Exactly one new label."),
    ("B12", 1, "And a control: the same check, run on the scene before the edit, fails. A check that cannot fail proves nothing."),
    ("B13", 1, "One difference. The agent left out an identifier that every other node in that scene carries. Godot loaded the file anyway. When Godot saved the scene itself, it added one. So the text was valid, but not what Godot itself saves."),
    ("B14", 1, "Now the limits. One run. A tiny change: one node, no resources, no signals. Nothing was drawn on screen, so this does not show it looks right. And the agent's tool limits were written in its prompt, not enforced, because the headless sign-in on this machine had expired."),

    # ── ACT III · a complete command line ────────────────────────────────────────────────
    ("B15", 2, "The second property: Godot has a complete command line. You can run it with no window, and tell it to import a project, run a script, check a script for errors, or export a build."),
    ("B16", 2, "Its help lists ninety-five options. Here is a real project, imported headless on a copy: exit code zero, in three seconds. Then run and quit: exit code zero, in a quarter of a second."),
    ("B17", 2, "That is what makes the A. I.'s work checkable. It can run the game for sixty frames without a window, and the exit code and output tell you whether it ran. You can run the same command yourself."),
    ("B18", 2, "And one more honest detail. That import quietly created one new file, a missing sidecar the project should have had. Even a command that sounds read-only can change your folder. Check the diff."),

    # ── ACT IV · the other two engines ───────────────────────────────────────────────────
    ("B19", 3, "Now the other two big engines, Unity and Unreal. Both now have an official M C P server, from the company itself, that lets an A. I. call the editor's tools directly. Godot has none."),
    ("B20", 3, "Unity's went public in March twenty twenty-six, and is in open beta. Unity's own blog says features may change. Its scenes are text too, by default, in a format called YAML, though they are packed with cross-references."),
    ("B21", 3, "Unreal Engine five point eight shipped an M C P plug-in in June twenty twenty-six, labelled Experimental. Epic's own documentation says many features are incomplete or missing. And Unreal's levels and assets are binary files, which an A. I. cannot read as text."),
    ("B22", 3, "Godot has no official M C P. It has several from the community. The best known has about six thousand stars on GitHub, and has not been updated since April. Unity's biggest community server has more than twice that."),
    ("B23", 3, "So if you heard that Godot has the better M C P story, it does not. Godot does not need one for the basic work: its files are plain text and its command line is complete."),
    ("B24", 3, "One thing not to confuse. In June twenty twenty-six, Godot's foundation said engine code must be human-written, and would ban autonomous agents from its repository. That is about contributing to Godot. Using an A. I. to make a game with Godot is a different thing."),

    # ── ACT V · why it fits ──────────────────────────────────────────────────────────────
    ("B25", 4, "So why Godot, for this course? Not because it has the best A. I. features. Because everything you need to inspect is plain text, everything you need to run is on the command line, and nothing sits behind an account."),
    ("B26", 4, "Unity is close on text. Unreal is furthest. And both say their features may change. This is the picture on the ninth of October, twenty twenty-six. Check it again before you rely on it."),
    ("B27", 4, "What this film does not show: that Godot makes better games, or that an agent handles large, complicated scenes without help. Those are for you to test."),
]

BIDEA = ("Hola. This is Liam, in for Bear. In C S Y E seven two seven zero, every game is made in one engine: Godot. "
         "The easy answer is that it is free. The real answer is about what an A. I. can read, and what you can check.")

BDEFS = ("Five terms. A game engine is the program that runs a game's graphics, physics and input. "
         "A scene is one saved arrangement of a game's parts. "
         "Headless means running a program without a window, from the command line. "
         "M C P, the Model Context Protocol, is a standard that lets an A. I. call another program's tools. "
         "And the M I T licence lets anyone use, change and share software for free.")

BDEFS_TERMS = [
    ("Game engine", "the program that runs a game's graphics, physics and input"),
    ("Scene", "one saved arrangement of a game's parts"),
    ("Headless", "running a program with no window, from the command line"),
    ("MCP", "Model Context Protocol: an AI calls another program's tools"),
    ("MIT licence", "anyone may use, change and share the software, free"),
]

BIDEA_TEXT = ("We use Godot because it is free.", "free", "readable")

BVDT_HEADING = "Why Godot"
BVDT_LINES = [
    "Godot is free, open source, and one small application.",
    "A scene is a text file an agent can read and edit.",
    "The command line runs, imports and checks with no window.",
    "Unity and Unreal have official MCP, in beta. Godot has none.",
    "Godot's edge is what you can read and check, not its AI features.",
    "One run proves little. Check it yourself.",
]
BVDT_NARRATION = ("Let's recap with Claude. Godot is free, open source, and one small application. "
                  "A scene is a text file an agent can read and edit. "
                  "The command line runs, imports and checks with no window. "
                  "Unity and Unreal have official M C P, in beta. Godot has none. "
                  "Godot's edge is what you can read and check, not its A. I. features. "
                  "One run proves little. Check it yourself.")

BHTF_PROMPT = ("Here is a copy of a small Godot project. Make one change by editing a scene's text file: add a label that says hello. "
               "Then prove it by running Godot with no window. Tell me exactly what you ran, what it printed, and what you could not check.")
BHTF_CHECKS = ["Check: write a second check yourself, outside the project. Run it on the edited scene and on the original.",
               "Check: open the game and look at the label."]
BHTF_NARRATION = ("Your turn. Paste this into Claude: " + BHTF_PROMPT +
                  " Then check two things yourself. Write a second check outside the project, and run it on the edited scene and on the original. "
                  "And open the game, and look at the label.")
BHTF_SEGMENT = "Edit the Text, Then Prove It"
TOPIC = "CSYE 7270 · WHY GODOT"
TAGS = ["CSYE 7270", "Godot", "Unity", "Unreal Engine", "MCP", "Game development", "AI agents", "Claude Code", "Nik Bear Brown"]
