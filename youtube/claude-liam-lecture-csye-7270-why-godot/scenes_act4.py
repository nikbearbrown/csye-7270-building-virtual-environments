"""ACT IV · The Other Two Engines  (B19–B24, all Manim)

HONESTY RULE for the act (LANE-PLAN.md): Godot has NO official MCP; Unity (public 2026-03-03, open beta) and Unreal 5.8 (Experimental) DO. Nothing here
draws Godot "ahead on MCP" or Unity / Unreal as "raw": their own labels are shown. Unity scenes are text by default; only Unreal's are binary.
Everything on screen is real or labelled:
  * REAL captures (pantry/a4_*.png, cropped from EVID/web-captures by evidence/act4/make_crops_act4.py, never altered): Unity's docs page and
    changelog, the two GitHub repo headers, the Godot Foundation's policy post, and 15 real gameplay frames of the walker-claude capture.
  * unity.com blog and Epic docs returned HTTP 403 to the capture: they are shown ONLY as short quotes (<= 15 words), attributed, labelled
    "quoted, not captured". The capture PNGs of those pages are error pages and are NOT used.
  * The YAML lines are verbatim from Unity's own Manual page (docs.unity3d.com/Manual/FormatDescription.html), trimmed.
  * Star counts: GitHub API 2026-10-09 (Coding-Solo/godot-mcp 5,987; CoplayDev/unity-mcp 14,793); the pages' own buttons read 6k and 14.8k.
One cast for the act (ACTS.md): an engine = a kraft box with its name; an official MCP server = the kit's dark MCP block on top of it; "none" = the
empty outlined slot where it would sit. Pacing lands on real spoken times (evidence/act4/word_times.py, faster-whisper).
"""

A4P = "pantry/"
A4_CABLE = "#9C8462"
A4_PX = {"a4_unity_docs.png": (1680, 540), "a4_unity_changelog.png": (1680, 378), "a4_godot_mcp_banner.png": (1035, 138),
         "a4_unity_mcp_banner.png": (855, 138), "a4_policy_title.png": (2040, 264)}


def a4_at(self, t, lead=0.0):
    """Wait until the clip clock reaches t seconds (the real spoken time of a word, minus an optional lead)."""
    gap = t - lead - _elapsed(self)
    if gap > 0.05:
        self.wait(gap)


A4_W = {
    ('14.8k', 40, False): 1.115,
    ('30 Jun 2026, same page', 32, False): 3.94,
    ('6.0k', 40, False): 0.89,
    ('Epic, Unreal MCP docs', 32, False): 4.063,
    ('Experimental', 36, False): 2.492,
    ('GitHub stars, 9 Oct 2026', 32, False): 4.383,
    ('Godot', 40, False): 1.445,
    ('Godot Foundation', 32, False): 3.104,
    ('June 2026', 32, False): 1.734,
    ('No.', 48, True): 0.98,
    ('The Other Two Engines', 40, False): 4.997,
    ('Unity', 40, False): 1.233,
    ('Unity', 48, False): 1.479,
    ('Unity Manual, trimmed', 32, False): 4.213,
    ('Unity blog, 11 May 2026', 32, False): 4.192,
    ('Unreal Engine 5.8', 44, False): 4.104,
    ('YAML', 40, False): 1.519,
    ('a different thing', 40, False): 3.324,
    ('be human authored.”', 34, False): 3.921,
    ('beta', 34, False): 0.78,
    ('better MCP story?', 40, False): 3.864,
    ('binary', 40, False): 1.387,
    ('command line', 34, False): 2.556,
    ('community server', 32, False): 3.031,
    ('contributing TO Godot', 38, False): 4.893,
    ('cross-references', 36, False): 2.878,
    ('experimental', 34, False): 2.34,
    ('has it', 32, False): 0.928,
    ('incomplete or', 36, False): 2.603,
    ('lacks it', 32, False): 1.178,
    ('last push 16 Apr 2026', 32, False): 3.795,
    ('last push 8 Oct 2026', 32, False): 3.595,
    ('licence', 34, False): 1.213,
    ('making a game WITH Godot', 38, False): 5.999,
    ('missing.”', 36, False): 1.628,
    ('no', 34, False): 0.456,
    ('no official MCP', 32, False): 2.723,
    ('none', 34, False): 0.911,
    ('official MCP', 34, False): 2.332,
    ('open beta', 44, False): 2.222,
    ('or be discontinued', 36, False): 3.434,
    ("per Epic's UE 4.26 docs", 32, False): 4.021,
    ('public, March 2026', 34, False): 3.607,
    ('quoted, not captured', 32, False): 3.608,
    ('read as text', 36, False): 2.038,
    ('recorded 2026-10-09', 32, False): 3.243,
    ('scenes as text', 34, False): 2.381,
    ('scripted input,', 32, False): 2.468,
    ('text by default', 40, False): 2.9,
    ('use or vibe coding”', 34, False): 3.465,
    ('without notice”', 36, False): 2.937,
    ('yes', 34, False): 0.535,
    ('yes, YAML', 34, False): 2.069,
    ('“Many features are', 36, False): 3.462,
    ('“No autonomous AI agent', 34, False): 4.925,
    ('“We require all code to', 34, False): 4.148,
    ('“may change, be limited,', 36, False): 4.521,
}  # measured


