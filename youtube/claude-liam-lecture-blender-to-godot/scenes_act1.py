"""ACT I · One Column, Three Arrivals  (B01–B06 Manim; B07 is a Remotion LibraryIconRow, see lanes/act1.json)

One cast for the act: the COLUMN. B01 stands it up in isometric with its three dimensions. B03–B05 read it the way
Godot does, in a SIDE VIEW (Godot's Y up, Z across, X toward you): the same 0.2 x 1.8 x 0.2 m column arriving three ways.
Numbers on screen are the real probe output (evidence/probe/godot-mutations.log); nothing is invented.
"""

A1_U = 1.5                                    # side view: scene units per metre
A1_O = np.array([-3.3, -2.55, 0.0])           # side view: ground point under the column's bottom-right corner
A1_W, A1_H = 0.2, 1.8                         # the column, metres


def a1_ground():
    """Axes of the side view: Y up, Z across (Godot's), meeting at the left of the ground line."""
    y_ax = Arrow([-6.0, -2.55, 0], [-6.0, 1.05, 0], buff=0, color=INK, stroke_width=5, tip_length=0.22)
    z_ax = Arrow([-6.0, -2.55, 0], [-0.9, -2.55, 0], buff=0, color=INK, stroke_width=5, tip_length=0.22)
    ly = T("Y up", 34).move_to([-5.25, 1.1, 0])
    lz = T("Z", 34).move_to([-0.55, -2.55, 0])
    return y_ax, z_ax, ly, lz


def a1_rect(w_m, h_m, fill=BOX_L):
    """A column in the side view standing on the ground with its bottom-RIGHT corner at A1_O."""
    r = Rectangle(width=w_m * A1_U, height=h_m * A1_U, fill_color=fill, fill_opacity=1, stroke_color=INK, stroke_width=5)
    r.move_to(A1_O + np.array([-w_m * A1_U / 2, h_m * A1_U / 2, 0]))
    return r


def a1_chips(vals, x0=1.0, y=1.15, hi=None):
    """Three outlined cells X / Y / Z with their numbers. No fill behind text; `hi` rings one cell."""
    cells = VGroup()
    for i, (ax, v) in enumerate(zip("XYZ", vals)):
        x = x0 + i * 1.95
        box = RoundedRectangle(width=1.6, height=1.55, corner_radius=0.2, fill_opacity=0, stroke_color=INK if i == hi else DIM,
                               stroke_width=6 if i == hi else 4).move_to([x, y, 0])
        a = T(ax, 36, DIM).move_to([x, y + 0.42, 0])
        n = T(v, 62).move_to([x, y - 0.22, 0])
        cells.add(VGroup(box, a, n))
    return cells


def a1_logline(s, y=-2.45, x=2.5):
    return M(s, 32, DIM).move_to([x, y, 0])


# ── B01 · the column and its three dimensions ──────────────────────────────────────────────────────────────
class B01_Column(Scene):
    def construct(self):
        iso = Iso(-0.6, -2.3, 2.3)
        floor = iso.quad([(-0.5, -0.5, 0), (0.7, -0.5, 0), (0.7, 0.7, 0), (-0.5, 0.7, 0)], GHOST, stroke=GHOST, sw=0)
        col = iso.box(0, 0, 0, 0.2, 0.2, 1.8, top="#C7AE86", left="#A38C66", right="#8F7A57", sw=6)
        title = T("One Column, Three Arrivals", 40).move_to([-3.1, 3.05, 0])
        self.add(floor, col, title)
        until(self, "point two metres wide", lead=0.15)
        w_a = dim_arrow(iso.p(0, 0, 0) + np.array([0, -0.55, 0]), iso.p(0.2, 0, 0) + np.array([0, -0.55, 0]))
        w_l = T("0.2 m wide", 36).move_to([1.35, -3.1, 0])
        self.play(Create(w_a), FadeIn(w_l), run_time=0.5)
        until(self, "point two deep", lead=0.15)
        d_a = dim_arrow(iso.p(0, 0, 0) + np.array([-0.55, -0.35, 0]), iso.p(0, 0.2, 0) + np.array([-0.55, -0.35, 0]))
        d_l = T("0.2 m deep", 36).move_to([-3.05, -2.6, 0])
        self.play(Create(d_a), FadeIn(d_l), run_time=0.5)
        until(self, "one point eight metres tall", lead=0.15)
        h_a = dim_arrow(iso.p(0.2, 0, 0) + np.array([1.1, 0, 0]), iso.p(0.2, 0, 1.8) + np.array([1.1, 0, 0]))
        h_l = T("1.8 m tall", 36).move_to([2.45, -0.4, 0])
        self.play(Create(h_a), FadeIn(h_l), run_time=0.6)
        done(self)


