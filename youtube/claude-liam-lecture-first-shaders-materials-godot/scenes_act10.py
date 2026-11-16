"""ACT X · Ship It, and How It's Graded  (B69, B70, B72, B73, B74 Manim; B71 is a Remotion CCPlainShell, see lanes/act10.json)

Cast of the act: the path of what the film shows (B69), the repository (a low-walled iso box with white file-cubes), the commit chain and the a5 tag on a
string (B70), the grade column 60 / 10 / 10 / 20 (B72), three challenge cards with REAL lines of the example's shaders (B73), the two stamps and the REAL lab
panel (B74). Real pictures are crops made by evidence/act10/make_crops.py (nothing redrawn): pantry/a10_pad_idle.png and a10_lab_panel.png come from
captures/lab/ (scripted input, labelled so), pantry/a10_pad_half.png from the example's pad capture at activation 0.5 (Compatibility).
Text widths are measured (EB Garamond / Menlo, real Manim): the Gate A stub's Text.width is wrong, so nothing here positions with .width.
No video number and no assignment number appears on screen; the tag a5 is the assignment's own tag name.
"""

A10_CW = {20: 0.15, 24: 0.20}
A10_W = {   # measured EB Garamond widths (units) at the size noted in the key
    ("your game", 34): 1.870, ("four answers", 34): 2.276, ("captures", 34): 1.521, ("tests, mutations", 34): 2.821, ("the limits", 34): 1.621,
    ("scripted input", 32): 2.373, ("reconstruction", 32): 2.462, ("held frame", 32): 1.804,
    ("shaders", 32): 1.216, ("scenes", 32): 0.966, ("driver", 32): 0.931, ("materials", 32): 1.519, ("textures", 32): 1.314, ("tests", 32): 0.714,
    ("wrapper", 32): 1.444, ("documents, logs", 32): 2.714, ("cache", 32): 0.947, ("credentials", 32): 1.714, ("over 25 MB", 32): 1.928,
    ("shader", 32): 1.083, ("draft", 32): 0.820, ("review", 32): 1.044, ("change", 32): 1.247, ("check", 32): 0.997,
    ("100 points", 40): 2.161, ("implementation", 34): 2.877, ("honest log", 34): 1.899, ("GitHub = Canvas", 34): 3.266, ("relative", 34): 1.259,
    ("specification", 34): 2.275, ("shader from code", 34): 3.159, ("textures, materials", 34): 3.221, ("the language", 34): 2.256,
    ("verification", 34): 2.036, ("the film", 34): 1.390,
    ("late work", 34): 1.667, ("change a line, predict", 34): 3.828, ("set a uniform, predict a pixel", 34): 5.141,
    ("point to the line that makes data", 34): 5.879, ("no hint: data", 34): 2.327,
    ("audio, video", 32): 1.988, ("earlier take, 14 Oct", 32): 3.173,
    ("authorship", 34): 1.961, ("course A. I. policy", 34): 3.293, ("policy video", 34): 2.158, ("your eyes", 34): 1.685,
}


def a10_w(s, size):
    return A10_W[(s, size)]


def a10_lab(s, x, y, size=34, color=INK):
    return T(s, size, color).move_to([x, y, 0])


def a10_left(s, x, y, size=34, color=INK):
    """A label whose LEFT edge sits at x (from the measured width)."""
    return T(s, size, color).move_to([x + a10_w(s, size) / 2, y, 0])


def a10_img(path, x, y, w=None, h=None):
    im = ImageMobject(path)
    if w is not None:
        im.set_width(w)
    else:
        im.set_height(h)
    return im.move_to([x, y, 0])


def a10_no(x, y, r=0.3, sw=6):
    """A prohibition mark (ink ring + bar), drawn over a picture, never over type."""
    d = r * 0.7071
    return VGroup(Circle(radius=r, stroke_color=INK, stroke_width=sw).move_to([x, y, 0]),
                  Line([x - d, y + d, 0], [x + d, y - d, 0], color=INK, stroke_width=sw))