def a4_w(s, size, bold=False):
    """Width of an EB Garamond string: the measured value when known, else about 0.0058 x size per character."""
    if _os.environ.get("A4_REC"):
        with open(_os.environ["A4_REC"], "a") as _f:
            _f.write(_json.dumps([s, size, bool(bold)]) + "\n")
    return A4_W.get((s, size, bool(bold)), len(s) * size * 0.0058)


def a4_tl(s, x, y, size=34, color=INK, bold=False):
    """Text whose LEFT edge sits at x."""
    return T(s, size, color, bold).move_to([x + a4_w(s, size, bold) / 2.0, y, 0])


def a4_nx(s, x, size, gap=0.3):
    """x just right of the string s whose left edge is at x."""
    return x + a4_w(s, size) + gap


def a4_tc(s, x, y, size=34, color=INK, bold=False):
    return T(s, size, color, bold).move_to([x, y, 0])


def a4_ml(s, x, y, size=32):
    """Menlo text whose left edge sits at x (0.2459 units per character at size 32)."""
    return M(s, size).move_to([x + len(s) * 0.2459 * size / 32.0 / 2.0, y, 0])


def a4_img(name, cx, cy, w):
    """A real capture crop with a ghost offset shadow behind it. Returns (shadow, image, height)."""
    pw, ph = A4_PX[name]
    h = w * ph / pw
    shadow = Rectangle(width=w, height=h, fill_color=GHOST, fill_opacity=1, stroke_width=0).move_to([cx + 0.07, cy - 0.07, 0])
    im = ImageMobject(A4P + name).set_width(w).move_to([cx, cy, 0])
    return shadow, im, h


def a4_page(cx, cy, w=1.0, h=1.3, lines=3):
    """A page icon: card body with a folded corner and ghost text lines (grey outline, no ink)."""
    f = 0.28
    pts = [[cx - w / 2, cy - h / 2, 0], [cx + w / 2, cy - h / 2, 0], [cx + w / 2, cy + h / 2 - f, 0], [cx + w / 2 - f, cy + h / 2, 0],
           [cx - w / 2, cy + h / 2, 0]]
    body = Polygon(*pts, fill_color=CARD, fill_opacity=1, stroke_color=DIM, stroke_width=4)
    fold = Polygon([cx + w / 2 - f, cy + h / 2, 0], [cx + w / 2 - f, cy + h / 2 - f, 0], [cx + w / 2, cy + h / 2 - f, 0],
                   fill_color=GHOST, fill_opacity=1, stroke_color=DIM, stroke_width=3)
    ls = [Line([cx - w / 2 + 0.18, cy + h / 2 - 0.5 - i * 0.24, 0], [cx + w / 2 - 0.18, cy + h / 2 - 0.5 - i * 0.24, 0], color=GHOST, stroke_width=4)
          for i in range(lines)]
    return VGroup(body, fold, *ls)


