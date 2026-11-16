"""ACT II · Angle In, Position Out  (B06, B07, B09-B15, all Manim; B08 is Remotion)

One cast for the act: the unit circle drawn ON PAPER (y up, angles counterclockwise), the terracotta dot, the triangle inside it,
and the plot beside it. Everything is a drawing and says so ('on paper'). Real numbers only: cos 30 = 0.87, sin 30 = 0.50,
0.6 x cos 30 = 0.52, 0.6 x sin 30 = 0.30, 6.28, sin(30.0) = -0.99, sin(radians(30.0)) = 0.50 (verify-math.gd, Lab 21).
"""

A2_PALE = "#9A8F7A"      # the cosine curve: a lighter grey-brown (mid-tone, outside the text-like grey band)


def a2_d(deg):
    a = np.radians(deg)
    return np.array([np.cos(a), np.sin(a), 0.0])


def a2_dot(p, r=0.17):
    return Dot(np.array(p, dtype=float), radius=r, color=TERRA).set_stroke(DIM, width=3)


def a2_arcmark(c, deg, rad=0.7):
    """A thick terracotta arc (never a wedge) over a grey backing."""
    a = max(float(deg), 0.5)
    back = Arc(radius=rad, start_angle=0, angle=np.radians(a), arc_center=c, stroke_color=DIM, stroke_width=17, stroke_opacity=0.55)
    arc = Arc(radius=rad, start_angle=0, angle=np.radians(a), arc_center=c, stroke_color=TERRA, stroke_width=10)
    return VGroup(back, arc)


def a2_foot(c, r, deg):
    return c + np.array([r * np.cos(np.radians(deg)), 0.0, 0.0])


def a2_vleg(c, r, deg, color=INK, w=5):
    return DashedLine(c + r * a2_d(deg), a2_foot(c, r, deg), color=color, stroke_width=w, dash_length=0.12)


def a2_hleg(c, r, deg, color=INK, w=8):
    return Line(c, a2_foot(c, r, deg), color=color, stroke_width=w)


def a2_rt(c, r, deg, s=0.22):
    f = a2_foot(c, r, deg)
    m = VMobject(stroke_color=DIM, stroke_width=4)
    m.set_points_as_corners([f + [-s, 0, 0], f + [-s, s, 0], f + [0, s, 0]])
    return m


def a2_axes(c, ext, extv=None):
    extv = ext if extv is None else extv
    return VGroup(Line(c + [-ext, 0, 0], c + [ext, 0, 0], color=DIM, stroke_width=3, stroke_opacity=0.6),
                  Line(c + [0, -extv, 0], c + [0, extv, 0], color=DIM, stroke_width=3, stroke_opacity=0.6))


def a2_label_beside(txt, mid, n, pad=0.2):
    """A label centred off a point along unit normal n, clear of the line."""
    off = n * (pad + abs(n[0]) * txt.width / 2 + abs(n[1]) * txt.height / 2)
    return txt.move_to(mid + off)


_A2_CW = {}


def a2_cw(size=32):
    if size not in _A2_CW:
        _A2_CW[size] = M("MMMMMMMMMM", size).width / 10
    return _A2_CW[size]


def a2_mline(s, x, y, size=32, align="left", color=INK):
    """A monospace line placed token by token at explicit character positions (Pango drops single spaces here). Returns a VGroup of tokens."""
    import re
    cw = a2_cw(size)
    xl = x if align == "left" else x - len(s) * cw / 2
    toks = []
    for m in re.finditer(r"\S+", s):
        t = M(m.group(0), size, color)
        t.move_to([xl + (m.start() + len(m.group(0)) / 2) * cw, y, 0])
        toks.append(t)
    return VGroup(*toks)


