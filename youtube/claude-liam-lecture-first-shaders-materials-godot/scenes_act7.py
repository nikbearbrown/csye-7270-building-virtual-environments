"""ACT VII · Read the Language  (B49-B55, B55B, Manim)

One cast for the act: the REAL generated shader (standard_generated.gdshader, 48 lines, Godot 4.7.2's own conversion of the example's
StandardMaterial3D; sha256 ca1c191c44fb614ae64a258fce3efbc13b77fdc82f480e98ac4582e30805650d, evidence/example/conversion-receipt.json) shown
in the REAL Godot Shader Editor (captures/editor/, strips cut by evidence/act5/make_editor_crops.py), the example's own three shaders
(embedded below verbatim with their real line numbers, checked by evidence/act5/verify_embedded.py) and the flat 3 x 2 pad quad of
render-material-evidence.gd:29 for the corner arithmetic. Editor frames are labelled "scripted editor session"; the menu was opened in
a scratch copy (nothing converted or saved). Drawings of ideas (B52, B54, B55) are labelled and never styled as Godot.
"""

A7P = "pantry/"

# REAL source lines, embedded verbatim (Gate A runs scenes.py from a folder with no evidence/); evidence/act5/verify_embedded.py checks them.
A7_REAL = {'signal.gdshader': {1: 'shader_type spatial;', 3: 'uniform float activation : hint_range(0.0, 1.0) = 0.0;'},
 'surface.gdshader': {1: 'shader_type spatial;',
                      3: 'uniform sampler2D color_map : source_color, filter_nearest;',
                      12: '\tROUGHNESS = clamp(texture(roughness_map, UV * uv_scale).r * roughness_gain, 0.05, 1.0);'},
 'hint.gdshader': {1: 'shader_type spatial;',
                   3: 'uniform sampler2D as_color : source_color, filter_nearest;',
                   4: 'uniform sampler2D as_data : filter_nearest;',
                   9: '\tALBEDO = use_color ? texture(as_color, UV).rgb : texture(as_data, UV).rgb;',
                   10: '\tif (show_screen_grid && mod(FRAGCOORD.x, VIEWPORT_SIZE.x / 8.0) < 2.0) {'},
 'standard_generated.gdshader': {3: 'shader_type spatial;',
                                 4: 'render_mode blend_mix, depth_draw_opaque, cull_back, diffuse_burley, specular_schlick_ggx;',
                                 6: 'uniform vec4 albedo : source_color;',
                                 7: 'uniform sampler2D texture_albedo : source_color, filter_linear_mipmap, repeat_enable;',
                                 19: 'uniform sampler2D texture_normal : hint_roughness_normal, filter_linear_mipmap, repeat_enable;',
                                 20: 'uniform float normal_scale : hint_range(-16.0, 16.0);',
                                 35: '\tALBEDO = albedo.rgb * albedo_tex.rgb;',
                                 43: '\tROUGHNESS = roughness_tex * roughness;',
                                 46: '\tNORMAL_MAP = texture(texture_normal, base_uv).rgb;'},
 'standard-source.tres': {6: 'albedo_color = Color(0.85, 0.8, 0.7, 1)',
                          7: 'albedo_texture = ExtResource("1")',
                          10: 'roughness_texture = ExtResource("2")',
                          13: 'normal_texture = ExtResource("3")'}}


# REAL log lines of evidence/act7/vertex_albedo_check.log (verbatim, leading spaces kept); verify_embedded.py checks them.
A7_LOG = ['    2 | void vertex() {', 'E   3->  ALBEDO = vec3(1.0);', "SHADER ERROR: Unknown identifier in expression: 'ALBEDO'."]

A7_CW = {20: 0.15, 24: 0.2}            # measured Menlo units per character
A7_LH = {20: 0.2875, 24: 0.345}        # default row pitch (size / 32 * 0.46)


def a7_line(fname, n):
    return A7_REAL[fname][n]


def a7_lab(s, x, y, size=34, color=INK, left=False):
    t = T(s, size, color)
    if left:
        return t.move_to([x, y, 0], aligned_edge=LEFT)
    return t.move_to([x, y, 0])


def a7_img(name, h=None, w=None, at=(0.0, 0.0)):
    im = ImageMobject(A7P + name)
    try:
        im.set_resampling_algorithm(RESAMPLING_ALGORITHMS["linear"])   # bicubic rings near light-on-dark text and breaks GATE T's ink mask
    except Exception:
        pass
    if h is not None:
        im.set_height(h)
    if w is not None:
        im.set_width(w)
    return im.move_to(np.array([at[0], at[1], 0.0]))


def a7_hook(x, y, s=0.13):
    """The wrap mark: a drawn elbow (down, then left with a small head). A shape, not a glyph."""
    return VGroup(Line([x, y + s * 0.6, 0], [x, y - s * 0.7, 0], color=DIM, stroke_width=4),
                  Line([x, y - s * 0.7, 0], [x - s * 1.4, y - s * 0.7, 0], color=DIM, stroke_width=4),
                  Line([x - s * 1.4, y - s * 0.7, 0], [x - s * 0.8, y - s * 0.2, 0], color=DIM, stroke_width=4),
                  Line([x - s * 1.4, y - s * 0.7, 0], [x - s * 0.8, y - s * 1.2, 0], color=DIM, stroke_width=4))


def a7_split(text, budget):
    """Soft-wrap `text` at the last space at or before `budget` characters, preferring a space after a comma/&&/colon.
    Returns a list of pieces (characters verbatim; only the breaking space is dropped)."""
    if len(text) <= budget:
        return [text]
    cut = text.rfind(" ", 0, budget + 1)
    if cut <= 0:
        return [text]
    return [text[:cut]] + a7_split(text[cut + 1:], budget)