def a10_code(spec, left, y, size=24, pad=0.3, lh=None):
    """Real code, Menlo, outline frame, real line numbers: spec = [(label, text), ...]. The frame's LEFT edge sits at `left`. Widths from character counts."""
    cw = A10_CW[size]
    lh = lh or size / 32 * 0.46
    nw = max(len(l) for l, _ in spec) * cw + 0.25
    tw = max(len(t.replace("\t", "    ")) for _, t in spec) * cw
    W = tw + nw + 2 * pad
    H = len(spec) * lh + 2 * pad
    x = left + W / 2
    frame = RoundedRectangle(width=W, height=H, corner_radius=0.14, stroke_color=DIM, stroke_width=4, fill_opacity=0).move_to([x, y, 0])
    rows = VGroup()
    for i, (lab, t) in enumerate(spec):
        t = t.replace("\t", "    ")
        yy = y + H / 2 - pad - lh * (i + 0.5)
        n = M(lab, size, DIM).move_to([left + pad + (len(lab) * cw) / 2, yy, 0])
        tx = M(t, size).move_to([left + pad + nw + len(t) * cw / 2, yy, 0])
        rows.add(VGroup(n, tx))
    g = VGroup(frame, rows)
    g.frame, g.rows, g.W, g.H, g.lh, g.x_, g.y_ = frame, rows, W, H, lh, x, y
    g.row_y = lambda i: y + H / 2 - pad - lh * (i + 0.5)
    return g


# ── B69 · one film: the path of what it shows, then the three labels ──────────────────────────────────────────────────────
class B69_OneFilm(Scene):
    def construct(self):
        title = T("Ship It, and How It's Graded", 40).move_to([-3.0, 3.0, 0])
        xs = [-5.0, -2.5, 0.0, 2.5, 5.0]
        py = 0.1
        path = Line([-5.9, py, 0], [5.9, py, 0], color=DIM, stroke_width=5)
        stops = [Circle(radius=0.13, stroke_color=INK, stroke_width=4, fill_color=CARD, fill_opacity=1).move_to([x, py, 0]) for x in xs]
        self.add(title)
        self.play(Create(path), LaggedStart(*[GrowFromCenter(d) for d in stops], lag_ratio=0.15), run_time=0.8)
        ptr = Dot([xs[0], py, 0], radius=0.09, color=TERRA)
        # 1 · your game: the real pad (scripted input)
        icon1 = a10_img("pantry/a10_pad_idle.png", xs[0], 1.55, h=1.5)
        l1 = a10_lab("your game", xs[0], -0.55)
        until(self, "your game", lead=0.15)
        self.play(FadeIn(icon1, shift=DOWN * 0.2), FadeIn(l1), FadeIn(ptr, scale=0.5), run_time=0.45)
        # 2 · the four answers: four ticked circles
        cells = VGroup(*[VGroup(Circle(radius=0.27, stroke_color=INK, stroke_width=4).move_to([xs[1] + dx, 1.55 + dy, 0]),
                                check(xs[1] + dx - 0.02, 1.55 + dy + 0.02, 0.12, INK, 5))
                         for dx, dy in [(-0.34, 0.34), (0.34, 0.34), (-0.34, -0.34), (0.34, -0.34)]])
        l2 = a10_lab("four answers", xs[1], -0.55)
        until(self, "the four answers", lead=0.3)
        self.play(ptr.animate.move_to([xs[1], py, 0]), LaggedStart(*[Create(c) for c in cells], lag_ratio=0.2), FadeIn(l2), run_time=0.6)
        # 3 · captures against predictions: the real pad capture beside a swatch of the predicted colour
        thumb = a10_img("pantry/a10_pad_half.png", xs[2] - 0.45, 1.55, w=1.25)
        pred = swatch((48, 105, 74), xs[2] + 0.62, 1.55, w=0.55, h=0.83)           # predicted dark-stripe pixel at activation 0.5 (controlled-predictions.json)
        l3 = a10_lab("captures", xs[2], -0.55)
        etag = example_tag(x=3.05, y=-3.1)          # the pad capture at activation 0.5 is the example's own (14 Oct)
        until(self, "your captures", lead=0.5)
        self.play(ptr.animate.move_to([xs[2], py, 0]), FadeIn(thumb), FadeIn(pred), FadeIn(l3), FadeIn(etag), run_time=0.5)
        # 4 · tests and mutations: a terminal and a failing cross
        term = terminal_icon(xs[3] - 0.3, 1.55, 0.7)
        cross = cross_mark(xs[3] + 0.75, 1.55, 0.22)
        l4 = a10_lab("tests, mutations", xs[3], -0.55)
        until(self, "the tests", lead=0.35)
        self.play(ptr.animate.move_to([xs[3], py, 0]), FadeIn(term), Create(cross), FadeIn(l4), run_time=0.5)
        # 5 · what no headless run can show: an eye
        eye = eye_icon(xs[4], 1.55, 0.7)
        l5 = a10_lab("the limits", xs[4], -0.55)
        until(self, "what no headless", lead=0.3)
        self.play(ptr.animate.move_to([xs[4], py, 0]), FadeIn(eye), FadeIn(l5), run_time=0.5)
        # the three labels
        w1, w2, w3 = [a10_w(s, 32) + 0.5 for s in ("scripted input", "reconstruction", "held frame")]
        gap = 0.5
        x0 = -(w1 + w2 + w3 + 2 * gap) / 2
        c1 = status_tag("scripted input", x0 + w1 / 2, -2.3)
        c2 = status_tag("reconstruction", x0 + w1 + gap + w2 / 2, -2.3)
        c3 = status_tag("held frame", x0 + w1 + gap + w2 + gap + w3 / 2, -2.3)
        until(self, "Label scripted", lead=0.25)
        self.play(FadeIn(c1, shift=UP * 0.15), run_time=0.3)
        until(self, "reconstructions", lead=0.9)
        self.play(FadeIn(c2, shift=UP * 0.15), run_time=0.3)
        self.play(FadeIn(c3, shift=UP * 0.15), run_time=0.3)
        done(self)


