"""ACT V (second half) · Building the Post, Then Checking the Builder  (B59-B71B)

One cast for the act: the CHECKPOINT POST drawn in Godot's side view (x across, Y up, metres), the pennant at its top right,
the collider outline around it (first the 0.6 m box, then the tapered hull), and Godot's floor line at y = -4.0.
The real Blender renders appear where the picture IS the thing: B59 continues act 5's layout (the real render on its ghost floor tile, marks placed through the render's camera), B70 and B71 use crops of post_visual.png / post_collider_only.png.
Every number on screen is a real log line, a real transcript line, or arithmetic reproduced by evidence/act6/derive_geometry.py.
"""
# ───────────────────────── act-6 helpers ─────────────────────────
A6_PENN_X0, A6_PENN_X1, A6_PENN_Y0, A6_PENN_Y1 = 0.08, 0.48, 1.55, 1.80      # the pennant, metres (Godot axes: x across, y up)


def a6_P(U, ox, oy):
    """Metres (x across, y up, y = 0 at the post's base underside) -> scene point."""
    return lambda x, y: np.array([ox + x * U, oy + y * U, 0.0])


def a6_rect(P, x0, y0, x1, y1, fill=None, stroke=INK, sw=4, fo=1.0):
    """Axis-aligned rectangle between two metre corners (explicit corners, no get_left)."""
    pts = [P(x0, y0), P(x1, y0), P(x1, y1), P(x0, y1)]
    return Polygon(*pts, fill_color=fill if fill else STAGE, fill_opacity=fo if fill else 0, stroke_color=stroke, stroke_width=sw)


def a6_post(P, ghost=False, sw=4, metal=BAR3):
    """The post in Godot's side view: base slab, pole, pennant. ghost=True redraws it faded (an excluded body)."""
    if ghost:
        c = GHOST
        return VGroup(a6_rect(P, -0.3, 0.0, 0.3, 0.1, None, DIM, 3), a6_rect(P, -0.08, 0.1, 0.08, 1.8, None, DIM, 3),
                      a6_rect(P, A6_PENN_X0, A6_PENN_Y0, A6_PENN_X1, A6_PENN_Y1, None, DIM, 3))
    return VGroup(a6_rect(P, -0.3, 0.0, 0.3, 0.1, metal, INK, sw), a6_rect(P, -0.08, 0.1, 0.08, 1.8, metal, INK, sw),
                  a6_rect(P, A6_PENN_X0, A6_PENN_Y0, A6_PENN_X1, A6_PENN_Y1, BOX_L, INK, sw))


def a6_hull_pts():
    """The tapered hull's silhouette in the side view (6 corners): base slab +-0.30 up to y = 0.1, straight slope to +-0.08 at y = 1.8."""
    return [(-0.3, 0.0), (0.3, 0.0), (0.3, 0.1), (0.08, 1.8), (-0.08, 1.8), (-0.3, 0.1)]


def a6_hw(y):
    """Hull half-width at height y (metres): reproduces evidence/act6/derive_geometry.py."""
    return 0.30 if y <= 0.1 else 0.30 - 0.22 * (y - 0.1) / 1.7


def a6_mono(s, xl, y, size=32, color=INK):
    """Menlo line whose LEFT edge sits at xl (Menlo is 0.25 units per character at size 32)."""
    return M(s, size, color).move_to([xl + 0.25 * (size / 32.0) * len(s) / 2.0, y, 0])


# ── the real render (pantry/a6_post_run1.png, the act-V post, same camera as post_visual.png): marks are placed through the camera model ──
A6_CAM_LOC, A6_CAM_TGT, A6_FOCAL_PX = np.array([3.9, -4.6, 2.0]), np.array([0.12, 0.0, 0.9]), 42.0 / 36.0 * 4800     # evidence/act6/project_points.py
A6_CROP_W, A6_CROP_H, A6_CROP_ORG, A6_RENDER_ORG = 1457, 1943, (735.5, 1723.2), (1582, 402)                          # crop px of the pole's foot
A6_FLOOR_PX = [(-480.9, 1761.0), (860.9, 2201.3), (1903.2, 1687.0), (653.4, 1410.4)]                                 # the floor tile's corners (act 5's anchors)


def a6_proj(P):
    """World point (Blender x, y, z up) -> pixel in the crop."""
    f = A6_CAM_TGT - A6_CAM_LOC
    f = f / np.linalg.norm(f)
    r = np.cross(f, [0, 0, 1])
    r = r / np.linalg.norm(r)
    u = np.cross(r, f)
    v = np.array(P, dtype=float) - A6_CAM_LOC
    return (2400.0 + A6_FOCAL_PX * (v @ r) / (v @ f) - A6_RENDER_ORG[0], 1350.0 - A6_FOCAL_PX * (v @ u) / (v @ f) - A6_RENDER_ORG[1])


def a6_pt(px, py, x0, yf, s):
    """Crop pixel -> scene point when the pole's foot is at scene (x0, yf) and one crop pixel is s scene units."""
    return np.array([x0 + (px - A6_CROP_ORG[0]) * s, yf + (A6_CROP_ORG[1] - py) * s, 0.0])


def a6_wp(P, x0, yf, s):
    px, py = a6_proj(P)
    return a6_pt(px, py, x0, yf, s)


def a6_img(path, x0, yf, s, opacity=1.0):
    im = ImageMobject(path)
    im.set_height(A6_CROP_H * s)
    im.move_to([x0 + (A6_CROP_W / 2 - A6_CROP_ORG[0]) * s, yf + (A6_CROP_ORG[1] - A6_CROP_H / 2) * s, 0])
    if opacity < 1.0:
        im.set_opacity(opacity)
    return im


def a6_tile(x0, yf, s, k=0.72):
    """The ghost floor tile under the post (the same tile as the preceding beats)."""
    org = a6_pt(A6_CROP_ORG[0], A6_CROP_ORG[1], x0, yf, s)
    pts = [org + (a6_pt(px, py, x0, yf, s) - org) * k for px, py in A6_FLOOR_PX]
    return Polygon(*pts, fill_color=GHOST, fill_opacity=1, stroke_width=0)