def a2_plot_static(cy, x0=-2.0, W=6.4, R=1.4):
    """The plot of the act: angle along the bottom, 'height' up the side, a faint zero line. Returns (group, px(theta), py(value))."""
    yb = cy - R - 0.3
    px = lambda th: x0 + th / (2 * np.pi) * W
    py = lambda v: cy + v * R
    g = VGroup(Line([x0, yb, 0], [x0, cy + R + 0.3, 0], color=INK, stroke_width=5),
               Line([x0, yb, 0], [x0 + W, yb, 0], color=INK, stroke_width=5),
               DashedLine([x0, cy, 0], [x0 + W, cy, 0], color=DIM, stroke_width=3, dash_length=0.12))
    for th, s in [(np.pi / 2, "π/2"), (np.pi, "π"), (3 * np.pi / 2, "3π/2"), (2 * np.pi, "τ")]:
        g.add(Line([px(th), yb, 0], [px(th), yb - 0.13, 0], color=DIM, stroke_width=4))
        g.add(T(s, 32).move_to([px(th), yb - 0.48, 0]))
    h = T("height", 32).rotate(PI / 2).move_to([x0 - 0.5, cy + 0.85, 0])
    g.add(h)
    g.add(T("angle", 32, DIM).move_to([x0 + W / 2, yb - 1.05, 0]))
    return g, px, py


def a2_curve(fn, px, py, color, th0=0.0, th1=2 * np.pi, n=90, w=7):
    pts = [np.array([px(t), py(fn(t)), 0]) for t in np.linspace(th0, th1, n)]
    m = VMobject(stroke_color=color, stroke_width=w)
    m.set_points_smoothly(pts)
    return m


class B06_UnitCircle(Scene):
    def construct(self):
        c = np.array([0.0, -0.5, 0.0]); r = 2.2
        title = T("Angle In, Position Out", 40)
        title.move_to([-6.0 + title.width / 2, 2.95, 0])
        cap = T("on paper", 32, DIM).move_to([5.0, -2.85, 0])
        axes = a2_axes(c, r + 0.6, r + 0.45)
        circ = Circle(radius=r, stroke_color=INK, stroke_width=5).move_to(c)
        self.play(Create(circ), Create(axes), FadeIn(title), FadeIn(cap), run_time=1.0)
        tr = ValueTracker(0)
        rad = always_redraw(lambda: Line(c, c + r * a2_d(tr.get_value()), color=INK, stroke_width=6))
        arc = always_redraw(lambda: a2_arcmark(c, tr.get_value()))
        self.add(rad, arc)
        until(self, "Walk out")
        self.play(tr.animate.set_value(30), run_time=1.4)
        p = c + r * a2_d(30)
        dot = a2_dot(p)
        n = np.array([-np.sin(np.radians(30)), np.cos(np.radians(30)), 0])
        lab = a2_label_beside(T("radius 1", 32), c + r * a2_d(30) / 2, n, 0.12)
        ang = T("30°", 32).move_to(c + 1.25 * a2_d(14))
        self.play(GrowFromCenter(dot), FadeIn(lab), FadeIn(ang), run_time=0.8)
        until(self, "The triangle's two short")
        vl = a2_vleg(c, r, 30); hl = a2_hleg(c, r, 30); rt = a2_rt(c, r, 30)
        self.add(vl, hl, rt); self.bring_to_front(dot)
        self.remove(vl, hl, rt)
        self.play(Create(vl), Create(hl), FadeIn(rt), run_time=1.3)
        self.bring_to_front(dot)
        done(self)


