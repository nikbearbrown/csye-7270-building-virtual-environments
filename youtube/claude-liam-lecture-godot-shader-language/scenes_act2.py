"""ACT II . Types and Vectors  (B10, B12, B13, B14, B16, B19; all Manim)

Cast for the act: the bundle, a row of outlined cells (1 to 4 cells; the count IS the size), small type tags, mono code with
explicit per-token coordinates (Pango may drop spaces). Every drawing here is a drawing; the numbers are the Lab's own
(0.4/0.7/0.6/1.0 from 33-swizzle-pick; 0.37/0.64/0.57/1.0 are the sprite centre of 08-texture-vec4 to two places).
"""

_A2_CW = []


def a2_cw():
    """Width of one Menlo character at size 32 (measured once)."""
    if not _A2_CW:
        _A2_CW.append(M("0" * 20).width / 20.0)
    return _A2_CW[0]


def a2_code(line, x_left, y, size=32):
    """A mono code line with EXPLICIT coordinates: one Text per token, each placed by its character index (so a dropped space cannot shift anything).
    Returns VGroup with .tokens (list of (start, end, Text)) and .xs(i) -> scene x of the left edge of character i."""
    cw = a2_cw() * size / 32.0
    g = VGroup()
    toks = []
    i = 0
    n = len(line)
    while i < n:
        if line[i] == " ":
            i += 1
            continue
        j = i
        while j < n and line[j] != " ":
            j += 1
        t = M(line[i:j], size)
        t.move_to([x_left + (i + (j - i) / 2.0) * cw, y, 0])
        g.add(t)
        toks.append((i, j, t))
        i = j
    g.tokens = toks
    g.xs = lambda k: x_left + k * cw
    g.cw = cw
    return g


def a2_cell(x, y, txt="", w=1.05, h=0.82, color=INK, sw=4):
    """One outlined cell of the bundle (no fill behind the text). Returns VGroup(frame, text) with .frame."""
    fr = RoundedRectangle(width=w, height=h, corner_radius=0.1, stroke_color=color, stroke_width=sw).move_to([x, y, 0])
    g = VGroup(fr)
    g.frame = fr
    g.txt = None
    if txt:
        t = T(txt, 32).move_to([x, y, 0])
        g.add(t)
        g.txt = t
    return g


def a2_bundle(vals, x0, y, pitch=1.15, w=1.05, h=0.82):
    """A row of cells starting at x0. Returns VGroup of cells with .cells."""
    cells = [a2_cell(x0 + k * pitch, y, v, w, h) for k, v in enumerate(vals)]
    g = VGroup(*cells)
    g.cells = cells
    return g


def a2_tag(text, x, y, size=32):
    """A small outlined type tag centred at (x, y)."""
    t = T(text, size) if not text.startswith(".") else M(text, size)
    box_ = RoundedRectangle(width=t.width + 0.4, height=0.62, corner_radius=0.12, stroke_color=INK, stroke_width=3).set_fill(PALEBOX, opacity=1)
    g = VGroup(box_, t).move_to([x, y, 0])
    return g


def a2_title(s):
    t = T(s, 40)
    t.move_to([-6.2 + t.width / 2.0, 3.0, 0])
    return t


