"""ACT III · Your Own Functions  (B20, B21, B23, B25 Manim; B22/B24 are other lanes)

Cast: the `soften` function box with its signature; three-cell bundle tokens travelling in and out; the wall between fragment() and your function.
All drawings; the only real text is code and the engine's own message (Lab 45-err-return-type, quoted word for word).
"""


def a3_mono(s, size, xl, y):
    """Monospace line placed by its LEFT edge; .xl, .cw (measured char width) let a3_x find a column."""
    m = M(s, size)
    m.move_to([xl + m.width / 2.0, y, 0])
    m.xl = xl
    m.cw = {32: 0.2461, 36: 0.2950, 40: 0.3440}.get(size, size * 0.0077)   # measured Menlo advance (fixed, so Gate A's stub text agrees)
    return m


def a3_x(m, col):
    return m.xl + col * m.cw


def a3_tag(text, x0, x1, y, up=False, dy=0.55, shift=0.0, size=32):
    """A drawn bracket from x0 to x1 at height y with a stem to an outlined tag. up=False: bracket under the text (ticks point up); up=True: above it."""
    d = 1 if up else -1
    tk = -d * 0.14
    br = VGroup(Line([x0, y, 0], [x1, y, 0], color=DIM, stroke_width=5), Line([x0, y, 0], [x0, y + tk, 0], color=DIM, stroke_width=5),
                Line([x1, y, 0], [x1, y + tk, 0], color=DIM, stroke_width=5))
    t = T(text, size)
    xm = (x0 + x1) / 2.0
    cy = y + d * dy
    tagbox = RoundedRectangle(width=t.width + 0.4, height=t.height + 0.3, corner_radius=0.12, stroke_color=INK, stroke_width=3).set_fill(PALEBOX, opacity=1)
    tg = VGroup(tagbox, t).move_to([xm + shift, cy, 0])
    stem = Line([xm, y, 0], [xm + shift, cy - d * tagbox.height / 2, 0], color=DIM, stroke_width=4)
    g = VGroup(br, stem, tg)
    g.br = br; g.stem = stem; g.tag = tg; g.d = d
    return g


def a3_show(self, g, rt=0.5):
    self.play(AnimationGroup(Create(g.br), FadeIn(g.stem), FadeIn(g.tag, shift=UP * g.d * 0.15), lag_ratio=0.35), run_time=rt)


def a3_tok(n, x, y, color=TEAL, cell=0.28, gap=0.07):
    """A bundle token: n separate cells (the series' bundle). No text inside, so a fill is fine."""
    cs = VGroup(*[Square(side_length=cell, fill_color=color, fill_opacity=1, stroke_width=0).move_to([(i - (n - 1) / 2.0) * (cell + gap), 0, 0]) for i in range(n)])
    return cs.move_to([x, y, 0])


# ═════════════════════════════ B20 · the signature ═════════════════════════════
class B20_Signature(Scene):
    def construct(self):
        title = T("Your Own Functions", 40).to_corner(UL, buff=0.95)
        xl = -3.9
        l1 = a3_mono("vec3 soften(vec3 c) {", 40, xl, 1.6)
        l2 = a3_mono("    return 0.4 + 0.6 * c;", 40, xl, -1.3)
        l3 = a3_mono("}", 40, xl, -2.0)
        cap = T("signature: the first line of a function", 32).move_to([0, -3.0, 0])
        self.play(FadeIn(title), FadeIn(l1), run_time=0.5)
        self.play(FadeIn(l2), FadeIn(l3), run_time=0.4)
        self.play(FadeIn(cap), run_time=0.4)
        yb = 1.18
        t1 = a3_tag("hands back", a3_x(l1, 0), a3_x(l1, 4), yb, dy=0.62)
        t2 = a3_tag("name", a3_x(l1, 5), a3_x(l1, 11), yb, dy=0.62)
        t3 = a3_tag("arguments, each with a type", a3_x(l1, 11), a3_x(l1, 19), yb, dy=1.45)
        until(self, "It has three parts", lead=0.1)
        a3_show(self, t1, 0.5)
        until(self, "the type it hands back", lead=0.2)
        a3_show(self, t2, 0.5)
        until(self, "its arguments", lead=0.5)
        a3_show(self, t3, 0.6)
        done(self)


