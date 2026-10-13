"""ACT III · Write the Brief Before You Build  (B21–B28, all Manim)

One cast for the act: THE CRATE (the real crate, 0.8 x 0.8 x 0.8 m, built by evidence/assets/build_crate.py) and its ORIGIN as a
terracotta dot. Where the crate is the real thing it is the real render (pantry/a3_crate_34.png, a crop of ev_crate_34.png) or the real
Blender window (pantry/a3_bl_crate_origin.png); where the beat is about an IDEA (where the origin sits, what the floor does with it) it
is a side-view drawing of the same crate: a 0.8 m square with its bottom and top bands and its centre strap, like the render.
Every number on screen is from a real run: build_crate.log / build_lantern.log (Blender 5.1.2), evidence/godot/*.log (Godot 4.7.2).
Illustrative values (the example player, the example brief entries) say "example" on screen.
"""

A3_FRAME_W = 14.222                              # Manim frame width (units) at 16:9
A3_WOOD, A3_BAND = "#B5804D", "#7E5530"          # the crate's two materials: wood browns toward the real render (CrateWood/CrateBand);
                                                 # the pale kraft tones failed Gate V contrast (B25A 0.29 < 0.30, 4K review cut 2026-10-06)
A3_S = 3.0                                       # side views of the origin story: scene units per metre
A3_F = -0.2                                      # ... and the floor's y
A3_XL, A3_XR = -3.4, 3.0                         # ... and the two crates' centres

# real crate render crop (pantry/a3_crate_34.png = ev_crate_34.png cropped at 600,150 -> 1180 x 1160 px); corners projected from
# the render camera (evidence/act3/make_crops.log): x- y- z0, x+ y- z0 (nearest), x+ y+ z0, x+ y+ z0.8, x+ y- z0.8
A3_CRATE_PX = (1180, 1160)
A3_C_LB, A3_C_FB, A3_C_RB = (92.5, 896.4), (701.3, 1122.5), (1083.5, 814.9)
A3_C_RT, A3_C_FT = (1124.4, 141.3), (711.6, 340.7)

# the crate render's silhouette ON its edge (alpha > 10, not dilated; evidence/act3/make_crops.py). B22 draws it in ink over the render's own
# dark Workbench outline: GATE T read those edge pixels (they fall inside its MUTE tolerance after encoding) as text-like blobs (4K cut, 2026-10-06)
A3_CRATE_OUTLINE = [[702.0, 1122.5], [90.5, 895.0], [85.5, 814.0], [110.5, 800.0], [109.5, 772.0], [80.5, 298.0], [51.5, 287.0], [45.5, 205.0],
                    [48.0, 190.5], [514.0, 36.5], [1124.5, 140.0], [1119.5, 232.0], [1095.0, 244.5], [1092.5, 254.0], [1065.5, 722.0],
                    [1066.0, 728.5], [1088.5, 736.0], [1084.5, 815.0]]

# real lantern render crop (pantry/a3_lantern_34.png = ev_lantern_34.png cropped at 970,295 -> 461 x 825 px) and its silhouette
# (alpha > 10, dilated 14 px, simplified; evidence/act3/make_crops.py)
A3_LANTERN_PX = (461, 825)
A3_LANTERN_OUTLINE = [[236.0, 819.5], [191.0, 819.5], [91.0, 801.5], [20.5, 759.0], [6.5, 707.0], [5.5, 630.0], [48.0, 584.5],
                      [73.5, 575.0], [69.5, 334.0], [99.0, 306.5], [131.5, 297.0], [87.0, 287.5], [24.0, 260.5], [9.5, 225.0],
                      [9.5, 194.0], [184.0, 77.5], [184.5, 16.0], [208.0, 5.5], [273.0, 12.5], [274.5, 77.0], [427.0, 171.5],
                      [451.5, 206.0], [451.5, 236.0], [419.0, 270.5], [327.5, 296.0], [372.0, 314.5], [389.5, 342.0], [386.5, 577.0],
                      [429.0, 597.5], [454.5, 645.0], [453.5, 726.0], [416.0, 777.5], [337.0, 810.5]]


def a3_px(cx, cy, k, size, px, py):
    """Scene point of pixel (px, py) of an image of `size` (w, h) px shown at scale k units/px, centred on (cx, cy)."""
    return np.array([cx + (px - size[0] / 2) * k, cy - (py - size[1] / 2) * k, 0.0])