class B07_LegsAreCosSin(Scene):
    def construct(self):
        c = np.array([-1.8, -0.4, 0.0]); r = 2.2
        tr = ValueTracker(30)
        g = lambda: tr.get_value()
        axes = a2_axes(c, r + 0.6, r + 0.45)
        circ = Circle(radius=r, stroke_color=INK, stroke_width=5).move_to(c)
        rad = always_redraw(lambda: Line(c, c + r * a2_d(g()), color=INK, stroke_width=6))
        arc = always_redraw(lambda: a2_arcmark(c, g()))
        dot = always_redraw(lambda: a2_dot(c + r * a2_d(g())))
        vl = always_redraw(lambda: a2_vleg(c, r, g()))
        hl = always_redraw(lambda: a2_hleg(c, r, g()))
        rt = always_redraw(lambda: a2_rt(c, r, g()))
        radlab = a2_label_beside(T("radius 1", 32), c + r * a2_d(30) / 2, np.array([-0.5, 0.866, 0]), 0.2)
        self.add(axes, circ, rad, arc, hl, vl, rt, dot, radlab)
        self.wait(0.3)
        tl_ = T("unit circle", 36).move_to([-1.8, 2.55, 0])
        tag = VGroup(box(-1.8, 2.55, tl_.width + 0.5, 0.8, color=INK, sw=4), tl_)
        self.play(FadeIn(tag, shift=DOWN * 0.2), run_time=0.7)
        # legs labelled
        coslab = always_redraw(lambda: T("cos", 32).move_to([c[0] + r * np.cos(np.radians(g())) / 2, c[1] - 0.42, 0]))
        sinlab = always_redraw(lambda: T("sin", 32).move_to([c[0] + r * np.cos(np.radians(g())) + 0.5, c[1] + r * np.sin(np.radians(g())) / 2, 0]))
        x0 = 2.6
        w1 = T("cos", 40).move_to([x0 + 0.35, 0.8, 0]); w2 = T("sin", 40).move_to([x0 + 0.35, -0.2, 0])
        n1 = always_redraw(lambda: T(f"{np.cos(np.radians(g())):.2f}", 40).move_to([x0 + 1.55, 0.8, 0]))
        n2 = always_redraw(lambda: T(f"{np.sin(np.radians(g())):.2f}", 40).move_to([x0 + 1.55, -0.2, 0]))
        d1 = T("÷  1", 32, DIM).move_to([x0 + 2.85, 0.8, 0]); d2 = T("÷  1", 32, DIM).move_to([x0 + 2.85, -0.2, 0])
        self.play(FadeIn(coslab), FadeIn(sinlab), FadeIn(w1), FadeIn(w2), FadeIn(n1), FadeIn(n2), FadeIn(d1), FadeIn(d2), run_time=0.9)
        until(self, "dividing by one")
        self.play(*[m.animate.scale(0.05).set_opacity(0) for m in (d1, d2)], run_time=0.8)
        self.remove(d1, d2)
        until(self, "The point sits", lead=0.9)
        cs = always_redraw(lambda: a2_label_beside(T("(cos, sin)", 32), c + r * a2_d(g()), a2_d(20), 0.22))
        self.play(FadeIn(cs), FadeOut(radlab), tr.animate.set_value(60), run_time=1.1)
        self.play(tr.animate.set_value(30), FadeIn(radlab), run_time=1.1)
        done(self)


class B09_RadiusAndCenter(Scene):
    def construct(self):
        u = 1.1
        rs = ValueTracker(1.0); cx = ValueTracker(-2.4)
        cy = 0.6
        C = lambda: np.array([cx.get_value(), cy, 0.0])
        circ = always_redraw(lambda: Circle(radius=u * rs.get_value(), stroke_color=INK, stroke_width=5).move_to(C()))
        rad = always_redraw(lambda: Line(C(), C() + u * rs.get_value() * a2_d(30), color=INK, stroke_width=6))
        dot = always_redraw(lambda: a2_dot(C() + u * rs.get_value() * a2_d(30)))
        self.add(circ, rad, dot)
        y = -2.65
        cw = a2_cw(32)
        s = "c + r * vec2(cos(a), sin(a))"
        xl = -len(s) * cw / 2
        pos = lambda idx, ln: xl + (idx + ln / 2) * cw

        def tok(txt, idx):
            return M(txt, 32).move_to([pos(idx, len(txt)), y, 0])
        base1 = tok("vec2(cos(a),", 8); base2 = tok("sin(a))", 21)
        self.play(FadeIn(base1), FadeIn(base2), run_time=0.7)
        until(self, "Multiply by the radius")
        tr_, ts_ = tok("r", 4), tok("*", 6)
        rlab = always_redraw(lambda: T("r", 36).move_to(C() + u * rs.get_value() * a2_d(30) / 2 + np.array([0.12, -0.38, 0])))
        self.play(FadeIn(tr_, shift=DOWN * 0.2), FadeIn(ts_, shift=DOWN * 0.2), FadeIn(rlab), rs.animate.set_value(1.8), run_time=1.3)
        until(self, "Add the center")
        tc_, tp_ = tok("c", 0), tok("+", 2)
        cross = always_redraw(lambda: VGroup(
            Line(C() + [-0.2, 0, 0], C() + [0.2, 0, 0], color=DIM, stroke_width=15, stroke_opacity=0.55),
            Line(C() + [0, -0.2, 0], C() + [0, 0.2, 0], color=DIM, stroke_width=15, stroke_opacity=0.55),
            Line(C() + [-0.2, 0, 0], C() + [0.2, 0, 0], color=TERRA, stroke_width=9),
            Line(C() + [0, -0.2, 0], C() + [0, 0.2, 0], color=TERRA, stroke_width=9)))
        clab = always_redraw(lambda: T("c", 36).move_to(C() + np.array([-0.45, -0.4, 0])))
        self.play(FadeIn(tc_, shift=DOWN * 0.2), FadeIn(tp_, shift=DOWN * 0.2), FadeIn(cross), FadeIn(clab), run_time=0.6)
        self.play(cx.animate.set_value(2.4), run_time=1.5)
        done(self)


