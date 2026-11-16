"""narration.py — every spoken line of the lecture, in beat order. Liam, in for Bear (Kokoro am_onyx).

Source: the whole of the assignment "Shaders, Materials, and the Godot Shading Language"
(csye-7270-building-virtual-environments/assignments/05-shaders-materials-and-godot-shading-language.md, identical to
walker-claude/assignments/course-briefs/05-...md; read in full 2026-10-16), walked through with Bear's instructor example as the evidence.

This film is made FOR a course (metadata.course is set), so the course is named in BOPEN and BIDEA, as the lecture skill allows; everything else
stands on its own for someone who is not enrolled: no "this chapter", no "the book", no module numbers, and NO VIDEO NUMBERS.

HONESTY: "the example" always means the instructor example: shaders, tests and notes written by an AI (Codex) under Professor Bear's direction.
They are never called hand-written and never called a Claude Code session. The assignment's prompts are shown as the assignment's own text,
"documented, not run".

Pronunciation: numbers are spelled out so Kokoro reads them as meant; acronyms are spelled with spaces (G P U, S R G B, G L S L). "A. I." keeps its dots
(the pronunciation dictionary joins it). File names are spoken as words ("the change brief", "the project context file", "the test wrapper") because
Kokoro mangles "dot M D"; on-screen text keeps the real names. Whisper-check after audio (BUILD-PROMPT step).
"""

SLUG = "claude-liam-lecture-first-shaders-materials-godot"
TITLE = "Your First Shaders and Materials with Claude and Godot"
PLAYLIST = "CSYE 7270 Virtual Environments"        # the card's copy budget is 42 characters; the full playlist title (47) does not fit
GREETING = "Hallo"

ACTS = [
    ("I", "Two Shaders and Their Materials"),
    ("II", "Predict Before You Write"),
    ("III", "Give the Agent Rules"),
    ("IV", "The Shader From Code"),
    ("V", "A Shader That Reads Textures"),
    ("VI", "Textures Are Information"),
    ("VII", "Read the Language"),
    ("VIII", "What the Agent Gets Wrong"),
    ("IX", "Check What You See"),
    ("X", "Ship It, and How It's Graded"),
]

