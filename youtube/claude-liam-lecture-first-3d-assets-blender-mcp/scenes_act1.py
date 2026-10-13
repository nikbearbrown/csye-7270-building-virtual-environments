"""ACT I · Three Simple Assets  (B01–B13 Manim; B14 is a Remotion BrowserCapture, see lanes/act1.json)

One cast for the act: the three REAL assets (crate, lantern, coin) as real Blender 5.1.2 renders (pantry/ev_*_34.png,
cropped to pantry/a1_crate|lantern|coin.png). Everything else that is a real thing is shown as itself: Blender by its real
icon and its real window (Blender's own screenshot), Godot by its real icon and the real Godot screenshot, Claude Code by
the library's Claude Code skin with nothing typed, the add-on by its README's own words.
Act I renders (evidence/act1/render_act1.py, crop_act1.py): the five default basic shapes, the lantern and the crate built
shape by shape (same camera as the real renders, so the pictures stack), and four example assets (platform, tree, rock, gem).
Numbers on screen are the real counts from evidence/primitives/tris.log and evidence/act1/render_act1.log.
Pacing: until() leads were set from faster-whisper word times (evidence/act1/word_times.json), not from the character share.
"""

A1P = "pantry/"


def a1_img(name, h=None, w=None, at=(0.0, 0.0)):
    im = ImageMobject(A1P + name)
    if h is not None:
        im.set_height(h)
    if w is not None:
        im.set_width(w)
    im.move_to(np.array([at[0], at[1], 0.0]))
    return im


def a1_lab(s, x, y, size=34, color=INK):
    return T(s, size, color).move_to([x, y, 0])


def a1_no(x, y, r=0.32, sw=7):
    """A prohibition mark (ink ring + bar), drawn BESIDE or over a picture, never over type."""
    ring = Circle(radius=r, stroke_color=INK, stroke_width=sw).move_to([x, y, 0])
    d = r * 0.7071
    bar = Line([x - d, y + d, 0], [x + d, y - d, 0], color=INK, stroke_width=sw)
    return VGroup(ring, bar)


def a1_toggle(x, y):
    """A generic OFF switch (outline pill, grey knob on the left)."""
    pill = RoundedRectangle(width=0.84, height=0.42, corner_radius=0.21, fill_opacity=0, stroke_color=INK,
                            stroke_width=4).move_to([x, y, 0])
    knob = Circle(radius=0.13, fill_color=DIM, fill_opacity=1, stroke_width=0).move_to([x - 0.2, y, 0])
    return VGroup(pill, knob)


def a1_cloud(x, y, s=1.0):
    parts = [Circle(radius=0.62 * s).move_to([x - 0.55 * s, y - 0.1 * s, 0]),
             Circle(radius=0.8 * s).move_to([x + 0.15 * s, y + 0.25 * s, 0]),
             Circle(radius=0.6 * s).move_to([x + 0.85 * s, y - 0.12 * s, 0]),
             RoundedRectangle(width=2.6 * s, height=0.75 * s, corner_radius=0.37 * s).move_to([x + 0.12 * s, y - 0.35 * s, 0])]
    for p in parts:
        p.set_fill(BAR2, 1).set_stroke(width=0)
    rim = VGroup(*[p.copy().set_fill(opacity=0).set_stroke(INK, 4) for p in parts[:3]])
    rim.set_z_index(0)
    fill = VGroup(*parts).set_z_index(1)
    return VGroup(rim, fill)


# ── B01 · the job: three simple assets, then into the game engine ────────────────────────────────────────────────
class B01_ThreeAssets(Scene):
    def construct(self):
        title = T("Three  Simple  Assets", 40).move_to([-3.75, 2.95, 0])
        self.add(title)
        xs = [-4.4, -1.4, 1.5]
        until(self, "three simple", lead=0.25)
        slots = VGroup(*[Ellipse(width=1.9, height=0.42, fill_color=GHOST, fill_opacity=1, stroke_width=0).move_to([x, -1.25, 0])
                         for x in xs])
        self.play(LaggedStart(*[GrowFromCenter(s) for s in slots], lag_ratio=0.25), run_time=0.7)
        crate = a1_img("a1_crate.png", h=2.35, at=(xs[0], -0.05))
        lantern = a1_img("a1_lantern.png", h=2.35, at=(xs[1], -0.05))
        coin = a1_img("a1_coin.png", w=2.3, at=(xs[2], -0.55))
        labs = [a1_lab("crate", xs[0], -1.95, 36), a1_lab("lantern", xs[1], -1.95, 36), a1_lab("coin", xs[2], -1.95, 36)]
        for img, lab, ph, ld in [(crate, labs[0], "a crate", 0.34), (lantern, labs[1], "a lantern", 0.32), (coin, labs[2], "a coin", 0.23)]:
            until(self, ph, lead=ld)
            self.play(FadeIn(img, shift=DOWN * 0.25), FadeIn(lab), run_time=0.4)
        until(self, "Then show", lead=0.07)
        arrow = Arrow([3.05, -0.05, 0], [3.95, -0.05, 0], buff=0, color=INK, stroke_width=6, tip_length=0.24)
        godot = a1_img("ev_icon_godot.png", h=2.0, at=(5.05, -0.05))
        g_l = a1_lab("Godot", 5.05, -1.95, 36)
        self.play(GrowArrow(arrow), FadeIn(godot), FadeIn(g_l), run_time=0.6)
        # small copies of the three assets ride the arrow into the engine
        trio = Group(a1_img("a1_crate.png", h=0.55, at=(2.35, 0.6)), a1_img("a1_lantern.png", h=0.55, at=(2.85, 0.6)),
                     a1_img("a1_coin.png", w=0.6, at=(3.4, 0.45)))
        self.play(FadeIn(trio), run_time=0.3)
        self.play(trio.animate.scale(0.5).move_to([5.05, -0.05, 0]), run_time=0.8)
        self.play(FadeOut(trio), run_time=0.2)
        until(self, "the way you meant", lead=0.62)
        ok = check(5.0, 1.55, s=0.28, color=INK, w=8)
        spark = Dot([5.65, 1.7, 0], radius=0.1, color=TERRA)
        self.play(Create(ok), FadeIn(spark), run_time=0.5)
        done(self)


