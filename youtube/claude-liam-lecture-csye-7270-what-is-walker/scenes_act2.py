"""ACT II · The Loop and Who Decides  (B05–B07, all Manim)

One cast for the act: THE LOOP (six outlined nodes on a ring, one terracotta dot that travels it), then the same six steps as a
table of what each one produces and where it stops (the real table cells of Walker's workflow document, trimmed only with a visible
ellipsis), then the split between the agent and the human (the real README sentence cut at its semicolon).

Real material shown as itself:
- B05: frames of the REAL recorded run of the walker-claude Godot project (Godot 4.7.2 Movie Maker, scripted keyboard input,
  recorded 2026-10-09): pantry/a2_play_NNN.png are ffmpeg frames (15 per second, 960x540) of
  _conducting-series-evidence/godot-captures/walker-claude/walker-claude-jumpman-gameplay.mp4 from 0.3 s. It is the game the loop
  produces, played in the middle of the loop; it is not mapped to a step (the recording is not a play-test).
- B06: Walker docs/zelda-gdd-workflow.md lines 37-44, "Output / boundary" column.
- B07: Walker README.md lines 5-6.
Pacing: until() lands each motion on its spoken phrase (character share of the measured audio).
"""

A2P = "pantry/"
A2_FPS = 15.0
A2_NFRAMES = 93          # a2_play_001.png .. a2_play_093.png = clip time 0.3 s .. 6.5 s


def a2_lab(s, x, y, size=36, color=INK):
    return T(s, size, color).move_to([x, y, 0])


def a2_left(s, x, y, size=36, color=INK):
    """Text whose left edge sits at x (aligned_edge only; the position is an explicit coordinate)."""
    return T(s, size, color).move_to([x, y, 0], aligned_edge=LEFT)


def a2_right(s, x, y, size=36, color=INK):
    return T(s, size, color).move_to([x, y, 0], aligned_edge=RIGHT)


def a2_frame_tick(im, dt):
    """Updater: steps the real recorded frames in time (15 per second, from clip time 0.3 s)."""
    im.a2_t += dt
    k = min(A2_NFRAMES - 1, int(im.a2_t * A2_FPS) + im.a2_k0 - 1) + 1
    if k != im.a2_k:
        im.a2_k = k
        from PIL import Image
        arr = np.array(Image.open(A2P + "a2_play_%03d.png" % k).convert("RGBA"))
        im.pixel_array = arr


def a2_video(w, x, y, k0=1):
    """A moving picture of the real recording: an ImageMobject whose pixels step through the extracted frames."""
    im = ImageMobject(A2P + "a2_play_%03d.png" % k0)
    im.set_width(w)
    im.move_to([x, y, 0])
    im.a2_t, im.a2_k, im.a2_k0 = 0.0, k0, k0
    im.add_updater(a2_frame_tick)
    return im


# ───────────── the loop ring ─────────────
A2_CX, A2_CY, A2_RX, A2_RY = 0.0, -0.15, 4.0, 2.0
A2_STEPS = ["Game brief", "Build", "Play-test", "Inspect", "Revise", "Export"]
A2_ANG = [150, 90, 30, -30, -90, -150]       # clockwise from the upper left


def a2_pt(deg):
    r = np.radians(deg)
    return np.array([A2_CX + A2_RX * np.cos(r), A2_CY + A2_RY * np.sin(r), 0.0])


def a2_arc(d0, d1, color=INK, sw=6):
    """The ring between two angles (degrees, running clockwise: d0 > d1)."""
    return ParametricFunction(lambda t: a2_pt(t), t_range=[d1, d0], color=color, stroke_width=sw).reverse_points()


