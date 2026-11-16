"""ACT VI · Textures Are Information  (B40-B47 Manim; B48 is a Remotion CCPlainShell, see lanes/act6.json)

One cast for the act: the REAL 3 x 1 grey file (three texels 64 / 128 / 192, captures/forward-plus/gray-three-band.png) and the REAL two-row
hint fixture captures (pantry/ev_hint_*.png: top row source_color, bottom row data), then the Poly Haven stone-floor pair and the code-made map.
Everything on screen is read from the evidence:
  hint numbers ..... captures/forward-plus/hint_forward_plus.json and hint_compatibility.json (RGB8, re-run for this film, 16 Oct), and
                     evidence/example/hint-samples.json (the example's own capture, 14 Oct; floats x 255); the predicted 137/188/225 is the assignment's
                     encode(x) (evidence/act6/verify_act6_numbers.py)
  curl numbers ..... evidence/runs/R3-normal-calibration.json (stride 2, Poly Haven stone_floor GL / DX pair), evidence/runs/R1-baseline-60fps.log (code-made map)
  the audit ........ evidence/example/sources/MATERIALS.md and test-material-contract.gd (5 + 24 + 24 = 53)
  code lines ....... evidence/example/sources/hint.gdshader (lines 3, 4, 5, 9: the tab on line 9 is drawn as four spaces)
B44 is a DRAWING of an idea (a height surface, its slope arrows, a 0 / 1 / 2 number line): it is labelled "illustration" and nothing in it is measured.
Pacing: until() cues come from the character share of each narration (no audio exists yet); the build session re-checks [pace].
"""

A6P = "pantry/"


def a6_img(name, w=None, h=None, at=(0.0, 0.0)):
    im = ImageMobject(A6P + name)
    if w is not None:
        im.set_width(w)
    if h is not None:
        im.set_height(h)
    im.move_to(np.array([at[0], at[1], 0.0]))
    return im


def a6_lab(s, x, y, size=34, color=INK):
    return T(s, size, color).move_to([x, y, 0])


def a6_labl(s, x, y, size=34, color=INK):
    """A label whose LEFT edge sits at x."""
    return T(s, size, color).move_to([x, y, 0], aligned_edge=LEFT)


def a6_grey(v):
    return "#%02x%02x%02x" % (v, v, v)


def a6_cells(x, y, cw, gap=0.08):
    """The REAL 3 x 1 file: three texels 64 / 128 / 192 (captures/forward-plus/gray-three-band.png), drawn as three cells."""
    g = VGroup()
    for i, v in enumerate((64, 128, 192)):
        g.add(Rectangle(width=cw, height=cw, fill_color=a6_grey(v), fill_opacity=1, stroke_color=DIM, stroke_width=3)
              .move_to([x + (i - 1) * (cw + gap), y, 0]))
    return g


def a6_tri(vals, x, y, dx=1.3, size=44):
    """Three numbers in a row (real measured / computed values)."""
    return VGroup(*[T(str(v), size).move_to([x + (i - 1) * dx, y, 0]) for i, v in enumerate(vals)])


def a6_eq(x, y, w=0.9, gap=0.2, color=INK, sw=8):
    return VGroup(Line([x - w / 2, y + gap / 2, 0], [x + w / 2, y + gap / 2, 0], color=color, stroke_width=sw),
                  Line([x - w / 2, y - gap / 2, 0], [x + w / 2, y - gap / 2, 0], color=color, stroke_width=sw))


def a6_neq(x, y, w=0.9, gap=0.2, color=INK, sw=8):
    slash = Line([x - 0.2, y - 0.38, 0], [x + 0.2, y + 0.38, 0], color=color, stroke_width=sw)
    return VGroup(a6_eq(x, y, w, gap, color, sw), slash)


def a6_code(lines, x=0.0, y=0.0, size=20, first=1, lh=0.62, pad=0.3):
    """code_block with a wider row pitch (lh) so labels and arrows can sit at single rows. REAL code, Menlo, real line numbers (first=), outline-only frame.
    Same interface as the kit's code_block: .rows, .frame, .W, .H, .row(n), .ring_line(n).
    Text is placed LEFT-aligned at an explicit x (Pango drops leading spaces from a Text's width, so a centred placement would lose the indent; and the static
    check's stub guesses text width too wide): indent = leading whitespace (a tab = 4 spaces) x the measured Menlo advance (0.0074 units per size point)."""
    ns = [str(first + i) for i in range(len(lines))]
    cw = 0.00744 * size                           # measured: Menlo 20 -> 0.1488 units per character (58 chars = 8.63 units)
    nw = max(len(n) for n in ns) * cw + 0.25
    exp = [ln.replace("\t", "    ") for ln in lines]
    tw = max(len(e) for e in exp) * cw
    W = tw + nw + 2 * pad
    H = len(lines) * lh + 2 * pad
    frame = RoundedRectangle(width=W, height=H, corner_radius=0.14, stroke_color=DIM, stroke_width=4, fill_opacity=0).move_to([x, y, 0])
    left = x - W / 2 + pad
    rows = VGroup()
    for i, e in enumerate(exp):
        yy = y + H / 2 - pad - lh * (i + 0.5)
        indent = (len(e) - len(e.lstrip(" "))) * cw
        n = M(ns[i], size, DIM).move_to([left, yy, 0], aligned_edge=LEFT)
        t = M(e.lstrip(" ") or " ", size).move_to([left + nw + indent, yy, 0], aligned_edge=LEFT)
        rows.add(VGroup(n, t))
    g = VGroup(frame, rows)
    g.frame, g.rows, g.W, g.H, g.lh, g.first = frame, rows, W, H, lh, first
    g.row = lambda n: rows[n - first]
    ys = [y + H / 2 - pad - lh * (i + 0.5) for i in range(len(lines))]
    g.row_y = lambda n: ys[n - first]

    def _ring_line(n, color=TERRA):
        return RoundedRectangle(width=W - 0.16, height=lh * 0.98, corner_radius=0.1, stroke_color=color, stroke_width=6, fill_opacity=0).move_to([x, ys[n - first], 0])
    g.ring_line = _ring_line
    return g


