"""ACT VII · Ship It, and How It's Graded  (B61A–B69; B63 and B64 are Remotion CCPlainShell beats, see lanes/act7.json)

The cast of the act: the FILM (a strip of four frames, B61A), the REAL Godot scene (B61A tile, B61B, B69), the REAL Blender
window (B61A, B62, B68), the REPOSITORY (the terminal in B63/B64), and the GRADE COLUMN 60 / 10 / 10 / 20 (B66, B67).
Every image is a crop of a real capture in pantry/ev_* made by evidence/act7/make_crops.py (no pixel drawn). Numbers on
screen come from evidence/godot/check_good.log, godot/project_src/tests/check_assets.gd (the brief the check compares with,
shown as "example") and the assignment's rubric. The hand-edit pair is made by script and is labelled illustrative.
"""

A7_TILE_W, A7_TILE_H = 2.85, 2.064                        # B61A film frames (crop aspect 1.381)
A7_PIC_W = A7_TILE_W - 0.2                                  # a capture sits 0.1 inside its frame: a cream mount (GATE T samples the ring round a blob)
A7_TILE_X = [-4.575, -1.525, 1.525, 4.575]
A7_TILE_Y = 0.3


def a7_img(path, x, y, w=None, h=None):
    im = ImageMobject(path)
    if w is not None:
        im.set_width(w)
    else:
        im.set_height(h)
    im.move_to([x, y, 0])
    return im


def a7_lbl(s, x, y, size=34, color=INK):
    return T(s, size, color).move_to([x, y, 0])


def a7_lbl_bl(s, x, y, size=34, color=INK):
    """A centred label on a common BASELINE: invisible bars at both ends give every label the same ascender/descender box."""
    t = T("|" + s + "|", size, color)
    t[0].set_opacity(0)
    t[-1].set_opacity(0)
    return t.move_to([x, y, 0])


def a7_lbl_left(s, x, y, size=34, color=INK):
    """A label whose LEFT edge sits at x (computed from the text width, never from get_left())."""
    t = T(s, size, color)
    return t.move_to([x + t.width / 2, y, 0])


def a7_mono_left(s, x, y, size=32, color=INK):
    """Menlo text whose first visible character starts at x, on a common baseline (hidden bars at both ends)."""
    t = M("|" + s + "|", size, color)
    t[0].set_opacity(0)
    t[-1].set_opacity(0)
    return t.move_to([x - 0.243 + t.width / 2, y, 0])


def a7_strip():
    """The film: two DIM bands with sprocket holes, separators between four empty frames (the frames are bare stage)."""
    bands = VGroup()
    for yc in (A7_TILE_Y + A7_TILE_H / 2 + 0.22, A7_TILE_Y - A7_TILE_H / 2 - 0.22):
        bands.add(Rectangle(width=12.3, height=0.44, fill_color=DIM, fill_opacity=1, stroke_width=0).move_to([0, yc, 0]))
    seps = VGroup(*[Rectangle(width=0.2, height=A7_TILE_H + 0.02, fill_color=DIM, fill_opacity=1, stroke_width=0).move_to([x, A7_TILE_Y, 0])
                    for x in (-3.05, 0.0, 3.05)])
    caps = VGroup(*[Rectangle(width=0.15, height=A7_TILE_H + 0.02, fill_color=DIM, fill_opacity=1, stroke_width=0).move_to([x, A7_TILE_Y, 0])
                    for x in (-6.075, 6.075)])
    holes = VGroup()
    for yc in (A7_TILE_Y + A7_TILE_H / 2 + 0.22, A7_TILE_Y - A7_TILE_H / 2 - 0.22):
        for i in range(27):
            holes.add(Rectangle(width=0.17, height=0.15, fill_color=STAGE, fill_opacity=1, stroke_width=0).move_to([-5.85 + i * 0.45, yc, 0]))
    return VGroup(bands, seps, caps, holes)