# ── B05 · the six steps as one loop ──────────────────────────────────────────────────────────────────────────────
class B05_TheLoop(Scene):
    def construct(self):
        title = a2_lab("The Loop and Who Decides", 0.0, 2.95, 40)
        self.add(title)
        ring = Ellipse(width=2 * A2_RX, height=2 * A2_RY, color=DIM, stroke_width=4).move_to([A2_CX, A2_CY, 0])
        self.add(ring)
        # the centre starts as the real GAME-BRIEF.md (its promise line, verbatim); the real recorded run replaces it on "Build"
        page = RoundedRectangle(width=5.4, height=2.7, corner_radius=0.12, fill_opacity=0, stroke_color=DIM,
                                stroke_width=4).move_to([0, A2_CY, 0])
        fname = M("GAME-BRIEF.md", 32).move_to([-2.45, A2_CY + 0.9, 0], aligned_edge=LEFT)
        q1 = a2_lab("I can see why that failed,", 0.0, A2_CY + 0.05, 34)
        q2 = a2_lab("and I want one more try.", 0.0, A2_CY - 0.5, 34)
        ln = a2_right("line 11", 2.45, A2_CY - 0.95, 32, DIM)
        card = VGroup(page, fname, q1, q2, ln)
        self.add(card)
        vid = a2_video(4.6, 0.0, A2_CY, k0=20)
        cap = a2_right("recorded run, scripted input", 6.0, -3.0, 32)      # appears with the recording
        # labels: beside their nodes (left nodes: to the left; right nodes: to the right; top above; bottom below)
        labs = VGroup(
            a2_right("Game brief", a2_pt(150)[0] - 0.45, a2_pt(150)[1], 36),
            a2_lab("Build", 0.0, a2_pt(90)[1] + 0.5, 36),
            a2_left("Play-test", a2_pt(30)[0] + 0.45, a2_pt(30)[1], 36),
            a2_left("Inspect", a2_pt(-30)[0] + 0.45, a2_pt(-30)[1], 36),
            a2_lab("Revise", 0.0, a2_pt(-90)[1] - 0.5, 36),
            a2_right("Export", a2_pt(-150)[0] - 0.45, a2_pt(-150)[1], 36))
        nodes = VGroup(*[Circle(radius=0.17, stroke_color=INK, stroke_width=5, fill_color=STAGE, fill_opacity=1).move_to(a2_pt(a))
                         for a in A2_ANG])
        self.play(LaggedStart(*[Create(n) for n in nodes], lag_ratio=0.3), run_time=1.3)     # "six steps": six nodes, one by one
        self.play(FadeIn(labs), run_time=0.4)
        until(self, "Game brief.", lead=0.3)                    # the dot arrives on "Game brief"
        dot = Dot(a2_pt(150), radius=0.14, color=TERRA).set_z_index(10)
        self.play(FadeIn(dot, scale=0.5), nodes[0].animate.set_fill(INK, opacity=1), run_time=0.2)
        # (midpoint: six nodes, six labels, the game playing in the middle, the dot on "Game brief")
        marks = [("Build", 150, 90), ("Play-test", 90, 30), ("Inspect", 30, -30), ("Revise", -30, -90), ("Export", -90, -150)]
        for i, (ph, a0, a1) in enumerate(marks):
            until(self, ph + ".", lead=0.45)
            path = a2_arc(a0, a1)
            drawn = path.copy()
            extra, rt = [], 0.35
            if i == 0:                                           # "Build": the brief gives way to the game it produced
                rt = guard(self, 0.35)                           # (settle the midpoint wait BEFORE the video is staged)
                self.add(vid)
                extra = [FadeOut(card), FadeIn(cap)]
            self.play(MoveAlongPath(dot, path), Create(drawn), nodes[i + 1].animate.set_fill(INK, opacity=1), *extra,
                      run_time=rt, rate_func=smooth)
        closing = a2_arc(-150, -210)                             # the loop closes: Export back round to the brief
        self.play(Create(closing), run_time=0.2)

        done(self)


# ── B06 · what each step produces, and where it stops ────────────────────────────────────────────────────────────
A2_ROWS = [("Game brief", "Human-reviewed target revision … authorized build"),
           ("Build", "Runnable project … not a completion claim"),
           ("Play-test", "Recorded attempts, … and human feedback"),
           ("Inspect", "Defects, … prioritized next change"),
           ("Revise", "New revision, … approvals may become stale"),
           ("Export", "Versioned package and evidence;")]
A2_RY0, A2_RSTEP = 1.8, 0.72           # first row's y, row spacing
A2_XS, A2_XC, A2_XBAR = -6.0, -3.6, 6.15