def a6_brackets(cx, cy, w, h, arm=0.34, sw=7, color=TERRA):
    """Four terracotta corner brackets round a region (a viewfinder). A full terracotta ring is one big outline blob that GATE T's accent-text check reads as
    terracotta type; four separate L marks are not."""
    out = VGroup()
    for sx, sy in ((-1, 1), (1, 1), (-1, -1), (1, -1)):
        x0, y0 = cx + sx * w / 2, cy + sy * h / 2
        out.add(VMobject(stroke_color=color, stroke_width=sw).set_points_as_corners([[x0 - sx * arm, y0, 0], [x0, y0, 0], [x0, y0 - sy * arm, 0]]))
    return out


def a6_toggle(x, y, on=True):
    pill_ = RoundedRectangle(width=0.84, height=0.42, corner_radius=0.21, fill_opacity=0, stroke_color=INK, stroke_width=4).move_to([x, y, 0])
    knob = Circle(radius=0.13, fill_color=DIM if not on else INK, fill_opacity=1, stroke_width=0).move_to([x + (0.2 if on else -0.2), y, 0])
    return VGroup(pill_, knob)


HINT_LINES = {3: "uniform sampler2D as_color : source_color, filter_nearest;",
              4: "uniform sampler2D as_data : filter_nearest;",
              5: "uniform bool use_color = true;",
              9: "\tALBEDO = use_color ? texture(as_color, UV).rgb : texture(as_data, UV).rgb;"}


# ── B40 · the hint experiment's build: the file, the script, one shader that binds it twice ───────────────────────
class B40_HintBuild(Scene):
    def construct(self):
        title = T("Textures Are Information", 40).move_to([-6.15, 2.95, 0], aligned_edge=LEFT)
        self.add(title)
        # stage 1: a script writes the real 3 x 1 file (64 / 128 / 192); the assignment's import; the example built it in memory
        script = terminal_icon(-4.3, 0.55, s=0.8)
        script_l = a6_lab("script", -4.3, -0.35, 34)
        wr = arrow([-3.25, 0.55, 0], [-1.85, 0.55, 0])
        file = a6_cells(0.4, 0.55, 1.2)
        nums = VGroup(*[T(str(v), 44).move_to([0.4 + (i - 1) * 1.28, -0.5, 0]) for i, v in enumerate((64, 128, 192))])
        self.wait(0.3)
        self.play(FadeIn(script, shift=RIGHT * 0.2), FadeIn(script_l), GrowArrow(wr), run_time=0.5)
        until(self, "three-by-one", lead=0.4)
        self.play(LaggedStart(*[GrowFromCenter(c) for c in file], lag_ratio=0.3), run_time=0.8)
        self.play(FadeIn(nums), run_time=0.3)
        tag1 = status_tag("assignment: lossless, no mipmaps", 0.4, -1.55)
        tag2 = status_tag("example: built in memory", 0.4, -2.3)
        until(self, "imported lossless", lead=0.55)
        self.play(FadeIn(tag1, shift=UP * 0.15), run_time=0.4)
        self.play(FadeIn(tag2, shift=UP * 0.15), run_time=0.4)
        # stage 2 (after the midpoint): the file shrinks into the corner, the real shader lines land, the file fans out to both samplers
        until(self, "One shader binds", lead=0.45)
        blockA = a6_code([HINT_LINES[3], HINT_LINES[4], HINT_LINES[5]], x=1.55, y=0.45, size=20, first=3, lh=0.62, pad=0.3)
        self.play(FadeOut(script), FadeOut(script_l), FadeOut(wr), FadeOut(nums), FadeOut(tag1), FadeOut(tag2),
                  file.animate.scale(0.5833).move_to([-4.85, 2.05, 0]), FadeIn(blockA), run_time=0.7)
        nlab = T("64 · 128 · 192", 36).move_to([-1.5, 2.05, 0])
        ex = example_tag(3.0, 2.95)
        self.play(FadeIn(nlab), FadeIn(ex), run_time=0.4)
        y3, y4, y5 = blockA.row_y(3), blockA.row_y(4), blockA.row_y(5)
        until(self, "binds it twice", lead=0.3)
        a_c = arrow([-4.6, 1.62, 0], [-3.42, y3, 0], w=5, tip=0.2)
        a_d = arrow([-4.6, 1.62, 0], [-3.42, y4, 0], w=5, tip=0.2)
        self.play(GrowArrow(a_c), GrowArrow(a_d), run_time=0.5)
        until(self, "with source color", lead=0.55)
        r3 = blockA.ring_line(3)
        self.play(Create(r3), run_time=0.4)
        until(self, "and without", lead=0.45)
        r4 = blockA.ring_line(4)
        self.play(FadeOut(r3), Create(r4), run_time=0.4)
        until(self, "a boolean picks", lead=0.75)
        r5 = blockA.ring_line(5)
        tg = a6_toggle(-4.85, y5, on=True)
        t_on = M("as_color", 28).move_to([-4.85, y5 - 0.62, 0])
        a_t = arrow([-4.25, y5, 0], [-3.42, y5, 0], w=5, tip=0.2)
        self.play(FadeOut(r4), Create(r5), FadeIn(tg), FadeIn(t_on), GrowArrow(a_t), run_time=0.4)
        until(self, "which writes", lead=1.25)
        blockB = a6_code([HINT_LINES[9]], x=0.0, y=-2.45, size=20, first=9, lh=0.62, pad=0.3)
        r9 = blockB.ring_line(9)
        t_off = M("as_data", 28).move_to([-4.85, y5 - 0.62, 0])
        knob = tg[1]
        # the switch flips (the knob slides, grey = off) and its caption cross-fades from the colour sampler to the data sampler
        self.play(FadeOut(r5), FadeIn(blockB), Create(r9), knob.animate.move_to([-4.85 - 0.2, y5, 0]).set_fill(DIM), FadeOut(t_on), FadeIn(t_off), run_time=0.5)
        done(self)


