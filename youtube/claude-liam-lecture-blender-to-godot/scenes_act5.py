"""ACT V · Building the Post, Then Checking the Builder — part 1 (B45–B58)

One cast for the act: the CHECKPOINT POST, as the REAL Blender render (pantry/a5_post.png, Blender 5.1.2 Workbench, same camera as
the act-6 builder's pantry/post_visual.png, re-rendered at 2x from the first agent's own run-1 script), with every mark placed on
the real pixels through the camera projection of the real script's 3D points (evidence/act5/post_anchors.json, inlined below
because Gate A copies only scenes.py). The run-1 collision BOX (0.6 x 0.6 x 1.8 m) is pantry/a5_box.png, same crop.
B48, B49, B50, B51 and B54 (the Claude Code session) are Remotion `CCSession` beats: see lanes/act5.json and SESSION-act5.md.
B45–B47B, B52, B53, B55 and B56–B58 are Manim and live here (B52/B53/B55 are drawn from the session's result and system events, which a
`-p` run never printed on a screen). B58_X0 / B58_YF / B58_S fix the post's place on the floor if a later beat wants to continue it.
"""

# ── the real post: crop-pixel anchors from evidence/act5/post_anchors.json (crop 1457 x 1943 px, origin top-left) ─────────────────
A5_PT = {
    "z0_c": (735.5, 1723.2), "pole_top_c": (731.0, 104.3), "pole_bot_c": (735.3, 1637.7), "w_a": (195.7, 1792.1),
    "w_b": (611.1, 1915.8), "h_a": (37.4, 1744.9), "h_b": (-5.9, 106.7), "t_edge": (356.1, 1692.0),
    "pen_tl": (788.8, 105.9), "pen_tr": (1092.9, 114.4), "pen_br": (1090.7, 362.0), "pen_bl": (789.0, 343.2),
    "pen_len_a": (715.0, 108.9), "pen_len_b": (1020.8, 117.7), "pen_h_a": (1148.9, 115.9),
    "pen_h_b": (1146.2, 365.5), "floor_a": (-480.9, 1761.0), "floor_b": (860.9, 2201.3), "floor_c": (1903.2, 1687.0),
    "floor_d": (653.4, 1410.4), "lift16": (735.1, 1586.2), "lift158": (735.1, 1587.8), "ray_start158": (730.0, -239.2), "ray_top": (730.4, -86.6), "ray_bot": (735.5, 1723.2),
    "base_mm_0": (356.8, 1735.0), "base_mp_0": (706.1, 1611.2), "base_pm_0": (769.0, 1851.1),
    "base_pp_0": (1109.4, 1711.6), "base_mm_1": (355.4, 1649.0), "base_mp_1": (705.8, 1530.7),
    "base_pm_1": (768.9, 1759.9), "base_pp_1": (1110.2, 1626.6), "box_mm_0": (356.8, 1735.0),
    "box_mm_18": (331.3, 105.6), "box_mp_0": (706.1, 1611.2), "box_mp_18": (700.4, 91.9),
    "box_pm_0": (769.0, 1851.1), "box_pm_18": (766.2, 118.6), "box_pp_0": (1109.4, 1711.6),
    "box_pp_18": (1125.2, 103.0), "pole_top_0": (788.8, 105.9), "pole_top_1": (805.7, 104.0),
    "pole_top_2": (779.1, 102.4), "pole_top_3": (724.9, 101.8), "pole_top_4": (674.2, 102.7),
    "pole_top_5": (656.0, 104.5), "pole_top_6": (681.9, 106.2), "pole_top_7": (737.2, 106.8),
}
A5_CROP_W, A5_CROP_H = 1457, 1943
A5_S = 0.0030                                   # scene units per crop pixel (the 1.8 m pole is ~4.4 units tall)
A5_ORG = (735.5, 1723.2)                        # crop pixel of the pole's foot (world 0, 0, 0)


def a5_P(key, x0, yf, s=A5_S):
    """Scene point of a real anchor when the pole's foot sits at scene (x0, yf)."""
    px, py = A5_PT[key]
    return np.array([x0 + (px - A5_ORG[0]) * s, yf + (A5_ORG[1] - py) * s, 0.0])


def a5_img(path, x0, yf, s=A5_S, opacity=1.0):
    """The real render, placed so the pole's foot lands on (x0, yf)."""
    im = ImageMobject(path)
    im.set_height(A5_CROP_H * s)
    im.move_to([x0 + (A5_CROP_W / 2 - A5_ORG[0]) * s, yf + (A5_ORG[1] - A5_CROP_H / 2) * s, 0])
    if opacity < 1.0:
        im.set_opacity(opacity)
    return im


def a5_floor(x0, yf, k=0.72, s=A5_S):
    """A ghost floor tile under the post (the real floor quad's corners, pulled in so it stays on stage)."""
    org = a5_P("z0_c", x0, yf, s)
    pts = []
    for key in ("floor_a", "floor_b", "floor_c", "floor_d"):
        p = a5_P(key, x0, yf, s)
        pts.append(org + (p - org) * k)
    return Polygon(*pts, fill_color=GHOST, fill_opacity=1, stroke_width=0)


def a5_lbl(s, x, y, size=36, color=INK):
    return T(s, size, color).move_to([x, y, 0])


# ── B45 · the job, drawn on the real render ──────────────────────────────────────────────────────────────────────────────────
A5_X0, A5_YF = -0.3, -2.25


