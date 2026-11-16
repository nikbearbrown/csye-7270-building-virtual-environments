"""ACT V · Angle from a Position  (B31, B32, B34, B37; Manim)

Cast: the circle with the pixel dot, SCREEN orientation (y down): a screen angle s puts a point at c + r*(cos s, -sin s) in scene coordinates;
the arc tangent of a pixel p = (x, y) with y down is atan2(y, x). Terracotta only as dots, thick arcs and rings.
"""


def a5_pt(c, r, s):
    return np.array([c[0] + r * np.cos(s), c[1] - r * np.sin(s), 0.0])


def a5_axes(c, r):
    """Small grey axes, the screen way: x to the right, y pointing DOWN."""
    ax = arrow(c + np.array([0.0, 0.0, 0.0]), c + np.array([r + 0.5, 0, 0]), color=DIM, w=4, tip=0.2)
    ay = arrow(c, c + np.array([0, -(r + 0.3), 0]), color=DIM, w=4, tip=0.2)
    lx = T("x", 32, DIM).move_to(c + np.array([r + 0.85, 0, 0]))
    ly = T("y", 32, DIM).move_to(c + np.array([0.4, -(r + 0.15), 0]))
    return VGroup(ax, ay, lx, ly)


def a5_dot(p, r=0.17):
    return Dot(p, radius=r, color=TERRA).set_stroke(DIM, width=3)


# ═════════════════════════════ B31 · two ways ═════════════════════════════
class B31_TwoWays(Scene):
    def construct(self):
        title = T("Angle from a Position", 40).to_corner(UL, buff=0.95)
        c = np.array([0.5, 0.1, 0.0]); r = 1.7; s0 = 0.61
        circ = Circle(radius=r, stroke_color=INK, stroke_width=5).move_to(c)
        axes = a5_axes(c, r)
        dot = a5_dot(a5_pt(c, r, s0))
        radial = Line(c, a5_pt(c, r, s0), color=DIM, stroke_width=4)
        arc = Arc(radius=1.1, start_angle=0, angle=-s0, arc_center=c, color=TERRA, stroke_width=11)
        arc_back = Arc(radius=1.1, start_angle=0, angle=-s0, arc_center=c, color=DIM, stroke_width=18, stroke_opacity=0.5)
        fwd = arrow([-0.2, 2.35, 0], [4.6, 2.35, 0], color=INK, w=7)
        fwd_l = T("angle in, position out", 32).move_to([2.2, 2.9, 0])
        bwd = arrow([4.6, -2.5, 0], [-0.2, -2.5, 0], color=INK, w=7)
        bwd_l = T("position in, angle out", 32).move_to([2.2, -2.98, 0])
        q = T("?", 40).move_to(a5_pt(c, r + 0.75, s0 / 2))
        word = T("angle", 32).move_to(a5_pt(c, r + 0.85, s0 / 2))

        self.add(title, circ, axes, radial, dot)
        self.wait(0.4)
        self.play(GrowArrow(fwd), FadeIn(fwd_l), run_time=0.6)
        self.play(FadeIn(arc_back), Create(arc), run_time=1.4, rate_func=smooth)
        until(self, "A pixel knows")
        self.play(GrowArrow(bwd), FadeIn(bwd_l), run_time=0.7)
        self.play(FadeIn(q), run_time=0.4)
        until(self, "What angle")
        self.play(ReplacementTransform(q, word), run_time=0.5)
        done(self)


# ═════════════════════════════ B32 · arc tangent: two sides in, angle out ═════════════════════════════
class B32_AtanIdea(Scene):
    def construct(self):
        S = 5.0
        O = np.array([-5.0, 1.5, 0.0])
        A = O + np.array([0.5 * S, 0, 0])
        P = O + np.array([0.5 * S, -0.35 * S, 0])
        hyp = Line(O, P, color=INK, stroke_width=7)
        adj = Line(O, A, color=INK, stroke_width=7)
        opp = Line(A, P, color=INK, stroke_width=7)
        mid_dot = Dot(O, radius=0.1, color=DIM)
        pix = a5_dot(P)
        arc = Arc(radius=1.1, start_angle=0, angle=-np.arctan2(0.35, 0.5), arc_center=O, color=TERRA, stroke_width=11)
        arc_back = Arc(radius=1.1, start_angle=0, angle=-np.arctan2(0.35, 0.5), arc_center=O, color=DIM, stroke_width=18, stroke_opacity=0.5)
        l_adj = T("adjacent", 32).move_to(O + np.array([1.25, 0.45, 0]))
        l_opp = T("opposite", 32).move_to(A + np.array([1.05, -0.65, 0]))
        l_ang = T("angle?", 32).move_to(O + np.array([0.55, -1.3, 0]))
        bx = box(2.9, 0.9, 3.3, 1.1, color=INK, sw=5)
        bt = T("arc tangent", 32).move_to(bx.get_center())
        t_opp = T("0.35", 32).move_to(A + np.array([0.9, -1.45, 0]))
        t_adj = T("0.5", 32).move_to(A + np.array([0.7, 0.45, 0]))
        out = arrow([2.9, 0.3, 0], [2.9, -1.0, 0], color=INK, w=7)
        out_l = T("angle", 32).move_to([4.15, -0.65, 0])
        res = T("0.61 rad", 32).move_to(l_ang.get_center())
        down = T("down", 32).move_to(l_opp.get_center())
        across = T("across", 32).move_to(l_adj.get_center())

        self.add(mid_dot, adj, opp, hyp)
        until(self, "Tangent was", lead=0.0)
        self.play(FadeIn(pix), FadeIn(l_adj), FadeIn(l_opp), run_time=0.6)
        self.play(FadeIn(arc_back), Create(arc), FadeIn(l_ang), run_time=0.7)
        until(self, "Arc tangent undoes")
        self.play(FadeIn(bx), FadeIn(bt), run_time=0.5)
        # the two numbers travel into the box, the angle comes out
        self.play(FadeIn(t_opp), FadeIn(t_adj), run_time=0.3)
        self.play(t_opp.animate.move_to([0.65, 0.65, 0]), t_adj.animate.move_to([0.65, 1.15, 0]), run_time=0.9, rate_func=smooth)
        self.play(FadeOut(t_opp), FadeOut(t_adj), GrowArrow(out), FadeIn(out_l), run_time=0.5)
        self.play(ReplacementTransform(l_ang, res), run_time=0.5)
        until(self, "For a pixel")
        self.play(ReplacementTransform(l_adj, across), ReplacementTransform(l_opp, down), run_time=0.6)
        done(self)