# ── B41 · Compatibility result: both rows read 64 / 128 / 192 (the example's own capture, 14 Oct) ─────────────────────
class B41_CompatResult(Scene):
    def construct(self):
        # the example's REAL capture (Compatibility, 3840 x 2160 SubViewport, cropped): top row source_color, bottom row data
        im = a6_img("ev_hint_compat_example.png", w=6.9, at=(-2.3, -0.5))
        pic = framed(im)
        self.play(FadeIn(pic), run_time=0.5)
        yt, yb = 1.0, -2.0                       # band-row centres of the picture (same y as the numbers beside it)
        xs = [-4.6, -2.3, 0.0]                   # band-column centres
        col_x = [2.8, 4.1, 5.4]
        lab1 = a6_lab("colour read", 4.1, yt - 0.58, 34)
        lab2 = a6_lab("data read", 4.1, yb + 0.58, 34)
        until(self, "on two quads", lead=0.45)
        self.play(FadeIn(lab1), FadeIn(lab2), run_time=0.4)
        tag = status_tag("the example, 14 Oct", 4.1, 1.9)
        until(self, "In the example", lead=0.35)
        self.play(FadeIn(tag, shift=UP * 0.15), run_time=0.35)
        head = a6_lab("Compatibility", 4.1, 3.0, 46)
        ver = a6_lab("Godot 4.7.2", 4.1, 2.45, 32, DIM)
        until(self, "on Compatibility", lead=0.35)
        self.play(FadeIn(head), FadeIn(ver), run_time=0.4)
        vals = [64, 128, 192]
        for i, ph, ld in [(0, "sixty-four", 0.3), (1, "one twenty-eight", 0.3), (2, "one ninety-two", 0.3)]:
            until(self, ph, lead=ld)
            dots = VGroup(Dot([xs[i], yt, 0], radius=0.13, color=TERRA), Dot([xs[i], yb, 0], radius=0.13, color=TERRA))
            n1 = T(str(vals[i]), 44).move_to([col_x[i], yt, 0])
            n2 = T(str(vals[i]), 44).move_to([col_x[i], yb, 0])
            self.play(FadeIn(dots, scale=0.5), FadeIn(n1), FadeIn(n2), run_time=0.35)
        until(self, "This renderer", lead=0.35)
        eq = a6_eq(4.1, -0.5)
        self.play(Create(eq), run_time=0.5)
        done(self)