def a6_grid(P, only_x_below=None, hull=False):
    """The 41 x 26 sample grid of the physics query (1 cm pitch). Returns (all dots, inside dots, outside dots, n_inside).
    Inside = strictly inside the collider surface, the rule that reproduces the logged 572 (box) and 55 (hull)."""
    allg, ins, outs = [], [], []
    n = 0
    for i in range(41):
        x = round(0.08 + 0.01 * i, 2)
        for j in range(26):
            y = round(1.55 + 0.01 * j, 2)
            inside = (x < a6_hw(y) - 1e-9) if hull else (x < only_x_below - 1e-9)
            d = Dot(P(x, y), radius=0.03, color=BAR2)
            allg.append(d)
            (ins if inside else outs).append(d)
            n += 1 if inside else 0
    return VGroup(*allg), VGroup(*ins), VGroup(*outs), n


# ── B59 · the finished test's ray stops on the post; ours ignores the post and finds the floor (the real render, as in B58) ──────────
class B59_TwoRays(Scene):
    def construct(self):
        s, yf = 0.0013, -2.1
        xl, xr = -3.2, 2.9
        tile_l, tile_r = a6_tile(xl, yf, s), a6_tile(xr, yf, s)
        post_l = a6_img("pantry/a6_post_run1.png", xl, yf, s)
        post_r = a6_img("pantry/a6_post_run1.png", xr, yf, s)
        cap_l = T("the finished test", 36).move_to([xl, 3.05, 0])
        cap_r = T("our check", 36).move_to([xr, 3.05, 0])
        fl = T("floor", 34).move_to([xl - 2.15, yf - 0.02, 0])
        self.add(tile_l, tile_r, post_l, post_r, cap_l, cap_r, fl)
        top = a6_wp((0, 0, 1.8), xl, yf, s)
        start = a6_wp((0, 0, 3.8), xl, yf, s)               # 2 m above the post's top
        until(self, "starts two metres", lead=0.1)
        sdot = Dot(start, radius=0.1, color=INK)
        dm = dim_arrow([xl - 0.75, top[1] + 0.03, 0], [xl - 0.75, start[1], 0])
        dml = T("2 m", 36).move_to([xl - 1.4, (top[1] + start[1]) / 2, 0])
        self.play(FadeIn(sdot), Create(dm), FadeIn(dml), run_time=0.5)
        until(self, "stops on the post's own collider", lead=0.5)
        ray1 = Arrow(start + np.array([0, -0.12, 0]), top + np.array([0, 0.02, 0]), buff=0, color=INK, stroke_width=6, tip_length=0.22)
        self.play(GrowArrow(ray1), run_time=0.7)
        hit = Dot(top, radius=0.13, color=TERRA)
        hl = T("hit, y = -2.2", 34).move_to([xl + 1.95, top[1] + 0.05, 0])
        self.play(FadeIn(hit), FadeIn(hl), run_time=0.3)
        until(self, "not that it stands on anything", lead=0.0)
        nf = T("floor never reached", 34).move_to([xl, yf - 0.85, 0])
        self.play(FadeIn(nf), run_time=0.4)
        until(self, "Our ray", lead=0.2)
        self.play(post_r.animate.set_opacity(0.3), run_time=0.5)
        s2 = a6_wp((0, 0, 0.5), xr, yf, s)
        foot = a6_wp((0, 0, 0), xr, yf, s)
        sdot2 = Dot(s2, radius=0.1, color=INK)
        self.play(FadeIn(sdot2), run_time=0.25)
        until(self, "found the floor", lead=0.9)
        ray2 = Arrow(s2 + np.array([0, -0.1, 0]), foot + np.array([0, 0.03, 0]), buff=0, color=INK, stroke_width=6, tip_length=0.2)
        self.play(GrowArrow(ray2), run_time=0.6)
        fdot = Dot(foot, radius=0.13, color=TERRA)
        fy = T("y = -4.0", 34).move_to([xr, yf - 0.85, 0])
        self.play(FadeIn(fdot), FadeIn(fy), run_time=0.35)
        until(self, "with a gap of zero", lead=0.1)
        gp = T("gap 0.0 m", 36).move_to([xr + 2.1, yf + 0.55, 0])
        self.play(FadeIn(gp), run_time=0.4)
        done(self)


# ── B60 · the weakened check, in the agent's own two versions ───────────────────────────────────────────────────────
class B60_Weakened(Scene):
    def construct(self):
        XL = -5.0
        tag1 = T("first run", 36).move_to([XL + 0.9, 2.78, 0])
        f1 = a6_mono("FAIL  no unexpected materials", XL, 2.2)
        f2 = a6_mono('[found ["PostMetal", "FlagCloth", ""]]', XL, 1.7)
        tag2 = T("the edit", 36).move_to([XL + 0.78, 0.72, 0])
        tag3 = T("later run", 36).move_to([XL + 0.95, -1.12, 0])
        self.add(tag1, f1, f2)
        until(self, "unnamed default material", lead=0.3)
        # the unnamed entry: the empty name in the found list (index of the "" inside the line)
        s = '[found ["PostMetal", "FlagCloth", ""]]'
        k = s.index('""')
        dx = XL + 0.25 * (k + 1)
        dot = Dot([dx, 1.22, 0], radius=0.11, color=TERRA)
        self.play(FadeIn(dot), run_time=0.3)
        until(self, "later version skips", lead=0.0)
        old = a6_mono("- if mat:", XL, 0.2, color=DIM)
        new = a6_mono('+ if mat and mat.resource_name != "":', XL, -0.32)
        self.play(FadeIn(tag2), FadeIn(old), run_time=0.3)
        self.play(FadeIn(new), run_time=0.5)
        until(self, "unnamed materials", lead=0.0)
        p1 = a6_mono("PASS  no unexpected named materials", XL, -1.72)
        p2 = a6_mono('["PostMetal", "FlagCloth"]', XL + 0.5, -2.22)
        ck = check(XL - 0.35, -1.72, 0.17, INK, 7)
        self.play(FadeIn(tag3), FadeIn(p1), FadeIn(p2), Create(ck), run_time=0.5)
        until(self, "Don't weaken", lead=0.1)
        mk = Dot([XL - 0.4, -0.32, 0], radius=0.11, color=TERRA)
        self.play(FadeIn(mk), run_time=0.3)
        done(self)