class A7Code:
    """Real code rows: Menlo, real line numbers, outline-only frame, optional gap markers and wraps.
    spec: list of (real_line_number, text) or None (a gap marker). `dedent` strips the common leading tab(s).
    Attributes: .group (frame + rows + marks), .frame, .W, .H, .pitch, .cw, .size; rows(n) -> VGroup of line n (number + pieces);
    ring(n) -> terracotta ring round the whole line n; tok(n, token, k=0) -> (cx, cy, w) of a token; piece_y(n, i)."""

    def __init__(self, spec, x=0.0, y=0.0, size=20, wrap=None, dedent=True, pad=0.3, pitch=None, gap=0.32, width=None, extra=0.0):
        self.size, self.cw = size, A7_CW[size]
        self.pitch = pitch or A7_LH[size]
        items = []
        tabs = [len(t) - len(t.lstrip("\t")) for s in spec if s for t in [s[1]] if t.strip()]
        cut = min(tabs) if (dedent and tabs) else 0
        for s in spec:
            if s is None:
                items.append(("gap", None, None, None, 0))
                continue
            n, t = s
            t = t[cut:] if t.startswith("\t" * cut) else t
            t = t.replace("\t", "    ")
            lead = len(t) - len(t.lstrip(" "))
            pieces = a7_split(t, wrap) if wrap else [t]
            for i, p in enumerate(pieces):
                items.append(("row", n if i == 0 else None, p, i, lead))
        digits = max(len(str(s[0])) for s in spec if s)
        self.nw = digits * self.cw + 0.25
        longest = max(len(p) + ((ld + 2) if i else 0) for k, n, p, i, ld in items if k == "row")
        self.W = width or (longest * self.cw + self.nw + 2 * pad + extra)
        h = sum(self.pitch if it[0] == "row" else gap for it in items)
        self.H = h + 2 * pad
        self.x, self.y, self.pad = x, y, pad
        self.frame = RoundedRectangle(width=self.W, height=self.H, corner_radius=0.14, stroke_color=DIM, stroke_width=4, fill_opacity=0).move_to([x, y, 0])
        self.text_left = x - self.W / 2 + pad + self.nw
        self.rows_, self.pos, self.marks, self.hooks = {}, {}, VGroup(), VGroup()
        cy = y + self.H / 2 - pad
        cur = None
        for k, n, p, i, ld in items:
            if k == "gap":
                cy -= gap
                self.marks.add(*[Dot([self.x - self.W / 2 + pad + self.nw * 0.5, cy + gap / 2 + dy, 0], radius=0.035, color=DIM) for dy in (-0.07, 0.0, 0.07)])
                continue
            yy = cy - self.pitch / 2
            cy -= self.pitch
            ind = (ld + 2) * self.cw if i else 0.0
            tx = M(p if p else " ", self.size)
            lead_p = len(p) - len(p.lstrip(" "))            # Text() drops leading spaces: place by character column so indentation is kept
            tx.move_to([self.text_left + ind + lead_p * self.cw + tx.width / 2, yy, 0])
            grp = VGroup(tx)
            if n is not None:
                nm = M(str(n), self.size, DIM)
                nm.move_to([self.text_left - 0.25 - nm.width / 2, yy, 0])
                grp.add(nm)
                cur = n
                self.rows_[n] = VGroup()
                self.pos[n] = []
            self.rows_[cur].add(grp)
            self.pos[cur].append((yy, p, ind))
            if i:
                prev = self.pos[cur][i - 1]
                hk = a7_hook(self.text_left + prev[2] + len(prev[1]) * self.cw + 0.2, prev[0])
                self.hooks.add(hk)
        self.group = VGroup(self.frame, *[r for r in self.rows_.values()], self.marks, self.hooks)

    def rows(self, n):
        return self.rows_[n]

    def piece_y(self, n, i=0):
        return self.pos[n][i][0]

    def ring(self, n, color=TERRA, sw=6, shrink=0.8, pieces=None):
        """One flat terracotta ring per visual row of line n (GATE T reads a ring whose width/height < 15 as accent TEXT, so a
        wrapped line gets one ring per piece and the rings never touch)."""
        rs = VGroup()
        for i, (yy, p, ind) in enumerate(self.pos[n]):
            if pieces is not None and i not in pieces:
                continue
            rs.add(RoundedRectangle(width=self.W - 0.3, height=self.pitch * shrink, corner_radius=0.1, stroke_color=color, stroke_width=sw,
                                    fill_opacity=0).move_to([self.x, yy, 0]))
        return rs

    def tok(self, n, token, k=0):
        for yy, p, ind in self.pos[n]:
            i = -1
            for _ in range(k + 1):
                i = p.find(token, i + 1)
                if i < 0:
                    break
            if i >= 0:
                w = len(token) * self.cw
                return (self.text_left + ind + i * self.cw + w / 2, yy, w)
        raise ValueError(f"token {token!r} not in line {n}")

    def tok_ring(self, n, token, k=0, color=TERRA, sw=5, padx=0.05):
        cx, cy, w = self.tok(n, token, k)
        return RoundedRectangle(width=w + 2 * padx, height=self.pitch * 0.9, corner_radius=0.07, stroke_color=color, stroke_width=sw, fill_opacity=0).move_to([cx, cy, 0])


def a7_mono(s, x, y, size=24, color=INK, left=False):
    t = M(s, size, color)
    if left:
        return t.move_to([x, y, 0], aligned_edge=LEFT)
    return t.move_to([x, y, 0])


def a7_x(x, y, s=0.1, w=5):
    """A multiplication mark drawn as a shape."""
    return cross_mark(x, y, s, INK, w)


