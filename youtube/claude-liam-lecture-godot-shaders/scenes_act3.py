"""ACT III · The Three Functions  (B15, B17, B18, B19, B22, B23: Manim; B16/B20/B21 are captures, B24 a table)

Cast for the act: the test rectangle with four terracotta corner dots (B15, B18), the pixel grid of outline cells (B18), the leaning square's
left edge (B17, five REAL measured shifts from evidence/planning-checks/lean-edge.txt), a teal fragment token (B19, B22).
Drawings are drawings: B18's grid is not to scale, B17's edge is drawn from measured numbers.
"""


def a3_row(items, y, gap=0.3, cx=0.0):
    """Centre a row of mobjects horizontally at cx with explicit gaps (no Pango spacing involved)."""
    total = sum(m.width for m in items) + gap * (len(items) - 1)
    x = cx - total / 2.0
    for m in items:
        m.move_to([x + m.width / 2.0, y, 0])
        x += m.width + gap
    return VGroup(*items)


# ═════════════════════════════ B15 · vertex runs once per corner ═════════════════════════════
class B15_FourCorners(Scene):
    def construct(self):
        title = T("The Three Functions", 40).to_corner(UL, buff=0.95)
        q = vertex_quad(4.6, 2.5, 0.0, 0.1)
        lab = M("vertex() runs", 32)
        num = T("1", 56)
        row = a3_row([lab, num], -1.75, gap=0.55)
        cap = T("its job: place the corners", 36).move_to([0, -2.75, 0])
        self.add(title)
        self.play(Create(q.body), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(c, scale=0.4) for c in q.corners], lag_ratio=0.2), run_time=0.9)
        until(self, "once for each vertex")
        self.play(FadeIn(lab), run_time=0.3)
        for i, c in enumerate(q.corners):
            new = T(str(i + 1), 56).move_to(num.get_center()) if i else num
            if i == 0:
                self.play(FadeIn(num), Indicate(c, scale_factor=2.0, color=TERRA), run_time=0.6)
            else:
                self.play(Indicate(c, scale_factor=2.0, color=TERRA), Transform(num, new), run_time=0.6)
            self.wait(0.15)
        until(self, "Its job")
        self.play(FadeIn(cap, shift=UP * 0.15), run_time=0.5)
        done(self)


# ═════════════════════════════ B17 · even steps down the edge (five real measurements) ═════════════════════════════
class B17_EvenSteps(Scene):
    def construct(self):
        # measured (lean-edge.txt, white-square render, left edge x at rows 0.02/0.25/0.50/0.75/0.98; first row 256):
        # x = 257, 268, 281, 293, 305  ->  shifts +1, +12, +25, +37, +49 px (rounded to whole pixels, as measured)
        meas = [(0.02, 257), (0.25, 268), (0.50, 281), (0.75, 293), (0.98, 305)]
        shifts = [x - 256 for _, x in meas]
        assert shifts == [1, 12, 25, 37, 49]
        H = 4.0                                    # 128 rows drawn 4.0 units tall (31.25 rows per unit)
        k = H / 128.0                              # units per pixel, same scale both ways
        top = np.array([-1.7, 1.95, 0.0])
        bot = top + np.array([50 * k, -H, 0.0])
        guide = DashedLine(top, top + np.array([0, -H, 0]), color=DIM, stroke_width=4, dash_length=0.18)
        edge = Line(top, bot, color=INK, stroke_width=7)
        ttl = T("left edge", 36).move_to([top[0] + 0.1, top[1] + 0.5, 0])
        gl = T("not leaned", 32, DIM).move_to([top[0] - 1.1, top[1] - 0.4, 0])
        self.add(ttl)
        until(self, "Between the corners", lead=0.0)
        self.play(Create(guide), run_time=0.6)
        self.play(Create(edge), FadeIn(gl), run_time=0.9)
        until(self, "The left edge slides evenly")
        dots, labs = [], []
        for (f, _), s in zip(meas, shifts):
            p = top + (bot - top) * f
            d = Dot(p, radius=0.16, color=TERRA).set_stroke(DIM, width=3)
            lb = M("+%d px" % s, 32).move_to([p[0] + 1.75, p[1], 0])
            ln = Line(p + np.array([0.28, 0, 0]), p + np.array([0.62, 0, 0]), color=DIM, stroke_width=4)
            dots.append(d); labs.append(lb)
            self.play(FadeIn(d, scale=0.4), Create(ln), FadeIn(lb, shift=LEFT * 0.2), run_time=0.7)
            self.wait(0.1)
        cap = a3_row([T("four corners", 36), arrow([0, 0, 0], [0.9, 0, 0]), T("straight edges", 36)], -2.9, gap=0.3, cx=0.0)
        until(self, "Four corners can only")
        self.play(FadeIn(cap, shift=UP * 0.15), run_time=0.5)
        done(self)


