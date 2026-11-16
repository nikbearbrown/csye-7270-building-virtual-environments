"""Act I · Corners (B02, B03, B04, B08, B10; B01/B05-B07/B09 are captures). Manim only, kit objects.
Cast: the test rectangle with four terracotta corner dots. Numbers are the measured ones (CAPTURE-PLAN, evidence/planning-checks/measurements.txt)."""


def a1_at(mob, x, y, left=False, right=False):
    """Place a mob by an edge: left=True puts its left edge at x, right=True its right edge at x; else centred."""
    if left:
        mob.move_to([x + mob.width / 2.0, y, 0])
    elif right:
        mob.move_to([x - mob.width / 2.0, y, 0])
    else:
        mob.move_to([x, y, 0])
    return mob


def a1_dot(p):
    return Dot(np.array(p, dtype=float), radius=0.16, color=TERRA).set_stroke(DIM, width=3)


# ═════════════════════════ B02 · four corners ═════════════════════════
class B02_FourCorners(Scene):
    def construct(self):
        self.camera.background_color = STAGE
        W, H, cy = 4.4, 2.6, 0.3
        P0 = [np.array(p, dtype=float) for p in ([-W / 2, cy + H / 2, 0], [W / 2, cy + H / 2, 0], [W / 2, cy - H / 2, 0], [-W / 2, cy - H / 2, 0])]
        dots = [a1_dot(p) for p in P0]
        body = Polygon(*P0, stroke_color=INK, stroke_width=5)
        offs = [np.array(o) for o in ([-0.42, 0.38, 0], [0.42, 0.38, 0], [0.42, -0.38, 0], [-0.42, -0.38, 0])]
        nums = [T(str(i + 1), 36).move_to(P0[i] + offs[i]) for i in range(4)]
        cap = T("vertex(): runs once for each vertex; places the corners", 32).move_to([0, -2.75, 0])
        self.add(body)
        self.play(FadeIn(VGroup(*dots)), FadeIn(cap), run_time=0.7)
        self.wait(0.3)
        for i in range(4):
            self.play(FadeIn(nums[i], run_time=0.2), Indicate(dots[i], scale_factor=1.9, color=TERRA), run_time=0.55)
        until(self, "where does this corner go", lead=2.6)
        q = T("where?", 36).move_to([0, cy, 0])
        self.play(FadeIn(q), run_time=0.3)
        until(self, "where does this corner go", lead=0.2)
        P1 = [[-1.4, cy + H / 2, 0], [3.0, cy + H / 2, 0], [1.7, cy - H / 2, 0], [-2.7, cy - H / 2, 0]]
        trails = VGroup(*[Line(np.array(P0[i]), np.array(P1[i], dtype=float), color=DIM, stroke_width=4) for i in range(4)])
        newbody = Polygon(*[np.array(p, dtype=float) for p in P1], stroke_color=INK, stroke_width=5)
        self.play(FadeOut(q), Create(trails), Transform(body, newbody), *[dots[i].animate.move_to(P1[i]) for i in range(4)],
                  *[nums[i].animate.move_to(np.array(P1[i], dtype=float) + offs[i]) for i in range(4)], run_time=1.5, rate_func=smooth)
        done(self)