# ═════════════════════════════ B21 · call and return ═════════════════════════════
class B21_CallAndReturn(Scene):
    def construct(self):
        call = a3_mono("soften(vec3(UV, 0.5))", 32, -6.0, 2.3)
        body = M("return 0.4 + 0.6 * c;", 32).move_to([3.25, 2.3, 0])
        fbox = box(3.2, 2.3, 5.95, 1.1, color=INK, sw=4)
        slot = Square(side_length=0.62, stroke_color=INK, stroke_width=4).move_to([0.95, 1.4, 0])
        cc = M("c", 32).move_to(slot.get_center())
        func = VGroup(fbox, body)
        self.play(FadeIn(call), FadeIn(func), FadeIn(slot), FadeIn(cc), run_time=0.6)
        path1 = DashedLine([-3.4, 1.4, 0], [0.55, 1.4, 0], color=DIM, stroke_width=4)
        tok = a3_tok(3, -3.4, 1.4)
        until(self, "hands values into", lead=0.6)
        self.play(Create(path1), FadeIn(tok), run_time=0.4)
        self.play(tok.animate.move_to([0.95, 1.4, 0]), run_time=0.9)
        until(self, "The body runs", lead=0.1)
        self.play(FadeOut(tok), func.animate.scale(1.05), run_time=0.3)
        self.play(func.animate.scale(1 / 1.05), run_time=0.3)
        # the bundle comes back, tagged
        path2 = DashedLine([4.2, 1.7, 0], [4.2, 0.55, 0], color=DIM, stroke_width=4)
        path3 = DashedLine([4.2, 0.55, 0], [-3.4, 0.55, 0], color=DIM, stroke_width=4)
        tok2 = a3_tok(3, 4.2, 1.7)
        until(self, "return hands one value back", lead=1.4)
        self.play(FadeIn(tok2), Create(path2), run_time=0.25)
        self.play(tok2.animate.move_to([4.2, 0.55, 0]), Create(path3), run_time=0.3)
        self.play(tok2.animate.move_to([-3.4, 0.55, 0]), run_time=0.8)
        back = T("vec3, as promised", 32).move_to([-3.4, 0.0, 0])
        self.play(FadeIn(back, shift=UP * 0.1), run_time=0.4)
        # the wrong size bounces
        until(self, "Break that promise", lead=1.2)
        bar = Line([-1.7, -1.55, 0], [-1.7, -0.45, 0], color=DIM, stroke_width=16)
        cross = VGroup(Line([-2.1, -0.75, 0], [-1.3, -1.25, 0], color=INK, stroke_width=6), Line([-2.1, -1.25, 0], [-1.3, -0.75, 0], color=INK, stroke_width=6))
        tok4 = VGroup(a3_tok(4, 0, 0), T("vec4", 32).move_to([0, -0.45, 0])).move_to([5.35, 1.7, 0])
        self.play(FadeIn(bar), FadeIn(tok4), run_time=0.3)
        self.play(tok4.animate.move_to([5.35, -1.0, 0]), run_time=0.4)
        self.play(tok4.animate.move_to([-0.7, -1.0, 0]), run_time=0.6)
        self.play(Create(cross), tok4.animate.move_to([0.9, -1.0, 0]), run_time=0.4)
        m1 = a3_mono("Expected return with an expression", 32, -6.0, -2.15)
        m2 = a3_mono("of type 'vec3'.", 32, -6.0, -2.65)
        self.play(FadeIn(m1), FadeIn(m2), run_time=0.4)
        done(self)


# ═════════════════════════════ B23 · the wall ═════════════════════════════
class B23_TheWall(Scene):
    def construct(self):
        frag = box(3.6, 0.5, 4.6, 3.3, color=INK, sw=4)
        flab = M("fragment()", 32).move_to([3.6, 1.7, 0])
        chips = []
        for i, w in enumerate(["UV", "COLOR", "TEXTURE"]):
            tx = M(w, 32)
            cb = RoundedRectangle(width=tx.width + 0.4, height=0.6, corner_radius=0.12, stroke_color=INK, stroke_width=3)
            ch = VGroup(cb, tx).move_to([3.6, 0.85 - i * 0.8, 0])
            chips.append(ch)
        soft = box(-3.6, 0.5, 4.0, 3.3, color=INK, sw=4)
        slab = M("soften()", 32).move_to([-3.6, 1.7, 0])
        mine = T("your own", 32).move_to([-3.6, -0.3, 0])
        wall = Line([0, -1.3, 0], [0, 2.2, 0], color=DIM, stroke_width=26)
        self.play(FadeIn(frag), FadeIn(flab), FadeIn(soft), FadeIn(slab), FadeIn(mine), *[FadeIn(c) for c in chips], run_time=0.6)
        self.play(FadeIn(wall), run_time=0.4)
        cap1 = T("built-in: a value the engine hands to a function, or collects from it", 32).move_to([0, -2.5, 0])
        until(self, "A built-in is a value", lead=0.2)
        self.play(FadeIn(cap1), run_time=0.5)
        uv = chips[0]
        until(self, "Use U V inside yours", lead=0.3)
        self.play(uv.animate.move_to([0.95, 0.85, 0]), run_time=0.8, rate_func=linear)
        self.play(uv.animate.move_to([2.6, 0.85, 0]), run_time=0.5)
        self.play(uv.animate.move_to([3.6, 0.85, 0]), run_time=0.4)
        bub = RoundedRectangle(width=3.7, height=0.7, corner_radius=0.3, stroke_color=INK, stroke_width=4).move_to([-0.2, 2.78, 0])
        bt = T("unknown identifier", 32).move_to(bub.get_center())
        tail = Polygon([-0.05, 2.43, 0], [0.2, 2.43, 0], [0.0, 2.15, 0], stroke_color=INK, stroke_width=4, fill_opacity=0)
        until(self, "Godot says unknown identifier", lead=0.1)
        self.play(FadeIn(bub), FadeIn(bt), FadeIn(tail), run_time=0.4)
        done(self)