# (beat_id, act index, narration)
BODY = [
    # ── ACT I · the job and its four ideas ──────────────────────────────────────────────────────────────
    ("B01", 0, "Here is the job: two shaders you write by hand, and the materials that use them, added to your game. One tints an object while a game state holds. One dresses a surface with textures."),
    ("B02", 0, "A shader is a small program the G P U runs for every pixel it draws, all at once. It sees only built-ins, uniforms and textures, and remembers nothing. So game state must arrive as a uniform."),
    ("B03", 0, "A material pairs one shader with values for its uniforms, textures included. Many materials can share one shader. Your second shader gets two that look different."),
    ("B04", 0, "A texture is a grid of numbers, and the shader decides what they mean. Colour is stored as S R G B and must be decoded first. A mask, noise or roughness map must be read as stored."),
    ("B05", 0, "Godot's shading language is close to G L S L. You choose a shader type instead of writing main, and the type decides which functions and built-ins exist. Hints shape the Inspector; some change what the shader receives."),
    ("B06", 0, "You write every line of both shaders and your language notes. Claude Code drafts the project context file, writes the driver and tests, audits the materials, and reviews on request. It never edits your shaders. If you adopt a suggestion, type it yourself and record it."),
    ("B07", 0, "A note on the example you will see. An A. I. wrote its shaders, tests and notes, under Professor Bear's direction. They are not student work, and no Claude Code session produced them. The runs and captures are real."),
    ("B08", 0, "Credit every texture: source address, authors, licence, and the date you checked. Poly Haven needs no credit; the course still does. A texture written by code is fine; show the code. Never commit credentials."),
    # ── ACT II · predict ────────────────────────────────────────────────────────────────────────────────
    ("B09", 1, "Predict first. Commit a change brief before you write either shader or send a prompt. Keep the original; add dated revisions below it. The agent works to this file."),
    ("B10", 1, "The state: what the effect communicates, why the player needs it, and which script holds it. In the example, the pad shows charge, one script owns it, and the shader only watches."),
    ("B11", 1, "The specification: the shader's path and type, and each uniform's name, type, hint, default, and what sets it. The example has four. Only activation comes from the game."),
    ("B12", 1, "The colour line: the one line in the fragment function that changes the colour. You write the shader from it, and predict from it. Here it mixes the stripe colour toward the active colour."),
    ("B13", 1, "Make rules measurable: the uniform's value at start and end, and a change that takes the same game time at thirty, sixty and one hundred forty-four frames per second. A second press: restart, extend or ignore? The example ignores it."),
    ("B14", 1, "Boundaries: collision, movement, input and earlier tests stay unchanged. Presentation reads game state and never writes it. Then the evidence split: for each rule, a headless test, or your own eyes."),
    ("B15", 1, "Controlled inputs: three uniform values, two pixels, computed by hand. At zero, a dark stripe is the quiet colour times point six five: sixty-six, twenty-seven, fifteen. Only unshaded output keeps that arithmetic honest."),
    ("B16", 1, "The hint experiment gets predictions too: greys sixty-four, one twenty-eight, one ninety-two, sampled with and without source color. By the S R G B formula, Forward Plus leaves the colour read alone and brightens the data read to one thirty-seven, one eighty-eight, two twenty-five. On Compatibility, say so, and measure."),
    ("B17", 1, "The material plan names each texture's role and import settings, and each uniform's type, range, default and group. Predict at least three failures, with their checks. The example predicted four: a missing colour hint, an undeclared uniform, a shader edit changing both materials, and a headless pass that cannot certify colour."),
    ("B18", 1, "Then five questions: the renderer the project names, the colour arriving in fragment, how long a frame-counting version lasts at three frame rates, where the default lives, and whether hint range clamps a value set from code."),
    # ── ACT III · rules for the agent ───────────────────────────────────────────────────────────────────
    ("B19", 2, "Before the first prompt, commit one wrapper script and run every earlier test through it, as your baseline. It sets a timeout, pins the frame rate, keeps a log, and fails on any shader error or script error."),
    ("B20", 2, "The timeout matters: a script error before the test quits leaves headless Godot running. In the example, a driver test hit one and ran until the clock stopped it. Exit status one twenty-four means the test hung."),
    ("B21", 2, "The log check matters too: Godot can print a shader error and still exit with status zero. The wrapper reads the log, and turns that zero into a one."),
    ("B22", 2, "After every agent session, two checks. Read its final result event, which shows a hit turn limit and permission denials. Then run git diff stat on the shaders folder. It must print nothing."),
    ("B23", 2, "Step one: the agent drafts the project context file. Facts it cannot find quickly, each with a file reference, under a hundred twenty lines, importing your change brief instead of pasting it."),
    ("B24", 2, "Commit the draft unedited, then your review, separately. The recorded draft cited wrong lines and claimed a headless test would settle the look. Scope the session too: an agent allowed all of git can commit its own draft, and erase who wrote what."),
    # ── ACT IV · the shader from code ───────────────────────────────────────────────────────────────────
    ("B25", 3, "Now the shader, from code alone. Write it by hand from the specification, with the colour line exactly; if it must change, revise the specification first, dated. Reimport, confirm no shader error, commit it alone. The built-in time is global, never time since your event."),
    ("B26", 3, "The example's first lines choose the spatial type and unshaded rendering. Then four uniforms, each with a type, a hint and a default: activation, two colours, and a stripe count."),
    ("B27", 3, "In fragment, U V picks the stripe: the fractional part of U V times the stripe count, cut at one half. A dark stripe is the quiet colour at sixty-five percent; a light stripe, the quiet colour."),
    ("B28", 3, "Line ten is the colour line: mix the stripe colour toward the active colour, by activation. At zero, stripes. At half, stripes fading. At one, one flat green."),
    ("B29", 3, "Then direct the driver and its test, plan first. The prompt forbids editing your shader, asks for the smallest plan before any edit, and wants real input, three frame rates, and what the test cannot prove."),
    ("B30", 3, "In the example, the driver is one line. Each physics tick, the game sets activation to charge divided by point six. The game owns the state; the shader only observes."),
    ("B31", 3, "The test sends real key events, times the charge in game seconds, presses again mid-charge, pauses, resets, and compares the uniform with the charge on every sample. Ten checks."),
    ("B32", 3, "At thirty, sixty and a hundred forty-four frames per second: point six game seconds each time, no failures. All headless. Nothing is drawn, so none of it can say what colour the pad is."),
    ("B33", 3, "Now break your shader twice. First, delete a semicolon. A shader that fails to parse reports an empty uniform list, so the test must exit one. Restore the file."),
    ("B34", 3, "Second, rename the driven uniform in the shader only. Setting an undeclared uniform raises no error. In a re-run of the example, the driver test still passed ten of ten, and the pad would never change colour. Only the uniform list catches it."),
    # ── ACT V · the textured shader and two materials ───────────────────────────────────────────────────
    ("B35", 4, "Next, the textured shader. Get textures first, with provenance. Then set their import settings yourself rather than leave them on detect: compress mode, mipmaps, and the normal map flag in the import file. The editor then has nothing to change later."),
    ("B36", 4, "The example's textures are sixty-four pixels square, written by a script. One holds two colours in stripes. The other holds two numbers, one hundred two and two sixteen. Same kind of file, different meaning."),
    ("B37", 4, "Two samplers: the colour map says source color, the roughness map says nothing. That one hint separates colour from data. Four more uniforms sit in two groups, surface and pattern."),
    ("B38", 4, "Fragment multiplies the colour map by the tint, reads roughness from the red channel, scales it by a gain, and clamps it. Metallic is just a number."),
    ("B39", 4, "Two materials use this shader: matte and coated. They differ in tint, roughness, scale and metallic. Save them as resource files. For an imported scene, keep them behind Use External, so a reimport keeps them."),
    # ── ACT VI · the hint experiment, the normal-map check, the audit ───────────────────────────────────
    ("B40", 5, "The hint experiment, in its own scene. A committed script writes a three-by-one picture, imported lossless with no mipmaps. One shader binds it twice, with source color and without, and a boolean picks which writes the colour."),
    ("B41", 5, "Two materials, one per value, on two quads. In the example, on Compatibility, both read sixty-four, one twenty-eight, one ninety-two. This renderer hides the difference."),
    ("B42", 5, "Run the experiment again on Forward Plus and the quads disagree. The colour read stays sixty-four, one twenty-eight, one ninety-two. The data read comes out one thirty-seven, one eighty-eight, two twenty-five, as predicted."),
    ("B43", 5, "So a texture is information, not a picture. One file, read two ways, gives two sets of numbers. Which is right depends on what the numbers mean, and on the renderer you name."),
    ("B44", 5, "Normal maps get a curl check. A real map stores a surface's slopes, which have no curl; an imitation has no surface. The ratio lands near zero in the right convention, near one with no surface, near two in the wrong convention."),
    ("B45", 5, "Calibrate on a pair: OpenGL and DirectX, same material. On Poly Haven's stone floor, OpenGL read as OpenGL measured point four eight; read as DirectX, one point five two. Not zero and two. Set the threshold from the pair."),
        ("B46", 5, "A map made by code measured point zero five and one point nine five. The example's game materials use no normal map, so these are calibration runs. And know the limit: a Sobel-filtered picture passes. Curl-free means a surface exists, not the right one."),
    ("B47", 5, "The audit. Commit your work, then have the agent audit it, changing nothing: a materials table, and a test of shader path, hints, values, texture paths and import settings. The example's test makes fifty-three checks."),
    ("B48", 5, "Verify from an empty cache: delete the cache folder, reimport, run again. Then delete source color from the colour sampler. The test must exit one: two failures, one per material. Restore it."),
    # ── ACT VII · read the language ─────────────────────────────────────────────────────────────────────
    ("B49", 6, "Last build step: read the shader Godot writes. Make a standard material with albedo, normal and roughness textures, make it unique, and convert it to a shader material in the Inspector. Save the code. The game never uses it."),
    ("B50", 6, "In the generated file: shader type and render mode, lines three and four. Albedo colour, line six; its sampler, line seven, says source color. The normal sampler, line nineteen, does not. Albedo is written at thirty-five, roughness at forty-three, normal map at forty-six."),
    ("B51", 6, "Then eight questions, in your own words, with line references to your shaders. What does the shader type decide? Which functions and built-ins exist. All three example shaders say spatial, on line one."),
    ("B52", 6, "Which functions did you write, and when do they run? Fragment runs for every pixel covered; vertex, once per corner. Move the colour line into vertex and it will not compile: albedo is a fragment output. Compute it there and pass it on, and it is blended between corners: the stripes are lost."),
    ("B53", 6, "Which built-ins did you read, and which did you write? The hint fixture reads U V, the fragment coordinate and the viewport size, all read-only. The shaders write albedo and roughness."),
    ("B54", 6, "Does a hint change only the Inspector, or the value the shader receives? Range shapes the slider. On Forward Plus, source color on a texture changes the value, as the experiment showed. Whether range clamps a value set from code, a capture will show."),
    ("B55", 6, "Last two. Each fragment runs alone, so it cannot read its neighbour: game state arrives as a uniform. And Godot gives you processor functions and hints that become controls. The agent may check your line references, never write the answers."),
    ("B55B", 6, "Done is a list. Every rule has a recorded check. All three mutations fail their tests. No session changed your shaders. Every texture is credited, every language question answered with a line. The earlier suites keep their counts. Claude said it works is not on the list."),
    # ── ACT VIII · what the agent gets wrong ────────────────────────────────────────────────────────────
    ("B56", 7, "Recorded mistakes. After a thirty frames-per-second failure, an agent rewrote its test to call the update function directly; the summary still said thirty and one forty-four. And its type checks were round trips: with a semicolon deleted, all eleven passed. Reading the test, and the mutation, caught them."),
    ("B57", 7, "An audit misnamed an enum: four is the Ag X tone mapper, not Aces. An import setting was a key the importer ignores. A material with ambient occlusion off passed a hundred checks that never asserted it. Look every value up."),
    ("B58", 7, "The example made its own: an audit that expected a vector type where the engine reports a colour, four failures before the fix; and a calibration script that would not parse, because two variables had no declared type."),
    # ── ACT IX · use it ─────────────────────────────────────────────────────────────────────────────────
    ("B59", 8, "Green logs are not done. A headless pass proves your shaders parse, their uniforms are declared and driven, and your materials are wired. It proves nothing about the screen. Every visual rule ends in a human check."),
    ("B60", 8, "Capture in the engine, not with a screenshot tool: operating system screenshots apply colour profiles and scaling. Switch the driver off, set the value, wait for the frame to draw, and save the viewport's image."),
    ("B61", 8, "The example's four captures: activation zero, half, one and two, with two named pixels in each, measured beside the prediction. At half, they match within one."),
    ("B62", 8, "Not every value matches: the dark stripe at zero is off by five in blue, full activation by three in red. That is a finding. A probe on a plain constant colour shows the same shortfall: not the shader's arithmetic. Cause still open."),
    ("B63", 8, "Switch renderer and the gap grows. On Forward Plus, the same shader at half, on the light stripe, reads seventy-six, one thirty-seven, ninety-seven, not sixty-six, one twelve, seventy-eight. Those numbers fit a calculation in linear light. Predict for the renderer you use."),
    ("B64", 8, "At two, the Compatibility pad turns cyan: red goes negative, green passes one, and the display clips. Hint range did not stop it, in either renderer. So the answer is no. The range belongs to the slider, not the shader."),
    ("B65", 8, "In play: trigger the state by normal play several times and check the boundaries hold. The example's footage is scripted key presses, labelled that way. Your own playtest is required."),
    ("B66", 8, "Interface sweep: each uniform at minimum, default and maximum. In the example, roughness spreads the highlight, scale repeats the texture, a black tint hides detail. Record what changed, and what breaks the look."),
    ("B67", 8, "One shader, two materials. Edit the shader temporarily and both objects change. Restore it, change one value in one material, and only that one changes. In the example, the shared edit changed both spheres; the tint edit, the left."),
    ("B68", 8, "After your first editor session, run git status and explain any import file the editor rewrote; include a revision driven by something you saw. What the example did not do: no person played it, no screenshot was compared with an engine capture, no Claude Code session ran, and the colour shortfall is unexplained. Say so plainly."),
    # ── ACT X · ship it, and how it's graded ────────────────────────────────────────────────────────────
    ("B69", 9, "Make one film: your game, the state, and the textured object; the four answers, each pointing at a line of your code; your captures against the predictions; the tests, the mutations, and what no headless run can show. Label scripted input and reconstructions."),
    ("B70", 9, "Post the project on GitHub: shaders, scenes, driver, materials, textures with import files, tests, wrapper, reviewed documents and logs. No cache, no credentials, no audio or video, and no file over twenty-five megabytes. Commit in the order the work happened, so a reviewer sees who wrote which lines. Tag the final commit a five."),
    ("B71", 9, "Then verify from a clean clone of the tag: import once, run every test at its pinned frame rate, and match the counts to your test report. Submit a source zip of that revision, with a note naming the commit and the film's checksum."),
    ("B72", 9, "One hundred points. Sixty for implementation and explanation, ten for your honest log, ten for GitHub matching Canvas, twenty relative to the class. Of the sixty: eight, twelve, fourteen, ten, eight and eight."),
    ("B73", 9, "Late work loses ten percent a day. And you must be able to explain it: change a line and predict the result, set your uniform and predict a pixel, point to the line that makes a texture read as data."),
    ("B74", 9, "Presenting agent-written shader code as hand-written misrepresents authorship. Recording a human check you did not perform misrepresents verification. Both break the course's A. I. policy; watch its video first. A passing run proves it is wired. Your eyes decide how it looks."),
]