# ── B61 · the box ran out to 0.3 m; the pennant runs 0.08 to 0.48 ───────────────────────────────────────────────────
class B61_BoxVsPennant(Scene):
    def construct(self):
        U = 10.0
        P = lambda x, y: np.array([-2.0 + U * x, 2.4 - U * (1.8 - y), 0.0])
        penn = a6_rect(P, 0.08, 1.55, 0.48, 1.80, BOX_R, INK, 5)
        pole = a6_rect(P, -0.08, 1.49, 0.08, 1.8, BAR1, INK, 5)
        lab_p = T("pennant", 36).move_to([4.15, 1.15, 0])
        lab_pole = T("pole", 36).move_to([-3.9, 0.9, 0])
        self.add(pole, penn, lab_p, lab_pole)
        until(self, "inside the collider", lead=1.5)
        top = Line(P(-0.3, 1.8), P(0.3, 1.8), color=INK, stroke_width=6)
        lft = Line(P(-0.3, 1.8), P(-0.3, 1.47), color=INK, stroke_width=6)
        rgt = Line(P(0.3, 1.8), P(0.3, 1.47), color=INK, stroke_width=6)
        lab_b = T("collider box", 36).move_to([-3.3, 2.92, 0])
        self.play(Create(top), Create(lft), Create(rgt), FadeIn(lab_b), run_time=0.9)
        over = a6_rect(P, 0.08, 1.55, 0.30, 1.80, "#A38C66", INK, 5)
        self.play(FadeIn(over), run_time=0.4)
        until(self, "point three metres", lead=0.6)
        d1 = dim_arrow([-2.0, -1.3, 0], [1.0, -1.3, 0])
        e1 = Line(P(0.3, 1.47), [1.0, -1.3, 0], color=DIM, stroke_width=3)
        l1 = T("box edge  0.3 m", 36).move_to([-0.5, -1.78, 0])
        self.play(Create(e1), Create(d1), FadeIn(l1), run_time=0.6)
        until(self, "pennant runs from", lead=0.1)
        d2 = dim_arrow([-1.2, -2.45, 0], [2.8, -2.45, 0])
        l2 = T("pennant  0.08 to 0.48 m", 36).move_to([0.8, -2.93, 0])
        self.play(Create(d2), FadeIn(l2), run_time=0.7)
        done(self)


# ── B62 · 1,066 sample points on a 1 cm grid; 572 inside the box; the agent's check passed anyway ──────────────────────
class B62_Sampled(Scene):
    def construct(self):
        U = 14.0
        P = lambda x, y: np.array([-4.4 + U * (x - 0.08), 1.9 - U * (1.8 - y), 0.0])
        outline = a6_rect(P, 0.08, 1.55, 0.48, 1.80, None, DIM, 4)
        pole = a6_rect(P, -0.0557, 1.53, 0.08, 1.8, BAR1, DIM, 4)
        face = Line(P(0.30, 1.843), P(0.30, 1.53), color=INK, stroke_width=6)
        fl = T("box face 0.3 m", 34).move_to([-1.32, 3.02, 0])
        cap = T("an illustration of the sampling; counts are from the run", 32).move_to([0.0, -3.05, 0])
        allg, ins, outs, n_in = a6_grid(P, only_x_below=0.30)
        self.add(outline, pole, face, fl, cap)
        until(self, "one centimetre grid", lead=1.4)
        gl = T("1 cm grid", 34).move_to([-5.2, 2.55, 0])
        self.play(FadeIn(allg), FadeIn(gl), run_time=0.7)
        until(self, "asked the physics server", lead=0.1)
        self.play(ins.animate.set_color(INK), run_time=0.5)
        until(self, "Five hundred seventy-two", lead=0.2)
        n572 = T("572", 84).move_to([4.1, 1.15, 0])
        self.play(FadeIn(n572), run_time=0.4)
        until(self, "of one thousand sixty-six", lead=0.2)
        n1066 = T("of 1,066 points", 40).move_to([4.1, 0.3, 0])
        lg = Dot([2.35, -0.5, 0], radius=0.1, color=BAR1)
        lgl = T("inside the collider", 34).move_to([4.5, -0.5, 0])
        self.play(FadeIn(n1066), FadeIn(lg), FadeIn(lgl), run_time=0.4)
        until(self, "The agent's check", lead=0.2)
        line1 = a6_mono("PASS  collision X_max ≤ 0.35 … [got 0.300]", -5.0, -2.45)
        self.play(FadeIn(line1), run_time=0.5)
        until(self, "passed anyway", lead=0.1)
        ck = check(-5.4, -2.45, 0.17, INK, 7)
        self.play(Create(ck), run_time=0.4)
        done(self)