# ── B02 · Claude drives Blender through MCP; you stay in the loop ────────────────────────────────────────────────
class B02_ClaudeDrives(Scene):
    def construct(self):
        cc = a1_img("a1_cc_shell.png", w=3.5, at=(-4.35, 1.05))
        cc_l = a1_lab("Claude Code", -4.35, -0.35, 36)
        bl = a1_img("ev_icon_blender.png", h=1.85, at=(4.35, 1.05))
        bl_l = a1_lab("Blender", 4.35, -0.35, 36)
        self.add(cc, cc_l, bl, bl_l)
        until(self, "Claude drives", lead=0.37)
        long = Arrow([-2.4, 1.05, 0], [3.2, 1.05, 0], buff=0, color=INK, stroke_width=6, tip_length=0.26)
        self.play(GrowArrow(long), run_time=0.7)
        until(self, "the free", lead=0.46)
        free = a1_lab("free", 4.35, -0.9, 32)
        self.play(FadeIn(free), run_time=0.35)
        until(self, "through a standard", lead=0.85)
        iso = Iso(-0.65, 0.42, 1.0)
        block = iso.mcp(0, 0, 0, w=1.3, d=1.3, h=0.7)
        m_l = a1_lab("MCP", 0.0, -0.35, 36)
        a1 = Arrow([-2.4, 1.05, 0], [-1.35, 1.05, 0], buff=0, color=INK, stroke_width=6, tip_length=0.24)
        a2 = Arrow([1.35, 1.05, 0], [3.2, 1.05, 0], buff=0, color=INK, stroke_width=6, tip_length=0.26)
        self.play(FadeOut(long), FadeIn(a1), FadeIn(a2), FadeIn(block, shift=DOWN * 0.3), FadeIn(m_l), run_time=0.6)
        until(self, "And you stay", lead=0.05)
        you = cursor(4.7, -1.75, s=0.6)
        you_l = a1_lab("you", 3.85, -2.05, 36)
        self.play(FadeIn(you, shift=UP * 0.2), FadeIn(you_l), run_time=0.45)
        until(self, "at least one edit", lead=0.75)
        loop = CurvedArrow([5.25, -2.0, 0], [5.55, 0.35, 0], angle=PI / 2.2, color=INK, stroke_width=6, tip_length=0.24)
        e_l = a1_lab("one edit by hand", 3.85, -2.8, 34)
        self.play(Create(loop), FadeIn(e_l), run_time=0.7)
        until(self, "made by hand", lead=1.07)
        spark = Dot([5.75, -0.1, 0], radius=0.11, color=TERRA)
        self.play(FadeIn(spark, scale=0.5), run_time=0.35)
        done(self)


# ── B03 · three kinds of asset, each named thing appears on its word ────────────────────────────────────────────
class B03_ThreeKinds(Scene):
    def construct(self):
        cols = [-4.3, 0.0, 4.3]
        divs = VGroup(*[Line([x, 2.35, 0], [x, -2.4, 0], color=GHOST, stroke_width=4) for x in (-2.15, 2.15)])
        self.play(Create(divs), run_time=0.4)
        heads = [a1_lab("prop", cols[0], 2.8, 38), a1_lab("environment", cols[1], 2.8, 38), a1_lab("collectible", cols[2], 2.8, 38)]
        pointer = Dot([cols[0] - 0.85, 2.8, 0], radius=0.1, color=TERRA)
        crate = a1_img("a1_crate.png", h=1.75, at=(cols[0], 1.0))
        lantern = a1_img("a1_lantern.png", h=1.75, at=(cols[0], -1.35))
        platform = a1_img("a1_ex_platform.png", w=2.7, at=(cols[1], 1.15))
        tree = a1_img("a1_ex_tree.png", h=1.8, at=(cols[1] - 0.85, -1.3))
        rock = a1_img("a1_ex_rock.png", w=1.45, at=(cols[1] + 0.9, -1.75))
        coin = a1_img("a1_coin.png", w=2.2, at=(cols[2], 0.95))
        gem = a1_img("a1_ex_gem.png", h=1.15, at=(cols[2], -1.45))
        until(self, "A prop", lead=0.68)
        self.play(FadeIn(heads[0]), FadeIn(pointer, scale=0.5), run_time=0.35)
        for img, ph, ld in [(crate, "a crate", 0.81), (lantern, "a lantern", 0.79)]:
            until(self, ph, lead=ld)
            self.play(FadeIn(img, shift=DOWN * 0.2), run_time=0.35)
        until(self, "A piece of the environment", lead=0.53)
        self.play(FadeIn(heads[1]), pointer.animate.move_to([cols[1] - 1.55, 2.8, 0]), run_time=0.45)
        for img, ph, ld in [(platform, "a platform", 0.77), (tree, "a tree", 0.76), (rock, "a rock", 0.65)]:
            until(self, ph, lead=ld)
            self.play(FadeIn(img, shift=DOWN * 0.2), run_time=0.35)
        until(self, "something the player collects", lead=0.55)
        self.play(FadeIn(heads[2]), pointer.animate.move_to([cols[2] - 1.4, 2.8, 0]), run_time=0.45)
        for img, ph, ld in [(coin, "a coin", 1.17), (gem, "a gem", 0.97)]:
            until(self, ph, lead=ld)
            self.play(FadeIn(img, shift=DOWN * 0.2), run_time=0.35)
        done(self)


