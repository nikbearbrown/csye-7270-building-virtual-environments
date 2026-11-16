"""ACT II · Predict Before You Write  (B09 is a Remotion CCPlainShell, see lanes/act2.json; B10-B18 are Manim)

One cast for the act: signal.gdshader (the example's 11-line pad shader) and the pad itself. The pad is shown as the REAL lab frames
(captures/lab/, scripted input, cropped to pantry/a2_pad_*.png by evidence/act2/make_pad_crops.py). Every code line is real text from the frozen
copies in evidence/example/sources/ (signal.gdshader, garden.gd) with real line numbers. Every number is read from those files, from
evidence/example/controlled-predictions.json or recomputed by evidence/act2/verify_arithmetic.py. Drawings (the sRGB curve, the rulers, the
timelines, the mix bar) are drawings of an idea: nothing here is styled as a screenshot of Godot.
Pacing: until() leads are from the character share of the narration; fixed sequences end by ~75% of the estimate.
"""

A2P = "pantry/"


def a2_lab(s, x, y, size=34, color=INK):
    return T(s, size, color).move_to([x, y, 0])


def a2_mono(s, x, y, size=24, color=INK):
    return M(s, size, color).move_to([x, y, 0])


def a2_mono_l(s, xl, y, size=24, color=INK):
    """Menlo text whose LEFT edge sits at xl (aligned_edge, never get_left())."""
    return M(s, size, color).move_to([xl, y, 0], aligned_edge=LEFT)


def a2_lab_l(s, xl, y, size=34, color=INK):
    return T(s, size, color).move_to([xl, y, 0], aligned_edge=LEFT)


def a2_img(name, h=None, w=None, at=(0.0, 0.0)):
    im = ImageMobject(A2P + name)
    if h is not None:
        im.set_height(h)
    if w is not None:
        im.set_width(w)
    im.move_to(np.array([at[0], at[1], 0.0]))
    return im


def a2_hex(rgb8):
    return "#%02x%02x%02x" % tuple(max(0, min(255, int(round(v)))) for v in rgb8)


def a2_mix(c0, c1, t):
    return tuple(a + (b - a) * t for a, b in zip(c0, c1))


def a2_swatch(rgb8, x, y, w=1.0, h=0.7, outline=None):
    """A colour chip of a REAL (computed or measured) RGB8 triple. Light chips get a thin grey outline (so they do not vanish on the cream stage); dark and
    mid-dark chips get none: GATE T reads a chip within 75 RGB of ink as a text run and measures it against the ring just outside it, and a grey outline there
    fails the local-contrast check (found at 4K in B15). outline=True/False overrides."""
    lum = sum(rgb8) / 3.0
    if outline is None:
        outline = lum > 150
    r = Rectangle(width=w, height=h, fill_color=a2_hex(rgb8), fill_opacity=1, stroke_color=DIM if outline else a2_hex(rgb8), stroke_width=3 if outline else 0)
    return r.move_to([x, y, 0])


def a2_cross(x, y, s=0.17, w=6, color=INK):
    """A multiplication sign drawn as two strokes (no glyph, no font fallback)."""
    return VGroup(Line([x - s, y - s, 0], [x + s, y + s, 0], color=color, stroke_width=w),
                  Line([x - s, y + s, 0], [x + s, y - s, 0], color=color, stroke_width=w))


def a2_eq(x, y, s=0.17, w=6, color=INK):
    return VGroup(Line([x - s, y + 0.07, 0], [x + s, y + 0.07, 0], color=color, stroke_width=w),
                  Line([x - s, y - 0.07, 0], [x + s, y - 0.07, 0], color=color, stroke_width=w))


A2_CW = {20: 0.15, 24: 0.2}     # Menlo advance in scene units per character, measured as (width of 80 x) - (width of 10 x) over 70 (0.15000 and 0.20000); width / n of a short string reads ~2% low


def a2_code(lines, x=0.0, y=0.0, size=24, first=1, width=None, pad=0.3, numbers=True, dim_lines=()):
    """The kit's code_block, with explicit coordinates only (Gate A's stub over-estimates Text widths, so a 70-character row would 'leave the frame') and REAL
    indentation (Pango drops leading spaces; a tab counts as 4). Same interface: .frame .rows .row(n) .ring_line(n) .W .H. The text is never touched.
    numbers=False turns the line-number gutter off (a terminal, not a listing); dim_lines = row indices drawn in DIM ink (the commands above their output)."""
    cw = A2_CW[int(size)]
    lh = size / 32 * 0.46
    ns = [str(first + i) for i in range(len(lines))]
    raw = [ln.replace("\t", "    ") for ln in lines]
    nw = (max(len(n) for n in ns) * cw + 0.25) if numbers else 0.0
    tw = max(len(r) * cw for r in raw)
    W = width or (tw + nw + 2 * pad)
    H = len(lines) * lh + 2 * pad
    frame = RoundedRectangle(width=W, height=H, corner_radius=0.14, stroke_color=DIM, stroke_width=4, fill_opacity=0).move_to([x, y, 0])
    left = x - W / 2 + pad
    rows = VGroup()
    for i, r in enumerate(raw):
        yy = y + H / 2 - pad - lh * (i + 0.5)
        k = len(r) - len(r.lstrip(" "))
        num = M(ns[i], size, DIM).move_to([left, yy, 0], aligned_edge=LEFT) if numbers else VGroup()
        body = r.lstrip(" ")
        if body:
            txt = M(body, size, DIM if i in dim_lines else INK).move_to([left + nw + k * cw, yy, 0], aligned_edge=LEFT)
        else:                                            # a real blank line: an invisible placeholder keeps the row in the group
            txt = M(".", size, INK).set_opacity(0).move_to([left + nw, yy, 0], aligned_edge=LEFT)
        rows.add(VGroup(num, txt))
    g = VGroup(frame, rows)
    g.frame, g.rows, g.W, g.H, g.lh, g.first, g.size_ = frame, rows, W, H, lh, first, size
    g.row = lambda n: rows[n - first]

    def _ring_line(n, color=TERRA, h=None):
        yy = y + H / 2 - pad - lh * (n - first + 0.5)
        return RoundedRectangle(width=W - 0.3, height=h or lh * 0.98, corner_radius=0.1, stroke_color=color, stroke_width=6, fill_opacity=0).move_to([x, yy, 0])
    g.ring_line = _ring_line
    return g