# ═════════════════════════ B03 · in and out ═════════════════════════
class B03_InAndOut(Scene):
    def construct(self):
        self.camera.background_color = STAGE
        bx = box(0, 0.65, 5.7, 2.5, color=INK, sw=4)
        title = M("vertex()", 32).move_to([0, 1.5, 0])
        code = M("VERTEX.x += 40.0;", 32).move_to([0, 0.85, 0])
        cap = T("built-in: a value the engine hands to a function", 32).move_to([0, -2.75, 0])
        self.play(Create(bx), FadeIn(title), FadeIn(code), FadeIn(cap), run_time=0.9)
        yy = 0.0
        ghost = Dot([-4.5, yy, 0], radius=0.2, color=DIM)
        d = Dot([-6.0, yy, 0], radius=0.2, color=TERRA).set_stroke(DIM, width=3)
        nm = M("VERTEX", 32).move_to([-4.5, yy + 0.6, 0])
        lab_in = M("(-64, -64)", 32).move_to([-4.5, yy - 0.6, 0])
        self.play(d.animate.move_to([-4.5, yy, 0]), FadeIn(ghost), FadeIn(nm), FadeIn(lab_in), run_time=1.0, rate_func=smooth)
        self.remove(ghost); self.add(ghost)
        until(self, "a value it gives", lead=0.0)
        hl = VGroup(Rectangle(width=code.width + 0.3, height=0.2, stroke_width=0).set_fill(DIM, opacity=0.55).next_to(code, DOWN, buff=0.08), Rectangle(width=code.width + 0.3, height=0.12, stroke_width=0).set_fill(TERRA, opacity=1).next_to(code, DOWN, buff=0.12))  # terracotta underline bar over a grey backing (a bar, never text)
        self.play(d.animate.move_to([4.5, yy, 0]), FadeIn(hl), run_time=1.6, rate_func=linear)
        lab_out = M("(-24, -64)", 32).move_to([4.5, yy - 0.6, 0])
        nm2 = M("VERTEX", 32).move_to([4.5, yy + 0.6, 0])
        self.play(FadeIn(lab_out), FadeIn(nm2), FadeOut(hl), run_time=0.4)
        until(self, "Whatever you leave", lead=0.1)
        self.play(Indicate(d, scale_factor=1.7, color=TERRA), run_time=0.6)
        done(self)


# ═════════════════════════ B04 · pixels from the middle ═════════════════════════
class B04_PixelsFromTheMiddle(Scene):
    def construct(self):
        self.camera.background_color = STAGE
        S, cy = 2.8, 0.2
        sq = Square(side_length=S, stroke_color=INK, stroke_width=5).move_to([0, cy, 0])
        cross = VGroup(Line([-0.2, cy, 0], [0.2, cy, 0], color=INK, stroke_width=5), Line([0, cy - 0.2, 0], [0, cy + 0.2, 0], color=INK, stroke_width=5))
        ax = arrow([0.25, cy, 0], [2.5, cy, 0], color=INK, w=5)
        ay = arrow([0, cy - 0.25, 0], [0, cy - 2.2, 0], color=INK, w=5)
        lx = T("x", 36).move_to([2.8, cy, 0]); ly = T("y", 36).move_to([0.85, cy - 2.0, 0])
        bar = dim_arrow([-S / 2, 2.05, 0], [S / 2, 2.05, 0], color=DIM)
        bl = T("128 px", 32).move_to([0, 2.55, 0])
        credit = T("measured in Godot 4.7.2 · Forward+", 32, DIM).move_to([0, -3.0, 0])
        self.play(Create(sq), FadeIn(cross), FadeIn(bar), FadeIn(bl), run_time=0.8)
        self.play(GrowArrow(ax), GrowArrow(ay), FadeIn(lx), FadeIn(ly), FadeIn(credit), run_time=0.8)
        until(self, "corners at minus", lead=0.4)
        h = S / 2
        specs = [("(-64, -64)", -h, cy + h, True), ("(64, -64)", h, cy + h, False), ("(-64, 64)", -h, cy - h, True), ("(64, 64)", h, cy - h, False)]
        dots = []
        for s, px, py, isl in specs:
            dt = a1_dot([px, py, 0])
            lb = M(s, 32)
            a1_at(lb, px - 0.35, py, right=True) if isl else a1_at(lb, px + 0.35, py, left=True)
            self.play(FadeIn(dt, scale=1.6), FadeIn(lb), run_time=0.45)
        until(self, "The y axis points down", lead=0.1)
        r = ring(ay, pad=0.18)
        self.play(FadeIn(r), run_time=0.5)
        self.play(Indicate(ly, scale_factor=1.5, color=INK), run_time=0.6)
        done(self)


