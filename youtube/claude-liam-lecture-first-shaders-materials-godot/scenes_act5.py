"""ACT V · A Shader That Reads Textures  (B35-B39, Manim)

One cast for the act: the two REAL 64 x 64 textures (pantry/ev_tex_color.png, ev_tex_rough.png), the REAL 14-line surface.gdshader
(evidence/example/sources/surface.gdshader) and the two REAL material spheres (circle cut-outs of the example's own capture,
pantry/a5_mat_matte.png and a5_mat_coated.png, made by evidence/act5/make_a5_pantry.py).
Every line of code on screen is verbatim from evidence/example/sources/ with its REAL line number; excerpts are dedented by the
common leading tab, and a line longer than the frame (surface.gdshader line 12 is 87 characters) wraps at a space with a drawn
continuation hook (the characters are untouched; the line number shows once). Numbers on screen are the file's own (matte.tres /
coated.tres lines 9-12, garden-textures.py, the .import files).
Editor frames (the Import dock, the Inspector of matte.tres) are NOT drawn here: B35 and B37 carry labelled fallbacks that name the
REAL file lines; the real frames drop into a5_import_panel() / the right-hand slot of B37 once evidence/editor/EDITOR-NOTES.md exists.
"""

A5P = "pantry/"

# REAL source lines, embedded verbatim (Gate A runs scenes.py from a folder with no evidence/); evidence/act5/verify_embedded.py checks them.
A5_REAL = {'surface.gdshader': {1: 'shader_type spatial;',
                      2: 'group_uniforms Surface;',
                      3: 'uniform sampler2D color_map : source_color, filter_nearest;',
                      4: 'uniform sampler2D roughness_map : filter_nearest;',
                      5: 'uniform vec4 tint : source_color = vec4(1.0);',
                      6: 'uniform float roughness_gain : hint_range(0.0, 1.0) = 0.8;',
                      7: 'group_uniforms Pattern;',
                      8: 'uniform float uv_scale : hint_range(0.25, 4.0) = 1.0;',
                      9: 'uniform float metallic_gain : hint_range(0.0, 1.0) = 0.0;',
                      10: 'void fragment() {',
                      11: '\tALBEDO = texture(color_map, UV * uv_scale).rgb * tint.rgb;',
                      12: '\tROUGHNESS = clamp(texture(roughness_map, UV * uv_scale).r * roughness_gain, 0.05, 1.0);',
                      13: '\tMETALLIC = metallic_gain;',
                      14: '}'},
 'gate-color.png.import': {16: '[params]', 18: 'compress/mode=0', 24: 'compress/normal_map=2', 26: 'mipmaps/generate=false'},
 'gate-roughness.png.import': {18: 'compress/mode=0', 24: 'compress/normal_map=2', 26: 'mipmaps/generate=false'},
 'matte.tres': {9: 'shader_parameter/tint = Color(1, 1, 1, 1)',
                10: 'shader_parameter/roughness_gain = 0.9',
                11: 'shader_parameter/uv_scale = 1.0',
                12: 'shader_parameter/metallic_gain = 0.0'},
 'coated.tres': {9: 'shader_parameter/tint = Color(0.45, 0.95, 0.72, 1)',
                 10: 'shader_parameter/roughness_gain = 0.25',
                 11: 'shader_parameter/uv_scale = 2.0',
                 12: 'shader_parameter/metallic_gain = 0.4'},
 'garden-textures.py': {2: '"""Original algorithmic textures. No model, network, or borrowed image."""',
                        11: '            stripe=(x//8)%2',
                        12: "            data.extend(((44+stripe*15,78+stripe*18,85+stripe*16) if role=='color' else (int(255*(0.4 if stripe else "
                            '0.85)),)*3))',
                        15: "png('gate-color.png','color');png('gate-roughness.png','data')"}}

A5_CW = {20: 0.15, 24: 0.2}            # measured Menlo units per character
A5_LH = {20: 0.2875, 24: 0.345}        # default row pitch (size / 32 * 0.46)


def a5_line(fname, n):
    return A5_REAL[fname][n]


def a5_lab(s, x, y, size=34, color=INK, left=False):
    t = T(s, size, color)
    if left:
        return t.move_to([x, y, 0], aligned_edge=LEFT)
    return t.move_to([x, y, 0])