class B10_WorkedExample(Scene):
    def construct(self):
        c = np.array([-3.4, -0.3, 0.0]); R = 1.8
        circ = Circle(radius=R, stroke_color=INK, stroke_width=5).move_to(c)
        axes = a2_axes(c, R + 0.5, R + 0.4)
        p = c + R * a2_d(30)
        rad = Line(c, p, color=INK, stroke_width=5)
        hl = a2_hleg(c, R, 30, DIM, 4); vl = Line(p, a2_foot(c, R, 30), color=DIM, stroke_width=4)
        n = np.array([-0.5, 0.866, 0])
        r06 = a2_label_beside(T("0.6", 36), c + (p - c) / 2, n, 0.1)
        self.play(Create(circ), Create(axes), Create(rad), Create(hl), Create(vl), run_time=1.0)
        dot = a2_dot(p)
        self.play(GrowFromCenter(dot), FadeIn(r06), run_time=0.6)
        # equations
        xl = -0.4
        e1a = T("0.6 × cos 30°", 38); e1b = T("=", 38); e1c = T("0.52", 38)
        e2a = T("0.6 × sin 30°", 38); e2b = T("=", 38); e2c = T("0.30", 38)

        def row(a, b, c_, y):
            VGroup(a, b, c_).arrange(RIGHT, buff=0.3).align_to([xl, 0, 0], LEFT).set_y(y)
        row(e1a, e1b, e1c, -0.55); row(e2a, e2b, e2c, -1.55)
        until(self, "The first number")
        self.play(hl.animate.set_stroke(INK, width=10), FadeIn(e1a), run_time=0.6)
        self.play(FadeIn(e1b), FadeIn(e1c), run_time=0.5)
        until(self, "The second is")
        self.play(vl.animate.set_stroke(INK, width=10), FadeIn(e2a), run_time=0.6)
        self.play(FadeIn(e2b), FadeIn(e2c), run_time=0.5)
        until(self, "Hold on")
        bt = T("(0.52, 0.30)", 40).move_to([0.5, 1.4, 0])
        bx = box(0.5, 1.4, bt.width + 0.5, bt.height + 0.4, color=INK, sw=4)
        note = T("hold on to these", 32, DIM).move_to([0.5, 0.65, 0])
        self.play(ReplacementTransform(VGroup(e1c.copy(), e2c.copy()), bt), Create(bx), run_time=1.0)
        self.play(FadeIn(note), run_time=0.5)
        done(self)