# ── B61A · one film: four frames, each from the real evidence ─────────────────────────────────────────────────────────────
class B61A_OneFilm(Scene):
    def construct(self):
        title = T("Ship It, and How It's Graded", 40).move_to([-3.05, 3.05, 0])
        strip = a7_strip()
        self.add(title)
        self.play(FadeIn(strip, shift=LEFT * 0.4), run_time=0.6)
        head = Dot([A7_TILE_X[0], 2.2, 0], radius=0.11, color=TERRA)
        self.play(FadeIn(head), run_time=0.3)
        # frame 1: the game and its three assets, in the running Godot scene
        until(self, "It names", lead=-0.1)
        g = a7_img("pantry/a7_godot_tile2.png", A7_TILE_X[0], A7_TILE_Y, w=A7_PIC_W)
        l1a, l1b = a7_lbl_bl("your game,", A7_TILE_X[0], -1.72), a7_lbl_bl("three assets", A7_TILE_X[0], -2.25)
        self.play(FadeIn(g), FadeIn(l1a), FadeIn(l1b), run_time=0.5)
        # frame 2: the real Blender session
        until(self, "and shows your real Blender", lead=-0.2)
        b = a7_img("pantry/a7_bl_session_tile.png", A7_TILE_X[1], A7_TILE_Y, w=A7_PIC_W)
        l2 = a7_lbl_bl("Blender session", A7_TILE_X[1], -1.72)
        self.play(head.animate.move_to([A7_TILE_X[1], 2.2, 0]), FadeIn(b), FadeIn(l2), run_time=0.5)
        # frame 3: a prompt (the assignment's own words, from its adapted prompt)
        until(self, "with at least one prompt", lead=0.0)
        p = VGroup(*[M(s, 32).move_to([A7_TILE_X[2], A7_TILE_Y + 0.5 - i * 0.5, 0]) for i, s in enumerate(["Do not", "build", "yet."])])
        l3 = a7_lbl_bl("a prompt", A7_TILE_X[2], -1.72)
        self.play(head.animate.move_to([A7_TILE_X[2], 2.2, 0]), FadeIn(p), FadeIn(l3), run_time=0.45)
        # frame 4: the hand edit, before -> after (made by script: illustrative)
        until(self, "and your own hand edit", lead=0.05)
        hb = a7_img("pantry/a7_hand_before_tile.png", A7_TILE_X[3], A7_TILE_Y, w=A7_PIC_W)
        ha = a7_img("pantry/a7_hand_after_tile.png", A7_TILE_X[3], A7_TILE_Y, w=A7_PIC_W)
        l4a, l4b = a7_lbl_bl("hand edit", A7_TILE_X[3], -1.72), a7_lbl_bl("(illustrative)", A7_TILE_X[3], -2.25)
        self.play(head.animate.move_to([A7_TILE_X[3], 2.2, 0]), FadeIn(hb), FadeIn(l4a), FadeIn(l4b), run_time=0.4)
        self.wait(0.15)
        self.play(FadeIn(ha), run_time=0.3)
        done(self)


# ── B61B · the real Godot scene, with the headless numbers beside the brief ─────────────────────────────────────────────────
A7_BRIEF = [("crate", "(0.8, 0.8, 0.8)"), ("lantern", "(0.3, 0.5, 0.3)"), ("coin", "(0.3, 0.04, 0.3)")]     # check_assets.gd BRIEF (Godot X, Y, Z)
A7_HEADLESS = ["(0.8, 0.8, 0.8)", "(0.3, 0.5, 0.3)", "(0.3, 0.04, 0.3)"]                                    # check_good.log, bounding box size


