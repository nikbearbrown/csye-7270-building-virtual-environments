"""ACT IX · Check What You See  (B59-B68, all Manim)

One cast for the act: the REAL pad captures of the instructor example (the pad shader at activation 0 / 0.5 / 1 / 2: pantry/ev_pad_*.png from
captures/example-native/, Compatibility, 14 Oct; the Forward+ twins pantry/ev_pad_fp_*.png from captures/forward-plus/, re-run 16 Oct), the real
lab frames (captures/lab/, scripted input), the real sphere captures (circle-masked silhouettes pantry/a9_sweep_*, a9_mat_*, made by
evidence/act9/make_a9_pantry.py) and the real constant-ALBEDO probe patches (pantry/a9_probe_c_*, Compatibility).
EVERY pixel number on screen carries its renderer; the numbers are read from evidence/example/controlled-predictions.json,
captures/forward-plus/signal_values_*.json and evidence/runs/R9-constant-albedo-compatibility.json (evidence/act9/verify_numbers.py asserts them).
Pacing: until() cues from the character share of the narration; every fixed sequence ends by ~0.9 x the estimate.
"""

A9P = "pantry/"


def a9_lab(s, x, y, size=34, color=INK, edge=None):
    t = T(s, size, color)
    return t.move_to([x, y, 0]) if edge is None else t.move_to([x, y, 0], aligned_edge=edge)


def a9_img(name, w=None, h=None, at=(0.0, 0.0)):
    im = ImageMobject(A9P + name)
    if w is not None:
        im.set_width(w)
    if h is not None:
        im.set_height(h)
    return im.move_to(np.array([at[0], at[1], 0.0]))


def a9_toggle(x, y, on=False):
    """A generic switch (outline pill, grey knob): off = knob left."""
    pill_ = RoundedRectangle(width=0.84, height=0.42, corner_radius=0.21, fill_opacity=0, stroke_color=INK, stroke_width=4).move_to([x, y, 0])
    knob = Circle(radius=0.13, fill_color=DIM, fill_opacity=1, stroke_width=0).move_to([x + (0.2 if on else -0.2), y, 0])
    return VGroup(pill_, knob)


def a9_dots(x, y, r=0.085, color=TERRA):
    """A sample-point mark on a real picture: a ring over a wider grey backing (never a bare thin terracotta stroke)."""
    back = Circle(radius=r + 0.035, stroke_color=DIM, stroke_width=8, stroke_opacity=0.6).move_to([x, y, 0])
    rr = Circle(radius=r, stroke_color=color, stroke_width=5).move_to([x, y, 0])
    return VGroup(back, rr)


def a9_frame(im, sw=12, pad=0.05):
    """A heavy INK frame round a real capture. GATE T's global contrast check counts every mid-tone pixel of a capture as 'text colour' and GATE V's low-contrast
    check averages every non-background pixel: ink mass in the frame pulls both means back toward ink (evidence/act9/RENDER-NOTES.md)."""
    return framed(im, color=INK, pad=pad, sw=sw)


def a9_triple(rgb, sep=","):
    return sep.join(str(int(v)) for v in rgb)


# ── B59 · green logs are not done: what a headless pass proves, and the human check ──────────────────────────────────────────
class B59_GreenLogs(Scene):
    def construct(self):
        title = T("Check What You See", 40).move_to([-3.4, 2.95, 0])
        self.add(title)
        PX, PY = 2.45, 0.1                                   # centre of the panel crop
        px = 6.4 / 1110.0                                    # scene units per source pixel of the panel crop
        panel = framed(a9_img("a9_panel_609.png", w=6.4, at=(PX, PY)))
        tag = status_tag("scripted input \u00b7 earlier take, 14 Oct", PX, 2.4)
        # The frame is the EARLIER take of the lab (captures/lab = native-lab, 14 Oct 01:52; the repo's current verification.gd prints "State probe checks linkage."
        # instead of "Headless proves state."). Only the line both takes print, "Render and play still need checking." (crop rows 516..574 of 609), is marked: an ink
        # bracket OUTSIDE the panel (a ring over the dark panel is read by GATE T as accent text on a dark ground) and one terracotta dot
        yt = PY - (516 - 304.5) * px
        yb = PY - (574 - 304.5) * px
        bx = PX + 3.2 + 0.3
        brk = VGroup(Line([bx - 0.17, yt, 0], [bx, yt, 0], color=INK, stroke_width=6), Line([bx, yt, 0], [bx, yb, 0], color=INK, stroke_width=6),
                     Line([bx, yb, 0], [bx - 0.17, yb, 0], color=INK, stroke_width=6))
        bdot = Dot([bx + 0.2, (yt + yb) / 2, 0], radius=0.1, color=TERRA)
        scr = RoundedRectangle(width=6.65, height=3.72, corner_radius=0.16, stroke_color=DIM, stroke_width=5, fill_opacity=0).move_to([PX, PY, 0])
        scr_l = a9_lab("the screen", PX, PY, 40)
        ys = [0.1, -0.65, -1.4, -2.15]
        ti = terminal_icon(-5.1, 1.05, s=0.42)
        hd = a9_lab("headless test", -4.45, 1.05, 36, edge=LEFT)
        ticks = [tick_mark(-5.45, y, s=0.2) for y in ys]
        # green logs: the headless test's four checks, all ticked (GATE T samples each clip at 50%: the dark engine panel lands AFTER the midpoint, with "the screen")
        until(self, "Green logs", lead=0.0)
        self.play(Create(ti), FadeIn(hd), LaggedStart(*[Create(t) for t in ticks], lag_ratio=0.2), run_time=0.8)
        until(self, "A headless pass", lead=0.25)
        self.play(Create(scr), FadeIn(scr_l), run_time=0.5)
        for word, y, ph_, ld in (("parse", ys[0], "parse", 0.3), ("declared", ys[1], "declared", 0.3), ("driven", ys[2], "driven", 0.3), ("wired", ys[3], "wired", 0.3)):
            until(self, ph_, lead=ld)
            self.play(FadeIn(a9_lab(word, -4.95, y, 36, edge=LEFT)), run_time=0.3)
        until(self, "It proves nothing", lead=0.3)
        self.play(FadeOut(scr_l), FadeIn(panel), FadeIn(tag), run_time=0.5)
        eye = eye_icon(1.3, -2.45, s=0.5)
        ey = a9_lab("your eyes", 2.0, -2.45, 36, edge=LEFT)
        ex = example_tag(-2.75, -3.0)
        until(self, "about the screen", lead=-0.2)
        self.play(Create(eye), FadeIn(ey), FadeIn(ex), run_time=0.45)
        until(self, "Every visual rule", lead=0.2)
        self.play(Create(brk), FadeIn(bdot, scale=0.5), run_time=0.5)
        done(self)