# ── B70 · the repository on GitHub, what goes in and stays out, the commit chain, the tag ─────────────────────────────────
A10_ISO = Iso(2.55, -0.05, 0.62)
A10_ITEMS = ["shaders", "scenes", "driver", "materials", "textures", "tests", "wrapper", "documents, logs"]
A10_SLOTS = [(2.2, 2.2), (1.2, 2.2), (0.2, 2.2), (2.2, 1.2), (1.2, 1.2), (0.2, 1.2), (2.2, 0.2), (1.2, 0.2)]      # back to front; the front corner is left empty


def a10_cube(ix, iy):
    c = A10_ISO.box(ix, iy, 0.02, 0.8, 0.8, 0.8, PAGE_TOP, PAGE_L, PAGE_R, sw=3)
    c.set_z_index(1 + (100 - (ix + iy) * 10) / 1000.0)
    return c


class B70_Repository(Scene):
    def construct(self):
        back, front = A10_ISO.open_box(0, 0, 0, 3.2, 3.2, 0.45)
        gh = logo_chip("github", 5.4, 2.4, h=0.9)
        self.add(back, front)
        self.play(FadeIn(gh, shift=DOWN * 0.2), run_time=0.4)
        # the list, each item dropping a file into the box as it is named
        ys = [2.75 - 0.5 * i for i in range(8)]
        labs = [a10_left(n, -5.75, y, 32) for n, y in zip(A10_ITEMS, ys)]
        ptr = Dot([-6.05, ys[0], 0], radius=0.09, color=TERRA)
        cues = [("shaders", 0.3), ("scenes", 0.25), ("driver", 0.25), ("materials", 0.3), ("textures with", 0.3),
                ("tests", 0.25), ("wrapper", 0.25), ("reviewed documents", 0.3)]
        cubes = []
        for i, ((cue, ld), (ix, iy)) in enumerate(zip(cues, A10_SLOTS)):
            cube = a10_cube(ix, iy)
            cubes.append(cube)
            until(self, cue, lead=ld)
            anims = [FadeIn(labs[i]), FadeIn(cube, shift=DOWN * 1.4)]
            anims.append(FadeIn(ptr, scale=0.5) if i == 0 else ptr.animate.move_to([-6.05, ys[i], 0]))
            self.play(*anims, run_time=0.35)
        # what stays out: four items with a prohibition mark each (cache, credentials, audio or video, a file over 25 MB)
        bx = -2.45
        by = [2.0, 1.0, 0.0, -1.0]
        folder = VGroup(Rectangle(width=0.8, height=0.55, stroke_color=INK, stroke_width=4, fill_opacity=0).move_to([bx, by[0] - 0.05, 0]),
                        Polygon([bx - 0.4, by[0] + 0.22, 0], [bx - 0.4, by[0] + 0.38, 0], [bx - 0.1, by[0] + 0.38, 0], [bx - 0.02, by[0] + 0.22, 0],
                                stroke_color=INK, stroke_width=4, fill_opacity=0))
        key = VGroup(Circle(radius=0.18, stroke_color=INK, stroke_width=4).move_to([bx - 0.25, by[1], 0]),
                     Line([bx - 0.07, by[1], 0], [bx + 0.42, by[1], 0], color=INK, stroke_width=4),
                     Line([bx + 0.28, by[1], 0], [bx + 0.28, by[1] - 0.17, 0], color=INK, stroke_width=4),
                     Line([bx + 0.42, by[1], 0], [bx + 0.42, by[1] - 0.17, 0], color=INK, stroke_width=4))
        media = VGroup(Rectangle(width=1.0, height=0.62, stroke_color=INK, stroke_width=4, fill_opacity=0).move_to([bx, by[2], 0]),
                       Polygon([bx - 0.12, by[2] + 0.17, 0], [bx - 0.12, by[2] - 0.17, 0], [bx + 0.2, by[2], 0], stroke_color=INK, stroke_width=4, fill_opacity=0))
        bigfile = VGroup(Polygon([bx - 0.3, by[3] - 0.42, 0], [bx + 0.3, by[3] - 0.42, 0], [bx + 0.3, by[3] + 0.16, 0], [bx + 0.04, by[3] + 0.42, 0], [bx - 0.3, by[3] + 0.42, 0],
                                 stroke_color=INK, stroke_width=4, fill_opacity=0),
                         Line([bx + 0.04, by[3] + 0.42, 0], [bx + 0.04, by[3] + 0.16, 0], color=INK, stroke_width=4),
                         Line([bx + 0.04, by[3] + 0.16, 0], [bx + 0.3, by[3] + 0.16, 0], color=INK, stroke_width=4))
        nos = [a10_no(bx, y, 0.4) for y in by]
        names = ["cache", "credentials", "audio, video", "over 25 MB"]
        nlabs = [a10_left(n, -1.7, y, 32) for n, y in zip(names, by)]
        for pic, no, lab, cue, ld in zip([folder, key, media, bigfile], nos, nlabs, ["No cache", "no credentials", "no audio or video", "no file over"], [0.4, 0.4, 0.4, 0.3]):
            until(self, cue, lead=ld)
            self.play(FadeIn(pic), Create(no), FadeIn(lab), run_time=0.4)
        # the list and the refusals leave; the commit chain takes the bottom of the frame
        until(self, "Commit in the order", lead=0.55)
        self.play(FadeOut(VGroup(*labs)), FadeOut(ptr), FadeOut(VGroup(folder, key, media, bigfile)), FadeOut(VGroup(*nos)), FadeOut(VGroup(*nlabs)), run_time=0.4)
        cx = [-4.6, -2.9, -1.2, 0.5, 2.2]
        cy = -2.0
        who = ["human", "agent", "human", "agent", "human"]
        names2 = ["shader", "draft", "review", "change", "check"]
        line = Line([cx[0], cy, 0], [cx[-1], cy, 0], color=INK, stroke_width=5)
        nodes = [Circle(radius=0.17, stroke_color=INK, stroke_width=5, fill_color=CARD, fill_opacity=1).move_to([x, cy, 0]) for x in cx]
        chips = [professor_bear("1x1", 0.8, seed=f"B70-{i}", x=x, y=-0.95, shape="circle") if w == "human" else logo_chip("claude", x, -0.95, h=0.8)
                 for i, (x, w) in enumerate(zip(cx, who))]
        labs2 = [a10_lab(n, x, -2.75, 32) for n, x in zip(names2, cx)]
        self.play(Create(line), run_time=0.3)
        for i in range(5):
            self.play(GrowFromCenter(nodes[i]), FadeIn(chips[i], shift=DOWN * 0.15), FadeIn(labs2[i]), run_time=0.3)
        # a reviewer reads along the chain (one terracotta dot), then the tag hangs from the last commit
        rd = Dot([cx[0], cy, 0], radius=0.1, color=TERRA)
        until(self, "a reviewer sees", lead=0.2)
        self.play(FadeIn(rd, scale=0.5), run_time=0.2)
        self.play(rd.animate.move_to([cx[-1], cy, 0]), run_time=1.4)
        until(self, "Tag the final", lead=0.6)
        string = Line([cx[-1] + 0.17, cy + 0.02, 0], [3.3, -1.6, 0], color=INK, stroke_width=4)
        tag = Polygon([3.3, -1.6, 0], [3.65, -1.25, 0], [4.95, -1.25, 0], [4.95, -1.95, 0], [3.65, -1.95, 0],
                      fill_color=BOX_TOP, fill_opacity=1, stroke_color=INK, stroke_width=5)
        hole = Circle(radius=0.08, stroke_color=INK, stroke_width=4).move_to([3.68, -1.6, 0])
        t5 = M("a5", 36).move_to([4.4, -1.6, 0])
        self.play(Create(string), FadeIn(tag), FadeIn(hole), run_time=0.45)
        self.play(FadeIn(t5), run_time=0.25)
        done(self)