# ── B42 · Forward+ result: the data row brightens to 137 / 188 / 225, as the assignment's formula predicts ───────────────
class B42_ForwardResult(Scene):
    def construct(self):
        yt, yb = 1.0, -2.0
        xs = [-4.6, -2.3, 0.0]
        col_x = [2.8, 4.1, 5.4]
        compat = a6_img("ev_hint_compat.png", w=6.9, at=(-2.3, -0.5))
        fp_im = a6_img("ev_hint_fp.png", w=6.9, at=(-2.3, -0.5))
        frame_ = Rectangle(width=6.9 + 0.12, height=compat.height + 0.12, stroke_color=DIM, stroke_width=4, fill_opacity=0).move_to([-2.3, -0.5, 0])
        head_c = a6_lab("Compatibility", 4.1, 3.0, 46)
        ver = a6_lab("Godot 4.7.2", 4.1, 2.45, 32, DIM)
        tag = status_tag("re-run for this film", 4.1, 1.9)
        self.add(compat, frame_, head_c, ver, tag)
        lab1 = a6_lab("colour read", 4.1, yt - 0.58, 34)
        lab2 = a6_lab("data read", 4.1, yb + 0.58, 34)
        # the same fixture, run again on Forward+: the picture cross-fades and only the bottom row brightens
        until(self, "Forward Plus", lead=0.5)
        head_f = a6_lab("Forward+", 4.1, 3.0, 46)
        self.play(FadeIn(fp_im), FadeOut(head_c), FadeIn(head_f), FadeIn(lab1), FadeIn(lab2), run_time=0.9)
        self.remove(compat)
        # the colour read keeps 64 / 128 / 192
        until(self, "sixty-four", lead=0.35)
        n_top = a6_tri([64, 128, 192], 4.1, yt, dx=1.3)
        d_top = VGroup(*[Dot([xs[i], yt, 0], radius=0.13, color=TERRA) for i in range(3)])
        self.play(FadeIn(n_top), FadeIn(d_top, scale=0.5), run_time=0.45)
        # after the midpoint: the data row is ringed, then its three numbers land
        until(self, "The data read", lead=0.35)
        rg = a6_brackets(-2.3, yb, 6.9 + 0.2, 1.72 + 0.2)
        ne = a6_neq(4.1, -0.5)
        self.play(Create(rg), Create(ne), run_time=0.5)
        vals = [137, 188, 225]
        n_bot = []
        for i, ph, ld in [(0, "one thirty-seven", 0.3), (1, "one eighty-eight", 0.3), (2, "two twenty-five", 0.3)]:
            until(self, ph, lead=ld)
            d = Dot([xs[i], yb, 0], radius=0.13, color=TERRA)
            n = T(str(vals[i]), 44).move_to([col_x[i], yb, 0])
            n_bot.append(n)
            self.play(FadeIn(d, scale=0.5), FadeIn(n), run_time=0.35)
        until(self, "as predicted", lead=0.85)
        ok = tick_mark(3.0, -2.85, s=0.25)
        pr = a6_labl("as predicted", 3.4, -2.85, 36)
        self.play(Create(ok), FadeIn(pr), run_time=0.35)
        done(self)


# ── B43 · one file, two readings, two renderers: four triples of real numbers ─────────────────────────────────────────
class B43_OneFileTwoReads(Scene):
    def construct(self):
        cx = [-0.4, 3.8]
        y1, y2, y3 = 0.85, -0.45, -1.85
        fx, fy = 1.7, 2.2
        file = a6_cells(fx, fy, 0.8, gap=0.07)
        flab = a6_lab("one file", -0.5, fy, 40)
        self.wait(0.3)
        self.play(LaggedStart(*[GrowFromCenter(c) for c in file], lag_ratio=0.3), run_time=0.8)
        until(self, "One file", lead=0.3)
        self.play(FadeIn(flab, shift=RIGHT * 0.15), run_time=0.35)
        b1 = box(cx[0], y1, 3.1, 0.9, color=INK, sw=4)
        b2 = box(cx[1], y1, 3.1, 0.9, color=INK, sw=4)
        t1 = a6_lab("colour read", cx[0], y1, 36)
        t2 = a6_lab("data read", cx[1], y1, 36)
        arr1 = arrow([fx - 0.5, fy - 0.55, 0], [cx[0] + 0.5, y1 + 0.5, 0], w=5, tip=0.2)
        arr2 = arrow([fx + 0.5, fy - 0.55, 0], [cx[1] - 0.5, y1 + 0.5, 0], w=5, tip=0.2)
        until(self, "read two ways", lead=0.5)
        self.play(Create(b1), Create(b2), FadeIn(t1), FadeIn(t2), GrowArrow(arr1), GrowArrow(arr2), run_time=0.7)
        # Forward+: colour read 64 / 128 / 192, data read 137 / 188 / 225 (hint_forward_plus.json)
        lab_f = a6_labl("Forward+", -5.7, y2, 40)
        lab_c = a6_labl("Compatibility", -5.7, y3, 40)
        f_col = a6_tri([64, 128, 192], cx[0], y2, dx=1.05, size=48)
        f_dat = a6_tri([137, 188, 225], cx[1], y2, dx=1.05, size=48)
        until(self, "two sets of numbers", lead=0.9)
        self.play(FadeIn(lab_f), FadeIn(lab_c), run_time=0.3)
        self.play(FadeIn(f_col, shift=DOWN * 0.15), FadeIn(f_dat, shift=DOWN * 0.15), run_time=0.45)
        # Compatibility: both reads 64 / 128 / 192 (hint_compatibility.json); ≠ in Forward+, = in Compatibility
        c_col = a6_tri([64, 128, 192], cx[0], y3, dx=1.05, size=48)
        c_dat = a6_tri([64, 128, 192], cx[1], y3, dx=1.05, size=48)
        until(self, "Which is right", lead=0.2)
        self.play(FadeIn(c_col, shift=DOWN * 0.15), FadeIn(c_dat, shift=DOWN * 0.15), run_time=0.5)
        until(self, "what the numbers mean", lead=0.45)
        ne = a6_neq(1.7, y2, w=0.7, gap=0.17, sw=7)
        eq = a6_eq(1.7, y3, w=0.7, gap=0.17, sw=7)
        self.play(Create(ne), Create(eq), run_time=0.5)
        until(self, "the renderer you name", lead=0.55)
        rg = a6_brackets(-4.2, (y2 + y3) / 2, 3.9, 2.7, arm=0.34)
        tg = status_tag("re-run for this film", 0.0, -3.0)
        self.play(Create(rg), FadeIn(tg), run_time=0.5)
        done(self)