# ═════════════════════════════ B18 · fragment runs once per covered pixel ═════════════════════════════
class B18_FillIn(Scene):
    def construct(self):
        cell = 0.55
        g = pixel_grid(14, 6, cell, 0.0, 0.1, color=DIM, sw=2)
        q = vertex_quad(4.4, 2.2, 0.0, 0.1)
        tag = M("fragment()", 32)
        tag.move_to([0, 2.95, 0])
        lab = T("every covered pixel", 36).move_to([0, -2.55, 0])
        self.add(g)
        self.play(Create(q.body), run_time=0.7)
        self.play(LaggedStart(*[FadeIn(c, scale=0.4) for c in q.corners], lag_ratio=0.15), run_time=0.6)
        # covered cells in reading order
        xs = [p[0] for p in q.pts]; ys = [p[1] for p in q.pts]
        cov = []
        for r in range(g.rows):
            for c in range(g.cols):
                p = g.cells[r][c].get_center()
                if min(xs) <= p[0] <= max(xs) and min(ys) <= p[1] <= max(ys):
                    cov.append((r, c))
        first = [rc for rc in cov if rc[0] == cov[0][0]]
        rest = [rc for rc in cov if rc[0] != cov[0][0]]
        until(self, "It runs once for each pixel")
        pc = g.cells[first[0][0]][first[0][1]].get_center()
        tag.move_to([pc[0], 2.95, 0])
        ptr = Line([pc[0], 2.62, 0], [pc[0], pc[1] + cell * 0.5, 0], color=DIM, stroke_width=4)
        self.play(FadeIn(tag), Create(ptr), run_time=0.35)
        for (r, c) in first:
            pc = g.cells[r][c].get_center()
            nptr = Line([pc[0], 2.62, 0], [pc[0], pc[1] + cell * 0.5, 0], color=DIM, stroke_width=4)
            self.play(tag.animate.move_to([pc[0], 2.95, 0]), Transform(ptr, nptr), tint(g.cells[r][c], TEAL, 0.9), run_time=0.26, rate_func=linear)
        self.play(LaggedStart(*[tint(g.cells[r][c], TEAL, 0.9) for (r, c) in rest], lag_ratio=0.08), run_time=1.5)
        until(self, "The shape is already decided")
        self.play(FadeIn(lab, shift=UP * 0.15), run_time=0.5)
        done(self)


# ═════════════════════════════ B19 · two names, one job ═════════════════════════════
class B19_TwoNames(Scene):
    def construct(self):
        bx = box(2.9, 1.75, 3.6, 1.3, DIM, 5, fill=PALEBOX)
        same = T("same job", 36).move_to(bx.get_center())
        l1 = T("pixel shader", 36)
        l2 = T("fragment shader", 36)
        l1.move_to([-3.9, 2.4, 0]); l2.move_to([-3.9, 1.1, 0])
        a1 = arrow([-2.2, 2.4, 0], [1.0, 1.95, 0], DIM, 5)
        a2 = arrow([-2.2, 1.1, 0], [1.0, 1.55, 0], DIM, 5)
        self.add(bx, same)
        self.play(FadeIn(l1, shift=RIGHT * 0.9), FadeIn(l2, shift=RIGHT * 0.9), run_time=0.8)
        self.play(GrowArrow(a1), GrowArrow(a2), run_time=0.7)
        # the strip: fragment -> tests, blending -> pixel
        y = -0.95
        bs = [box(-4.2, y, 2.5, 1.0, DIM, 4, fill=PALEBOX), box(0.0, y, 3.9, 1.0, DIM, 4, fill=PALEBOX), box(4.3, y, 1.9, 1.0, DIM, 4, fill=PALEBOX)]
        ts = [T("fragment", 36).move_to([-4.2, y, 0]), T("tests, blending", 36).move_to([0.0, y, 0]), T("pixel", 36).move_to([4.3, y, 0])]
        ar = [arrow([-2.8, y, 0], [-2.2, y, 0], INK, 5, 0.2), arrow([2.1, y, 0], [2.75, y, 0], INK, 5, 0.2)]
        until(self, "Microsoft")
        self.play(*[Create(b) for b in bs], *[FadeIn(t) for t in ts], run_time=0.8)
        self.play(*[GrowArrow(a) for a in ar], run_time=0.5)
        cap = T("a fragment is a pixel-to-be", 36).move_to([0, -2.7, 0])
        tok = Circle(radius=0.22, stroke_color=TEAL, stroke_width=6).move_to([-4.2, -0.05, 0])
        until(self, "The careful word")
        self.play(FadeIn(tok, scale=0.4), run_time=0.4)
        until(self, "because a fragment", lead=1.2)
        self.play(tok.animate.move_to([0.0, -0.05, 0]), run_time=0.9)
        self.play(tok.animate.move_to([4.3, -0.05, 0]), run_time=0.9)
        self.play(tok.animate.set_fill(TEAL, opacity=1), FadeIn(cap, shift=UP * 0.15), run_time=0.6)
        done(self)