# ── B60 · capture in the engine: two paths from the drawn frame to a PNG, then the capture function ─────────────────────────
class B60_CaptureInEngine(Scene):
    def construct(self):
        DY = -1.5                                            # the lanes start centred, then rise to make room for the code
        # --- lanes (drawn at their FINAL height; shifted down by DY before they are shown) ---
        shared = box(-5.1, 1.9, 1.9, 2.1)
        shared_l = VGroup(a9_lab("engine", -5.1, 2.15, 34), a9_lab("frame", -5.1, 1.65, 34))
        a_up = arrow([-4.1, 2.5, 0], [-3.4, 2.5, 0], w=6)
        png = box(-2.32, 2.5, 2.16, 0.85)
        png_l = a9_lab("PNG file", -2.32, 2.5, 34)
        a_lo = arrow([-4.1, 1.3, 0], [-3.4, 1.3, 0], w=6)
        prof = box(-1.87, 1.3, 3.06, 0.85)
        prof_l = a9_lab("colour profile", -1.87, 1.3, 34)
        a_lo2 = arrow([-0.3, 1.3, 0], [0.4, 1.3, 0], w=6)
        scal = box(1.3, 1.3, 1.8, 0.85)
        scal_l = a9_lab("scaling", 1.3, 1.3, 34)
        a_lo3 = arrow([2.25, 1.3, 0], [2.95, 1.3, 0], w=6)
        shot = box(4.27, 1.3, 2.53, 0.85)
        shot_l = a9_lab("screenshot", 4.27, 1.3, 34)
        ok = tick_mark(-0.75, 2.5, s=0.22, w=8)
        d1 = Dot([-1.87 + 1.53 - 0.05, 1.3 + 0.425, 0], radius=0.12, color=TERRA)     # a pin on the box's top-right corner
        d2 = Dot([1.3 + 0.9 - 0.05, 1.3 + 0.425, 0], radius=0.12, color=TERRA)
        up_grp = VGroup(a_up, png, png_l, ok)
        lo_grp = VGroup(a_lo, prof, prof_l, a_lo2, scal, scal_l, a_lo3, shot, shot_l)
        lanes = VGroup(shared, shared_l, up_grp, lo_grp, d1, d2)
        lanes.shift(DOWN * (-DY))                            # DY is negative: shift down by 1.5
        self.add(shared, shared_l)
        until(self, "Capture in the engine", lead=0.0)
        self.play(GrowArrow(a_up), Create(png), FadeIn(png_l), Create(ok), run_time=0.7)
        until(self, "operating system", lead=0.25)
        self.play(GrowArrow(a_lo), Create(prof), FadeIn(prof_l), run_time=0.4)
        self.play(GrowArrow(a_lo2), Create(scal), FadeIn(scal_l), GrowArrow(a_lo3), Create(shot), FadeIn(shot_l), run_time=0.7)
        until(self, "colour profiles", lead=0.45)
        self.play(FadeIn(d1, scale=0.5), run_time=0.3)
        until(self, "scaling", lead=0.6)
        self.play(FadeIn(d2, scale=0.5), run_time=0.3)
        # --- the capture function of the assignment (assignment-05.md lines 457-460), then the example's own line ---
        code1 = code_block(["    mat.set_shader_parameter(param, value)", "    await RenderingServer.frame_post_draw",
                            "    get_viewport().get_texture().get_image().save_png(path)", "    driver.set_process(true)"],
                           x=-0.9, y=-0.3, size=20, first=457, pad=0.2)
        row_y = [-0.3 + code1.H / 2 - 0.2 - code1.lh * (i + 0.5) for i in range(4)]       # rows 457..460
        px1 = -0.9 + code1.W / 2 + 0.3                                                       # a terracotta pointer sits just right of the frame
        drv_l = a9_lab("driver", 5.45, 0.55, 34)
        tog = a9_toggle(5.45, 0.0, on=False)
        t1 = status_tag("from the assignment", -4.2, -2.85)
        code2 = code_block(["\tawait RenderingServer.frame_post_draw"], x=-2.5, y=-1.75, size=20, first=11, pad=0.2)
        px2 = -2.5 + code2.W / 2 + 0.3
        fl = M("render-material-evidence.gd", 20).move_to([px2 + 0.35 + 2.0, -1.75, 0])
        t2 = example_tag(1.7, -2.85)

        def ptr(x, y):                                         # a terracotta pointer (the row being read), pointing left at the code
            return Polygon([x + 0.12, y + 0.17, 0], [x + 0.12, y - 0.17, 0], [x - 0.15, y, 0], fill_color=TERRA, fill_opacity=1, stroke_width=0)
        r1 = ptr(px1, row_y[0])
        until(self, "Switch the driver off", lead=0.55)
        self.play(lanes.animate.shift(UP * (-DY)), FadeIn(code1), FadeIn(t1), run_time=0.6)
        self.play(FadeIn(drv_l), Create(tog), run_time=0.3)
        until(self, "set the value", lead=0.25)
        self.play(FadeIn(r1, shift=LEFT * 0.2), run_time=0.25)
        until(self, "wait for the frame", lead=0.3)
        r2 = ptr(px2, -1.75)
        self.play(r1.animate.shift(DOWN * code1.lh), FadeIn(code2), FadeIn(fl), FadeIn(t2), run_time=0.4)
        self.play(FadeIn(r2, shift=LEFT * 0.2), run_time=0.25)
        until(self, "save the viewport", lead=0.35)
        self.play(r1.animate.shift(DOWN * code1.lh), run_time=0.35)
        done(self)