def a5_img(name, h=None, w=None, at=(0.0, 0.0)):
    im = ImageMobject(A5P + name)
    try:
        im.set_resampling_algorithm(RESAMPLING_ALGORITHMS["linear"])   # bicubic rings near light-on-dark text and breaks GATE T's ink mask
    except Exception:
        pass
    if h is not None:
        im.set_height(h)
    if w is not None:
        im.set_width(w)
    return im.move_to(np.array([at[0], at[1], 0.0]))


def a5_hook(x, y, s=0.13):
    """The wrap mark: a drawn elbow (down, then left with a small head). A shape, not a glyph."""
    return VGroup(Line([x, y + s * 0.6, 0], [x, y - s * 0.7, 0], color=DIM, stroke_width=4),
                  Line([x, y - s * 0.7, 0], [x - s * 1.4, y - s * 0.7, 0], color=DIM, stroke_width=4),
                  Line([x - s * 1.4, y - s * 0.7, 0], [x - s * 0.8, y - s * 0.2, 0], color=DIM, stroke_width=4),
                  Line([x - s * 1.4, y - s * 0.7, 0], [x - s * 0.8, y - s * 1.2, 0], color=DIM, stroke_width=4))


def a5_split(text, budget):
    """Soft-wrap `text` at the last space at or before `budget` characters, preferring a space after a comma/&&/colon.
    Returns a list of pieces (characters verbatim; only the breaking space is dropped)."""
    if len(text) <= budget:
        return [text]
    cut = text.rfind(" ", 0, budget + 1)
    if cut <= 0:
        return [text]
    return [text[:cut]] + a5_split(text[cut + 1:], budget)


class A5Code:
    """Real code rows: Menlo, real line numbers, outline-only frame, optional gap markers and wraps.
    spec: list of (real_line_number, text) or None (a gap marker). `dedent` strips the common leading tab(s).
    Attributes: .group (frame + rows + marks), .frame, .W, .H, .pitch, .cw, .size; rows(n) -> VGroup of line n (number + pieces);
    ring(n) -> terracotta ring round the whole line n; tok(n, token, k=0) -> (cx, cy, w) of a token; piece_y(n, i)."""

    def __init__(self, spec, x=0.0, y=0.0, size=20, wrap=None, dedent=True, pad=0.3, pitch=None, gap=0.32, width=None, extra=0.0):
        self.size, self.cw = size, A5_CW[size]
        self.pitch = pitch or A5_LH[size]
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
            pieces = a5_split(t, wrap) if wrap else [t]
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
                hk = a5_hook(self.text_left + prev[2] + len(prev[1]) * self.cw + 0.2, prev[0])
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


def a5_mono(s, x, y, size=24, color=INK, left=False):
    t = M(s, size, color)
    if left:
        return t.move_to([x, y, 0], aligned_edge=LEFT)
    return t.move_to([x, y, 0])


def a5_x(x, y, s=0.1, w=5):
    """A multiplication mark drawn as a shape."""
    return cross_mark(x, y, s, INK, w)


def a5_rev(*mobs):
    return [FadeIn(m) for m in mobs]


# ── B35 · textured shader: textures first, import settings set by hand ───────────────────────────────────────────
A5_SCALE_DOCK = 2.0                    # the Import dock crop is shown at 2x its native pixels (UI text then reads at 4K)


def a5_row_y(top, py, scale):
    """Scene y of pixel row py of a crop whose top edge sits at scene y `top`, shown at `scale` x native (1 unit = 270 px at 4K)."""
    return top - py * scale / 270.0