# ── B02 · one script, three builds, one engine ───────────────────────────────────────────────────────────────
class B02_ThreeBuilds(Scene):
    def construct(self):
        bl = ImageMobject("pantry/icon_blender.png").set_height(1.5).move_to([-5.5, -0.25, 0])
        bl_l = T("Blender", 34).move_to([-5.5, -1.45, 0])
        self.add(bl, bl_l)
        xs = [-2.7, 0.2, 3.1]
        cols = VGroup(*[Iso(x, -2.15, 1.0).box(0, 0, 0, 0.2, 0.2, 1.8) for x in xs])
        shadows = VGroup(*[Iso(x, -2.15, 1.0).quad([(-0.3, -0.3, 0), (0.5, -0.3, 0), (0.5, 0.5, 0), (-0.3, 0.5, 0)], GHOST, stroke=GHOST, sw=0)
                           for x in xs])
        src = Arrow([-4.6, -0.25, 0], [-3.7, -0.25, 0], buff=0, color=INK, stroke_width=5, tip_length=0.2)
        self.play(FadeIn(shadows), Create(src), run_time=0.4)
        until(self, "three times", lead=0.3)
        for c in cols:
            self.play(FadeIn(c, shift=DOWN * 0.15), run_time=0.35)
        until(self, "changing one setting", lead=0.2)
        labs = [T("default", 32).move_to([xs[0] + 0.25, -2.85, 0]),
                T("Y up off", 32).move_to([xs[1] + 0.25, -2.85, 0]),
                T("scale not\napplied", 32).move_to([xs[2] + 0.25, -2.85, 0])]
        for l in labs:
            self.play(FadeIn(l), run_time=0.25)
        until(self, "Godot game engine", lead=1.0)
        to_g = Arrow([4.4, -0.25, 0], [4.85, -0.25, 0], buff=0, color=INK, stroke_width=5, tip_length=0.2)
        gd = ImageMobject("pantry/icon_godot.png").set_height(1.5).move_to([5.55, -0.25, 0])
        gd_l = T("Godot", 34).move_to([5.55, -1.45, 0])
        self.play(Create(to_g), FadeIn(gd), FadeIn(gd_l), run_time=0.5)
        done(self)


# ── B03 · the good arrival ──────────────────────────────────────────────────────────────────────────────────
class B03_Good(Scene):
    def construct(self):
        y_ax, z_ax, ly, lz = a1_ground()
        self.add(y_ax, z_ax, ly, lz)
        col = a1_rect(A1_W, A1_H)
        cap = T("bounding box, in metres", 36).move_to([2.6, 2.45, 0])
        self.play(GrowFromEdge(col, DOWN), FadeIn(cap), run_time=0.6)
        chips = a1_chips(["0.2", "1.8", "0.2"], hi=1)
        until(self, "point two, one point eight, point two", lead=0.2)
        self.play(FadeIn(chips[0]), run_time=0.3)
        self.play(FadeIn(chips[1]), run_time=0.3)
        self.play(FadeIn(chips[2]), run_time=0.3)
        until(self, "vertical axis", lead=0.6)
        ring = Dot([A1_O[0] - 0.15, A1_O[1] + 1.8 * A1_U + 0.2, 0], radius=0.12, color=TERRA)
        self.play(FadeIn(ring), run_time=0.3)
        until(self, "a scale of one", lead=0.2)
        sc = a1_logline("node scale (1.0, 1.0, 1.0)", y=-0.75)
        lg = a1_logline("mesh AABB size (0.2, 1.8, 0.2)", y=-1.5)
        self.play(FadeIn(sc), FadeIn(lg), run_time=0.4)
        done(self)