def a5_b45_marks(x0, yf):
    """Every B45 mark, built in one place so B46 can start from exactly B45's last frame."""
    s = A5_S
    # base: 0.6 m x 0.6 m, one arrow along each front edge (offset outward from the edge, in screen space)
    a0, a1 = a5_P("base_mm_0", x0, yf), a5_P("base_pm_0", x0, yf)
    b0, b1 = a5_P("base_pm_0", x0, yf), a5_P("base_pp_0", x0, yf)
    wl = dim_arrow(a0 + np.array([-0.08, -0.3, 0]), a1 + np.array([-0.08, -0.3, 0]))
    wr = dim_arrow(b0 + np.array([0.12, -0.28, 0]), b1 + np.array([0.12, -0.28, 0]))
    wl_l = a5_lbl("0.6 m", a0[0] - 0.95, a0[1] - 0.62)
    wr_l = a5_lbl("0.6 m", b1[0] + 1.0, b1[1] - 0.55)
    # thickness: a leader from the base's left corner edge to its label, terracotta dot on the edge
    te = a5_P("t_edge", x0, yf)
    th_dot = Dot(te + np.array([0.0, 0.0, 0]), radius=0.1, color=TERRA)
    th_ld = Line(te + np.array([-0.12, 0.0, 0]), [te[0] - 1.35, te[1] + 0.35, 0], color=INK, stroke_width=4)
    th_l = a5_lbl("0.1 m", te[0] - 2.05, te[1] + 0.4)
    # eight-sided pole: a top-down octagon (vertex on +X, as the script builds it), leader to a dot on the pole
    oct_c = np.array([x0 - 3.05, yf + 2.35, 0])
    octo = RegularPolygon(n=8, radius=0.5, start_angle=0, color=INK, stroke_width=6).move_to(oct_c)
    oct_l = a5_lbl("8 sides", oct_c[0], oct_c[1] - 0.95)
    pole_pt = np.array([x0 - 0.12, yf + 2.35, 0])
    o_ld = Line([oct_c[0] + 0.62, oct_c[1], 0], [pole_pt[0] - 0.12, pole_pt[1], 0], color=INK, stroke_width=4)
    o_dot = Dot(pole_pt, radius=0.1, color=TERRA)
    # height: 1.8 m, to the right of the pennant, on the world line (0.55, 0, 0..1.8)
    ha = a5_P("pen_h_a", x0, yf)
    hb = np.array([ha[0] + 0.0, yf + 0.0, 0.0])
    h_arrow = dim_arrow(hb + np.array([0.72, -0.05, 0]), ha + np.array([0.72, 0.0, 0]))
    h_l = a5_lbl("1.8 m", ha[0] + 1.95, yf + 2.3)
    return dict(wl=wl, wr=wr, wl_l=wl_l, wr_l=wr_l, th_dot=th_dot, th_ld=th_ld, th_l=th_l, octo=octo, oct_l=oct_l, o_ld=o_ld,
                o_dot=o_dot, h_arrow=h_arrow, h_l=h_l)


class B45_TheJob(Scene):
    def construct(self):
        x0, yf = A5_X0, A5_YF
        title = T("Building the Post, Then Checking the Builder", 40).move_to([-0.2, 3.1, 0])
        floor = a5_floor(x0, yf)
        post = a5_img("pantry/a5_post.png", x0, yf)
        self.add(floor, title)
        m = a5_b45_marks(x0, yf)
        until(self, "a low-poly", lead=0.2)
        self.play(FadeIn(post), run_time=0.7)
        until(self, "point six", lead=0.35)
        self.play(Create(m["wl"]), Create(m["wr"]), FadeIn(m["wl_l"]), FadeIn(m["wr_l"]), run_time=0.6)
        until(self, "a tenth", lead=0.65)
        self.play(FadeIn(m["th_dot"]), Create(m["th_ld"]), FadeIn(m["th_l"]), run_time=0.5)
        until(self, "eight-sided", lead=0.4)
        self.play(Create(m["octo"]), FadeIn(m["oct_l"]), run_time=0.5)
        self.play(Create(m["o_ld"]), FadeIn(m["o_dot"]), run_time=0.4)
        until(self, "one point eight", lead=0.3)
        self.play(Create(m["h_arrow"]), FadeIn(m["h_l"]), run_time=0.6)
        done(self)