# ───────────────────────────── B10 . three types ─────────────────────────────
class B10_ThreeTypes(Scene):
    def construct(self):
        title = a2_title("Types and Vectors")
        xs = [-4.5, -1.5, 1.5, 4.5]
        ty = 1.35
        specs = [("float", "0.5", "decimal number"), ("int", "3", "whole number"), ("bool", "true", "true or false"), ("sampler2D", None, "texture's type")]
        tiles = []
        for x, (ty_name, val, lab) in zip(xs, specs):
            fr = box(x, ty, 2.75, 1.5, INK, 4)
            nm = M(ty_name, 32).move_to([x, ty + 0.42, 0])
            if val is not None:
                v = M(val, 32).move_to([x, ty - 0.22, 0])
            else:
                sq = Square(side_length=0.62, stroke_color=INK, stroke_width=4).move_to([x, ty - 0.27, 0])
                hill = VMobject(stroke_color=TEAL, stroke_width=5).set_points_as_corners([[x - 0.26, ty - 0.45, 0], [x - 0.08, ty - 0.2, 0], [x + 0.06, ty - 0.36, 0], [x + 0.26, ty - 0.12, 0]])
                v = VGroup(sq, hill)
            l = T(lab, 32).move_to([x, ty - 1.2, 0])
            tiles.append(VGroup(fr, nm, v, l))
        self.add(title)
        self.wait(0.2)
        self.play(FadeIn(tiles[0], scale=0.8), run_time=0.4)
        until(self, "an int")
        self.play(FadeIn(tiles[1], scale=0.8), run_time=0.4)
        until(self, "a bool")
        self.play(FadeIn(tiles[2], scale=0.8), run_time=0.4)
        until(self, "A texture", lead=0.7)
        self.play(FadeIn(tiles[3], scale=0.8), run_time=0.4)
        cap = T("texture: an image a shader can read by address", 32).move_to([0, -0.55, 0])
        self.play(FadeIn(cap), run_time=0.4)
        # the declaration, typed in
        until(self, "You declare", lead=0.9)
        decl = a2_code("float level = 0.5;", -18 * a2_cw() * 1.25 / 2.0, -1.65, 40)
        self.play(LaggedStart(*[FadeIn(t) for _, _, t in decl.tokens], lag_ratio=0.35), run_time=0.9)
        cw = decl.cw
        y_b = -1.65 - 0.5

        def span(i0, i1):
            return decl.xs(i0), decl.xs(i1)
        tg1 = type_tag("type", *span(0, 5), y_b)
        tg2 = type_tag("name", *span(6, 11), y_b)
        tg3 = type_tag("value", *span(14, 17), y_b)
        until(self, "its type first")
        self.play(Create(tg1.bracket), FadeIn(tg1.tag), run_time=0.35)
        until(self, "then its name", lead=0.1)
        self.play(Create(tg2.bracket), FadeIn(tg2.tag), run_time=0.35)
        self.play(Create(tg3.bracket), FadeIn(tg3.tag), run_time=0.35)
        done(self)


# ───────────────────────────── B12 . bundles ─────────────────────────────
class B12_Bundles(Scene):
    def construct(self):
        x0 = -1.5
        y2, y3, y4 = 2.2, 0.95, -0.3
        r2 = a2_bundle(["", ""], x0, y2)
        r3 = a2_bundle(["", "", ""], x0, y3)
        r4 = a2_bundle(["0.37", "0.64", "0.57", "1.0"], x0, y4)
        n2 = M("vec2", 32).move_to([-2.9, y2, 0])
        n3 = M("vec3", 32).move_to([-2.9, y3, 0])
        n4 = M("vec4", 32).move_to([-2.9, y4, 0])
        letters = VGroup(*[T(c, 32).move_to([x0 + k * 1.15, y4 - 0.78, 0]) for k, c in enumerate("rgba")])
        swatch = RoundedRectangle(width=0.95, height=0.82, corner_radius=0.1, fill_color=TEAL, fill_opacity=1, stroke_width=0).move_to([3.75, y4, 0])
        swl = T("a color", 32).move_to([5.3, y4, 0])
        # a drawn texture: a 4 x 4 gradient of separate tiles
        tex = VGroup()
        for r in range(4):
            for c in range(4):
                tex.add(Rectangle(width=0.27, height=0.27, fill_color=_rgb((r + c) / 6.0), fill_opacity=1, stroke_width=0).move_to([-5.2 + (c - 1.5) * 0.31, y4 + (1.5 - r) * 0.31, 0]))
        texfr = Rectangle(width=1.38, height=1.38, stroke_color=INK, stroke_width=4).move_to([-5.2, y4, 0])
        texl = T("texture lookup", 32).move_to([-5.0, y4 - 1.1, 0])
        tarr = arrow([-4.35, y4, 0], [-3.55, y4, 0])
        cap1 = T("vector: a bundle of two to four numbers", 32).move_to([0, -2.15, 0])
        cap2 = T("alpha: how visible a pixel is: 0 invisible, 1 solid", 32).move_to([0, -2.95, 0])
        self.wait(0.2)
        until(self, "bundles of two")
        self.play(FadeIn(cap1), run_time=0.4)
        until(self, "vec two")
        self.play(FadeIn(n2), LaggedStart(*[FadeIn(c, scale=0.7) for c in r2.cells], lag_ratio=0.3), run_time=0.6)
        until(self, "vec three")
        self.play(FadeIn(n3), LaggedStart(*[FadeIn(c, scale=0.7) for c in r3.cells], lag_ratio=0.3), run_time=0.7)
        until(self, "vec four", lead=0.1)
        self.play(FadeIn(n4), LaggedStart(*[FadeIn(c, scale=0.7) for c in r4.cells], lag_ratio=0.25), FadeIn(letters), run_time=0.9)
        until(self, "A color is")
        self.play(FadeIn(swatch), FadeIn(swl), run_time=0.4)
        until(self, "alpha", lead=0.2)
        self.play(FadeIn(cap2), run_time=0.4)
        until(self, "Reading a texture", lead=0.3)
        self.play(FadeIn(texfr), FadeIn(tex), FadeIn(texl), run_time=0.4)
        self.play(GrowArrow(tarr), run_time=0.4)
        done(self)