# ───────────────────────────────────────────────── B09 · commit the brief first ─────────────────────────────────────────────────
# "Predict first. Commit a change brief before you write either shader or send a prompt. Keep the original; add dated revisions below it. The agent works to this file."
# ACT TITLE beat (serif 40, top-left). The REAL output of three read-only commands run in the instructor example's repository (evidence/act2/b09-run-git-manim.sh; output
# evidence/act2/b09-git-output-manim.txt, 13 lines, replayed verbatim as the literal below; verify_arithmetic.py asserts they are equal), commands in DIM ink above their output:
# the log of CHANGE-BRIEF.md (the original commit and a later one on the same file), then the stat of the brief's commit (five files, none a shader). Menlo 20: the longest real row is
# 79 characters (11.85 units), so the log prints hash + date only and the stat prints the hash only (rows are never reflowed). The CCPlainShell version is kept in lanes/act2.json under "alt".
A2_GIT = [
    '$ cd assignments/05-shaders-materials',
    "$ git log --reverse --date=short --format='%h %ad' -- CHANGE-BRIEF.md",
    '93be391 2026-10-14',
    '48c6177 2026-10-16',
    "$ git show --stat --format='%h' 93be391",
    '93be391',
    '',
    ' assignments/04-gdd/GDD.md                        | 43 ++++++++++++++++++++++++',
    ' assignments/05-shaders-materials/CHANGE-BRIEF.md | 11 ++++++',
    ' assignments/06-particles/CHANGE-BRIEF.md         |  7 ++++',
    ' assignments/07-animation/CHANGE-BRIEF.md         |  7 ++++',
    ' assignments/09-game-ai-brief.md                  | 17 ++++++++++',
    ' 5 files changed, 85 insertions(+)',
]


class B09_Brief(Scene):
    def construct(self):
        title = T("Predict Before You Write", 40).move_to([-6.0, 2.95, 0], aligned_edge=LEFT)
        repo = a2_mono("walker-claude", 4.75, 2.95, 24, DIM)
        blk = a2_code(A2_GIT, x=0.0, y=0.12, size=20, pad=0.2, numbers=False, dim_lines=(0, 1, 4))
        tag_rec = status_tag("recorded output", -4.3, -3.12)
        tag_ex = example_tag(3.05, -3.12)
        R = blk.rows
        # rows: 0 cd, 1 git log, 2-3 its output, 4 git show, 5 subject, 6 blank, 7-11 the five files, 12 summary
        self.add(title, repo, blk.frame)
        until(self, "Commit a change brief", lead=0.35)
        self.play(FadeIn(R[0]), FadeIn(R[1]), FadeIn(tag_rec), run_time=0.4)
        self.play(FadeIn(R[2]), FadeIn(R[3]), run_time=0.3)
        until(self, "before you write either shader", lead=0.3)
        self.play(FadeIn(R[4]), FadeIn(R[5]), FadeIn(tag_ex), run_time=0.35)
        files = [R[6], R[7], R[8], R[9], R[10], R[11]]
        self.play(LaggedStart(*[FadeIn(r) for r in files], lag_ratio=0.18), run_time=0.9)
        until(self, "send a prompt", lead=0.15)
        self.play(FadeIn(R[12]), run_time=0.3)
        # after the midpoint: the five-file stat is ringed (on 'Keep the'), then the log rows on their words, then the brief's own row
        until(self, "Keep the", lead=0.0)
        self.play(Create(blk.ring_line(13)), run_time=0.35)
        until(self, "the original", lead=-0.1)
        self.play(Create(blk.ring_line(3, h=0.26)), run_time=0.3)
        until(self, "dated revisions", lead=0.1)
        self.play(Create(blk.ring_line(4, h=0.26)), run_time=0.3)
        until(self, "to this file", lead=0.3)
        self.play(Create(blk.ring_line(9)), run_time=0.3)
        done(self)


# ───────────────────────────────────────────────── B10 · the state ─────────────────────────────────────────────────
# "The state: what the effect communicates, why the player needs it, and which script holds it. In the example, the pad shows charge,
#  one script owns it, and the shader only watches."
class B10_State(Scene):
    def construct(self):
        xs = [-3.0, 0.0, 3.0]
        names = ["a2_pad_000300.png", "a2_pad_000597.png", "a2_pad_000609.png"]
        ims = [a2_img(n, h=2.0, at=(x, 1.7)) for n, x in zip(names, xs)]
        crops = [framed(im) for im in ims]
        pct = [a2_lab(s, x, 0.16, 36) for s, x in zip(["0%", "27%", "94%"], xs)]
        # the script card: two real lines of garden.gd, real line numbers
        ga = a2_code(["const CHARGE_SECONDS := 0.6"], x=-2.95, y=-1.12, size=24, first=4, width=6.3)
        gb = a2_code(["var charge := 0.0"], x=-2.95, y=-2.25, size=24, first=11, width=6.3)
        gd = a2_mono("garden.gd", -5.2, -0.38, 24, DIM)
        # the shader card (watches only)
        card = box(3.75, -1.7, 3.8, 1.9, DIM, 4)
        sname = a2_mono("signal.gdshader", 3.75, -1.23, 24)
        eye = eye_icon(2.9, -2.1, 0.4)
        watches = a2_lab("watches", 4.4, -2.1, 34)
        a_read = arrow([0.4, -2.25, 0], [1.75, -2.25, 0], INK, 6)
        a_pad = arrow([4.55, -0.75, 0], [4.55, 0.45, 0], INK, 6)
        tag_ex = example_tag(3.1, -3.12)
        tag_sc = status_tag("scripted input", -4.55, 3.0)

        until(self, "what the effect", lead=0.0)
        self.play(FadeIn(crops[0]), FadeIn(pct[0]), run_time=0.4)
        until(self, "communicates", lead=0.05)
        self.play(FadeIn(crops[1]), FadeIn(pct[1]), run_time=0.4)
        until(self, "why the player", lead=0.1)
        self.play(FadeIn(crops[2]), FadeIn(pct[2]), FadeIn(tag_sc), run_time=0.4)
        until(self, "which script holds it", lead=0.35)
        self.play(FadeIn(gd), Create(ga.frame), Create(gb.frame), run_time=0.4)
        self.play(FadeIn(ga.rows), FadeIn(gb.rows), run_time=0.3)
        until(self, "the pad shows charge", lead=0.1)
        pad_ring = ring(crops[2][1], TERRA, pad=0.12)
        self.play(Create(pad_ring), run_time=0.45)
        until(self, "one script owns it", lead=0.1)
        line_ring = gb.ring_line(11)
        self.play(Create(line_ring), run_time=0.4)
        until(self, "the shader only watches", lead=0.3)
        self.play(Create(card), FadeIn(sname), FadeIn(tag_ex), run_time=0.35)
        self.play(GrowArrow(a_read), FadeIn(eye), FadeIn(watches), GrowArrow(a_pad), run_time=0.5)
        done(self)