class B35_ImportSettings(Scene):
    def construct(self):
        title = T("A  Shader  That  Reads  Textures", 40).move_to([-6.0, 2.95, 0], aligned_edge=LEFT)
        self.add(title)
        tc = framed(a5_img("ev_tex_color.png", h=1.0, at=(-5.5, 1.85)))
        tr = framed(a5_img("ev_tex_rough.png", h=1.0, at=(-5.5, 0.55)))
        n1 = a5_mono("gate-color.png", -4.75, 1.85, 20, left=True)
        n2 = a5_mono("gate-roughness.png", -4.75, 0.55, 20, left=True)
        until(self, "Get textures first", lead=0.2)
        self.play(FadeIn(tc), FadeIn(tr), FadeIn(n1), FadeIn(n2), run_time=0.5)
        until(self, "Then set their import settings", lead=0.2)
        blk = A5Code([(n, a5_line("gate-color.png.import", n)) for n in (18, 24, 26)], x=-2.9, y=-1.85, size=24, dedent=False, pitch=0.5, gap=0.0)
        head = a5_mono("gate-color.png.import", -2.9, -0.5, 24)
        self.play(Create(blk.frame), FadeIn(head), FadeIn(VGroup(*[blk.rows(n) for n in (18, 24, 26)])), run_time=0.6)
        dock = framed(a5_img("a5_ed_import_compress.png", w=760 * A5_SCALE_DOCK / 270.0, at=(3.3, 1.3)), pad=0.05)
        TOP = 1.3 + 283 * A5_SCALE_DOCK / 270.0 / 2
        y_mode, y_gen = a5_row_y(TOP, 79, A5_SCALE_DOCK), a5_row_y(TOP, 246, A5_SCALE_DOCK)
        gx = blk.x - blk.W / 2 - 0.3
        until(self, "compress mode", lead=0.5)
        d1 = Dot([0.2, y_mode, 0], radius=0.11, color=TERRA)
        g1 = Dot([gx, blk.piece_y(18), 0], radius=0.11, color=TERRA)
        self.play(FadeIn(dock), FadeIn(d1, scale=0.4), FadeIn(g1, scale=0.4), run_time=0.5)
        tag = status_tag("scripted editor session", 3.3, -0.3)
        self.add(tag)
        until(self, "mipmaps", lead=0.3)
        d2 = Dot([0.2, y_gen, 0], radius=0.11, color=TERRA)
        g2 = Dot([gx, blk.piece_y(26), 0], radius=0.11, color=TERRA)
        self.play(FadeOut(VGroup(d1, g1)), FadeIn(d2, scale=0.4), FadeIn(g2, scale=0.4), run_time=0.4)
        until(self, "the normal map flag", lead=0.3)
        g3 = Dot([gx, blk.piece_y(24), 0], radius=0.11, color=TERRA)
        nm = a5_lab("no Normal Map row", 3.3, -1.0, 36)
        self.play(FadeOut(VGroup(d2, g2)), FadeIn(g3, scale=0.4), FadeIn(nm), run_time=0.4)
        until(self, "The editor then has nothing", lead=0.2)
        ok = check(5.6, -2.25, s=0.28, color=INK, w=8)
        spark = Dot([6.0, -2.05, 0], radius=0.1, color=TERRA)
        self.play(Create(ok), FadeIn(spark), run_time=0.5)
        self.add(example_tag(2.85, -3.05))
        done(self)


# ── B36 · the two textures: colour stripes and 102 / 216 ─────────────────────────────────────────────────────────
def a5_chip(cx, y, rgb, text, size=34, sw=0.7, sh=0.5):
    """A real texel value: a swatch of the real colour + its real numbers (BESIDE it), the pair centred on cx."""
    tx = T(text, size)
    total = sw + 0.15 + tx.width
    x0 = cx - total / 2
    sq = swatch(rgb, x0 + sw / 2, y, sw, sh)
    fr = Rectangle(width=sw, height=sh, stroke_color=DIM, stroke_width=3, fill_opacity=0).move_to([x0 + sw / 2, y, 0])
    tx.move_to([x0 + sw + 0.15, y, 0], aligned_edge=LEFT)
    return VGroup(sq, fr, tx)


