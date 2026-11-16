"""ACT V · Read One Aloud  (B35 to B39 Manim; B34, B40, B41 are other lanes)

Cast: the real `breathe` file (lab-shaders/01-breathe.gdshader) read line by line: each line zoomed (monospace, as in the file), small outlined
type tags landing under or over its pieces; the gray-to-teal ramp strip. Every line below is copied from that file, nothing is invented.
"""


def a5_line(s, size, xl, y):
    """A real code line placed by its LEFT edge; .xl and .cw (measured character width) let a5_x find a column."""
    m = M(s, size)
    m.move_to([xl + m.width / 2.0, y, 0])
    m.xl = xl
    m.cw = {32: 0.2461, 36: 0.2950, 40: 0.3440}.get(size, size * 0.0077)   # measured Menlo advance (fixed, so Gate A's stub text agrees)
    return m


def a5_x(m, col):
    return m.xl + col * m.cw


def a5_tag(text, x0, x1, y, up=False, dy=0.55, shift=0.0, size=32):
    """A drawn bracket from x0 to x1 at height y with a stem to an outlined tag (under the text by default, above it with up=True)."""
    d = 1 if up else -1
    tk = -d * 0.14
    br = VGroup(Line([x0, y, 0], [x1, y, 0], color=DIM, stroke_width=5), Line([x0, y, 0], [x0, y + tk, 0], color=DIM, stroke_width=5),
                Line([x1, y, 0], [x1, y + tk, 0], color=DIM, stroke_width=5))
    t = T(text, size)
    xm = (x0 + x1) / 2.0
    tagbox = RoundedRectangle(width=t.width + 0.4, height=t.height + 0.3, corner_radius=0.12, stroke_color=DIM, stroke_width=3).set_fill(PALEBOX, opacity=1)
    tg = VGroup(tagbox, t).move_to([xm + shift, y + d * dy, 0])
    stem = Line([xm, y, 0], [xm + shift, y + d * dy - d * tagbox.height / 2, 0], color=DIM, stroke_width=4)
    g = VGroup(br, stem, tg)
    g.br = br; g.stem = stem; g.tag = tg; g.d = d
    return g


def a5_show(self, g, rt=0.45):
    """The tag flies out to its piece: stem and tag slide in from the line, the bracket closes."""
    self.play(AnimationGroup(Create(g.br), FadeIn(g.stem), FadeIn(g.tag, shift=UP * g.d * 0.2), lag_ratio=0.3), run_time=rt)


def a5_tok(n, x, y, color=TEAL, cell=0.28, gap=0.07):
    cs = VGroup(*[Square(side_length=cell, fill_color=color, fill_opacity=1, stroke_width=0).move_to([(i - (n - 1) / 2.0) * (cell + gap), 0, 0]) for i in range(n)])
    return cs.move_to([x, y, 0])


# ═════════════════════════════ B35 · the two uniform lines ═════════════════════════════
class B35_ReadUniforms(Scene):
    def construct(self):
        xl = -4.87
        l3 = a5_line("uniform vec4 tint : source_color;", 36, xl, 1.4)
        l4 = a5_line("uniform float speed = 2.0;", 36, xl, -1.35)
        cap = T("hint: the word after a colon that tells Godot how to treat a uniform", 32).move_to([0, -3.0, 0])
        self.play(FadeIn(l3), FadeIn(l4), run_time=0.5)
        self.play(FadeIn(cap), run_time=0.4)
        yu, yd = 1.88, 0.93
        t_uni = a5_tag("set from outside", a5_x(l3, 0), a5_x(l3, 7), yu, up=True, dy=0.55)
        t_vec = a5_tag("a color", a5_x(l3, 8), a5_x(l3, 12), yd, dy=0.5)
        t_hint = a5_tag("hint", a5_x(l3, 18), a5_x(l3, 33), yd, dy=0.5)
        sw = Circle(radius=0.22, fill_color=TEAL, fill_opacity=1, stroke_color=DIM, stroke_width=3).move_to([0.9, -0.22, 0])
        swl = T("treated as a color", 32).move_to([sw.get_center()[0] + 0.45 + 1.5, -0.22, 0])
        t_nod = a5_tag("no default: black", a5_x(l3, 32), a5_x(l3, 33), yu, up=True, dy=0.55, shift=-0.3)
        yd4 = -1.8
        t_flt = a5_tag("a decimal number", a5_x(l4, 8), a5_x(l4, 13), yd4, dy=0.5)
        t_def = a5_tag("default", a5_x(l4, 20), a5_x(l4, 26), yd4, dy=0.5)
        until(self, "Line three is a uniform", lead=0.1)
        a5_show(self, t_uni)
        until(self, "a vec four", lead=0.2)
        a5_show(self, t_vec)
        until(self, "Source color is a hint", lead=0.3)
        a5_show(self, t_hint)
        self.play(FadeIn(sw, scale=0.6), FadeIn(swl), run_time=0.4)
        until(self, "With no default", lead=0.7)
        a5_show(self, t_nod)
        until(self, "Line four is a float", lead=0.4)
        a5_show(self, t_flt)
        until(self, "default of two", lead=0.6)
        a5_show(self, t_def)
        done(self)