class B11_Radians(Scene):
    def construct(self):
        c = np.array([-1.8, -0.2, 0.0]); R = 2.0
        axes = a2_axes(c, R + 0.45, R + 0.4)
        circ = Circle(radius=R, stroke_color=DIM, stroke_width=4).move_to(c)
        bar = Line(c, c + [R, 0, 0], color=INK, stroke_width=11)
        self.play(Create(axes), Create(circ), Create(bar), run_time=0.9)
        cols = [INK, TEAL, INK, TEAL, INK, TEAL]
        arcs = [Arc(radius=R, start_angle=k, angle=1.0, arc_center=c, stroke_color=cols[k], stroke_width=11) for k in range(6)]
        left = Arc(radius=R, start_angle=6.0, angle=2 * np.pi - 6.0, arc_center=c, stroke_color=GOLD, stroke_width=11)
        counter = T("1", 72).move_to([3.9, 0.9, 0])
        cap = T("radii", 32, DIM).move_to([3.9, 0.15, 0])
        until(self, "Lay one radius")
        self.play(TransformFromCopy(bar, arcs[0]), run_time=1.0)
        mark = a2_arcmark(c, np.degrees(1.0), 0.65)
        edge = Line(c, c + R * np.array([np.cos(1.0), np.sin(1.0), 0]), color=DIM, stroke_width=3)
        rlab = T("radian", 32).move_to(c + np.array([1.15, 0.5, 0]))
        self.play(Create(mark), Create(edge), FadeIn(rlab), FadeIn(counter), FadeIn(cap), run_time=0.8)
        for k in (1, 2):
            nc = T(str(k + 1), 72).move_to(counter.get_center())
            self.play(Create(arcs[k]), Transform(counter, nc), run_time=0.55)
        until(self, "A full turn")
        for k in (3, 4, 5):
            nc = T(str(k + 1), 72).move_to(counter.get_center())
            self.play(Create(arcs[k]), Transform(counter, nc), run_time=0.5)
        ll = T("left over", 32).move_to([1.7, -0.9, 0])
        self.play(Create(left), FadeIn(ll), run_time=0.5)
        total = T("6.28 = a full turn", 36).move_to([3.5, -1.8, 0])
        until(self, "about six point")
        self.play(FadeIn(total), run_time=0.6)
        done(self)


class B12_PiTau(Scene):
    def construct(self):
        c = np.array([-2.4, -0.3, 0.0]); R = 1.9
        axes = a2_axes(c, R + 0.4, R + 0.3)
        circ = Circle(radius=R, stroke_color=INK, stroke_width=5).move_to(c)
        a = ValueTracker(0.0)
        rad = always_redraw(lambda: Line(c, c + R * np.array([np.cos(a.get_value()), np.sin(a.get_value()), 0]), color=INK, stroke_width=6))

        def trail():
            v = a.get_value()
            if v < 0.03:
                return VMobject()
            return Arc(radius=R, start_angle=0, angle=v, arc_center=c, stroke_color=TEAL, stroke_width=8)
        tl = always_redraw(trail)
        self.play(Create(circ), Create(axes), run_time=0.8)
        self.add(rad, tl)
        dirs = [(np.pi / 2, "PI / 2", [0, R + 0.6, 0]), (np.pi, "PI", [-R - 0.65, 0, 0]),
                (3 * np.pi / 2, "3 * PI / 2", [0, -R - 0.6, 0]), (2 * np.pi, "TAU", [R + 0.85, 0, 0])]
        until(self, "Pi is half", lead=1.6)
        prev = 0.0
        for th, s, off in dirs:
            tick = Line(c + 0.8 * R * np.array([np.cos(th), np.sin(th), 0]), c + 1.12 * R * np.array([np.cos(th), np.sin(th), 0]), color=INK, stroke_width=8)
            lab = a2_mline(s, c[0] + off[0], c[1] + off[1], 32, "center")
            self.play(a.animate.set_value(th), rate_func=linear, run_time=0.6)
            self.play(Create(tick), FadeIn(lab), run_time=0.25)
            prev = th
        until(self, "And the function")
        self.wait(max(0.05, _TARGET.get("B12", 10.7) / 2 + 0.15 - _elapsed(self)))
        p45 = c + R * a2_d(45)
        edge = Line(c, p45, color=INK, stroke_width=5)
        mark = a2_arcmark(c, 45, 0.95)
        l1 = a2_mline("radians(45.0)", 1.5, 0.5, 32)
        l2 = a2_mline("= PI / 4.0", 1.5, -0.2, 32)
        cr = T("Godot 4.7 docs · Global built-ins", 32, DIM).move_to([2.9, -2.85, 0])
        self.play(Create(edge), Create(mark), run_time=0.8)
        self.play(FadeIn(l1), FadeIn(l2), FadeIn(cr), run_time=0.8)
        done(self)