# ── B04 · simple = Blender's basic shapes, moved, scaled, combined, one flat colour; four things ruled out ─────────────
A1_K = 1.85 / 1116.0                              # scene units per pixel: the five primitives share one camera, so sizes compare
A1_PRIMS = [("cube", 1109, 1116, -4.30), ("cylinder", 807, 999, -1.96), ("cone", 744, 903, 0.08),
            ("sphere", 774, 774, 2.08), ("plane", 1064, 426, 4.35)]


class B04_BasicShapes(Scene):
    def construct(self):
        icon = a1_img("ev_icon_blender.png", h=0.72, at=(-5.65, 2.8))
        head = a1_lab("basic shapes", -4.0, 2.8, 38)
        until(self, "basic shapes", lead=0.58)
        self.play(FadeIn(icon), FadeIn(head), run_time=0.4)
        prims, labs = [], []
        base = Line([-5.4, -0.32, 0], [5.4, -0.32, 0], color=GHOST, stroke_width=4)
        self.play(Create(base), run_time=0.3)
        for (name, pw, ph, x), ld in zip(A1_PRIMS, (0.46, 0.48, 0.59, 0.41, 0.57)):
            h = ph * A1_K
            im = a1_img(f"a1_clay_{name}.png", h=h, at=(x, -0.3 + h / 2))
            lb = a1_lab(name, x, -0.9, 34)
            prims.append(im); labs.append(lb)
            until(self, name, lead=ld)
            self.play(FadeIn(im, shift=DOWN * 0.2), FadeIn(lb), run_time=0.28)
        until(self, "Move them", lead=-0.4)                # just after the midpoint: the row of shapes is the still GATE T reads
        # the clay lantern's five parts arrive spread out and oversized: move, scale, combine
        LH, LX, LY = 4.3, -3.2, -0.25
        cum = [a1_img(f"a1_clay_lancum_{i}.png", h=LH, at=(LX, LY)) for i in range(1, 6)]
        parts = [a1_img(f"a1_clay_lanpart_{i}.png", h=LH, at=(LX, LY)) for i in range(1, 6)]
        offs = [(-0.9, -0.55), (0.0, -0.1), (0.9, 0.3), (-0.6, 0.7), (0.7, 1.0)]
        for p, (dx, dy) in zip(parts, offs):
            p.scale(1.25).shift(np.array([dx, dy, 0.0]))
        self.play(*[FadeOut(m) for m in prims + labs + [base, head, icon]], *[FadeIn(p) for p in parts], run_time=0.45)
        until(self, "combine them", lead=0.67)
        self.play(*[p.animate.shift(np.array([-dx, -dy, 0.0])).scale(1 / 1.25) for p, (dx, dy) in zip(parts, offs)],
                  run_time=0.7)
        self.add(cum[4]); self.remove(*parts)           # the running total, so the parts overlap exactly as Blender drew them
        until(self, "give them a flat colour", lead=0.85)
        colour = a1_img("a1_lantern_colour.png", h=LH, at=(LX, LY))
        l_l = a1_lab("5 shapes, flat colours", LX, 2.6, 34)
        self.play(FadeIn(colour), FadeIn(l_l), run_time=0.5)
        self.remove(cum[4])
        rows = [("sculpting", 1.45, "No sculpting", 0.91), ("painted textures", 0.45, "no painted textures", 0.87),
                ("rigging", -0.55, "no rigging", 0.83), ("animation", -1.55, "no animation", 0.91)]
        for word, y, ph, ld in rows:
            until(self, ph, lead=ld)
            mark = a1_no(0.95, y, r=0.3)
            lab = T(word, 36).move_to([1.6, y, 0], aligned_edge=LEFT)
            self.play(Create(mark), FadeIn(lab), run_time=0.35)
        done(self)


# ── B05 · the budget: six shapes, 500 triangles; what a triangle is ─────────────────────────────────────────────────
def a1_cube_pt(x, y, z):
    """An oblique (not isometric) view, so the hidden back corner does not land on a front corner."""
    return np.array([3.2 + 2.0 * x - 1.1 * y, -1.9 + 0.6 * x + 0.8 * y + 2.0 * z, 0.0])