# ═════════════════════════════ B36 · the signature of breathe ═════════════════════════════
class B36_ReadSignature(Scene):
    def construct(self):
        xl = -5.0
        l6 = a5_line("vec3 breathe(vec3 base, float t) {", 36, xl, 1.2)
        self.play(FadeIn(l6), run_time=0.5)
        yu, yd = 1.7, 0.7
        t_name = a5_tag("name", a5_x(l6, 5), a5_x(l6, 12), yu, up=True, dy=1.2)
        t_ret = a5_tag("hands back a vec3", a5_x(l6, 0), a5_x(l6, 4), yu, up=True, dy=0.55, shift=-0.1)
        t_a1 = a5_tag("argument: vec3", a5_x(l6, 13), a5_x(l6, 22), yd, dy=0.5)
        t_a2 = a5_tag("argument: float", a5_x(l6, 24), a5_x(l6, 31), yd, dy=1.15)
        # the flow: a three-cell and a one-cell token into the function, a three-cell token out
        fb = box(0.2, -1.55, 2.3, 0.85, color=INK, sw=4)
        fl = M("breathe", 32).move_to(fb.get_center())
        ar_in = arrow([-1.6, -1.55, 0], [-1.0, -1.55, 0], color=DIM, w=5, tip=0.2)
        ar_out = arrow([1.4, -1.55, 0], [2.0, -1.55, 0], color=DIM, w=5, tip=0.2)
        k3 = a5_tok(3, -4.6, -1.55)
        k1 = a5_tok(1, -3.1, -1.55)
        note = T("the body must return a vec3", 32).move_to([0.2, -2.75, 0])
        until(self, "declares breathe", lead=0.2)
        a5_show(self, t_name)
        until(self, "hands back a vec three", lead=0.2)
        a5_show(self, t_ret)
        until(self, "a vec three called base", lead=0.3)
        a5_show(self, t_a1)
        until(self, "a float called t", lead=0.3)
        a5_show(self, t_a2)
        until(self, "So the body gets", lead=0.4)
        self.play(FadeIn(fb), FadeIn(fl), FadeIn(ar_in), FadeIn(ar_out), FadeIn(k3), FadeIn(k1), run_time=0.4)
        self.play(k3.animate.move_to([-1.2, -1.55, 0]), k1.animate.move_to([-0.9, -1.55, 0]), run_time=0.6)
        self.play(FadeOut(k3), FadeOut(k1), fb.animate.scale(1.05), run_time=0.2)
        out = a5_tok(3, 1.5, -1.55)
        self.play(FadeIn(out), fb.animate.scale(1 / 1.05), run_time=0.2)
        self.play(out.animate.move_to([3.6, -1.55, 0]), FadeIn(note), run_time=0.6)
        done(self)