# ── B72 · 100 points: 60 / 10 / 10 / 20, then the 60 split 8 / 12 / 14 / 10 / 8 / 8 ───────────────────────────────────────
A10_CX, A10_CW_, A10_NUMX, A10_LBLX = -2.2, 1.6, -0.55, 0.3
A10_SEGS = [(-3.2, 0.38, BAR1, None, "60", "implementation"),
            (0.46, 1.06, BAR2, None, "10", "honest log"),
            (1.14, 1.74, BAR2, None, "10", "GitHub = Canvas"),
            (1.82, 3.01, GHOST, DIM, "20", "relative")]
A10_SPLIT = [("8", "specification"), ("12", "shader from code"), ("14", "textures, materials"), ("10", "the language"), ("8", "verification"), ("8", "the film")]
A10_NUMW = {"60": 0.549, "10": 0.522, "20": 0.559, "8": 0.229, "12": 0.532, "14": 0.538}


def a10_seg(y0, y1, fill, stroke=None):
    r = Rectangle(width=A10_CW_, height=y1 - y0, fill_color=fill, fill_opacity=1, stroke_color=stroke or fill, stroke_width=3 if stroke else 0)
    return r.move_to([A10_CX, (y0 + y1) / 2, 0])


class B72_Rubric(Scene):
    def construct(self):
        top = a10_left("100 points", -6.0, 2.95, 40)
        self.add(top)
        segs = []
        for y0, y1, fill, stroke, num, lbl in A10_SEGS:
            yc = (y0 + y1) / 2
            segs.append((a10_seg(y0, y1, fill, stroke), T(num, 44).move_to([A10_NUMX, yc, 0]), a10_left(lbl, A10_LBLX, yc, 34)))
        for (seg, n, l), cue, ld in zip(segs, ["Sixty for", "ten for your honest", "ten for GitHub", "twenty relative"], [0.1, 0.1, 0.1, 0.35]):
            until(self, cue, lead=ld)
            self.play(GrowFromEdge(seg, DOWN), FadeIn(n), FadeIn(l), run_time=0.5)
        # the sixty becomes the whole column and splits
        until(self, "Of the sixty", lead=0.6)
        seg60 = segs[0][0]
        tall = Rectangle(width=A10_CW_, height=6.2, fill_opacity=0, stroke_color=DIM, stroke_width=4).move_to([A10_CX, -0.1, 0])
        br = Brace(Line([A10_CX - 1.0, -3.2, 0], [A10_CX - 1.0, 3.0, 0]), direction=LEFT, color=INK, buff=0.1)
        b60 = T("60", 52).move_to([A10_CX - 2.0, -0.1, 0])
        rest = [m for part in segs[1:] for m in part] + [segs[0][1], segs[0][2], top]
        self.play(Transform(seg60, tall), *[FadeOut(m) for m in rest], run_time=0.45)
        self.play(GrowFromCenter(br), FadeIn(b60), run_time=0.25)
        gap, u = 0.07, (6.2 - 5 * 0.07) / 60
        top_y = 3.0
        for i, ((num, lbl), cue, ld) in enumerate(zip(A10_SPLIT, ["eight,", "twelve", "fourteen", "ten, eight", "eight", "and eight"], [0.2, 0.3, 0.3, 0.25, 0.1, 0.35])):
            h = int(num) * u
            ya, yb = top_y - h, top_y
            until(self, cue, lead=ld)
            piece = a10_seg(ya, yb, BAR1 if i % 2 == 0 else BAR2)
            nn = T(num, 44).move_to([A10_NUMX, (ya + yb) / 2, 0])
            ll = a10_left(lbl, A10_LBLX, (ya + yb) / 2, 34)
            self.play(GrowFromEdge(piece, UP), FadeIn(nn), FadeIn(ll), run_time=0.3)
            top_y = ya - gap
        done(self)


