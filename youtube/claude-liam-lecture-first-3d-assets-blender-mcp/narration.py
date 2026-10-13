"""narration.py — every spoken line of the lecture, in beat order. Liam, in for Bear (Kokoro am_onyx).

Source: assignments/03-first-3d-assets-with-blender-mcp.md (the whole assignment, read in full 2026-10-06).
This film is made FOR a course (metadata.course is set), so the course is named in BIDEA, as the lecture skill allows;
everything else stands on its own for someone who is not enrolled: no "this chapter", no "the book", no module numbers.

Numbers are spelled out so Kokoro reads them the way they are meant (whisper-check after audio). Acronyms Kokoro
mangles (glTF, GLB, MCP, AI, CSYE, uv) are spelled out in the narration only; on-screen text keeps the real spelling.

ACTS follows the assignment's own order: the task, the interface tour it says to do BEFORE the brief, the brief,
the MCP connection, the build loop, export and checks, then shipping and grading.
"""

SLUG = "claude-liam-lecture-first-3d-assets-blender-mcp"
TITLE = "Your First 3D Game Assets with Claude and Blender"
GREETING = "Hallo"

ACTS = [
    ("I", "Three Simple Assets"),
    ("II", "Learn the Window First"),
    ("III", "Write the Brief Before You Build"),
    ("IV", "Connect Claude to Blender"),
    ("V", "Build the Assets"),
    ("VI", "Export, Import, Check"),
    ("VII", "Ship It, and How It's Graded"),
]