def a4_binfile(cx, cy, w=1.0, h=1.3):
    """A binary file: the page with a grid of small grey squares where text would be (an idea drawing: bytes, not real data)."""
    pg = a4_page(cx, cy, w, h, lines=0)
    shades = [BAR1, BAR3, BAR2, GHOST]
    sq = []
    for i in range(5):
        for j in range(4):
            c = shades[(i * 7 + j * 3 + i * j) % 4]
            sq.append(Rectangle(width=0.15, height=0.15, fill_color=c, fill_opacity=1, stroke_width=0).move_to(
                [cx - 0.3 + j * 0.2, cy + 0.12 - i * 0.2, 0]))
    return VGroup(pg, *sq)


def a4_no(x, y, r=0.3, sw=7):
    """A prohibition mark (ink ring + bar), standing alone."""
    ring = Circle(radius=r, stroke_color=INK, stroke_width=sw).move_to([x, y, 0])
    d = r * 0.7071
    bar = Line([x - d, y + d, 0], [x + d, y - d, 0], color=INK, stroke_width=sw)
    return VGroup(ring, bar)


def a4_iso(cx, cy, s, W, D, H=0.0):
    """An Iso whose projected footprint W x D x H is centred on the scene point (cx, cy)."""
    ox = cx - (W - D) * C30 * s / 2
    oy = cy - ((W + D) / 2 + H) * s / 2
    return Iso(ox, oy, s)


def a4_engine(cx, cy, s=0.85, official=True):
    """An engine: kraft box + (the kit's dark MCP block on top | the empty outlined slot where it would sit)."""
    W = D = 1.5
    H = 0.8
    iso = a4_iso(cx, cy, s, W, D, H)
    d = {"iso": iso, "box": iso.box(0, 0, 0, W, D, H)}
    if official:
        d["mcp"] = iso.mcp(0.45, 0.45, H, 0.6, 0.6, 0.4)
    else:
        d["slot"] = Polygon(*[iso.p(x, y, H) for x, y in [(0.45, 0.45), (1.05, 0.45), (1.05, 1.05), (0.45, 1.05)]],
                            stroke_color=DIM, stroke_width=5, fill_opacity=0)
    d["top"] = iso.p(0.75, 0.75, H + 0.4)        # where a call starts (the block's top)
    d["face"] = iso.p(0.0, 0.75, H * 0.5)         # where it lands (the box's left face)
    return d


# ───────────────────────── B19 · three engines: official MCP | official MCP | none ─────────────────────────
class B19_ThreeEngines(Scene):
    """Act title first. Unity and Unreal each get a kraft box, then an official MCP block drops onto it; a terracotta call goes from the block into
    the editor; then Godot's box arrives with an EMPTY slot where the block would sit."""
    def construct(self):
        title = a4_tl("The Other Two Engines", -6.1, 3.05, 40)
        self.play(FadeIn(title), run_time=0.4)
        cols = {"Unity": -4.3, "Unreal Engine": 0.0, "Godot": 4.3}
        cy = -0.35
        a4_at(self, 1.55)                                          # "Unity"
        u = a4_engine(cols["Unity"], cy, 1.1)
        un = a4_tc("Unity", cols["Unity"], 2.15, 44)
        self.play(FadeIn(un), FadeIn(u["box"], shift=UP * 0.2), run_time=0.45)
        a4_at(self, 2.05)                                          # "Unreal"
        r = a4_engine(cols["Unreal Engine"], cy, 1.1)
        rn = a4_tc("Unreal Engine", cols["Unreal Engine"], 2.15, 44)
        self.play(FadeIn(rn), FadeIn(r["box"], shift=UP * 0.2), run_time=0.45)
        a4_at(self, 3.9)                                           # "official" ... "MCP"
        u["mcp"].shift(UP * 1.3)
        r["mcp"].shift(UP * 1.3)
        self.add(u["mcp"], r["mcp"])
        self.play(u["mcp"].animate.shift(DOWN * 1.3), r["mcp"].animate.shift(DOWN * 1.3), run_time=0.5)
        lu = a4_tc("official MCP", cols["Unity"], -2.2, 36)
        lr = a4_tc("official MCP", cols["Unreal Engine"], -2.2, 36)
        self.play(FadeIn(lu), FadeIn(lr), run_time=0.35)
        a4_at(self, 7.1)                                           # "that lets an AI call the editor's tools directly"
        du = Dot(u["top"], radius=0.12, color=TERRA)
        dr = Dot(r["top"], radius=0.12, color=TERRA)
        self.play(GrowFromCenter(du), GrowFromCenter(dr), run_time=0.25)
        self.play(du.animate.move_to(u["face"]), dr.animate.move_to(r["face"]), run_time=0.8)
        a4_at(self, 9.55)                                          # "Godot has none"
        g = a4_engine(cols["Godot"], cy, 1.1, official=False)
        gn = a4_tc("Godot", cols["Godot"], 2.15, 44)
        self.play(FadeIn(gn), FadeIn(g["box"], shift=UP * 0.2), run_time=0.4)
        lg = a4_tc("none", cols["Godot"], -2.2, 36)
        self.play(Create(g["slot"]), FadeIn(lg), run_time=0.45)
        done(self)