# ───────────────────────────── B13 . build a vector ─────────────────────────────
class B13_BuildAVector(Scene):
    def construct(self):
        cw = a2_cw()
        ys = [2.15, 0.1, -1.95]
        lab1 = a2_code("vec3(0.5)", -6.0, ys[0])
        lab2 = a2_code("vec4(c, 1.0)", -6.0, ys[1])
        lab3 = a2_code("vec3(0.1, 0.2)", -6.0, ys[2])
        # (1) one number fills three cells
        c1 = a2_cell(-1.6, ys[0], "0.5")
        c1b = a2_cell(-1.6, ys[0], "0.5")
        c1c = a2_cell(-1.6, ys[0], "0.5")
        # (2) three plus one
        c2 = [a2_cell(-1.6 + k * 1.15, ys[1], "") for k in range(3)]
        dots = [Dot([-1.6 + k * 1.15, ys[1], 0], radius=0.11, color=TEAL) for k in range(3)]
        one = a2_cell(3.2, ys[1], "1.0")
        cnt = T("3 + 1 = 4", 32).move_to([5.0, ys[1], 0])
        # (3) two cells and a gap
        c3 = [a2_cell(-1.6, ys[2], "0.1"), a2_cell(-0.45, ys[2], "0.2")]
        gap = DashedVMobject(RoundedRectangle(width=1.05, height=0.82, corner_radius=0.1, stroke_color=DIM, stroke_width=4).move_to([0.7, ys[2], 0]), num_dashes=24)
        cross = VGroup(Line([0.4, ys[2] - 0.28, 0], [1.0, ys[2] + 0.28, 0], color=INK, stroke_width=7), Line([0.4, ys[2] + 0.28, 0], [1.0, ys[2] - 0.28, 0], color=INK, stroke_width=7))
        cnt3 = T("2 of 3", 32).move_to([3.0, ys[2], 0])
        few = T("too few", 32).move_to([5.0, ys[2], 0])
        self.wait(0.2)
        until(self, "Give vec three one number", lead=0.3)
        self.play(FadeIn(lab1), FadeIn(c1), run_time=0.4)
        self.add(c1b, c1c)
        self.play(c1b.animate.shift(RIGHT * 1.15), c1c.animate.shift(RIGHT * 2.3), run_time=0.7)
        until(self, "Give vec four a vec three", lead=0.3)
        self.play(FadeIn(lab2), LaggedStart(*[FadeIn(c) for c in c2], lag_ratio=0.2), *[FadeIn(d) for d in dots], FadeIn(one), run_time=0.7)
        until(self, "and a number")
        grp1 = VGroup(one)
        self.play(one.animate.move_to([-1.6 + 3 * 1.15, ys[1], 0]), run_time=0.7)
        self.play(FadeIn(cnt), run_time=0.3)
        until(self, "The pieces must add up", lead=0.4)
        self.play(FadeIn(lab3), *[FadeIn(c) for c in c3], FadeIn(gap), run_time=0.5)
        until(self, "Godot refuses", lead=0.3)
        self.play(Create(cross[0]), Create(cross[1]), FadeIn(cnt3), FadeIn(few), run_time=0.6)
        done(self)