class B61B_GodotNumbers(Scene):
    def construct(self):
        img = a7_img("pantry/a7_godot_lookA_wide.png", A7_TILE_X[0], A7_TILE_Y, h=A7_TILE_H)
        self.add(img)
        self.play(img.animate.set_height(3.49).move_to([-1.2, 1.45, 0]), run_time=0.7)
        until(self, "running Godot scene", lead=0.3)
        g1, g2 = a7_lbl("running", 3.7, 2.35, 36), a7_lbl("Godot scene", 3.7, 1.8, 36)
        spark = Dot([2.55, 2.35, 0], radius=0.1, color=TERRA)
        self.play(FadeIn(g1), FadeIn(g2), FadeIn(spark), run_time=0.4)
        hy = -0.85
        h1 = a7_lbl_bl("brief (example)", -1.5, hy, 34)
        h2 = a7_lbl_bl("headless", 3.15, hy, 34)
        h0 = a7_lbl_bl("in metres", -4.7, hy, 34)
        sep = Line([0.82, -0.55, 0], [0.82, -3.1, 0], color=DIM, stroke_width=4)
        self.play(FadeIn(h0), FadeIn(h1), FadeIn(h2), Create(sep), run_time=0.35)
        rows_y = [-1.55, -2.2, -2.85]
        until(self, "with the headless numbers", lead=0.0)
        for (name, brief), hv, y in zip(A7_BRIEF, A7_HEADLESS, rows_y):
            n = a7_lbl_bl(name, -4.7, y, 36)
            bv = M(brief, 32).move_to([-1.5, y, 0])
            hvm = M(hv, 32).move_to([3.15, y, 0])
            self.play(FadeIn(n), FadeIn(bv), FadeIn(hvm), run_time=0.3)
        until(self, "beside your brief", lead=0.1)
        checks = VGroup(*[check(5.6, y + 0.05, 0.2) for y in rows_y])
        self.play(LaggedStart(*[Create(c) for c in checks], lag_ratio=0.3), run_time=0.6)
        done(self)


# ── B62 · the ledger: checked / uncertain / Claude got wrong / human and AI; then labelled evidence ─────────────────────────
def a7_person(x, y, s=1.0, color=INK):
    head = Circle(radius=0.17 * s, color=color, stroke_width=5).move_to([x, y + 0.2 * s, 0])
    body = Arc(radius=0.34 * s, start_angle=0, angle=PI, color=color, stroke_width=5).move_to([x, y - 0.22 * s, 0])
    return VGroup(head, body)


def a7_cross(x, y, s=0.26, color=INK):
    return VGroup(Line([x - s, y - s, 0], [x + s, y + s, 0], color=color, stroke_width=7),
                  Line([x - s, y + s, 0], [x + s, y - s, 0], color=color, stroke_width=7))


def a7_lantern(cx, base_y, u=3.6):
    """The lantern redrawn from its own build numbers (evidence/assets/ASSETS.md), side view: a RECONSTRUCTION."""
    base = Rectangle(width=0.30 * u, height=0.04 * u, fill_color=BAR1, fill_opacity=1, stroke_color=INK, stroke_width=4)
    base.move_to([cx, base_y + 0.02 * u, 0])
    glass = Rectangle(width=0.20 * u, height=0.23 * u, fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=4)
    glass.move_to([cx, base_y + 0.155 * u, 0])
    flame = Circle(radius=0.06 * u, fill_color=TERRA, fill_opacity=1, stroke_width=0).move_to([cx, base_y + 0.32 * u, 0])
    roof = Polygon([cx - 0.14 * u, base_y + 0.37 * u, 0], [cx + 0.14 * u, base_y + 0.37 * u, 0], [cx, base_y + 0.47 * u, 0],
                   fill_color=BAR1, fill_opacity=1, stroke_color=INK, stroke_width=4)
    fin = Rectangle(width=0.04 * u, height=0.03 * u, fill_color=BAR1, fill_opacity=1, stroke_color=INK, stroke_width=3)
    fin.move_to([cx, base_y + 0.485 * u, 0])
    return VGroup(base, glass, flame, roof, fin)