# ───────────────────────────────────────────── B11 · the specification ─────────────────────────────────────────────
# "The specification: the shader's path and type, and each uniform's name, type, hint, default, and what sets it. The example has four. Only activation comes from the game."
# The four rows are signal.gdshader lines 3-6, read verbatim. 'set by': garden.gd line 253 sets only activation; the other three keep their defaults.
class B11_Specification(Scene):
    def construct(self):
        ROWS = [3, 4, 5, 6]
        ys = [1.15, 0.2, -0.75, -1.7]
        X_NUM, X_NAME, X_TYPE, X_HINT, X_SET = -5.85, -5.5, -2.85, -1.55, 4.4
        # headers: path and type (real: the file's path in the example's project, and line 1)
        h_path = a2_mono_l("shaders/signal.gdshader", -5.9, 2.95, 24)
        h_type = a2_mono_l("shader_type spatial;", -0.8, 2.95, 24)
        h_four = a2_lab_l("4  uniforms", 3.75, 2.92, 40)
        # column headers
        c_name = a2_lab_l("name", X_NAME, 2.1, 32, DIM)
        c_type = a2_lab_l("type", X_TYPE, 2.1, 32, DIM)
        c_hint = a2_lab_l("hint", X_HINT, 2.1, 32, DIM)
        c_def = a2_lab("default", 2.3, 2.1, 32, DIM)
        c_set = a2_lab_l("set by", X_SET, 2.1, 32, DIM)
        names = ["activation", "quiet_color", "active_color", "stripe_count"]
        types = ["float", "vec4", "vec4", "float"]
        hints = ["hint_range", "source_color", "source_color", "hint_range"]
        nums = [a2_mono(str(n), X_NUM, y, 24, DIM) for n, y in zip(ROWS, ys)]
        cn = [a2_mono_l(t, X_NAME, y, 24) for t, y in zip(names, ys)]
        ct = [a2_mono_l(t, X_TYPE, y, 24) for t, y in zip(types, ys)]
        ch = [a2_mono_l(t, X_HINT, y, 24) for t, y in zip(hints, ys)]
        # default column: two sliders (real ranges, real defaults) and two colour chips (real defaults, as written x 255)
        TR0, TR1 = 1.2, 3.4

        def slider(y, lo, hi, d, lo_s, hi_s, d_s):
            line = Line([TR0, y + 0.12, 0], [TR1, y + 0.12, 0], color=DIM, stroke_width=5)
            caps = VGroup(Line([TR0, y - 0.02, 0], [TR0, y + 0.26, 0], color=DIM, stroke_width=5),
                          Line([TR1, y - 0.02, 0], [TR1, y + 0.26, 0], color=DIM, stroke_width=5))
            xd = TR0 + (d - lo) / (hi - lo) * (TR1 - TR0)
            dot = Dot([xd, y + 0.12, 0], radius=0.13, color=TERRA)
            labs = VGroup(a2_mono(lo_s, TR0, y - 0.32, 24), a2_mono(hi_s, TR1, y - 0.32, 24))
            if d_s is not None:
                labs.add(a2_mono(d_s, xd, y - 0.32, 24))
            return VGroup(line, caps, dot, labs)
        d0 = slider(ys[0], 0.0, 1.0, 0.0, "0.0", "1.0", None)
        d3 = slider(ys[3], 1.0, 16.0, 8.0, "1.0", "16.0", "8.0")
        d1 = a2_swatch((102, 41, 23), 2.3, ys[1], 1.3, 0.55)
        d2 = a2_swatch((31, 184, 133), 2.3, ys[2], 1.3, 0.55)
        defaults = [d0, d1, d2, d3]
        sets = [a2_mono_l("garden.gd", X_SET, ys[0], 24)] + [a2_lab_l("default", X_SET, y, 34, DIM) for y in ys[1:]]
        tag_ex = example_tag(3.1, -3.12)

        until(self, "the shader's path", lead=0.1)
        self.play(FadeIn(h_path), run_time=0.35)
        until(self, "and type", lead=0.1)
        self.play(FadeIn(h_type), Create(Line([-5.9, 2.55, 0], [5.9, 2.55, 0], color=GHOST, stroke_width=4)), run_time=0.35)
        until(self, "each uniform's name", lead=0.1)
        self.play(FadeIn(c_name), *[FadeIn(m) for m in nums + cn], run_time=0.4)
        until(self, "type, hint", lead=0.2)
        self.play(FadeIn(c_type), *[FadeIn(m) for m in ct], run_time=0.3)
        until(self, "hint, default", lead=0.2)
        self.play(FadeIn(c_hint), *[FadeIn(m) for m in ch], run_time=0.3)
        until(self, "default, and", lead=0.4)
        self.play(FadeIn(c_def), *[FadeIn(m) for m in defaults], run_time=0.4)
        until(self, "what sets it", lead=0.15)
        self.play(FadeIn(c_set), *[FadeIn(m) for m in sets], FadeIn(tag_ex), run_time=0.4)
        until(self, "The example has four", lead=0.1)
        self.play(FadeIn(h_four, shift=LEFT * 0.2), run_time=0.35)
        until(self, "Only activation", lead=0.15)
        pt = Dot([X_SET - 0.28, ys[0], 0], radius=0.14, color=TERRA)
        self.play(GrowFromCenter(pt), run_time=0.4)
        done(self)


# ─────────────────────────────────────────────── B12 · the colour line ───────────────────────────────────────────────
# "The colour line: the one line in the fragment function that changes the colour. You write the shader from it, and predict from it.
#  Here it mixes the stripe colour toward the active colour."
# The whole real file (11 lines, size 20, read from the frozen copy). Line 10 is ringed; the rest of the shader is written in around it; then the colour
# line is run as arithmetic: a bar from base to active_color, a handle (activation) slides 0 -> 1, the result swatch follows (ALBEDO).
# The mix colours are the example's own prediction arithmetic (quiet_color x 0.65 = dark-stripe base, x 255), not a capture.
# verbatim copy of evidence/example/sources/signal.gdshader (tabs kept); evidence/act2/verify_arithmetic.py asserts it is identical to the frozen file
A2_SIGNAL = [
    'shader_type spatial;',
    'render_mode unshaded;',
    'uniform float activation : hint_range(0.0, 1.0) = 0.0;',
    'uniform vec4 quiet_color : source_color = vec4(0.40, 0.16, 0.09, 1.0);',
    'uniform vec4 active_color : source_color = vec4(0.12, 0.72, 0.52, 1.0);',
    'uniform float stripe_count : hint_range(1.0, 16.0, 1.0) = 8.0;',
    'void fragment() {',
    '\tfloat stripe = step(0.5, fract(UV.x * stripe_count));',
    '\tvec3 base = quiet_color.rgb * mix(0.65, 1.0, stripe);',
    '\tALBEDO = mix(base, active_color.rgb, activation);',
    '}',
]


def a2_signal_lines():
    return list(A2_SIGNAL)


