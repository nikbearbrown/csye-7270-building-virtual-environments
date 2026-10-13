"""ACT VI · What Walker Is Not  (B24-B26, all Manim)

One cast for the act, drawn from REAL things only:
  B24  the real design-status file of the Clawd game (game folder design/DESIGN-STATUS.json, lines 9-14: the four gate lines, every
       "signed_by": null), its real file mode (-rw-r--r--, from `ls -l`), and Walker's own sentence (docs/zelda-gdd-workflow.md:66,
       the LOCAL working copy: it is not in the committed version). The open padlock is a drawing of the idea, not an observed lock.
  B25  a real run of `walker gdd` on this Mac (zsh:1: command not found: walker, exit 127), the repo search for a test framework,
       the REAL public GitHub page of nikbearbrown/walker (captured 2026-10-09T18:03Z, folder list cropped: no gdd folder) and the
       real file counts of the two publisher runs (11 files from the committed version, 54 from the local working copy).
  B26  the habit as five verbs, each with the exhibit it came from in Act V: CHANGE-BRIEF.md (three predictions, scope), a real frame
       of the running Clawd game, the rejected takes (343 of 540 frames; exit 0, no receipt) and CLAWD-STATUS.json ("human_playtest": "pending").
Every file name, number and line on screen is printed, with its source, by evidence/act6/make_evidence.sh (a plain shell script).
Pacing: a6_at() lands each motion on the real spoken word (faster-whisper times, evidence/act6/word_times.json).
Wording rules: no "this chapter", "the book", "the course", assignment or module on screen; "3D model" never appears bare; AI is "AI".
"""

A6P = "pantry/"
A6_GREY = DIM                 # outlines around text are grey, never ink (GATE T 8.6b)


def a6_at(self, t):
    """Wait until the clip clock reaches t seconds (the real spoken time of a word, minus a small lead)."""
    gap = t - _elapsed(self)
    if gap > 0.05:
        self.wait(gap)


def a6_lab(s, x, y, size=34, color=INK, left=False):
    t = T(s, size, color)
    if left:
        return t.move_to([x, y, 0], aligned_edge=LEFT)
    return t.move_to([x, y, 0])


def a6_mono(s, x, y, size=32, left=False):
    t = M(s, size)
    if left:
        return t.move_to([x, y, 0], aligned_edge=LEFT)
    return t.move_to([x, y, 0])


def a6_img(name, w=None, h=None, at=(0.0, 0.0)):
    im = ImageMobject(A6P + name)
    if w is not None:
        im.set_width(w)
    if h is not None:
        im.set_height(h)
    im.move_to(np.array([at[0], at[1], 0.0]))
    return im


def a6_box(cx, cy, w, h, color=A6_GREY, sw=4, dashed=False):
    """An outline-only cell (never a fill behind text). dashed = drawn but not built."""
    r = Rectangle(width=w, height=h, stroke_color=color, stroke_width=sw, fill_opacity=0).move_to([cx, cy, 0])
    if dashed:
        n = int(2 * (w + h) / 0.42)
        return DashedVMobject(r, num_dashes=n, dashed_ratio=0.6)
    return r