# ── B63 · two constants typed into the test, not read from the scenes ───────────────────────────────────────────────
class B63_Constants(Scene):
    def construct(self):
        XL = -5.9
        r1 = a6_mono("PLAYER_CAP_H  := 2.10", XL, 0.7)
        r2 = a6_mono("POST_WORLD    := Vector3(-6.5, -4.0, 3.9334)", XL, -0.4)
        fn = a6_mono("test_checkpoint_post.gd", -4.9, -1.75, color=DIM)
        b1 = RoundedRectangle(width=3.5, height=0.85, corner_radius=0.2, fill_opacity=0, stroke_color=DIM, stroke_width=4).move_to([-3.3, 2.75, 0])
        t1 = a6_mono("player.tscn", -3.3 - 0.25 * 11 / 2, 2.75)
        b2 = RoundedRectangle(width=3.0, height=0.85, corner_radius=0.2, fill_opacity=0, stroke_color=DIM, stroke_width=4).move_to([3.0, -2.75, 0])
        t2 = a6_mono("game.tscn", 3.0 - 0.25 * 9 / 2, -2.75)
        self.add(fn, b1, t1, b2, t2)
        until(self, "capsule height", lead=0.3)
        self.play(AddTextLetterByLetter(r1, run_time=0.9), run_time=0.9)
        until(self, "post's position", lead=0.3)
        self.play(AddTextLetterByLetter(r2, run_time=1.3), run_time=1.3)
        until(self, "not read from the scenes", lead=0.1)
        a1 = DashedLine([-3.3, 2.3, 0], [-3.3, 1.85, 0], color=DIM, stroke_width=5)
        a2 = DashedLine([3.0, -2.3, 0], [3.0, -1.6, 0], color=DIM, stroke_width=5)
        x1 = VGroup(Line([-3.5, 1.68, 0], [-3.1, 1.32, 0], color=INK, stroke_width=7), Line([-3.5, 1.32, 0], [-3.1, 1.68, 0], color=INK, stroke_width=7))
        x2 = VGroup(Line([2.8, -1.18, 0], [3.2, -1.52, 0], color=INK, stroke_width=7), Line([2.8, -1.52, 0], [3.2, -1.18, 0], color=INK, stroke_width=7))
        self.play(Create(a1), Create(a2), run_time=0.5)
        self.play(Create(x1), Create(x2), run_time=0.3)
        done(self)


# ───────────────────────── Codex beats: a real Codex still, pushed into ─────────────────────────
def a6_cam(st, g, zt, pb):
    """Animation that moves Group g so base-point pb sits at the frame centre at zoom zt. st = {"z":…, "t":…} is the group's current state."""
    r = zt / st["z"]
    t_new = -zt * np.array(pb, dtype=float)
    d = t_new - r * st["t"]
    st["z"], st["t"] = zt, t_new
    return g.animate.scale(r, about_point=ORIGIN).shift(d)


def a6_cur(st, pb):
    """Where base-point pb is on screen under the group's current camera state."""
    return st["z"] * np.array(pb, dtype=float) + st["t"]


# ── B64 · the revision prompt, typed into Codex: five asks ───────────────────────────────────────────────────────────
class B64_CodexAsk(Scene):
    def construct(self):
        W = 9.2
        C0 = np.array([0.0, 0.3, 0.0])
        img = ImageMobject("pantry/a6_codex_ask.png").set_width(W).move_to(C0)
        edge = Rectangle(width=W, height=W * 900 / 1600.0, stroke_color=DIM, stroke_width=3, fill_opacity=0).move_to(C0)
        grp = Group(img, edge)
        self.add(grp)
        WC, CY = 11.2, 0.3                                   # the two pre-cropped views of the prompt stay fully inside the title-safe frame
        kc = WC / 900.0
        HC = 450 * kc

        def cropmob(path):
            im = ImageMobject(path).set_width(WC).move_to([0, CY, 0])
            ed = Rectangle(width=WC, height=HC, stroke_color=DIM, stroke_width=3, fill_opacity=0).move_to([0, CY, 0])
            return Group(im, ed)

        def mark(v, v0):                                      # a terracotta dot beside ask n: preview px (452, v) in the crop whose top is v0
            return Dot([-WC / 2 + (452 - 440) * kc, CY + HC / 2 - (v - v0) * kc, 0.0], radius=0.09, color=TERRA)
        cA, cB = cropmob("pantry/a6_codex_ask_cropA.png"), cropmob("pantry/a6_codex_ask_cropB.png")
        until(self, "session limit", lead=0.5)
        c1 = T("Claude Code, asked first:", 32, DIM).move_to([0, -2.62, 0])
        c2 = T("You've hit your session limit · resets 6:40pm (America/New_York)", 34).move_to([0, -3.06, 0])
        self.play(FadeIn(c1), FadeIn(c2), run_time=0.5)
        until(self, "Five asks", lead=0.1)
        self.play(FadeOut(c1), FadeOut(c2), FadeOut(grp), FadeIn(cA), run_time=0.5)
        until(self, "fix only the import setting", lead=0.2)
        m1 = mark(272, 115)
        self.play(FadeIn(m1), run_time=0.2)
        until(self, "make the floor check honest", lead=0.2)
        m2 = mark(445, 115)
        self.play(FadeOut(m1), FadeIn(m2), run_time=0.2)
        until(self, "read the capsule height", lead=0.2)
        m3 = mark(532, 115)
        self.play(FadeOut(m2), FadeIn(m3), run_time=0.2)
        until(self, "replace the pennant check", lead=0.7)
        self.play(FadeOut(m3), FadeOut(cA), FadeIn(cB), run_time=0.4)
        m4 = mark(561, 425)
        self.play(FadeIn(m4), run_time=0.2)
        until(self, "then rebuild and report", lead=0.2)
        m5 = mark(677, 425)
        self.play(FadeOut(m4), FadeIn(m5), run_time=0.2)
        done(self)


# ── B65 · what Codex did, then four crashes in its sandbox ───────────────────────────────────────────────────────────
A6_HULL6 = [(-0.3, 0.0), (0.3, 0.0), (0.3, 0.1), (0.08, 1.8), (-0.08, 1.8), (-0.3, 0.1)]
A6_BOX6 = [(-0.3, 0.0), (0.3, 0.0), (0.3, 0.1), (0.3, 1.8), (-0.3, 1.8), (-0.3, 0.1)]


