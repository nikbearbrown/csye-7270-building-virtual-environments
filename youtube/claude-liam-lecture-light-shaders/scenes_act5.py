"""ACT V · Where Is the Light?  (B31, B32, B34: Manim)

Cast: the window frame (a 1920 x 1080 window drawn at 0.00375 units per pixel, origin dot at the top left, y axis pointing DOWN), the gold lamp dot,
the terracotta pixel dot, the ring. Screen-space numbers are window pixels: (960, 540) lamp, (1130, 640) pixel (measured, verify2 P/V, verify6).
"""


def a5_lamp(x, y, r=0.2):
    d = Dot([x, y, 0], radius=r, color=GOLD)
    d.set_stroke(DIM, width=3)
    return d


def a5_pixdot(x, y, r=0.16):
    d = Dot([x, y, 0], radius=r, color=TERRA)
    d.set_stroke(DIM, width=3)
    return d


def a5_put(t, anchor, side):
    """Place text t so its left ('l'), right ('r') or centre ('c') edge sits at anchor (x, y)."""
    w = t.width / 2.0
    dx = {"l": w, "r": -w, "c": 0.0}[side]
    return t.move_to([anchor[0] + dx, anchor[1], 0])


def a5_count(fmt, a, b, anchor, side):
    """UpdateFromAlphaFunc helper: replace a label by fmt(value) counting from a to b, edge-aligned at anchor."""
    def f(m, al):
        v = int(round(a + (b - a) * al))
        m.become(a5_put(T(fmt(v), 32, DIM), anchor, side))
    return f


class B31_ScreenSpace(Scene):
    def construct(self):
        title = T("Where Is the Light?", 40)
        title.move_to([-6.1 + title.width / 2, 3.1, 0])
        sc = 0.0042
        W, H = 1920 * sc, 1080 * sc
        wx, wy = -1.0, -0.3
        ox, oy = wx - W / 2, wy + H / 2          # window top-left in the scene
        P = lambda px, py: np.array([ox + px * sc, oy - py * sc, 0])
        win = Rectangle(width=W, height=H, stroke_color=INK, stroke_width=5).move_to([wx, wy, 0])
        origin = Dot(P(0, 0), radius=0.14, color=TERRA).set_stroke(DIM, width=3)
        o_lab = T("(0, 0)", 32).move_to(P(0, 0) + np.array([0.85, -0.4, 0]))
        xa = arrow([ox, oy + 0.4, 0], [ox + W + 0.2, oy + 0.4, 0], color=DIM, w=5)
        ya = arrow([ox - 0.4, oy, 0], [ox - 0.4, oy - H - 0.2, 0], color=DIM, w=5)
        xl = T("x", 32).move_to([ox + W + 0.5, oy + 0.4, 0])
        yl = T("y", 32).move_to([ox - 0.4, oy - H - 0.55, 0])
        self.play(FadeIn(title), Create(win), run_time=0.9)
        self.play(FadeIn(origin), FadeIn(o_lab), GrowArrow(xa), GrowArrow(ya), FadeIn(xl), FadeIn(yl), run_time=0.8)
        # lamp
        until(self, "Light position")
        LP, PP = P(960, 540), P(1130, 640)
        lamp = a5_lamp(*LP[:2])
        la_n = LP[:2] + np.array([-0.35, 0.28]); la_c = LP[:2] + np.array([-0.35, -0.22])
        l_name = a5_put(M("LIGHT_POSITION", 32), la_n, "r")
        l_xy = a5_put(T("(0, 0)", 32, DIM), la_c, "r")
        hz = DashedLine(P(0, 0), P(960, 0), color=DIM, stroke_width=4)
        vt = DashedLine(P(960, 0), P(960, 540), color=DIM, stroke_width=4)
        self.play(FadeOut(o_lab), FadeIn(l_name), FadeIn(l_xy), run_time=0.4)
        self.play(Create(hz), UpdateFromAlphaFunc(l_xy, a5_count(lambda v: "(%d, 0)" % v, 0, 960, la_c, "r")), run_time=0.6)
        self.play(Create(vt), FadeIn(lamp), UpdateFromAlphaFunc(l_xy, a5_count(lambda v: "(960, %d)" % v, 0, 540, la_c, "r")), run_time=0.6)
        # pixel
        until(self, "light vertex")
        pix = a5_pixdot(*PP[:2])
        pn = PP[:2] + np.array([-0.2, -0.6]); pc = PP[:2] + np.array([-0.2, -1.05])
        p_name = a5_put(M("LIGHT_VERTEX", 32), pn, "l")
        p_xy = a5_put(T("(0, 0)", 32, DIM), pc, "l")
        hz2 = DashedLine(P(0, 0), P(1130, 0), color=DIM, stroke_width=4)
        vt2 = DashedLine(P(1130, 0), P(1130, 640), color=DIM, stroke_width=4)
        self.play(hz.animate.set_opacity(0.3), vt.animate.set_opacity(0.3), FadeIn(p_name), FadeIn(p_xy), run_time=0.4)
        self.play(Create(hz2), UpdateFromAlphaFunc(p_xy, a5_count(lambda v: "(%d, 0)" % v, 0, 1130, pc, "l")), run_time=0.5)
        self.play(Create(vt2), FadeIn(pix), UpdateFromAlphaFunc(p_xy, a5_count(lambda v: "(1130, %d)" % v, 0, 640, pc, "l")), run_time=0.5)
        note = T("window 1920 x 1080", 32, DIM).move_to([4.5, 3.1, 0])
        until(self, "Both are in screen space")
        cap = T("screen space: pixels of the window, from the top left", 32).move_to([0.0, -3.0, 0])
        self.play(FadeIn(cap), FadeIn(note), run_time=0.7)
        done(self)