def a7_chip(cx, y, rgb, text, size=34, sw=0.7, sh=0.5):
    """A real texel value: a swatch of the real colour + its real numbers (BESIDE it), the pair centred on cx."""
    tx = T(text, size)
    total = sw + 0.15 + tx.width
    x0 = cx - total / 2
    sq = swatch(rgb, x0 + sw / 2, y, sw, sh)
    fr = Rectangle(width=sw, height=sh, stroke_color=DIM, stroke_width=3, fill_opacity=0).move_to([x0 + sw / 2, y, 0])
    tx.move_to([x0 + sw + 0.15, y, 0], aligned_edge=LEFT)
    return VGroup(sq, fr, tx)


def a7_row_y(top, py, scale):
    """Scene y of pixel row py of a crop whose top edge sits at scene y `top`, shown at `scale` x native (1 unit = 270 px at 4K)."""
    return top - py * scale / 270.0




def a7_pill(text, x, y, w, size=26, h=0.62):
    """A white mono pill (no outline), 0.62 high: a name of a real built-in or output."""
    lab = M(text, size)
    shadow = pill(x + 0.07, y - 0.07, w, h=h, fill=BOX_L)
    p = pill(x, y, w, h=h)
    lab.move_to([x, y, 0])
    return VGroup(shadow, p, lab)


def a7_doc(x, y, w=1.5, h=1.9):
    """A drawn page (a file): outline, three ghost text lines."""
    page = RoundedRectangle(width=w, height=h, corner_radius=0.1, stroke_color=INK, stroke_width=5, fill_opacity=0).move_to([x, y, 0])
    lines = VGroup(*[Line([x - w * 0.3, y + h * 0.26 - i * 0.3, 0], [x + w * 0.3 - (0.4 if i == 3 else 0.0), y + h * 0.26 - i * 0.3, 0],
                          color=BAR2, stroke_width=6) for i in range(4)])
    return VGroup(page, lines)


def a7_no(x, y, r=0.3, sw=7):
    """A prohibition mark (ink ring + bar): shapes only, drawn over an arrow, never over type."""
    ring_ = Circle(radius=r, stroke_color=INK, stroke_width=sw).move_to([x, y, 0])
    d = r * 0.7071
    return VGroup(ring_, Line([x - d, y + d, 0], [x + d, y - d, 0], color=INK, stroke_width=sw))


# ── B49 · convert a StandardMaterial3D, save the generated code ──────────────────────────────────────────────────
class B49_ConvertMaterial(Scene):
    def construct(self):
        title = T("Read  the  Language", 40).move_to([-6.0, 2.95, 0], aligned_edge=LEFT)
        self.add(title)
        SC = 1.35
        godot = logo_chip("godot", -3.2, 0.5, h=1.5)
        doc = a7_doc(1.7, 0.5)
        dn = a7_mono("standard_generated.gdshader", 1.7, -0.95, 20)
        ar0 = arrow([-1.9, 0.5, 0], [0.6, 0.5, 0], INK, 6, 0.24)
        s0 = Group(godot, doc, dn, ar0)
        until(self, "Last build step", lead=-0.3)
        self.play(FadeIn(godot), run_time=0.4)
        until(self, "read the shader", lead=0.2)
        self.play(GrowArrow(ar0), FadeIn(doc), FadeIn(dn), run_time=0.5)
        # the example's StandardMaterial3D as the editor shows it (albedo, roughness and normal textures)
        cxl, cxr, cyc = -3.6, 3.6, -0.15
        im5b = framed(a7_img("a7_ed_f5b_textures.png", w=900 * SC / 270.0, at=(cxl, cyc)), pad=0.05)
        top5b = cyc + 1005 * SC / 270.0 / 2
        left5b = cxl - 900 * SC / 270.0 / 2
        until(self, "Make a standard material", lead=0.35)
        self.play(FadeOut(s0), FadeIn(im5b), run_time=0.45)
        py = {"albedo": 177, "normal": 934, "roughness": 586}
        dots = {k: Dot([left5b - 0.25, a7_row_y(top5b, v, SC), 0], radius=0.1, color=TERRA) for k, v in py.items()}
        for k, ph in (("albedo", "with albedo"), ("normal", "normal and"), ("roughness", "roughness textures")):
            until(self, ph, lead=0.25)
            self.play(FadeIn(dots[k], scale=0.4), run_time=0.25)
        until(self, "make it unique", lead=0.15)
        mu = chip("Make Unique", 0.0, 0.5, w=2.55, size=32)
        a_mu = arrow([1.45, 0.5, 0], [1.1, 0.5, 0], INK, 5, 0.18)
        self.play(FadeIn(mu), run_time=0.3)
        until(self, "convert it to a shader material", lead=0.2)
        im5e = framed(a7_img("a7_ed_f5e_menu.png", w=900 * SC / 270.0, at=(cxr, cyc)), pad=0.05)
        top5e = cyc + 1050 * SC / 270.0 / 2
        y_conv = a7_row_y(top5e, 982, SC)
        self.play(FadeOut(mu), FadeOut(VGroup(*dots.values())), FadeIn(im5e), run_time=0.45)
        t1 = status_tag("scripted editor session", -3.6, -3.1)
        t2 = status_tag("menu opened in a scratch copy", 3.4, -3.1)
        self.add(t1, t2)
        until(self, "in the Inspector", lead=0.1)
        dc = Dot([cxr - 450 * SC / 270.0 - 0.25, y_conv, 0], radius=0.11, color=TERRA)
        self.play(FadeIn(dc, scale=0.4), run_time=0.3)
        until(self, "Save the code", lead=0.55)
        self.play(FadeOut(Group(im5b, im5e, dc, t1, t2)), run_time=0.25)
        doc2 = a7_doc(-3.4, 0.5)
        dn2 = a7_mono("standard_generated.gdshader", -3.4, -0.95, 20)
        n48 = a7_lab("48 lines", -3.4, -1.55, 34)
        self.play(FadeIn(doc2), FadeIn(dn2), FadeIn(n48), run_time=0.35)
        until(self, "never uses it", lead=1.5)
        game = VGroup(box(3.3, 0.5, 2.2, 1.1, DIM, 4), a7_lab("game", 3.3, 0.5, 38))
        dash = DashedLine([-2.4, 0.5, 0], [2.1, 0.5, 0], color=INK, stroke_width=5, dash_length=0.2)
        no = a7_no(-0.15, 0.5)
        self.play(Create(dash), FadeIn(game), run_time=0.35)
        self.play(Create(no), run_time=0.25)
        self.add(example_tag(2.9, -3.05))
        done(self)