class B65_CodexCrashes(Scene):
    def construct(self):
        # ── Codex's own thread: found in the docs, edited, the hull ──
        W = 12.0
        C0 = np.array([0.0, 0.0, 0.0])
        k = W / 1600.0
        pv = lambda u, v: C0 + np.array([(u - 800) * k, -(v - 285) * k, 0.0])        # preview-pixel (1600 x 569)
        img = ImageMobject("pantry/a6_codex_found.png").set_width(W).move_to(C0)
        edge = Rectangle(width=W, height=W * 569 / 1600.0, stroke_color=DIM, stroke_width=3, fill_opacity=0).move_to(C0)
        marks = [Dot(pv(452, y), radius=0.09, color=TERRA).set_opacity(0) for y in (378, 446, 566)]
        grp = Group(img, edge, *marks)
        st = {"z": 1.0, "t": np.zeros(3)}
        self.add(grp)
        self.play(a6_cam(st, grp, 1.75, pv(963, 330)), run_time=0.9)
        until(self, "in the documentation", lead=0.9)
        self.play(marks[0].animate.set_opacity(1), run_time=0.2)
        until(self, "already on", lead=0.2)
        self.play(marks[0].animate.set_opacity(0), marks[1].animate.set_opacity(1), run_time=0.2)
        until(self, "replaced the box", lead=0.3)
        self.play(marks[1].animate.set_opacity(0), marks[2].animate.set_opacity(1), run_time=0.2)
        # ── the box becomes a tapered hull ──
        until(self, "tapered convex hull", lead=1.3)
        U = 2.4
        PH = a6_P(U, -3.4, -2.9)
        post = a6_post(PH)
        box = Polygon(*[PH(x, y) for x, y in A6_BOX6], fill_opacity=0, stroke_color=INK, stroke_width=6)
        hull = Polygon(*[PH(x, y) for x, y in A6_HULL6], fill_opacity=0, stroke_color=INK, stroke_width=6)
        lb = T("a box", 36).move_to([-1.5, 0.5, 0])
        self.play(FadeOut(grp), FadeIn(post), Create(box), FadeIn(lb), run_time=0.5)
        self.play(Transform(box, hull), run_time=0.8)
        lh = T("a tapered convex hull", 36).move_to([0.3, 0.5, 0])
        self.play(FadeOut(lb), FadeIn(lh), run_time=0.3)
        # ── the rebuild: four crashes ──
        until(self, "tried to rebuild", lead=0.2)
        self.play(FadeOut(post), FadeOut(box), FadeOut(lh), run_time=0.3)
        title = T("Blender, inside Codex's sandbox", 38).move_to([0, 2.75, 0])
        labels = ["as written", "private temp folder", "separate config folder", "--gpu-backend flag"]
        rows = [T(s, 36).move_to([-6.0 + 0.19 * len(s) / 2 + 0.0, 1.75 - 0.62 * i, 0]) for i, s in enumerate(labels)]
        exits = [a6_mono("exit 139", 3.9, 1.75 - 0.62 * i) for i in range(4)]
        self.play(FadeIn(title), FadeIn(rows[0]), run_time=0.4)
        until(self, "four times", lead=1.6)
        self.play(FadeIn(rows[1]), run_time=0.25)
        self.play(FadeIn(rows[2]), run_time=0.25)
        self.play(FadeIn(rows[3]), run_time=0.25)
        until(self, "exit code", lead=0.2)
        crosses = VGroup(*[VGroup(Line([3.35, 1.75 - 0.62 * i + 0.14, 0], [3.65, 1.75 - 0.62 * i - 0.14, 0], color=INK, stroke_width=7),
                                  Line([3.35, 1.75 - 0.62 * i - 0.14, 0], [3.65, 1.75 - 0.62 * i + 0.14, 0], color=INK, stroke_width=7)) for i in range(4)])
        self.play(FadeIn(VGroup(*exits)), Create(crosses), run_time=0.5)
        until(self, "graphics-backend check", lead=0.5)
        cl = T("crash site, from Blender's own crash log", 34).move_to([0, -0.95, 0])
        s1 = a6_mono("GPU_backend_type_selection_detect", -4.1, -1.65)
        s2 = a6_mono("metal_is_supported", -4.1, -2.17)
        self.play(FadeIn(cl), run_time=0.3)
        self.play(FadeIn(s1), FadeIn(s2), run_time=0.4)
        done(self)