class B62_Ledger(Scene):
    def construct(self):
        xs = A7_TILE_X
        heads = ["checked", "uncertain", "Claude got wrong", "human / AI"]
        cues = ["It says what you checked", "what's uncertain", "what Claude got wrong", "and who did what"]
        leads = [-0.6, 0.0, 0.0, 0.1]
        for i, (x, hd, cue, ld) in enumerate(zip(xs, heads, cues, leads)):
            until(self, cue, lead=ld)
            cell = RoundedRectangle(width=2.85, height=2.1, corner_radius=0.18, fill_opacity=0, stroke_color=DIM, stroke_width=4).move_to([x, 1.15, 0])
            h = a7_lbl_bl(hd, x, 2.72, 34)
            if i == 0:
                glyph = check(x - 0.05, 1.68, 0.3)
            elif i == 1:
                glyph = T("?", 64).move_to([x, 1.66, 0])
            elif i == 2:
                glyph = a7_cross(x, 1.66)
            else:
                glyph = VGroup(a7_person(x - 0.35, 1.66), Dot([x + 0.45, 1.6, 0], radius=0.15, color=TERRA))
            rows = VGroup(*[Line([x - 1.0, yy, 0], [x + 1.0, yy, 0], color=GHOST, stroke_width=6) for yy in (0.82, 0.45)])
            self.play(Create(cell), FadeIn(h), FadeIn(glyph), Create(rows), run_time=0.45)
        # evidence you made, labelled; a reconstruction, labelled a reconstruction
        until(self, "Use screenshots", lead=0.0)
        shot = a7_img("pantry/a7_bl_view_tile2.png", -3.2, -2.1, h=2.2)
        self.play(FadeIn(shot, shift=UP * 0.2), run_time=0.45)
        until(self, "labelled as such", lead=0.1)
        s_lbl = a7_lbl("screenshot", -3.2, -0.5, 34)
        s_dot = Dot([-4.55, -0.5, 0], radius=0.1, color=TERRA)
        self.play(FadeIn(s_lbl), FadeIn(s_dot), run_time=0.35)
        until(self, "A reconstruction is labelled", lead=0.1)
        frame = RoundedRectangle(width=3.04, height=2.2, corner_radius=0.12, fill_opacity=0, stroke_color=DIM, stroke_width=4).move_to([3.2, -2.1, 0])
        lan = a7_lantern(3.2, -2.97)
        self.play(Create(frame), LaggedStart(*[FadeIn(p) for p in lan], lag_ratio=0.25), run_time=0.7)
        until(self, "a reconstruction.", lead=0.15)
        r_lbl = a7_lbl("reconstruction", 3.2, -0.5, 34)
        self.play(FadeIn(r_lbl), run_time=0.35)
        done(self)


# ── B65 · the submission note: the assignment's own template, field by field ─────────────────────────────────────────────
A7_FORM = ["…",
           "The three assets and what each is for:",
           "MCP project and version, or \"script route\" …",
           "My hand edit in Blender:",
           "Checks run (command and result):",
           "Final film URL and filename:",
           "Final film SHA-256:",
           "…"]