# ── B24 · not an enforcer: the gates live in a file the agent could edit ────────────────────────────────────────────
class B24_NotAnEnforcer(Scene):
    def construct(self):
        # real word times (s): enforcer 1.74 · Gates 2.70 · status file 3.70 · could edit 4.90-5.14 · Walker's own document 5.88 · convention 8.40
        title = T("What Walker Is Not", 40).move_to([-6.0, 2.95, 0], aligned_edge=LEFT)
        self.add(title)
        # the real file, drawn as itself: its name, the four gate rows, each "signed_by": null exactly as the file prints it
        PX0, PX1, PY0, PY1 = -6.15, 0.75, -1.55, 2.2
        panel = Rectangle(width=PX1 - PX0, height=PY1 - PY0, stroke_color=A6_GREY, stroke_width=4, fill_opacity=0).move_to(
            [(PX0 + PX1) / 2, (PY0 + PY1) / 2, 0])
        head = a6_mono("design/DESIGN-STATUS.json", -5.95, 1.78, 32, left=True)
        rows = [("vision", 0.95), ("systems", 0.25), ("world", -0.45), ("scope", -1.15)]
        labs = [a6_lab(n, -5.45, y, 34, left=True) for n, y in rows]
        nulls = [a6_mono('"signed_by": null', -3.7, y, 32, left=True) for n, y in rows]
        self.play(Create(panel), FadeIn(head), run_time=0.45)
        self.play(LaggedStart(*[AnimationGroup(FadeIn(a), FadeIn(b)) for a, b in zip(labs, nulls)], lag_ratio=0.35), run_time=0.9)
        # "it is not an enforcer": a padlock drawn closed, then the shackle lifts open ("no lock")
        a6_at(self, 1.25)
        RX = 2.9
        body = Rectangle(width=0.8, height=0.6, stroke_color=A6_GREY, stroke_width=6, fill_opacity=0).move_to([RX, 1.2, 0])
        arc = Arc(radius=0.28, start_angle=0, angle=PI, arc_center=[RX, 1.85, 0], color=A6_GREY, stroke_width=6)
        legR = Line([RX + 0.28, 1.85, 0], [RX + 0.28, 1.5, 0], color=A6_GREY, stroke_width=6)
        legL = Line([RX - 0.28, 1.85, 0], [RX - 0.28, 1.5, 0], color=A6_GREY, stroke_width=6)
        key = Dot([RX, 1.2, 0], radius=0.07, color=TERRA)
        self.play(Create(body), Create(arc), Create(legR), Create(legL), FadeIn(key), run_time=0.5)
        a6_at(self, 1.78)
        no_l = a6_lab("no lock", RX + 0.85, 1.55, 34, left=True)
        self.play(arc.animate.shift(UP * 0.22), legL.animate.shift(UP * 0.22), legR.animate.put_start_and_end_on([RX + 0.28, 2.07, 0], [RX + 0.28, 1.5, 0]),
                  FadeIn(no_l), run_time=0.4)
        # "Gates are recorded in a status file": a terracotta dot lands beside each gate row
        a6_at(self, 2.65)
        dots = [Dot([-5.85, y, 0], radius=0.09, color=TERRA) for n, y in rows]
        self.play(LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.3), run_time=0.7)
        # "the agent could edit": an edit caret appears after the first null and blinks
        a6_at(self, 4.6)
        caret = Line([0.58, 1.15, 0], [0.58, 0.75, 0], color=INK, stroke_width=6)
        self.play(Create(caret), run_time=0.25)
        st = {"t": 0.0}

        def blink(m, dt):
            st["t"] += dt
            m.set_stroke(opacity=1.0 if (st["t"] % 0.9) < 0.55 else 0.0)
        caret.add_updater(blink)
        a6_at(self, 5.0)
        perm = a6_mono("-rw-r--r--", -6.0, -2.35, 32, left=True)
        perm_l = a6_lab("plain file, owner can write", -3.3, -2.35, 32, left=True)
        self.play(FadeIn(perm), FadeIn(perm_l), run_time=0.35)
        # "Walker's own document says...": the sentence, quoted (13 words), with its file and line
        a6_at(self, 6.25)
        QX = 2.0
        q = [a6_lab(s, QX, y, 34, left=True) for s, y in [("Gate validation is a", 0.35), ("convention the skill", -0.15),
                                                           ("follows, not code that", -0.65), ("enforces it.", -1.15)]]
        self.play(LaggedStart(*[FadeIn(x) for x in q], lag_ratio=0.25), run_time=0.75)
        a6_at(self, 7.15)
        s1 = a6_lab("zelda-gdd-workflow.md,", QX, -1.85, 32, left=True)
        s2 = a6_lab("line 66, local copy", QX, -2.3, 32, left=True)
        self.play(FadeIn(s1), FadeIn(s2), run_time=0.35)
        # "convention": the file's own note is one more sentence, not a lock (DESIGN-STATUS.json line 19)
        a6_at(self, 8.2)
        nt = a6_lab("the file's own note:", -6.0, -3.0, 34, left=True)
        nq = a6_lab("\u201cGates are signed by humans only.\u201d", -2.2, -3.0, 34, left=True)
        self.play(FadeIn(nt), FadeIn(nq), run_time=0.4)
        # "not code that enforces it": the open lock pulses
        a6_at(self, 9.9)
        self.play(Indicate(VGroup(body, arc, legR, legL, key), scale_factor=1.15, color=A6_GREY), run_time=0.7)
        done(self)