class B12_ColourLine(Scene):
    def construct(self):
        lines = a2_signal_lines()
        blk = a2_code(lines, x=0.0, y=1.4, size=20, first=1)
        others = [blk.rows[i] for i in range(len(lines)) if i != 9]
        for r in others:
            r.set_opacity(0)
        base, act = (66, 27, 15), (31, 184, 133)
        N = 24
        seg = 6.0 / N
        bar = VGroup(*[Rectangle(width=seg + 0.004, height=0.4, stroke_width=0, fill_opacity=1,
                                 fill_color=a2_hex(a2_mix(base, act, i / (N - 1)))).move_to([-3.0 + seg / 2 + i * seg, -1.75, 0]) for i in range(N)])
        bar_frame = Rectangle(width=6.0, height=0.4, stroke_color=DIM, stroke_width=3, fill_opacity=0).move_to([0, -1.75, 0])
        l_base = a2_mono("base", -3.0, -2.2, 24)
        l_act = a2_mono("active_color", 3.0, -2.2, 24)
        dot = Dot([-3.0, -1.32, 0], radius=0.16, color=TERRA)
        l_activation = a2_mono("activation", -3.0, -0.95, 24)
        handle = VGroup(dot, l_activation)
        res = a2_swatch(base, -2.7, -2.85, 1.4, 0.55)
        l_res = a2_mono_l("ALBEDO", -1.8, -2.85, 24)
        a_pred = arrow([-5.4, -0.62, 0], [-5.4, -2.2, 0], INK, 6)
        l_pred = a2_lab("predict", -4.35, -1.35, 36)
        tag_ex = example_tag(3.1, -3.12)

        self.add(blk.frame, blk.rows[9])
        until(self, "the one line", lead=0.2)
        rl = blk.ring_line(10)
        self.play(Create(rl), run_time=0.45)
        until(self, "You write the shader", lead=0.3)
        self.play(*[r.animate.set_opacity(1) for r in others], FadeIn(tag_ex), run_time=0.5)
        until(self, "predict from it", lead=0.35)
        self.play(GrowArrow(a_pred), FadeIn(l_pred), FadeIn(bar), Create(bar_frame), FadeIn(l_base), FadeIn(l_act),
                  FadeIn(handle), FadeIn(res), FadeIn(l_res), run_time=0.55)
        until(self, "Here it mixes", lead=0.1)
        self.play(handle.animate.shift(RIGHT * 6.0), res.animate.set_fill(a2_hex(act)), run_time=2.4, rate_func=linear)
        done(self)


# ───────────────────────────────────────────── B13 · measurable rules ─────────────────────────────────────────────
# "Make rules measurable: the uniform's value at start and end, and a change that takes the same game time at thirty, sixty and one hundred forty-four frames
#  per second. A second press: restart, extend or ignore? The example ignores it."
# A RULE, not a measurement: three rulers of the same length (0.6 s = CHARGE_SECONDS, garden.gd line 4) with frame ticks at 30, 60 and 144 per second; a bar fills 0.0 -> 1.0
# (activation = charge / 0.6, garden.gd line 253) and all three finish together. Then the second press: restart / extend / ignore, and the example's answer
# (garden.gd line 222: a press while charging is ignored) as an arrow turned away while the bar goes on. No tick count is shown: 0.6 s holds 18, 36 and 86.4 frames.
class B13_MeasurableRules(Scene):
    def construct(self):
        X0, X1 = -3.6, 3.6
        rows = {30: 1.75, 60: 0.45, 144: -0.85}

        def ruler(fps, y):
            n = int(round(0.6 * fps))              # whole frames inside 0.6 s (18, 36, 86)
            base = Line([X0, y, 0], [X1, y, 0], color=DIM, stroke_width=4)
            ticks = VGroup(*[Line([X0 + (X1 - X0) * k / (0.6 * fps), y, 0], [X0 + (X1 - X0) * k / (0.6 * fps), y + 0.16, 0], color=DIM, stroke_width=3)
                             for k in range(n + 1)])
            track = Rectangle(width=X1 - X0, height=0.22, stroke_color=DIM, stroke_width=3, fill_opacity=0).move_to([0, y - 0.22, 0])
            return VGroup(base, ticks, track)

        def fill(y):
            return Rectangle(width=X1 - X0, height=0.22, stroke_width=0, fill_color=BAR1, fill_opacity=1).move_to([0, y - 0.22, 0])

        def dot_at(y, x=X0):
            return Dot([x, y - 0.22, 0], radius=0.15, color=TERRA)

        r = {f: ruler(f, y) for f, y in rows.items()}
        lab = {f: a2_lab(f"{f} fps", -5.0, rows[f] - 0.1, 36) for f in rows}
        dim = dim_arrow([X0, -1.75, 0], [X1, -1.75, 0], DIM, 4)
        l_dim = a2_lab("0.6 s", 0, -2.3, 40)
        l_start = a2_mono("0.0", X0, rows[60] - 0.62, 24)
        l_end = a2_mono("1.0", X1, rows[60] - 0.62, 24)
        tag_rule = status_tag("a rule, not a result", -3.0, -3.05)

        # phase 1: one ruler, the value goes 0.0 -> 1.0
        until(self, "Make rules measurable", lead=-0.15)
        self.play(Create(r[60]), FadeIn(lab[60]), Create(dim), FadeIn(l_dim), run_time=0.5)
        until(self, "the uniform's value at start", lead=0.1)
        d60, f60 = dot_at(rows[60]), fill(rows[60])
        self.play(FadeIn(l_start), FadeIn(d60), run_time=0.3)
        until(self, "and end", lead=1.25)
        self.play(GrowFromEdge(f60, LEFT), d60.animate.shift(RIGHT * (X1 - X0)), run_time=1.3, rate_func=linear)
        self.play(FadeIn(l_end), run_time=0.25)
        # phase 2: the same rule at three frame rates (rows land before the midpoint, then all three replay together)
        until(self, "the same game time", lead=0.55)
        d30, d144 = dot_at(rows[30], X1), dot_at(rows[144], X1)
        f30, f144 = fill(rows[30]), fill(rows[144])
        self.play(Create(r[30]), Create(r[144]), FadeIn(lab[30]), FadeIn(lab[144]), FadeIn(d30), FadeIn(d144), FadeIn(f30), FadeIn(f144), FadeIn(tag_rule), run_time=0.6)
        until(self, "sixty and", lead=-0.35)             # just after the midpoint: all three bars empty, then fill together
        self.play(FadeOut(f30), FadeOut(f60), FadeOut(f144), FadeOut(l_start), FadeOut(l_end), d30.animate.shift(LEFT * (X1 - X0)), d60.animate.shift(LEFT * (X1 - X0)),
                  d144.animate.shift(LEFT * (X1 - X0)), run_time=0.35)
        g30, g60, g144 = fill(rows[30]), fill(rows[60]), fill(rows[144])
        self.play(GrowFromEdge(g30, LEFT), GrowFromEdge(g60, LEFT), GrowFromEdge(g144, LEFT), d30.animate.shift(RIGHT * (X1 - X0)), d60.animate.shift(RIGHT * (X1 - X0)),
                  d144.animate.shift(RIGHT * (X1 - X0)), run_time=1.8, rate_func=linear)
        # phase 3: the second press (the 60 row stays; the other two clear). The bar fills in four chunks so each cue lands on its word.
        until(self, "A second press", lead=0.1)
        W = X1 - X0
        key1 = VGroup(RoundedRectangle(width=0.7, height=0.7, corner_radius=0.12, stroke_color=INK, stroke_width=5, fill_opacity=0).move_to([X0, rows[60] + 1.15, 0]),
                      a2_lab("E", X0, rows[60] + 1.15, 38))
        p1 = arrow([X0, rows[60] + 0.75, 0], [X0, rows[60] + 0.3, 0], INK, 6)
        self.play(FadeOut(g30), FadeOut(g144), FadeOut(r[30]), FadeOut(r[144]), FadeOut(lab[30]), FadeOut(lab[144]), FadeOut(d30), FadeOut(d144),
                  FadeOut(g60), d60.animate.shift(LEFT * W), FadeIn(key1), GrowArrow(p1), run_time=0.45)

        def seg(a, b):
            return Rectangle(width=W * (b - a), height=0.22, stroke_width=0, fill_color=BAR1, fill_opacity=1).move_to([X0 + W * (a + b) / 2, rows[60] - 0.22, 0])
        opts = [a2_lab("restart", 5.0, 1.75, 40), a2_lab("extend", 5.0, 0.9, 40), a2_lab("ignore", 5.0, 0.05, 40)]
        until(self, "restart", lead=0.1)
        s1 = seg(0.0, 0.3)
        self.play(FadeIn(opts[0]), GrowFromEdge(s1, LEFT), d60.animate.shift(RIGHT * W * 0.3), run_time=0.6, rate_func=linear)
        until(self, "extend", lead=0.1)
        s2 = seg(0.3, 0.5)
        self.play(FadeIn(opts[1]), GrowFromEdge(s2, LEFT), d60.animate.shift(RIGHT * W * 0.2), run_time=0.5, rate_func=linear)
        until(self, "ignore?", lead=0.1)
        s3 = seg(0.5, 0.7)
        key2 = VGroup(RoundedRectangle(width=0.7, height=0.7, corner_radius=0.12, stroke_color=INK, stroke_width=5, fill_opacity=0).move_to([0.0, rows[60] + 1.15, 0]),
                      a2_lab("E", 0.0, rows[60] + 1.15, 38))
        p2 = arrow([0.0, rows[60] + 0.75, 0], [0.0, rows[60] + 0.3, 0], INK, 6)
        self.play(FadeIn(opts[2]), FadeIn(key2), GrowArrow(p2), GrowFromEdge(s3, LEFT), d60.animate.shift(RIGHT * W * 0.2), run_time=0.5, rate_func=linear)
        until(self, "The example ignores", lead=0.05)
        s4 = seg(0.7, 1.0)
        no = cross_mark(0.0, rows[60] + 0.98, 0.2)
        ign = ring(opts[2], TERRA, pad=0.14)
        self.play(key2.animate.shift(UP * 0.5 + RIGHT * 0.9).set_opacity(0.25), p2.animate.shift(UP * 0.5 + RIGHT * 0.9).set_opacity(0.25), Create(no), Create(ign),
                  GrowFromEdge(s4, LEFT), d60.animate.shift(RIGHT * W * 0.3), FadeIn(example_tag(3.1, -3.12)), run_time=0.7, rate_func=linear)
        done(self)