# ═════════════════════════════ B25 · in, inout, out ═════════════════════════════
def a3_chip(word, cap, xl):
    """A mode chip (outlined, monospace word) with a one-to-three-word caption to its right. Returns VGroup with .chip."""
    tx = M(word, 32)
    cb = RoundedRectangle(width=tx.width + 0.4, height=0.62, corner_radius=0.12, stroke_color=INK, stroke_width=3)
    chip = VGroup(cb, tx).move_to([xl + cb.width / 2.0, 2.75, 0])
    c = T(cap, 32).move_to([xl + cb.width + 0.3, 2.75, 0])
    c.shift(RIGHT * c.width / 2.0)
    g = VGroup(chip, c)
    g.chip = chip
    return g


class B25_InOutInout(Scene):
    def construct(self):
        YA, YC = 0.55, -1.4
        c1 = a3_chip("in", "a copy", -6.0)
        c2 = a3_chip("inout", "the original", -2.6)
        c3 = a3_chip("out", "writes back", 2.7)
        scard = box(-1.0, YC, 7.0, 0.95, color=INK, sw=4)
        sig_in = a3_mono("float bump(float x)", 32, -3.4, YC)
        sig_io = a3_mono("void bump(inout float x)", 32, -4.0, YC)
        sig_o = a3_mono("void make(out vec3 c)", 32, -3.6, YC)
        a_box = box(-4.3, YA, 2.5, 0.8, color=INK, sw=4)
        a_t = M("a = 0.25", 32).move_to(a_box.get_center())
        b_box = box(4.3, YA, 2.5, 0.8, color=INK, sw=4)
        b_t = M("b = 0.75", 32).move_to(b_box.get_center())
        self.play(FadeIn(c1), FadeIn(c2), FadeIn(c3), FadeIn(a_box), FadeIn(a_t), FadeIn(scard), FadeIn(sig_in), run_time=0.6)
        rg = ring(c1.chip)
        self.play(FadeIn(rg), run_time=0.3)
        # IN: a ghost copy goes in, changes, comes back to b; a stays
        until(self, "hands over a copy", lead=0.5)
        ghost = M("0.25", 32)
        gbox = RoundedRectangle(width=1.5, height=0.6, corner_radius=0.12, stroke_color=DIM, stroke_width=3)
        gh = VGroup(gbox, ghost).move_to([-2.2, YA, 0])
        self.play(FadeIn(gh), run_time=0.25)
        self.play(gh.animate.move_to([-1.0, YC + 0.95, 0]), run_time=0.5)
        g2 = M("0.75", 32).move_to(gh.get_center())
        self.play(Transform(ghost, g2), run_time=0.3)
        self.play(gh.animate.move_to([2.3, YA, 0]), run_time=0.55)
        self.play(FadeOut(gh), FadeIn(b_box), FadeIn(b_t), run_time=0.3)
        # INOUT: a double-headed arrow ties the function to the original itself; a changes
        until(self, "In out hands over the original", lead=0.3)
        rg2 = ring(c2.chip)
        io_arrow = dim_arrow([-4.3, YC + 0.5, 0], [-4.3, YA - 0.45, 0], color=INK, w=6, tip=0.2)
        a_t2 = M("a = 0.75", 32).move_to(a_box.get_center())
        self.play(FadeOut(b_box), FadeOut(b_t), Transform(rg, rg2), Transform(sig_in, sig_io), run_time=0.4)
        self.play(FadeIn(io_arrow), run_time=0.3)
        self.play(Transform(a_t, a_t2), run_time=0.4)
        # OUT: the function writes into an empty three-cell box
        until(self, "Out is for writing", lead=0.4)
        rg3 = ring(c3.chip)
        cbox = VGroup(*[Rectangle(width=0.95, height=0.8, stroke_color=INK, stroke_width=4).move_to([-4.0 + (i - 1) * 0.95, YA, 0]) for i in range(3)])
        cname = M("c", 32).move_to([-5.75, YA, 0])
        self.play(FadeOut(a_box), FadeOut(a_t), FadeOut(io_arrow), Transform(rg, rg3), Transform(sig_in, sig_o), run_time=0.4)
        self.play(FadeIn(cbox), FadeIn(cname), run_time=0.3)
        wr = arrow([-4.0, YC + 0.5, 0], [-4.0, YA - 0.45, 0], color=INK, w=6, tip=0.2)
        vals = VGroup(*[M(v, 32).move_to(cbox[i].get_center()) for i, v in enumerate(["0.1", "0.5", "0.9"])])
        self.play(FadeIn(wr), run_time=0.25)
        self.play(FadeIn(vals, lag_ratio=0.3), run_time=0.6)
        done(self)