# ═════════════════════════ B08 · the address ═════════════════════════
class B08_Address(Scene):
    def construct(self):
        self.camera.background_color = STAGE
        S, cy = 2.8, 0.3
        h = S / 2
        sq = Square(side_length=S, stroke_color=INK, stroke_width=5).move_to([0, cy, 0])
        cs = [(-h, cy + h, True, "(-64, -64)", "(0, 0)"), (h, cy + h, False, "(64, -64)", "(1, 0)"),
              (-h, cy - h, True, "(-64, 64)", "(0, 1)"), (h, cy - h, False, "(64, 64)", "(1, 1)")]
        pix = []; adr = []
        for x, y, isl, p, a in cs:
            pl = M(p, 32, DIM); al = M(a, 32, INK)
            if isl:
                a1_at(pl, x - 0.4, y + 0.3, right=True); a1_at(al, x - 0.4, y - 0.3, right=True)
            else:
                a1_at(pl, x + 0.4, y + 0.3, left=True); a1_at(al, x + 0.4, y - 0.3, left=True)
            pix.append(pl); adr.append(al)
        cd = [Dot([x, y, 0], radius=0.09, color=DIM) for x, y, *_ in cs]
        lg1 = T("pixels", 32, DIM).move_to([-1.3, -2.3, 0]); lg2 = T("address", 32, INK).move_to([1.3, -2.3, 0])
        cap = T("UV: a point's address on the shape: 0 to 1 across, 0 to 1 down", 32).move_to([0, -3.0, 0])
        self.play(Create(sq), FadeIn(VGroup(*cd)), FadeIn(VGroup(*pix)), FadeIn(lg1), run_time=0.9)
        until(self, "The engine gives each", lead=0.3)
        self.play(FadeIn(lg2), FadeIn(cap), run_time=0.5)
        walker = a1_dot([cs[0][0], cs[0][1], 0])
        self.play(FadeIn(walker, scale=1.5), FadeIn(adr[0]), run_time=0.4)
        for i in (1, 2, 3):
            self.play(walker.animate.move_to([cs[i][0], cs[i][1], 0]), run_time=0.5, rate_func=smooth)
            self.play(FadeIn(adr[i]), run_time=0.2)
        until(self, "Top left is zero", lead=0.1)
        r1 = ring(adr[0], pad=0.06, sw=6)
        self.play(FadeIn(r1), run_time=0.4)
        until(self, "Bottom right is one", lead=0.1)
        r2 = ring(adr[3], pad=0.06, sw=6)
        self.play(FadeIn(r2), run_time=0.4)
        done(self)


# ═════════════════════════ B10 · even steps ═════════════════════════
class B10_EvenSteps(Scene):
    def construct(self):
        self.camera.background_color = STAGE
        k = 3.6 / 128.0                     # one pixel row/column in scene units
        x0, ytop = -1.4, 1.95
        P = lambda shift, row: np.array([x0 + shift * k, ytop - row * k, 0])
        ref = DashedLine(P(0, 0), P(0, 128), color=DIM, stroke_width=4, dash_length=0.12)
        edge = Line(P(0, 0), P(50, 128), color=INK, stroke_width=6)
        self.play(Create(ref), run_time=0.6)
        self.play(Create(edge), run_time=1.2)
        until(self, "in even steps", lead=0.3)
        for shift, row in [(1, 2), (12, 31), (25, 63), (37, 95), (49, 124)]:
            d = a1_dot(P(shift, row))
            lb = T(f"+{shift} px", 32)
            a1_at(lb, P(shift, row)[0] + 0.4, P(shift, row)[1], left=True)
            self.play(FadeIn(d, scale=1.7), FadeIn(lb), run_time=0.4)
            self.wait(0.1)
        cap = T("four corners: straight edges", 36).move_to([0, -2.2, 0])
        until(self, "on a straight line", lead=0.3)
        self.play(FadeIn(cap), run_time=0.4)
        c1 = T("Apple M4 Pro · Godot 4.7.2 · Forward+", 32, DIM).move_to([0, -2.65, 0])
        c2 = T("straight to within half a pixel", 32, DIM).move_to([0, -3.05, 0])
        until(self, "to within half", lead=0.3)
        self.play(FadeIn(c1), FadeIn(c2), run_time=0.4)
        until(self, "Remember that", lead=0.1)
        self.play(Indicate(edge, color=TEAL, scale_factor=1.0), run_time=0.8)
        done(self)
