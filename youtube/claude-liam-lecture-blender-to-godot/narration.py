"""narration.py — every spoken line of the lecture, in beat order. Liam, in for Bear (Kokoro am_onyx).

Self-contained law: no "this chapter", no "the book", no course name. Numbers are spelled out so Kokoro
reads them the way they are meant (whisper-check after audio). Acronyms Kokoro mangles are spelled out
in the narration only; on-screen text keeps the real spelling (glTF, GLB, AABB).

ACTS is the coverage structure; ACTS.md maps every source section to one of these.
"""

SLUG = "claude-liam-lecture-blender-to-godot"
TITLE = "Proving a 3D Model Arrived in Godot"
GREETING = "Bonjour"

ACTS = [
    ("I", "One Column, Three Arrivals"),
    ("II", "Two Ways to Let an Agent Drive Blender"),
    ("III", "Metres, Axes and Applied Scale"),
    ("IV", "What Godot Builds From a File"),
    ("V", "Building the Post, Then Checking the Builder"),
]

# (beat_id, act index, narration)
BODY = [
    # ── ACT I ─────────────────────────────────────────────────────────────────────────────────────
    ("B01", 0, "Here is a column. It should be point two metres wide, point two deep, and one point eight metres tall."),
    ("B02", 0, "We built it in Blender three times, from the same script, changing one setting each time. Then we sent all three into the Godot game engine."),
    ("B03", 0, "The first arrives the way you'd hope. Godot measures its bounding box and reports point two, one point eight, point two: one point eight metres on the vertical axis, and a scale of one."),
    ("B04", 0, "The second arrives lying on its side. The same numbers, but the one point eight now sits on the depth axis, not the vertical one. One setting about which way is up was switched off, and nothing complained."),
    ("B05", 0, "The third looks identical to the first in the running game. Its drawn size is right. But its mesh is a two metre cube, wearing a scale of point one, point nine, point one."),
    ("B06", 0, "Anything generated from that mesh inherits that scale. And a fourth failure shows up on none of these lines: a collision shape that Godot imports as a visible box, with no collision at all."),
    ("B07", 0, "So the question isn't whether the model looks right. It's which facts about an imported model a test can establish, which settings decide them, and what still needs your eyes."),
    # ── ACT II ────────────────────────────────────────────────────────────────────────────────────
    ("B08", 1, "A coding agent is an AI that edits files and runs commands. When it builds a model, it can drive Blender in two ways."),
    ("B09", 1, "The first is live. In the community version, an add-on inside a running Blender opens a local socket, and a small server relays the agent's tool calls into the open window. That's the M C P route."),
    ("B10", 1, "Two projects offer it, a community one and one from the Blender Lab. Both let the agent run Python inside Blender and take screenshots of it."),
    ("B11", 1, "By default, both run agent-written code with no guard. The community project's readme says its socket has no authentication or encryption, so anyone who can reach that port can run Python inside Blender."),
    ("B12", 1, "The Blender Lab page warns of the same risk: no guards. So two rules. Keep the port on localhost. And leave the community add-on's model-generation services off unless you've approved the spend, because they call remote services."),
    ("B13", 1, "The second way needs no window at all. Blender can run a Python script in the background: it builds the model, exports it, and exits."),
    ("B14", 1, "Read the flags. Dash b runs Blender in the background. Factory startup skips your personal settings, so every run starts the same. And python runs the script."),
    ("B15", 1, "Add one more flag: python exit code one. Without it, Blender exits with zero even when your script raises an exception. We raised the same error both ways and got exit codes zero and one."),
    ("B16", 1, "A script that fails but exits zero looks like success to everything downstream. That one flag is the difference."),
    ("B17", 1, "What do you keep from each route? Live, you keep a transcript of tool calls, and a scene that changed with no record of how. By script, you keep a Python file you can diff, rerun and review."),
    ("B18", 1, "The script route has its own failure mode: the script can encode a wrong assumption and repeat it faithfully. Neither route makes the model look right. Both just hand you numbers."),
    # ── ACT III ───────────────────────────────────────────────────────────────────────────────────
    ("B19", 2, "Start with size. In Blender's default scene, one unit is one metre. The glTF format says every linear distance is in metres. And Godot says one unit in three-D is one metre."),
    ("B20", 2, "So a model needs no conversion on the way, as long as Blender's unit scale stays at one."),
    ("B21", 2, "Size matters for physics, not just looks. In Godot's official three-D platformer demo, the player's collision capsule is two point one metres tall, under gravity of twenty-two, at a hundred and twenty physics ticks a second."),
    ("B22", 2, "A prop at the wrong scale becomes a wall the robot can't climb, or a step it never notices."),
    ("B23", 2, "Now direction. Blender is right-handed, with Z pointing up. The glTF format and Godot are also right-handed, but with Y pointing up. Somebody has to turn the world on the way in."),
    ("B24", 2, "Blender's exporter does it, through one option: plus Y up, on by default. It puts Blender's Z extent onto Godot's Y, and Blender's Y extent onto Godot's Z. That's a claim a test can check."),
    ("B25", 2, "Switch the option off, and you get the second column: one point eight on the wrong axis, and a column lying on its side."),
    ("B26", 2, "Next, applied transforms. A Blender object has a transform, location, rotation and scale, and separate mesh data, the vertices. Add a two metre cube and scale it down to a pole, and the vertices still describe a two metre cube."),
    ("B27", 2, "Only the object's scale makes it look thin. The exporter writes that scale onto the node, and Godot shows a mesh with a scale that isn't one. That's the third column. It draws right, and measures wrong."),
    ("B28", 2, "Godot's physics documentation says to avoid scaling collision shapes, so the physics engine can optimize. Separately, its export guidance says to apply the object transform in the modelling software before exporting."),
    ("B29", 2, "In Blender that's Object, Apply, Rotation and Scale. In a script, it's one call, transform apply. Afterwards the scale is one, and the vertices carry the real size."),
    ("B30", 2, "A test can then check both halves: unit scale on every node, and the right size in metres."),
    ("B31", 2, "One more trap, for scripts an agent writes. In Blender five point one, an object's dimensions don't refresh until the scene updates. Set the scale and print the dimensions right away, and you get the old size: two, two, two."),
    ("B32", 2, "Update the view layer first, and you get point two, point two, one point eight. If an agent's log is its evidence, make sure the log is current."),
    # ── ACT IV ────────────────────────────────────────────────────────────────────────────────────
    ("B33A", 3, "Now the file itself. Godot lists glTF two point oh as its recommended three-D format, in a text form and a binary form called G L B."),
    ("B33B", 3, "It can read a dot blend file directly, but only by calling Blender's own exporter, so Blender has to be installed."),
    ("B34", 3, "F B X goes through a library called u f b x. O B J can't carry skinning, animation, a second U V set, or physically based materials."),
    ("B35", 3, "For a small prop, use G L B: one file, no loose textures. Use the text form when you want version control to show changes. Either way, the source of truth for how the asset was made is the script."),
    ("B36", 3, "Materials cross as glTF's metallic-roughness model. A Blender material named PostMetal arrives as a standard material named PostMetal. Blender-only shader nodes don't cross, and lights don't unless you ask for them."),
    ("B37", 3, "Every imported G L B gets a small text file beside it, with import settings. These lines decide what Godot builds. Two of them matter here: use name suffixes, and use node type suffixes."),
    ("B38", 3, "In both of the demo's model files, those two lines are false. A fresh import in Godot four point seven sets both to true. Copy the demo's import file as a template, and Godot ignores the collision hints in your model's names."),
    ("B39", 3, "Those hints are how collision gets decided at import. A mesh named with dash col keeps its mesh and gains a static collision body from the same geometry. Dash conv col does the same with a convex shape."),
    ("B40", 3, "Dash col only removes the mesh and makes a static body with a concave shape. Dash conv col only removes the mesh and makes one with a convex shape. And dash no imp removes the node altogether."),
    ("B41", 3, "Through Blender's glTF export, a collider has to be a mesh. A Blender empty drawn as a box becomes a box shape only with Collada files. So for a prop, the usual pattern is a separate, simple mesh named dash conv col only: invisible, convex, cheap, and shaped by you."),
    ("B42", 3, "Godot's collision page says you can only use concave shapes within static bodies. And primitive shapes often perform best, convex shapes are a compromise, and concave shapes are the slowest."),
    ("B43", 3, "You can also skip names and add a collision shape in a wrapper scene, as the demo does. Its enemy has five collision shapes, and the one named Box holds a sphere, while the one named Sphere four holds the box."),
    ("B44", 3, "Names are claims. The shape is the fact. A test that finds collision by name is trusting a label."),
    # ── ACT V ─────────────────────────────────────────────────────────────────────────────────────
    ("B45", 4, "Now put it to work. The job is a low-poly checkpoint post: a base point six metres square, a tenth of a metre thick, and an eight-sided pole whose top is one point eight metres above the floor."),
    ("B46", 4, "A flat pennant, point four metres long and a quarter metre tall, hangs from the top. Two named materials: PostMetal and FlagCloth. And a separate collision box around the base and pole only, not the pennant."),
    ("B47A", 4, "Before anything runs, predict. Which Godot axis carries the one point eight? What does the bounding box say with plus Y up off? What does Godot report for a scale that was never applied?"),
    ("B47B", 4, "And what happens to a collider named dash conv col only if you copy the demo's import file?"),
    ("B48", 4, "The prompt asks for one bounded change. Write the Blender script. Run Blender only in the background and never open its window. Export a G L B, place it in the level, and write a headless test for size, materials and collision."),
    ("B49", 4, "The first coding agent, Claude Code, took the task. Before its first import, it wrote the model's import file itself, copying the enemy's. That file turns node type suffixes off, which is exactly the setting that disables the collider."),
    ("B50", 4, "Its first Blender run failed: a face already exists. It had added the pennant's back face over the same four vertices. It fixed that, and Blender printed each object's size, scale and materials. Every scale was one."),
    ("B51", 4, "Then its own test failed: no static body. Here the transcript shows the difference between a diagnosis and a guess. The agent decided that Godot four point seven seems to check the mesh name too. It renamed the mesh, rebuilt, reimported. Nothing changed."),
    ("B52", 4, "It wrote a debug script that called a method that doesn't exist. The script never reached its quit line, so headless Godot kept running. At sixty-one turns, after twenty-one minutes, the session hit its turn limit. Nine commands had been refused by the allow list along the way."),
    ("B53", 4, "But the session wasn't over. When we stopped the hung process, the background task's completion woke the agent, and it carried on for twenty-four more turns."),
    ("B54", 4, "It changed two things at once. It turned node type suffixes on, and added a block asking Godot to generate physics for the collision node. The collider appeared, so the fix couldn't tell you which change mattered."),
    ("B55", 4, "Then its context was compacted, and the agent forgot that the godot command was on the path. It tried the full application path seven times, and ended by asking a human to approve a command. It never ran its own finished test."),
    ("B56", 4, "We ran it ourselves. Fifteen of fifteen checks passed. Then we checked what the agent hadn't. A fresh import of the same file uses the defaults, both suffix settings on, and builds a static body with a convex shape."),
    ("B57", 4, "Turn off only node type suffixes, reimport, and the collider comes back as a visible box with no collision. The suffix setting alone was enough. The extra physics block was redundant."),
    ("B58", 4, "The floor check wasn't a floor check. The agent had first placed the post sixteen centimetres too high. Its first test sent a ray straight through the missing collider and found the floor, so the agent moved the post."),
    ("B59", 4, "But the finished test's ray starts two metres above the post and stops on the post's own collider. It proves the post is solid, not that it stands on anything. Our ray, which ignored the post's body, found the floor at minus four, with a gap of zero."),
    ("B60", 4, "A check was weakened to get green. The first run failed because the collision box carried an unnamed default material. The agent's later version skips unnamed materials. Don't weaken an expected result just to get a green report."),
    ("B61", 4, "And the pennant was inside the collider. The box ran out to point three metres, and the pennant runs from point oh eight to point four eight."),
    ("B62", 4, "We sampled the pennant on a one centimetre grid and asked the physics server. Five hundred seventy-two of one thousand sixty-six points were inside the collider. The agent's check, X max at most point three five, passed anyway."),
    ("B63", 4, "Two more weaknesses: the player's capsule height and the post's position were constants typed into the test, not read from the scenes."),
    ("B64", 4, "The revision went to a second agent, Codex, because the first agent's session limit had run out. Five asks: fix only the import setting, make the floor check honest, read the capsule height from the scene, replace the pennant check with one that measures overlap, then rebuild and report."),
    ("B65", 4, "Codex found the setting in the documentation, saw it was already on, removed the extra physics block, and replaced the box with a tapered convex hull. Then it tried to rebuild. Blender crashed in Codex's sandbox four times, with exit code one thirty-nine, a crash in Blender's graphics-backend check at start-up."),
    ("B66", 4, "Then Codex reached for a tool that operates the Blender application itself. That tool refused. We stopped the run there. The prompt hadn't repeated the rule never to open the window, and an agent will look for another way when its first way fails."),
    ("B67A", 4, "We ran the rest ourselves, outside the sandbox. Sixteen of sixteen checks passed."),
    ("B67B", 4, "The size and height on Y, unit scale, exactly two materials, one static body with a convex shape, the capsule read from the scene, a floor gap of zero, and no pennant inside the collider."),
    ("B68", 4, "That last line is wrong. The check looked only at the hull's vertices at the pennant's height, and those are the pole's corners. The slanted faces between them aren't vertices."),
    ("B69", 4, "Sampling the physics server: fifty-five of one thousand sixty-six pennant points are inside, reaching point one one metres. A three centimetre sliver. Far better than the box's five hundred seventy-two, and still not zero."),
    ("B70", 4, "The tapered hull also leaves invisible collision around the pole, about eleven centimetres on each side, halfway up the taper. That's a design judgment, not a test result."),
    ("B71A", 4, "So what does a pass prove? The imported scene's size, axes, scale, materials and collision shape are what the test says, and the post's base touches the floor."),
    ("B71B", 4, "What it doesn't prove: that it looks right lit, that the materials read as metal and cloth, that the collider feels fair, or that the placement suits the level. Those are for a person."),
]