# ── B73 · late work, and three things you must be able to do, on REAL lines of the example's shaders ───────────────────────
class B73_Explain(Scene):
    def construct(self):
        late = a10_left("late work", -6.0, 3.0, 34)
        cells = VGroup(*[Rectangle(width=0.26, height=0.42, fill_color=BAR2, fill_opacity=1, stroke_width=0).move_to([-3.85 + i * 0.32, 3.0, 0]) for i in range(10)])
        self.add(late, cells)
        until(self, "ten percent", lead=0.3)
        gone = DashedVMobject(Rectangle(width=0.26, height=0.42, color=DIM, stroke_width=4).move_to([-3.85 + 9 * 0.32, 3.0, 0]), num_dashes=10)
        m10 = T("−10%", 44).move_to([0.2, 3.0, 0])
        pd = T("a day", 36).move_to([1.8, 3.0, 0])
        self.play(FadeOut(cells[9], shift=DOWN * 0.5), Create(gone), FadeIn(m10), FadeIn(pd), run_time=0.5)
        tag = example_tag(x=3.05, y=-3.0)
        self.play(FadeIn(tag), run_time=0.3)
        left = -6.35        # frames stay inside the title-safe margin (+-6.4); card 3 is 12.55 wide at pad 0.15
        # card 1: change a line, predict the result
        c1l = a10_left("change a line, predict", -6.2, 2.2, 34)
        c1 = a10_code([("10", "\tALBEDO = mix(base, active_color.rgb, activation);")], left, 1.55, 24, pad=0.15)
        until(self, "change a line", lead=0.45)
        self.play(FadeIn(c1l), Create(c1.frame), FadeIn(c1.rows), run_time=0.5)
        # card 2: set a uniform, predict a pixel
        c2l = a10_left("set a uniform, predict a pixel", -6.2, 0.7, 34)
        c2 = a10_code([("3", "uniform float activation : hint_range(0.0, 1.0) = 0.0;")], left, 0.05, 24, pad=0.15)
        until(self, "set your uniform", lead=0.35)
        self.play(FadeIn(c2l), Create(c2.frame), FadeIn(c2.rows), run_time=0.5)
        # card 3: point to the line that makes a texture read as data (line 4 has no source_color)
        c3l = a10_left("point to the line that makes data", -6.2, -0.8, 34)
        c3 = a10_code([("3", "uniform sampler2D color_map : source_color, filter_nearest;"),
                       ("4", "uniform sampler2D roughness_map : filter_nearest;")], left, -1.78, 24, pad=0.15, lh=0.5)
        until(self, "point to the line", lead=0.35)
        self.play(FadeIn(c3l), Create(c3.frame), FadeIn(c3.rows), run_time=0.5)
        until(self, "makes a texture", lead=0.2)
        r4 = RoundedRectangle(width=c3.W - 0.3, height=c3.lh - 0.12, corner_radius=0.1, stroke_color=TERRA, stroke_width=6, fill_opacity=0).move_to([c3.x_, c3.row_y(1), 0])
        nh = a10_left("no hint: data", -5.9, -2.85, 34)
        self.play(Create(r4), FadeIn(nh), run_time=0.45)
        done(self)