# ── B50 · the generated file's lines ─────────────────────────────────────────────────────────────────────────────
# (The same lines in the REAL Shader Editor are in captures/editor/ F1a/F1b and cut to pantry/a7_ed_gen_*.png; dark code strips fail GATE T at 4K
#  with light-on-dark glyph halos, so the picture shows the file's real text on the stage and B49 carries the real editor frames.)
class B50_GeneratedLines(Scene):
    def construct(self):
        L = lambda n: (n, a7_line("standard_generated.gdshader", n))
        spec = [L(3), L(4), None, L(6), L(7), None, L(19), None, L(35), None, L(43), None, L(46)]
        blk = A7Code(spec, x=-1.25, y=0.15, size=20, wrap=60, pitch=0.38, gap=0.26, pad=0.2, dedent=False, extra=0.35)
        self.add(blk.frame)
        until(self, "In the generated file", lead=0.1)
        self.play(FadeIn(VGroup(*[blk.rows(n) for n in (3, 4, 6, 7, 19, 35, 43, 46)])), FadeIn(blk.marks), FadeIn(blk.hooks), run_time=0.5)
        ring = lambda n: blk.ring(n, pieces=(0,))
        until(self, "lines three and four", lead=0.6)
        r3, r4 = ring(3), ring(4)
        self.play(Create(r3), run_time=0.3)
        self.play(FadeOut(r3), Create(r4), run_time=0.3)
        until(self, "line six", lead=0.5)
        r6 = ring(6)
        self.play(FadeOut(r4), Create(r6), run_time=0.3)
        until(self, "says source color", lead=1.0)
        r7 = ring(7)
        tick = check(4.45, blk.piece_y(7), s=0.22, color=INK, w=8)
        l_c = a7_lab("colour", 5.4, blk.piece_y(7) - 0.05, 36)
        self.play(FadeOut(r6), Create(r7), Create(tick), FadeIn(l_c), run_time=0.35)
        until(self, "line nineteen", lead=0.3)
        r19 = ring(19)
        circ = open_circle(4.45, blk.piece_y(19), 0.17, INK, 6)
        l_d = a7_lab("data", 5.4, blk.piece_y(19) - 0.05, 36)
        self.play(FadeOut(r7), Create(r19), Create(circ), FadeIn(l_d), run_time=0.35)
        until(self, "written at thirty-five", lead=0.8)
        r35 = ring(35)
        self.play(FadeOut(r19), Create(r35), run_time=0.3)
        until(self, "roughness at forty-three", lead=0.7)
        r43 = ring(43)
        self.play(FadeOut(r35), Create(r43), run_time=0.3)
        until(self, "normal map at forty-six", lead=0.8)
        r46 = ring(46)
        self.play(FadeOut(r43), Create(r46), run_time=0.3)
        self.add(example_tag(3.1, -3.1))
        done(self)


# ── B51 · Q1: what the shader type decides ──────────────────────────────────────────────────────────────────────
A7_TYPES = ["spatial", "canvas_item", "particles", "sky", "fog", "texture_blit"]     # the six shader_type values of Godot 4.7.2 (see factcheck/act7.md)


class B51_ShaderType(Scene):
    def construct(self):
        xs = [-5.6 + 0.8 * k for k in range(8)]
        circles = [Circle(radius=0.3, stroke_color=INK, stroke_width=5).move_to([x, 2.65, 0]) for x in xs]
        nums = [T(str(k + 1), 32).move_to([x, 2.65, 0]) for k, x in enumerate(xs)]
        until(self, "Then eight questions", lead=0.0)
        self.play(LaggedStart(*[AnimationGroup(Create(c), FadeIn(n)) for c, n in zip(circles, nums)], lag_ratio=0.12), run_time=1.3)
        rows = [("signal.gdshader:1", a7_line("signal.gdshader", 1)), ("surface.gdshader:1", a7_line("surface.gdshader", 1)), ("hint.gdshader:1", a7_line("hint.gdshader", 1))]
        blk = A7Code(rows, x=-1.6, y=0.45, size=24, pitch=0.8, dedent=False)
        until(self, "with line references", lead=0.1)
        self.play(Create(blk.frame), FadeIn(VGroup(*[blk.rows(k) for k, _ in rows])), run_time=0.6)
        until(self, "What does the shader type decide", lead=0.2)
        dot1 = Dot([xs[0], 2.2, 0], radius=0.09, color=TERRA)
        head = a7_mono("shader_type", 4.7, 2.65, 24, DIM)
        ys = [1.85 - 0.55 * i for i in range(len(A7_TYPES))]
        items = [a7_mono(t, 3.95, y, 24, left=True) for t, y in zip(A7_TYPES, ys)]
        self.play(FadeIn(dot1, scale=0.4), FadeIn(head), LaggedStart(*[FadeIn(i) for i in items], lag_ratio=0.12), run_time=0.9)
        until(self, "Which functions and built-ins exist", lead=0.2)
        c1, c2 = chip("functions", 4.75, -1.75, w=2.6, size=32), chip("built-ins", 4.75, -2.6, w=2.6, size=32)
        self.play(FadeIn(c1), run_time=0.3)
        self.play(FadeIn(c2), run_time=0.3)
        until(self, "All three example shaders", lead=0.6)
        sp = Dot([3.62, ys[0], 0], radius=0.1, color=TERRA)
        rr = [blk.ring(k, shrink=0.45) for k, _ in rows]
        self.play(FadeIn(sp, scale=0.4), Create(rr[0]), run_time=0.3)
        until(self, "example shaders", lead=0.6)
        self.play(FadeOut(rr[0]), Create(rr[1]), run_time=0.3)
        until(self, "say spatial", lead=0.6)
        self.play(FadeOut(rr[1]), Create(rr[2]), run_time=0.3)
        self.add(example_tag(-2.95, -3.1))
        done(self)


