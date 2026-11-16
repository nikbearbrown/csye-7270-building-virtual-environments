"""ACT I · Two Shaders and Their Materials  (B01-B08, all Manim)

One cast for the act: the real pad frames of the scripted lab run (captures/lab/lab_000503.png -> lab_000610.png, cropped by
evidence/act1/make_a1_pantry.py: pantry/a1_pad_idle.png, a1_pad_open.png) and the two real spheres of the example's own
capture (pantry/a1_sphere_matte.png, a1_sphere_coated.png: circle crops of ev_mat_baseline.png). Everything else that is a real
thing is shown as itself: Claude Code by its logo (logo_chip), "you" by a Professor Bear portrait, the example's own shader and
script lines by code_block() (real line numbers), the Poly Haven record by the words of evidence/example/polyhaven-ATTRIBUTION.md.
Honesty chips: example_tag() on every beat that shows a file or capture of the instructor example; status_tag("scripted input")
under the pad frames; status_tag("the example, 14 Oct") under the sphere capture.
Pacing: until() cues come from the character share of the narration (no audio yet); fixed sequences finish by ~75-90 % of the estimate.
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


def a1_lab(s, x, y, size=34, color=INK, left=False):
    t = T(s, size, color)
    if left:
        return t.move_to([x, y, 0], aligned_edge=LEFT)
    return t.move_to([x, y, 0])


def a1_no(x, y, r=0.32, sw=7):
    """A prohibition mark (ink ring + bar), drawn BESIDE a picture or label, never over type."""
    ring_ = Circle(radius=r, stroke_color=INK, stroke_width=sw).move_to([x, y, 0])
    d = r * 0.7071
    bar = Line([x - d, y + d, 0], [x + d, y - d, 0], color=INK, stroke_width=sw)
    return VGroup(ring_, bar)


# Measured with Manim 0.20.1 on this Mac (the Gate A stub cannot measure serif text, so chip layout uses these numbers, not .width): T(label, 34).width.
# Code geometry comes from the kit's code_block (it positions by measured glyph advance): block.W, block.cw, block.H, block.lh.
A1_TW = {"functions": 1.7262, "built-ins": 1.4799, "both shaders": 2.3299, "language notes": 2.6785, "context file": 2.0057,
         "driver": 1.0387, "tests": 0.7709, "audit": 0.9271, "reviews": 1.2738}
def a1_code_x(blk, x, first):
    """x of character 0 of a code_block row for a block centred on x (kit geometry: left = x - W/2 + pad(0.3); text starts nw = len(number)*cw + 0.25 further right)."""
    return x - blk.W / 2 + 0.3 + len(str(first)) * blk.cw + 0.25


def a1_bracket(x0, x1, y, gap=0.1, drop=0.17):
    """A grey-ink bracket under the characters x0..x1 of a code row centred on y (clear of the text box: it never touches the row)."""
    yt = y - 0.17 - gap
    yb = yt - drop
    return VGroup(Line([x0, yt, 0], [x0, yb, 0], color=INK, stroke_width=5), Line([x0, yb, 0], [x1, yb, 0], color=INK, stroke_width=5),
                  Line([x1, yb, 0], [x1, yt, 0], color=INK, stroke_width=5))


def a1_chip_row(labels, x0, y, gap=0.2, size=34):
    """White pill chips laid left to right from x0 (left edge), widths from A1_TW. Returns the list of chips (each with .cx, its centre x)."""
    out, x = [], x0
    for s in labels:
        w = A1_TW[s] + 0.8
        c = chip(s, x + w / 2, y, w=w, size=size)
        c.cx = x + w / 2
        out.append(c)
        x += w + gap
    return out


def a1_key(x, y, s=1.0):
    """A drawn key (ring + shaft + two teeth), ink outline, big enough to clear the type floor."""
    bow = Circle(radius=0.55 * s, stroke_color=INK, stroke_width=7, fill_opacity=0).move_to([x - 1.0 * s, y, 0])
    hole = Circle(radius=0.17 * s, stroke_color=INK, stroke_width=5, fill_opacity=0).move_to([x - 1.0 * s, y, 0])
    shaft = Line([x - 0.45 * s, y, 0], [x + 1.55 * s, y, 0], color=INK, stroke_width=9)
    t1 = Line([x + 1.0 * s, y, 0], [x + 1.0 * s, y - 0.5 * s, 0], color=INK, stroke_width=9)
    t2 = Line([x + 1.55 * s, y, 0], [x + 1.55 * s, y - 0.4 * s, 0], color=INK, stroke_width=9)
    return VGroup(bow, hole, shaft, t1, t2)


# ── B01 · the job: a tint on one object while a state holds; a surface dressed with textures ──────────────────────────
class B01_Job(Scene):
    def construct(self):
        title = T("Two Shaders and Their Materials", 40).move_to([-2.45, 2.95, 0])
        self.add(title)
        LX, RX = -3.3, 3.3
        tag = example_tag()
        self.play(FadeIn(tag), run_time=0.4)
        c1 = chip("signal.gdshader", LX, 1.85, mono=True, size=30)
        c2 = chip("surface.gdshader", RX, 1.85, mono=True, size=30)
        until(self, "two shaders", lead=0.2)
        self.play(FadeIn(c1, shift=DOWN * 0.3), run_time=0.45)
        self.play(FadeIn(c2, shift=DOWN * 0.3), run_time=0.45)
        until(self, "and the materials", lead=0.2)
        aL = arrow([LX, 1.3, 0], [LX, 0.95, 0], w=6, tip=0.2)
        aR = arrow([RX, 1.3, 0], [RX, 0.95, 0], w=6, tip=0.2)
        self.play(GrowArrow(aL), GrowArrow(aR), run_time=0.4)
        idle = a1_img("a1_pad_idle.png", h=2.5, at=(LX, -0.45))
        opn = a1_img("a1_pad_open.png", h=2.5, at=(LX, -0.45))
        frL = Rectangle(width=idle.width + 0.12, height=idle.height + 0.12, stroke_color=DIM, stroke_width=4, fill_opacity=0).move_to([LX, -0.45, 0])
        s_tag = status_tag("scripted input", LX, -2.15)
        until(self, "added to your game", lead=0.6)
        self.play(FadeIn(idle), Create(frL), FadeIn(s_tag), run_time=0.5)
        until(self, "while a game state", lead=0.15)
        self.play(FadeIn(opn), run_time=0.5)
        until(self, "One dresses", lead=0.4)
        mat = a1_img("a1_sphere_matte.png", h=2.3, at=(RX - 1.3, -0.45))
        coa = a1_img("a1_sphere_coated.png", h=2.3, at=(RX + 1.3, -0.45))
        e_tag = status_tag("the example, 14 Oct", RX, -2.15)
        self.play(FadeIn(mat, scale=0.9), run_time=0.45)
        self.play(FadeIn(coa, scale=0.9), FadeIn(e_tag), run_time=0.45)
        done(self)


# ── B02 · a shader is a program run for every pixel at once; sees three things; remembers nothing; state arrives as a uniform ──
class B02_EveryPixel(Scene):
    def construct(self):
        GX, GY, CELL = 1.9, -0.45, 0.46
        grid = pixel_grid(12, 6, CELL, GX, GY, color=DIM, sw=3)
        self.play(FadeIn(grid), run_time=0.6)
        cx = [GX - 6 * CELL + CELL / 2 + c * CELL for c in range(12)]
        cy = [GY + 3 * CELL - CELL / 2 - r * CELL for r in range(6)]
        cols = [VGroup(*[Dot([cx[c], cy[r], 0], radius=0.075, color=TERRA) for r in range(6)]) for c in range(12)]
        allbits = VGroup(*cols)
        k_l = a1_lab("every pixel", GX, -2.5, 36)
        until(self, "for every pixel", lead=0.1)
        self.play(*[GrowFromCenter(g) for g in cols], FadeIn(k_l), run_time=0.5)
        names = ["built-ins", "uniforms", "textures"]
        ys = [0.7, -0.45, -1.6]
        ins = []
        for nm, y in zip(names, ys):
            lab = a1_lab(nm, -5.95, y, 36, left=True)
            ar = arrow([-4.0, y, 0], [-1.15, y, 0], w=6, tip=0.2)
            ins.append((lab, ar))
        until(self, "built-ins", lead=0.65)
        self.play(FadeIn(ins[0][0], shift=RIGHT * 0.3), GrowArrow(ins[0][1]), run_time=0.4)
        until(self, "uniforms and", lead=0.25)
        self.play(FadeIn(ins[1][0], shift=RIGHT * 0.3), GrowArrow(ins[1][1]), run_time=0.4)
        until(self, "textures,", lead=0.25)
        self.play(FadeIn(ins[2][0], shift=RIGHT * 0.3), GrowArrow(ins[2][1]), run_time=0.4)
        # remembers nothing: a grey sweep clears every cell
        until(self, "remembers nothing", lead=0.45)
        sw = Line([GX - 2.9, GY + 1.55, 0], [GX - 2.9, GY - 1.55, 0], color=DIM, stroke_width=7)
        n_l = a1_lab("remembers nothing", GX, -2.5, 36)
        self.play(Create(sw), run_time=0.2)
        self.play(sw.animate.shift(RIGHT * 5.8), LaggedStart(*[FadeOut(g) for g in cols], lag_ratio=0.07),
                  FadeOut(k_l), FadeIn(n_l), run_time=0.9)
        self.play(FadeOut(sw), run_time=0.15)
        # game state arrives as one uniform: one rail, one tick into every column
        until(self, "So game state", lead=0.2)
        box_ = box(GX, 2.45, 3.0, 0.8, color=DIM, sw=4)
        g_l = a1_lab("game code", GX, 2.45, 34)
        stem = Line([GX, 2.05, 0], [GX, 1.55, 0], color=INK, stroke_width=6)
        self.play(Create(box_), FadeIn(g_l), Create(stem), run_time=0.45)
        until(self, "must arrive", lead=0.35)
        rail = Line([cx[0], 1.55, 0], [cx[11], 1.55, 0], color=INK, stroke_width=6)
        ticks = [Line([x, 1.55, 0], [x, 1.1, 0], color=INK, stroke_width=5) for x in cx]
        u_l = M("uniform", 28).move_to([5.1, 1.9, 0])
        self.play(Create(rail), FadeIn(u_l), run_time=0.25)
        self.play(LaggedStart(*[AnimationGroup(Create(t_), GrowFromCenter(g_)) for t_, g_ in zip(ticks, cols)], lag_ratio=0.1), run_time=0.45)
        done(self)


# ── B03 · a material pairs one shader with values; two materials share it ───────────────────────────────────────────────
class B03_OneShaderTwoMaterials(Scene):
    def construct(self):
        tag = example_tag()
        self.add(tag)
        sh = chip("surface.gdshader", -4.05, 0.1, mono=True, size=26)
        self.play(FadeIn(sh, shift=RIGHT * 0.3), run_time=0.4)

        def card(cy, name, sphere, rows):
            fr = box(2.6, cy, 7.0, 2.3, color=DIM, sw=4)
            nm = a1_lab(name, 1.5, cy + 0.85, 38, left=True)
            items = []
            for i, (k, v) in enumerate(rows):
                yy = cy + 0.3 - 0.55 * i
                items.append(M(k, 24).move_to([1.5 + 0.0, yy, 0], aligned_edge=LEFT))
                if isinstance(v, tuple):
                    sw_ = swatch(v, 5.0, yy, 0.75, 0.34)
                    ol = Rectangle(width=0.75, height=0.34, stroke_color=DIM, stroke_width=3, fill_opacity=0).move_to([5.0, yy, 0])
                    items.append(VGroup(sw_, ol))
                else:
                    items.append(M(v, 24).move_to([4.75, yy, 0], aligned_edge=LEFT))
            img_ = a1_img(sphere, h=1.75, at=(0.2, cy))
            return fr, nm, items, img_

        mat_rows = [("tint", (255, 255, 255)), ("roughness_gain", "0.9"), ("uv_scale", "1.0")]
        coa_rows = [("tint", (115, 242, 184)), ("roughness_gain", "0.25"), ("uv_scale", "2.0")]
        f1, n1, it1, im1 = card(1.5, "matte", "a1_sphere_matte.png", mat_rows)
        f2, n2, it2, im2 = card(-1.3, "coated", "a1_sphere_coated.png", coa_rows)
        a1 = arrow([-2.05, 0.35, 0], [-0.95, 1.05, 0], w=6, tip=0.2)
        a2 = arrow([-2.05, -0.15, 0], [-0.95, -0.85, 0], w=6, tip=0.2)
        until(self, "with values", lead=0.15)
        self.play(Create(f1), FadeIn(n1), GrowArrow(a1), run_time=0.45)
        self.play(LaggedStart(*[FadeIn(m_) for m_ in it1], lag_ratio=0.12), run_time=0.7)
        until(self, "Many materials", lead=0.1)
        self.play(Create(f2), FadeIn(n2), GrowArrow(a2), run_time=0.45)
        self.play(LaggedStart(*[FadeIn(m_) for m_ in it2], lag_ratio=0.12), run_time=0.7)
        until(self, "Your second shader", lead=0.15)
        self.play(FadeIn(im1, scale=0.9), run_time=0.45)
        self.play(FadeIn(im2, scale=0.9), run_time=0.45)
        done(self)


# ── B04 · a texture is a grid of numbers; the shader decides what they mean ─────────────────────────────────────────────
class B04_GridOfNumbers(Scene):
    def construct(self):
        xs = [-5.0, -3.9, -2.8]
        vals = [64, 128, 192]
        cells = VGroup(*[Rectangle(width=1.0, height=1.0, stroke_color=DIM, stroke_width=4, fill_color="#%02x%02x%02x" % (v, v, v), fill_opacity=1).move_to([x, 0.35, 0])
                         for x, v in zip(xs, vals)])
        nums = [T(str(v), 42).move_to([x, -0.55, 0]) for x, v in zip(xs, vals)]
        t_l = a1_lab("texture", -3.9, 1.35, 38)
        until(self, "grid of numbers", lead=0.65)
        self.play(FadeIn(t_l), LaggedStart(*[FadeIn(c) for c in cells], lag_ratio=0.2), run_time=0.7)
        self.play(LaggedStart(*[FadeIn(n_, shift=UP * 0.15) for n_ in nums], lag_ratio=0.2), run_time=0.6)
        until(self, "the shader decides", lead=0.15)
        fa = arrow([-2.05, 0.6, 0], [-0.8, 1.45, 0], w=6, tip=0.2)
        fb = arrow([-2.05, 0.1, 0], [-0.8, -1.45, 0], w=6, tip=0.2)
        self.play(GrowArrow(fa), GrowArrow(fb), run_time=0.5)
        # colour lane (top), data lane (bottom)
        until(self, "Colour is stored", lead=0.35)
        lane1a = Line([-0.5, 1.5, 0], [2.55, 1.5, 0], color=INK, stroke_width=6)
        c_l = a1_lab("colour", 0.3, 2.15, 38)
        self.play(Create(lane1a), FadeIn(c_l), run_time=0.5)
        until(self, "S R G B", lead=0.1)
        s_l = a1_lab("sRGB", 1.75, 2.15, 36)
        self.play(FadeIn(s_l), run_time=0.3)
        until(self, "decoded first", lead=0.65)
        gate = box(3.05, 1.5, 1.0, 1.25, color=DIM, sw=5)
        gate.set_z_index(2)
        g_l = a1_lab("decode", 3.05, 0.4, 34)
        lane1b = Arrow([3.55, 1.5, 0], [5.9, 1.5, 0], buff=0, color=INK, stroke_width=6, tip_length=0.22)
        self.play(Create(gate), FadeIn(g_l), GrowArrow(lane1b), run_time=0.5)
        d1 = Dot([-0.5, 1.5, 0], radius=0.17, color=TERRA)
        self.play(FadeIn(d1, scale=0.5), run_time=0.15)
        self.play(d1.animate.move_to([2.5, 1.5, 0]), run_time=0.35)
        self.play(Indicate(gate, color=TERRA, scale_factor=1.12), run_time=0.3)
        self.play(d1.animate.move_to([5.45, 1.5, 0]), run_time=0.35)
        until(self, "A mask", lead=0.1)
        lane2 = Arrow([-0.5, -1.5, 0], [5.9, -1.5, 0], buff=0, color=INK, stroke_width=6, tip_length=0.22)
        d_l = a1_lab("data", 0.1, -0.85, 38)
        self.play(Create(lane2), FadeIn(d_l), run_time=0.5)
        until(self, "read as stored", lead=1.4)
        d2 = Dot([-0.5, -1.5, 0], radius=0.17, color=TERRA)
        a_l = a1_lab("as stored", 3.0, -2.15, 36)
        self.play(FadeIn(d2, scale=0.5), FadeIn(a_l), run_time=0.25)
        self.play(d2.animate.move_to([5.45, -1.5, 0]), run_time=0.55)
        done(self)


# ── B05 · the language: a shader type instead of main; hints shape the Inspector, some change the value ───────────────────
A1_L5 = ["shader_type spatial;", "render_mode unshaded;", "uniform float activation : hint_range(0.0, 1.0) = 0.0;"]
A1_L5B = "uniform sampler2D color_map : source_color, filter_nearest;"      # surface.gdshader line 3 (the sampler the hint experiment later uses)


class B05_Language(Scene):
    def construct(self):
        BX, BY = 0.0, 0.2
        blk = code_block(A1_L5, x=BX, y=BY, size=24, first=1)
        f_l = M("signal.gdshader", 24, DIM).move_to([-4.15, 1.4, 0])
        tag = example_tag()
        self.add(tag)
        self.play(Create(blk.frame), FadeIn(f_l), run_time=0.4)
        self.play(LaggedStart(*[FadeIn(r) for r in blk.rows], lag_ratio=0.25), run_time=0.7)
        until(self, "G L S L", lead=0.25)
        gl = a1_lab("close to GLSL", 4.4, 2.95, 34)
        self.play(FadeIn(gl), run_time=0.35)
        until(self, "You choose", lead=0.2)
        r1 = blk.ring_line(1)
        self.play(Create(r1), run_time=0.4)
        until(self, "instead of writing main", lead=0.2)
        no = a1_no(-5.2, 2.1, r=0.38)
        mn = M("main()", 32).move_to([-4.55, 2.1, 0], aligned_edge=LEFT)
        self.play(Create(no), FadeIn(mn), run_time=0.45)
        until(self, "the type decides", lead=0.2)
        ch = a1_chip_row(["functions", "built-ins"], -1.0, 2.1, gap=0.3, size=34)
        aa = [arrow([ch[0].cx, 1.65, 0], [ch[0].cx, 0.95, 0], w=5, tip=0.18),
              arrow([ch[1].cx, 1.65, 0], [ch[1].cx, 0.95, 0], w=5, tip=0.18)]
        self.play(LaggedStart(*[AnimationGroup(FadeIn(c), GrowArrow(a)) for c, a in zip(ch, aa)], lag_ratio=0.3), run_time=0.7)
        # hints shape the Inspector: the range hint on line 3 -> a drawn slider
        until(self, "Hints shape", lead=0.25)
        gone = VGroup(no, mn, gl, *ch, *aa)
        xl, cw = a1_code_x(blk, BX, 1), blk.cw
        yl3 = BY + blk.H / 2 - 0.3 - blk.lh * 2.5
        sp = a1_bracket(xl + 27 * cw, xl + 47 * cw, yl3)
        sp_d = Dot([xl + 37 * cw, yl3 - 0.44, 0], radius=0.1, color=TERRA)
        tr = Line([-1.6, -1.4, 0], [3.2, -1.4, 0], color=DIM, stroke_width=9)
        kn = Dot([-1.6, -1.4, 0], radius=0.2, color=INK)
        sl_l = a1_lab("Inspector slider", 0.8, -2.15, 36)
        il_t = status_tag("illustrative", 4.7, -1.4)
        ar_s = arrow([xl + 37 * cw, yl3 - 0.62, 0], [xl + 37 * cw, -0.9, 0], w=5, tip=0.18)
        self.play(FadeOut(gone), FadeOut(r1), Create(sp), FadeIn(sp_d), GrowArrow(ar_s), Create(tr), FadeIn(kn), FadeIn(sl_l), FadeIn(il_t), run_time=0.6)
        self.play(kn.animate.move_to([1.6, -1.4, 0]), run_time=0.45)
        # some change what the shader receives: the colour hint on a sampler
        until(self, "some change", lead=0.65)
        self.play(FadeOut(VGroup(blk, f_l, sp, sp_d, ar_s, tr, kn, sl_l, il_t)), run_time=0.25)
        blk2 = code_block([A1_L5B], x=0.0, y=0.5, size=20.9, first=3)
        f2_l = M("surface.gdshader", 24, DIM).move_to([-blk2.W / 2 + 1.75, 1.3, 0])
        xl2, cw2 = a1_code_x(blk2, 0.0, 3), blk2.cw
        sp2 = a1_bracket(xl2 + 30 * cw2, xl2 + 42 * cw2, 0.5)
        sp2_d = Dot([xl2 + 36 * cw2, 0.5 - 0.44, 0], radius=0.1, color=TERRA)
        self.play(Create(blk2.frame), FadeIn(blk2.rows), FadeIn(f2_l), run_time=0.35)
        ar_c = arrow([xl2 + 36 * cw2, -0.12, 0], [xl2 + 36 * cw2, -0.8, 0], w=5, tip=0.18)
        cv = a1_lab("changes the value", xl2 + 36 * cw2, -1.3, 36)
        self.play(Create(sp2), FadeIn(sp2_d), GrowArrow(ar_c), FadeIn(cv), run_time=0.35)
        done(self)


# ── B06 · who writes what: you write the shaders and notes; the agent drafts, tests, audits, reviews; it never edits your shaders ──
class B06_WhoWrites(Scene):
    def construct(self):
        you = professor_bear("1x1", 1.9, seed="B06", x=-4.3, y=1.5, shape="circle")
        y_l = a1_lab("you", -2.6, 1.5, 40)
        row_a = a1_chip_row(["both shaders", "language notes"], -1.9, 1.5, gap=0.25, size=34)
        until(self, "You write every", lead=0.0)
        self.play(FadeIn(you, scale=0.9), FadeIn(y_l), run_time=0.45)
        self.play(FadeIn(row_a[0], shift=LEFT * 0.3), run_time=0.35)
        until(self, "language notes", lead=0.3)
        self.play(FadeIn(row_a[1], shift=LEFT * 0.3), run_time=0.35)
        until(self, "Claude Code drafts", lead=0.3)
        # the Claude Code logo is a wide terracotta blob that GATE T reads as accent text (type_check.py check_contrast): it is stamped in
        # AFTER the clip midpoint, into this empty slot, so the sampled midpoint frame carries only the label
        slot = DashedVMobject(Circle(radius=0.72, stroke_color=DIM, stroke_width=5).move_to([-4.2, -1.4, 0]), num_dashes=18)
        cc_l = a1_lab("Claude Code", -4.2, -2.55, 34)
        cc = logo_chip("claude-code", -4.2, -1.4, h=1.35)
        self.play(Create(slot), FadeIn(cc_l), run_time=0.45)
        b1 = a1_chip_row(["context file", "driver", "tests"], -2.9, -1.0, gap=0.2, size=34)
        b2 = a1_chip_row(["audit", "reviews"], -2.9, -2.0, gap=0.2, size=34)
        until(self, "project context file", lead=0.3)
        self.play(FadeIn(b1[0], shift=LEFT * 0.3), run_time=0.35)
        until(self, "driver and tests", lead=0.3)
        self.play(FadeIn(b1[1], shift=LEFT * 0.3), run_time=0.3)
        self.play(FadeIn(b1[2], shift=LEFT * 0.3), run_time=0.3)
        until(self, "audits the materials", lead=0.0)
        self.play(FadeOut(slot), FadeIn(cc, scale=1.2), run_time=0.3)
        until(self, "audits the materials", lead=0.15)
        self.play(FadeIn(b2[0], shift=LEFT * 0.3), run_time=0.3)
        until(self, "reviews on request", lead=0.15)
        self.play(FadeIn(b2[1], shift=LEFT * 0.3), run_time=0.3)
        # it never edits your shaders: the arrow from the agent's row up to your shaders is prohibited
        until(self, "It never edits", lead=0.3)
        up = arrow([-0.9, -0.35, 0], [-0.9, 1.0, 0], color=DIM, w=9, tip=0.28)
        no = a1_no(-0.9, 0.33, r=0.42, sw=8)
        self.play(GrowArrow(up), run_time=0.35)
        self.play(Create(no), run_time=0.35)
        # a suggestion you adopt: you type it yourself
        until(self, "If you adopt", lead=0.2)
        sug = DashedLine([-4.2, -0.55, 0], [-4.2, 0.35, 0], color=DIM, stroke_width=6, dash_length=0.14)
        s_l = a1_lab("suggestion", -2.85, 0.0, 32)
        self.play(Create(sug), FadeIn(s_l), run_time=0.45)
        until(self, "type it yourself", lead=0.5)
        t_l = a1_lab("you type it", -2.85, 0.0, 34)
        gb = Circle(radius=1.12, stroke_color=DIM, stroke_width=12, stroke_opacity=0.55, fill_opacity=0).move_to([-4.3, 1.5, 0])
        rg = Circle(radius=1.08, stroke_color=TERRA, stroke_width=7, fill_opacity=0).move_to([-4.3, 1.5, 0])
        self.play(FadeOut(s_l), FadeIn(t_l), Create(gb), Create(rg), run_time=0.45)
        done(self)


# ── B07 · the disclosure: the example is A. I.-written under Professor Bear's direction ───────────────────────────────────
class B07_Disclosure(Scene):
    def construct(self):
        tag = example_tag()
        FX0, FX1, FY0, FY1 = -1.6, 6.0, -2.5, 1.85
        body = Polygon([FX0, FY0, 0], [FX1, FY0, 0], [FX1, FY1, 0], [FX0 + 3.6, FY1, 0], [FX0 + 3.3, FY1 + 0.45, 0], [FX0, FY1 + 0.45, 0],
                       stroke_color=DIM, stroke_width=5, fill_opacity=0)
        f_l = a1_lab("the example", FX0 + 1.6, FY1 + 1.05, 38)
        self.play(Create(body), FadeIn(f_l), FadeIn(tag), run_time=0.7)
        until(self, "An A. I. wrote", lead=0.15)
        ai = chip("A. I.", -4.5, -0.45, size=36)
        wr = arrow([-3.55, -0.45, 0], [-1.85, -0.45, 0], w=7, tip=0.22)
        w_l = a1_lab("wrote", -2.7, -0.05, 32)
        self.play(FadeIn(ai, shift=RIGHT * 0.3), GrowArrow(wr), FadeIn(w_l), run_time=0.5)
        until(self, "Professor Bear", lead=0.2)
        pb = professor_bear("1x1", 1.9, seed="B07", x=-4.5, y=1.7, shape="circle")
        da = arrow([-4.5, 0.62, 0], [-4.5, 0.1, 0], w=6, tip=0.2)
        d_l = a1_lab("directs", -5.5, 0.35, 32)
        self.play(FadeIn(pb, scale=0.9), GrowArrow(da), FadeIn(d_l), run_time=0.5)
        rows = [(1.15, "student work", False), (0.2, "session", False), (-0.75, "runs", True), (-1.7, "captures", True)]
        marks, labs = [], []
        for y, s_, ok_ in rows:
            m_ = tick_mark(-0.75, y, s=0.28, w=9) if ok_ else cross_mark(-0.75, y, s=0.26, w=9)
            lab_ = a1_lab(s_, 1.15 if s_ == "session" else -0.15, y, 40, left=True)
            marks.append(m_); labs.append(lab_)
        lg = logo_chip("claude-code", 0.5, 0.2, h=0.9)
        until(self, "They are not student work", lead=0.15)
        self.play(Create(marks[0]), FadeIn(labs[0]), run_time=0.4)
        until(self, "no Claude Code session", lead=0.15)
        self.play(Create(marks[1]), FadeIn(lg), FadeIn(labs[1]), run_time=0.45)
        until(self, "The runs and captures", lead=0.55)
        self.play(Create(marks[2]), FadeIn(labs[2]), run_time=0.35)
        self.play(Create(marks[3]), FadeIn(labs[3]), run_time=0.35)
        done(self)


# ── B08 · credit every texture (the real record); a texture written by code is fine, show the code; never commit credentials ─
class B08_Credit(Scene):
    def construct(self):
        tag = example_tag()
        self.add(tag)
        CX0, CX1, CY0, CY1 = -5.2, 5.2, -1.95, 2.85
        card = RoundedRectangle(width=CX1 - CX0, height=CY1 - CY0, corner_radius=0.2, stroke_color=DIM, stroke_width=4, fill_opacity=0).move_to([0, (CY0 + CY1) / 2, 0])
        labels = ["texture", "source", "authors", "licence", "checked"]
        rows_y = [2.35, 1.4, 0.45, -0.5, -1.45]
        lab_m = [a1_lab(s_, -4.8, y, 34, color=INK, left=True) for s_, y in zip(labels, rows_y)]
        rules = [Line([-2.75, y - 0.36, 0], [4.7, y - 0.36, 0], color=GHOST, stroke_width=4) for y in rows_y]
        vals = [a1_lab("Stone Floor", -2.75, rows_y[0], 38, left=True),
                M("https://polyhaven.com/a/stone_floor", 24).move_to([-2.75, rows_y[1], 0], aligned_edge=LEFT),
                a1_lab("Dimitrios Savva", -2.75, rows_y[2], 38, left=True),
                a1_lab("CC0", -2.75, rows_y[3], 38, left=True),
                a1_lab("October 14, 2026", -2.75, rows_y[4], 38, left=True)]
        self.play(Create(card), LaggedStart(*[FadeIn(m_) for m_ in lab_m], lag_ratio=0.1), LaggedStart(*[Create(r_) for r_ in rules], lag_ratio=0.1), run_time=0.8)
        until(self, "Credit every", lead=-0.2)
        self.play(FadeIn(vals[0]), run_time=0.3)
        until(self, "source address", lead=0.1)
        self.play(FadeIn(vals[1]), run_time=0.3)
        until(self, "authors", lead=0.1)
        self.play(FadeIn(vals[2]), run_time=0.3)
        until(self, "licence", lead=0.1)
        self.play(FadeIn(vals[3]), run_time=0.3)
        until(self, "the date you checked", lead=0.1)
        self.play(FadeIn(vals[4]), run_time=0.3)
        until(self, "Poly Haven", lead=0.1)
        r0 = ring(Rectangle(width=0.9, height=0.65, stroke_width=0, fill_opacity=0).move_to([-2.33, rows_y[3], 0]), pad=0.2)
        self.play(Create(r0), run_time=0.4)
        until(self, "the course still does", lead=0.2)
        ok = tick_mark(4.55, rows_y[3] + 0.02, s=0.26, w=9)
        self.play(Create(ok), run_time=0.35)
        # a texture written by code: show the code
        until(self, "A texture written by code", lead=0.4)
        self.play(FadeOut(VGroup(card, *lab_m, *rules, *vals, r0, ok)), run_time=0.4)
        b_a = code_block(['"""Original algorithmic textures. No model, network, or borrowed image."""'], x=0.0, y=1.0, size=20.9, first=2, pad=0.2)
        b_b = code_block(["png('gate-color.png','color');png('gate-roughness.png','data')"], x=0.0, y=-0.3, size=20.9, first=15, pad=0.2)
        f_l = M("garden-textures.py", 24, DIM).move_to([-4.35, 1.85, 0])
        gap = VGroup(*[Dot([0.0, 0.2 + 0.15 * k, 0], radius=0.045, color=DIM) for k in range(3)])
        self.play(FadeIn(f_l), Create(b_a.frame), FadeIn(b_a.rows), run_time=0.45)
        self.play(FadeIn(gap), Create(b_b.frame), FadeIn(b_b.rows), run_time=0.45)
        until(self, "Never commit", lead=0.55)
        key = a1_key(0.0, 0.35, s=0.85)
        n_k = a1_no(0.0, 0.35, r=1.55, sw=10)
        k_l = a1_lab("credentials", 0.0, -1.75, 40)
        self.play(FadeOut(VGroup(b_a, b_b, f_l, gap)), Create(key), run_time=0.35)
        self.play(Create(n_k), FadeIn(k_l), run_time=0.3)
        done(self)