class B32_Subtract(Scene):
    def construct(self):
        # small window with the two dots, and a loupe that enlarges the neighbourhood
        sc = 0.0027
        W, H = 1920 * sc, 1080 * sc
        wx, wy = -3.4, 0.2
        ox, oy = wx - W / 2, wy + H / 2
        P = lambda px, py: np.array([ox + px * sc, oy - py * sc, 0])
        win = Rectangle(width=W, height=H, stroke_color=INK, stroke_width=5).move_to([wx, wy, 0])
        og = Dot(P(0, 0), radius=0.1, color=TERRA).set_stroke(DIM, width=3)
        sl, sp = a5_lamp(*P(960, 540)[:2], r=0.1), a5_pixdot(*P(1130, 640)[:2], r=0.1)
        cx0 = (P(960, 540)[0] + P(1130, 640)[0]) / 2; cy0 = (P(960, 540)[1] + P(1130, 640)[1]) / 2
        zb = Rectangle(width=0.9, height=0.7, stroke_color=DIM, stroke_width=4).move_to([cx0, cy0, 0])
        # the enlarged panel
        k = 5.0
        px, py = 3.7, 0.3
        panel = Rectangle(width=5.0, height=3.9, stroke_color=DIM, stroke_width=4).move_to([px, py, 0])
        Lp = np.array([2.0, 1.2, 0])
        Pp = Lp + np.array([170 * sc * k, -100 * sc * k, 0])
        ll = a5_lamp(*Lp[:2], r=0.2)
        pl = a5_pixdot(*Pp[:2], r=0.2)
        l_t = T("lamp", 32).move_to(Lp + np.array([0.0, 0.55, 0]))
        z_t = T("zoomed in", 32, DIM).move_to([px, py - 2.3, 0])
        c1 = Line(zb.get_corner(UR), panel.get_corner(UL), color=GHOST, stroke_width=3)
        c2 = Line(zb.get_corner(DR), panel.get_corner(DL), color=GHOST, stroke_width=3)
        self.play(Create(win), FadeIn(og), run_time=0.6)
        self.play(FadeIn(sl), FadeIn(sp), Create(zb), Create(c1), Create(c2), Create(panel), run_time=0.8)
        self.play(FadeIn(ll), FadeIn(pl), FadeIn(l_t), FadeIn(z_t), run_time=0.5)
        # the arrow lamp -> pixel
        until(self, "Subtract")
        u = (Pp - Lp) / np.linalg.norm(Pp - Lp)
        ar = arrow(Lp + u * 0.28, Pp - u * 0.3, w=7, tip=0.24)
        self.play(GrowArrow(ar), run_time=1.6)
        lab = T("pixel - lamp", 32).move_to((Lp + Pp) / 2 + np.array([0.55, 0.6, 0]))
        until(self, "an arrow from the lamp")
        self.play(FadeIn(lab), run_time=0.5)
        off = T("(170, 100)", 32, DIM).move_to(Pp + np.array([0.75, 0.55, 0]))
        self.play(FadeIn(off), run_time=0.4)
        # dimension line (below-left of the arrow) with a counting label
        until(self, "Its length")
        nrm = np.array([-u[1], u[0], 0])
        if nrm[1] > 0:
            nrm = -nrm
        o = nrm * 0.55
        a0, a1 = Lp + o, Pp + o
        dl = Line(a0, a1, color=INK, stroke_width=5)
        t0 = Line(a0 - nrm * 0.12, a0 + nrm * 0.12, color=INK, stroke_width=5)
        t1 = Line(a1 - nrm * 0.12, a1 + nrm * 0.12, color=INK, stroke_width=5)
        mid = (a0 + a1) / 2 + nrm * 1.2 + np.array([0.4, 0, 0])
        cnt = T("length 0 px", 32).move_to(mid)
        self.play(Create(dl), FadeIn(t0), FadeIn(t1), run_time=0.5)
        self.play(UpdateFromAlphaFunc(cnt, lambda m, al: m.become(T("length %d px" % int(round(197 * al)), 32).move_to(mid))), run_time=1.1)
        until(self, "That is what the length")
        cap = T("length(v): the length of a vector; of an offset, the distance", 32).move_to([0.0, -3.0, 0])
        self.play(FadeIn(cap), run_time=0.6)
        done(self)