class B05_Budget(Scene):
    def construct(self):
        until(self, "no more than six", lead=0.73)
        six = T("6", 120).move_to([-4.85, 1.35, 0])
        six_l = a1_lab("basic shapes", -4.85, 0.0, 34)
        self.play(FadeIn(six, shift=UP * 0.2), FadeIn(six_l), run_time=0.45)
        until(self, "five hundred triangles", lead=0.95)
        five = T("500", 120).move_to([-1.95, 1.35, 0])
        five_l = a1_lab("triangles", -1.95, 0.0, 34)
        self.play(FadeIn(five, shift=UP * 0.2), FadeIn(five_l), run_time=0.45)
        until(self, "A triangle is", lead=0.65)
        P = a1_cube_pt
        vis = [((0, 0, 0), (1, 0, 0)), ((1, 0, 0), (1, 0, 1)), ((1, 0, 1), (0, 0, 1)), ((0, 0, 1), (0, 0, 0)),
               ((0, 0, 0), (0, 1, 0)), ((0, 1, 0), (0, 1, 1)), ((0, 1, 1), (0, 0, 1)), ((0, 1, 1), (1, 1, 1)), ((1, 1, 1), (1, 0, 1))]
        hid = [((1, 1, 0), (1, 0, 0)), ((1, 1, 0), (0, 1, 0)), ((1, 1, 0), (1, 1, 1))]
        edges = VGroup(*[Line(P(*a), P(*b), color=INK, stroke_width=6) for a, b in vis])
        back = VGroup(*[DashedLine(P(*a), P(*b), color=DIM, stroke_width=4, dash_length=0.14) for a, b in hid])
        tri = Polygon(P(0, 0, 1), P(1, 0, 1), P(1, 1, 1), fill_color=TERRA, fill_opacity=1, stroke_width=0)
        tri.set_z_index(-1)
        t_l = a1_lab("a triangle", 4.35, 2.2, 34)
        self.play(Create(edges), Create(back), run_time=0.6)
        self.play(FadeIn(tri), FadeIn(t_l), run_time=0.4)
        until(self, "every surface is cut into", lead=0.64)
        diag_v = VGroup(Line(P(0, 0, 0), P(1, 0, 1), color=INK, stroke_width=5), Line(P(0, 0, 0), P(0, 1, 1), color=INK, stroke_width=5),
                        Line(P(0, 0, 1), P(1, 1, 1), color=INK, stroke_width=5))
        diag_h = VGroup(DashedLine(P(1, 0, 0), P(1, 1, 1), color=DIM, stroke_width=4, dash_length=0.14),
                        DashedLine(P(0, 1, 0), P(1, 1, 1), color=DIM, stroke_width=4, dash_length=0.14),
                        DashedLine(P(0, 0, 0), P(1, 1, 0), color=DIM, stroke_width=4, dash_length=0.14))
        self.play(Create(diag_v), Create(diag_h), run_time=0.8)
        c_l = a1_lab("cube: 12 triangles", 3.35, -2.6, 34)
        self.play(FadeIn(c_l), run_time=0.35)
        until(self, "Those limits", lead=0.10)
        brace = BraceBetweenPoints([-6.0, -0.55, 0], [-0.8, -0.55, 0], direction=DOWN, color=INK)
        k_l = a1_lab("course limits", -3.4, -1.45, 36)
        self.play(GrowFromCenter(brace), FadeIn(k_l), run_time=0.5)
        until(self, "They aren't", lead=0.29)
        n_l = a1_lab("not engine limits", -3.4, -2.1, 34)
        self.play(FadeIn(n_l), run_time=0.35)
        done(self)


# ── B06 · the trap: real triangle counts against the 500 budget ─────────────────────────────────────────────────────
A1_BASE = -2.25
A1_KT = 4.55 / 960.0
A1_BARS = [("cube", 12, -3.35), ("cylinder", 124, -1.45), ("cone", 62, 0.45), ("sphere", 960, 2.35)]


def a1_bar(n, x, fill):
    h = max(0.04, n * A1_KT)
    return Rectangle(width=1.2, height=h, fill_color=fill, fill_opacity=1, stroke_width=0).move_to([x, A1_BASE + h / 2, 0])


class B06_Trap(Scene):
    def construct(self):
        cap = a1_lab("triangles, at Blender 5.1.2's defaults", -2.35, 2.95, 34)
        yb = A1_BASE + 500 * A1_KT
        budget = DashedLine([-5.6, yb, 0], [3.25, yb, 0], color=INK, stroke_width=5, dash_length=0.2)
        b_l = a1_lab("budget 500", -4.75, yb + 0.5, 34)
        self.add(cap, budget, b_l)
        base = Line([-4.15, A1_BASE, 0], [3.25, A1_BASE, 0], color=DIM, stroke_width=4)
        self.play(Create(base), run_time=0.4)
        bars, nums, names = {}, {}, {}
        for name, n, x in A1_BARS:
            bars[name] = a1_bar(n, x, BAR1 if name == "sphere" else BAR2)
            nums[name] = T(str(n), 40).move_to([x, A1_BASE + n * A1_KT + 0.38, 0])
            names[name] = a1_lab(name, x, A1_BASE - 0.5, 34)
        for name, ph, ld in [("cube", "A cube is", 0.31), ("cylinder", "A default cylinder", 0.25)]:
            until(self, ph, lead=ld)
            self.play(GrowFromEdge(bars[name], DOWN), FadeIn(names[name]), run_time=0.5)
            self.play(FadeIn(nums[name]), run_time=0.25)
        self.play(GrowFromEdge(bars["cone"], DOWN), FadeIn(names["cone"]), FadeIn(nums["cone"]), run_time=0.45)
        until(self, "A default sphere", lead=0.47)
        self.play(GrowFromEdge(bars["sphere"], DOWN), FadeIn(names["sphere"]), run_time=1.0)
        self.play(FadeIn(nums["sphere"]), run_time=0.3)
        until(self, "nearly twice", lead=0.80)
        over = dim_arrow([3.3, yb, 0], [3.3, A1_BASE + 960 * A1_KT, 0])
        o_l = a1_lab("1.92 × budget", 4.75, (yb + A1_BASE + 960 * A1_KT) / 2, 34)
        spark = Dot([2.35, A1_BASE + 960 * A1_KT - 0.25, 0], radius=0.11, color=TERRA)
        self.play(GrowFromCenter(over), FadeIn(o_l), FadeIn(spark), run_time=0.6)
        done(self)