BOPEN = ("C S Y E seventy-two seventy, Virtual Environments. Your First Shaders and Materials with Claude and Godot. "
         "Learn to write a shader, give it materials, and tell what a passing test proves from what only your eyes can.")

BIDEA = ("Hallo. This is Liam, in for Bear, with the fifth assignment for C S Y E seventy-two seventy. "
         "The easy belief is that a passing test means the shader looks right. This assignment is the opposite: the tests prove it is wired, and you prove how it looks.")

BDEFS = ("Six terms. A G P U is the chip that draws graphics. A pixel is one dot of the image. A uniform is a value game code hands to a shader. "
         "The renderer is the part of Godot that draws. Headless means running Godot with no window. And a mutation is a deliberate break, to prove a test notices.")

BVDT_LINES = [
    "A shader runs for every pixel and remembers nothing.",
    "A material pairs one shader with values.",
    "A texture is numbers, and the shader decides what they mean.",
    "Predict first, then break your shader to prove the tests notice.",
    "Tests prove it is wired; your eyes prove how it looks.",
    "You write the shaders; the agent never edits them.",
]
BVDT_NARRATION = "Let's recap with Claude. " + " ".join(BVDT_LINES)

BHTF_PROMPT = ("Read my change brief and my project context file. List every observable rule in the specification, and for each one say whether a headless test can prove it "
               "or only my eyes can. Then propose the smallest test plan. Do not write or edit any shader, and do not commit.")
BHTF_NARRATION = BHTF_PROMPT          # lecture skill: props.command == narration_text; "Your turn." is the on-screen greeting
BHTF_CHECKS = [
    "Check: every rule is marked test, or eyes.",
    "Check: git diff --stat godot/shaders/ prints nothing.",
]