# ── B25 · not finished: a specification, no test framework, and the public version is smaller ───────────────────────
class B25_NotFinished(Scene):
    def construct(self):
        # real word times (s): command line adapter 1.06 · specification 2.56 · test framework 4.56 · And on the day 5.62 · recorded 6.48 ·
        # public version 7.16 · GitHub 8.06 · installed 8.22 · asset tool 9.48 · eleven-line 10.34 · Godot guide 12.14 · ignore file 13.26 · larger kit 14.48
        head = T("Not finished", 40).move_to([-6.0, 2.95, 0], aligned_edge=LEFT)
        self.add(head)
        # (1) the command-line adapter: a dashed cell (drawn, not built) holding the real run of `walker gdd` on this Mac
        a6_at(self, 0.85)
        box1 = a6_box(-1.85, 1.35, 8.5, 1.55, dashed=True)
        c1 = a6_mono("$ walker gdd", -5.85, 1.62, 32, left=True)
        self.play(Create(box1), FadeIn(c1), run_time=0.5)
        a6_at(self, 1.9)
        c2 = a6_mono("zsh:1: command not found: walker", -5.85, 1.06, 32, left=True)
        self.play(FadeIn(c2), run_time=0.3)
        a6_at(self, 2.4)
        s1a = a6_lab("still a", 2.85, 1.62, 36, left=True)
        s1b = a6_lab("specification", 2.85, 1.07, 36, left=True)
        cap1 = a6_lab("recorded run, this Mac, 9 October 2026", -6.0, 0.1, 32, left=True)
        self.play(FadeIn(s1a), FadeIn(s1b), FadeIn(cap1), run_time=0.35)
        # (2) no test framework: another dashed cell, with the search that backs it
        a6_at(self, 4.1)
        box2 = a6_box(-4.0, -1.0, 4.2, 0.95, dashed=True)
        c3 = a6_mono("test framework", -5.85, -1.0, 32, left=True)
        self.play(Create(box2), FadeIn(c3), run_time=0.45)
        a6_at(self, 4.6)
        s2 = a6_lab("none ships with Walker", -1.5, -1.0, 36, left=True)
        cap2 = a6_lab("repo searched, 9 October 2026", -6.0, -1.9, 32, left=True)
        self.play(FadeIn(s2), FadeIn(cap2), run_time=0.35)
        ledger = VGroup(head, box1, c1, c2, s1a, s1b, cap1, box2, c3, s2, cap2)
        # (3) "on the day this was recorded": the ledger clears, the real public page of the repo arrives
        a6_at(self, 5.6)
        self.play(FadeOut(ledger), run_time=0.45)
        a6_at(self, 6.15)
        cap = a6_img("a6_github_list.png", w=5.0, at=(-3.5, 1.5))
        self.play(FadeIn(cap), run_time=0.4)
        c_a = a6_lab("public page,", -0.5, 2.1, 38, left=True)
        c_b = a6_lab("captured 9 Oct 2026", -0.5, 1.5, 38, left=True)
        self.play(FadeIn(c_a), FadeIn(c_b), run_time=0.3)
        # (4) the two publisher runs as file counts: 11 from the committed (public) version, 54 from the local working copy
        U, X0 = 0.1, -1.7
        a6_at(self, 7.7)
        r1c = a6_lab("public, on GitHub", -6.0, -1.5, 32, left=True)
        self.play(FadeIn(r1c), run_time=0.25)
        a6_at(self, 9.3)
        seg_a = Rectangle(width=8 * U, height=0.34, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([X0 + 4 * U, -0.95, 0])
        self.play(GrowFromEdge(seg_a, LEFT), run_time=0.45)
        a6_at(self, 10.2)
        seg_b = Rectangle(width=3 * U, height=0.34, fill_color=BAR2, fill_opacity=1, stroke_width=0).move_to([X0 + 8.4 * U + 1.5 * U, -0.95, 0])
        r1a = a6_lab("asset tool, CLAUDE.md (11 lines),", -0.15, -0.75, 32, left=True)
        r1b = a6_lab("godot.md, .gitignore", -0.15, -1.2, 32, left=True)
        self.play(GrowFromEdge(seg_b, LEFT), FadeIn(r1a), run_time=0.5)
        a6_at(self, 12.0)
        self.play(FadeIn(r1b), run_time=0.3)
        a6_at(self, 13.6)
        n1 = a6_lab("11 files", -6.0, -0.95, 44, left=True)
        self.play(FadeIn(n1), run_time=0.3)
        a6_at(self, 14.4)
        n2 = a6_lab("54 files", -6.0, -2.45, 44, left=True)
        r2c = a6_lab("local copy", -6.0, -2.95, 32, left=True)
        seg_a2 = Rectangle(width=8 * U, height=0.34, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([X0 + 4 * U, -2.45, 0])
        seg_b2 = Rectangle(width=3 * U, height=0.34, fill_color=BAR2, fill_opacity=1, stroke_width=0).move_to([X0 + 8.4 * U + 1.5 * U, -2.45, 0])
        self.play(FadeIn(n2), FadeIn(r2c), FadeIn(seg_a2), FadeIn(seg_b2), run_time=0.35)
        a6_at(self, 14.9)
        gdd = a6_box(X0 + 11.8 * U + 21.5 * U, -2.45, 43 * U, 0.34, dashed=True, sw=4)
        gl = a6_lab("the /gdd skill, 43 files", 1.63, -1.95, 32)
        gl2 = a6_lab("not on the page above", 1.63, -2.95, 32)
        self.play(Create(gdd), FadeIn(gl), FadeIn(gl2), run_time=0.7)
        done(self)


# ── B26 · why use it: a rule you can check, and the habit of five verbs, each from the real record ───────────────────
class B26_TheHabit(Scene):
    def construct(self):
        # real word times (s): rule 1.06 · check 2.74 · The value 4.26 · habit 5.00 · predict 5.52 · change 6.04 · run 7.16 · keep 8.24 · leave 9.40 · human 10.62
        # phase A (to 3.9 s): a real rule from the installed instructions, checked against the running game
        a6_at(self, 0.3)
        r_lab = a6_lab("a rule", -6.0, 2.3, 40, left=True)
        qs = [a6_lab(s, -6.0, y, 36, left=True) for s, y in [("Judge progress from the", 1.35), ("running game, never", 0.75),
                                                              ("from a clean build", 0.15)]]
        self.play(FadeIn(r_lab), run_time=0.3)
        self.play(LaggedStart(*[FadeIn(x) for x in qs], lag_ratio=0.3), run_time=0.9)
        a6_at(self, 1.9)
        src = a6_mono("CLAUDE.md, line 10", -6.0, -0.55, 32, left=True)
        src2 = a6_lab("installed by Walker's publisher", -6.0, -1.1, 32, left=True)
        self.play(FadeIn(src), FadeIn(src2), run_time=0.3)
        a6_at(self, 2.1)
        fr = a6_img("a6_frame_jump.png", w=5.8, at=(3.2, 0.55))
        self.play(FadeIn(fr), run_time=0.4)
        g_lab = a6_lab("the running game", 3.2, -1.6, 36)
        g_c1 = a6_lab("recorded run, scripted input,", 3.2, -2.2, 32)
        g_c2 = a6_lab("9 October 2026", 3.2, -2.7, 32)
        a6_at(self, 2.65)
        arr = Arrow([-1.15, 0.55, 0], [0.05, 0.55, 0], buff=0, color=INK, stroke_width=6, tip_length=0.2)
        self.play(Create(arr), FadeIn(g_lab), FadeIn(g_c1), FadeIn(g_c2), run_time=0.5)
        phaseA = Group(r_lab, *qs, src, src2, fr, arr, g_lab, g_c1, g_c2)
        # "The value is the habit": the picture clears, the heading arrives
        a6_at(self, 3.9)
        self.play(FadeOut(phaseA), run_time=0.35)
        a6_at(self, 4.3)
        hab = a6_lab("The habit", -6.0, 3.0, 40, left=True)
        self.play(FadeIn(hab), run_time=0.25)
        EX = -1.3
        ys = [2.0, 1.0, -0.1, -1.35, -2.55]
        # the five verbs stand as a list first (the habit), then each row's real exhibit lands on its spoken word
        v1 = a6_lab("Predict.", -6.0, ys[0], 36, left=True)
        v2 = a6_lab("Change one thing.", -6.0, ys[1], 36, left=True)
        v3 = a6_lab("Run the real game.", -6.0, ys[2], 36, left=True)
        v4 = a6_lab("Keep the failed receipts.", -6.0, ys[3], 36, left=True)
        v5 = VGroup(a6_lab("Leave the judgment", -6.0, ys[4] + 0.27, 36, left=True), a6_lab("to the human.", -6.0, ys[4] - 0.27, 36, left=True))
        a6_at(self, 4.5)
        self.play(LaggedStart(*[FadeIn(v, shift=RIGHT * 0.15) for v in (v1, v2, v3, v4, v5)], lag_ratio=0.25), run_time=0.7)
        # 1 Predict: the three predictions, in the brief (CHANGE-BRIEF.md lines 16-21)
        cells = VGroup(*[VGroup(a6_box(EX + 0.33 + 0.75 * i, ys[0], 0.65, 0.65), T(str(i + 1), 36).move_to([EX + 0.33 + 0.75 * i, ys[0], 0]))
                         for i in range(3)])
        w1 = a6_lab("in the change brief", EX + 2.45, ys[0], 34, left=True)
        a6_at(self, 5.25)
        self.play(FadeIn(cells, scale=0.8), FadeIn(w1), run_time=0.25)
        # 2 Change one thing: the scope: drawing only, physics left alone (CHANGE-BRIEF.md 25-27)
        a6_at(self, 6.0)
        e2 = VGroup(a6_box(EX + 1.35, ys[1], 2.7, 0.75), a6_lab("drawing only", EX + 1.35, ys[1], 34),
                    a6_box(EX + 4.6, ys[1], 3.6, 0.75), a6_lab("physics left alone", EX + 4.6, ys[1], 34))
        self.play(FadeIn(e2, shift=RIGHT * 0.2), run_time=0.35)
        # 3 Run the real game: what the game itself printed when the scripted run ended (raw-log-game.txt: LEVEL COMPLETE f=205 deaths=0 time=5.63)
        a6_at(self, 7.1)
        r1 = a6_mono("LEVEL COMPLETE", EX, ys[2] + 0.28, 32, left=True)
        r2 = a6_mono("deaths=0 time=5.63", EX, ys[2] - 0.28, 32, left=True)
        r3 = a6_lab("game's own log", EX + 3.8, ys[2] + 0.28, 34, left=True)
        self.play(FadeIn(r1), FadeIn(r3), run_time=0.3)
        self.play(FadeIn(r2), run_time=0.3)
        # 4 Keep the failed receipts: the two rejected takes (FRICTIONAL.md lines 39-44, 48-50)
        a6_at(self, 8.2)
        m1 = a6_mono("343 of 540 frames", EX, ys[3] + 0.28, 32, left=True)
        m1b = a6_lab("said PASS", EX + 4.7, ys[3] + 0.28, 34, left=True)
        m2 = a6_mono("exit 0, no receipt", EX, ys[3] - 0.28, 32, left=True)
        self.play(FadeIn(m1), FadeIn(m1b), run_time=0.3)
        self.play(FadeIn(m2), run_time=0.3)
        # 5 Leave the judgment to the human: the status file still says pending (CLAWD-STATUS.json line 12)
        a6_at(self, 9.5)
        m3 = a6_mono('"human_playtest": "pending"', EX, ys[4], 32, left=True)
        self.play(FadeIn(m3), run_time=0.4)
        # the habit repeats: an arrow runs from the last row back up to the first
        a6_at(self, 10.5)
        loop = VMobject(color=A6_GREY, stroke_width=5)
        loop.set_points_as_corners([[5.75, ys[4], 0], [6.0, ys[4], 0], [6.0, ys[0], 0], [5.8, ys[0], 0]])
        tip = Arrow([5.95, ys[0], 0], [5.7, ys[0], 0], buff=0, color=A6_GREY, stroke_width=5, tip_length=0.2)
        self.play(Create(loop), run_time=0.5)
        self.play(Create(tip), run_time=0.15)
        done(self)