# ─────────────────────────────────────────────── B14 · boundaries and the evidence split ───────────────────────────────────────────────
# "Boundaries: collision, movement, input and earlier tests stay unchanged. Presentation reads game state and never writes it. Then the evidence split:
#  for each rule, a headless test, or your own eyes."
# Phase 1: a fence round what must not change; presentation sits outside it, one arrow in (reads), one arrow back crossed out (never writes).
# Phase 2: four of the example's own rules are sorted into two columns: timing and reset -> a headless test (the driver test's checks 'scaled duration',
# 'reset clears uniform'); colour and readability -> your eyes (CHANGE-BRIEF 'a headless pass cannot certify color'; MATERIALS.md 'human readability ... outside the headless claims').
class B14_Boundaries(Scene):
    def construct(self):
        fence = box(-3.9, 0.55, 4.2, 4.4, DIM, 5)
        f_title = a2_lab("unchanged", -3.9, 2.2, 38)
        items = [a2_lab(t, -3.9, y, 38) for t, y in zip(["collision", "movement", "input", "earlier tests"], [1.35, 0.55, -0.25, -1.05])]
        pres = box(3.7, 0.8, 3.8, 2.0, DIM, 5)
        p_lab = a2_lab("presentation", 3.7, 1.3, 38)
        p_eye = eye_icon(3.7, 0.35, 0.42)
        a_read = arrow([-1.65, 1.3, 0], [1.75, 1.3, 0], INK, 6)
        l_read = a2_lab("reads", 0.05, 1.8, 36)
        a_write = arrow([1.75, 0.3, 0], [-1.65, 0.3, 0], DIM, 6)
        no = cross_mark(0.05, 0.3, 0.22, INK, 8)
        l_write = a2_lab("writes", 0.05, -0.2, 36)
        # phase 2
        t_icon = terminal_icon(-3.2, 2.2, 0.6)
        e_icon = eye_icon(3.2, 2.2, 0.6)
        t_lab = a2_lab("headless test", -3.2, 1.2, 38)
        e_lab = a2_lab("your eyes", 3.2, 1.2, 38)
        rules = [a2_lab("timing", 0.0, 1.0, 40), a2_lab("reset", 0.0, 0.2, 40), a2_lab("colour", 0.0, -0.6, 40), a2_lab("readability", 0.0, -1.4, 40)]
        u_t = Line([-4.5, 0.76, 0], [-1.9, 0.76, 0], color=DIM, stroke_width=4)
        u_e = Line([1.9, 0.76, 0], [4.5, 0.76, 0], color=DIM, stroke_width=4)
        tag_ex = example_tag(3.1, -3.12)

        until(self, "collision", lead=0.35)
        self.play(Create(fence), FadeIn(items[0]), run_time=0.4)
        until(self, "movement", lead=0.1)
        self.play(FadeIn(items[1]), run_time=0.3)
        until(self, "input and", lead=0.1)
        self.play(FadeIn(items[2]), run_time=0.3)
        until(self, "earlier tests", lead=0.1)
        self.play(FadeIn(items[3]), run_time=0.3)
        until(self, "stay unchanged", lead=0.1)
        self.play(FadeIn(f_title), run_time=0.3)
        until(self, "Presentation reads", lead=0.1)
        self.play(Create(pres), FadeIn(p_lab), FadeIn(p_eye), run_time=0.4)
        until(self, "game state", lead=0.3)
        self.play(GrowArrow(a_read), FadeIn(l_read), run_time=0.4)
        until(self, "never writes", lead=0.15)
        self.play(GrowArrow(a_write), FadeIn(l_write), Create(no), run_time=0.5)
        until(self, "Then the evidence split", lead=0.15)
        self.play(*[FadeOut(m) for m in (fence, f_title, pres, p_lab, p_eye, a_read, l_read, a_write, l_write, no)] + [FadeOut(m) for m in items], run_time=0.4)
        until(self, "for each rule", lead=0.1)
        self.play(*[FadeIn(r) for r in rules], run_time=0.5)
        until(self, "a headless test", lead=0.3)
        self.play(FadeIn(t_icon), FadeIn(t_lab), Create(u_t), FadeIn(tag_ex), rules[0].animate.move_to([-3.2, 0.3, 0]), rules[1].animate.move_to([-3.2, -0.5, 0]), run_time=0.45)
        until(self, "or your own eyes", lead=0.3)
        self.play(FadeIn(e_icon), FadeIn(e_lab), Create(u_e), rules[2].animate.move_to([3.2, 0.3, 0]), rules[3].animate.move_to([3.2, -0.5, 0]), run_time=0.45)
        done(self)