# ═════════════════════════════ B34 · the compass and the seam ═════════════════════════════
def a5_atan(s):
    """arc tangent of the dot at screen angle s: atan2(sin s, cos s) with y down (what the shader sees)."""
    return float(np.arctan2(np.sin(s), np.cos(s)))


class B34_Compass(Scene):
    def construct(self):
        c = np.array([-1.6, 0.0, 0.0]); r = 2.3
        s = ValueTracker(0.0)
        circ = Circle(radius=r, stroke_color=INK, stroke_width=5).move_to(c)
        axes = a5_axes(c, r)
        dot = always_redraw(lambda: a5_dot(a5_pt(c, r, s.get_value()), 0.2))
        rb = box(3.9, 0.1, 3.5, 2.4, color=INK, sw=4)
        rt = T("arc tangent", 32).move_to([3.9, 0.85, 0])
        readout = always_redraw(lambda: T("%.2f" % (a5_atan(s.get_value()) + 0.0 if abs(a5_atan(s.get_value())) > 0.005 else 0.0), 56).move_to([3.9, -0.15, 0]))
        flash = ring(rb, pad=0.1)
        seam = Line(c + np.array([-r - 0.3, 0, 0]), c + np.array([-r + 0.3, 0, 0]), color=DIM, stroke_width=14)
        seam_l = T("seam", 32).move_to(c + np.array([-r - 0.95, 0.5, 0]))
        ghost = lambda a: Dot(a5_pt(c, r, a), radius=0.09, color=DIM)

        self.add(circ, axes, rb, rt, readout, dot)
        until(self, "Straight down")
        self.play(s.animate.set_value(np.pi / 2), run_time=1.0)
        self.add(ghost(np.pi / 2))
        until(self, "Straight left")
        self.play(s.animate.set_value(np.pi - 0.002), run_time=1.2, rate_func=smooth)
        self.play(FadeIn(seam), FadeIn(seam_l), run_time=0.4)
        until(self, "nearly minus pi")
        self.play(FadeIn(flash), s.animate.set_value(np.pi + 0.002), run_time=0.3, rate_func=linear)
        self.play(FadeOut(flash), run_time=0.4)
        until(self, "Past the wrap")
        self.play(s.animate.set_value(1.5 * np.pi), run_time=0.9)
        self.add(ghost(1.5 * np.pi))
        until(self, "straight up is")
        self.play(s.animate.set_value(2 * np.pi), run_time=0.9)
        done(self)


# ═════════════════════════════ B37 · one pixel by hand ═════════════════════════════
class B37_WorkedPixel(Scene):
    def construct(self):
        sq = 3.2; c = np.array([-4.3, 1.0, 0.0])
        frame = Square(side_length=sq, stroke_color=INK, stroke_width=5).move_to(c)
        cross = VGroup(Line(c + np.array([-sq / 2, 0, 0]), c + np.array([sq / 2, 0, 0]), color=DIM, stroke_width=3),
                       Line(c + np.array([0, -sq / 2, 0]), c + np.array([0, sq / 2, 0]), color=DIM, stroke_width=3))
        mid = Dot(c, radius=0.09, color=DIM)
        pp = c + np.array([-0.3, 0.3, 0]) * (sq / 2)
        dot = a5_dot(pp)
        pl = T("p", 36).move_to(pp + np.array([-0.4, 0.3, 0]))
        head = M("p = (-0.3, -0.3)", 32).move_to([-2.2 + 2.0, 2.6, 0]); head.move_to([-2.2 + head.width / 2, 2.6, 0])
        L = [M("atan(-0.3, -0.3) = -3 * PI / 4", 32), M("÷ TAU = -0.375", 32), M("+ 0.5 = 0.125", 32)]
        for i, t in enumerate(L):
            t.move_to([-2.2 + t.width / 2, 1.3 - 0.95 * i, 0])
        rs = ramp_strip(width=4.0, x=-3.9, y=-2.2, labels=True)
        mk = ramp_marker(rs, 0.125, r=0.18)
        eighth = T("1/8", 32).move_to([rs.x0 + rs.width_s * 0.125, -1.6, 0])

        self.add(frame, cross, mid)
        self.play(FadeIn(dot, scale=0.5), FadeIn(pl), FadeIn(head), run_time=0.6)
        self.play(FadeIn(rs), run_time=0.4)
        until(self, "Arc tangent says")
        self.play(FadeIn(L[0], shift=RIGHT * 0.2), run_time=0.7)
        until(self, "Divide by tau")
        self.play(FadeIn(L[1], shift=RIGHT * 0.2), run_time=0.6)
        until(self, "Add one half")
        self.play(FadeIn(L[2], shift=RIGHT * 0.2), run_time=0.6)
        until(self, "One eighth")
        self.play(FadeIn(mk, scale=0.5), FadeIn(eighth), run_time=0.5)
        done(self)