def a3_crate_side(cx, base_y, s=A3_S):
    """The crate in side view: a 0.8 m square, bottom and top bands 0.1 m, a 0.1 m centre strap (the real crate's pattern)."""
    w = 0.8 * s
    body = Rectangle(width=w, height=w, fill_color=A3_WOOD, fill_opacity=1, stroke_width=0).move_to([cx, base_y + w / 2, 0])
    bot = Rectangle(width=w, height=0.1 * s, fill_color=A3_BAND, fill_opacity=1, stroke_width=0).move_to([cx, base_y + 0.05 * s, 0])
    top = Rectangle(width=w, height=0.1 * s, fill_color=A3_BAND, fill_opacity=1, stroke_width=0).move_to([cx, base_y + 0.75 * s, 0])
    strap = Rectangle(width=0.1 * s, height=w, fill_color=A3_BAND, fill_opacity=1, stroke_width=0).move_to([cx, base_y + w / 2, 0])
    edge = Rectangle(width=w, height=w, fill_opacity=0, stroke_color=INK, stroke_width=5).move_to([cx, base_y + w / 2, 0])
    return VGroup(body, bot, top, strap, edge)


def a3_dot(x, y, r=0.13):
    return Dot([x, y, 0], radius=r, color=TERRA).set_z_index(6)


def a3_floor(x0=-6.1, x1=6.1, y=A3_F):
    return Line([x0, y, 0], [x1, y, 0], color=DIM, stroke_width=8).set_z_index(4)


def a3_page(x, y, w=1.6, h=1.9, fill=CARD, stroke=INK):
    """A document: a sheet with a folded top-right corner (no lines on it)."""
    f = 0.42
    sheet = Polygon([x - w / 2, y - h / 2, 0], [x + w / 2, y - h / 2, 0], [x + w / 2, y + h / 2 - f, 0], [x + w / 2 - f, y + h / 2, 0],
                    [x - w / 2, y + h / 2, 0], fill_color=fill, fill_opacity=1, stroke_color=stroke, stroke_width=4)
    fold = Polygon([x + w / 2 - f, y + h / 2, 0], [x + w / 2 - f, y + h / 2 - f, 0], [x + w / 2, y + h / 2 - f, 0],
                   fill_color=GHOST, fill_opacity=1, stroke_color=stroke, stroke_width=3)
    return VGroup(sheet, fold)


def a3_no(x, y, r=0.42):
    """A 'not this' mark: an ink ring with a bar."""
    ring = Circle(radius=r, stroke_color=INK, stroke_width=8).move_to([x, y, 0])
    d = r * 0.7071
    bar = Line([x - d, y + d, 0], [x + d, y - d, 0], color=INK, stroke_width=8)
    return VGroup(ring, bar)


def a3_left(mob, x, y):
    """Place a text so its LEFT edge sits at x (explicit numbers: Gate A's stub cannot measure text)."""
    return mob.move_to([x + mob.width / 2, y, 0])


# ── B21 · the brief, committed before anything is built; revisions added, the original kept ─────────────────────────────
class B21_BriefFirst(Scene):
    def construct(self):
        title = T("Write the Brief Before You Build", 40).move_to([-2.6, 3.0, 0])
        line = Line([-5.7, -1.45, 0], [5.7, -1.45, 0], color=DIM, stroke_width=6)
        self.add(title, line)
        until(self, "Before you ask Claude", lead=0.1)
        crate = ImageMobject("pantry/a3_crate_34.png").set_height(2.1).move_to([0.0, -0.05, 0])
        crate.set_opacity(0.3)
        c2 = Dot([0.0, -1.45, 0], radius=0.14, color=GHOST).set_z_index(3)
        l2 = T("build", 36).move_to([0.0, -2.05, 0])
        self.play(FadeIn(crate), FadeIn(c2), FadeIn(l2), run_time=0.5)
        until(self, "commit a file", lead=0.2)
        p1 = a3_page(-3.8, 0.1)
        p1.shift(UP * 1.2)
        c1 = Dot([-3.8, -1.45, 0], radius=0.14, color=INK).set_z_index(3)
        self.play(p1.animate.shift(DOWN * 1.2), FadeIn(c1), rate_func=ease_in, run_time=0.55)
        l1 = M("CHANGE-BRIEF.md", 32).move_to([-3.8, -2.05, 0])
        self.play(FadeIn(l1), run_time=0.3)
        until(self, "Keep the original", lead=0.15)
        orig = T("original", 36).move_to([-3.8, 1.55, 0])
        tick = check(-2.55, 1.6, s=0.2)
        self.play(FadeIn(orig), Create(tick), run_time=0.4)
        until(self, "Add revisions", lead=0.25)
        p2 = a3_page(3.8, 0.1)
        p2.shift(UP * 1.2)
        c3 = Dot([3.8, -1.45, 0], radius=0.14, color=INK).set_z_index(3)
        self.play(p2.animate.shift(DOWN * 1.2), FadeIn(c3), rate_func=ease_in, run_time=0.5)
        l3 = T("revision", 36).move_to([3.8, -2.05, 0])
        self.play(FadeIn(l3), run_time=0.25)
        until(self, "rewrite it", lead=0.3)
        back = CurvedArrow(np.array([2.85, 0.75, 0]), np.array([-2.75, 0.75, 0]), angle=TAU / 5, color=INK, stroke_width=5, tip_length=0.24)
        self.play(Create(back), run_time=0.6)
        until(self, "every prediction", lead=0.2)
        no = a3_no(0.0, 1.62)
        self.play(GrowFromCenter(no), run_time=0.4)
        done(self)