# ─────────────────────────────────────────────── B15 · controlled inputs, by hand ───────────────────────────────────────────────
# "Controlled inputs: three uniform values, two pixels, computed by hand. At zero, a dark stripe is the quiet colour times point six five: sixty-six, twenty-seven,
#  fifteen. Only unshaded output keeps that arithmetic honest."
# Left: the hand arithmetic for ONE pixel (signal.gdshader line 4 quiet_color x 0.65, the dark stripe's factor from line 9, then x 255). Right: the example's own
# prediction table (evidence/example/controlled-predictions.json), dark stripe numbers + light stripe swatches at activation 0.0 / 0.5 / 1.0.
# All values recomputed by evidence/act2/verify_arithmetic.py. These are predictions by hand: no engine has drawn anything yet (tag).
A2_PRED = {  # activation -> (dark stripe RGB8, light stripe RGB8), from controlled-predictions.json (checked in verify_arithmetic.py)
    0.0: ((66, 27, 15), (102, 41, 23)),
    0.5: ((48, 105, 74), (66, 112, 78)),
    1.0: ((31, 184, 133), (31, 184, 133)),
}


class B15_ByHand(Scene):
    def construct(self):
        OPX, VX = -5.6, -4.9
        # left column
        l_quiet = a2_mono_l("quiet_color", VX, 2.75, 24, DIM)
        t1 = a2_mono_l("(0.40, 0.16, 0.09)", VX, 2.15, 24)
        s1 = a2_swatch((102, 41, 23), -0.7, 2.15, 0.8, 0.55)
        x1 = a2_cross(OPX, 1.4)
        m1 = a2_mono_l("0.65", VX, 1.4, 24)
        rule1 = Line([-5.9, 0.98, 0], [-0.3, 0.98, 0], color=DIM, stroke_width=3)
        t2 = a2_mono_l("(0.26, 0.104, 0.0585)", VX, 0.45, 24)
        x2 = a2_cross(OPX, -0.35)
        m2 = a2_mono_l("255", VX, -0.35, 24)
        rule2 = Line([-5.9, -0.78, 0], [-0.3, -0.78, 0], color=DIM, stroke_width=3)
        t3 = a2_mono_l("(66, 27, 15)", VX, -1.25, 24)
        s3 = a2_swatch((66, 27, 15), -1.55, -1.25, 0.9, 0.6)
        # right panel: 3 activation values x 2 pixels (swatch + the example's predicted RGB8 under it)
        acts = [0.0, 0.5, 1.0]
        ys = [2.05, 0.9, -0.25]
        XL, XD, XG = 0.7, 2.2, 4.9
        heads = [a2_lab("dark", XD, 2.95, 36), a2_lab("light", XG, 2.95, 36)]
        labs = [a2_mono(f"{a:.1f}", XL, y, 24) for a, y in zip(acts, ys)]
        slots_d = [Rectangle(width=0.9, height=0.55, stroke_color=GHOST, stroke_width=3, fill_opacity=0).move_to([XD, y, 0]) for y in ys]
        slots_l = [Rectangle(width=0.9, height=0.55, stroke_color=GHOST, stroke_width=3, fill_opacity=0).move_to([XG, y, 0]) for y in ys]
        sw_d = [a2_swatch(A2_PRED[a][0], XD, y, 0.9, 0.55) for a, y in zip(acts, ys)]
        sw_l = [a2_swatch(A2_PRED[a][1], XG, y, 0.9, 0.55) for a, y in zip(acts, ys)]
        nums_d = [a2_mono("(%d, %d, %d)" % A2_PRED[a][0], XD, y - 0.5, 20) for a, y in zip(acts, ys)]
        nums_l = [a2_mono("(%d, %d, %d)" % A2_PRED[a][1], XG, y - 0.5, 20) for a, y in zip(acts, ys)]
        # the unshaded line of the shader (line 2), and the honesty tags
        code2 = a2_code([A2_SIGNAL[1]], x=3.3, y=-1.75, size=24, first=2, width=5.2)
        tag_hand = status_tag("computed by hand, not measured", -3.0, -2.55)
        tag_ex = example_tag(3.1, -3.12)

        until(self, "three uniform values", lead=0.1)
        self.play(*[FadeIn(m) for m in labs], *[Create(m) for m in slots_d], run_time=0.5)
        until(self, "two pixels", lead=0.1)
        self.play(*[FadeIn(m) for m in heads], *[Create(m) for m in slots_l], FadeIn(tag_hand), run_time=0.5)
        until(self, "quiet colour", lead=0.5)
        self.play(FadeIn(l_quiet), FadeIn(t1), FadeIn(s1), run_time=0.45)
        until(self, "times point six five", lead=0.0)
        self.play(FadeIn(x1), FadeIn(m1), Create(rule1), FadeIn(t2), run_time=0.5)
        until(self, "sixty-six", lead=0.25)
        self.play(FadeIn(x2), FadeIn(m2), Create(rule2), FadeIn(t3), FadeIn(s3), run_time=0.5)
        cp = s3.copy()
        self.play(cp.animate.move_to([XD, ys[0], 0]), FadeIn(nums_d[0]), FadeIn(tag_ex), run_time=0.5)
        self.play(*[FadeIn(sw_d[i]) for i in (1, 2)], *[FadeIn(sw_l[i]) for i in (0, 1, 2)], *[FadeIn(nums_d[i]) for i in (1, 2)],
                  *[FadeIn(nums_l[i]) for i in (0, 1, 2)], run_time=0.5)
        until(self, "Only unshaded", lead=0.1)
        self.play(Create(code2.frame), run_time=0.3)
        self.play(FadeIn(code2.rows), run_time=0.25)
        until(self, "keeps that arithmetic honest", lead=0.7)
        self.play(Create(code2.ring_line(2)), run_time=0.45)
        done(self)


# ─────────────────────────────────────────────── B16 · the hint experiment's predictions ───────────────────────────────────────────────
# "The hint experiment gets predictions too: greys sixty-four, one twenty-eight, one ninety-two, sampled with and without source color. By the S R G B formula, Forward Plus
#  leaves the colour read alone and brightens the data read to one thirty-seven, one eighty-eight, two twenty-five. On Compatibility, say so, and measure."
# A drawing of the assignment's encode function (assignment line 91; EVIDENCE-NOTES.md 'Predicted' table): x = byte / 255, y = encode(x). The colour read goes decode -> encode and
# lands back on the diagonal (unchanged); the data read is encoded once and climbs the curve: 64 -> 137, 128 -> 188, 192 -> 225. These are PREDICTIONS (no capture here).
def a2_encode(x):
    return 12.92 * x if x <= 0.0031308 else 1.055 * x ** (1 / 2.4) - 0.055