# ── B44 · the curl check, drawn (an illustration: a hill, its slope arrows, a 0 / 1 / 2 number line; nothing measured) ────
def a6_field(kind, cx, cy):
    """4 x 3 slope arrows over one panel. 'real': slopes of a hill (curl-free); 'wrong': the same with the second component flipped; 'none': random."""
    rng = np.random.RandomState(44)
    arrows = VGroup()
    pts = [((i - 1.5) * 0.8, (j - 1) * 0.78) for j in range(3) for i in range(4)]
    for (px, py) in pts:
        if kind == "none":
            ang = rng.uniform(0, 2 * np.pi)
            L = 0.5
            vx, vy = L * np.cos(ang), L * np.sin(ang)
        else:
            r2 = px * px + py * py
            g = np.exp(-r2 / (2 * 0.8 ** 2))
            vx, vy = px * g, py * g
            n = np.hypot(vx, vy)
            if n < 1e-6:
                continue
            L = 0.36 + 0.2 * min(1.0, n / 0.6)
            vx, vy = vx / n * L, vy / n * L
            if kind == "wrong":
                vy = -vy
        a = Arrow(np.array([cx + px - vx / 2, cy + py - vy / 2, 0.0]), np.array([cx + px + vx / 2, cy + py + vy / 2, 0.0]), buff=0, color=INK,
                  stroke_width=5, tip_length=0.2, max_tip_length_to_length_ratio=0.5)
        arrows.add(a)
    return arrows


def a6_contours(cx, cy):
    return VGroup(*[Ellipse(width=2 * r * 1.45, height=2 * r * 1.05, stroke_color=GHOST, stroke_width=4, fill_opacity=0).move_to([cx, cy, 0]) for r in (0.35, 0.72, 1.1)])


class B44_CurlCheck(Scene):
    def construct(self):
        px = [-4.2, 0.0, 4.2]
        py = 0.95
        panels = [RoundedRectangle(width=3.5, height=2.6, corner_radius=0.14, stroke_color=DIM, stroke_width=4, fill_opacity=0).move_to([x, py, 0]) for x in px]
        ill = status_tag("illustration", 5.0, 2.95)
        # the number line (0 / 1 / 2) is there from the start; the dot rides it later
        ly = -1.85
        line = Line([-5.4, ly, 0], [5.4, ly, 0], color=INK, stroke_width=5)
        ticks = VGroup(*[Line([x, ly - 0.15, 0], [x, ly + 0.15, 0], color=INK, stroke_width=5) for x in px])
        nums = VGroup(*[T(s, 44).move_to([x, -2.45, 0]) for s, x in zip(("0", "1", "2"), px)])
        cl = a6_lab("curl ratio", 0.0, -3.05, 34)
        self.add(ill)
        until(self, "A real map", lead=0.5)
        # panel 1: a real surface in the right convention
        c1 = a6_contours(px[0], py)
        f1 = a6_field("real", px[0], py)
        lab1 = a6_lab("right convention", px[0], -0.75, 32)
        self.play(Create(panels[0]), Create(c1), run_time=0.6)
        self.play(LaggedStart(*[Create(a) for a in f1], lag_ratio=0.06), FadeIn(lab1), run_time=0.9)
        # "no curl": a small circulating arrow with a bar through it, above the real panel
        until(self, "no curl", lead=0.3)
        swirl = Arc(radius=0.27, start_angle=0.7, angle=4.5, color=INK, stroke_width=5).move_to([-4.9, 2.75, 0])
        swirl.add_tip(tip_length=0.15)
        bar_ = Line([-5.2, 3.05, 0], [-4.6, 2.45, 0], color=INK, stroke_width=6)
        l_nc = a6_labl("no curl", -4.4, 2.75, 32)
        self.play(Create(swirl), Create(bar_), FadeIn(l_nc), run_time=0.4)
        until(self, "an imitation", lead=0.45)
        c2_f = a6_field("none", px[1], py)
        lab2 = a6_lab("no surface", px[1], -0.75, 32)
        self.play(Create(panels[1]), run_time=0.4)
        self.play(LaggedStart(*[Create(a) for a in c2_f], lag_ratio=0.06), FadeIn(lab2), run_time=0.9)
        # number line: the ratio lands near 0 (right convention), near 1 (no surface), near 2 (wrong convention)
        until(self, "The ratio", lead=0.3)
        self.play(Create(line), Create(ticks), FadeIn(nums), FadeIn(cl), run_time=0.6)
        dot = Dot([px[0], ly, 0], radius=0.17, color=TERRA)
        until(self, "near zero", lead=0.3)
        self.play(FadeIn(dot, scale=0.5), run_time=0.35)
        until(self, "near one", lead=0.45)
        self.play(dot.animate.move_to([px[1], ly, 0]), run_time=0.5)
        c3 = a6_contours(px[2], py)
        f3 = a6_field("wrong", px[2], py)
        lab3 = a6_lab("wrong convention", px[2], -0.75, 32)
        until(self, "near two", lead=0.95)
        self.play(dot.animate.move_to([px[2], ly, 0]), Create(panels[2]), Create(c3), run_time=0.5)
        self.play(LaggedStart(*[Create(a) for a in f3], lag_ratio=0.06), FadeIn(lab3), run_time=0.7)
        done(self)