class B36_TwoTextures(Scene):
    def construct(self):
        S, XL, XR, YT = 3.0, -2.9, 2.9, 0.95
        tc = a5_img("ev_tex_color.png", h=S, at=(XL, YT))
        tr = a5_img("ev_tex_rough.png", h=S, at=(XR, YT))
        gc, gr = framed(tc, pad=0.07), framed(tr, pad=0.07)
        until(self, "The example's textures", lead=0.15)
        self.play(FadeIn(gc), FadeIn(gr), run_time=0.5)
        dim = dim_arrow([-4.8, YT - S / 2, 0], [-4.8, YT + S / 2, 0], color=INK, w=4)
        d_l = a5_lab("64 px", -5.45, YT, 34)
        until(self, "sixty-four pixels square", lead=0.3)
        self.play(GrowFromCenter(dim), FadeIn(d_l), run_time=0.4)
        until(self, "written by a script", lead=0.2)
        scr = a5_mono("garden-textures.py", -3.35, -3.0, 24)
        self.play(FadeIn(scr), run_time=0.3)
        until(self, "One holds two colours", lead=0.2)
        px = lambda cx, k: cx - S / 2 + S / 8 * (k + 0.5)
        stripe = lambda cx, k: ring(Rectangle(width=S / 8 - 0.04, height=S - 0.1, stroke_width=0, fill_opacity=0).move_to([px(cx, k), YT, 0]), pad=0.0, sw=6, backing=False)
        dots = [stripe(XL, 0), stripe(XL, 1)]
        chips = [a5_chip(XL, -1.0, (44, 78, 85), "44, 78, 85"), a5_chip(XL, -1.65, (59, 96, 101), "59, 96, 101")]
        lc = a5_lab("colour", XL, -2.4, 40)
        for i, (d, c) in enumerate(zip(dots, chips)):
            self.play(FadeIn(d), FadeIn(c), *([FadeOut(dots[0])] if i else []), run_time=0.3)
        self.play(FadeIn(lc), run_time=0.3)
        until(self, "The other holds two numbers", lead=0.2)
        self.play(FadeOut(dots[1]), run_time=0.2)
        dots2 = [stripe(XR, 1), stripe(XR, 0)]
        chips2 = [a5_chip(XR, -1.0, (102, 102, 102), "102"), a5_chip(XR, -1.65, (216, 216, 216), "216")]
        until(self, "one hundred two", lead=0.25)
        self.play(FadeIn(dots2[0]), FadeIn(chips2[0]), run_time=0.3)
        until(self, "two sixteen", lead=0.25)
        self.play(FadeOut(dots2[0]), FadeIn(dots2[1]), FadeIn(chips2[1]), run_time=0.3)
        until(self, "Same kind of file", lead=0.2)
        eq = VGroup(Line([-0.35, YT + 0.1, 0], [0.35, YT + 0.1, 0], color=INK, stroke_width=7), Line([-0.35, YT - 0.1, 0], [0.35, YT - 0.1, 0], color=INK, stroke_width=7))
        rc = a5_lab("data", XR, -2.4, 40)
        self.play(Create(eq), run_time=0.35)
        self.play(FadeIn(rc), run_time=0.3)
        self.add(example_tag(2.9, -3.0))
        done(self)


# ── B37 · two samplers, one hint, four uniforms, two groups ─────────────────────────────────────────────────────
class B37_TwoSamplers(Scene):
    def construct(self):
        spec = [(n, a5_line("surface.gdshader", n)) for n in range(2, 10)]
        blk = A5Code(spec, x=-1.2, y=0.15, size=20, pitch=0.5, dedent=False)
        self.add(blk.frame)
        self.play(FadeIn(VGroup(*[blk.rows(n) for n in range(2, 10)])), run_time=0.5)
        until(self, "Two samplers", lead=0.2)
        r3 = blk.ring(3)
        until(self, "the colour map says source color", lead=0.4)
        t_c = a5_lab("colour", 5.05, blk.piece_y(3) + 0.14, 36)
        self.play(Create(r3), FadeIn(t_c), run_time=0.4)
        until(self, "the roughness map says nothing", lead=0.45)
        r4 = blk.ring(4)
        t_d = a5_lab("data", 5.05, blk.piece_y(4) - 0.14, 36)
        self.play(Create(r4), FadeIn(t_d), run_time=0.4)
        until(self, "Four more uniforms", lead=0.5)
        self.play(FadeOut(Group(blk.group, r3, r4, t_c, t_d)), run_time=0.3)
        # the same uniforms as the editor draws them: the REAL Inspector of matte.tres (scripted editor session)
        SC = 2.0
        cx, cy = 0.2, -0.1
        im = framed(a5_img("a5_ed_matte_params.png", w=900 * SC / 270.0, at=(cx, cy)), pad=0.05)
        top = cy + 670 * SC / 270.0 / 2
        left = cx - 900 * SC / 270.0 / 2
        self.play(FadeIn(im), run_time=0.4)
        until(self, "Four more uniforms", lead=-0.2)
        rows_py = (404, 465, 571, 632)
        dots = VGroup(*[Dot([left - 0.28, a5_row_y(top, py, SC), 0], radius=0.1, color=TERRA) for py in rows_py])
        self.play(LaggedStart(*[FadeIn(d, scale=0.4) for d in dots], lag_ratio=0.25), run_time=0.7)
        until(self, "in two groups", lead=0.2)
        hdr = lambda py: RoundedRectangle(width=900 * SC / 270.0 - 0.1, height=0.34, corner_radius=0.08, stroke_color=TERRA, stroke_width=6,
                                          fill_opacity=0).move_to([cx, a5_row_y(top, py, SC), 0])
        h1, h2 = hdr(89), hdr(520)
        until(self, "surface and pattern", lead=0.55)
        self.play(FadeOut(dots), Create(h1), Create(h2), run_time=0.4)
        self.add(status_tag("scripted editor session", -2.9, -3.05), example_tag(3.0, -3.05))
        done(self)