# ───────────────────────── B20 · Unity: public March 2026, open beta, text scenes full of references ─────────────────────────
class B20_UnityBeta(Scene):
    """Phase A: Unity's own docs page and the changelog entry dated 2026-03-03 that made MCP public (real captures). Phase B (before the midpoint):
    the blog's words, quoted not captured. Phase C: Unity's own YAML excerpt, with its fileID cross-references marked."""
    def construct(self):
        un = a4_tl("Unity", -6.1, 2.6, 48)
        sh1, im1, h1 = a4_img("a4_unity_docs.png", 2.1, 1.55, 8.2)
        self.play(FadeIn(un), FadeIn(sh1), FadeIn(im1), run_time=0.45)
        a4_at(self, 1.0)                                           # "went public in March 2026"
        sh2, im2, h2 = a4_img("a4_unity_changelog.png", 2.1, -1.0, 8.2)
        self.play(FadeIn(sh2), FadeIn(im2), run_time=0.45)
        d1 = Dot([-2.45, -1.0, 0], radius=0.11, color=TERRA)
        l1 = a4_tl("public, March 2026", -6.1, -1.0, 32)
        self.play(GrowFromCenter(d1), FadeIn(l1), run_time=0.3)
        a4_at(self, 2.6)                                           # "open beta"
        l2 = a4_tl("open beta", -6.1, 1.75, 44)
        self.play(FadeIn(l2), run_time=0.3)
        # phase B: the blog's words (before the clip midpoint)
        a4_at(self, 3.9)                                           # "Unity's own blog"
        self.play(FadeOut(sh1), FadeOut(im1), FadeOut(sh2), FadeOut(im2), FadeOut(d1), FadeOut(l1), run_time=0.3)
        pg = a4_page(-0.9, 0.9)
        q = [a4_tl("“may change, be limited,", 0.2, 1.4, 36), a4_tl("or be discontinued", 0.2, 0.85, 36), a4_tl("without notice”", 0.2, 0.3, 36)]
        src = a4_tl("Unity blog, 11 May 2026", 0.2, -0.6, 32)
        nt = a4_tl("quoted, not captured", 0.2, -1.1, 32)
        self.play(FadeIn(pg), run_time=0.3)
        self.play(*[FadeIn(x) for x in q], FadeIn(src), FadeIn(nt), run_time=0.5)
        # phase C (after the midpoint): Unity's own YAML, trimmed
        a4_at(self, 6.75)                                          # "Its scenes are text"
        self.play(FadeOut(pg), *[FadeOut(x) for x in q], FadeOut(src), FadeOut(nt), FadeOut(l2), run_time=0.3)
        hd = a4_tl("text by default", -1.6, 2.4, 40)
        lines = ["--- !u!4 &8", "Transform:", "  m_GameObject: {fileID: 6}", "  m_Father: {fileID: 0}"]
        ys = [1.55, 0.95, 0.35, -0.25]
        ml = [a4_ml(s, -1.6, y) for s, y in zip(lines, ys)]
        self.play(FadeIn(hd), FadeIn(ml[0]), FadeIn(ml[1]), run_time=0.4)
        a4_at(self, 8.0)                                           # "by default"
        self.play(FadeIn(ml[2]), FadeIn(ml[3]), run_time=0.4)
        sc = a4_tl("Unity Manual, trimmed", -1.6, -2.0, 32)
        self.play(FadeIn(sc), run_time=0.25)
        a4_at(self, 9.15)                                          # "YAML"
        ya = a4_tl("YAML", 3.6, 2.4, 40)
        self.play(FadeIn(ya), run_time=0.3)
        a4_at(self, 10.0)                                          # "packed with cross-references"
        k1 = Dot([-1.95, 0.35, 0], radius=0.1, color=TERRA)
        k2 = Dot([-1.95, -0.25, 0], radius=0.1, color=TERRA)
        cr = a4_tl("cross-references", -1.6, -1.1, 36)
        self.play(GrowFromCenter(k1), GrowFromCenter(k2), FadeIn(cr), run_time=0.35)
        done(self)