# ── B45 · calibrate on the Poly Haven stone-floor pair: 0.484 / 1.516, not 0 and 2 ───────────────────────────────────
class B45_Calibrate(Scene):
    def construct(self):
        gl = a6_img("ev_normal_gl.png", h=2.5, at=(-4.8, 1.3))
        dx = a6_img("ev_normal_dx.png", h=2.5, at=(-1.9, 1.3))
        pg, pd = framed(gl), framed(dx)
        l_gl = a6_lab("OpenGL", -4.8, 2.95, 36)
        l_dx = a6_lab("DirectX", -1.9, 2.95, 36)
        until(self, "OpenGL and DirectX", lead=0.5)
        self.play(FadeIn(pg), FadeIn(l_gl), run_time=0.4)
        self.play(FadeIn(pd), FadeIn(l_dx), run_time=0.4)
        until(self, "Poly Haven", lead=0.4)
        c1 = chip("Stone Floor · Poly Haven", 3.65, 2.35, size=32)
        c2 = chip("Dimitrios Savva · CC0", 3.65, 1.5, size=32)
        ex = example_tag(3.2, 0.7)
        self.play(FadeIn(c1, shift=LEFT * 0.2), FadeIn(c2, shift=LEFT * 0.2), FadeIn(ex), run_time=0.5)
        # two number lines: the OpenGL file (top), the DirectX file (bottom); x = 0 -> -4.8, x = 2 -> +4.8
        def X(v):
            return -4.8 + v * 4.8
        y_a, y_b = -1.55, -2.55
        la = Line([X(0), y_a, 0], [X(2), y_a, 0], color=INK, stroke_width=5)
        lb = Line([X(0), y_b, 0], [X(2), y_b, 0], color=INK, stroke_width=5)
        tks = VGroup(*[Line([X(v), y_b - 0.14, 0], [X(v), y_b + 0.14, 0], color=INK, stroke_width=5) for v in (0, 1, 2)],
                     *[Line([X(v), y_a - 0.14, 0], [X(v), y_a + 0.14, 0], color=INK, stroke_width=5) for v in (0, 2)])
        nums = VGroup(*[T(str(v), 36).move_to([X(v), y_b - 0.5, 0]) for v in (0, 1, 2)])
        th_a = a6_img("ev_normal_gl.png", h=0.62, at=(-5.65, y_a))
        th_b = a6_img("ev_normal_dx.png", h=0.62, at=(-5.65, y_b))
        until(self, "same material", lead=0.45)
        self.play(Create(la), Create(lb), Create(tks), FadeIn(nums), FadeIn(th_a), FadeIn(th_b), run_time=0.6)
        v1, v2 = 0.484, 1.516                      # 0.48445 and 1.51555 (evidence/runs/R3-normal-calibration.json), shown to 3 places
        d_a1 = Dot([X(v1), y_a, 0], radius=0.17, color=TERRA)
        d_a2 = Dot([X(v2), y_a, 0], radius=0.17, color=TERRA)
        n_a1 = T("0.484", 40).move_to([X(v1), y_a + 0.55, 0])
        n_a2 = T("1.516", 40).move_to([X(v2), y_a + 0.55, 0])
        s_a1 = a6_lab("read as OpenGL", X(v1), y_a + 1.0, 30)
        s_a2 = a6_lab("read as DirectX", X(v2), y_a + 1.0, 30)
        until(self, "point four eight", lead=0.5)
        self.play(FadeIn(d_a1, scale=0.5), FadeIn(n_a1), FadeIn(s_a1), run_time=0.4)
        until(self, "one point five two", lead=0.55)
        self.play(FadeIn(d_a2, scale=0.5), FadeIn(n_a2), FadeIn(s_a2), run_time=0.4)
        # not zero and two: open circles at the ideal ends
        until(self, "Not zero and two", lead=0.4)
        g0 = open_circle(X(0), y_a, r=0.2, color=DIM, w=5)
        g2 = open_circle(X(2), y_a, r=0.2, color=DIM, w=5)
        gap0 = DashedLine([X(0) + 0.25, y_a, 0], [X(v1) - 0.22, y_a, 0], color=DIM, stroke_width=4, dash_length=0.12)
        gap2 = DashedLine([X(v2) + 0.22, y_a, 0], [X(2) - 0.25, y_a, 0], color=DIM, stroke_width=4, dash_length=0.12)
        self.play(Create(g0), Create(g2), Create(gap0), Create(gap2), run_time=0.5)
        # the DirectX file gives the mirror pair: the threshold is set from the pair
        until(self, "Set the threshold", lead=0.45)
        d_b1 = Dot([X(v2), y_b, 0], radius=0.17, color=TERRA)
        d_b2 = Dot([X(v1), y_b, 0], radius=0.17, color=TERRA)
        n_b1 = T("1.516", 40).move_to([X(v2), y_b + 0.5, 0])
        n_b2 = T("0.484", 40).move_to([X(v1), y_b + 0.5, 0])
        self.play(FadeIn(d_b1, scale=0.5), FadeIn(d_b2, scale=0.5), FadeIn(n_b1), FadeIn(n_b2), run_time=0.5)
        done(self)