# ═════════════════════════════ B37 · the wave line ═════════════════════════════
class B37_ReadWave(Scene):
    def construct(self):
        xl = -6.0
        l7 = a5_line("float wave = 0.5 + 0.5 * sin(t);", 36, xl, 2.55)
        self.play(FadeIn(l7), run_time=0.5)
        rows = [(29, 29, "t"), (25, 30, "sin(t)"), (19, 30, "0.5 * sin(t)"), (13, 30, "0.5 + 0.5 * sin(t)")]
        yb0, step = 1.85, 0.62
        brs = []
        for k, (c0, c1, nm) in enumerate(rows):
            x0, x1 = a5_x(l7, c0), a5_x(l7, c1 + 1)
            y = yb0 - k * step
            g = a5_tag("float", x0, x1, y, dy=0.0)
            # side tag at the right end of the bracket instead of a stem tag
            t = T("float", 32)
            tb = RoundedRectangle(width=t.width + 0.4, height=t.height + 0.3, corner_radius=0.12, stroke_color=INK, stroke_width=3).set_fill(PALEBOX, opacity=1)
            tg = VGroup(tb, t).move_to([x1 + 0.2 + tb.width / 2.0, y, 0])
            br = g.br
            brs.append(VGroup(br, tg))
        # into wave
        wx0, wx1 = a5_x(l7, 6), a5_x(l7, 10)
        wb = a5_tag("float", wx0, wx1, yb0, dy=0.0)
        wt = T("float", 32)
        wtb = RoundedRectangle(width=wt.width + 0.4, height=wt.height + 0.3, corner_radius=0.12, stroke_color=INK, stroke_width=3).set_fill(PALEBOX, opacity=1)
        wtg = VGroup(wtb, wt).move_to([wx0 - 0.2 - wtb.width / 2.0, yb0, 0])
        wave_t = VGroup(wb.br, wtg)
        into = arrow([a5_x(l7, 13) - 0.15, yb0 - 3 * step, 0], [(wx0 + wx1) / 2, yb0 - 0.12, 0], color=DIM, w=5, tip=0.2)
        # the sine curve: -1..1 squeezed into 0..1
        pl = plot(lambda v: np.sin(v), x_range=(0, 2 * np.pi), y_range=(-1, 1), size=(3.6, 1.7), x=-3.6, y=-1.55, color=DIM)
        pl_labels = VGroup(T("1", 32).move_to([-5.75, -0.7, 0]), T("-1", 32).move_to([-5.8, -2.4, 0]))
        sq = VMobject(stroke_color=INK, stroke_width=7).set_points_smoothly([pl.pt(v) for v in np.linspace(0, 2 * np.pi, 80)])
        sq.set_points_smoothly([pl.pt(v) for v in np.linspace(0, 2 * np.pi, 80)])
        sq2 = VMobject(stroke_color=INK, stroke_width=7)
        sq2_pts = []
        ax_x0, ax_y0 = -3.6 - 1.8, -1.55 - 0.85
        for v in np.linspace(0, 2 * np.pi, 80):
            yv = 0.5 + 0.5 * np.sin(v)
            sq2_pts.append(np.array([ax_x0 + v / (2 * np.pi) * 3.6, ax_y0 + (yv + 1) / 2 * 1.7, 0]))
        sq2.set_points_smoothly(sq2_pts)
        zero = T("0", 32).move_to([-5.7, -1.55, 0])
        until(self, "Sine of t is a float", lead=0.3)
        self.play(FadeIn(brs[0]), FadeIn(brs[1]), run_time=0.5)
        self.play(FadeIn(pl), FadeIn(pl_labels), run_time=0.4)
        until(self, "Half of that", lead=0.4)
        self.play(FadeIn(brs[2]), run_time=0.35)
        self.play(FadeIn(brs[3]), run_time=0.35)
        self.play(Transform(pl.curve, sq2), FadeIn(zero), run_time=0.7)
        dot = Dot(sq2_pts[0], radius=0.15, color=TERRA).set_stroke(DIM, width=3)
        until(self, "now swinging", lead=0.3)
        self.add(dot)
        self.play(MoveAlongPath(dot, pl.curve), run_time=1.5, rate_func=linear)
        until(self, "stored in wave", lead=0.5)
        self.play(FadeIn(wave_t), FadeIn(into), run_time=0.4)
        done(self)