# ── B52 · Q2: fragment per pixel, vertex per corner; the colour line cannot live in vertex() ───────────────────────
class B52_PerPixelPerCorner(Scene):
    def construct(self):
        W_, H_, XL, XR, YQ = 4.2, 2.625, -3.4, 3.4, 0.55           # the flat 3 x 2 quad of render-material-evidence.gd:29, drawn 4.2 x 2.625 (cells 16 x 10)
        qL = Rectangle(width=W_, height=H_, stroke_color=INK, stroke_width=5).move_to([XL, YQ, 0])
        qR = Rectangle(width=W_, height=H_, stroke_color=INK, stroke_width=5).move_to([XR, YQ, 0])
        lf, lv = a7_mono("fragment()", XL, 2.5, 28), a7_mono("vertex()", XR, 2.5, 28)
        ill = status_tag("illustrative", -4.7, -3.1)
        until(self, "Which functions did you write", lead=0.0)
        self.play(Create(qL), Create(qR), FadeIn(lf), FadeIn(lv), FadeIn(ill), run_time=0.6)
        grid = pixel_grid(16, 10, W_ / 16, XL, YQ, DIM, 2)
        until(self, "Fragment runs for every pixel", lead=0.2)
        self.play(FadeIn(grid), run_time=0.3)
        anims = [tint(grid.cells[r][c], BAR1 if c % 2 == 0 else BAR3) for c in range(16) for r in range(10)]
        self.play(LaggedStart(*anims, lag_ratio=0.006), run_time=1.3)
        until(self, "vertex, once per corner", lead=0.2)
        cs = [(XR - W_ / 2, YQ + H_ / 2), (XR + W_ / 2, YQ + H_ / 2), (XR - W_ / 2, YQ - H_ / 2), (XR + W_ / 2, YQ - H_ / 2)]
        dots = [Dot([x, y, 0], radius=0.13, color=INK) for x, y in cs]
        self.play(LaggedStart(*[FadeIn(d, scale=0.4) for d in dots], lag_ratio=0.2), run_time=0.6)
        stageA = Group(qL, qR, lf, lv, grid, *dots, ill)
        # stage B: the colour line written inside vertex() does not compile (the REAL log of a Godot 4.7.2 run)
        until(self, "Move the colour line into vertex", lead=0.3)
        self.play(FadeOut(stageA), run_time=0.3)
        cw = 0.2
        rowsB = [M(t, 24) for t in A7_LOG]
        wB = max(len(t) for t in A7_LOG) * cw + 0.6
        frame = RoundedRectangle(width=wB, height=len(A7_LOG) * 0.5 + 0.6, corner_radius=0.14, stroke_color=DIM, stroke_width=4, fill_opacity=0).move_to([0, 1.5, 0])
        for k, (t, tx) in enumerate(zip(A7_LOG, rowsB)):
            tx.move_to([-wB / 2 + 0.3 + (len(t) - len(t.lstrip(' '))) * cw + tx.width / 2, 1.5 + 0.5 - 0.5 * k, 0])
        self.play(Create(frame), FadeIn(VGroup(*rowsB)), run_time=0.5)
        until(self, "it will not compile", lead=1.0)
        xm = cross_mark(-1.6, -0.4, 0.3, INK, 10)
        t_re = status_tag("re-run for this film", 1.3, -0.4)
        self.play(Create(xm), FadeIn(t_re), run_time=0.4)
        until(self, "albedo is a fragment output", lead=0.5)
        p_fr = a7_pill("fragment()", -2.6, -1.8, 2.9, size=28, h=0.7)
        p_al = a7_pill("ALBEDO", 2.6, -1.8, 2.3, size=28, h=0.7)
        a_ou = arrow([-1.0, -1.8, 0], [1.3, -1.8, 0], INK, 6, 0.22)
        l_ou = a7_lab("output", 0.15, -1.3, 34)
        self.play(FadeIn(p_fr), GrowArrow(a_ou), FadeIn(p_al), FadeIn(l_ou), run_time=0.5)
        stageB = Group(frame, VGroup(*rowsB), xm, t_re, p_fr, p_al, a_ou, l_ou)
        # stage C: compute it in vertex and pass it on (a varying): corner values 0 and 1, the stripes are lost between the corners
        until(self, "Compute it there and pass it on", lead=0.4)
        self.play(FadeOut(stageB), run_time=0.3)
        cL = Group(qL, lf, grid)
        qR2 = Rectangle(width=W_, height=H_, stroke_color=INK, stroke_width=5).move_to([XR, YQ, 0])
        lv2 = a7_mono("vertex()", XR, 2.85, 28)
        dots2 = [Dot([x, y, 0], radius=0.13, color=INK) for x, y in cs]
        nl = [T("0", 38).move_to([cs[0][0] - 0.35, cs[0][1], 0]), T("0", 38).move_to([cs[2][0] - 0.35, cs[2][1], 0]),
              T("1", 38).move_to([cs[1][0] + 0.35, cs[1][1], 0]), T("1", 38).move_to([cs[3][0] + 0.35, cs[3][1], 0])]
        f0, f1 = a7_mono("fract(0 * 8) = 0", XR, -1.25, 24), a7_mono("fract(1 * 8) = 0", XR, -1.75, 24)
        po = a7_lab("pass on", XR, 2.3, 34)
        self.play(FadeIn(cL), FadeIn(qR2), FadeIn(lv2), FadeIn(VGroup(*dots2)), FadeIn(VGroup(*nl)), FadeIn(po), FadeIn(ill), run_time=0.5)
        self.play(FadeIn(f0), run_time=0.3)
        self.play(FadeIn(f1), run_time=0.3)
        until(self, "it is blended between corners", lead=0.5)
        flat = Rectangle(width=W_, height=H_, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([XR, YQ, 0]).set_z_index(-1)
        self.play(FadeIn(flat), run_time=0.8)
        until(self, "the stripes are lost", lead=0.9)
        lost = a7_lab("flat", XR, -2.4, 40)
        keep = a7_lab("stripes", XL, -1.3, 40)
        self.play(FadeIn(lost), FadeIn(keep), run_time=0.3)
        self.add(example_tag(3.05, -3.1))
        done(self)


# ── B53 · Q3: built-ins read and written ────────────────────────────────────────────────────────────────────────
class B53_BuiltIns(Scene):
    def construct(self):
        H, S = "hint.gdshader", "surface.gdshader"
        spec = [(9, a7_line(H, 9)), (10, a7_line(H, 10)), None, (12, a7_line(S, 12))]
        blk = A7Code(spec, x=-1.6, y=1.7, size=20, wrap=52, pitch=0.38, gap=0.26, pad=0.2, dedent=True, extra=0.35)
        f_h = a7_mono(H, 4.65, (blk.piece_y(9, 0) + blk.piece_y(10, 1)) / 2, 20, DIM)
        f_s = a7_mono(S, 4.65, (blk.piece_y(12, 0) + blk.piece_y(12, 1)) / 2, 20, DIM)
        cap = framed(a7_img("ev_hint_grid_example.png", w=3.5, at=(-4.0, -1.45)), pad=0.05)
        until(self, "Which built-ins did you read", lead=0.0)
        self.play(Create(blk.frame), FadeIn(VGroup(*[blk.rows(n) for n in (9, 10, 12)])), FadeIn(blk.marks), FadeIn(blk.hooks), FadeIn(f_h), FadeIn(f_s), FadeIn(cap), run_time=0.7)
        mk = lambda t, x, y: a7_pill(t, x, y, len(t) * 0.2 + 0.8)
        uv, fc, vp = mk("UV", 0.85, -0.85), mk("FRAGCOORD", 1.35, -1.57), mk("VIEWPORT_SIZE", 1.65, -2.29)
        r9 = blk.ring(9)
        until(self, "reads U V", lead=0.6)
        self.play(Create(r9), FadeIn(uv), run_time=0.35)
        r10a, r10b = blk.ring(10, pieces=(0,)), blk.ring(10, pieces=(1,))
        until(self, "the fragment coordinate", lead=0.6)
        self.play(FadeOut(r9), Create(r10a), FadeIn(fc), run_time=0.35)
        until(self, "the viewport size", lead=0.6)
        self.play(FadeOut(r10a), Create(r10b), FadeIn(vp), run_time=0.35)
        until(self, "all read-only", lead=0.6)
        ro = a7_lab("read-only", 1.45, -0.2, 36)
        self.play(FadeOut(r10b), FadeIn(ro), run_time=0.3)
        until(self, "write albedo", lead=0.7)
        r9a = blk.ring(9, pieces=(0,))
        al = mk("ALBEDO", 4.9, -0.85)
        wr = a7_lab("written", 4.9, -0.2, 36)
        self.play(Create(r9a), FadeIn(al), FadeIn(wr), run_time=0.35)
        until(self, "and roughness", lead=0.9)
        r12 = blk.ring(12, pieces=(0,))
        ro2 = mk("ROUGHNESS", 4.9, -1.57)
        self.play(FadeOut(r9a), Create(r12), FadeIn(ro2), run_time=0.35)
        self.add(status_tag("the example, 14 Oct", -4.2, -3.1), example_tag(2.9, -3.1))
        done(self)


# ── B54 · Q4/5: what a hint changes ─────────────────────────────────────────────────────────────────────────────
class B54_HintChanges(Scene):
    def construct(self):
        code = A7Code([("signal.gdshader:3", a7_line("signal.gdshader", 3))], x=0.0, y=2.65, size=20, dedent=False)
        until(self, "Does a hint change", lead=0.0)
        self.play(Create(code.frame), FadeIn(code.rows("signal.gdshader:3")), run_time=0.5)
        r3 = code.ring("signal.gdshader:3", shrink=1.3)
        h1, h2 = a7_lab("Inspector", -1.4, 1.5, 36), a7_lab("shader receives", 3.6, 1.5, 36)
        until(self, "only the Inspector", lead=0.4)
        self.play(FadeIn(h1), Create(r3), run_time=0.4)
        until(self, "the value the shader receives", lead=0.4)
        self.play(FadeIn(h2), run_time=0.3)
        # row A: hint_range -> a DRAWN slider (a drawing, not the editor)
        YA, YB, YC = 0.5, -1.4, -2.25
        lA = a7_mono("hint_range", -5.95, YA, 24, left=True)
        track1 = Line([-2.6, YA, 0], [-0.2, YA, 0], color=INK, stroke_width=7)
        tk1 = VGroup(Line([-2.6, YA - 0.12, 0], [-2.6, YA + 0.12, 0], color=INK, stroke_width=5), Line([-0.2, YA - 0.12, 0], [-0.2, YA + 0.12, 0], color=INK, stroke_width=5))
        n01 = VGroup(a7_lab("0", -2.6, YA - 0.45, 32), a7_lab("1", -0.2, YA - 0.45, 32))
        knob1 = Circle(radius=0.14, stroke_color=INK, stroke_width=5, fill_color=CARD, fill_opacity=1).move_to([-0.92, YA, 0])
        until(self, "Range shapes the slider", lead=0.4)
        self.play(FadeOut(r3), FadeIn(lA), Create(track1), Create(tk1), FadeIn(n01), run_time=0.5)
        ok1 = check(0.55, YA, s=0.22, color=INK, w=8)
        self.play(FadeIn(knob1), Create(ok1), run_time=0.3)
        # rows B and C: source_color against no hint (Forward+, the re-run's three grey bands)
        lB = a7_mono("source_color", -5.95, YB, 24, left=True)
        lC = a7_lab("no hint", -5.95, YC, 36, left=True)
        sw = lambda v, x, y: VGroup(swatch((v, v, v), x, y, 0.5, 0.5), Rectangle(width=0.5, height=0.5, stroke_color=DIM, stroke_width=3, fill_opacity=0).move_to([x, y, 0]))
        pairB = VGroup(sw(64, 2.0, YB), arrow([2.35, YB, 0], [2.95, YB, 0], INK, 5, 0.18), sw(64, 3.3, YB), a7_lab("64", 3.65, YB, 38, left=True))
        pairC = VGroup(sw(64, 2.0, YC), arrow([2.35, YC, 0], [2.95, YC, 0], INK, 5, 0.18), sw(137, 3.3, YC), a7_lab("137", 3.65, YC, 38, left=True))
        until(self, "On Forward Plus", lead=0.3)
        tagF = status_tag("Forward+ · re-run for this film", 3.25, -3.05)
        self.play(FadeIn(lB), FadeIn(pairB), FadeIn(tagF), run_time=0.4)
        self.play(FadeIn(lC), FadeIn(pairC), run_time=0.4)
        br = VGroup(Line([4.85, YB, 0], [4.85, YC, 0], color=INK, stroke_width=5), Line([4.85, YB, 0], [4.7, YB, 0], color=INK, stroke_width=5),
                    Line([4.85, YC, 0], [4.7, YC, 0], color=INK, stroke_width=5))
        dif = a7_lab("differ", 5.5, (YB + YC) / 2, 34)
        until(self, "as the experiment showed", lead=0.3)
        self.play(Create(br), FadeIn(dif), run_time=0.4)
        # row A, shader side: a value of 2 sits beyond the slider's end
        track2 = Line([2.2, YA, 0], [4.2, YA, 0], color=INK, stroke_width=7)
        tk2 = VGroup(Line([2.2, YA - 0.12, 0], [2.2, YA + 0.12, 0], color=INK, stroke_width=5), Line([4.2, YA - 0.12, 0], [4.2, YA + 0.12, 0], color=INK, stroke_width=5))
        n02 = VGroup(a7_lab("0", 2.2, YA - 0.45, 32), a7_lab("1", 4.2, YA - 0.45, 32))
        ext = DashedLine([4.2, YA, 0], [5.7, YA, 0], color=INK, stroke_width=5, dash_length=0.15)
        knob2 = Circle(radius=0.14, stroke_color=INK, stroke_width=5, fill_color=CARD, fill_opacity=1).move_to([5.3, YA, 0])
        two = a7_lab("2", 5.3, YA + 0.5, 38)
        until(self, "Whether range clamps", lead=0.3)
        self.play(Create(track2), Create(tk2), FadeIn(n02), run_time=0.4)
        self.play(Create(ext), FadeIn(knob2), FadeIn(two), run_time=0.4)
        until(self, "a capture will show", lead=0.5)
        q = a7_lab("clamped?", 3.9, -0.7, 36)
        self.play(FadeIn(q), run_time=0.3)
        self.add(example_tag(-3.0, -3.1))
        done(self)


# ── B55 · Q7/8: each fragment alone; what Godot gives you; the agent checks references ───────────────────────────
class B55_AloneAndGiven(Scene):
    def construct(self):
        # stage 1: sealed pixel boxes, one uniform bus feeds all
        xs = [-4.4, -2.2, 0.0, 2.2, 4.4]
        boxes = VGroup(*[box(x, 0.9, 1.3, 1.3, DIM, 5) for x in xs])
        dots = VGroup(*[Dot([x, 0.9, 0], radius=0.1, color=INK) for x in xs])
        blocked = VGroup(*[VGroup(arrow([xs[i] + 0.78, 0.9, 0], [xs[i + 1] - 0.78, 0.9, 0], INK, 4, 0.16), cross_mark((xs[i] + xs[i + 1]) / 2, 0.9, 0.14, INK, 6)) for i in range(4)])
        bus = Line([-5.2, -1.0, 0], [5.2, -1.0, 0], color=BAR1, stroke_width=12)
        drops = VGroup(*[arrow([x, -1.0, 0], [x, 0.2, 0], INK, 5, 0.2) for x in xs])
        lab_u = a7_lab("uniform", 0.0, -1.75, 38)
        until(self, "Each fragment runs alone", lead=0.0)
        self.play(LaggedStart(*[AnimationGroup(Create(b), FadeIn(d, scale=0.4)) for b, d in zip(boxes, dots)], lag_ratio=0.2), run_time=0.9)
        until(self, "cannot read its neighbour", lead=0.3)
        self.play(LaggedStart(*[FadeIn(b) for b in blocked], lag_ratio=0.25), run_time=0.8)
        until(self, "game state arrives", lead=0.3)
        self.play(Create(bus), FadeIn(lab_u), run_time=0.4)
        self.play(LaggedStart(*[GrowArrow(d) for d in drops], lag_ratio=0.15), run_time=0.7)
        stage1 = Group(boxes, dots, blocked, bus, drops, lab_u)
        # stage 2: what Godot gives you
        until(self, "And Godot gives you", lead=0.45)
        self.play(FadeOut(stage1), run_time=0.25)
        fr = a7_pill("fragment()", -3.1, 1.95, 2.9, size=28, h=0.7)
        outs = [a7_pill(t, -3.1, y, len(t) * 0.2 + 0.9) for t, y in (("ALBEDO", 0.65), ("ROUGHNESS", -0.1), ("METALLIC", -0.85))]
        a_fr = arrow([-3.1, 1.55, 0], [-3.1, 1.05, 0], INK, 5, 0.2)
        self.play(FadeIn(fr), run_time=0.25)
        self.play(GrowArrow(a_fr), LaggedStart(*[FadeIn(o) for o in outs], lag_ratio=0.2), run_time=0.55)
        no_l = a7_lab("named outputs", -3.1, -1.7, 36)
        cite = a7_mono("surface.gdshader:10-13", -3.1, -2.35, 20, DIM)
        self.play(FadeIn(no_l), FadeIn(cite), run_time=0.3)
        until(self, "hints that become controls", lead=0.5)
        SCs = 1.4
        hr = a7_pill("hint_range", 3.5, 1.95, 2.8, size=28, h=0.7)
        a_h = arrow([3.5, 1.55, 0], [3.5, 1.12, 0], INK, 5, 0.18)
        sl = framed(a7_img("a7_ed_matte_sliders.png", w=900 * SCs / 270.0, at=(3.5, 0.45)), pad=0.05)
        ins = a7_lab("Inspector controls", 3.5, -0.55, 34)
        t_e = status_tag("scripted editor session", 3.5, -1.25)
        self.play(FadeIn(hr), GrowArrow(a_h), FadeIn(sl), FadeIn(ins), FadeIn(t_e), run_time=0.6)
        # stage 3: the agent checks references, never writes the answers
        until(self, "The agent may check", lead=0.35)
        self.play(FadeOut(Group(fr, *outs, a_fr, no_l, cite, hr, a_h, sl, ins, t_e)), run_time=0.3)
        agent = logo_chip("claude-code", -4.1, 0.0, h=1.7)
        ref = a7_pill("surface.gdshader:12", 3.0, 1.45, 19 * 0.2 + 0.9)
        pg = a7_doc(3.0, -1.2, 1.4, 1.5)
        a1 = arrow([-2.9, 0.3, 0], [0.3, 1.3, 0], INK, 6, 0.22)
        a2 = arrow([-2.9, -0.3, 0], [0.3, -1.1, 0], INK, 6, 0.22)
        no = a7_no(-1.3, -0.7, 0.28, 7)
        l_ref = a7_lab("line references", 3.0, 0.75, 34)
        l_ans = a7_lab("your answers", 3.0, -2.35, 36)
        until(self, "may check your line references", lead=0.55)
        self.play(FadeIn(agent), GrowArrow(a1), FadeIn(ref), FadeIn(l_ref), run_time=0.5)
        ok = check(5.75, 1.45, s=0.24, color=INK, w=8)
        self.play(Create(ok), run_time=0.25)
        until(self, "never write the answers", lead=0.7)
        self.play(GrowArrow(a2), FadeIn(pg), FadeIn(l_ans), run_time=0.4)
        self.play(Create(no), run_time=0.25)
        done(self)


# ── B55B · what done means ──────────────────────────────────────────────────────────────────────────────────────
class B55B_DoneMeans(Scene):
    def construct(self):
        head = T("Done  means", 56).move_to([-3.3, 2.9, 0], aligned_edge=LEFT)
        items = [("a recorded check", 2.0), ("3 mutations fail", 1.25), ("shaders untouched", 0.5), ("textures credited", -0.25), ("questions answered", -1.0), ("earlier suites", -1.75)]
        phrases = ("Every rule has a recorded check", "All three mutations fail", "No session changed", "Every texture is credited", "every language question answered", "The earlier suites keep their counts")
        until(self, "Done is a list", lead=0.0)
        self.play(FadeIn(head), run_time=0.4)
        for (txt, y), ph in zip(items, phrases):
            until(self, ph, lead=0.3)
            t = T(txt, 48).move_to([-2.5, y, 0], aligned_edge=LEFT)
            k = tick_mark(-3.3, y, 0.28, INK, 9)
            self.play(Create(k), FadeIn(t), run_time=0.35)
        yc = -2.85
        until(self, "Claude said it works", lead=0.45)
        tc = T("Claude said it works", 48, DIM).move_to([-2.5, yc, 0], aligned_edge=LEFT)
        xm = cross_mark(-3.3, yc, 0.28, INK, 9)
        self.play(FadeIn(tc), Create(xm), run_time=0.4)
        spark = Dot([3.4, yc + 0.05, 0], radius=0.12, color=TERRA)
        self.play(FadeIn(spark, scale=0.4), run_time=0.25)
        done(self)