# ── B22 · name, what it is, where it appears (an example brief entry for the real crate) ─────────────────────────────────
class B22_NameRoleWhere(Scene):
    def construct(self):
        ch, ccx, ccy = 4.0, -3.45, -0.25
        crate = ImageMobject("pantry/a3_crate_34.png").set_height(ch).move_to([ccx, ccy, 0])
        kc = ch / A3_CRATE_PX[1]
        edge = Polygon(*[a3_px(ccx, ccy, kc, A3_CRATE_PX, x, y) for x, y in A3_CRATE_OUTLINE], stroke_color=INK, stroke_width=6, fill_opacity=0)
        self.add(crate, edge)
        head = a3_left(M("CHANGE-BRIEF.md", 32), 0.3, 2.35)
        ex = a3_left(T("example", 32), 4.55, 2.35)
        self.play(FadeIn(head), FadeIn(ex), run_time=0.3)        # text only: the dot below is the first NEW shape (Gate A)
        # (key, key centre-above-baseline, value, value centre-above-baseline, baseline): offsets measured in Manim so the rows share a baseline
        base = [("name", 0.094, "Crate", 0.188, 1.0), ("what it is", 0.162, "a prop", 0.048, -0.1), ("where", 0.162, "the dock", 0.198, -1.2)]
        rows = [(k, v, yb + 0.12) for k, ko, v, vo, yb in base]                     # the dot sits at x-height
        keys = [a3_left(T(k, 32), 0.3, yb + ko) for k, ko, v, vo, yb in base]          # ink: DIM type risks GATE T's contrast floor
        vals = [a3_left(T(v, 40), 2.6, yb + vo) for k, ko, v, vo, yb in base]
        cue = ["its name", "what it is in your game", "where it appears"]
        mark = None
        for i in range(3):
            until(self, cue[i], lead=0.3)
            if mark is None:
                mark = a3_dot(-0.05, rows[i][2], r=0.11)
                self.play(FadeIn(keys[i]), FadeIn(vals[i]), GrowFromCenter(mark), run_time=0.3)
            else:
                self.play(FadeIn(keys[i]), FadeIn(vals[i]), mark.animate.move_to([-0.05, rows[i][2], 0]), run_time=0.3)
        done(self)