# ───────────────────────────── B14 . all at once ─────────────────────────────
class B14_AllAtOnce(Scene):
    def construct(self):
        cols = [-3.8, -2.65, -1.5]
        yt_in, yt_out = 2.5, 1.0
        yb_in, yb_mid, yb_out = -0.45, -1.65, -2.85
        vin = ["0.2", "0.3", "0.4"]
        top_in = [a2_cell(x, yt_in, v) for x, v in zip(cols, vin)]
        top_out = [a2_cell(x, yt_out, v) for x, v in zip(cols, ["0.4", "0.6", "0.8"])]
        two = a2_cell(-5.7, 1.75, "2.0", w=0.9)
        times = VGroup(Line([-4.92, 1.75 - 0.14, 0], [-4.64, 1.75 + 0.14, 0], color=INK, stroke_width=6), Line([-4.92, 1.75 + 0.14, 0], [-4.64, 1.75 - 0.14, 0], color=INK, stroke_width=6))
        lab1 = a2_code("* 2.0", -0.6, 1.75)
        arrs = [arrow([x, yt_in - 0.45, 0], [x, yt_out + 0.45, 0]) for x in cols]
        bot_in = [a2_cell(x, yb_in, v) for x, v in zip(cols, vin)]
        bot_mid = [a2_cell(x, yb_mid, v) for x, v in zip(cols, ["2.0", "1.0", "0.5"])]
        bot_out = [a2_cell(x, yb_out, v) for x, v in zip(cols, ["0.4", "0.3", "0.2"])]
        lab2 = a2_code("* vec3(2.0, 1.0, 0.5)", -0.6, yb_mid)
        pair = [dim_arrow([x, yb_in - 0.43, 0], [x, yb_mid + 0.43, 0], color=DIM, w=5, tip=0.13) for x in cols]
        arrs2 = [arrow([x, yb_mid - 0.43, 0], [x, yb_out + 0.43, 0], w=5, tip=0.14) for x in cols]
        self.wait(0.2)
        self.play(LaggedStart(*[FadeIn(c) for c in top_in], lag_ratio=0.2), run_time=0.6)
        until(self, "by two point zero", lead=0.6)
        self.play(FadeIn(two), FadeIn(times), FadeIn(lab1), run_time=0.4)
        until(self, "all three numbers double", lead=0.5)
        self.play(*[GrowArrow(a) for a in arrs], run_time=0.5)
        self.play(*[FadeIn(c) for c in top_out], run_time=0.3)
        until(self, "Multiply two vectors", lead=0.4)
        self.play(*[FadeIn(c) for c in bot_in], *[FadeIn(c) for c in bot_mid], FadeIn(lab2), run_time=0.5)
        until(self, "each part meets", lead=0.5)
        self.play(*[GrowArrow(a) for a in pair], run_time=0.5)
        self.play(*[GrowArrow(a) for a in arrs2], run_time=0.4)
        self.play(*[FadeIn(c) for c in bot_out], run_time=0.3)
        done(self)