# ── B04 · the same column, Y-up off: it lies down ───────────────────────────────────────────────────────────────
class B04_LiesDown(Scene):
    def construct(self):
        y_ax, z_ax, ly, lz = a1_ground()
        col = a1_rect(A1_W, A1_H)
        cap = T("bounding box, in metres", 36).move_to([2.6, 2.45, 0])
        chips = a1_chips(["0.2", "1.8", "0.2"], hi=1)
        ring = Dot([A1_O[0] - 0.15, A1_O[1] + 1.8 * A1_U + 0.2, 0], radius=0.12, color=TERRA)
        sc = a1_logline("node scale (1.0, 1.0, 1.0)", y=-0.75)
        self.add(y_ax, z_ax, ly, lz, col, cap, chips, ring, sc)
        until(self, "lying on its side", lead=0.3)
        self.play(FadeOut(ring), Rotate(col, angle=-PI / 2, about_point=A1_O.copy()), run_time=1.0)
        lab = T("1.8 now along Z", 34).move_to([-3.7, -1.5, 0])
        self.play(FadeIn(lab), run_time=0.3)
        until(self, "the one point eight now sits on the depth axis", lead=0.2)
        newvals = a1_chips(["0.2", "0.2", "1.8"], hi=2)
        self.play(Transform(chips[1][2], newvals[1][2]), Transform(chips[2][2], newvals[2][2]),
                  chips[1][0].animate.set_stroke(DIM, 4), chips[2][0].animate.set_stroke(INK, 6), run_time=0.7)
        ring2 = Dot([1.0 + 2 * 1.95 + 0.62, 1.15 + 0.62, 0], radius=0.12, color=TERRA)
        self.play(FadeIn(ring2), run_time=0.3)
        until(self, "One setting about which way is up", lead=0.2)
        lg = a1_logline("mesh AABB size (0.2, 0.2, 1.8)", y=-1.5)
        self.play(FadeIn(lg), run_time=0.4)
        done(self)


# ── B05 · looks identical; the mesh is a two-metre cube wearing a scale ───────────────────────────────────────────
class B05_Disguise(Scene):
    def construct(self):
        y_ax, z_ax, ly, lz = a1_ground()
        col = a1_rect(A1_W, A1_H)
        cap = T("node scale", 36).move_to([2.6, 2.45, 0])
        self.add(y_ax, z_ax, ly, lz, col, cap)
        until(self, "But its mesh", lead=0.2)
        cube = Rectangle(width=2.0 * A1_U, height=2.0 * A1_U, fill_opacity=0, stroke_color=DIM, stroke_width=6)
        cube.move_to(A1_O + np.array([-0.1 * A1_U, 0.9 * A1_U, 0]))
        cl = T("mesh: 2 × 2 × 2 m", 36).move_to([-3.4, 1.7, 0])
        self.play(Create(cube), FadeIn(cl), run_time=0.8)
        until(self, "wearing a scale of", lead=0.2)
        chips = a1_chips(["0.1", "0.9", "0.1"], hi=None)
        self.play(FadeIn(chips[0]), run_time=0.3)
        self.play(FadeIn(chips[1]), run_time=0.3)
        self.play(FadeIn(chips[2]), run_time=0.3)
        until(self, "point one, point nine, point one", lead=0.1)
        lg = a1_logline("mesh AABB size (2.0, 2.0, 2.0)", y=-0.75)
        lg2 = a1_logline("node scale (0.1, 0.9, 0.1)", y=-1.5)
        self.play(FadeIn(lg), FadeIn(lg2), run_time=0.4)
        done(self)


# ── B06 · inherited scale, and the fourth failure: a collider that is only a box ───────────────────────────────────
class B06_Inherited(Scene):
    def construct(self):
        y_ax, z_ax, ly, lz = a1_ground()
        col = a1_rect(A1_W, A1_H)
        cube = Rectangle(width=2.0 * A1_U, height=2.0 * A1_U, fill_opacity=0, stroke_color=DIM, stroke_width=6)
        cube.move_to(A1_O + np.array([-0.1 * A1_U, 0.9 * A1_U, 0]))
        self.add(y_ax, z_ax, ly, lz, col, cube)
        until(self, "generated from that mesh", lead=0.3)
        shape = cube.copy().set_stroke(INK, 8)
        sl = T("a collider built from it", 34).move_to([-3.4, 1.7, 0])
        self.play(Create(shape), FadeIn(sl), run_time=0.7)
        until(self, "a fourth failure", lead=0.3)
        box = Square(side_length=2.6, fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([3.6, -0.55, 0])
        bl = T("a visible box", 34).move_to([3.6, 1.35, 0])
        self.play(FadeIn(box), FadeIn(bl), run_time=0.5)
        until(self, "no collision at all", lead=0.4)
        ring = Circle(radius=0.55, stroke_color=INK, stroke_width=8).move_to([3.6, -0.55, 0])
        bar = Line([3.21, -0.16, 0], [3.99, -0.94, 0], color=INK, stroke_width=8)
        nl = T("no collision", 34).move_to([3.6, -2.55, 0])
        self.play(Create(ring), Create(bar), FadeIn(nl), run_time=0.7)
        done(self)