# ── B07 · the same sphere, 12 segments × 6 rings: 960 → 120 ─────────────────────────────────────────────────────────
class B07_LowerSegments(Scene):
    def construct(self):
        big = a1_img("a1_sphere_960.png", h=3.3, at=(-3.4, 0.55))
        b1 = a1_lab("32 segments × 16 rings", -3.4, -1.55, 34)
        b2 = a1_lab("960 triangles", -3.4, -2.2, 36)
        self.add(big, b1, b2)
        until(self, "lower the segment", lead=0.31)
        arrow = Arrow([-1.25, 0.55, 0], [1.25, 0.55, 0], buff=0, color=INK, stroke_width=6, tip_length=0.26)
        self.play(GrowArrow(arrow), run_time=0.6)
        until(self, "The same sphere", lead=0.16)
        small = a1_img("a1_sphere_120.png", h=3.3, at=(3.4, 0.55))
        self.play(FadeIn(small, shift=LEFT * 0.3), run_time=0.5)
        until(self, "twelve segments", lead=0.42)
        s1 = a1_lab("12 segments × 6 rings", 3.4, -1.55, 34)
        self.play(FadeIn(s1), run_time=0.35)
        until(self, "a hundred and twenty", lead=0.51)
        s2 = a1_lab("120 triangles", 3.4, -2.2, 36)
        spark = Dot([4.75, -2.2, 0], radius=0.1, color=TERRA)
        self.play(FadeIn(s2), FadeIn(spark, scale=0.5), run_time=0.4)
        done(self)


# ── B08 · one game, one repository; each assignment a layer; this one is tagged a3 ──────────────────────────────────
A1_SLAB = 0.34


def a1_slab(i, ghost=False):
    iso = Iso(-0.55, -2.55, 1.0)
    z = i * A1_SLAB
    if ghost:
        return iso.box(0, 0, z, 2.4, 2.4, 0.27, top=CARD, left=BAR2, right=BAR1, sw=3)
    return iso.box(0, 0, z, 2.4, 2.4, 0.27)


def a1_slab_y(i):
    """Screen y of the middle of layer i's left face (Iso(-0.55,-2.55)): y0 + (x+y)/2 + z with x=0, y=1.2."""
    return -2.55 + 0.6 + i * A1_SLAB + 0.135


class B08_OneGame(Scene):
    def construct(self):
        floor = Iso(-0.55, -2.55, 1.0).quad([(-0.2, -0.2, 0), (2.6, -0.2, 0), (2.6, 2.6, 0), (-0.2, 2.6, 0)], GHOST, stroke=GHOST, sw=0)
        self.add(floor)
        until(self, "From the second", lead=0.13)
        s2 = a1_slab(0)
        l2 = M("a2", 34).move_to([-3.25, a1_slab_y(0), 0])
        self.play(FadeIn(s2, shift=DOWN * 0.4), FadeIn(l2), run_time=0.45)
        until(self, "one game in one repository", lead=0.96)
        g_l = a1_lab("one game,", -4.6, 1.75, 36)
        r_l = a1_lab("one repository", -4.6, 1.15, 36)
        self.play(FadeIn(g_l), FadeIn(r_l), run_time=0.45)
        until(self, "Each assignment adds", lead=0.45)
        s3 = a1_slab(1)
        self.play(FadeIn(s3, shift=DOWN * 0.4), run_time=0.4)
        ghosts = [a1_slab(i, ghost=True) for i in range(2, 9)]
        self.play(LaggedStart(*[FadeIn(g, shift=DOWN * 0.3) for g in ghosts], lag_ratio=0.35), run_time=1.0)
        lg = M("a4 … a10", 32).move_to([-4.15, a1_slab_y(5), 0])
        self.play(FadeIn(lg), run_time=0.3)
        until(self, "git tag", lead=1.08)
        # the tag hangs from the a3 layer's right face (Iso(-0.55,-2.55): p(2.3, 0, 0.475) = (1.44, -0.925))
        tag = Polygon([2.75, -0.75, 0], [3.15, -0.4, 0], [4.55, -0.4, 0], [4.55, -1.1, 0], [3.15, -1.1, 0],
                      fill_color=BOX_TOP, fill_opacity=1, stroke_color=INK, stroke_width=5)
        hole = Circle(radius=0.09, stroke_color=INK, stroke_width=4).move_to([3.18, -0.75, 0])
        string = Line([1.44, -0.925, 0], [2.75, -0.75, 0], color=INK, stroke_width=4)
        t_l = M("git tag a3", 32).move_to([3.65, -1.7, 0])
        self.play(Create(string), FadeIn(tag), FadeIn(hole), run_time=0.5)
        self.play(FadeIn(t_l), run_time=0.3)
        until(self, "a three", lead=0.81)
        spark = Dot([3.18, -0.75, 0], radius=0.09, color=TERRA)
        self.play(FadeIn(spark, scale=0.4), run_time=0.4)
        done(self)