class B65_SubmissionNote(Scene):
    def construct(self):
        iso = Iso(3.0, 2.3, 0.5)
        box = iso.box(0, 0, 0, 1.0, 1.0, 0.75)
        zl = a7_lbl_left("source zip", 3.95, 2.72, 34)
        self.play(FadeIn(box, shift=DOWN * 0.25), FadeIn(zl), run_time=0.45)
        until(self, "a submission note", lead=0.2)
        fname = a7_mono_left("SUBMISSION.md", -6.0, 2.75)
        tl = a7_lbl_left("the template", -2.45, 2.72, 34)
        page = RoundedRectangle(width=12.2, height=5.45, corner_radius=0.15, fill_opacity=0, stroke_color=DIM, stroke_width=4).move_to([0, -0.5, 0])
        ys = [1.72 - i * 0.62 for i in range(len(A7_FORM))]
        rows = [a7_mono_left(s, -5.25, y) for s, y in zip(A7_FORM, ys)]
        self.play(FadeIn(fname), FadeIn(tl), Create(page), FadeIn(rows[0]), FadeIn(rows[-1]), run_time=0.6)
        ptr = Dot([-5.65, ys[1], 0], radius=0.09, color=TERRA)
        # each field lands as it is named; the one terracotta dot points at it ("the film link with its checksum" is one item: both rows)
        steps = [("the three assets", [1], 1, 0.15), ("which route", [2], 2, 0.15), ("your hand edit", [3], 3, 0.15),
                 ("the checks you ran", [4], 4, 0.15), ("and the film link", [5, 6], 5, 0.15), ("checksum", [], 6, 0.3)]
        for k, (cue, new_rows, at, ld) in enumerate(steps):
            until(self, cue, lead=ld)
            anims = [FadeIn(rows[r], shift=RIGHT * 0.15) for r in new_rows]
            anims.append(FadeIn(ptr, scale=1.6) if k == 0 else ptr.animate.move_to([-5.65, ys[at], 0]))
            self.play(*anims, run_time=0.3)
        done(self)


# ── B66 · grading: 60 / 10 / 10 / 20, the 80 bracketed, the 20 ringed ────────────────────────────────────────────────────
A7_CX, A7_CW, A7_U = -1.2, 1.6, 0.06              # grade column: centre x, width, units per point
A7_NUMX, A7_LBLX = 0.45, 1.45


def a7_seg(y0, y1, fill, stroke=None):
    r = Rectangle(width=A7_CW, height=y1 - y0, fill_color=fill, fill_opacity=1,
                  stroke_color=stroke or fill, stroke_width=3 if stroke else 0)
    return r.move_to([A7_CX, (y0 + y1) / 2, 0])


A7_SEGS = [(-3.2, 0.4, BAR1, None, "60", "the work"),
           (0.48, 1.08, BAR2, None, "10", "honest log"),
           (1.16, 1.76, BAR2, None, "10", "GitHub = Canvas"),
           (1.84, 3.04, GHOST, DIM, "20", "relative")]


def a7_b66_parts():
    """Every B66 mobject at its final place (B66 builds them on cue; B67 opens on all of them, so the cut is seamless)."""
    top = a7_lbl_left("100 points", -6.0, 2.7, 40)
    segs = []
    for y0, y1, fill, stroke, num, lbl in A7_SEGS:
        segs.append((a7_seg(y0, y1, fill, stroke), T(num, 44).move_to([A7_NUMX, (y0 + y1) / 2, 0]),
                     a7_lbl_left(lbl, A7_LBLX, (y0 + y1) / 2, 34)))
    br = Brace(Line([-2.15, -3.2, 0], [-2.15, 1.76, 0]), direction=LEFT, color=INK, buff=0.1)
    e80 = T("80", 52).move_to([-3.4, -0.55, 0])
    ecl = a7_lbl("criteria met", -3.9, -1.3, 34)
    ring = Ellipse(width=1.25, height=0.95, color=TERRA, stroke_width=7).move_to([A7_NUMX, 2.44, 0])
    return dict(top=top, segs=segs, br=br, e80=e80, ecl=ecl, ring=ring)


class B66_Grading(Scene):
    def construct(self):
        P = a7_b66_parts()
        self.add(P["top"])
        for (seg, n, l), cue in zip(P["segs"], ["Sixty points", "ten for your honest log", "ten for matching", "and twenty relative"]):
            until(self, cue, lead=0.1)
            self.play(GrowFromEdge(seg, DOWN), FadeIn(n), FadeIn(l), run_time=0.5)
        until(self, "Meeting the criteria", lead=0.1)
        self.play(FadeIn(P["ecl"]), run_time=0.4)
        until(self, "the other eighty", lead=0.05)
        self.play(GrowFromCenter(P["br"]), FadeIn(P["e80"]), run_time=0.5)
        until(self, "the twenty", lead=0.0)
        self.play(Create(P["ring"]), run_time=0.48)
        done(self)