# ── B38 · fragment: three outputs, three flows ──────────────────────────────────────────────────────────────────
def a5_chain(items, y, x_right, size=20):
    """Right-aligned chain of boxed identifiers joined by x and arrows. items: ('box', text) | ('x',) | ('to',). Returns (VGroup parts, list of box centres)."""
    cw = A5_CW[size]
    ws = {"x": 0.5, "to": 0.75}
    wid = lambda it: (len(it[1]) * cw + 0.5) if it[0] == "box" else ws[it[0]]
    total = sum(wid(it) for it in items)
    cx = x_right - total
    parts, boxes = VGroup(), []
    for it in items:
        w = wid(it)
        mid = cx + w / 2
        if it[0] == "box":
            b = box(mid, y, w - 0.08, 0.62, color=INK, sw=4)
            t = M(it[1], size).move_to([mid, y, 0])
            parts.add(VGroup(b, t)); boxes.append((mid, w))
        elif it[0] == "x":
            parts.add(a5_x(mid, y, 0.11, 6))
        else:
            parts.add(arrow([mid - 0.3, y, 0], [mid + 0.3, y, 0], INK, 5, 0.2))
        cx += w
    return parts, boxes


class B38_FragmentLines(Scene):
    def construct(self):
        spec = [(n, a5_line("surface.gdshader", n)) for n in range(10, 14)]
        blk = A5Code(spec, x=0.0, y=1.95, size=20, wrap=64, pitch=0.4, dedent=False, extra=0.35)
        self.add(blk.frame)
        self.play(FadeIn(VGroup(*[blk.rows(n) for n in range(10, 14)])), FadeIn(blk.hooks), run_time=0.5)
        flows = {
            11: a5_chain([("box", "color_map"), ("x",), ("box", "tint"), ("to",), ("box", "ALBEDO")], -0.35, 5.7),
            12: a5_chain([("box", "roughness_map.r"), ("x",), ("box", "roughness_gain"), ("to",), ("box", "clamp"), ("to",), ("box", "ROUGHNESS")], -1.4, 5.7),
            13: a5_chain([("box", "metallic_gain"), ("to",), ("box", "METALLIC")], -2.45, 5.7),
        }
        until(self, "Fragment multiplies", lead=0.2)
        ring = blk.ring(11)
        self.play(Create(ring), run_time=0.3)
        self.play(LaggedStart(*[FadeIn(p) for p in flows[11][0]], lag_ratio=0.2), run_time=0.8)
        until(self, "reads roughness", lead=0.25)
        ring2 = blk.ring(12)
        self.play(FadeOut(ring), Create(ring2), run_time=0.3)
        p12 = flows[12][0]
        until(self, "from the red channel", lead=0.25)
        self.play(FadeIn(p12[0]), run_time=0.3)
        until(self, "scales it by a gain", lead=0.3)
        self.play(FadeIn(p12[1]), FadeIn(p12[2]), run_time=0.3)
        until(self, "and clamps it", lead=0.35)
        self.play(FadeIn(p12[3]), FadeIn(p12[4]), FadeIn(p12[5]), FadeIn(p12[6]), run_time=0.4)
        until(self, "Metallic is just a number", lead=0.8)
        ring3 = blk.ring(13)
        self.play(FadeOut(ring2), Create(ring3), run_time=0.3)
        self.play(LaggedStart(*[FadeIn(p) for p in flows[13][0]], lag_ratio=0.2), run_time=0.5)
        spark = Dot([6.0, -2.45, 0], radius=0.1, color=TERRA)
        self.play(FadeIn(spark, scale=0.4), run_time=0.25)
        done(self)