# ── B74 · two misrepresentations, the course policy, then the real lab panel ──────────────────────────────────────────────
class B74_Integrity(Scene):
    def construct(self):
        def seal(x, y, inner):
            outer = Circle(radius=1.0, stroke_color=INK, stroke_width=5).move_to([x, y, 0])
            ring2 = Circle(radius=0.85, stroke_color=DIM, stroke_width=3).move_to([x, y, 0])
            return VGroup(outer, ring2, inner)
        # authorship: a page with three lines; verification: a tick
        page = VGroup(Rectangle(width=0.7, height=0.9, stroke_color=INK, stroke_width=4, fill_opacity=0).move_to([-3.2, 0.7, 0]),
                      *[Line([-3.45, 0.7 + dy, 0], [-2.95, 0.7 + dy, 0], color=DIM, stroke_width=4) for dy in (0.22, 0.02, -0.18)])
        s1 = seal(-3.2, 0.7, page)
        s2 = seal(3.2, 0.7, check(3.2, 0.7, 0.35, INK, 9))
        l1 = a10_lab("authorship", -3.2, -0.85)
        l2 = a10_lab("verification", 3.2, -0.85)
        until(self, "hand-written", lead=1.2)
        self.play(FadeIn(s1, scale=1.25), FadeIn(l1), run_time=0.5)
        r1 = ring(s1[0], pad=0.18)
        self.play(FadeIn(r1), run_time=0.3)
        until(self, "misrepresents verification", lead=1.8)
        self.play(FadeIn(s2, scale=1.25), FadeIn(l2), run_time=0.5)
        r2 = ring(s2[0], pad=0.18)
        self.play(FadeIn(r2), run_time=0.3)
        # both break the course policy: one brace over both, then the policy video as a play button
        until(self, "Both break", lead=0.2)
        brc = Brace(Line([-4.6, 1.95, 0], [4.6, 1.95, 0]), direction=UP, color=INK, buff=0.05)
        pol = a10_lab("course A. I. policy", 0.0, 2.95)
        self.play(GrowFromCenter(brc), FadeIn(pol), run_time=0.5)
        until(self, "watch its video", lead=0.3)
        vid = RoundedRectangle(width=1.5, height=1.0, corner_radius=0.18, stroke_color=INK, stroke_width=5, fill_opacity=0).move_to([0.0, -1.55, 0])
        play = Polygon([-0.2, -1.2, 0], [-0.2, -1.9, 0], [0.4, -1.55, 0], stroke_color=INK, stroke_width=5, fill_opacity=0)
        vl = a10_lab("policy video", 0.0, -2.6)
        self.play(Create(vid), Create(play), FadeIn(vl), run_time=0.5)
        # a passing run proves it is wired; your eyes decide how it looks: the real lab panel (scripted input)
        until(self, "A passing run", lead=0.45)
        gone = VGroup(s1, s2, l1, l2, r1, r2, brc, pol, vid, play, vl)
        panel = a10_img("pantry/a10_lab_panel.png", -1.25, 0.0, w=7.6)
        pf = framed(panel, color=DIM, pad=0.1, sw=4)
        w_a, w_b = a10_w("scripted input", 32) + 0.5, a10_w("earlier take, 14 Oct", 32) + 0.5
        x_a = -1.25 - (w_a + w_b + 0.4) / 2 + w_a / 2
        x_b = -1.25 - (w_a + w_b + 0.4) / 2 + w_a + 0.4 + w_b / 2
        stag = VGroup(status_tag("scripted input", x_a, -2.65), status_tag("earlier take, 14 Oct", x_b, -2.65))
        self.play(FadeOut(gone), FadeIn(pf), FadeIn(stag), run_time=0.45)
        # ring ONLY the line that is in both takes of the panel script: "Render and play still need checking."
        yb = A10_PANEL_ROWS[5]
        px0, px1 = -1.25 - 4.2, -1.25 + 4.2       # 8.4 wide x 0.5 tall: aspect 16.8 (the stroke adds to the bbox)
        until(self, "Your eyes", lead=0.5)
        r_b = RoundedRectangle(width=px1 - px0, height=0.5, corner_radius=0.1, stroke_color=TERRA, stroke_width=6, fill_opacity=0).move_to([-1.25, yb, 0])
        eye = eye_icon(5.0, 0.3, 0.6)
        el = a10_lab("your eyes", 5.0, -0.5)
        self.play(Create(r_b), FadeIn(eye), FadeIn(el), run_time=0.45)
        done(self)


# centres of the six text rows of pantry/a10_lab_panel.png (crop of lab_000609, 1104 x 604 px; row centres 72, 172, 264.5, 350.5, 451, 544 px from its top)
# shown 7.6 units wide (0.006884 units per pixel), centred at y 0: row y = 2.079 - px * 0.006884
A10_PANEL_ROWS = [2.079 - r * 0.006884 for r in (72, 172, 264.5, 350.5, 451, 544)]