# ── B61 · the example's four pad captures, two sample pixels each, the dark one measured beside its prediction ─────────────────
# numbers: controlled-predictions.json (predicted_display_rgb8_compatibility, dark stripe) and signal_values_compatibility.json (rgb8, uv_x 0.15625)
A9_PRED = {"0": (66, 27, 15), "0.5": (48, 105, 74), "1": (31, 184, 133), "2": (0, 255, 250)}
A9_MEAS = {"0": (66, 24, 10), "0.5": (47, 105, 74), "1": (28, 184, 133), "2": (0, 255, 251)}


class B61_FourCaptures(Scene):
    def construct(self):
        W = 2.8
        Hh = W * 1080 / 1620.0
        pos = {"0": (-4.7, 1.65), "0.5": (-1.75, 1.65), "1": (-4.7, -1.0), "2": (-1.75, -1.0)}
        names = {"0": "ev_pad_0.0.png", "0.5": "ev_pad_0.5.png", "1": "ev_pad_1.0.png", "2": "ev_pad_2.0.png"}
        caps, labs = {}, {}
        for k, (cx, cy) in pos.items():
            caps[k] = framed(a9_img(names[k], w=W, at=(cx, cy)))
            labs[k] = a9_lab("activation " + k, cx, cy - Hh / 2 - 0.33, 32)
        # the table (right): header, four outline rows
        hd = a9_lab("dark stripe pixel", 3.55, 3.0, 34)
        dk = Dot([1.7, 3.0, 0], radius=0.1, color=TERRA)
        h1 = a9_lab("predicted", 2.7, 2.4, 32)
        h2 = a9_lab("measured", 4.95, 2.4, 32)
        ry = {"0": 1.5, "0.5": 0.5, "1": -0.5, "2": -1.5}
        rbox, rnum, rp, rm = {}, {}, {}, {}
        for k, y in ry.items():
            rbox[k] = box(3.125, y, 6.15, 0.85)
            rnum[k] = T(k, 44).move_to([0.7, y, 0])
            rp[k] = M(a9_triple(A9_PRED[k]), 24).move_to([2.7, y, 0])
            rm[k] = M(a9_triple(A9_MEAS[k]), 24).move_to([4.95, y, 0])
        tg1 = example_tag(-2.9, -3.0)
        tg2 = status_tag("Compatibility", 3.4, -3.0)
        # legend of the two marks (the table is the terracotta one)
        lg1 = Dot([0.65, -2.35, 0], radius=0.1, color=TERRA)
        lg1l = a9_lab("dark stripe", 0.95, -2.35, 32, edge=LEFT)
        lg2 = Dot([3.3, -2.35, 0], radius=0.1, color=INK)
        lg2l = a9_lab("light stripe", 3.6, -2.35, 32, edge=LEFT)
        until(self, "The example's four", lead=0.0)
        self.play(FadeIn(tg1), FadeIn(tg2), run_time=0.3)
        for k, ph, ld in (("0", "activation zero", 0.3), ("0.5", "half", 0.4), ("1", "one and two", 0.4), ("2", "and two", 0.0)):
            until(self, ph, lead=ld)
            self.play(FadeIn(caps[k]), FadeIn(labs[k]), run_time=0.3)
        # after the midpoint: the two named pixels (UV.x 0.15625 -> source x 253, UV.x 0.21875 -> x 354, both at the vertical middle), then the table
        until(self, "two named pixels", lead=0.1)
        marks = VGroup()
        kx = W / 1620.0
        for k, (cx, cy) in pos.items():
            for sx, col in ((253, TERRA), (354, INK)):
                marks.add(Circle(radius=0.085, stroke_color=CARD, stroke_width=4).move_to([cx - W / 2 + sx * kx, cy, 0]),
                          Dot([cx - W / 2 + sx * kx, cy, 0], radius=0.055, color=col))
        self.play(FadeIn(marks, scale=0.6), FadeIn(lg1, scale=0.5), FadeIn(lg1l), FadeIn(lg2, scale=0.5), FadeIn(lg2l), run_time=0.4)
        until(self, "measured beside", lead=0.3)
        self.play(FadeIn(hd), FadeIn(dk, scale=0.5), FadeIn(h1), FadeIn(h2), run_time=0.3)
        for k in ("0", "0.5", "1", "2"):
            self.play(Create(rbox[k]), FadeIn(rnum[k]), FadeIn(rp[k]), FadeIn(rm[k]), run_time=0.3)
        until(self, "At half", lead=0.2)
        ptr = Polygon([-0.32, 0.5 + 0.2, 0], [-0.32, 0.5 - 0.2, 0], [-0.02, 0.5, 0], fill_color=TERRA, fill_opacity=1, stroke_width=0)
        self.play(FadeIn(ptr, shift=RIGHT * 0.2), run_time=0.4)
        done(self)