# ───────────────────────── B21 · Unreal 5.8: Experimental; Epic's words; binary files ─────────────────────────
class B21_UnrealExperimental(Scene):
    """Left: Unreal's kraft box, an MCP block dropping on, the word Experimental in a tag. Right (before the midpoint): Epic's docs, quoted not
    captured. Bottom: .umap and .uasset as binary files, with a prohibition mark on 'read as text'."""
    def construct(self):
        t1 = a4_tl("Unreal Engine 5.8", -6.1, 2.9, 44)
        self.play(FadeIn(t1), run_time=0.4)
        e = a4_engine(-3.7, 0.55, 0.8)
        a4_at(self, 1.1)                                           # "5.8"
        self.play(FadeIn(e["box"], shift=UP * 0.2), run_time=0.4)
        a4_at(self, 1.9)                                           # "an MCP plug-in"
        e["mcp"].shift(UP * 1.2)
        self.add(e["mcp"])
        self.play(e["mcp"].animate.shift(DOWN * 1.2), run_time=0.45)
        a4_at(self, 3.05)                                          # "in June 2026"
        mo = a4_tl("June 2026", -6.1, 2.3, 32)
        self.play(FadeIn(mo), run_time=0.3)
        a4_at(self, 4.3)                                           # "labelled Experimental"
        pill = RoundedRectangle(width=3.5, height=0.7, corner_radius=0.35, stroke_color=DIM, stroke_width=4, fill_opacity=0).move_to([-3.7, -0.95, 0])
        px = a4_tl("Experimental", -3.7 - 1.75 + 0.7, -0.95, 36)
        pd = Dot([-3.7 - 1.75 + 0.4, -0.95, 0], radius=0.1, color=TERRA)
        self.play(Create(pill), FadeIn(px), GrowFromCenter(pd), run_time=0.4)
        # Epic's own docs, quoted (before the midpoint)
        a4_at(self, 6.35)                                          # "Epic's own documentation"
        pg = a4_page(0.3, 1.3)
        src = a4_tl("Epic, Unreal MCP docs", 1.3, 0.1, 32)
        nt = a4_tl("quoted, not captured", 1.3, -0.4, 32)
        self.play(FadeIn(pg), FadeIn(src), FadeIn(nt), run_time=0.4)
        q = [a4_tl("“Many features are", 1.3, 1.9, 36), a4_tl("incomplete or", 1.3, 1.35, 36), a4_tl("missing.”", 1.3, 0.8, 36)]
        a4_at(self, 7.0)
        self.play(*[FadeIn(x) for x in q], run_time=0.4)
        # the files (after the midpoint)
        a4_at(self, 10.9)                                          # "levels"
        bl = a4_tl("binary", -6.1, -2.1, 40)
        f1 = a4_binfile(-3.2, -2.05, 1.0, 1.1)
        l1 = M(".umap", 32).move_to([-3.2, -3.0, 0])
        self.play(FadeIn(bl), FadeIn(f1), FadeIn(l1), run_time=0.4)
        a4_at(self, 11.35)                                         # "assets"
        f2 = a4_binfile(-1.3, -2.05, 1.0, 1.1)
        l2 = M(".uasset", 32).move_to([-1.3, -3.0, 0])
        self.play(FadeIn(f2), FadeIn(l2), run_time=0.4)
        a4_at(self, 12.85)                                         # "an AI cannot read"
        no = a4_no(0.9, -2.0)
        rt = a4_tl("read as text", 1.45, -2.0, 36)
        self.play(Create(no), FadeIn(rt), run_time=0.45)
        a4_at(self, 14.0)
        ep = a4_tl("per Epic's UE 4.26 docs", 1.45, -2.75, 32)
        self.play(FadeIn(ep), run_time=0.3)
        done(self)