# ── B67 · the sixty, split: 10 / 14 / 18 / 10 / 8 ───────────────────────────────────────────────────────────────────────
A7_SPLIT = [("10", "brief"), ("14", "process"), ("18", "three assets"), ("10", "Godot checks"), ("8", "film")]


class B67_TheSixty(Scene):
    def construct(self):
        P = a7_b66_parts()
        everything = [P["top"], P["br"], P["e80"], P["ecl"], P["ring"]] + [m for part in P["segs"] for m in part]
        self.add(*everything)                                   # B66's last frame
        seg = P["segs"][0][0]
        tall = Rectangle(width=A7_CW, height=6.2, fill_opacity=0, stroke_color=DIM, stroke_width=4).move_to([A7_CX, -0.1, 0])
        br = Brace(Line([-2.15, -3.2, 0], [-2.15, 3.0, 0]), direction=LEFT, color=INK, buff=0.1)
        b60 = T("60", 52).move_to([-3.4, -0.1, 0])
        self.play(Transform(seg, tall), *[FadeOut(m) for m in everything if m is not seg], run_time=0.45)
        self.play(GrowFromCenter(br), FadeIn(b60), run_time=0.25)
        gap, u = 0.07, (6.2 - 4 * 0.07) / 60
        top_y = 3.0
        cues = ["ten for the brief", "fourteen for the process", "eighteen for the three assets", "ten for the Godot checks", "and eight for the film"]
        for i, ((num, lbl), cue) in enumerate(zip(A7_SPLIT, cues)):
            h = int(num) * u
            ya, yb = top_y - h, top_y
            until(self, cue, lead=0.1)
            piece = a7_seg(ya, yb, BAR1 if i % 2 == 0 else BAR2)
            nn = T(num, 44).move_to([A7_NUMX, (ya + yb) / 2, 0])
            ll = a7_lbl_left(lbl, A7_LBLX, (ya + yb) / 2, 34)
            self.play(GrowFromEdge(piece, UP), FadeIn(nn), FadeIn(ll), run_time=0.4)
            top_y = ya - gap
        done(self)


# ── B68 · late work, and explaining it from the real Blender sidebar ─────────────────────────────────────────────────────
A7_PX = 1.45 / 270.0                              # scene units per crop pixel (crop shown at 1.45x its pixels on a 4K frame)
A7_LOC = ("pantry/a7_bl_location.png", 970, 345, 1.7, 1.55)      # path, w px, h px, centre x, centre y
A7_SD = ("pantry/a7_bl_scale_dims.png", 970, 669, 1.7, -1.45)


def a7_crop(spec):
    path, w, h, cx, cy = spec
    return a7_img(path, cx, cy, w=w * A7_PX)


def a7_ring(spec, box, color=TERRA):
    """A ring round a pixel box (x0, y0, x1, y1) of a crop placed by its spec."""
    _, w, h, cx, cy = spec
    x0, y0, x1, y1 = box
    left, top = cx - w * A7_PX / 2, cy + h * A7_PX / 2
    pa = np.array([left + x0 * A7_PX, top - y1 * A7_PX, 0])
    pb = np.array([left + x1 * A7_PX, top - y0 * A7_PX, 0])
    return RoundedRectangle(width=pb[0] - pa[0], height=pb[1] - pa[1], corner_radius=0.12, fill_opacity=0,
                            stroke_color=color, stroke_width=7).move_to((pa + pb) / 2)