BIDEA = ("Bonjour. This is Liam, in for Bear. A model that looks right in Blender can still arrive in a game wrong. "
         "So the real question isn't how it looks. It's what the game actually received.")

BDEFS = ("Six terms. A mesh is the points and faces that make a shape. A collider is an invisible shape the physics engine tests against. "
         "A bounding box is the smallest upright box around a shape. G L T F is a file format for three-D models. "
         "Headless means running a program with no window. And M C P, the Model Context Protocol, is a standard that lets an agent call another program's tools.")

BVDT_LINES = [
    "A model that looks right can arrive wrong; check the numbers.",
    "A script run leaves a file you can diff; set the exit-code flag.",
    "Metres need no conversion; the Y-up option turns the axes.",
    "Apply scale before export, or the mesh is a disguise.",
    "A name is a claim; the imported shape is the fact.",
    "A green test is a claim; look at the floor and the sliver.",
]
BVDT_NARRATION = ("Let's recap with Claude. A model that looks right can arrive wrong, so check the numbers. "
                  "A script run leaves a file you can diff, so set the exit code flag. "
                  "Metres need no conversion, but the plus Y up option turns the axes. "
                  "Apply scale before export, or the mesh is a disguise. "
                  "A name is a claim; the imported shape is the fact. "
                  "And a green test is a claim, so look at the floor and the sliver.")

BHTF_PROMPT = ("I have a Blender script that builds a prop and exports it as a glb. Write a headless Godot test that loads the glb and checks "
               "its bounding box in metres with the height on Y, unit scale on every mesh node, the exact material names, and which collision shape "
               "the importer built. Read the expected sizes from the script's own printed output, not from constants. Then add a downward ray from "
               "above the prop that ignores the prop's own collider, and require the floor within two centimetres of its base. "
               "Finally, tell me what this test cannot prove.")
BHTF_CHECKS = ["Check: the expected sizes come from your script's output, not typed into the test.",
               "Check: the floor ray ignores the prop's own collider."]
BHTF_NARRATION = ("Your turn. Paste this into Claude: " + BHTF_PROMPT + " Then check two things yourself. Do the expected sizes come from your script's own output, "
                  "and not from numbers typed into the test? And does the floor ray ignore the prop's own collider?")
