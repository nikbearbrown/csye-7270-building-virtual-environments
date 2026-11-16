"""ACT V · Which Renderer?  (B40, B41; Manim)

B40 two lanes: the same chip 0.5 goes through "linear to sRGB" in Forward+ and comes out 0.74; straight through in Compatibility and stays 0.50; a small plot
(the diagonal against the standard screen curve) shows the lift once. B41 one channel on one line (red: rust 0.40, green 0.12): one dot, two midpoints.
Numbers are the measured ones in FACTCHECK.md (Apple M4 Pro, Godot 4.7.2); the curve is the standard sRGB encoding, written inline.
"""


def a5_at(self, t_abs):
    gap = t_abs - _elapsed(self)
    if gap > 0.03:
        self.wait(gap)


def a5_dot(x=0.0, y=0.0, r=0.16):
    return Dot([x, y, 0], radius=r, color=TERRA).set_stroke(DIM, width=3)


def a5_srgb(v):
    return 12.92 * v if v <= 0.0031308 else 1.055 * v ** (1 / 2.4) - 0.055


def a5_chip(text, x, y, w=1.3):
    b = box(x, y, w, 0.7, color=INK, sw=4, fill=CARD)
    t = T(text, 32).move_to([x, y, 0])
    g = VGroup(b, t)
    g.b = b; g.t = t
    return g


# ═════════════════════════════ B40 · two lanes ═════════════════════════════
class B40_TwoLanes(Scene):
    def construct(self):
        # the plot, once: diagonal (Compatibility) against the screen curve (Forward+)
        px, py, pw, ph = -0.4, 2.15, 2.1, 1.75
        x0, y0 = px - pw / 2, py - ph / 2
        P = lambda u, v: np.array([x0 + u * pw, y0 + v * ph, 0])
        axes = VGroup(Line(P(0, 0), P(1, 0), color=INK, stroke_width=5), Line(P(0, 0), P(0, 1), color=INK, stroke_width=5))
        diag = Line(P(0, 0), P(1, 1), color=DIM, stroke_width=6)
        curve = VMobject(stroke_color=INK, stroke_width=6).set_points_smoothly([P(u, a5_srgb(u)) for u in np.linspace(0.0, 1.0, 60)])
        k1 = VGroup(Line([1.3, 2.75, 0], [1.75, 2.75, 0], color=INK, stroke_width=6), T("Forward+", 32).move_to([3.15, 2.75, 0]))
        k2 = VGroup(Line([1.3, 1.95, 0], [1.75, 1.95, 0], color=DIM, stroke_width=6), T("Compatibility", 32).move_to([3.45, 1.95, 0]))
        # lanes
        ly1, ly2 = 0.2, -0.95
        n1 = T("Forward+", 32).move_to([-5.0, ly1, 0])
        n2 = T("Compatibility", 32).move_to([-4.65, ly2, 0])
        sx, ex = -2.6, 4.9
        track1 = arrow([sx - 0.6, ly1 - 0.52, 0], [ex + 0.6, ly1 - 0.52, 0], color=GHOST, w=6)
        track2 = arrow([sx - 0.6, ly2 - 0.52, 0], [ex + 0.6, ly2 - 0.52, 0], color=GHOST, w=6)
        blk = box(0.9, ly1, 3.5, 0.85, color=INK, sw=4)
        blkt = T("linear to sRGB", 32).move_to([0.9, ly1, 0])
        cap1 = T("linear: the scale light adds up on, in a straight line", 32).move_to([0.0, -1.95, 0])
        cap2 = T("sRGB: the scale a color picker's numbers use, spaced for the eye", 32).move_to([0.0, -2.45, 0])
        credit = T("measured · Apple M4 Pro · Godot 4.7.2", 32).move_to([0.0, -3.15, 0])
        c1 = a5_chip("0.5", sx, ly1)
        c2 = a5_chip("0.5", sx, ly2)
        self.add(axes, diag, curve, k1, k2, n1, n2, track1, track2, blk, blkt, cap1, cap2, credit)
        self.wait(0.3)
        self.play(FadeIn(c1), FadeIn(c2), run_time=0.5)
        # Forward+: through the block, out as 0.74; the plot dot rises with it
        ddot = a5_dot(*P(0.5, 0.5)[:2])
        gdot = Circle(radius=0.14, stroke_color=DIM, stroke_width=5).move_to(P(0.5, 0.5))
        self.add(gdot)
        self.play(FadeIn(ddot), run_time=0.3)
        until(self, "Forward Plus", lead=0.0)
        self.play(c1.animate.move_to([-1.6, ly1, 0]), run_time=0.7)
        c1n = a5_chip("0.74", 3.4, ly1)
        self.play(FadeOut(c1, shift=RIGHT * 0.6), run_time=0.4)
        self.play(FadeIn(c1n, shift=RIGHT * 0.3), ddot.animate.move_to(P(0.5, a5_srgb(0.5))), run_time=0.5)
        self.play(c1n.animate.move_to([ex, ly1, 0]), run_time=0.6)
        # Compatibility: straight through, still 0.50
        until(self, "Compatibility skips", lead=0.2)
        self.play(c2.animate.move_to([ex, ly2, 0]), run_time=1.4)
        c2n = a5_chip("0.50", ex, ly2)
        self.play(ReplacementTransform(c2, c2n), run_time=0.4)
        done(self)