class B68_LateAndExplain(Scene):
    def construct(self):
        late = a7_lbl_left("late work", -6.0, 2.95, 36)
        cells = VGroup(*[Rectangle(width=0.4, height=0.55, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([-5.8 + i * 0.45, 2.2, 0])
                         for i in range(10)])
        self.add(late, cells)
        until(self, "ten percent a day", lead=0.2)
        gone = DashedVMobject(Rectangle(width=0.4, height=0.55, color=DIM, stroke_width=4).move_to([-5.8 + 9 * 0.45, 2.2, 0]), num_dashes=10)
        self.play(FadeOut(cells[9], shift=DOWN * 0.6), Create(gone), run_time=0.55)
        m10 = T("−10%", 60).move_to([-3.85, 1.1, 0])
        pdy = a7_lbl("per day", -3.85, 0.35, 36)
        self.play(FadeIn(m10), FadeIn(pdy), run_time=0.35)
        until(self, "And you must be able", lead=0.0)
        ex = a7_lbl("explain it", -3.85, -2.3, 40)
        self.play(FadeIn(ex), run_time=0.35)
        until(self, "Be ready to open", lead=0.1)
        icon = a7_img("pantry/ev_icon_blender.png", -3.85, -1.05, h=1.1)
        arr = Arrow([-3.05, -1.05, 0], [-1.25, -1.05, 0], buff=0, color=INK, stroke_width=5, tip_length=0.2)
        loc, sd = a7_crop(A7_LOC), a7_crop(A7_SD)
        self.play(FadeIn(icon), Create(arr), FadeIn(loc, shift=LEFT * 0.3), FadeIn(sd, shift=LEFT * 0.3), run_time=0.6)
        # rings: size (Dimensions), origin (Location: where the origin sits), applied transforms (Scale 1.000)
        until(self, "size, origin", lead=0.05)
        r_size = a7_ring(A7_SD, (14, 408, 948, 660))
        t_size = a7_lbl("size", 5.3, -2.35, 36)
        self.play(Create(r_size), FadeIn(t_size), run_time=0.4)
        until(self, "origin and applied", lead=0.05)
        r_org = a7_ring(A7_LOC, (14, 80, 815, 336))
        t_org = a7_lbl("origin", 5.3, 1.3, 36)
        self.play(Create(r_org), FadeIn(t_org), run_time=0.4)
        until(self, "applied transforms", lead=0.0)
        r_scl = a7_ring(A7_SD, (14, 78, 740, 330))
        t_scl = a7_lbl("scale 1", 5.3, -0.6, 36)
        self.play(Create(r_scl), FadeIn(t_scl), run_time=0.4)
        done(self)


# ── B69 · what a check shows, and what only you judge ─────────────────────────────────────────────────────────────────────
class B69_JudgmentIsYours(Scene):
    def construct(self):
        div = Line([0, 2.95, 0], [0, -3.05, 0], color=DIM, stroke_width=4)
        h1 = a7_lbl("a check shows", -3.3, 2.7, 40)
        h2 = a7_lbl("only you judge", 3.3, 2.7, 40)
        self.add(div)
        self.play(FadeIn(h1), FadeIn(h2), run_time=0.4)
        items = ["size", "orientation", "scale"]
        ys = [1.35, 0.25, -0.85]
        until(self, "A passing check", lead=0.0)
        labels = VGroup(*[a7_lbl_left(s, -4.25, y, 40) for s, y in zip(items, ys)])
        self.play(FadeIn(labels), run_time=0.4)
        for y, cue in zip(ys, ["the size", "orientation", "and scale"]):
            until(self, cue, lead=0.0)
            self.play(Create(check(-5.1, y + 0.03, 0.22)), run_time=0.3)
        until(self, "It doesn't show", lead=0.1)
        g = a7_img("pantry/a7_godot_lookA_wide.png", 3.3, 0.55, w=5.6)
        self.play(FadeIn(g), run_time=0.5)
        until(self, "look right", lead=0.2)
        tl = a7_lbl("the look", 2.9, -1.75, 40)
        self.play(FadeIn(tl), run_time=0.35)
        until(self, "That judgment", lead=0.1)
        eye = Ellipse(width=0.95, height=0.52, color=INK, stroke_width=5).move_to([4.6, -1.75, 0])
        pupil = Dot([4.6, -1.75, 0], radius=0.14, color=TERRA)
        self.play(Create(eye), FadeIn(pupil), run_time=0.45)
        done(self)