# ═════════════════════════════ B22 · the fixed order ═════════════════════════════
def a3_ubar(mob, pad=0.08):
    """terracotta underline bar over a grey backing (a bar, never text): the emphasis mark that does not read as accent text"""
    w = mob.width + 2 * pad
    return VGroup(Rectangle(width=w, height=0.2, stroke_width=0).set_fill(DIM, opacity=0.55).move_to(mob.get_bottom() + DOWN * 0.18),
                  Rectangle(width=w, height=0.12, stroke_width=0).set_fill(TERRA, opacity=1).move_to(mob.get_bottom() + DOWN * 0.18))


class B22_Order(Scene):
    def construct(self):
        xs = [-4.35, 0.0, 4.35]
        y = 0.9
        bxs = [box(x, y, 3.4, 1.9, DIM, 5, fill=PALEBOX) for x in xs]
        top = [M("vertex()", 32), T("the GPU", 36), M("fragment()", 32)]
        bot = [T("places corners", 36), T("fills the shape", 36), T("colors pixels", 36)]
        grp = []
        for x, t, b in zip(xs, top, bot):
            t.move_to([x, y + 0.38, 0]); b.move_to([x, y - 0.4, 0])
            grp.append(VGroup(t, b))
        ar = [arrow([-2.55, y, 0], [-1.8, y, 0], INK, 6, 0.24), arrow([1.8, y, 0], [2.55, y, 0], INK, 6, 0.24)]
        track = Line([-4.35, -1.1, 0], [4.35, -1.1, 0], color=GHOST, stroke_width=6)
        tok = sprite_icon(-4.35, -1.1, 0.34)
        self.add(track)
        until(self, "order of work", lead=0.0)
        self.play(*[Create(b) for b in bxs], *[FadeIn(g) for g in grp], run_time=0.8)
        self.play(*[GrowArrow(a) for a in ar], FadeIn(tok), run_time=0.6)
        until(self, "First vertex")
        r1 = a3_ubar(bxs[0], pad=0.1)
        self.play(FadeIn(r1), run_time=0.3)
        until(self, "Then the card")
        r2 = a3_ubar(bxs[1], pad=0.1)
        self.play(tok.animate.move_to([0.0, -1.1, 0]), FadeOut(r1), FadeIn(r2), run_time=0.9)
        until(self, "Then fragment")
        r3 = a3_ubar(bxs[2], pad=0.1)
        self.play(tok.animate.move_to([4.35, -1.1, 0]), FadeOut(r2), FadeIn(r3), run_time=0.9)
        # never back: a grey backward arrow with a prohibition mark
        back = arrow([3.2, -2.25, 0], [-0.6, -2.25, 0], DIM, 6, 0.24)
        no = a1_no_mark(-1.35, -2.25)
        fwd = T("forward only", 36).move_to([2.1, -2.95, 0])
        until(self, "Information flows")
        self.play(GrowArrow(back), FadeIn(no), FadeIn(fwd), run_time=0.6)
        done(self)


def a1_no_mark(x, y, r=0.3, sw=6):
    """A prohibition mark in grey: ring + bar (series idiom), sits beside an arrow."""
    rg = Circle(radius=r, stroke_color=DIM, stroke_width=sw).move_to([x, y, 0])
    d = r * 0.7071
    bar = Line([x - d, y + d, 0], [x + d, y - d, 0], color=DIM, stroke_width=sw)
    return VGroup(rg, bar)


# ═════════════════════════════ B23 · built-ins in, color out ═════════════════════════════
class B23_FunctionBox(Scene):
    def construct(self):
        y0 = 0.35
        fb = box(0.0, y0, 3.6, 2.4, INK, 5)
        fl = M("fragment()", 32).move_to([0.0, y0, 0])
        ins = [("UV", 1.25), ("TIME", 0.35), ("TEXTURE", -0.55)]
        groups = []
        for name, dy in ins:
            lb = M(name, 32)
            lb.move_to([-5.8 + lb.width / 2.0, y0 + dy + 0.0, 0])
            ar = arrow([-3.0, y0 + dy, 0], [-1.95, y0 + dy, 0], INK, 6, 0.22)
            groups.append(VGroup(lb, ar))
        out_ar = arrow([1.95, y0, 0], [3.5, y0, 0], INK, 6, 0.22)
        out_lb = M("COLOR", 32)
        out_lb.move_to([3.7 + out_lb.width / 2.0, y0, 0])
        cap = a3_row([T("built-ins", 36), Dot(radius=0.07, color=INK), T("capital letters", 36)], -2.55, gap=0.3)
        self.play(Create(fb), FadeIn(fl), run_time=0.8)
        until(self, "called built-ins")
        self.play(FadeIn(cap, shift=UP * 0.15), run_time=0.5)
        until(self, "Some come in")
        for g in groups:
            self.play(FadeIn(g, shift=RIGHT * 0.8), run_time=0.7)
            self.wait(0.15)
        until(self, "One goes out")
        self.play(GrowArrow(out_ar), FadeIn(out_lb, shift=RIGHT * 0.3), run_time=0.7)
        done(self)