# ── B46 · the code-made map (0.054 / 1.946), no normal map in the game's materials, and the Sobel limit ───────────────────
class B46_CodeMadeMap(Scene):
    def construct(self):
        im = a6_img("ev_normal_analytic.png", h=2.6, at=(-4.55, 1.3))
        pic = framed(im)
        lab = a6_lab("made by code", -4.55, 3.05, 34)
        ex = example_tag(3.0, 2.95)
        self.play(FadeIn(pic), FadeIn(lab), FadeIn(ex), run_time=0.5)
        # number line, 0 .. 2 (x = -2.2 .. 5.6); the two code-made-map points sit near the ends
        def X(v):
            return -2.2 + v * 3.9
        ly = 1.0
        line = Line([X(0), ly, 0], [X(2), ly, 0], color=INK, stroke_width=5)
        ticks = VGroup(*[Line([X(v), ly - 0.15, 0], [X(v), ly + 0.15, 0], color=INK, stroke_width=5) for v in (0, 1, 2)])
        nums = VGroup(*[T(str(v), 36).move_to([X(v), ly - 0.55, 0]) for v in (0, 1, 2)])
        self.play(Create(line), Create(ticks), FadeIn(nums), run_time=0.5)
        d1 = Dot([X(0.054), ly, 0], radius=0.17, color=TERRA)
        d2 = Dot([X(1.946), ly, 0], radius=0.17, color=TERRA)
        n1 = T("0.054", 40).move_to([X(0.054) + 0.2, ly + 0.55, 0])
        n2 = T("1.946", 40).move_to([X(1.946) - 0.1, ly + 0.55, 0])
        s1 = a6_lab("read as OpenGL", X(0.054) + 0.55, ly + 1.05, 30)
        s2 = a6_lab("read as DirectX", X(1.946) - 0.4, ly + 1.05, 30)
        until(self, "point zero five", lead=0.45)
        self.play(FadeIn(d1, scale=0.5), FadeIn(n1), FadeIn(s1), run_time=0.4)
        until(self, "one point nine five", lead=0.5)
        self.play(FadeIn(d2, scale=0.5), FadeIn(n2), FadeIn(s2), run_time=0.4)
        until(self, "no normal map", lead=0.5)
        chip_ = status_tag("game materials: no normal map", -3.1, -0.85)
        self.play(FadeIn(chip_, shift=UP * 0.15), run_time=0.4)
        # after the midpoint: a normal map computed from a picture with a Sobel filter passes the check
        until(self, "And know the limit", lead=0.2)
        sy = -2.0
        pic_box = box(-4.6, sy, 1.4, 1.0, color=INK, sw=4)
        hill = VMobject(stroke_color=INK, stroke_width=4).set_points_as_corners([[-5.15, sy - 0.28, 0], [-4.85, sy + 0.02, 0], [-4.6, sy - 0.1, 0], [-4.3, sy + 0.2, 0], [-4.05, sy - 0.28, 0]])
        sun = Dot([-4.9, sy + 0.25, 0], radius=0.07, color=DIM)
        map_box = box(-1.2, sy, 1.4, 1.0, color=INK, sw=4)
        mp = VGroup(*[Line([-1.75, sy - 0.3 + k * 0.2, 0], [-0.65, sy - 0.3 + k * 0.2, 0], color=BAR2, stroke_width=4) for k in range(4)])
        a_s1 = arrow([-3.7, sy, 0], [-2.15, sy, 0], w=5, tip=0.2)
        a_s2 = arrow([-0.3, sy, 0], [1.1, sy, 0], w=5, tip=0.2)
        l_pic = a6_lab("picture", -4.6, sy - 0.82, 32)
        l_sob = a6_lab("Sobel", -2.95, sy + 0.45, 34)
        l_map = a6_lab("normal map", -1.2, sy - 0.82, 32)
        until(self, "Sobel", lead=0.9)
        self.play(Create(pic_box), Create(hill), FadeIn(sun), FadeIn(l_pic), GrowArrow(a_s1), FadeIn(l_sob), run_time=0.6)
        self.play(Create(map_box), Create(mp), FadeIn(l_map), GrowArrow(a_s2), run_time=0.5)
        ok1 = tick_mark(1.55, sy, s=0.25)
        l_ok = a6_labl("passes the check", 2.0, sy, 34)
        until(self, "passes", lead=0.35)
        self.play(Create(ok1), FadeIn(l_ok), run_time=0.4)
        ok2 = tick_mark(1.55, -2.55, s=0.2)
        l_s = a6_labl("a surface exists", 2.0, -2.55, 34)
        x3 = cross_mark(1.55, -3.05, s=0.2)
        l_r = a6_labl("the right one", 2.0, -3.05, 34)
        until(self, "a surface exists", lead=0.7)
        self.play(Create(ok2), FadeIn(l_s), run_time=0.35)
        until(self, "not the right one", lead=0.85)
        self.play(Create(x3), FadeIn(l_r), run_time=0.35)
        done(self)