# ── B23 · size in metres, against something in the game ──────────────────────────────────────────────────────────────────
class B23_SizeInMetres(Scene):
    def construct(self):
        k, cx, cy = 0.00262, -3.0, -1.079
        crate = ImageMobject("pantry/a3_crate_34.png").set_height(A3_CRATE_PX[1] * k).move_to([cx, cy, 0])
        self.add(crate)
        P = lambda q: a3_px(cx, cy, k, A3_CRATE_PX, *q)
        lb, fb, rb, rt = P(A3_C_LB), P(A3_C_FB), P(A3_C_RB), P(A3_C_RT)
        until(self, "width", lead=0.25)
        w_a = dim_arrow(lb + np.array([-0.12, -0.33, 0]), fb + np.array([-0.12, -0.33, 0]))
        w_l = T("0.8 m wide", 36).move_to([-4.55, -3.0, 0])
        self.play(Create(w_a), FadeIn(w_l), run_time=0.4)
        until(self, "depth", lead=0.25)
        d_a = dim_arrow(fb + np.array([0.22, -0.27, 0]), rb + np.array([0.22, -0.27, 0]))
        d_l = T("0.8 m deep", 36).move_to([-0.55, -2.8, 0])
        self.play(Create(d_a), FadeIn(d_l), run_time=0.4)
        until(self, "height.", lead=0.25)
        h_a = dim_arrow(rb + np.array([0.4, 0, 0]), rt + np.array([0.4, 0, 0]))
        h_l = T("0.8 m tall", 36).move_to([0.05, -0.8, 0])
        self.play(Create(h_a), FadeIn(h_l), run_time=0.4)
        until(self, "the player's height", lead=0.45)
        u = (P(A3_C_FB)[1] - P(A3_C_FT)[1]) / -0.8           # units per metre at the crate's nearest corner (0.8 m edge)
        feet, tall = -2.5, 1.8 * u
        body = RoundedRectangle(width=1.0, height=tall - 0.72, corner_radius=0.45, fill_color=BAR2, fill_opacity=1,
                                stroke_color=INK, stroke_width=4).move_to([2.2, feet + (tall - 0.72) / 2, 0])
        head = Circle(radius=0.33, fill_color=BAR2, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([2.2, feet + tall - 0.33, 0])
        self.play(FadeIn(VGroup(body, head), shift=LEFT * 0.3), run_time=0.45)
        p_a = dim_arrow([3.3, feet, 0], [3.3, feet + tall, 0])
        p_l = T("player 1.8 m", 36).move_to([4.75, 0.15, 0])
        p_x = T("example", 32).move_to([4.75, -0.5, 0])
        self.play(Create(p_a), FadeIn(p_l), FadeIn(p_x), run_time=0.4)
        done(self)


# ── B24 · Blender and Godot both count in metres: the crate's 0.8 stays 0.8 ────────────────────────────────────────────────
class B24_SameUnits(Scene):
    def construct(self):
        k = 2.0 / A3_CRATE_PX[1]
        sx = (-3.4, 3.4)
        bl = ImageMobject("pantry/ev_icon_blender.png").set_height(1.0).move_to([sx[0] - 1.15, 2.45, 0])
        bl_n = T("Blender", 40).move_to([sx[0] + 0.55, 2.45, 0])
        crate = ImageMobject("pantry/a3_crate_34.png").set_height(2.0).move_to([sx[0] - 0.3, -0.45, 0])
        self.add(bl, bl_n, crate)
        fb_y = a3_px(sx[0] - 0.3, -0.45, k, A3_CRATE_PX, *A3_C_FB)[1]
        u = (A3_C_FB[1] - A3_C_FT[1]) * k / 0.8                       # units per metre at the crate's nearest corner

        def ruler(x):
            return VGroup(Line([x, fb_y, 0], [x, fb_y + u, 0], color=INK, stroke_width=6),
                          Line([x - 0.16, fb_y, 0], [x + 0.16, fb_y, 0], color=INK, stroke_width=6),
                          Line([x - 0.16, fb_y + u, 0], [x + 0.16, fb_y + u, 0], color=INK, stroke_width=6))
        until(self, "one unit is one metre", lead=0.25)
        r1 = ruler(sx[0] + 1.6)
        u1 = T("1 unit = 1 m", 36).move_to([sx[0], 1.2, 0])
        self.play(Create(r1), FadeIn(u1), run_time=0.5)
        until(self, "And Godot's", lead=0.25)
        gd = ImageMobject("pantry/ev_icon_godot.png").set_height(1.0).move_to([sx[1] - 1.15, 2.45, 0])
        gd_n = T("Godot", 40).move_to([sx[1] + 0.45, 2.45, 0])
        self.play(FadeIn(gd), FadeIn(gd_n), run_time=0.35)
        until(self, "units are metres too", lead=0.25)
        r2 = ruler(sx[1] + 1.6)
        u2 = T("1 unit = 1 m", 36).move_to([sx[1], 1.2, 0])
        self.play(Create(r2), FadeIn(u2), run_time=0.5)
        until(self, "So if you keep it", lead=0.2)
        o1 = M("0.800 x 0.800 x 0.800", 32).move_to([sx[0], -2.35, 0])
        self.play(FadeIn(o1), run_time=0.3)
        go = Arrow([-1.0, -0.45, 0], [1.0, -0.45, 0], buff=0, color=INK, stroke_width=6, tip_length=0.24)
        self.play(Create(go), run_time=0.3)
        until(self, "nothing needs converting", lead=0.75)
        copy = crate.copy()
        self.play(copy.animate.move_to([sx[1] - 0.3, -0.45, 0]), run_time=0.7)
        o2 = M("(0.8, 0.8, 0.8) m", 32).move_to([sx[1], -2.35, 0])
        self.play(FadeIn(o2), run_time=0.3)
        done(self)


# ── B25A · the origin: the point the model is placed and rotated from; on the floor, the centre of the underside ────────────
class B25A_Origin(Scene):
    def construct(self):
        s, x0, x1, y_air, y_floor = 3.5, -2.9, -0.3, 0.0, -1.0           # centred: the crate settles just left of centre, labels to its right
        crate = a3_crate_side(x0, y_air, s)
        self.add(crate)
        until(self, "origin:", lead=0.2)
        dot = a3_dot(x0, y_air)
        lab = T("origin", 36).move_to([x0, y_air - 0.55, 0])
        self.play(GrowFromCenter(dot), FadeIn(lab), run_time=0.35)
        until(self, "placed", lead=0.55)        # leads from the whisper word times of the re-voiced mp3 (placed 2.20 s)
        self.play(VGroup(crate, dot, lab).animate.shift(RIGHT * (x1 - x0)), run_time=0.55)
        until(self, "rotated", lead=0.6)         # rotated 2.78 s
        piv = np.array([x1, y_air, 0.0])
        self.play(Rotate(VGroup(crate, dot), angle=-0.4, about_point=piv), run_time=0.4)
        self.play(Rotate(VGroup(crate, dot), angle=0.4, about_point=piv), run_time=0.4)
        until(self, "For a prop", lead=0.3)
        floor = a3_floor(-5.1, 4.5, y_floor)
        fl = T("floor", 36).move_to([3.65, y_floor + 0.38, 0])
        self.play(Create(floor), FadeIn(fl), run_time=0.35)
        self.play(VGroup(crate, dot, lab).animate.shift(DOWN * (y_air - y_floor)), rate_func=ease_in, run_time=0.45)
        until(self, "the centre of the underside", lead=0.6)    # centre 6.02 s
        w = 0.4 * s
        a_l = dim_arrow([x1 - w, -2.2, 0], [x1, -2.2, 0], tip=0.22)          # tips >= GATE T size floor
        a_r = dim_arrow([x1, -2.2, 0], [x1 + w, -2.2, 0], tip=0.22)
        h_l = T("0.4 m", 38).move_to([x1 - w / 2, -2.78, 0])
        h_r = T("0.4 m", 38).move_to([x1 + w / 2, -2.78, 0])
        cl = T("centre of the underside", 36).move_to([3.55, -2.2, 0])
        self.play(GrowFromCenter(a_l), GrowFromCenter(a_r), FadeIn(h_l), FadeIn(h_r), FadeIn(cl), run_time=0.5)
        done(self)


# ── B25B · Blender's world origin: three axes meet at a point on the floor; the crate is built with its base there ───────────
# (isometric drawing; the real-window version failed GATE T: Blender's dark viewport sits inside its INK tolerance, so any crop of it reads as text)
def a3_crate_iso(iso, w=0.8, alpha=0.62):
    """The crate in isometric, centred on (0, 0), base at z = 0: wood faces, band-coloured lid, bottom bands and a centre strap per face.
    Fills are see-through (like Blender's X-ray) so the axes and the origin show inside; edges are ink."""
    h = w
    x0, y0, x1, y1 = -w / 2, -w / 2, w / 2, w / 2
    b, t = 0.1, 0.05
    Q = lambda pts, c: iso.quad(pts, c, stroke=c, sw=0).set_fill(c, opacity=alpha)
    left = [(x0, y0, 0), (x0, y1, 0), (x0, y1, h), (x0, y0, h)]           # the x = x0 face
    right = [(x0, y0, 0), (x1, y0, 0), (x1, y0, h), (x0, y0, h)]          # the y = y0 face
    top = [(x0, y0, h), (x1, y0, h), (x1, y1, h), (x0, y1, h)]
    fills = VGroup(Q(left, A3_WOOD), Q(right, "#A06F42"), Q(top, A3_BAND),
                   Q([(x0, y0, 0), (x0, y1, 0), (x0, y1, b), (x0, y0, b)], A3_BAND),
                   Q([(x0, y0, 0), (x1, y0, 0), (x1, y0, b), (x0, y0, b)], A3_BAND),
                   Q([(x0, -t, 0), (x0, t, 0), (x0, t, h), (x0, -t, h)], A3_BAND),
                   Q([(-t, y0, 0), (t, y0, 0), (t, y0, h), (-t, y0, h)], A3_BAND))
    edges = VGroup(*[Polygon(*[iso.p(*q) for q in f], fill_opacity=0, stroke_color=INK, stroke_width=4) for f in (left, right, top)])
    fills.set_z_index(1); edges.set_z_index(3)
    return VGroup(fills, edges)


class B25B_WorldOrigin(Scene):
    def construct(self):
        iso = Iso(-1.3, -0.1, 1.6)
        L = 1.6                                                              # axis half-length, metres
        ax_x = Line(iso.p(-L, 0, 0), iso.p(L, 0, 0), color=DIM, stroke_width=6)
        ax_y = Line(iso.p(0, -L, 0), iso.p(0, L, 0), color=DIM, stroke_width=6)
        ax_z = Line(iso.p(0, 0, 0), iso.p(0, 0, L), color=DIM, stroke_width=6)
        VGroup(ax_x, ax_y, ax_z).set_z_index(2)                             # axes show through the see-through crate
        lx, ly, lz = T("X", 36).move_to(iso.p(L + 0.25, 0, 0)), T("Y", 36).move_to(iso.p(0, L + 0.25, 0)), T("Z", 36).move_to(iso.p(0, 0, L + 0.25))
        floor = Polygon(*[iso.p(x, y, 0) for x, y in ((-1.0, -1.0), (1.0, -1.0), (1.0, 1.0), (-1.0, 1.0))], fill_opacity=0, stroke_color=DIM, stroke_width=3)
        self.add(floor)
        until(self, "world origin", lead=0.4)
        self.play(Create(ax_x), Create(ax_y), Create(ax_z), FadeIn(lx), FadeIn(ly), FadeIn(lz), run_time=0.7)
        until(self, "the point where", lead=0.3)
        o = iso.p(0, 0, 0)
        start = iso.p(-1.2, 0, 0)
        dot = a3_dot(start[0], start[1], r=0.14)
        key = a3_dot(2.25, 1.25, r=0.13)
        kl = a3_left(T("world origin", 36), 2.6, 1.25)
        self.play(GrowFromCenter(dot), GrowFromCenter(key), FadeIn(kl), run_time=0.3)
        self.play(MoveAlongPath(dot, Line(np.array(start), np.array(o))), run_time=0.55)
        until(self, "with the base on the floor", lead=0.3)
        crate = a3_crate_iso(iso)
        crate.shift(UP * 1.6)
        self.play(FadeIn(crate), run_time=0.15)
        self.play(crate.animate.shift(DOWN * 1.6), rate_func=ease_in, run_time=0.45)
        l1 = a3_left(M("origin at world (0.000, 0.000, 0.000)", 32), -5.6, -2.35)
        l2 = a3_left(M("lowest point z = 0.0000 m", 32), -5.6, -2.95)
        self.play(FadeIn(l1), run_time=0.3)
        self.play(FadeIn(l2), run_time=0.3)
        done(self)


# ── B26A · origin in the middle: at floor level it sinks (-0.4 m); lifted by a guess it floats (+0.1 m) ─────────────────────
class B26A_SinkFloat(Scene):
    def construct(self):
        s = A3_S
        floor = a3_floor()
        fl = T("floor", 36).move_to([-0.2, A3_F + 0.38, 0])
        c1 = a3_crate_side(A3_XL, A3_F)
        d1 = a3_dot(A3_XL, A3_F)
        self.add(c1, floor, fl, d1)
        until(self, "in the middle", lead=0.2)
        self.play(d1.animate.move_to([A3_XL, A3_F + 0.4 * s, 0]), run_time=0.5)
        until(self, "won't sit on the floor", lead=0.95)    # whisper: "won't" 2.28 s
        self.play(VGroup(c1, d1).animate.shift(DOWN * 0.4 * s), rate_func=ease_in, run_time=0.55)
        sk = T("sinks", 36).move_to([A3_XL, -1.95, 0])
        self.play(FadeIn(sk), run_time=0.25)
        until(self, "it sinks half", lead=0.8)    # sinks 4.92 s
        g1 = M("gap to floor = -0.4 m", 32).move_to([A3_XL, -2.6, 0])
        self.play(FadeIn(g1), run_time=0.3)
        until(self, "Lift it by a guess", lead=0.75)    # lift 6.34 s
        c2 = a3_crate_side(A3_XR, A3_F - 0.4 * s)
        d2 = a3_dot(A3_XR, A3_F)
        self.play(FadeIn(c2), FadeIn(d2), run_time=0.3)
        up = Arrow([A3_XR + 1.6, A3_F, 0], [A3_XR + 1.6, A3_F + 0.5 * s, 0], buff=0, color=INK, stroke_width=6, tip_length=0.22)
        ul = T("+0.5 m", 34).move_to([A3_XR + 2.55, A3_F + 0.25 * s, 0])
        self.play(VGroup(c2, d2).animate.shift(UP * 0.5 * s), GrowArrow(up), FadeIn(ul), run_time=0.6)
        ft = T("floats", 36).move_to([A3_XR, -1.95, 0])
        g2 = M("gap to floor = 0.1 m", 32).move_to([A3_XR, -2.6, 0])
        self.play(FadeIn(ft), FadeIn(g2), run_time=0.3)
        done(self)


# ── B26B · lifted by exactly 0.4 m it sits and the gap check PASSES; the origin check FAILS it ─────────────────────────────
class B26B_OriginCheck(Scene):
    def construct(self):
        s = A3_S
        floor = a3_floor()
        fl = T("floor", 36).move_to([-0.2, A3_F + 0.38, 0])
        c1 = a3_crate_side(A3_XL, A3_F - 0.4 * s)
        d1 = a3_dot(A3_XL, A3_F)
        sk = T("sinks", 36).move_to([A3_XL, -1.95, 0])
        g1 = M("gap to floor = -0.4 m", 32).move_to([A3_XL, -2.6, 0])
        c2 = a3_crate_side(A3_XR, A3_F + 0.1 * s)
        d2 = a3_dot(A3_XR, A3_F + 0.5 * s)
        up = Arrow([A3_XR + 1.6, A3_F, 0], [A3_XR + 1.6, A3_F + 0.5 * s, 0], buff=0, color=INK, stroke_width=6, tip_length=0.22)
        ul = T("+0.5 m", 34).move_to([A3_XR + 2.55, A3_F + 0.25 * s, 0])
        ft = T("floats", 36).move_to([A3_XR, -1.95, 0])
        g2 = M("gap to floor = 0.1 m", 32).move_to([A3_XR, -2.6, 0])
        self.add(c1, c2, floor, fl, d1, d2, sk, g1, up, ul, ft, g2)
        self.play(FadeOut(VGroup(c2, d2, up, ul, ft, g2, sk, g1)), fl.animate.move_to([5.35, A3_F + 0.38, 0]), run_time=0.35)
        lift = Arrow([A3_XL + 1.6, A3_F, 0], [A3_XL + 1.6, A3_F + 0.4 * s, 0], buff=0, color=INK, stroke_width=6, tip_length=0.22)
        ll = T("moved 0.4 m", 34).move_to([A3_XL + 3.15, A3_F + 0.2 * s, 0])
        self.play(VGroup(c1, d1).animate.shift(UP * 0.4 * s), GrowArrow(lift), FadeIn(ll), run_time=0.7)
        until(self, "and it sits", lead=0.15)
        p1 = a3_left(M("gap to floor = 0.0 m", 32), 1.0, 2.05)
        p2 = a3_left(M("PASS", 32), 1.0, 1.35)
        pt = check(2.45, 1.4, s=0.2)
        self.play(FadeIn(p1), FadeIn(p2), Create(pt), run_time=0.4)
        until(self, "only because you moved it", lead=0.2)
        self.play(Indicate(VGroup(lift, ll), color=INK, scale_factor=1.12), run_time=0.7)
        until(self, "look at the origin", lead=0.35)
        ring = Circle(radius=0.34, stroke_color=INK, stroke_width=7).move_to([A3_XL, A3_F + 0.4 * s, 0]).set_z_index(5)
        self.play(GrowFromCenter(ring), run_time=0.35)
        f = [M("FAIL crate_origin_centre.glb:", 32), M("the origin is 0.4 m above the base:", 32),
             M("it sits on the floor only because", 32), M("the node was moved", 32)]
        for i, m in enumerate(f):
            a3_left(m, -5.75, -1.0 - 0.6 * i)
        self.play(FadeIn(VGroup(*f)), run_time=0.45)
        until(self, "not just the gap", lead=0.2)
        self.play(VGroup(p1, p2, pt).animate.set_opacity(0.3), run_time=0.45)
        done(self)


# ── B27 · look and budget: the real lantern, its real materials, its real 202 triangles ────────────────────────────────────
class B27_LookBudget(Scene):
    def construct(self):
        h, cx, cy = 5.4, -3.6, 0.0
        k = h / A3_LANTERN_PX[1]
        lan = ImageMobject("pantry/a3_lantern_34.png").set_height(h).move_to([cx, cy, 0])
        self.add(lan)
        P = lambda x, y: a3_px(cx, cy, k, A3_LANTERN_PX, x, y)
        until(self, "the shape that makes it", lead=0.25)
        outline = Polygon(*[P(x, y) for x, y in A3_LANTERN_OUTLINE], stroke_color=INK, stroke_width=5, fill_opacity=0)
        self.play(Create(outline), run_time=0.9)
        until(self, "material colours", lead=0.3)
        mats = [("DarkIron", P(400, 215), 1.29), ("Flame", P(262, 323), 0.59), ("WarmGlass", P(370, 455), -0.28)]
        leads, labs = [], []
        for name, at, y in mats:
            leads.append(Line(np.array([at[0], y, 0]), np.array([-1.45, y, 0]), color=INK, stroke_width=4))
            labs.append(a3_left(T(name, 36), -1.15, y))
        self.play(*[Create(l) for l in leads], *[FadeIn(l) for l in labs], run_time=0.5)
        until(self, "Its budget", lead=0.0)                          # starts just after the midpoint: no empty bar in the sampled frame
        x0, x5, by = 1.5, 5.9, -0.3
        bar = Rectangle(width=x5 - x0, height=0.6, fill_opacity=0, stroke_color=DIM, stroke_width=4).move_to([(x0 + x5) / 2, by, 0])
        fill = Rectangle(width=0.02, height=0.6, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([x0 + 0.01, by, 0])
        self.play(Create(bar), run_time=0.25)
        self.add(fill)
        wf = 202 / 500 * (x5 - x0)
        self.play(fill.animate.stretch_to_fit_width(wf).move_to([x0 + wf / 2, by, 0]), run_time=0.75)
        n = a3_left(T("202", 96), x0, 1.3)
        nl = a3_left(T("triangles", 36), x0 + 1.89 + 0.3, 1.1)        # "202" at size 96 is 1.89 wide (measured; Gate A's stub cannot measure)
        spark = a3_dot(x0 + wf, by + 0.55, r=0.11)
        self.play(FadeIn(n), FadeIn(nl), GrowFromCenter(spark), run_time=0.35)
        until(self, "at or under five hundred", lead=0.2)
        cap = T("500", 36).move_to([x5 - 0.3, by - 0.7, 0])
        sh = a3_left(T("5 shapes", 36), x0, -1.95)
        self.play(FadeIn(cap), bar.animate.set_stroke(INK, 5), run_time=0.35)
        self.play(FadeIn(sh), run_time=0.3)
        done(self)


# ── B28 · four predicted failures, each with the check that catches it (three are real runs; the server one is not run) ────
class B28_FourFailures(Scene):
    def construct(self):
        W, H = 5.9, 2.85
        cen = [(-3.05, 1.6), (3.05, 1.6), (-3.05, -1.6), (3.05, -1.6)]
        panels = [RoundedRectangle(width=W, height=H, corner_radius=0.2, fill_opacity=0, stroke_color=DIM, stroke_width=4).move_to([x, y, 0])
                  for x, y in cen]
        # an empty slot holds only its number (ink: numerals are ink) until its failure is named; the check mark lands LAST
        nums = [a3_left(T(str(i + 1), 36), x - W / 2 + 0.35, y + H / 2 - 0.5) for i, (x, y) in enumerate(cen)]
        for i, cue in enumerate(["at least", "three", "predicted", "failures"]):
            until(self, cue, lead=0.15)
            self.play(Create(panels[i]), FadeIn(nums[i]), run_time=0.3)

        def label(i, s):                       # top-left of the panel: the predicted failure (takes the number's place)
            x, y = cen[i]
            return a3_left(T(s, 36), x - W / 2 + 0.35, y + H / 2 - 0.5)

        def line(i, mob):                      # bottom row: what the check reports
            x, y = cen[i]
            return a3_left(mob, x - W / 2 + 1.0, y - H / 2 + 0.5)

        def tick(i):                           # the check mark, beside the check's report
            x, y = cen[i]
            return check(x - W / 2 + 0.55, y - H / 2 + 0.55, s=0.19)
        # pictures sit in the upper right of each panel, on a base line 0.2 below the panel's centre

        # 1 · lying on its side (Godot 4.7.2, +Y Up off: longest axis Z) - the real lantern render topples about its corner
        until(self, "It arrives", lead=0.25)
        x, y = cen[0]
        lh = 1.45
        lw = lh * A3_LANTERN_PX[0] / A3_LANTERN_PX[1]
        lan1 = ImageMobject("pantry/a3_lantern_34.png").set_height(lh).move_to([x + 0.75, y - 0.2 + lh / 2, 0])
        self.play(FadeOut(nums[0]), FadeIn(label(0, "lying on its side")), FadeIn(lan1), FadeIn(line(0, M("longest axis Z", 32))), run_time=0.3)
        self.play(Rotate(lan1, angle=-PI / 2, about_point=np.array([x + 0.75 + lw / 2, y - 0.2, 0.0])), run_time=0.5)
        self.play(Create(tick(0)), run_time=0.2)
        # 2 · ten times too big (every axis x10: the real run printed (3.0, 5.0, 3.0) m against the brief's (0.3, 0.5, 0.3))
        until(self, "wrong by a factor", lead=0.35)
        x, y = cen[1]
        lan2 = ImageMobject("pantry/a3_lantern_34.png").set_height(0.42).move_to([x + 1.65, y - 0.2 + 0.21, 0])
        self.play(FadeOut(nums[1]), FadeIn(label(1, "ten times too big")), FadeIn(lan2), run_time=0.3)
        self.play(lan2.animate.scale(1.45 / 0.42, about_edge=DOWN), run_time=0.6)
        self.play(FadeIn(line(1, M("(3.0, 5.0, 3.0) m", 32))), run_time=0.3)
        self.play(Create(tick(1)), run_time=0.2)
        # 3 · the server won't connect (predicted; the MCP route was not run, so no output is shown)
        until(self, "The server", lead=0.3)
        x, y = cen[2]
        py = y + 0.25
        sock = RoundedRectangle(width=0.75, height=1.1, corner_radius=0.12, fill_color=BAR1, fill_opacity=1, stroke_color=INK,
                                stroke_width=4).move_to([x + 2.3, py, 0])
        holes = VGroup(*[Circle(radius=0.08, fill_color=INK, fill_opacity=1, stroke_width=0).move_to([x + 2.15, py + d, 0]) for d in (0.22, -0.22)])
        plug = VGroup(RoundedRectangle(width=0.7, height=0.8, corner_radius=0.12, fill_color=A3_WOOD, fill_opacity=1, stroke_color=INK,
                                       stroke_width=4).move_to([x + 0.3, py, 0]),
                      *[Line([x + 0.65, py + d, 0], [x + 0.97, py + d, 0], color=DIM, stroke_width=9) for d in (0.22, -0.22)],
                      Line([x - 0.05, py, 0], [x - 0.75, py, 0], color=A3_BAND, stroke_width=9))
        self.play(FadeOut(nums[2]), FadeIn(label(2, "won't connect")), FadeIn(sock), FadeIn(holes), FadeIn(plug), run_time=0.3)
        self.play(plug.animate.shift(RIGHT * 0.6), run_time=0.45)
        nr = a3_left(T("not run", 32), x - W / 2 + 3.4, y + H / 2 - 0.5)
        self.play(FadeIn(line(2, T("MCP for Blender tab", 36))), FadeIn(nr), run_time=0.3)     # 36: at 32 Pango splits "Blen der"
        self.play(Create(tick(2)), run_time=0.2)
        # 4 · a colour does not survive the export (Godot reads albedo #E7E7E7 for both of the crate's materials)
        until(self, "A colour", lead=0.3)
        x, y = cen[3]
        cr = a3_crate_side(x + 1.65, y - 0.2, s=1.8)
        self.play(FadeOut(nums[3]), FadeIn(label(3, "colour lost")), FadeIn(cr), run_time=0.3)
        self.play(*[cr[i].animate.set_fill("#E7E7E7") for i in range(4)], run_time=0.7)
        self.play(FadeIn(line(3, M("albedo #E7E7E7", 32))), run_time=0.3)
        self.play(Create(tick(3)), run_time=0.2)
        done(self)