# ───────────────────────── B22 · stars: the community Godot server vs Unity's (real repo-header buttons + a bar each) ─────────────────────────
class B22_StarCounts(Scene):
    """Top row: the best-known community Godot MCP server (the real Fork / Star buttons of its GitHub header, Star 6k) and its bar; its last push in
    April. Second row: Unity's biggest community server (real buttons, Star 14.8k) and its bar, with ticks at 1x and 2x of Godot's. Scale: 0.4 units
    per thousand stars. The repo names are set as labels beside the real buttons."""
    def construct(self):
        K = 0.4
        X0 = -5.6
        gl = a4_tl("Godot", -6.1, 3.05, 40)
        rg = Circle(radius=0.13, stroke_color=DIM, stroke_width=5).move_to([a4_nx("Godot", -6.1, 40, 0.5), 3.05, 0])
        c1 = a4_tl("no official MCP", a4_nx("Godot", -6.1, 40, 0.8), 3.05, 32)
        self.play(FadeIn(gl), Create(rg), FadeIn(c1), run_time=0.4)
        a4_at(self, 2.3)                                           # "several from the community"
        shG, imG, hG = a4_img("a4_godot_mcp_banner.png", 2.8, 2.15, 6.42)
        nG = a4_tl("Coding-Solo/godot-mcp", -6.0, 2.15, 32)
        self.play(FadeIn(nG), FadeIn(shG), FadeIn(imG), run_time=0.45)
        c2 = a4_tl("community server", 1.5, 3.05, 32)
        self.play(FadeIn(c2), run_time=0.25)
        a4_at(self, 4.9)                                           # "about six thousand stars"
        bG = Rectangle(width=6.0 * K, height=0.42, fill_color=BAR1, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([X0 + 6.0 * K / 2, 1.15, 0])
        self.play(GrowFromEdge(bG, LEFT), run_time=0.6)
        vG = a4_tl("6.0k", X0 + 6.0 * K + 0.3, 1.15, 40)
        ft = a4_tl("GitHub stars, 9 Oct 2026", -6.1, -3.0, 32)
        self.play(FadeIn(vG), FadeIn(ft), run_time=0.3)
        a4_at(self, 7.3)                                           # "has not been updated since April"
        dG = Dot([-1.5, 1.15, 0], radius=0.1, color=TERRA)
        pG = a4_tl("last push 16 Apr 2026", -1.2, 1.15, 32)
        self.play(GrowFromCenter(dG), FadeIn(pG), run_time=0.35)
        a4_at(self, 9.25)                                          # "Unity's biggest community server"
        ul = a4_tl("Unity", -6.1, 0.3, 40)
        shU, imU, hU = a4_img("a4_unity_mcp_banner.png", 3.35, -0.6, 5.30)
        nU = a4_tl("CoplayDev/unity-mcp", -6.0, -0.6, 32)
        self.play(FadeIn(ul), FadeIn(nU), FadeIn(shU), FadeIn(imU), run_time=0.45)
        c3 = a4_tl("community server", a4_nx("Unity", -6.1, 40, 0.8), 0.3, 32)
        bU = Rectangle(width=14.8 * K, height=0.42, fill_color=BAR1, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to(
            [X0 + 14.8 * K / 2, -1.55, 0])
        self.play(FadeIn(c3), GrowFromEdge(bU, LEFT), run_time=0.9)
        vU = a4_tl("14.8k", X0 + 14.8 * K + 0.3, -1.55, 40)
        dU = Dot([2.2, -1.55, 0], radius=0.1, color=TERRA)
        pU = a4_tl("last push 8 Oct 2026", 2.45, -1.55, 32)
        self.play(FadeIn(vU), GrowFromCenter(dU), FadeIn(pU), run_time=0.3)
        a4_at(self, 11.4)                                          # "more than twice that"
        t1 = Line([X0 + 6.0 * K, -1.23, 0], [X0 + 6.0 * K, -1.95, 0], color=DIM, stroke_width=5)
        t2 = Line([X0 + 12.0 * K, -1.23, 0], [X0 + 12.0 * K, -1.95, 0], color=DIM, stroke_width=5)
        n1 = a4_tc("1×", X0 + 6.0 * K, -2.35, 32)
        n2 = a4_tc("2×", X0 + 12.0 * K, -2.35, 32)
        self.play(Create(t1), Create(t2), FadeIn(n1), FadeIn(n2), run_time=0.4)
        done(self)


# ───────────────────────── B23 · "better MCP story?" No. The comparison, plainly ─────────────────────────
class B23_NoBetterStory(Scene):
    """A drawn table: rows official MCP / scenes as text / command line / licence, columns Godot / Unity / Unreal. Terracotta dot = has it, grey ring =
    lacks it. 'No.' lands with the MCP row (before the midpoint); 'no bridge needed' on 'basic work'; the text row on 'its files are plain text', the command-line row on 'its command line is complete', the licence row last."""
    def construct(self):
        CX = {"Godot": -1.7, "Unity": 1.3, "Unreal": 4.3}
        hd = a4_tl("better MCP story?", -6.1, 2.95, 40)
        self.play(FadeIn(hd), run_time=0.35)
        # legend + header + rules
        ld = Dot([1.75, 2.95, 0], radius=0.1, color=TERRA)
        lt = a4_tl("has it", 2.05, 2.95, 32)
        lr = Circle(radius=0.1, stroke_color=DIM, stroke_width=4).move_to([3.65, 2.95, 0])
        lt2 = a4_tl("lacks it", 3.95, 2.95, 32)
        heads = [a4_tc(k, x, 2.0, 36) for k, x in CX.items()]
        rules = [Line([-6.1, y, 0], [6.0, y, 0], color=GHOST, stroke_width=4) for y in (1.65, 0.75, -0.15, -1.05, -1.95)]
        self.play(FadeIn(ld), FadeIn(lt), Create(lr), FadeIn(lt2), *[FadeIn(h) for h in heads], Create(rules[0]), run_time=0.5)
        rows = [("official MCP", 1.2, [("none", 0), ("beta", 1), ("experimental", 1)]),
                ("scenes as text", 0.3, [("yes", 1), ("yes, YAML", 1), ("no", 0)]),
                ("command line", -0.6, [("yes", 1), ("yes", 1), ("yes", 1)]),
                ("licence", -1.5, [("MIT", None), ("proprietary", None), ("proprietary", None)])]

        def mkrow(r):
            name, y, cells = r
            grp = [a4_tl(name, -6.1, y, 34)]
            for (txt, has), x in zip(cells, CX.values()):
                grp.append(a4_tc(txt, x, y, 34))
                if has is not None:
                    px = x - a4_w(txt, 34) / 2.0 - 0.32
                    grp.append(Dot([px, y, 0], radius=0.1, color=TERRA) if has else Circle(radius=0.1, stroke_color=DIM, stroke_width=4).move_to([px, y, 0]))
            return grp
        a4_at(self, 1.75)                                          # "the better MCP story"
        r1 = mkrow(rows[0])
        self.play(Create(rules[1]), *[FadeIn(x) for x in r1], run_time=0.5)
        a4_at(self, 3.15)                                          # "it does not"
        no = a4_tl("No.", -1.7, 2.95, 48, INK, True)
        self.play(FadeIn(no), run_time=0.3)
        a4_at(self, 5.75)                                          # "for the basic work" (after the midpoint)
        nb = a4_tc("no bridge needed", CX["Godot"], -2.5, 36)
        self.play(FadeIn(nb), run_time=0.3)
        a4_at(self, 6.75)                                          # "its files are plain text"
        r2 = mkrow(rows[1])
        self.play(Create(rules[2]), *[FadeIn(x) for x in r2], run_time=0.45)
        a4_at(self, 8.15)                                          # "its command line is complete"
        r3 = mkrow(rows[2])
        self.play(Create(rules[3]), *[FadeIn(x) for x in r3], run_time=0.45)
        a4_at(self, 9.2)                                           # "complete" (the honest rest of the table)
        r4 = mkrow(rows[3])
        self.play(Create(rules[4]), *[FadeIn(x) for x in r4], run_time=0.4)
        done(self)


# ───────────────────────── B24 · two cards kept apart: contributing TO Godot / making a game WITH Godot ─────────────────────────
class B24_TwoThings(Scene):
    """A divider and two headings keep the two things apart. Left (before the midpoint): the Godot Foundation's real post header and two short
    quotes from the same page, with a prohibition mark by the agents line. Right (lands at 'Using an AI to make a game'): 1.4 s of REAL gameplay of
    the walker-claude capture, stepped at 10 fps, labelled 'scripted input, recorded 2026-10-09'."""
    def construct(self):
        dv = Line([0, 3.15, 0], [0, -3.15, 0], color=DIM, stroke_width=5)
        hl = a4_tl("contributing TO Godot", -6.1, 2.85, 36)
        hr = a4_tl("making a game WITH Godot", 0.4, 2.85, 36)
        self.play(Create(dv), FadeIn(hl), FadeIn(hr), run_time=0.5)
        a4_at(self, 1.75)                                          # "In June 2026"
        sh, im, h = a4_img("a4_policy_title.png", -3.1, 1.85, 6.0)
        self.play(FadeIn(sh), FadeIn(im), run_time=0.4)
        a4_at(self, 4.3)                                           # "engine code must be human-written"
        q1 = [a4_tl("“We require all code to", -5.3, 0.85, 34), a4_tl("be human authored.”", -5.3, 0.4, 34)]
        self.play(*[FadeIn(x) for x in q1], run_time=0.4)
        a4_at(self, 6.25)                                          # "and would ban autonomous agents"
        q2 = [a4_tl("“No autonomous AI agent", -5.3, -0.45, 34), a4_tl("use or vibe coding”", -5.3, -0.9, 34)]
        self.play(*[FadeIn(x) for x in q2], run_time=0.4)
        sr = a4_tl("Godot Foundation", -5.3, -1.7, 32)
        s2 = a4_tl("30 Jun 2026, same page", -5.3, -2.2, 32)
        self.play(FadeIn(sr), FadeIn(s2), run_time=0.3)
        a4_at(self, 7.85)                                          # "its repository" (after the midpoint)
        no = a4_no(-5.8, -0.68, 0.26, 6)
        self.play(Create(no), run_time=0.35)
        # the right card: a real game, after the midpoint
        a4_at(self, 11.35)                                         # "Using an AI to make a game with Godot"
        win = ImageMobject(A4P + "a4_game_00.png").set_width(5.4).move_to([3.2, 0.7, 0])
        gsh = Rectangle(width=5.4, height=5.4 * 720 / 1280, fill_color=GHOST, fill_opacity=1, stroke_width=0).move_to([3.27, 0.63, 0])
        self.play(FadeIn(gsh), FadeIn(win), run_time=0.4)
        cap1 = a4_tl("scripted input,", 0.55, -1.3, 32)
        cap2 = a4_tl("recorded 2026-10-09", 0.55, -1.75, 32)
        arrs = []
        for i in range(15):
            arrs.append(getattr(ImageMobject(A4P + f"a4_game_{i:02d}.png"), "pixel_array", None))
        if arrs[0] is not None and hasattr(arrs[0], "shape"):
            def step(m, a):
                m.pixel_array = arrs[min(14, int(a * 15))].copy()
            self.play(UpdateFromAlphaFunc(win, step), FadeIn(cap1), FadeIn(cap2), run_time=1.4, rate_func=linear)
        else:                                                      # Gate A's stub carries no pixels
            self.play(win.animate.shift(UP * 0.01), FadeIn(cap1), FadeIn(cap2), run_time=1.4)
        a4_at(self, 13.8)                                          # "a different thing"
        dt = a4_tl("a different thing", 0.55, -2.6, 40)
        self.play(FadeIn(dt), run_time=0.3)
        done(self)