# ── B46 · pennant, two materials, a separate collision box ───────────────────────────────────────────────────────────────────
class B46_PennantMaterialsCollider(Scene):
    def construct(self):
        x0, yf = A5_X0, A5_YF
        title = T("Building the Post, Then Checking the Builder", 40).move_to([-0.2, 3.1, 0])
        floor = a5_floor(x0, yf)
        post = a5_img("pantry/a5_post.png", x0, yf)
        m = a5_b45_marks(x0, yf)
        old = VGroup(*[m[k] for k in m], title)
        self.add(floor, post, old)
        # the base and pole marks go; the pennant's arrive
        bl, br = a5_P("pen_bl", x0, yf), a5_P("pen_br", x0, yf)
        tr, brr = a5_P("pen_h_a", x0, yf), a5_P("pen_h_b", x0, yf)
        pen_len = dim_arrow(bl + np.array([0.0, -0.4, 0]), br + np.array([0.0, -0.4, 0]))
        pen_len_l = a5_lbl("0.4 m", (bl[0] + br[0]) / 2 + 0.55, bl[1] - 0.95)
        pen_h = dim_arrow(brr + np.array([0.5, 0.0, 0]), tr + np.array([0.5, 0.0, 0]))
        pen_h_l = a5_lbl("0.25 m", tr[0] + 1.6, (tr[1] + brr[1]) / 2)
        att = Dot(a5_P("pen_tl", x0, yf) + np.array([0.0, -0.03, 0]), radius=0.1, color=TERRA)
        self.play(FadeOut(old), run_time=0.4)
        until(self, "point four", lead=0.2)
        self.play(Create(pen_len), FadeIn(pen_len_l), run_time=0.5)
        until(self, "a quarter", lead=0.25)
        self.play(Create(pen_h), FadeIn(pen_h_l), run_time=0.5)
        until(self, "hangs from the top", lead=0.25)
        self.play(FadeIn(att), run_time=0.3)
        # the materials: a leader and a swatch per name (after the midpoint: the dims leave as the tags land)
        pole_pt = np.array([x0 - 0.1, yf + 1.5, 0])
        pm_dot = Dot(pole_pt, radius=0.1, color=TERRA)
        pm_ld = Line([pole_pt[0] - 0.12, pole_pt[1], 0], [x0 - 2.2, pole_pt[1], 0], color=INK, stroke_width=4)
        pm_sw = Circle(radius=0.22, fill_color="#7C8088", fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([x0 - 2.5, pole_pt[1], 0])
        pm_l = a5_lbl("PostMetal", x0 - 4.3, pole_pt[1])
        pen_c = np.array([(bl[0] + br[0]) / 2, (bl[1] + a5_P("pen_tl", x0, yf)[1]) / 2, 0])
        fc_dot = Dot(pen_c, radius=0.1, color=TERRA)
        fc_ld = Line([pen_c[0] + 0.12, pen_c[1], 0], [pen_c[0] + 0.55, pen_c[1], 0], color=INK, stroke_width=4)
        fc_sw = Circle(radius=0.22, fill_color="#9B6150", fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([pen_c[0] + 0.8, pen_c[1], 0])
        fc_l = a5_lbl("FlagCloth", pen_c[0] + 2.15, pen_c[1])
        until(self, "PostMetal", lead=0.3)
        self.play(FadeOut(VGroup(pen_len, pen_len_l, pen_h, pen_h_l, att)), FadeIn(pm_dot), Create(pm_ld), FadeIn(pm_sw), FadeIn(pm_l), run_time=0.5)
        until(self, "FlagCloth", lead=0.3)
        self.play(FadeIn(fc_dot), Create(fc_ld), FadeIn(fc_sw), FadeIn(fc_l), run_time=0.5)
        # the collider: a separate box, same crop and scale, off to the side
        bx = 5.0
        box = a5_img("pantry/a5_box.png", bx, yf, opacity=0.55)
        edges = VGroup(*[Line(a5_P(a, bx, yf), a5_P(b, bx, yf), color=DIM, stroke_width=4) for a, b in [
            ("box_mm_0", "box_pm_0"), ("box_pm_0", "box_pp_0"), ("box_mm_18", "box_pm_18"), ("box_pm_18", "box_pp_18"),
            ("box_mm_0", "box_mm_18"), ("box_pm_0", "box_pm_18"), ("box_pp_0", "box_pp_18")]])
        bx_l = a5_lbl("collider", bx, yf + 5.2)
        bx_l2 = a5_lbl("base + pole", bx, yf - 0.83, 34)
        until(self, "separate collision", lead=0.3)
        self.play(FadeIn(box), Create(edges), FadeIn(bx_l), run_time=0.7)
        until(self, "around the base", lead=0.25)
        self.play(FadeIn(bx_l2), run_time=0.4)
        done(self)


# ── B47A / B47B · four predictions on one board ──────────────────────────────────────────────────────────────────────────────
A5_CELLS = [(-3.15, 1.15), (3.15, 1.15), (-3.15, -1.8), (3.15, -1.8)]
A5_CW, A5_CH = 5.8, 2.6


def a5_cell(i):
    """One prediction cell: (frame, [cue parts in draw order]). Every part is drawn small and outline-only."""
    cx, cy = A5_CELLS[i]
    frame = RoundedRectangle(width=A5_CW, height=A5_CH, corner_radius=0.25, fill_opacity=0, stroke_color=DIM, stroke_width=5).move_to([cx, cy, 0])
    parts = []
    if i == 0:                                      # which Godot axis carries the 1.8?
        thumb = a5_img("pantry/a5_post.png", cx - 1.9, cy - 0.78, s=0.0009)
        l18 = T("1.8 m", 34).move_to([cx - 0.95, cy - 0.05, 0])
        o = np.array([cx + 1.0, cy - 0.2, 0])
        ax = Arrow(o, o + np.array([0.85, -0.4, 0]), buff=0, color=INK, stroke_width=5, tip_length=0.16)
        ay = Arrow(o, o + np.array([0.0, 0.9, 0]), buff=0, color=INK, stroke_width=5, tip_length=0.16)
        az = Arrow(o, o + np.array([-0.85, -0.4, 0]), buff=0, color=INK, stroke_width=5, tip_length=0.16)
        lx = T("X", 34).move_to(o + np.array([1.15, -0.62, 0])); ly = T("Y", 34).move_to(o + np.array([0.0, 1.2, 0]))
        lz = T("Z", 34).move_to(o + np.array([-1.15, -0.62, 0]))
        q = T("?", 64).move_to([cx + 2.4, cy + 0.3, 0])
        parts = [Group(thumb, l18), VGroup(ax, ay, az, lx, ly, lz), q]
    elif i == 1:                                    # the bounding box with +Y up off
        chips = VGroup()
        for k, ax_ in enumerate("XYZ"):
            x = cx - 1.55 + k * 1.55
            ch = RoundedRectangle(width=1.15, height=1.25, corner_radius=0.18, fill_opacity=0, stroke_color=DIM, stroke_width=5).move_to([x, cy + 0.2, 0])
            chips.add(VGroup(ch, T(ax_, 34, DIM).move_to([x, cy + 0.48, 0]), T("?", 54).move_to([x, cy + 0.0, 0])))
        lab = T("Y up off", 36).move_to([cx, cy - 0.85, 0])
        parts = [chips, lab]
    elif i == 2:                                    # a scale that was never applied
        tag = RoundedRectangle(width=3.3, height=1.15, corner_radius=0.2, fill_opacity=0, stroke_color=INK, stroke_width=5).move_to([cx - 0.2, cy + 0.12, 0])
        hole = Circle(radius=0.11, color=INK, stroke_width=4).move_to([cx + 1.25, cy + 0.12, 0])
        string = Line([cx + 1.33, cy + 0.2, 0], [cx + 2.15, cy + 0.9, 0], color=INK, stroke_width=4)
        t1 = T("scale", 34).move_to([cx - 0.35, cy + 0.37, 0]); t2 = T("? ? ?", 44).move_to([cx - 0.35, cy - 0.05, 0])
        lab = T("never applied", 34).move_to([cx - 0.2, cy - 0.85, 0])
        parts = [VGroup(tag, hole, string), VGroup(t1, t2), lab]
    else:                                           # a collider named -convcolonly, demo's import file copied
        pg = Rectangle(width=0.8, height=1.05, fill_opacity=0, stroke_color=INK, stroke_width=5).move_to([cx - 2.0, cy + 0.2, 0])
        ln = VGroup(*[Line([cx - 2.22, cy + 0.2 + dy, 0], [cx - 1.78, cy + 0.2 + dy, 0], color=DIM, stroke_width=4) for dy in (0.25, 0.05, -0.15)])
        pl = T("import", 32).move_to([cx - 2.0, cy - 0.82, 0])
        arr = Arrow([cx - 1.35, cy + 0.2, 0], [cx - 0.1, cy + 0.2, 0], buff=0, color=INK, stroke_width=5, tip_length=0.16)
        thumb = a5_img("pantry/a5_box.png", cx + 0.9, cy - 0.45, s=0.0007, opacity=0.6)
        nm = M("-convcolonly", 32).move_to([cx + 1.2, cy - 0.95, 0])
        q = T("?", 64).move_to([cx + 2.3, cy + 0.3, 0])
        parts = [VGroup(pg, ln, pl), arr, Group(thumb, nm), q]
    return frame, parts


class B47A_ThreePredictions(Scene):
    def construct(self):
        head = T("Predict", 40).move_to([-5.2, 3.0, 0])
        self.add(head)
        f1, p1 = a5_cell(0); f2, p2 = a5_cell(1); f3, p3 = a5_cell(2)
        until(self, "Which Godot axis", lead=0.3)
        self.play(Create(f1), run_time=0.4)
        self.play(FadeIn(p1[0]), run_time=0.4)
        self.play(Create(p1[1]), run_time=0.6)
        self.play(FadeIn(p1[2]), run_time=0.3)
        until(self, "What does the bounding", lead=0.45)
        self.play(Create(f2), run_time=0.4)
        self.play(FadeIn(p2[0]), run_time=0.4)
        until(self, "plus Y up off", lead=0.2)
        self.play(FadeIn(p2[1]), run_time=0.3)
        until(self, "What does Godot report", lead=0.3)
        self.play(Create(f3), run_time=0.4)
        self.play(Create(p3[0]), run_time=0.5)
        self.play(FadeIn(p3[1]), run_time=0.3)
        until(self, "never applied", lead=0.25)
        self.play(FadeIn(p3[2]), run_time=0.3)
        done(self)


class B47B_FourthPrediction(Scene):
    def construct(self):
        head = T("Predict", 40).move_to([-5.2, 3.0, 0])
        cells = [a5_cell(i) for i in range(4)]
        self.add(head)
        for f, p in cells[:3]:
            self.add(f, *p)
        f4, p4 = cells[3]
        until(self, "collider named", lead=0.5)
        self.play(Create(f4), run_time=0.4)
        self.play(FadeIn(p4[0]), run_time=0.4)
        until(self, "dash conv col only", lead=0.2)
        self.play(FadeIn(p4[2]), run_time=0.4)
        until(self, "import file", lead=0.6)
        self.play(Create(p4[1]), FadeIn(p4[3]), run_time=0.4)
        done(self)


# ── B56 · our own run: the finished test, then a fresh import ────────────────────────────────────────────────────────────────
A5_MW = 0.2485          # Menlo at size 32: scene units per character (measured)


def a5_mline(text, x_left, y, size=32, color=INK):
    """A Menlo line whose LEFT edge sits at x_left (width = chars * 0.2485 at size 32, measured)."""
    w = len(text) * A5_MW * size / 32.0
    return M(text, size, color).move_to([x_left + w / 2.0, y, 0])


class B56_OurOwnRun(Scene):
    def construct(self):
        # part 1: the finished test's real log, one tick per PASS line (15 PASS, 0 FAIL: logs/verify1-test_checkpoint_post.log)
        tiles, ticks = VGroup(), VGroup()
        for r in range(3):
            for c in range(5):
                x, y = -2.4 + c * 1.2, 1.35 - r * 1.2
                tiles.add(RoundedRectangle(width=0.95, height=0.95, corner_radius=0.14, fill_opacity=0, stroke_color=DIM, stroke_width=5).move_to([x, y, 0]))
                ticks.add(check(x - 0.03, y + 0.04, s=0.2, color=INK, w=8))
        pass_l = T("PASS", 40).move_to([0, 2.75, 0])
        fail_l = M("Failures: 0", 32).move_to([0, -2.55, 0])
        self.add(tiles)
        until(self, "Fifteen of fifteen", lead=0.35)
        self.play(FadeIn(pass_l), LaggedStart(*[Create(t) for t in ticks], lag_ratio=0.12), run_time=1.9)
        self.play(FadeIn(fail_l), run_time=0.3)
        until(self, "Then we checked", lead=0.1)
        self.play(FadeOut(VGroup(tiles, ticks, pass_l, fail_l)), run_time=0.4)
        # part 2: a fresh import of the same file
        x0, yf, s = -4.3, -2.6, 0.003
        box = a5_img("pantry/a5_box.png", x0, yf, s=s, opacity=0.6)
        edges = VGroup(*[Line(a5_P(a, x0, yf, s), a5_P(b, x0, yf, s), color=DIM, stroke_width=4) for a, b in [
            ("box_mm_0", "box_pm_0"), ("box_pm_0", "box_pp_0"), ("box_mm_18", "box_pm_18"), ("box_pm_18", "box_pp_18"),
            ("box_mm_0", "box_mm_18"), ("box_pm_0", "box_pm_18"), ("box_pp_0", "box_pp_18")]])
        fresh = T("fresh import", 40).move_to([x0, 2.75, 0])
        until(self, "A fresh import", lead=0.5)
        self.play(FadeIn(box), Create(edges), FadeIn(fresh), run_time=0.5)
        l1 = a5_mline("nodes/use_name_suffixes=true", -2.3, 1.5)
        l2 = a5_mline("nodes/use_node_type_suffixes=true", -2.3, 0.85)
        until(self, "both suffix settings", lead=0.6)
        self.play(FadeIn(l1), run_time=0.3)
        self.play(FadeIn(l2), run_time=0.3)
        d1 = Dot([-4.75, -0.5, 0], radius=0.1, color=TERRA); ld1 = Line([-4.63, -0.5, 0], [-2.45, -0.5, 0], color=INK, stroke_width=4)
        t1 = T("StaticBody3D", 36).move_to([-0.65, -0.5, 0])
        d2 = Dot([-4.75, -1.4, 0], radius=0.1, color=TERRA); ld2 = Line([-4.63, -1.4, 0], [-2.45, -1.4, 0], color=INK, stroke_width=4)
        t2 = T("ConvexPolygonShape3D", 36).move_to([0.4, -1.4, 0])
        until(self, "builds a static", lead=0.35)
        self.play(FadeIn(d1), Create(ld1), FadeIn(t1), run_time=0.4)
        until(self, "convex shape", lead=0.55)
        self.play(FadeIn(d2), Create(ld2), FadeIn(t2), run_time=0.4)
        done(self)


# ── B57 · only that setting off: the collider comes back as a visible box ───────────────────────────────────────────────────────
def a5_toggle(on, x, y):
    """A switch: outlined pill, knob on the right when ON, on the left when OFF (the knob is a grey dot with an ink outline)."""
    pill = RoundedRectangle(width=1.5, height=0.8, corner_radius=0.4, fill_opacity=0, stroke_color=INK, stroke_width=6).move_to([x, y, 0])
    knob = Circle(radius=0.27, fill_color=BAR2, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([x + (0.37 if on else -0.37), y, 0])
    return pill, knob


class B57_SuffixAlone(Scene):
    def construct(self):
        x0, yf, s = 3.9, -2.55, 0.0026
        pill, knob = a5_toggle(True, -4.9, 1.9)
        name = a5_mline("use_node_type_suffixes", -3.75, 1.9)
        ghost = a5_img("pantry/a5_box.png", x0, yf, s=s, opacity=0.6)
        edges = VGroup(*[Line(a5_P(a, x0, yf, s), a5_P(b, x0, yf, s), color=DIM, stroke_width=4) for a, b in [
            ("box_mm_0", "box_pm_0"), ("box_pm_0", "box_pp_0"), ("box_mm_18", "box_pm_18"), ("box_pm_18", "box_pp_18"),
            ("box_mm_0", "box_mm_18"), ("box_pm_0", "box_pm_18"), ("box_pp_0", "box_pp_18")]])
        solid = a5_img("pantry/a5_boxopaque.png", x0, yf, s=s)
        self.add(pill, knob, name, ghost, edges)
        until(self, "Turn off", lead=0.1)
        self.play(knob.animate.move_to([-4.9 - 0.37, 1.9, 0]), run_time=0.45)
        until(self, "reimport", lead=0.2)
        loop = CurvedArrow([-1.6, 0.85, 0], [1.9, 0.2, 0], angle=-TAU / 6, color=INK, stroke_width=5, tip_length=0.2)
        self.play(Create(loop), run_time=0.5)
        until(self, "visible box", lead=0.9)
        self.play(FadeOut(Group(ghost, edges)), FadeIn(solid), run_time=0.5)
        vb = T("visible box", 38).move_to([x0, 2.55, 0])
        self.play(FadeIn(vb), run_time=0.3)
        # no collision: a ring with a bar through it, on the box's lit face
        ring = Circle(radius=0.62, stroke_color=INK, stroke_width=9).move_to([x0 - 0.45, -0.2, 0])
        bar = Line([x0 - 0.45 - 0.44, -0.2 + 0.44, 0], [x0 - 0.45 + 0.44, -0.2 - 0.44, 0], color=INK, stroke_width=9)
        nc = T("no collision", 38).move_to([0.55, -0.3, 0])
        until(self, "no collision", lead=0.05)
        self.play(Create(ring), Create(bar), FadeIn(nc), run_time=0.6)
        # the suffix alone was enough; the extra physics block was redundant
        keep = RoundedRectangle(width=8.2, height=1.3, corner_radius=0.25, fill_opacity=0, stroke_color=INK, stroke_width=6).move_to([-2.0, 1.9, 0])
        until(self, "The suffix setting alone", lead=0.1)
        self.play(Create(keep), run_time=0.5)
        sub = a5_mline("_subresources", -3.75, -1.9)
        xa = Line([-5.25, -1.65, 0], [-4.55, -2.15, 0], color=DIM, stroke_width=7)
        xb = Line([-5.25, -2.15, 0], [-4.55, -1.65, 0], color=DIM, stroke_width=7)
        until(self, "The extra physics", lead=0.1)
        self.play(FadeIn(sub), run_time=0.3)
        until(self, "redundant", lead=0.3)
        self.play(Create(xa), Create(xb), run_time=0.4)
        done(self)


# ── B58 · the floor check that was not a floor check ───────────────────────────────────────────────────────────────────────────
B58_X0, B58_YF, B58_S = -3.4, -2.75, 0.0026      # act 6 (B59+) continues this exact layout: pole foot on the floor at (B58_X0, B58_YF)


class B58_RayThroughNothing(Scene):
    def construct(self):
        x0, yf, s = B58_X0, B58_YF, B58_S
        lift = (A5_ORG[1] - A5_PT["lift158"][1]) * s            # the 15.8 cm the post floated, in scene units, from the real camera
        floor = a5_floor(x0, yf, s=s)
        fl = T("floor", 36).move_to([x0 - 1.85, yf + 0.65, 0])
        post = a5_img("pantry/a5_post.png", x0, yf + lift, s=s)
        self.add(floor, fl)
        until(self, "The agent had first", lead=0.3)
        self.play(FadeIn(post), run_time=0.5)
        # the gap: a dimension arrow on extension lines, to the right of the base
        pb = a5_P("base_pp_0", x0, yf + lift, s)
        xa = pb[0] + 0.85
        e1 = Line([pb[0] + 0.12, pb[1], 0], [xa + 0.2, pb[1], 0], color=DIM, stroke_width=3)
        e2 = Line([pb[0] + 0.12, pb[1] - lift, 0], [xa + 0.2, pb[1] - lift, 0], color=DIM, stroke_width=3)
        gap = dim_arrow([xa, pb[1] - lift, 0], [xa, pb[1], 0], tip=0.1)
        gl = T("16 cm", 36).move_to([xa + 1.0, pb[1] - lift / 2, 0])
        until(self, "sixteen centimetres", lead=0.35)
        self.play(Create(e1), Create(e2), Create(gap), FadeIn(gl), run_time=0.5)
        # the first test's ray: from 2 m above the post's base, straight down the pole's axis, through the missing collider, to the floor
        top = a5_P("ray_start158", x0, yf, s)
        bot = np.array([x0, yf, 0.0])
        ray = Arrow(top, bot, buff=0, color=INK, stroke_width=6, tip_length=0.22)
        hit = Dot(bot, radius=0.13, color=TERRA)
        ray_l = T("ray", 36).move_to([x0 + 0.75, top[1] - 0.15, 0])
        until(self, "Its first test", lead=0.0)
        self.play(Create(ray), FadeIn(ray_l), run_time=0.85)
        self.play(FadeIn(hit), run_time=0.2)
        nc = T("no collider", 36).move_to([x0 + 2.1, yf + 2.3, 0])
        ncd = Dot([x0 + 0.1, yf + 2.3, 0], radius=0.1, color=TERRA)
        ncl = Line([x0 + 0.22, yf + 2.3, 0], [x0 + 1.0, yf + 2.3, 0], color=INK, stroke_width=4)
        until(self, "straight through", lead=0.1)
        self.play(FadeIn(ncd), Create(ncl), FadeIn(nc), run_time=0.4)
        # what the first test printed (verbatim pieces of the real log line), joined to the dot and to the base by a leader each
        hit_l = a5_mline("ray hit at y=-4.0000", 1.2, -1.3)
        hit_ld = Line([x0 + 0.17, yf + 0.03, 0], [1.1, -1.3, 0], color=INK, stroke_width=4)
        until(self, "found the floor", lead=0.45)
        self.play(Create(hit_ld), FadeIn(hit_l), run_time=0.4)
        base_l2 = a5_mline("post base y=-3.8419", 1.2, -0.45)
        base_ld = Line([pb[0] + 0.05, pb[1] + 0.05, 0], [1.1, -0.45, 0], color=INK, stroke_width=4)
        self.play(Create(base_ld), FadeIn(base_l2), run_time=0.4)
        # the agent moved the post down onto the floor
        until(self, "so the agent moved", lead=0.2)
        new_l = a5_mline("post base y=-4.0", 1.2, -0.45)
        self.play(post.animate.shift(DOWN * lift), FadeOut(VGroup(e1, e2, gap, gl, base_ld)), run_time=0.7)
        base_ld2 = Line([pb[0] + 0.05, pb[1] - lift + 0.05, 0], [1.1, -0.45, 0], color=INK, stroke_width=4)
        self.play(FadeOut(base_l2), FadeIn(new_l), Create(base_ld2), run_time=0.3)
        done(self)


# ── B52 / B53 · the session on a timeline (numbers from the first run's own result events; transcripts/run1-claude.jsonl) ───────────────
A5_TL_X0, A5_TL_Y, A5_TL_U = -6.0, -2.45, 0.2927        # timeline: left edge, bar centre line, scene units per minute (41 min span)
A5_P1_MIN, A5_GAP_MIN, A5_P2_MIN = 21.2, 7.8, 11.96      # 1,271,707 ms | hung debug process | 717,737 ms


def a5_tl_x(minutes):
    return A5_TL_X0 + minutes * A5_TL_U


def a5_bar(m0, m1, y=A5_TL_Y, fill=BAR2):
    w = (m1 - m0) * A5_TL_U
    return Rectangle(width=w, height=0.55, fill_color=fill, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([a5_tl_x(m0) + w / 2.0, y, 0])


def a5_refusal_dots():
    """Nine refusals, drawn above the first bar (the nine 'requires approval' results in phase 1; see SESSION-act5.md)."""
    return VGroup(*[Dot([-5.35 + k * 0.62, A5_TL_Y + 0.8, 0], radius=0.12, color=TERRA) for k in range(9)])


class B52_TurnLimit(Scene):
    def construct(self):
        x_l = -5.45
        f = a5_mline("debug_options.gd", x_l, 2.85, color=DIM)
        n6, n8, n14 = a5_mline("6", -6.05, 2.2, color=DIM), a5_mline("8", -6.05, 1.55, color=DIM), a5_mline("14", -6.2, 0.9, color=DIM)
        l6 = a5_mline("var importer := ResourceImporterScene.new()", x_l, 2.2)
        l8 = a5_mline('importer.get_import_options("", opts, 0)', x_l, 1.55)
        l14 = a5_mline("quit(0)", x_l, 0.9, color=DIM)
        e1 = a5_mline("SCRIPT ERROR: Invalid call.", x_l, 0.05)
        e2 = a5_mline("Nonexistent function 'get_import_options'", x_l, -0.55)
        e3 = a5_mline("in base 'Nil'.", x_l, -1.15)
        fail = Dot([5.1, 1.55, 0], radius=0.11, color=TERRA)
        nev = T("never reached", 34).move_to([-2.35, 0.9, 0])
        run = T("kept running", 34).move_to([4.65, -1.45, 0])
        until(self, "It wrote", lead=0.0)
        self.play(FadeIn(f), FadeIn(VGroup(n6, l6)), run_time=0.4)
        self.play(FadeIn(VGroup(n8, l8)), run_time=0.3)
        until(self, "a method that", lead=0.45)
        self.play(FadeIn(fail), FadeIn(e1), run_time=0.3)
        self.play(FadeIn(e2), run_time=0.25)
        self.play(FadeIn(e3), run_time=0.25)
        until(self, "The script never", lead=0.3)
        self.play(FadeIn(VGroup(n14, l14)), FadeIn(nev), run_time=0.4)
        until(self, "kept running", lead=0.3)
        ring = Circle(radius=0.4, stroke_color=INK, stroke_width=6).move_to([5.5, -0.3, 0])
        arc = Arc(radius=0.4, start_angle=PI / 2, angle=-PI * 0.9, arc_center=[5.5, -0.3, 0], stroke_color=INK, stroke_width=12)
        self.play(Create(ring), Create(arc), FadeIn(run), run_time=0.4)
        bar1 = a5_bar(0, A5_P1_MIN)
        lab1 = T("61 turns · 21 min", 40).move_to([a5_tl_x(A5_P1_MIN / 2.0), A5_TL_Y - 0.65, 0])
        until(self, "At sixty-one", lead=0.0)
        self.play(GrowFromEdge(bar1, LEFT), FadeIn(lab1), run_time=0.9)
        lim = Line([a5_tl_x(A5_P1_MIN), A5_TL_Y - 0.5, 0], [a5_tl_x(A5_P1_MIN), A5_TL_Y + 0.5, 0], color=INK, stroke_width=8)
        limt = T("turn limit", 34).move_to([a5_tl_x(A5_P1_MIN) + 1.35, A5_TL_Y, 0])
        until(self, "turn limit", lead=0.45)
        self.play(Create(lim), FadeIn(limt), run_time=0.4)
        dots = a5_refusal_dots()
        ref = T("9 refused", 38).move_to([1.3, A5_TL_Y + 0.8, 0])
        until(self, "Nine commands", lead=0.15)
        self.play(LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.15), run_time=1.1)
        self.play(FadeIn(ref), run_time=0.3)
        done(self)


class B53_Resumed(Scene):
    def construct(self):
        bar1 = a5_bar(0, A5_P1_MIN)
        lab1 = T("61 turns · 21 min", 40).move_to([a5_tl_x(A5_P1_MIN / 2.0), A5_TL_Y - 0.65, 0])
        lim = Line([a5_tl_x(A5_P1_MIN), A5_TL_Y - 0.5, 0], [a5_tl_x(A5_P1_MIN), A5_TL_Y + 0.5, 0], color=INK, stroke_width=8)
        dots = a5_refusal_dots()
        ref = T("9 refused", 38).move_to([1.3, A5_TL_Y + 0.8, 0])
        self.add(bar1, lab1, lim, dots, ref)
        # the gap: the hung debug process, until we stopped it
        g0, g1 = a5_tl_x(A5_P1_MIN), a5_tl_x(A5_P1_MIN + A5_GAP_MIN)
        gap = Rectangle(width=g1 - g0, height=0.55, fill_opacity=0, stroke_color=DIM, stroke_width=5).move_to([(g0 + g1) / 2.0, A5_TL_Y, 0])
        gap_l = T("hung", 36).move_to([(g0 + g1) / 2.0, A5_TL_Y - 0.65, 0])
        until(self, "When we stopped", lead=0.3)
        self.play(Create(gap), FadeIn(gap_l), run_time=0.7)
        # the completion notice that woke the agent (two real rows from the record)
        nt = a5_mline("task_notification", -5.0, 2.7, color=DIM)
        n1 = a5_mline('Background command "Print available', -5.0, 2.0)
        n2 = a5_mline('import options" completed (exit code 0)', -5.0, 1.4)
        arrow = Arrow([g1, A5_TL_Y + 0.4, 0], [g1, 0.95, 0], buff=0, color=INK, stroke_width=5, tip_length=0.2)
        until(self, "background task", lead=0.5)
        self.play(FadeIn(nt), FadeIn(n1), run_time=0.35)
        self.play(FadeIn(n2), Create(arrow), run_time=0.35)
        bar2 = a5_bar(A5_P1_MIN + A5_GAP_MIN, A5_P1_MIN + A5_GAP_MIN + A5_P2_MIN)
        lab2 = T("24 turns · 12 min", 40).move_to([a5_tl_x(A5_P1_MIN + A5_GAP_MIN + A5_P2_MIN / 2.0), A5_TL_Y - 0.65, 0])
        until(self, "woke the agent", lead=0.3)
        self.play(GrowFromEdge(bar2, LEFT), run_time=0.9)
        until(self, "twenty-four more", lead=0.45)
        self.play(FadeIn(lab2), run_time=0.3)
        done(self)


# ── B55 · the context is compacted; the full path is tried seven times ─────────────────────────────────────────────────────────
class B55_Compacted(Scene):
    def construct(self):
        # gauge: 172390 tokens -> 10266 tokens (compact_boundary event, transcripts/run1-claude.jsonl line 219)
        gx, gy0, gh = -5.45, -1.6, 3.2
        gauge = Rectangle(width=1.0, height=gh, fill_opacity=0, stroke_color=INK, stroke_width=5).move_to([gx, gy0 + gh / 2.0, 0])
        fill = Rectangle(width=1.0, height=gh, fill_color=BAR2, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([gx, gy0 + gh / 2.0, 0])
        small = Rectangle(width=1.0, height=gh * 10266 / 172390.0, fill_color=BAR2, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to(
            [gx, gy0 + gh * 10266 / 172390.0 / 2.0, 0])
        ctx = T("context", 38).move_to([gx, gy0 + gh + 1.0, 0])
        n_pre = a5_mline("172390", gx - 0.75, gy0 + gh + 0.45)
        n_post = a5_mline("10266", gx - 0.62, gy0 - 0.45)
        self.add(gauge, ctx)
        self.play(FadeIn(fill), FadeIn(n_pre), run_time=0.5)
        until(self, "Then its context", lead=0.0)
        self.wait(0.3)
        self.play(Transform(fill, small), FadeIn(n_post), run_time=0.9)
        # what it forgot: the plain command that had worked every time before
        x_l = -3.6
        ok = a5_mline("godot --headless … --import", x_l, 2.45, color=DIM)
        okc = check(x_l - 0.38, 2.43, s=0.17, color=INK, w=7)
        until(self, "forgot that", lead=0.4)
        self.play(FadeIn(ok), Create(okc), run_time=0.5)
        # then the full application path, seven times, each one refused
        rows = VGroup(*[a5_mline("/Applications/Godot.app/…/Godot", x_l, 1.55 - k * 0.5) for k in range(7)])
        xs = VGroup(*[VGroup(Line([4.55, 1.55 - k * 0.5 + 0.17, 0], [4.9, 1.55 - k * 0.5 - 0.17, 0], color=INK, stroke_width=7),
                             Line([4.55, 1.55 - k * 0.5 - 0.17, 0], [4.9, 1.55 - k * 0.5 + 0.17, 0], color=INK, stroke_width=7)) for k in range(7)])
        until(self, "full application path", lead=0.9)
        for k in range(7):
            self.play(FadeIn(rows[k]), Create(xs[k]), run_time=0.3)
        ask = T("Please approve the Godot command …", 38).move_to([0.5, -2.15, 0])
        until(self, "asking a human", lead=0.2)
        self.play(FadeIn(ask), run_time=0.4)
        test = a5_mline("test_checkpoint_post.gd", -3.0, -2.95, color=DIM)
        nr = T("never ran", 36).move_to([4.5, -2.95, 0])
        until(self, "never ran", lead=0.35)
        self.play(FadeIn(test), FadeIn(nr), run_time=0.4)
        done(self)