# ── B09A / B09B / B10 · a 2-D game still gets three assets and a small 3-D scene; then the real scene ───────────────────
def a1_twod():
    frame = RoundedRectangle(width=4.3, height=2.7, corner_radius=0.12, fill_color=CARD, fill_opacity=1, stroke_color=INK,
                             stroke_width=5).move_to([-3.85, 0.55, 0])
    ground = Rectangle(width=4.0, height=0.36, fill_color=BAR2, fill_opacity=1, stroke_width=0).move_to([-3.85, -0.55, 0])
    plat1 = Rectangle(width=1.1, height=0.22, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([-4.85, 0.35, 0])
    plat2 = Rectangle(width=1.2, height=0.22, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([-2.85, 0.95, 0])
    hero = Square(side_length=0.42, fill_color=BOX_R, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([-4.85, 0.67, 0])
    pick = Circle(radius=0.14, fill_color=BOX_TOP, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([-2.85, 1.3, 0])
    lab = a1_lab("2-D game", -3.85, -1.2, 36)
    return VGroup(frame, ground, plat1, plat2, hero, pick), lab


A1_FLOOR = Iso(2.75, -2.15, 1.12)


def a1_floor():
    return A1_FLOOR.quad([(0, 0, 0), (2.5, 0, 0), (2.5, 2.5, 0), (0, 2.5, 0)], BOX_TOP, stroke="#9C8462", sw=4)


def a1_stage_assets(h=1.25):
    """The three real renders standing on the stage (equal heights: before 'game scale')."""
    c = a1_img("a1_crate.png", h=h, at=(1.75, -0.25))
    l = a1_img("a1_lantern.png", h=h, at=(2.85, 0.05))
    k = a1_img("a1_coin.png", w=h * 1.0, at=(3.95, -0.45))
    return c, l, k


class B09A_TwoD(Scene):
    def construct(self):
        until(self, "If it's two-D", lead=0.32)
        game, g_l = a1_twod()
        self.play(FadeIn(game), FadeIn(g_l), run_time=0.5)
        until(self, "three assets", lead=0.71)
        c, l, k = a1_stage_assets()
        for im in (c, l, k):
            self.play(FadeIn(im, shift=DOWN * 0.2), run_time=0.25)
        until(self, "a small three-D scene", lead=0.86)
        floor = a1_floor()
        floor.set_z_index(-1)
        s_l = a1_lab("small 3-D scene", 2.75, -2.75, 36)
        self.play(GrowFromCenter(floor), FadeIn(s_l), run_time=0.6)
        done(self)


def a1_light():
    halo = Circle(radius=0.42, fill_color=GHOST, fill_opacity=1, stroke_width=0).move_to([1.15, 2.3, 0])
    lamp = Dot([1.15, 2.3, 0], radius=0.2, color=TERRA)
    return halo, lamp


def a1_camera():
    body = RoundedRectangle(width=0.95, height=0.62, corner_radius=0.08, fill_color=BAR1, fill_opacity=1, stroke_color=INK,
                            stroke_width=4).move_to([5.3, 1.75, 0])
    lens = Circle(radius=0.2, fill_color=CARD, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([4.75, 1.62, 0])
    view = Polygon([4.55, 1.55, 0], [3.2, 0.9, 0], [4.1, 0.25, 0], fill_color=GHOST, fill_opacity=0.9, stroke_width=0)
    view.set_z_index(-2)
    return view, body, lens


# "Game scale": the three renders shown in their TRUE relative sizes. All three were rendered with the same 50 mm lens, from
# camera distances 3.6 m (crate), 2.3 m (lantern), 1.0 m (coin) (evidence/renders/render_assets.py), so a picture's real size is
# proportional to its pixel size x its camera distance: crate 1116 px x 3.6, lantern 815 px x 2.3, coin 1046 px wide x 1.0.
A1_GS = 1.76 / (1116 * 3.6)
A1_GS_CRATE_H, A1_GS_LANTERN_H, A1_GS_COIN_W = 1116 * 3.6 * A1_GS, 815 * 2.3 * A1_GS, 1046 * 1.0 * A1_GS   # 1.76, 0.82, 0.46


def a1_game_scale(c, l, k):
    c.set_height(A1_GS_CRATE_H).move_to([1.65, -0.1, 0])
    l.set_height(A1_GS_LANTERN_H).move_to([2.95, -0.55, 0])
    k.set_width(A1_GS_COIN_W).move_to([3.7, -0.8, 0])


class B09B_SceneParts(Scene):
    def construct(self):
        game, g_l = a1_twod()
        floor = a1_floor(); floor.set_z_index(-1)
        c, l, k = a1_stage_assets()
        s_l = a1_lab("small 3-D scene", 2.75, -2.75, 36)
        self.add(game, g_l, floor, c, l, k, s_l)
        f_l = a1_lab("floor", 5.55, -1.45, 34)
        self.play(FadeIn(f_l), run_time=0.3)
        until(self, "one light", lead=0.16)
        halo, lamp = a1_light()
        lamp_l = a1_lab("light", 0.0, 2.3, 34)
        self.play(GrowFromCenter(halo), FadeIn(lamp), FadeIn(lamp_l), run_time=0.35)
        until(self, "a camera", lead=0.38)
        view, body, lens = a1_camera()
        cam_l = a1_lab("camera", 5.3, 2.5, 34)
        self.play(FadeIn(view), FadeIn(body), FadeIn(lens), FadeIn(cam_l), run_time=0.35)
        until(self, "game scale", lead=0.77)
        self.play(c.animate.set_height(A1_GS_CRATE_H).move_to([1.65, -0.1, 0]),
                  l.animate.set_height(A1_GS_LANTERN_H).move_to([2.95, -0.55, 0]),
                  k.animate.set_width(A1_GS_COIN_W).move_to([3.7, -0.8, 0]), run_time=0.6)
        sc_l = a1_lab("game scale", 4.55, -2.75, 34)
        self.play(s_l.animate.move_to([1.6, -2.75, 0]), run_time=0.25)
        self.play(FadeIn(sc_l), run_time=0.25)
        done(self)


class B10_ReuseScene(Scene):
    def construct(self):
        game, g_l = a1_twod()
        floor = a1_floor(); floor.set_z_index(-1)
        c, l, k = a1_stage_assets()
        a1_game_scale(c, l, k)
        halo, lamp = a1_light()
        view, body, lens = a1_camera()
        labs = [a1_lab("floor", 5.55, -1.45, 34), a1_lab("light", 0.0, 2.3, 34), a1_lab("camera", 5.3, 2.5, 34),
                a1_lab("game scale", 4.55, -2.75, 34)]
        s_l = a1_lab("small 3-D scene", 1.6, -2.75, 36)
        self.add(game, g_l, floor, c, l, k, halo, lamp, view, body, lens, s_l, *labs)
        self.play(*[FadeOut(m) for m in labs], run_time=0.35)
        until(self, "reuse that scene", lead=0.36)
        a4 = Arrow([4.1, -1.05, 0], [4.55, -2.2, 0], buff=0, color=INK, stroke_width=6, tip_length=0.2)
        a5 = Arrow([4.75, -0.8, 0], [5.6, -2.2, 0], buff=0, color=INK, stroke_width=6, tip_length=0.2)
        l4 = M("a4", 36).move_to([4.55, -2.65, 0])
        l5 = M("a5", 36).move_to([5.65, -2.65, 0])
        self.play(GrowArrow(a4), GrowArrow(a5), FadeIn(l4), FadeIn(l5), run_time=0.5)
        until(self, "connect it", lead=0.54)
        link = DashedLine([-1.55, -0.2, 0], [0.1, -0.7, 0], color=DIM, stroke_width=5, dash_length=0.16)
        n_l = a1_lab("not yet", -0.65, 0.35, 34)
        self.play(Create(link), FadeIn(n_l), run_time=0.5)
        done(self)


# ── B11 · the tools, each shown as itself; all free ─────────────────────────────────────────────────────────────────
class B11_Tools(Scene):
    def construct(self):
        until(self, "Claude Code", lead=0.38)
        cc = a1_img("a1_cc_shell.png", w=3.3, at=(-4.5, 1.25))
        cc_l = a1_lab("Claude Code", -4.5, -0.45, 36)
        self.play(FadeIn(cc, shift=UP * 0.2), FadeIn(cc_l), run_time=0.4)
        until(self, "university access", lead=0.70)
        cc_s = a1_lab("university access", -4.5, -1.0, 32)
        self.play(FadeIn(cc_s), run_time=0.3)
        until(self, "Blender, which", lead=0.34)
        bw = a1_img("a1_blender_view.png", h=2.6, at=(-0.6, 1.25))
        bw_l = a1_lab("Blender", -0.6, -0.45, 36)
        bw_s = a1_lab("free", -0.6, -1.0, 32)
        self.play(FadeIn(bw, shift=UP * 0.2), FadeIn(bw_l), run_time=0.4)
        self.play(FadeIn(bw_s), run_time=0.25)
        until(self, "the Blender M C P add-on", lead=0.56)
        card = RoundedRectangle(width=3.9, height=2.5, corner_radius=0.14, fill_opacity=0, stroke_color=INK,
                                stroke_width=4).move_to([3.85, 1.25, 0])
        r1 = T("MCP for Blender", 36).move_to([3.85, 2.0, 0])
        r2 = T("Connect Blender", 32).move_to([3.85, 1.4, 0])
        r3 = T("to any LLM", 32).move_to([3.85, 0.95, 0])
        r4 = M("License: MIT", 32).move_to([3.85, 0.45, 0])
        ad_l = a1_lab("MCP add-on", 3.85, -0.45, 36)
        self.play(Create(card), FadeIn(r1), FadeIn(r2), FadeIn(r3), FadeIn(r4), FadeIn(ad_l), run_time=0.45)
        src = a1_lab("README 2.1.9, 6 Oct 2026", 3.85, -1.55, 32)
        self.play(FadeIn(src), run_time=0.25)
        until(self, "also free", lead=0.58)
        ad_s = a1_lab("free", 3.85, -1.0, 32)
        self.play(FadeIn(ad_s), run_time=0.3)
        until(self, "Nothing paid is needed", lead=0.13)
        mark = a1_no(-2.3, -2.35, r=0.34)
        n_l = a1_lab("nothing paid", -0.2, -2.35, 38)
        self.play(Create(mark), FadeIn(n_l), run_time=0.45)
        until(self, "earns credit", lead=0.73)
        n2 = a1_lab("no credit for paid tools", -0.2, -2.9, 32)
        self.play(FadeIn(n2), run_time=0.3)
        done(self)


# ── B12 · provenance: you build the geometry; downloaded or AI-generated meshes do not count ───────────────────────────
class B12_Provenance(Scene):
    def construct(self):
        # crate at the same size as B01 (2.35): at 3.3 its top band read as a low-contrast "text" blob under the real 4K GATE T
        CH, CX, CY = 2.35, -3.6, 0.6
        cum = [a1_img(f"a1_ccum_{i}.png", h=CH, at=(CX, CY)) for i in range(1, 6)]
        self.add(cum[0])
        offs = [None, (0.0, -0.8), (0.0, 0.7), (-1.0, 0.0), (1.0, 0.15)]
        until(self, "You build", lead=0.19)
        shown = cum[0]
        for i in range(1, 5):
            part = a1_img(f"a1_cpart_{i + 1}.png", h=CH, at=(CX, CY)).shift(np.array([offs[i][0], offs[i][1], 0.0]))
            self.play(FadeIn(part), run_time=0.15)
            self.play(part.animate.shift(np.array([-offs[i][0], -offs[i][1], 0.0])), run_time=0.4)
            self.add(cum[i]); self.remove(part, shown)
            shown = cum[i]
        joined = a1_img("a1_crate_colour.png", h=CH, at=(CX, CY))    # the finished asset: five shapes joined into one object
        self.add(joined); self.remove(shown)                           # same picture, one outline: an invisible swap
        until(self, "with Claude", lead=0.86)
        y_l = a1_lab("you build it", CX, -1.3, 36)
        y_s = a1_lab("from basic shapes", CX, -1.9, 32)      # true of THIS crate (script route); the rule itself is spoken
        ok = check(-1.95, 1.55, s=0.3, color=INK, w=8)
        self.play(FadeIn(y_l), FadeIn(y_s), Create(ok), run_time=0.45)
        until(self, "A downloaded", lead=0.59)
        tray = VGroup(Line([0.85, 0.8, 0], [0.85, 0.45, 0], color=INK, stroke_width=7),
                      Line([0.85, 0.45, 0], [1.95, 0.45, 0], color=INK, stroke_width=7),
                      Line([1.95, 0.45, 0], [1.95, 0.8, 0], color=INK, stroke_width=7))
        down = Arrow([1.4, 1.9, 0], [1.4, 0.65, 0], buff=0, color=INK, stroke_width=8, tip_length=0.3)
        d_l = VGroup(a1_lab("downloaded", 4.0, 1.45, 36), a1_lab("3D model", 4.0, 0.9, 36))
        self.play(Create(tray), GrowArrow(down), FadeIn(d_l), run_time=0.45)
        until(self, "generated mesh", lead=0.74)
        star = Star(n=4, outer_radius=0.5, inner_radius=0.17, fill_color=BOX_TOP, fill_opacity=1, stroke_color=INK,
                    stroke_width=5).move_to([1.3, -1.1, 0])
        star2 = Star(n=4, outer_radius=0.24, inner_radius=0.09, fill_color=BOX_TOP, fill_opacity=1, stroke_color=INK,
                     stroke_width=4).move_to([1.85, -0.55, 0])
        a_l = a1_lab("AI-generated mesh", 4.3, -1.0, 36)
        self.play(GrowFromCenter(star), GrowFromCenter(star2), FadeIn(a_l), run_time=0.45)
        until(self, "doesn't count", lead=0.66)
        n1 = a1_no(1.4, 1.2, r=0.8, sw=9)
        n2 = a1_no(1.45, -0.95, r=0.8, sw=9)
        self.play(Create(n1), Create(n2), run_time=0.5)
        done(self)


# ── B13 · the add-on's model fetchers and generators: leave every one off ─────────────────────────────────────────────
A1_SERV = [("Poly Haven", 1.75), ("Sketchfab", 1.15), ("Poly Pizza", 0.55), ("Hyper3D Rodin", -1.1), ("Hunyuan3D", -1.7), ("Tripo", -2.3)]


class B13_ServicesOff(Scene):
    def construct(self):
        until(self, "fetch three-D models", lead=0.42)
        h1 = T("fetch 3D models", 36).move_to([-5.6, 2.6, 0], aligned_edge=LEFT)
        rows, toggles = [], []
        for name, y in A1_SERV:
            rows.append(T(name, 34).move_to([-5.6, y, 0], aligned_edge=LEFT))
            toggles.append(a1_toggle(-0.65, y))
        self.play(FadeIn(h1), *[FadeIn(r) for r in rows[:3]], *[FadeIn(t) for t in toggles[:3]], run_time=0.5)
        until(self, "ask A. I. services", lead=1.03)
        h2 = T("generate 3D models", 36).move_to([-5.6, -0.35, 0], aligned_edge=LEFT)
        self.play(FadeIn(h2), *[FadeIn(r) for r in rows[3:]], *[FadeIn(t) for t in toggles[3:]], run_time=0.5)
        until(self, "Leave every one", lead=0.22)
        ring = RoundedRectangle(width=1.35, height=4.85, corner_radius=0.25, fill_opacity=0, stroke_color=INK,
                                stroke_width=5).move_to([-0.65, -0.27, 0])
        off_l = a1_lab("all off", -0.65, 2.6, 36)
        self.play(Create(ring), FadeIn(off_l), run_time=0.45)
        until(self, "They call remote", lead=0.51)
        cloud = a1_cloud(3.6, 0.55, 1.15)
        c_l = a1_lab("remote services", 3.75, -1.15, 36)
        links = VGroup(*[DashedLine([0.05, y, 0], [2.05, 0.35, 0], color=DIM, stroke_width=4, dash_length=0.14) for _, y in A1_SERV])
        self.play(FadeIn(cloud), Create(links), FadeIn(c_l), run_time=0.6)
        until(self, "cost money", lead=0.94)
        m_l = a1_lab("some may cost money", 3.75, -1.85, 34)
        spark = Dot([1.6, -1.85, 0], radius=0.1, color=TERRA)
        self.play(FadeIn(m_l), FadeIn(spark, scale=0.5), run_time=0.4)
        done(self)