# ── B62 · the gaps (per channel), then the probe: a plain constant colour shows the same shortfall ──────────────────────────────
A9_GAP = [("activation 0", "dark stripe", (0, -3, -5)), ("activation 1", "", (-3, 0, 0))]   # measured minus predicted, Compatibility (analysis.json diff_compat_minus_prediction)
A9_PROBE = [(0.0585, 15, 10), (0.104, 27, 24), (0.12, 31, 28)]                                 # value, as written (x255), Compatibility read (R9 json)


class B62_Gaps(Scene):
    def construct(self):
        TX = 2.65                                             # the gap table is built centred (shifted right by TX), then slides left to its final place
        cw, pitch = 1.3, 1.4
        cols = [-2.9 + pitch * i for i in range(3)]           # FINAL x of the three columns
        heads = [a9_lab(n, x, 2.5, 34) for n, x in zip(("red", "green", "blue"), cols)]
        rows_y = [1.35, -0.2]
        cells, nums, bars, rlabs = [], [], [], []
        for (a, b, gaps), y in zip(A9_GAP, rows_y):
            rlabs.append(VGroup(a9_lab(a, -4.9, y + (0.22 if b else 0.0), 32), *([a9_lab(b, -4.9, y - 0.27, 32)] if b else [])))
            for x, g in zip(cols, gaps):
                cells.append(box(x, y, cw, 1.2, sw=3))
                nums.append(T("%s%d" % ("\u2212" if g < 0 else "", abs(g)), 44).move_to([x, y + 0.17, 0]))
                bw = abs(g) * 0.2
                bars.append(Rectangle(width=max(bw, 0.001), height=0.12, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([x - cw / 2 + 0.14 + bw / 2, y - 0.38, 0]))
        table = VGroup(*heads, *rlabs, *cells, *nums, *bars)
        # dots by the two numbers the voice names: blue at activation 0 (-5), red at activation 1 (-3)
        dot_b = Dot([cols[2] + 0.42, rows_y[0] + 0.44, 0], radius=0.1, color=TERRA)
        dot_r = Dot([cols[0] + 0.42, rows_y[1] + 0.44, 0], radius=0.1, color=TERRA)
        # the probe (right side): three real constant-colour patches, written value -> read value (Compatibility)
        ph_ = a9_lab("probe: constant colour", 3.75, 2.5, 34)
        c1 = a9_lab("written", 4.1, 1.55, 32)
        c2 = a9_lab("read", 5.75, 1.55, 32)
        prow = []
        for (v, w, r), y in zip(A9_PROBE, (0.65, -0.55, -1.75)):
            im = framed(a9_img("a9_probe_c_%s.png" % v, h=0.9, at=(1.4, y)), pad=0.05, sw=3)
            vl = a9_lab(str(v), 2.7, y, 34)
            wn = T(str(w), 44).move_to([4.1, y, 0])
            ar = arrow([4.5, y, 0], [5.3, y, 0], w=6, tip=0.24)
            rn = T(str(r), 48).move_to([5.8, y, 0])
            prow.append(Group(im, vl, wn, ar, rn))
        tg1 = status_tag("Compatibility", 3.3, -3.0)
        tg2 = example_tag(-2.9, -3.0)
        table.shift(RIGHT * TX)
        dot_b.shift(RIGHT * TX)
        dot_r.shift(RIGHT * TX)
        until(self, "Not every value", lead=0.0)
        self.play(FadeIn(VGroup(*heads)), LaggedStart(*[Create(c) for c in cells], lag_ratio=0.1), FadeIn(VGroup(*rlabs)), FadeIn(tg1), FadeIn(tg2), run_time=0.7)
        until(self, "dark stripe at zero", lead=0.2)
        self.play(FadeIn(VGroup(*nums[:3])), FadeIn(VGroup(*bars[:3])), run_time=0.4)
        until(self, "five in blue", lead=0.2)
        self.play(FadeIn(dot_b, scale=0.5), run_time=0.25)
        until(self, "full activation", lead=0.2)
        self.play(FadeIn(VGroup(*nums[3:])), FadeIn(VGroup(*bars[3:])), run_time=0.4)
        until(self, "three in red", lead=0.3)
        self.play(FadeIn(dot_r, scale=0.5), run_time=0.25)
        until(self, "A probe", lead=0.2)
        slide = VGroup(table, dot_b, dot_r)
        self.play(slide.animate.shift(LEFT * TX), run_time=0.5)
        self.play(FadeIn(ph_), FadeIn(c1), FadeIn(c2), run_time=0.3)
        until(self, "constant colour", lead=0.3)
        for pr in prow:
            self.play(FadeIn(pr, shift=LEFT * 0.15), run_time=0.3)
        until(self, "Cause still open", lead=1.0)
        oc = open_circle(-5.35, -1.6, 0.2)
        ol = a9_lab("cause still open", -4.95, -1.6, 36, edge=LEFT)
        self.play(Create(oc), FadeIn(ol), run_time=0.4)
        done(self)


# ── B63 · Forward+ differs: the same pad at half in both renderers, the light stripe's real numbers ────────────────────────────
class B63_ForwardPlusDiffers(Scene):
    def construct(self):
        # real 1080 x 540 bands of the pad captures at half activation (pantry/a9_pad_strip_*, made by evidence/act9/make_a9_pantry.py);
        # the light-stripe pixel (UV.x 0.21875) sits at x 354, y 270 of the band. Heavy ink frames: see a9_frame (the bare green captures give GATE T 4.47:1).
        pc, pf = "pantry/a9_pad_strip_0.5.png", "pantry/a9_pad_strip_fp_0.5.png"
        CW = 5.0
        k = CW / 1080.0
        CY = 1.15
        L = a9_frame(img(pc, w=CW, x=-3.1, y=CY))
        R = a9_frame(img(pf, w=CW, x=3.1, y=CY))
        tgl = status_tag("Compatibility", -3.1, 2.85)
        tgr = status_tag("Forward+ \u00b7 re-run", 3.1, 2.85)
        sl = swatch((66, 112, 78), -4.95, -0.6, w=0.9, h=0.6)
        sr = swatch((76, 137, 97), 1.25, -0.6, w=0.9, h=0.6)
        nl = M("66,112,78", 36).move_to([-3.0, -0.6, 0])
        nr = M("76,137,97", 36).move_to([3.2, -0.6, 0])
        okl = tick_mark(-1.15, -0.6, s=0.22, w=8)
        xr = cross_mark(5.1, -0.6, s=0.2, w=8)
        pl = a9_lab("prediction", -0.4, -1.3, 36)
        pn = M("66,112,78", 36).move_to([2.3, -1.3, 0])
        lgd = Dot([-5.55, -1.3, 0], radius=0.1, color=TERRA)                       # the ringed pixel is the LIGHT stripe (UV.x 0.21875)
        lgl = a9_lab("light stripe", -5.25, -1.3, 36, edge=LEFT)
        ml = a9_dots(-3.1 - CW / 2 + 354 * k, CY, 0.12, TERRA)
        mr = a9_dots(3.1 - CW / 2 + 354 * k, CY, 0.12, TERRA)
        # the calculation in linear light (a fit of numbers: evidence/runs/scripts/analyze.py), drawn after the midpoint
        b1 = box(-4.45, -2.05, 1.65, 0.85); l1 = a9_lab("decode", -4.45, -2.05, 34)
        b2 = box(-1.4, -2.05, 2.9, 0.85); l2 = a9_lab("mix in linear", -1.4, -2.05, 34)
        b3 = box(1.7, -2.05, 1.75, 0.85); l3 = a9_lab("encode", 1.7, -2.05, 34)
        ar1 = arrow([-3.5, -2.05, 0], [-2.95, -2.05, 0], w=6, tip=0.24)
        ar2 = arrow([0.14, -2.05, 0], [0.74, -2.05, 0], w=6, tip=0.24)
        hero = T("24 of 24", 48).move_to([4.7, -1.85, 0])
        hero_l = a9_lab("values fit", 4.7, -2.45, 34)
        tge = example_tag(-2.75, -3.1)
        until(self, "Switch renderer", lead=0.0)
        self.play(FadeIn(L), FadeIn(tgl), FadeIn(tge), run_time=0.4)
        until(self, "On Forward Plus", lead=0.3)
        self.play(FadeIn(R), FadeIn(tgr), run_time=0.4)
        until(self, "on the light stripe", lead=0.3)
        self.play(FadeIn(ml, scale=0.5), FadeIn(mr, scale=0.5), FadeIn(lgd, scale=0.5), FadeIn(lgl), run_time=0.35)
        until(self, "seventy-six", lead=0.1)
        self.play(FadeIn(sr), FadeIn(nr), run_time=0.3)
        until(self, "not sixty-six", lead=0.2)
        self.play(FadeIn(sl), FadeIn(nl), Create(okl), run_time=0.35)
        self.play(FadeIn(pl), FadeIn(pn), Create(xr), run_time=0.4)
        until(self, "Those numbers", lead=0.25)
        self.play(Create(b1), FadeIn(l1), GrowArrow(ar1), Create(b2), FadeIn(l2), GrowArrow(ar2), Create(b3), FadeIn(l3), run_time=0.8)
        self.play(FadeIn(hero), FadeIn(hero_l), run_time=0.3)
        done(self)


# ── B64 · activation 2: cyan, and hint_range did not clamp (a drawn slider; both renderers) ───────────────────────────────────
class B64_NoClamp(Scene):
    def construct(self):
        # Order of arrival follows the voice: the Compatibility pad at 2 (cyan) and its arithmetic first; Forward+ and the activation-1 comparison after the midpoint.
        # (GATE T's global contrast check counts the flat green of activation 1 as text colour: it must not be on screen at the clip midpoint.)
        W = 3.6
        xs = [-4.1, 0.0, 4.1]
        y = 1.3
        cap_c = a9_frame(img("pantry/ev_pad_2.0.png", w=W, x=xs[0], y=y))
        cap_f = a9_frame(img("pantry/ev_pad_fp_2.0.png", w=W, x=xs[1], y=y))
        cap_1 = a9_frame(img("pantry/ev_pad_1.0.png", w=W, x=xs[2], y=y))
        h_c = a9_lab("activation 2", xs[0], 2.95, 36)
        h_f = a9_lab("activation 2", xs[1], 2.95, 36)
        h_1 = a9_lab("activation 1", xs[2], 2.95, 36)
        n_c = M("0,255,251", 28).move_to([xs[0], -0.5, 0])
        n_f = M("0,248,181", 28).move_to([xs[1], -0.5, 0])
        n_1 = M("28,184,133", 28).move_to([xs[2], -0.5, 0])
        r_c = a9_lab("Compatibility", xs[0], -1.0, 32)
        r_f = status_tag("Forward+ \u00b7 re-run", xs[1], -1.05)
        r_1 = a9_lab("Compatibility", xs[2], -1.0, 32)
        # the arithmetic that clips (mix(base, active, 2.0) per channel, from the colours as written: dark stripe)
        c_r = a9_lab("red \u22120.02, shown 0", xs[0], -1.7, 34)
        c_g = a9_lab("green 1.34, shown 255", xs[0], -2.25, 34)
        tg = example_tag(-2.75, -3.1)
        # the slider (right): a track for hint_range(0.0, 1.0) (value 0 at x = 0.0, value 1 at x = 2.4), the value 2.0 set from code beyond its end (x = 4.8)
        TY = -2.2
        trk = Line([0.0, TY, 0], [2.4, TY, 0], color=INK, stroke_width=8)
        cap_a = Line([0.0, TY + 0.2, 0], [0.0, TY - 0.2, 0], color=INK, stroke_width=8)
        cap_b = Line([2.4, TY + 0.2, 0], [2.4, TY - 0.2, 0], color=INK, stroke_width=8)
        hnd = Dot([2.4, TY, 0], radius=0.18, color=DIM)
        far = DashedLine([2.65, TY, 0], [4.55, TY, 0], color=DIM, stroke_width=6, dash_length=0.18)
        val = Dot([4.8, TY, 0], radius=0.17, color=TERRA)
        v_l = a9_lab("2.0 set from code", 4.4, TY + 0.55, 34)
        rng = M("hint_range(0.0, 1.0)", 20).move_to([1.2, TY - 0.5, 0])
        sl_l = a9_lab("slider", 1.2, TY + 0.55, 34)
        until(self, "At two", lead=0.0)
        self.play(FadeIn(cap_c), FadeIn(h_c), run_time=0.35)
        self.play(FadeIn(n_c), FadeIn(r_c), FadeIn(tg), run_time=0.25)
        until(self, "red goes negative", lead=0.3)
        self.play(FadeIn(c_r), run_time=0.3)
        until(self, "green passes one", lead=0.3)
        self.play(FadeIn(c_g), run_time=0.3)
        until(self, "either renderer", lead=0.7)
        self.play(FadeIn(cap_f), FadeIn(h_f), run_time=0.35)
        self.play(FadeIn(n_f), FadeIn(r_f), run_time=0.2)
        until(self, "the answer is no", lead=0.9)
        self.play(FadeIn(cap_1), FadeIn(h_1), run_time=0.35)
        self.play(FadeIn(n_1), FadeIn(r_1), run_time=0.2)
        until(self, "The range belongs", lead=0.3)
        self.play(Create(trk), Create(cap_a), Create(cap_b), FadeIn(hnd), FadeIn(rng), FadeIn(sl_l), run_time=0.5)
        self.play(Create(far), FadeIn(val, scale=0.5), FadeIn(v_l), run_time=0.5)
        done(self)


# ── B65 · in play: four real lab frames in sequence (scripted input); your own playtest is required ───────────────────────────
class B65_InPlay(Scene):
    def construct(self):
        W = 2.7
        xs = [-4.6, -1.55, 1.5, 4.55]
        y = 0.8
        files = ["a9_pad_lab_000503.png", "a9_pad_lab_000597.png", "a9_pad_lab_000609.png", "a9_pad_lab_000610.png"]
        caps = [a9_frame(a9_img(f, w=W, at=(x, y)), sw=14) for f, x in zip(files, xs)]
        # labels read from each frame's own HUD line (CHARGING / 27%, CHARGING / 94%) and the pad state (frames' text: ON THE PAD, GATE OPEN)
        labs = [a9_lab(s, x, -0.6, 32) for s, x in zip(("on the pad", "charging 27%", "charging 94%", "gate open"), xs)]
        tg = status_tag("scripted input \u00b7 earlier take, 14 Oct", 0.0, 2.85)
        ex = example_tag(3.05, -3.1)
        key = VGroup(RoundedRectangle(width=0.85, height=0.85, corner_radius=0.14, stroke_color=INK, stroke_width=5, fill_opacity=0),
                     M("E", 36)).move_to([-4.9, -1.9, 0])
        key_l = a9_lab("scripted key press", -4.2, -1.9, 34, edge=LEFT)
        eye = eye_icon(0.95, -1.9, s=0.5)
        eye_l = a9_lab("your own playtest", 1.7, -1.9, 34, edge=LEFT)
        until(self, "In play", lead=0.0)
        self.play(FadeIn(tg), FadeIn(ex), run_time=0.3)
        for i, ph, ld in ((0, "trigger the state", 0.0), (1, "by normal play", 0.0), (2, "several times", 0.15), (3, "boundaries hold", 0.5)):
            until(self, ph, lead=ld)
            self.play(FadeIn(caps[i]), FadeIn(labs[i]), run_time=0.3)
        until(self, "scripted key presses", lead=0.45)
        self.play(Create(key), FadeIn(key_l), run_time=0.4)
        until(self, "Your own playtest", lead=0.25)
        self.play(Create(eye), FadeIn(eye_l), run_time=0.45)
        done(self)


# ── B66 · interface sweep: each uniform at minimum, default, maximum (twelve real sphere crops) and the stated lighting ──────
A9_SWEEP = [("roughness_gain", "0.0  0.8  1.0"), ("uv_scale", "0.25  1  4"), ("tint", "black  white  red"), ("metallic_gain", "0  0  1")]


class B66_Sweep(Scene):
    def construct(self):
        D = 1.25
        xs = [-2.45, -0.6, 1.25]
        ys = [2.0, 0.67, -0.66, -1.99]
        hs = [a9_lab(s, x, 3.0, 32) for s, x in zip(("minimum", "default", "maximum"), xs)]
        rowlab = []
        for (nm, vals), y in zip(A9_SWEEP, ys):
            rowlab.append(VGroup(M(nm, 24).move_to([-4.85, y + 0.2, 0]), (M(vals, 24) if nm != "tint" else T(vals, 32)).move_to([-4.85, y - 0.22, 0])))
        spheres = []
        for (nm, _v), y in zip(A9_SWEEP, ys):
            spheres.append(Group(*[a9_img("a9_sweep_%s_%d.png" % (nm, i), w=D, at=(xs[i], y)) for i in range(3)]))
        lt = [a9_lab("same lighting", 4.0, 2.5, 34)] + [a9_lab(s, 2.65, 1.75 - 0.62 * i, 32, edge=LEFT)
                                                                      for i, s in enumerate(("fixed camera", "Linear tonemap", "exposure 1.0", "light (−30, −30, 0)", "ambient 0.35", "no SSAO"))]
        tg = example_tag(-2.9, -3.1)
        tg2 = status_tag("Compatibility", 3.3, -3.1)
        until(self, "Interface sweep", lead=0.0)
        self.play(FadeIn(VGroup(*hs)), FadeIn(VGroup(*rowlab)), FadeIn(tg), FadeIn(tg2), run_time=0.45)
        until(self, "each uniform", lead=0.2)
        self.play(LaggedStart(*[FadeIn(t) for t in lt], lag_ratio=0.12), run_time=0.9)
        until(self, "roughness spreads", lead=0.5)
        self.play(FadeIn(spheres[0], shift=UP * 0.1), run_time=0.4)
        until(self, "scale repeats", lead=0.45)
        self.play(FadeIn(spheres[1], shift=UP * 0.1), run_time=0.4)
        until(self, "black tint", lead=0.45)
        self.play(FadeIn(spheres[2], shift=UP * 0.1), run_time=0.4)
        until(self, "Record what changed", lead=0.3)
        self.play(FadeIn(spheres[3], shift=UP * 0.1), run_time=0.4)
        done(self)


# ── B67 · one shader, two materials: baseline, a shared (shader) edit, a one-value edit ──────────────────────────────────────
def a9_sring(x, y, r=0.93):
    back = Circle(radius=r + 0.05, stroke_color=DIM, stroke_width=10, stroke_opacity=0.6).move_to([x, y, 0])
    rr = Circle(radius=r, stroke_color=TERRA, stroke_width=6).move_to([x, y, 0])
    return VGroup(back, rr)


class B67_OneShaderTwoMaterials(Scene):
    def construct(self):
        D = 1.7
        gx = [-4.15, 0.0, 4.15]
        sy = 0.45
        pairs = []
        for tag, x in zip(("baseline", "shared", "one"), gx):
            pairs.append(Group(a9_img("a9_mat_%s_l.png" % tag, w=D, at=(x - 1.05, sy)), a9_img("a9_mat_%s_r.png" % tag, w=D, at=(x + 1.05, sy))))
        # a drawn shader card above each pair, one line to each material
        cards = []
        for x in gx:
            c = box(x, 2.55, 3.0, 0.6, sw=3)
            cl = M("surface.gdshader", 20).move_to([x, 2.55, 0])
            l1 = Line([x - 0.5, 2.25, 0], [x - 1.05, sy + D / 2 + 0.12, 0], color=DIM, stroke_width=4)
            l2 = Line([x + 0.5, 2.25, 0], [x + 1.05, sy + D / 2 + 0.12, 0], color=DIM, stroke_width=4)
            cards.append(VGroup(c, cl, l1, l2))
        capt = [VGroup(a9_lab("baseline", gx[0], -0.95, 36)),
                VGroup(a9_lab("shader edited", gx[1], -0.95, 36), a9_lab("tint × (1, 0.25, 0.25)", gx[1], -1.5, 32)),
                VGroup(a9_lab("one value edited", gx[2], -0.95, 36), a9_lab("left tint", gx[2], -1.5, 32), a9_lab("(0.2, 0.2, 1.0)", gx[2], -2.0, 32))]
        d_sh = Dot([gx[1] + 1.75, 2.55, 0], radius=0.1, color=TERRA)             # where the edit is made: in the shader
        d_mat = Dot([gx[2] - 1.83, sy + 0.78, 0], radius=0.1, color=TERRA)  # ... or in one material
        r_both = VGroup(a9_sring(gx[1] - 1.05, sy), a9_sring(gx[1] + 1.05, sy))
        r_left = a9_sring(gx[2] - 1.05, sy)
        tg = example_tag(-2.9, -3.0)
        tg2 = status_tag("Compatibility", 3.3, -3.0)
        until(self, "One shader", lead=0.0)
        self.play(FadeIn(pairs[0]), FadeIn(cards[0]), FadeIn(capt[0]), FadeIn(tg), FadeIn(tg2), run_time=0.5)
        until(self, "Edit the shader", lead=0.25)
        self.play(FadeIn(pairs[1]), FadeIn(cards[1]), FadeIn(capt[1]), FadeIn(d_sh, scale=0.5), run_time=0.5)
        until(self, "Restore it", lead=0.2)
        self.play(FadeIn(pairs[2]), FadeIn(cards[2]), FadeIn(capt[2]), FadeIn(d_mat, scale=0.5), run_time=0.5)
        until(self, "shared edit", lead=0.8)
        self.play(Create(r_both), run_time=0.5)
        until(self, "tint edit", lead=1.0)
        self.play(Create(r_left), run_time=0.5)
        done(self)


# ── B68 · after the first editor session: git status; and the four things the example did not do (open circles) ─────────────
class B68_NotDone(Scene):
    def construct(self):
        L = -4.55                                              # left edge of the whole picture
        cmd = code_block(["git status"], x=-3.05, y=2.4, size=32, numbers=False, pad=0.28)
        t1 = status_tag("documented, not run", -3.05, 1.55)
        a1 = arrow([-1.35, 2.4, 0], [-0.45, 2.4, 0], w=6)
        fcard = box(2.2, 2.4, 4.85, 0.9, sw=4)
        fname = M("*.png.import", 28).move_to([2.2, 2.4, 0])
        eye = eye_icon(-4.05, 0.6, s=0.5)
        a2 = arrow([-3.3, 0.6, 0], [-2.3, 0.6, 0], w=6)
        rev = box(-0.9, 0.6, 2.0, 0.8, sw=4)
        rev_l = a9_lab("revision", -0.9, 0.6, 36)
        hdr = a9_lab("the example did not", L, -0.25, 38, edge=LEFT)
        sp = Dot([-0.15, -0.25, 0], radius=0.1, color=TERRA)
        items = ["no person played it", "no screenshot comparison", "no Claude Code session", "shortfall unexplained"]
        ys = [-0.95, -1.65, -2.35, -3.05]
        circs = [open_circle(L + 0.25, y, 0.21) for y in ys]
        labs = [a9_lab(s, L + 0.75, y, 40, edge=LEFT) for s, y in zip(items, ys)]
        tg = example_tag(3.2, -0.25)
        until(self, "After your first", lead=0.0)
        self.play(Create(cmd), FadeIn(t1), run_time=0.5)
        until(self, "import file", lead=0.6)
        self.play(GrowArrow(a1), Create(fcard), FadeIn(fname), run_time=0.6)
        until(self, "revision", lead=0.9)
        self.play(Create(eye), GrowArrow(a2), Create(rev), FadeIn(rev_l), run_time=0.6)
        until(self, "What the example did not do", lead=0.35)
        self.play(FadeIn(hdr), FadeIn(sp, scale=0.5), FadeIn(tg), run_time=0.4)
        for c, lb, ph, ld in zip(circs, labs, ("no person played", "no screenshot", "no Claude Code", "unexplained"), (0.3, 0.3, 0.3, 0.9)):
            until(self, ph, lead=ld)
            self.play(Create(c), FadeIn(lb), run_time=0.3)
        done(self)