# ═════════════════════════════ B38 · the return line ═════════════════════════════
class B38_ReadReturn(Scene):
    def construct(self):
        xl = -5.0
        l8 = a5_line("return mix(vec3(0.9), base, wave);", 36, xl, 2.0)
        self.play(FadeIn(l8), run_time=0.5)
        yu, yd = 2.5, 1.5
        t_ret = a5_tag("matches the signature", a5_x(l8, 0), a5_x(l8, 6), yu, up=True, dy=0.5, shift=0.3)
        t_mix = a5_tag("vec3", a5_x(l8, 7), a5_x(l8, 33), yu, up=True, dy=0.5)
        t_v09 = a5_tag("fills all three: a pale gray", a5_x(l8, 11), a5_x(l8, 20), yd, dy=1.1, shift=-0.7)
        sw = Rectangle(width=0.5, height=0.5, fill_color="#E4E2DA", fill_opacity=1, stroke_color=DIM, stroke_width=3).move_to([(a5_x(l8, 11) + a5_x(l8, 21)) / 2 - 0.7 - 2.2 - 0.45, yd - 1.1, 0])
        t_base = a5_tag("vec3", a5_x(l8, 22), a5_x(l8, 26), yd, dy=0.5)
        t_wave = a5_tag("float: 0 to 1", a5_x(l8, 28), a5_x(l8, 32), yd, dy=0.5, shift=0.55)
        gl = T("mix(a, b, t): blends from a to b: t of 0 gives a, 1 gives b", 32).move_to([0, -0.55, 0])
        strip = ramp_strip(width=7.0, label0="0", label1="1", y=-1.55, x=0.0)
        note = T("0 gives the gray, 1 gives base", 32).move_to([0, -2.7, 0])
        dot = ramp_marker(strip, 0.0)
        until(self, "Vec three of zero", lead=0.2)
        a5_show(self, t_v09)
        self.play(FadeIn(sw), run_time=0.3)
        until(self, "Mix blends", lead=0.2)
        self.play(FadeIn(gl), run_time=0.4)
        self.play(FadeIn(strip), FadeIn(note), FadeIn(dot), run_time=0.4)
        until(self, "toward base", lead=0.1)
        a5_show(self, t_base, 0.35)
        a5_show(self, t_wave, 0.35)
        self.play(dot.animate.move_to([strip.x1, strip.y, 0]), run_time=1.5, rate_func=linear)
        until(self, "The result is a vec three", lead=0.3)
        a5_show(self, t_mix, 0.4)
        a5_show(self, t_ret, 0.4)
        done(self)


# ═════════════════════════════ B39 · the two fragment lines ═════════════════════════════
class B39_ReadFragment(Scene):
    def construct(self):
        xl = -5.65
        l12 = a5_line("vec3 color = breathe(tint.rgb, TIME * speed);", 32, xl, 1.75)
        l13 = a5_line("COLOR = vec4(color, tint.a);", 32, xl, -0.7)
        cap1 = T("TIME: seconds on one clock shared by the whole game", 32).move_to([0, -2.55, 0])
        cap2 = T("COLOR: the color of the pixel being drawn; fragment() sets it", 32).move_to([0, -3.05, 0])
        self.play(FadeIn(l12), FadeIn(l13), run_time=0.5)
        yu12, yd12 = 2.12, 1.38
        t_rgb = a5_tag("vec3 (swizzle)", a5_x(l12, 21), a5_x(l12, 29), yd12, dy=0.5, shift=-0.2)
        t_time = a5_tag("float", a5_x(l12, 31), a5_x(l12, 43), yd12, dy=0.5)
        t_br = a5_tag("vec3", a5_x(l12, 13), a5_x(l12, 44), yu12, up=True, dy=0.5)
        t_col = a5_tag("vec3", a5_x(l12, 5), a5_x(l12, 10), yd12, dy=0.5)
        yu13, yd13 = -0.33, -1.07
        t_v4 = a5_tag("vec4(...)", a5_x(l13, 8), a5_x(l13, 27), yd13, dy=0.5)
        t_c4 = a5_tag("vec4", a5_x(l13, 0), a5_x(l13, 5), yu13, up=True, dy=0.5)
        rg = Dot([xl - 0.3, -0.7, 0], radius=0.16, color=TERRA).set_stroke(DIM, width=3)
        until(self, "tint dot R G B", lead=0.1)
        a5_show(self, t_rgb)
        until(self, "time times speed", lead=0.2)
        a5_show(self, t_time)
        self.play(FadeIn(cap1), run_time=0.35)
        until(self, "Breathe turns", lead=0.2)
        a5_show(self, t_br)
        a5_show(self, t_col, 0.35)
        until(self, "Vec four adds", lead=0.2)
        a5_show(self, t_v4)
        until(self, "color, a vec four, takes it", lead=0.4)
        self.play(FadeIn(rg), run_time=0.3)
        a5_show(self, t_c4, 0.4)
        self.play(FadeIn(cap2), run_time=0.35)
        done(self)