# ── B47 · the audit: the real MATERIALS.md rows, five things the test pins, 5 + 24 + 24 = 53 ─────────────────────────────
A6_ROWS = [("Signal pad, per-instance ShaderMaterial", "shaders/signal.gdshader", "activation ← charge / 0.6; texture-free"),
           ("MaterialSpecimen0 / matte.tres", "shaders/surface.gdshader", "tint white; roughness .9; scale 1; metallic 0"),
           ("MaterialSpecimen1 / coated.tres", "same", "tint (.45,.95,.72); roughness .25; scale 2; metallic .4")]


class B47_Audit(Scene):
    def construct(self):
        fname = M("MATERIALS.md", 24).move_to([-6.15, 2.95, 0], aligned_edge=LEFT)
        ex = example_tag(3.0, 2.95)
        card = RoundedRectangle(width=11.2, height=3.45, corner_radius=0.16, stroke_color=DIM, stroke_width=4, fill_opacity=0).move_to([-0.6, 0.78, 0])
        ya = [2.02, 0.92, -0.18]
        rows = VGroup()
        for (c1, c2, c3), y in zip(A6_ROWS, ya):
            rows.add(VGroup(T(c1, 32).move_to([-5.9, y, 0], aligned_edge=LEFT),
                            M(c2, 20, DIM).move_to([1.2, y, 0], aligned_edge=LEFT),
                            T(c3, 32).move_to([-5.9, y - 0.47, 0], aligned_edge=LEFT)))
        self.add(fname)
        self.wait(0.3)
        self.play(Create(card), FadeIn(ex), run_time=0.6)
        until(self, "a materials table", lead=0.55)
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.35), run_time=0.9)
        # the five things the test pins, ticking in on the voice (two rows)
        items = [("shader path", -5.8, -1.55, "shader path", 0.3), ("hints", -2.65, -1.55, "hints", 0.2), ("values", -0.55, -1.55, "values", 0.2),
                 ("texture paths", -5.8, -2.3, "texture paths", 0.25), ("import settings", -2.2, -2.3, "import settings", 0.3)]
        for text, x, y, ph, ld in items:
            until(self, ph, lead=ld)
            tk = tick_mark(x, y, s=0.18)
            lb = a6_labl(text, x + 0.35, y, 34)
            self.play(Create(tk), FadeIn(lb), run_time=0.3)
        # the counter climbs: 5 on the pad shader, 24 per material
        until(self, "The example's test", lead=0.95)
        sx = 5.6
        n5 = T("5", 52).move_to([sx, 1.78, 0])
        n24a = T("24", 52).move_to([sx, 0.68, 0])
        n24b = T("24", 52).move_to([sx, -0.42, 0])
        bar = Line([5.05, -1.0, 0], [6.15, -1.0, 0], color=INK, stroke_width=6)
        vt = ValueTracker(0)
        hero = always_redraw(lambda: T(str(int(round(vt.get_value()))), 76).move_to([sx, -1.7, 0]))
        self.add(hero)
        self.play(FadeIn(n5), vt.animate.set_value(5), rate_func=linear, run_time=0.35)
        self.play(FadeIn(n24a), Create(bar), vt.animate.set_value(29), rate_func=linear, run_time=0.4)
        self.play(FadeIn(n24b), vt.animate.set_value(53), rate_func=linear, run_time=0.4)
        done(self)