class B13_DegreesTrap(Scene):
    def construct(self):
        R = 1.2; cy = 0.3
        cL = np.array([-3.9, cy, 0.0]); cR = np.array([2.1, cy, 0.0])
        circL = Circle(radius=R, stroke_color=INK, stroke_width=5).move_to(cL)
        circR = Circle(radius=R, stroke_color=INK, stroke_width=5).move_to(cR)
        axL = a2_axes(cL, R + 0.3, R + 0.3); axR = a2_axes(cR, R + 0.3, R + 0.3)
        tL = a2_mline("sin(30.0)", cL[0] + 0.9, 2.35, 32, "center")
        tRt = a2_mline("sin(radians(30.0))", cR[0] + 1.0, 2.35, 32, "center")
        bxL = cL[0] + 2.0; bxR = cR[0] + 2.0
        zeroL = Line([bxL - 0.4, cy, 0], [bxL + 0.4, cy, 0], color=INK, stroke_width=4)
        zeroR = Line([bxR - 0.4, cy, 0], [bxR + 0.4, cy, 0], color=INK, stroke_width=4)
        cred = T("math values · checked in a Godot 4.7.2 shader", 32, DIM).move_to([0, -3.0, 0])
        self.play(Create(circL), Create(circR), Create(axL), Create(axR), FadeIn(tL), FadeIn(tRt), Create(zeroL), Create(zeroR), FadeIn(cred), run_time=1.0)
        aL = ValueTracker(0.0); aR = ValueTracker(0.0); vL = ValueTracker(0.0); vR = ValueTracker(0.0)
        dL = always_redraw(lambda: a2_dot(cL + R * np.array([np.cos(aL.get_value()), np.sin(aL.get_value()), 0]), 0.16))
        dR = always_redraw(lambda: a2_dot(cR + R * np.array([np.cos(aR.get_value()), np.sin(aR.get_value()), 0]), 0.16))
        rL = always_redraw(lambda: Line(cL, cL + R * np.array([np.cos(aL.get_value()), np.sin(aL.get_value()), 0]), color=DIM, stroke_width=3))
        rR = always_redraw(lambda: Line(cR, cR + R * np.array([np.cos(aR.get_value()), np.sin(aR.get_value()), 0]), color=DIM, stroke_width=3))

        def bar(tr, bx):
            v = tr.get_value()
            h = max(abs(v) * R, 0.01)
            rect = Rectangle(width=0.5, height=h, fill_color=DIM, fill_opacity=1, stroke_width=0)
            rect.move_to([bx, cy + np.sign(v if v else 1) * h / 2, 0])
            return rect
        barL = always_redraw(lambda: bar(vL, bxL)); barR = always_redraw(lambda: bar(vR, bxR))
        cnt = always_redraw(lambda: T(str(int(aL.get_value() / (2 * np.pi))), 56).move_to([cL[0] + 0.9, -1.75, 0]))
        cl = T("turns", 32, DIM).move_to([cL[0] - 0.4, -1.75, 0])
        self.add(rL, rR, dL, dR, barL, barR, cl, cnt)
        until(self, "Thirty radians", lead=0.5)
        self.play(aL.animate.set_value(30.0), rate_func=smooth, run_time=1.8)
        until(self, "near minus one")
        vl = T("-0.99", 40).move_to([bxL + 0.35 + 0.65, cy - 0.99 * R + 0.1, 0])
        self.play(vL.animate.set_value(-0.988), FadeIn(vl), run_time=0.8)
        until(self, "Convert first")
        mk = a2_arcmark(cR, 30, 0.6)
        vr = T("0.50", 40).move_to([bxR + 0.35 + 0.6, cy + 0.5 * R, 0])
        self.play(aR.animate.set_value(np.radians(30)), vR.animate.set_value(0.5), Create(mk), FadeIn(vr), run_time=1.1)
        done(self)