class B16_HintPredictions(Scene):
    def construct(self):
        GREYS = [64, 128, 192]
        PRED = [137, 188, 225]            # round(encode(b/255) * 255), checked by evidence/act2/verify_arithmetic.py
        px, py, pw, ph = -5.0, -2.0, 4.6, 3.6         # plot origin and size
        P = lambda xv, yv: [px + xv * pw, py + yv * ph, 0]
        plt = plot(a2_encode, (0, 1), (0, 1), size=(pw, ph), x=px + pw / 2, y=py + ph / 2, color=INK)
        diag = DashedLine(P(0, 0), P(1, 1), color=DIM, stroke_width=4, dash_length=0.14)
        xs = [b / 255 for b in GREYS]
        ys = [a2_encode(x) for x in xs]
        xt = [a2_mono(str(b), P(x, 0)[0], py - 0.38, 24) for b, x in zip(GREYS, xs)]
        yt = [a2_mono(str(v), px - 0.5, P(0, y)[1], 24) for v, y in zip(PRED, ys)]
        vdash = [DashedLine(P(x, 0), P(x, y), color=GHOST, stroke_width=3, dash_length=0.1) for x, y in zip(xs, ys)]
        hdash = [DashedLine(P(x, y), P(0, y), color=GHOST, stroke_width=3, dash_length=0.1) for x, y in zip(xs, ys)]
        d_diag = [Dot(P(x, x), radius=0.1, color=INK) for x in xs]
        d_curve = [Dot(P(x, x), radius=0.13, color=TERRA) for x in xs]            # start on the diagonal, climb to the curve
        # right: two rows of three bands
        BX = [1.9, 3.55, 5.2]
        R1, R2 = 1.0, -1.45
        row1 = [a2_swatch((g, g, g), x, R1, 1.2, 0.9) for g, x in zip(GREYS, BX)]
        row2 = [a2_swatch((g, g, g), x, R2, 1.2, 0.9) for g, x in zip(GREYS, BX)]
        n1 = [a2_mono(str(g), x, R1 - 0.7, 24) for g, x in zip(GREYS, BX)]
        n2 = [a2_mono(str(g), x, R2 - 0.7, 24) for g, x in zip(GREYS, BX)]
        n2_new = [a2_mono(str(v), x, R2 - 0.7, 24) for v, x in zip(PRED, BX)]
        s1 = VGroup(DashedLine([1.3, 2.05, 0], [1.85, 2.05, 0], color=DIM, stroke_width=4, dash_length=0.13), a2_mono_l("source_color", 2.05, 2.05, 24))
        s2 = VGroup(Line([1.3, -0.4, 0], [1.85, -0.4, 0], color=INK, stroke_width=5), a2_mono_l("no hint", 2.05, -0.4, 24))
        tag_pred = status_tag("predicted, not measured", 3.5, 2.95)
        tag_comp = status_tag("Compatibility: measure first", 3.1, -3.12)
        l_x = a2_lab("in the file", px + pw / 2, -2.9, 34, DIM)
        l_y = a2_lab("on screen", px + 0.75, 2.05, 34, DIM)

        until(self, "The hint experiment", lead=-0.1)
        self.play(FadeIn(tag_pred), run_time=0.4)
        until(self, "greys sixty-four", lead=0.15)
        self.play(FadeIn(row1[0]), FadeIn(n1[0]), FadeIn(row2[0]), FadeIn(n2[0]), run_time=0.35)
        until(self, "one twenty-eight", lead=0.1)
        self.play(FadeIn(row1[1]), FadeIn(n1[1]), FadeIn(row2[1]), FadeIn(n2[1]), run_time=0.35)
        until(self, "one ninety-two", lead=0.1)
        self.play(FadeIn(row1[2]), FadeIn(n1[2]), FadeIn(row2[2]), FadeIn(n2[2]), run_time=0.35)
        until(self, "with and without", lead=0.25)
        self.play(FadeIn(s1), FadeIn(s2), run_time=0.45)
        until(self, "By the S R G B formula", lead=0.3)
        self.play(Create(plt.axes), Create(diag), FadeIn(l_x), FadeIn(l_y), run_time=0.5)
        self.play(Create(plt.curve), *[FadeIn(m) for m in xt], run_time=0.7)
        until(self, "the colour read alone", lead=0.4)
        self.play(*[GrowFromCenter(d) for d in d_diag], run_time=0.45)
        until(self, "brightens the data read", lead=0.1)
        self.play(*[GrowFromCenter(d) for d in d_curve], run_time=0.3)
        self.play(*[d.animate.move_to(P(x, y)) for d, x, y in zip(d_curve, xs, ys)], *[Create(v) for v in vdash], run_time=0.7)
        for i, ph_ in enumerate(["one thirty-seven", "one eighty-eight", "two twenty-five"]):
            until(self, ph_, lead=0.1)
            self.play(Create(hdash[i]), FadeIn(yt[i]), row2[i].animate.set_fill(a2_hex((PRED[i],) * 3)), FadeOut(n2[i]), FadeIn(n2_new[i]), run_time=0.5)
        until(self, "On Compatibility", lead=0.15)
        self.play(FadeIn(tag_comp), run_time=0.45)
        done(self)