class B34_RingFromSteps(Scene):
    def construct(self):
        sc = 0.0045
        cx, cy = -2.0, -0.1
        r1, r2, RG = 390 * sc, 450 * sc, 2.6
        gframe = Circle(radius=RG, stroke_color=GHOST, stroke_width=4).move_to([cx, cy, 0])
        gframe.set_z_index(3)
        c1 = Circle(radius=r1, stroke_color=TEAL, stroke_width=6).move_to([cx, cy, 0]); c1.set_z_index(4)
        c2 = Circle(radius=r2, stroke_color=INK, stroke_width=6).move_to([cx, cy, 0]); c2.set_z_index(4)
        lamp = Dot([cx, cy, 0], radius=0.2, color=GOLD).set_stroke(DIM, width=3); lamp.set_z_index(5)
        chip1 = VGroup(RoundedRectangle(width=3.7, height=0.8, corner_radius=0.12, stroke_color=TEAL, stroke_width=4), M("step(390, d)", 32)).move_to([3.6, 1.7, 0])
        chip2 = VGroup(RoundedRectangle(width=3.7, height=0.8, corner_radius=0.12, stroke_color=INK, stroke_width=4), M("step(450, d)", 32)).move_to([3.6, 0.2, 0])
        rl1 = T("radius 390", 32).move_to([3.6, 1.0, 0])
        rl2 = T("radius 450", 32).move_to([3.6, -0.5, 0])
        cap = T("step(edge, x): 0 below the edge, 1 from the edge up", 32).move_to([0.0, -3.05, 0])
        self.play(FadeIn(gframe), FadeIn(lamp), Create(c1), Create(c2), FadeIn(cap), run_time=1.0)
        self.play(FadeIn(chip1), FadeIn(rl1), FadeIn(chip2), FadeIn(rl2), run_time=0.7)
        # the ground splits: outside the small circle
        until(self, "the ground splits")
        A = Annulus(inner_radius=r1, outer_radius=RG, fill_color="#E2DDD1", fill_opacity=0.95, stroke_width=0).move_to([cx, cy, 0])
        A.set_z_index(1)
        out_t = T("outside", 32).move_to([cx, cy + 2.31, 0]); out_t.set_z_index(6)
        in_t = T("inside", 32).move_to([cx, cy - 0.7, 0]); in_t.set_z_index(6)
        self.play(FadeIn(A), run_time=0.6)
        self.play(FadeIn(out_t), FadeIn(in_t), run_time=0.4)
        # the second fill is subtracted
        until(self, "subtract one from the other")
        B = Annulus(inner_radius=r2, outer_radius=RG + 0.05, fill_color=STAGE, fill_opacity=1, stroke_width=0).move_to([cx, cy, 0])
        B.set_z_index(2)
        self.play(FadeOut(out_t), FadeOut(in_t), FadeIn(B), run_time=0.9)
        # the ring that is left
        until(self, "the band between")
        self.play(A.animate.set_fill(TEAL, opacity=0.85), run_time=0.5)
        rt = T("a ring", 32).move_to([3.6, -1.9, 0])
        pt = np.array([cx + 1.9 * np.cos(np.radians(-35)), cy + 1.9 * np.sin(np.radians(-35)), 0])
        ar = arrow([2.5, -1.9, 0], pt + np.array([0.25, -0.05, 0]), w=6, tip=0.2); ar.set_z_index(8)
        dot = Dot(pt, radius=0.12, color=TERRA).set_stroke(DIM, width=3); dot.set_z_index(7)
        self.play(FadeIn(rt), GrowArrow(ar), FadeIn(dot), run_time=0.5)
        done(self)