# (beat_id, act index, narration)
BODY = [
    # ── ACT I · the task ────────────────────────────────────────────────────────────────────────────────
    ("B01", 0, "Here is the job. Make three simple three-D assets for your own game: a crate, a lantern, a coin, whatever your game could use. Then show that they arrived in the game engine the way you meant."),
    ("B02", 0, "You don't make them alone. Claude drives Blender, the free three-D modelling program, through a standard called M C P. And you stay in the loop, because at least one edit has to be yours, made by hand."),
    ("B03", 0, "Pick things you actually want in your game. A prop, like a crate or a lantern. A piece of the environment: a platform, a tree, a rock. Or something the player collects, like a coin or a gem."),
    ("B04", 0, "Simple has a precise meaning. Build each asset from Blender's basic shapes: cube, cylinder, cone, sphere, plane. Move them, scale them, combine them, give them a flat colour. No sculpting, no painted textures, no rigging, no animation."),
    ("B05", 0, "And there's a budget: no more than six basic shapes, and no more than five hundred triangles. A triangle is the flat, three-sided face every surface is cut into. Those limits keep everyone's work comparable. They aren't the engine's."),
    ("B06", 0, "Watch the trap. We counted in Blender five point one. A cube is twelve triangles. A default cylinder is a hundred and twenty-four. A default sphere is nine hundred sixty, nearly twice the whole budget."),
    ("B07", 0, "So ask Claude to lower the segment counts. The same sphere, cut into twelve segments and six rings, is a hundred and twenty triangles."),
    ("B08", 0, "Now the game. From the second assignment on, you build one game in one repository. Each assignment adds a layer, and you hand it in as a git tag. This one's tag is a three."),
    ("B09A", 0, "Your game doesn't have to be three-D. If it's two-D, you still make three assets that suit it, and you add a small three-D scene to your repository."),
    ("B09B", 0, "A floor, one light, a camera, and your three assets side by side at game scale."),
    ("B10", 0, "Later assignments reuse that scene, so you don't need to connect it to your two-D game yet."),
    ("B11", 0, "The tools. Claude Code, through your university access. Blender, which is free. And the Blender M C P add-on, also free. Nothing paid is needed, and nothing paid earns credit."),
    ("B12", 0, "One rule on provenance. You build the geometry yourself, with Claude, in Blender. A downloaded three-D model, or an A. I. generated mesh, doesn't count."),
    ("B13", 0, "The add-on can also fetch three-D models from other sites, and ask A. I. services to generate three-D models. Leave every one of those switched off. They call remote services, and some may cost money."),
    ("B14", 0, "Before you start, watch the course's A. I. policy video. Whatever A. I. does for you, say what it did, and be able to explain every part of what you hand in."),
    # ── ACT II · learn the window ───────────────────────────────────────────────────────────────────────
    ("B15", 1, "Before you write a single prediction, open Blender and just look. Orbit, pan and zoom the three-D viewport. Spend a short session with no prompting at all."),
    ("B16", 1, "Then, in your own words, name six parts of the window. First, the three-D viewport: the big view where your three-D model lives."),
    ("B17", 1, "The toolbar holds the tools you click to move, rotate and scale things. The Outliner lists every object in the scene, as a tree."),
    ("B18", 1, "The Properties editor holds the settings of whatever is selected. Press N, and the sidebar opens. It shows the active object's location, rotation, scale and dimensions."),
    ("B19", 1, "And in the viewport's header, the mode selector switches between Object Mode, where you work on whole objects, and Edit Mode, where you reach into the points and faces of one."),
    ("B20", 1, "Add one screenshot of your own session, with an object selected, to a notes file. That's your evidence that you looked."),
    # ── ACT III · the brief ─────────────────────────────────────────────────────────────────────────────
    ("B21", 2, "Now the brief. Before you ask Claude to build anything, commit a file that says what you expect. Keep the original. Add revisions; don't rewrite it to make every prediction look right."),
    ("B22", 2, "For each asset: its name, what it is in your game, and where it appears."),
    ("B23", 2, "Its size, in metres: width, depth, height. Justify it against something in your game, like the player's height, a tile, or a door."),
    ("B24", 2, "In Blender, one unit is one metre. And Godot's three-D units are metres too. So if you keep it that way, nothing needs converting."),
    ("B25A", 2, "Its origin: the point the three-D model is placed and rotated from. For a prop that stands on the floor, the centre of the underside is usual."),
    ("B25B", 2, "Build around Blender's world origin, the point where the three axes meet, with the base on the floor there."),
    ("B26A", 2, "Put the origin in the middle instead, and the three-D model won't sit on the floor. At floor level, it sinks half its height. Lift it by a guess, and it floats."),
    ("B26B", 2, "Lift it by exactly half its height, and it sits, but only because you moved it. So a check has to look at the origin itself, not just the gap to the floor."),
    ("B27", 2, "Its look: the shape that makes it recognisable, and its material colours. Its budget: your triangle number, at or under five hundred, and why."),
    ("B28", 2, "Finally, at least three predicted failures, each with the check that would catch it. It arrives lying on its side. It's wrong by a factor of ten. The server won't connect. A colour doesn't survive the export."),
    # ── ACT IV · connect Claude to Blender ──────────────────────────────────────────────────────────────
    ("B29", 3, "Now connect Claude to Blender. An add-on inside a running Blender opens a local socket, and a small server, launched by Claude Code, relays Claude's tool calls into the open window. That's the M C P route."),
    ("B30", 3, "Be clear about what's known. The course hasn't run this route. These steps come from the project's own readme, as recorded on the twenty-seventh of September. And the project changes fast."),
    ("B31", 3, "By the sixth of October, the readme led with a one-line installer. It finds the M C P clients on your machine and lets you pick which to set up, not only Claude Code. The assignment says: use the manual steps."),
    ("B32", 3, "Step one, on a Mac: install u v with Homebrew. The readme warns against installing it with pip."),
    ("B33", 3, "Step two: register the server with Claude Code. The readme's own line is shorter. This version adds one setting, which turns off the server's anonymous usage record."),
    ("B34", 3, "Step three: install the add-on. Then, in Blender, open Edit, Preferences, Add-ons, and enable Interface: M C P for Blender."),
    ("B35", 3, "The add-on starts its server when Blender opens. To check, press N and open the M C P for Blender tab. Every service and download checkbox stays off. Then start a fresh Claude Code session, so it sees the server."),
    ("B36", 3, "Now the safety note, plainly. By default, this runs Python that Claude writes, inside your Blender, with no guard. The readme says the socket has no authentication or encryption: anyone who can reach that port can run Python inside Blender."),
    ("B37A", 3, "So keep the port on localhost. Save your work first. And turn the add-on off in Preferences when you're not using it, because the socket opens whenever Blender starts with it enabled."),
    ("B37B", 3, "Last, don't open Blender files from people you don't trust while the server is running."),
    ("B38", 3, "If it doesn't connect, that's data. Give it about two hours, and write down each step and its exact error. After that you may switch to the script route: Claude writes a Blender script, and you run Blender with no window."),
    ("B39A", 3, "Here is that command. Dash b runs Blender in the background. Factory startup skips your own settings. Python runs the script."),
    ("B39B", 3, "And python exit code one makes a crashing script fail loudly. Without it, Blender exits with zero even when the script raises an error."),
    ("B40", 3, "An honest, specific account of a failed attempt, with a working script fallback, earns up to six of the eight M C P points. Not all eight."),
    # ── ACT V · build the assets ────────────────────────────────────────────────────────────────────────
    ("B41", 4, "Now build, one asset at a time. Ask Claude for a plan first. The prompt names the workflow, points at your brief, and gives one task: this asset, exactly as the brief says."),
    ("B42", 4, "The prompt has Claude start by calling get scene info, and say what's already in the scene. Then propose steps. It doesn't build yet."),
    ("B43", 4, "After you approve: one execute Blender code call per object. After each, it has Claude report the object's location, size, rotation and scale, apply rotation and scale before finishing, and show you the result."),
    ("B44", 4, "The prompt names the three-D model downloads and the A. I. generation tools, and forbids them. And it ends with a request: say what you could not verify."),
    ("B45", 4, "Tool names drift. The version the course recorded had get object info, get viewport screenshot, and export scene. By the sixth of October, version two point one point nine had removed all three, and added a tool called look. Use whatever your install has."),
    ("B46", 4, "Your job in the loop: look at it yourself, in the viewport, after every step. Claude can't tell you whether it looks right."),
    ("B47", 4, "Make at least one change by hand: move a part, scale it, or change a colour. Write down what you changed, and what it taught you about the interface."),
    ("B48", 4, "Save the code. Copy every execute Blender code body into a script, one per asset. Otherwise git won't show how the asset was built."),
    ("B49", 4, "And save the dot blend source of each asset. Blender keeps the previous saved version beside it, named dot blend one. Don't commit that."),
    # ── ACT VI · export, import, check ──────────────────────────────────────────────────────────────────
    ("B50", 5, "Export each asset as a G L B: binary glTF, a format Godot reads directly. In Blender's exporter, the plus Y up option should be on. It is by default."),
    ("B51", 5, "That's because Blender's Z axis points up, and in glTF and Godot, Y does. The exporter turns the world on the way out."),
    ("B52", 5, "The newer M C P version has no export tool. So use Blender's own File, Export, glTF two point oh, or have Claude run the exporter through execute Blender code, and save that code too."),
    ("B53", 5, "Put the three files inside your Godot project, and import. Then build the small scene: a floor, a light, a camera, and the three assets side by side at game scale."),
    ("B54", 5, "Now check by number. Ask Claude Code to write a short headless script, one that runs with no window. It loads each asset and prints its bounding box size, its node scale, and the axis it stands along."),
    ("B55", 5, "Compare those numbers with your brief, and with the dimensions in Blender's sidebar. The node scale should be one, one, one. Each asset should stand upright."),
    ("B56", 5, "Place each asset on the floor without moving it. Does it sit, sink or float? That tests your origin. Move the node to compensate, and you've hidden the problem."),
    ("B57", 5, "Check the triangle count too. Right-click Blender's status bar and enable Scene Statistics. Is each asset within your budget?"),
    ("B58", 5, "Read the check Claude wrote. A check can prove less than it claims. In one recorded case, an agent's floor check stopped on the object's own collider, and proved nothing about the floor."),
    ("B59", 5, "Then the part no number covers. Walk the camera around each asset, including from behind and from below. Do the shapes read as what they are at game size? Are faces missing, or colours wrong?"),
    ("B60", 5, "And make at least one revision from something you saw: a size you corrected, an origin you moved, a part you rebuilt. Write the cycle down. Don't delete a failing assertion to turn a report green."),
    # ── ACT VII · ship it, and how it's graded ──────────────────────────────────────────────────────────
    ("B61A", 6, "Then one film. Short and plain is fine. It names your game and your three assets, and shows your real Blender session, with at least one prompt and your own hand edit."),
    ("B61B", 6, "It shows the assets in the running Godot scene, with the headless numbers beside your brief."),
    ("B62", 6, "It says what you checked, what's uncertain, what Claude got wrong, and who did what, human and A. I. Show screenshots or recordings you made yourself, labelled as such. A reconstruction is labelled a reconstruction."),
    ("B63", 6, "Post the source to GitHub: the project, the three G L B files, the blend sources, the scripts, and your notes. Keep large media out. Tag the submitted commit a three, push the tag, and don't move it after you submit."),
    ("B64", 6, "Then verify from a clean clone of the tag. Import once, run your check, open the scene. A working folder on your own machine isn't proof that everything was posted."),
    ("B65", 6, "Hand in a source zip and a submission note: the three assets, which route you used, your hand edit, the checks you ran, and the film link with its checksum."),
    ("B66", 6, "Grading. Sixty points for the work and its explanation, ten for your honest log, ten for matching versions on GitHub and Canvas, and twenty relative to the class. Meeting the criteria can earn the other eighty. It doesn't guarantee the twenty."),
    ("B67", 6, "Of the sixty: ten for the brief, fourteen for the process, eighteen for the three assets, ten for the Godot checks, and eight for the film."),
    ("B68", 6, "Late work loses ten percent a day. And you must be able to explain it. Be ready to open an asset in Blender and show where its size, origin and applied transforms are, and which part you edited by hand."),
    ("B69", 6, "One last point. A passing check shows your assets arrived at the size, orientation and scale you measured. It doesn't show they look right in your game. That judgment is yours."),
]