# ─────────────────────────────────────────────── B17 · the material plan and the four predicted failures ───────────────────────────────────────────────
# "The material plan names each texture's role and import settings, and each uniform's type, range, default and group. Predict at least three failures, with their checks.
#  The example predicted four: a missing colour hint, an undeclared uniform, a shader edit changing both materials, and a headless pass that cannot certify colour."
# Phase 1 (before the midpoint): the example's plan board. Textures: gate-color.png (colour, source_color) and gate-roughness.png (data, no hint), both imported with
# compress/mode=0 (Lossless), compress/normal_map=2 (Disabled), mipmaps/generate=false (gate-*.png.import lines 18, 24, 26; MATERIALS.md rows). Uniforms: surface.gdshader lines 5, 6, 8, 9
# with the groups of lines 2 and 7. Phase 2 (after it): three empty failure/check panels, then the example's four (CHANGE-BRIEF-a5.md 'Predictions'), each with the check that catches it:
# a headless test (colour hint: contract test 'color hint'; uniform name: 'declared <name>') or your eyes (shared shader vs one material: native captures; colour: 'a headless pass cannot certify color').
class B17_MaterialPlan(Scene):
    def construct(self):
        # ---- plan board
        th1 = framed(a2_img("ev_tex_color.png", h=1.0, at=(-5.35, 1.75)))
        th2 = framed(a2_img("ev_tex_rough.png", h=1.0, at=(-5.35, 0.35)))
        n1 = a2_mono_l("gate-color.png", -4.65, 2.05, 24)
        r1 = VGroup(a2_lab_l("colour", -4.65, 1.45, 36), a2_mono_l("source_color", -3.0, 1.45, 24))
        n2 = a2_mono_l("gate-roughness.png", -4.65, 0.65, 24)
        r2 = VGroup(a2_lab_l("data", -4.65, 0.05, 36), a2_mono_l("no hint", -3.4, 0.05, 24))
        imp_h = a2_lab_l("import", -5.9, -1.05, 36, DIM)
        imp = VGroup(a2_lab_l("lossless", -4.4, -1.05, 36), a2_lab_l("normal map: disabled", -4.4, -1.65, 36), a2_lab_l("mipmaps: off", -4.4, -2.25, 36))
        g1 = box(3.5, 1.45, 4.9, 2.1, DIM, 5)
        g1t = a2_lab_l("Surface", 1.25, 2.05, 38)
        g1r = VGroup(a2_mono_l("tint", 1.25, 1.4, 24), a2_mono_l("vec4", 4.35, 1.4, 24, DIM), a2_mono_l("roughness_gain", 1.25, 0.85, 24), a2_mono_l("float", 4.35, 0.85, 24, DIM))
        g2 = box(3.5, -1.15, 4.9, 2.1, DIM, 5)
        g2t = a2_lab_l("Pattern", 1.25, -0.65, 38)
        g2r = VGroup(a2_mono_l("uv_scale", 1.25, -1.3, 24), a2_mono_l("float", 4.35, -1.3, 24, DIM), a2_mono_l("metallic_gain", 1.25, -1.85, 24), a2_mono_l("float", 4.35, -1.85, 24, DIM))
        # ---- panels
        PC = [(-3.1, 1.1), (3.1, 1.1), (-3.1, -1.15), (3.1, -1.15)]
        panels = [box(x, y, 5.8, 1.9, DIM, 5) for x, y in PC]
        ph_lab = [a2_lab_l("failure", x - 2.55, y, 36) for x, y in PC]
        ph_chk = [Circle(radius=0.34, stroke_color=DIM, stroke_width=5, fill_opacity=0).move_to([x + 2.05, y + 0.2, 0]) for x, y in PC]
        ph_cl = [a2_lab("check", x + 2.05, y - 0.52, 32) for x, y in PC]
        labels = ["colour hint", "uniform name", "shader vs material", "headless vs colour"]
        real_lab = [a2_lab_l(t, x - 2.55, y, 40) for t, (x, y) in zip(labels, PC)]
        icons = [terminal_icon(PC[0][0] + 2.05, PC[0][1], 0.5), terminal_icon(PC[1][0] + 2.05, PC[1][1], 0.5),
                 eye_icon(PC[2][0] + 2.05, PC[2][1], 0.5), eye_icon(PC[3][0] + 2.05, PC[3][1], 0.5)]
        tag_ex = example_tag(3.1, -3.12)

        until(self, "each texture's role", lead=0.1)
        self.play(FadeIn(th1), FadeIn(n1), FadeIn(r1), FadeIn(tag_ex), run_time=0.4)
        self.play(FadeIn(th2), FadeIn(n2), FadeIn(r2), run_time=0.4)
        until(self, "import settings", lead=0.15)
        self.play(FadeIn(imp_h), FadeIn(imp), run_time=0.5)
        until(self, "each uniform's type", lead=0.15)
        self.play(Create(g1), FadeIn(g1t), FadeIn(g1r), run_time=0.5)
        until(self, "range, default", lead=0.35)
        self.play(Create(g2), FadeIn(g2t), FadeIn(g2r), run_time=0.5)
        until(self, "Predict at least three", lead=0.2)
        board = [th1, th2, n1, r1, n2, r2, imp_h, imp, g1, g1t, g1r, g2, g2t, g2r]
        self.play(*[FadeOut(m) for m in board], run_time=0.4)
        self.play(*[Create(panels[i]) for i in range(3)], *[FadeIn(ph_lab[i]) for i in range(3)], *[Create(ph_chk[i]) for i in range(3)], *[FadeIn(ph_cl[i]) for i in range(3)], run_time=0.7)
        until(self, "The example predicted four", lead=0.0)
        self.play(Create(panels[3]), FadeIn(ph_lab[3]), Create(ph_chk[3]), FadeIn(ph_cl[3]), run_time=0.4)
        for i, ph_ in enumerate(["a missing colour hint", "an undeclared uniform", "a shader edit", "a headless pass"]):
            until(self, ph_, lead=0.15)
            self.play(FadeOut(ph_lab[i]), FadeOut(ph_chk[i]), FadeOut(ph_cl[i]), FadeIn(real_lab[i]), FadeIn(icons[i]), run_time=0.45)
        done(self)


# ─────────────────────────────────────────────── B18 · five questions, and frame counting ───────────────────────────────────────────────
# "Then five questions: the renderer the project names, the colour arriving in fragment, how long a frame-counting version lasts at three frame rates, where the default lives,
#  and whether hint range clamps a value set from code."  (the assignment's five short questions, in its own order)
# Five numbered dots land on their words (a terracotta dot is the pointer). Question 3 opens a small sum for an ILLUSTRATIVE 36-frame effect, NOT the example's:
# 36 frames at 30, 60 and 144 frames per second last 1.2 s, 0.6 s and 0.25 s (verify_arithmetic.py). The bars are drawn to scale (same unit per second).
class B18_FiveQuestions(Scene):
    def construct(self):
        QY = [2.45, 1.3, 0.15, -1.0, -2.15]
        words = ["renderer", "colour", "frames", "default", "clamp?"]
        dots = [VGroup(Circle(radius=0.36, stroke_color=INK, stroke_width=5, fill_opacity=0).move_to([-5.4, y, 0]), a2_lab(str(i + 1), -5.4, y, 36)) for i, y in enumerate(QY)]
        labs = [a2_lab_l(w, -4.75, y, 40) for w, y in zip(words, QY)]
        pointer = Dot([-6.05, QY[0], 0], radius=0.13, color=TERRA)
        # the sum (right)
        tag = status_tag("illustrative: 36 frames", 2.7, 2.85)
        RY = [1.7, 0.45, -0.8]
        FPS = [30, 60, 144]
        SEC = [1.2, 0.6, 0.25]
        SEC_S = ["1.2 s", "0.6 s", "0.25 s"]
        k = 4.5                                           # bar units per second
        fl = [a2_lab_l(f"{f} fps", -1.3, y, 36) for f, y in zip(FPS, RY)]
        ex = [a2_mono_l(f"36 / {f} = {t}", 0.5, y, 32) for f, t, y in zip(FPS, SEC_S, RY)]
        bars = [Rectangle(width=k * t, height=0.22, stroke_width=0, fill_color=BAR1, fill_opacity=1).move_to([-1.3 + k * t / 2, y - 0.5, 0]) for t, y in zip(SEC, RY)]
        rows = [VGroup(fl[i], ex[i]) for i in range(3)]

        until(self, "the renderer", lead=0.1)
        self.play(FadeIn(dots[0]), FadeIn(labs[0]), FadeIn(pointer), run_time=0.4)
        until(self, "the colour arriving", lead=0.1)
        self.play(FadeIn(dots[1]), FadeIn(labs[1]), pointer.animate.move_to([-6.05, QY[1], 0]), run_time=0.4)
        until(self, "how long a", lead=0.2)
        self.play(FadeIn(dots[2]), FadeIn(labs[2]), pointer.animate.move_to([-6.05, QY[2], 0]), FadeIn(tag), run_time=0.4)
        until(self, "frame-counting", lead=0.1)
        self.play(FadeIn(rows[0]), GrowFromEdge(bars[0], LEFT), run_time=0.5)
        until(self, "three frame rates", lead=0.3)
        self.play(FadeIn(rows[1]), GrowFromEdge(bars[1], LEFT), run_time=0.45)
        self.play(FadeIn(rows[2]), GrowFromEdge(bars[2], LEFT), run_time=0.45)
        until(self, "where the default lives", lead=0.15)
        self.play(FadeIn(dots[3]), FadeIn(labs[3]), pointer.animate.move_to([-6.05, QY[3], 0]), run_time=0.4)
        until(self, "whether hint range clamps", lead=0.15)
        self.play(FadeIn(dots[4]), FadeIn(labs[4]), pointer.animate.move_to([-6.05, QY[4], 0]), run_time=0.4)
        done(self)