# ═════════════════════════════ B41 · two midpoints ═════════════════════════════
class B41_TwoMidpoints(Scene):
    def construct(self):
        L, R, y = -4.5, 4.5, 0.4
        X = lambda v: L + (0.40 - v) / 0.28 * (R - L)            # red 0.40 at left, 0.12 at right
        head = T("red channel", 32).move_to([0.0, 2.7, 0])
        line = Line([L, y, 0], [R, y, 0], color=DIM, stroke_width=7)
        sw1 = Square(side_length=0.45, stroke_color=INK, stroke_width=3).set_fill("#66291A", opacity=1).move_to([L, y, 0])
        sw2 = Square(side_length=0.45, stroke_color=INK, stroke_width=3).set_fill("#1FB885", opacity=1).move_to([R, y, 0])
        e1 = T("rust 0.40", 32).move_to([L, y - 0.65, 0])
        e2 = T("green 0.12", 32).move_to([R - 0.2, y - 0.65, 0])
        cred = T("measured 0.26 and 0.30 · Apple M4 Pro · Godot 4.7.2", 32).move_to([0.0, -3.05, 0])
        self.add(head, line, e1, e2, cred)
        self.play(FadeIn(sw1), FadeIn(sw2), run_time=0.4)
        dot = a5_dot(L, y)
        self.play(FadeIn(dot), run_time=0.3)
        # the tag by the two ends, on "marked source color"
        until(self, "marked source color", lead=0.3)
        tag = T("source_color: numbers are sRGB: convert to light first", 32).move_to([0.0, -2.35, 0])
        self.play(FadeIn(tag), run_time=0.5)
        # Forward+: linear light first, the midpoint lands at 0.30
        a5_at(self, 3.6)
        self.play(dot.animate.move_to([X(0.30), y, 0]), run_time=0.9)
        pf = Triangle(color=INK, fill_opacity=1).scale(0.16).rotate(PI).move_to([X(0.30), y + 0.35, 0])
        self.play(FadeIn(pf, shift=DOWN * 0.3), run_time=0.3)
        lf1 = T("Forward+", 32).move_to([X(0.30), y + 1.55, 0])
        lf2 = T("linear light 0.30", 32).move_to([X(0.30), y + 1.0, 0])
        self.play(FadeIn(lf1), FadeIn(lf2), run_time=0.4)
        # Compatibility: the numbers as written, midpoint 0.26
        until(self, "Compatibility blends", lead=0.2)
        self.play(dot.animate.move_to([X(0.26), y, 0]), run_time=0.9)
        pc = Triangle(color=DIM, fill_opacity=1).scale(0.16).move_to([X(0.26), y - 0.35, 0])
        self.play(FadeIn(pc, shift=UP * 0.3), run_time=0.3)
        cm1 = T("Compatibility", 32).move_to([X(0.26) + 0.6, y - 1.1, 0])
        cm2 = T("as written 0.26", 32).move_to([X(0.26) + 0.6, y - 1.55, 0])
        self.play(FadeIn(cm1), FadeIn(cm2), run_time=0.4)
        until(self, "One dial, two midpoints", lead=0.0)
        gap = Line([X(0.30), y, 0], [X(0.26), y, 0], color=DIM)
        self.play(FadeIn(ring(gap, pad=0.22)), run_time=0.5)
        done(self)