class B06_OutputAndBoundary(Scene):
    def construct(self):
        ys = [A2_RY0 - i * A2_RSTEP for i in range(6)]
        h1 = a2_left("Stage", A2_XS, 2.65, 34)
        h2 = a2_left("Output / boundary", A2_XC, 2.65, 34)
        rule = Line([-6.1, 2.3, 0], [6.1, 2.3, 0], color=DIM, stroke_width=4)
        steps = VGroup(*[a2_left(s, A2_XS, y, 32) for (s, _), y in zip(A2_ROWS, ys)])
        cells = VGroup(*[a2_left(c, A2_XC, y, 32) for (_, c), y in zip(A2_ROWS, ys)])
        self.play(FadeIn(h1), FadeIn(h2), Create(rule), run_time=0.4)
        self.play(LaggedStart(*[FadeIn(VGroup(s, c), shift=UP * 0.1) for s, c in zip(steps, cells)], lag_ratio=0.2), run_time=0.9)
        until(self, "stops somewhere", lead=0.5)                # "and stops somewhere": a stop bar closes each row's boundary
        bars = VGroup(*[Line([A2_XBAR, y - 0.27, 0], [A2_XBAR, y + 0.27, 0], color=INK, stroke_width=9) for y in ys])
        self.play(LaggedStart(*[Create(b) for b in bars], lag_ratio=0.2), run_time=0.8)
        until(self, "Build produces", lead=0.25)                # the Build row comes forward, the others step back
        mark = Dot([-6.15, ys[1], 0], radius=0.09, color=TERRA)
        others = [i for i in range(6) if i != 1]
        self.play(*[steps[i].animate.set_color(DIM) for i in others], *[cells[i].animate.set_color(DIM) for i in others],
                  FadeIn(mark, scale=0.5), run_time=0.4)
        # (midpoint: the Build row in ink with its dot, the other five rows grey, a stop bar on every row)
        until(self, "Export produces", lead=0.25)               # the Export row comes forward
        mark2 = Dot([-6.15, ys[5], 0], radius=0.09, color=TERRA)
        self.play(steps[1].animate.set_color(DIM), cells[1].animate.set_color(DIM), steps[5].animate.set_color(INK),
                  cells[5].animate.set_color(INK), FadeOut(mark), FadeIn(mark2, scale=0.5), run_time=0.4)
        until(self, "Publishing", lead=0.2)                     # "Publishing is a separate step": an arrow runs on and stops at a wall
        arr = Arrow([A2_XBAR - 0.45, ys[5] - 0.1, 0], [A2_XBAR - 0.45, -2.35, 0], buff=0, color=INK, stroke_width=6,
                    tip_length=0.28, max_tip_length_to_length_ratio=0.5)
        wall = Line([-3.7, -2.5, 0], [6.1, -2.5, 0], color=INK, stroke_width=9)
        sep = a2_left("publication remains separate", -3.7, -2.95, 32)
        self.play(GrowArrow(arr), Create(wall), FadeIn(sep), run_time=0.7)
        done(self)


# ── B07 · the split, in one line ──────────────────────────────────────────────────────────────────────────────────
class B07_TheSplit(Scene):
    def construct(self):
        top = Line([-6.1, 3.05, 0], [6.1, 3.05, 0], color=INK, stroke_width=6)
        self.play(Create(top), run_time=0.6)                    # "stated in one line": one line
        until(self, "in one line", lead=-0.2)
        mid = Line([0, 3.05, 0], [0, -2.55, 0], color=INK, stroke_width=6)
        self.play(Create(mid), run_time=0.6)                    # ... and it splits
        until(self, "The agent helps", lead=0.2)
        robot = SVGMobject(A2P + "a2_robot_face.svg", stroke_color=INK, stroke_width=5, fill_opacity=0).scale_to_fit_height(1.6)
        robot.move_to([-3.2, 1.2, 0])
        h_a = a2_lab("Agent", -3.2, 2.45, 40)
        self.play(FadeIn(h_a), Create(robot), run_time=0.5)
        l1 = a2_lab("helps execute", -3.2, -0.25, 38)
        l2 = a2_lab("and check changes", -3.2, -0.9, 38)
        until(self, "execute and check", lead=0.15)
        ck = check(-0.7, -0.9, s=0.2, w=7)
        self.play(FadeIn(l1), FadeIn(l2), run_time=0.35)
        self.play(Create(ck), run_time=0.3)
        # (midpoint: the agent side complete: icon, "helps execute and check changes", a check; the human side still empty)
        until(self, "The human decides", lead=0.2)
        face = ImageMobject(A2P + "a2_professor_bear_avatar.png").scale_to_fit_height(1.6).move_to([3.2, 1.2, 0])
        h_h = a2_lab("Human", 3.2, 2.45, 40)
        self.play(FadeIn(h_h), FadeIn(face), run_time=0.5)
        r1 = VGroup(a2_lab("decides what", 3.2, -0.25, 38), a2_lab("the game should be", 3.2, -0.9, 38))
        self.play(FadeIn(r1), run_time=0.35)
        until(self, "whether it feels right", lead=0.35)
        r2 = VGroup(a2_lab("and whether", 3.2, -1.65, 38), a2_lab("it feels right", 3.2, -2.3, 38))
        spark = Dot([0.4, -2.3, 0], radius=0.1, color=TERRA)
        self.play(FadeIn(r2), FadeIn(spark, scale=0.5), run_time=0.4)
        src = a2_lab("Walker README, lines 5 to 6", -3.2, -2.9, 32, DIM)
        self.play(FadeIn(src), run_time=0.3)
        done(self)