# ── B39 · two materials, one shader; resource files; Use External ───────────────────────────────────────────────
class B39_TwoMaterials(Scene):
    def construct(self):
        SC = 1.5
        CX = (-2.75, 2.75)
        shader = VGroup(box(0, 2.75, 4.0, 0.8, INK, 4), M("surface.gdshader", 24).move_to([0, 2.75, 0]))
        c_m, c_c = chip("matte", -4.0, 2.75, w=2.0, size=36), chip("coated", 4.0, 2.75, w=2.0, size=36)
        s_m = a5_img("a5_mat_matte.png", h=1.0, at=(-5.6, 2.75))
        s_c = a5_img("a5_mat_coated.png", h=1.0, at=(5.6, 2.75))
        a_m = arrow([-2.9, 2.75, 0], [-2.05, 2.75, 0], INK, 5, 0.2)
        a_c = arrow([2.9, 2.75, 0], [2.05, 2.75, 0], INK, 5, 0.2)
        until(self, "Two materials use this shader", lead=0.1)
        self.play(FadeIn(shader), run_time=0.35)
        until(self, "matte", lead=0.3)
        self.play(FadeIn(c_m), FadeIn(s_m), GrowArrow(a_m), run_time=0.4)
        until(self, "and coated", lead=0.3)
        self.play(FadeIn(c_c), FadeIn(s_c), GrowArrow(a_c), run_time=0.4)
        # the REAL Inspector of each saved material (scripted editor session): values read off the frames are the .tres values
        w_, h_ = 900 * SC / 270.0, 670 * SC / 270.0
        cyc = -0.45
        im_m = framed(a5_img("a5_ed_matte_params.png", w=w_, at=(CX[0], cyc)), pad=0.05)
        im_c = framed(a5_img("a5_ed_coated_params.png", w=w_, at=(CX[1], cyc)), pad=0.05)
        until(self, "They differ in", lead=0.1)
        self.play(FadeIn(im_m), FadeIn(im_c), run_time=0.5)
        top, left = cyc + h_ / 2, CX[0] - w_ / 2
        dots = VGroup(*[Dot([left - 0.2, a5_row_y(top, py, SC), 0], radius=0.09, color=TERRA) for py in (404, 465, 571, 632)])
        until(self, "tint", lead=0.1)
        self.play(LaggedStart(*[FadeIn(d, scale=0.4) for d in dots], lag_ratio=0.4), run_time=1.6)
        until(self, "resource files", lead=0.35)
        f_m = a5_mono("matte.tres", CX[0], 1.75, 24)
        f_c = a5_mono("coated.tres", CX[1], 1.75, 24)
        self.play(FadeOut(dots), FadeIn(f_m), FadeIn(f_c), run_time=0.3)
        # stage 3: Use External (a drawing of the setting, not the editor)
        until(self, "For an imported scene", lead=0.3)
        self.play(FadeOut(Group(im_m, im_c, f_m, f_c)), run_time=0.3)
        scene_box = box(-2.9, 0.15, 4.3, 2.0, DIM, 4)
        scene_l = a5_lab("imported scene", -2.9, -1.3, 34)
        slot = VGroup(box(-3.1, -0.1, 2.2, 0.62, INK, 4), a5_lab("material", -3.1, 0.65, 32))
        self.play(Create(scene_box), FadeIn(scene_l), FadeIn(slot), run_time=0.5)
        until(self, "behind Use External", lead=0.35)
        tres = chip("matte.tres", 3.9, -0.1, mono=True, size=28)
        link = DashedLine([-1.95, -0.1, 0], [2.3, -0.1, 0], color=INK, stroke_width=5, dash_length=0.18)
        ue = a5_lab("Use External", 0.75, 0.45, 38)
        self.play(Create(link), FadeIn(ue), FadeIn(tres), run_time=0.5)
        until(self, "so a reimport keeps them", lead=1.0)
        loop = CurvedArrow([-4.5, 1.3, 0], [-1.3, 1.3, 0], angle=-PI / 3.4, color=INK, stroke_width=5, tip_length=0.22)
        ri = a5_lab("reimport", -2.9, 1.95, 34)
        self.play(Create(loop), FadeIn(ri), run_time=0.5)
        ok = check(5.65, -0.1, s=0.25, color=INK, w=8)
        spark = Dot([6.0, 0.1, 0], radius=0.1, color=TERRA)
        self.play(Create(ok), FadeIn(spark), run_time=0.4)
        self.add(status_tag("setting from the assignment · not used in the example", -0.4, -2.2), example_tag(2.85, -3.0))
        done(self)