# ───────────────────────────── B16 . swizzle ─────────────────────────────
class B16_Swizzle(Scene):
    def construct(self):
        y0 = -0.35
        xs = [-1.8, -0.6, 0.6, 1.8]
        row = a2_bundle(["0.4", "0.7", "0.6", "1.0"], xs[0], y0)
        xyzw = VGroup(*[T(c, 32).move_to([x, y0 - 0.7, 0]) for x, c in zip(xs, "xyzw")])
        rgba = VGroup(*[T(c, 32).move_to([x, y0 - 1.15, 0]) for x, c in zip(xs, "rgba")])
        stpq = VGroup(*[T(c, 32, DIM).move_to([x, y0 - 1.6, 0]) for x, c in zip(xs, "stpq")])
        n4 = M("vec4", 32).move_to([-3.55, y0, 0])
        cap = T("swizzle: picking or reordering a vector's parts", 32).move_to([0, -2.85, 0])

        def lifted(k, label, dx, dy, tname):
            cells = [a2_cell(xs[i] + dx, y0 + dy, v) for i, v in enumerate(["0.4", "0.7", "0.6", "1.0"][:k])]
            return cells

        xm3 = sum(xs[:3]) / 3.0
        xm2 = sum(xs[:2]) / 2.0
        br3 = VGroup(Line([xs[0] - 0.5, y0 + 0.6, 0], [xs[2] + 0.5, y0 + 0.6, 0], color=DIM, stroke_width=5),
                     Line([xs[0] - 0.5, y0 + 0.6, 0], [xs[0] - 0.5, y0 + 0.45, 0], color=DIM, stroke_width=5),
                     Line([xs[2] + 0.5, y0 + 0.6, 0], [xs[2] + 0.5, y0 + 0.45, 0], color=DIM, stroke_width=5))
        l3 = M(".rgb", 32).move_to([xm3, y0 + 0.98, 0])
        br2 = VGroup(Line([xs[0] - 0.5, y0 + 0.6, 0], [xs[1] + 0.5, y0 + 0.6, 0], color=DIM, stroke_width=5),
                     Line([xs[0] - 0.5, y0 + 0.6, 0], [xs[0] - 0.5, y0 + 0.45, 0], color=DIM, stroke_width=5),
                     Line([xs[1] + 0.5, y0 + 0.6, 0], [xs[1] + 0.5, y0 + 0.45, 0], color=DIM, stroke_width=5))
        l2 = M(".xy", 32).move_to([xm2, y0 + 0.98, 0])
        # lifted copies: vec3 up-left, vec2 up-right
        v3 = [a2_cell(-4.9 + i * 1.15, 1.9, v) for i, v in enumerate(["0.4", "0.7", "0.6"])]
        v3l = M(".rgb", 32).move_to([-3.75, 2.75, 0])
        v3n = M("vec3", 32).move_to([-3.75, 1.05, 0])
        v2 = [a2_cell(2.9 + i * 1.15, 1.9, v) for i, v in enumerate(["0.4", "0.7"])]
        v2l = M(".xy", 32).move_to([3.475, 2.75, 0])
        v2n = M("vec2", 32).move_to([3.475, 1.05, 0])
        self.wait(0.2)
        self.play(FadeIn(row), FadeIn(n4), run_time=0.5)
        self.play(FadeIn(xyzw), FadeIn(rgba), FadeIn(stpq), run_time=0.5)
        until(self, "Dot R G B", lead=0.3)
        self.play(Create(br3), FadeIn(l3), run_time=0.4)
        cp3 = VGroup(*[c.copy() for c in row.cells[:3]])
        self.add(cp3)
        self.play(*[cp3[i].animate.move_to(v3[i].get_center()) for i in range(3)], run_time=0.8)
        self.play(FadeIn(v3l), FadeIn(v3n), FadeOut(br3), FadeOut(l3), run_time=0.3)
        until(self, "Dot X Y", lead=0.3)
        self.play(Create(br2), FadeIn(l2), run_time=0.4)
        cp2 = VGroup(*[c.copy() for c in row.cells[:2]])
        self.add(cp2)
        self.play(*[cp2[i].animate.move_to(v2[i].get_center()) for i in range(2)], run_time=0.8)
        self.play(FadeIn(v2l), FadeIn(v2n), FadeOut(br2), FadeOut(l2), run_time=0.3)
        until(self, "swizzling", lead=0.4)
        self.play(FadeIn(cap), run_time=0.4)
        done(self)


# ───────────────────────────── B19 . type chain ─────────────────────────────
class B19_TypeChain(Scene):
    def construct(self):
        line = "vec3 c = 0.4 + 0.6 * vec3(UV, 0.5);"
        cw = a2_cw()
        xl = -len(line) * cw / 2.0
        yl = 2.6
        code = a2_code(line, xl, yl)
        xs = code.xs
        y_levels = [yl - 0.5, yl - 1.65, yl - 2.8, yl - 3.95]
        self.add(code)
        self.wait(0.2)
        tg1 = type_tag("vec2", xs(26), xs(28), y_levels[0])
        tg2 = type_tag("vec3", xs(21), xs(34), y_levels[1])
        tg3 = type_tag("vec3", xs(15), xs(34), y_levels[2])
        tg4 = type_tag("vec3", xs(9), xs(34), y_levels[3])
        until(self, "U V is a vec two", lead=0.3)
        self.play(Create(tg1.bracket), FadeIn(tg1.tag), run_time=0.45)
        until(self, "Joined with one half", lead=0.3)
        self.play(Create(tg2.bracket), FadeIn(tg2.tag), run_time=0.45)
        until(self, "Times a float", lead=0.3)
        self.play(Create(tg3.bracket), FadeIn(tg3.tag), run_time=0.45)
        until(self, "Plus a float", lead=0.3)
        self.play(Create(tg4.bracket), FadeIn(tg4.tag), run_time=0.45)
        # a final arrow into c, tagged vec3
        xc = xs(5.5)
        yb = y_levels[3]
        link = Line([xs(9), yb, 0], [xc, yb, 0], color=DIM, stroke_width=5)
        up = arrow([xc, yb, 0], [xc, yl - 0.4, 0], color=DIM)
        ctag = a2_tag("vec3", xc - 1.0, (yb + yl) / 2.0)
        self.play(Create(link), GrowArrow(up), FadeIn(ctag), run_time=0.6)
        done(self)