class B14_SineWave(Scene):
    def construct(self):
        cy = 0.5; R = 1.4
        c = np.array([-4.4, cy, 0.0])
        plot, px, py = a2_plot_static(cy, -2.0, 6.4, R)
        circ = Circle(radius=R, stroke_color=INK, stroke_width=5).move_to(c)
        axes = a2_axes(c, R + 0.35, R + 0.35)
        self.play(Create(circ), Create(axes), Create(plot), run_time=1.0)
        th = ValueTracker(0.0)
        P = lambda: c + R * np.array([np.cos(th.get_value()), np.sin(th.get_value()), 0])

        def curve():
            v = th.get_value()
            if v < 0.03:
                return VMobject()
            ts = np.linspace(0, v, max(4, int(v / (2 * np.pi) * 90)))
            m = VMobject(stroke_color=INK, stroke_width=7)
            m.set_points_as_corners([np.array([px(t), py(np.sin(t)), 0]) for t in ts])
            return m
        cur = always_redraw(curve)
        dash = always_redraw(lambda: DashedLine(P(), [px(th.get_value()), P()[1], 0], color=DIM, stroke_width=4, dash_length=0.12))
        tip = always_redraw(lambda: Dot([px(th.get_value()), P()[1], 0], radius=0.1, color=TEAL))
        rad = always_redraw(lambda: Line(c, P(), color=INK, stroke_width=5))
        dot = always_redraw(lambda: a2_dot(P()))
        self.add(cur, dash, rad, dot, tip)
        until(self, "Plot the point's")
        self.play(th.animate.set_value(np.pi), rate_func=linear, run_time=3.0)
        until(self, "The height climbs", lead=0.1)
        self.play(th.animate.set_value(2 * np.pi), rate_func=linear, run_time=2.6)
        until(self, "That curve is")
        sl = T("sine", 40).move_to([px(2 * np.pi) + 0.75, py(0), 0])
        self.play(FadeIn(sl), run_time=0.6)
        done(self)


class B15_CosineShift(Scene):
    def construct(self):
        cy = 0.5; R = 1.4
        c = np.array([-4.4, cy, 0.0])
        plot, px, py = a2_plot_static(cy, -2.0, 6.4, R)
        circ = Circle(radius=R, stroke_color=INK, stroke_width=5).move_to(c)
        axes = a2_axes(c, R + 0.35, R + 0.35)
        sine = a2_curve(np.sin, px, py, INK)
        sl = T("sine", 40).move_to([px(2 * np.pi) + 0.75, py(0), 0])
        home = a2_dot(c + [R, 0, 0])
        self.add(circ, axes, plot, sine, sl, home)
        self.wait(0.3)
        cosine = a2_curve(np.cos, px, py, A2_PALE)
        cl = T("cosine", 40).move_to([px(2 * np.pi) + 0.85, py(1), 0])
        self.play(Create(cosine), run_time=2.0)
        yt = py(1) + 0.4
        brk = VGroup(Line([px(0), yt, 0], [px(np.pi / 2), yt, 0], color=INK, stroke_width=5),
                     Line([px(0), yt, 0], [px(0), yt - 0.3, 0], color=INK, stroke_width=5),
                     Line([px(np.pi / 2), yt, 0], [px(np.pi / 2), yt - 0.3, 0], color=INK, stroke_width=5))
        ql = T("quarter turn", 36).move_to([(px(0) + px(np.pi / 2)) / 2 + 0.2, yt + 0.45, 0])
        until(self, "a quarter turn earlier")
        self.play(Create(brk), FadeIn(ql), FadeIn(cl), run_time=0.9)
        th = ValueTracker(0.0)
        g = lambda: th.get_value()
        until(self, "Two waves", lead=0.7)
        cursor = always_redraw(lambda: Line([px(g()), cy - R - 0.3, 0], [px(g()), cy + R + 0.3, 0], color=DIM, stroke_width=4))
        sd = always_redraw(lambda: Dot([px(g()), py(np.sin(g())), 0], radius=0.13, color=INK))
        cd = always_redraw(lambda: Dot([px(g()), py(np.cos(g())), 0], radius=0.13, color=A2_PALE).set_stroke(INK, width=2))
        pt = always_redraw(lambda: a2_dot(c + R * np.array([np.cos(g()), np.sin(g()), 0])))

        def trail():
            v = g()
            if v < 0.03:
                return VMobject()
            return Arc(radius=R, start_angle=0, angle=v, arc_center=c, stroke_color=TEAL, stroke_width=8)
        tl = always_redraw(trail)
        self.remove(home)
        self.add(cursor, tl, sd, cd, pt)
        self.play(th.animate.set_value(2 * np.pi), rate_func=linear, run_time=2.4)
        done(self)