BIDEA = ("Hallo. This is Liam, in for Bear, with the third assignment for C S Y E seventy-two seventy, Virtual Environments and Real-Time Three-D. "
         "The shortcut is to let an A. I. make your three-D models and accept whatever comes back. This assignment is the opposite: you direct it, you measure it, and you judge it.")

BDEFS = ("Six terms. An asset is a three-D model, image or sound a game uses. M C P, the Model Context Protocol, is a standard that lets an A. I. call another program's tools. "
         "A G L B is a single file that holds a three-D model. The origin is the point a three-D model is placed and rotated from. "
         "A triangle budget is the most triangles a three-D model may use. And last, a bounding box is the smallest upright box around a shape.")

BVDT_LINES = [
    "Three simple assets: basic shapes, under five hundred triangles.",
    "Learn Blender's window first, and name its six parts yourself.",
    "Write the brief before you build: size, origin, budget, predicted failures.",
    "Connect with the manual steps, mind the open socket, fall back after two hours.",
    "Direct Claude one asset at a time, look yourself, and make one edit by hand.",
    "Check the numbers in Godot, judge the look with your own eyes, then ship.",
]
BVDT_NARRATION = ("Let's recap with Claude. Three simple assets: basic shapes, under five hundred triangles. "
                  "Learn Blender's window first, and name its six parts yourself. "
                  "Write the brief before you build: size, origin, budget, predicted failures. "
                  "Connect with the manual steps, mind the open socket, and fall back after two hours. "
                  "Direct Claude one asset at a time, look yourself, and make one edit by hand. "
                  "Check the numbers in Godot, judge the look with your own eyes, then ship.")

BHTF_PROMPT = ("I'm building a game that needs a simple three-D wooden crate. Help me write a brief for it: a size in metres, justified against my player's height, "
               "an origin at the centre of its base, a triangle budget of five hundred or less, and three predicted failures, each with the check that would catch it. "
               "Then write a short Blender Python script that builds the crate from basic shapes with no window, applies its transforms, and prints its dimensions and triangle count. "
               "Finally, tell me what that printout cannot prove.")
BHTF_CHECKS = ["Check: the size is justified against something in my game, not just made up.",
               "Check: the dimensions the script prints match the brief, with transforms applied."]
BHTF_NARRATION = ("Your turn. Paste this into Claude: " + BHTF_PROMPT + " Then check two things yourself. Is the size justified against something in your game, "
                  "and not just made up? And do the dimensions the script prints match the brief, with transforms applied?")