# ── B66 · Codex reaches for the Blender application; the tool refuses; the rule that was not repeated ────────────────────
class B66_CodexRefused(Scene):
    def construct(self):
        W = 11.6
        C0 = np.array([0.0, 0.7, 0.0])
        ia = ImageMobject("pantry/a6_codex_tool_a_crop.png").set_width(W).move_to(C0)
        ib = ImageMobject("pantry/a6_codex_tool_b_crop.png").set_width(W).move_to(C0).set_opacity(0)
        grp = Group(ia, ib)
        self.add(grp)
        until(self, "That tool refused", lead=0.1)
        self.play(ia.animate.set_opacity(0), ib.animate.set_opacity(1), run_time=0.5)
        until(self, "We stopped the run there", lead=0.0)
        stop = Dot([-4.3, -2.45, 0], radius=0.12, color=TERRA)
        sl = T("stopped by the operator, 5 min 31 s in", 36).move_to([0, -2.45, 0])
        self.play(FadeIn(stop), FadeIn(sl), run_time=0.4)
        # ── the missing rule ──
        until(self, "The prompt hadn't repeated", lead=0.0)
        self.play(FadeOut(grp), FadeOut(stop), FadeOut(sl), run_time=0.3)
        cardA = RoundedRectangle(width=4.6, height=2.3, corner_radius=0.2, fill_opacity=0, stroke_color=DIM, stroke_width=4).move_to([-3.4, 1.5, 0])
        cardB = RoundedRectangle(width=4.6, height=2.3, corner_radius=0.2, fill_opacity=0, stroke_color=DIM, stroke_width=4).move_to([3.4, 1.5, 0])
        ha = T("first prompt", 34).move_to([-3.4, 2.3, 0])
        hb = T("revision prompt", 34).move_to([3.4, 2.3, 0])
        ra1 = a6_mono("Never open", -3.4 - 0.25 * 10 / 2, 1.5)
        ra2 = a6_mono("its window.", -3.4 - 0.25 * 11 / 2, 1.0)
        self.play(FadeIn(cardA), FadeIn(cardB), FadeIn(ha), FadeIn(hb), run_time=0.4)
        self.play(FadeIn(ra1), FadeIn(ra2), run_time=0.3)
        until(self, "never to open the window", lead=0.0)
        g1 = a6_mono("Never open", 3.4 - 0.25 * 10 / 2, 1.5, color=GHOST)
        g2 = a6_mono("its window.", 3.4 - 0.25 * 11 / 2, 1.0, color=GHOST)
        gbox = DashedVMobject(RoundedRectangle(width=3.7, height=1.4, corner_radius=0.15, fill_opacity=0, stroke_color=DIM, stroke_width=4).move_to([3.4, 1.25, 0]), num_dashes=40)
        self.play(FadeIn(g1), FadeIn(g2), Create(gbox), run_time=0.5)
        # ── another way ──
        until(self, "another way", lead=0.7)
        l1 = T("first way", 34).move_to([-3.4, -0.55, 0])
        l2 = T("another way", 34).move_to([3.4, -0.55, 0])
        b1 = RoundedRectangle(width=3.4, height=0.85, corner_radius=0.2, fill_opacity=0, stroke_color=DIM, stroke_width=4).move_to([-3.4, -1.45, 0])
        t1 = a6_mono("Blender -b", -3.4 - 0.25 * 10 / 2, -1.45)
        x1 = a6_mono("exit 139", -3.4 - 0.25 * 8 / 2, -2.3)
        b2 = RoundedRectangle(width=3.4, height=0.85, corner_radius=0.2, fill_opacity=0, stroke_color=DIM, stroke_width=4).move_to([3.4, -1.45, 0])
        t2 = a6_mono("cua_repl js", 3.4 - 0.25 * 11 / 2, -1.45)
        ar = Arrow([-1.5, -1.45, 0], [1.5, -1.45, 0], buff=0, color=INK, stroke_width=6, tip_length=0.22)
        self.play(FadeIn(l1), FadeIn(b1), FadeIn(t1), FadeIn(x1), run_time=0.4)
        self.play(Create(ar), FadeIn(l2), FadeIn(b2), FadeIn(t2), run_time=0.6)
        done(self)


# ── B67A · outside the sandbox: every check of the finished test, as a slot that fills ───────────────────────────────────
# The 16 PASS lines of logs/verify2-test_checkpoint_post.log (a count the evidence script re-derives); nothing is typed in by hand but the count source.
A6_PASS_LINES = [
    "visual height (Godot Y = Blender Z) ≈ 1.80 m  [got 1.8000]", "visual depth  (Godot Z = Blender Y) ≈ 0.60 m  [got 0.6000]",
    "visual width  (Godot X = Blender X) ≈ 0.78 m  [got 0.7800]", "all MeshInstance3D have unit scale  [3 meshes checked]",
    "PostMetal material present", "FlagCloth material present", 'no unexpected named materials  ["PostMetal", "FlagCloth"]',
    "at least one StaticBody3D present  [found 1]", "StaticBody3D has a ConvexPolygonShape3D", "collision Y_min ≤ 0.02 (covers base floor)",
    "collision Y_max ≥ 1.75 (covers pole top)  [got 1.800]", "no pennant length lies inside collider  [overlap 0.0000 m]",
    "player scene has a capsule collision shape", "prop height 1.80 m < player capsule 2.10 m",
    "downward ray hits supporting floor with post excluded", "floor is within 0.02 m of post base  [distance 0.0000 m]"]


class B67A_AllPass(Scene):
    def construct(self):
        n = len(A6_PASS_LINES)                                                   # 16, from the log
        sb = DashedVMobject(RoundedRectangle(width=3.5, height=4.1, corner_radius=0.25, fill_opacity=0, stroke_color=DIM, stroke_width=4).move_to([-4.4, 0.35, 0]), num_dashes=60)
        sbl = T("Codex's sandbox", 34).move_to([-4.4, 2.0, 0])
        xx = VGroup(Line([-4.8, 1.0, 0], [-4.0, 0.2, 0], color=INK, stroke_width=9), Line([-4.8, 0.2, 0], [-4.0, 1.0, 0], color=INK, stroke_width=9))
        ex = a6_mono("exit 139", -5.0, -0.6)
        ol = T("outside the sandbox", 36).move_to([2.2, 2.95, 0])
        cells = VGroup(*[RoundedRectangle(width=1.2, height=0.7, corner_radius=0.18, fill_opacity=0, stroke_color=DIM, stroke_width=4)
                         .move_to([-0.1 + 1.4 * (i % 4), 1.9 - 1.0 * (i // 4), 0]) for i in range(n)])
        self.add(sb, sbl, xx, ex, ol)
        until(self, "outside the sandbox", lead=0.6)
        self.play(FadeIn(cells), run_time=0.4)
        for ph in ("Sixteen of sixteen", "Seventeen of seventeen"):      # the voice now says sixteen (the log holds 16 PASS lines); the old words still cue if the sheet is not yet re-voiced
            if ph in _NARR.get("B67A", ""):
                until(self, ph, lead=0.1)
                break
        ticks = [check(float(cells[i].get_center()[0]) - 0.05, float(cells[i].get_center()[1]) + 0.02, 0.15, INK, 7) for i in range(n)]
        self.play(AnimationGroup(*[Create(t) for t in ticks], lag_ratio=0.18), run_time=1.5)
        hero = T(f"{n} of {n}", 72).move_to([2.2, -2.45, 0])
        self.play(FadeIn(hero), run_time=0.3)
        done(self)


# ── B68 · the vertex-only check: the hull's vertices at the pennant's height are the pole's corners ────────────────────────
class B68_VertexCheck(Scene):
    def construct(self):
        U = 2.6
        PH = a6_P(U, -3.0, -2.75)
        # the real log line, then its tick turns into a cross
        l1 = a6_mono("no pennant length lies inside collider", -4.3, 2.95)
        l2 = a6_mono("[overlap 0.0000 m]", -4.3, 2.5)
        tick = check(-4.75, 2.95, 0.17, INK, 7)
        cross = VGroup(Line([-4.95, 3.1, 0], [-4.6, 2.8, 0], color=INK, stroke_width=7), Line([-4.95, 2.8, 0], [-4.6, 3.1, 0], color=INK, stroke_width=7))
        self.add(l1, l2, tick)
        until(self, "is wrong", lead=0.2)
        self.play(Transform(tick, cross), run_time=0.4)
        # the post and its hull
        post = a6_post(PH, metal=BAR2)
        hull = Polygon(*[PH(x, y) for x, y in A6_HULL6], fill_opacity=0, stroke_color=INK, stroke_width=6)
        until(self, "The check looked only", lead=0.3)
        self.play(FadeIn(post), Create(hull), run_time=0.9)
        until(self, "vertices at", lead=0.2)
        verts = VGroup(*[Dot(PH(x, y), radius=0.09, color=INK) for x, y in A6_HULL6])
        self.play(FadeIn(verts), run_time=0.3)
        vl = T("hull vertices", 34).move_to([0.2, -2.6, 0])
        self.play(FadeIn(vl), run_time=0.2)
        until(self, "pennant's height", lead=0.3)
        band = Polygon(PH(-0.55, 1.55), PH(0.95, 1.55), PH(0.95, 1.8), PH(-0.55, 1.8), fill_opacity=0, stroke_color=DIM, stroke_width=4)
        bl = T("the check's window", 34).move_to([2.55, 1.45, 0])
        self.play(Create(band), FadeIn(bl), run_time=0.45)
        until(self, "pole's corners", lead=0.2)
        rings = VGroup(Dot(PH(0.08, 1.8), radius=0.15, color=TERRA), Dot(PH(-0.08, 1.8), radius=0.15, color=TERRA))
        xl = T("x = 0.08", 34).move_to([2.55, 0.75, 0])
        self.play(FadeIn(rings), FadeIn(xl), run_time=0.3)
        until(self, "slanted faces", lead=0.2)
        slide = Dot(PH(0.08, 1.8), radius=0.12, color=TERRA)
        self.play(FadeIn(slide), run_time=0.15)
        self.play(MoveAlongPath(slide, Line(PH(0.08, 1.8), PH(0.3, 0.1))), run_time=1.3)
        fl = T("a face, not a vertex", 34).move_to([2.55, -0.45, 0])
        self.play(FadeIn(fl), run_time=0.3)
        done(self)


# ── B69 · the same 1,066 points against the tapered hull: 55 inside, a 3 cm sliver ────────────────────────────────────────
class B69_Sliver(Scene):
    def construct(self):
        U = 14.0
        P = lambda x, y: np.array([-4.4 + U * (x - 0.08), 1.9 - U * (1.8 - y), 0.0])
        outline = a6_rect(P, 0.08, 1.55, 0.48, 1.80, None, DIM, 4)
        pole = a6_rect(P, -0.0557, 1.543, 0.08, 1.8, BAR1, DIM, 4)
        yb = 1.543
        face = Line(P(0.08, 1.8), P(a6_hw(yb), yb), color=INK, stroke_width=6)
        cap = T("an illustration of the sampling; counts are from the run", 32).move_to([0.0, -3.15, 0])
        allg, ins, outs, n_in = a6_grid(P, hull=True)
        self.add(outline, pole, face, cap)
        self.play(FadeIn(allg), run_time=0.6)
        until(self, "fifty-five", lead=0.2)
        self.play(ins.animate.set_color(INK), run_time=0.5)
        n55 = T("55", 84).move_to([4.1, 1.15, 0])
        self.play(FadeIn(n55), run_time=0.35)
        until(self, "of one thousand sixty-six", lead=0.1)
        n1066 = T("of 1,066 points", 40).move_to([4.1, 0.3, 0])
        lg = Dot([2.35, -0.5, 0], radius=0.1, color=INK)
        lgl = T("inside the collider", 34).move_to([4.5, -0.5, 0])
        self.play(FadeIn(n1066), FadeIn(lg), FadeIn(lgl), run_time=0.4)
        until(self, "reaching point one one", lead=0.2)
        xm = T("x = 0.11 m", 34).move_to([-2.4, -2.52, 0])
        self.play(FadeIn(xm), run_time=0.3)
        until(self, "three centimetre", lead=0.2)
        d3 = dim_arrow([-4.4, -2.1, 0], [-3.98, -2.1, 0], tip=0.1)
        l3 = T("3 cm", 36).move_to([-4.19, -2.52, 0])
        self.play(Create(d3), FadeIn(l3), run_time=0.45)
        until(self, "box's five hundred", lead=0.1)
        b572 = T("572", 60, DIM).move_to([2.55, -1.4, 0])
        bl = T("with the box", 34).move_to([4.85, -1.4, 0])
        self.play(FadeIn(b572), FadeIn(bl), run_time=0.4)
        until(self, "still not zero", lead=0.0)
        nz = Dot([2.15, 1.15, 0], radius=0.12, color=TERRA)
        self.play(FadeIn(nz), run_time=0.3)
        done(self)


# ── B70 · the invisible collision around the pole: 0.19 m hull half-width at mid-taper against the pole's 0.08 m ─────────────
class B70_Invisible(Scene):
    def construct(self):
        U = 3.0
        PH = a6_P(U, -3.2, -2.85)
        post = a6_post(PH, metal=BAR2)
        img_v = ImageMobject("pantry/a6_post_visual.png").set_height(5.2).move_to([4.3, 0.2, 0])
        img_o = ImageMobject("pantry/a6_post_overlay.png").set_height(5.2).move_to([4.3, 0.2, 0]).set_opacity(0)
        self.add(post, img_v)
        until(self, "invisible collision", lead=1.2)
        hullfill = Polygon(*[PH(x, y) for x, y in A6_HULL6], fill_color=CARD, fill_opacity=1, stroke_color=INK, stroke_width=6).set_z_index(-1)
        self.add(img_o)
        self.play(FadeIn(hullfill), img_o.animate.set_opacity(1), run_time=0.8)
        il = T("invisible collision", 34).move_to([0.25, 1.3, 0])
        ld = Line([PH(a6_hw(1.38), 1.38)[0] + 0.2, 1.3, 0], [-1.6 - 0.35, 1.3, 0], color=DIM, stroke_width=3)
        ol = T("collider over the post", 32).move_to([4.3, -2.85, 0])
        self.play(FadeIn(il), Create(ld), FadeIn(ol), run_time=0.35)
        until(self, "eleven centimetres", lead=0.1)
        yy = 0.95
        hw = a6_hw(yy)
        dl = dim_arrow(PH(-hw, yy), PH(-0.08, yy), tip=0.1)
        dr = dim_arrow(PH(0.08, yy), PH(hw, yy), tip=0.1)
        ll = T("11 cm", 34).move_to([PH(-hw, yy)[0] - 0.8, PH(-hw, yy)[1], 0])
        lr = T("11 cm", 34).move_to([PH(hw, yy)[0] + 0.8, PH(hw, yy)[1], 0])
        self.play(Create(dl), Create(dr), FadeIn(ll), FadeIn(lr), run_time=0.6)
        until(self, "design judgment", lead=0.1)
        dj = T("a design judgment", 36).move_to([0.25, -1.7, 0])
        self.play(FadeIn(dj), run_time=0.4)
        done(self)


# ── B71A / B71B · what a pass proves and what it does not: the lecture's last picture ───────────────────────────────────
def a6_final_base(self):
    """The shared set of the last two beats: the real post render on its floor line, two column headers and the divider."""
    img = ImageMobject("pantry/a6_post_visual.png").set_height(5.3).move_to([-4.65, 0.1, 0])
    floor = Line([-6.1, -2.55, 0], [-3.2, -2.55, 0], color=DIM, stroke_width=6)
    div = Line([1.15, 2.3, 0], [1.15, -2.2, 0], color=DIM, stroke_width=3)
    ha = T("a test proves", 40).move_to([-1.0, 2.8, 0])
    hb = T("a person judges", 40).move_to([3.45, 2.8, 0])
    self.add(img, floor, div, ha, hb)


A6_PROVES = ["size", "axes", "scale", "materials", "collision shape", "base on the floor"]
A6_NOT = ["looks right, lit", "metal and cloth", "collider feels fair", "suits the level"]


A6_W36 = {"size": 0.618, "axes": 0.727, "scale": 0.818, "materials": 1.634, "collision shape": 2.615, "base on the floor": 3.106,
          "looks right, lit": 2.493, "metal and cloth": 2.884, "collider feels fair": 2.947, "suits the level": 2.396}   # measured: EB Garamond 36


def a6_row(label, xl, y, kind):
    """One row: a mark (ink check, or an empty ring) and its label (left edge xl + 0.5)."""
    t = T(label, 36).move_to([xl + 0.5 + A6_W36[label] / 2.0, y, 0])
    m = check(xl - 0.15, y, 0.17, INK, 7) if kind == "ok" else Circle(radius=0.17, stroke_color=DIM, stroke_width=5, fill_opacity=0).move_to([xl - 0.1, y, 0])
    return t, m


class B71A_Proves(Scene):
    def construct(self):
        a6_final_base(self)
        until(self, "size,", lead=0.2)
        for i, s in enumerate(A6_PROVES):
            if i == 4:
                until(self, "collision shape", lead=0.15)
            if i == 5:
                until(self, "base touches", lead=0.4)
            if i == 1:
                until(self, "axes", lead=0.1)
            if i == 2:
                until(self, "scale", lead=0.1)
            if i == 3:
                until(self, "materials", lead=0.1)
            t, m = a6_row(s, -2.9, 1.85 - 0.72 * i, "ok")
            self.play(FadeIn(t), Create(m), run_time=0.3)
        dot = Dot([-4.65 + 0.07, -2.5, 0], radius=0.13, color=TERRA)
        self.play(FadeIn(dot), run_time=0.3)
        done(self)


class B71B_Not(Scene):
    def construct(self):
        a6_final_base(self)
        for i, s in enumerate(A6_PROVES):
            t, m = a6_row(s, -2.9, 1.85 - 0.72 * i, "ok")
            self.add(t, m)
        self.add(Dot([-4.65 + 0.07, -2.5, 0], radius=0.13, color=TERRA))
        until(self, "looks right", lead=0.15)
        for i, s in enumerate(A6_NOT):
            if i == 1:
                until(self, "materials read", lead=0.15)
            if i == 2:
                until(self, "collider feels fair", lead=0.15)
            if i == 3:
                until(self, "placement suits", lead=0.15)
            t, m = a6_row(s, 1.75, 1.85 - 0.72 * i, "no")
            self.play(FadeIn(t), Create(m), run_time=0.3)
        until(self, "for a person", lead=0.2)
        eye = VGroup(Ellipse(width=1.5, height=0.8, stroke_color=INK, stroke_width=6, fill_opacity=0), Dot([0, 0, 0], radius=0.17, color=INK)).move_to([3.45, -1.55, 0])
        self.play(Create(eye), run_time=0.5)
        spark = Dot([3.45, -1.55, 0], radius=0.08, color=TERRA)
        self.play(FadeIn(spark), run_time=0.2)
        done(self)
