"""ACT I · What Godot Is  (B01–B05, all Manim)

One cast for the act: REAL captures shown as themselves in grey-framed windows on the cream stage: godotengine.org (home, licence,
download) and a real Godot game (Walker Pong, a recorded run, scripted input), plus real text from this Mac (the `godot --help`
copyright line, `du -sh`, the walker-claude player.gd lines). Drawings carry only ideas (a card pair, two bars, an indent guide)
and are labelled; the one Python block is labelled "illustrative". Nothing is mocked: every capture was taken 2026-10-09.

Frames of the Pong clip: pantry/a1_pong_001..105.jpg (15 fps, cropped to the playfield, 1152x720) from
_conducting-series-evidence/godot-captures/walker-pong/walker-pong-clip.mp4 (ffmpeg, see evidence/act1/README-evidence.md).
"""

A1P = "pantry/"
_A1_FR = {}


def a1_rgba(name):
    """A pantry frame as an RGBA array (cached) for the video updater."""
    if name not in _A1_FR:
        from PIL import Image
        _A1_FR[name] = np.array(Image.open(A1P + name).convert("RGBA"))
    return _A1_FR[name]


def a1_window(name, w, cx, cy):
    """A real capture shown as itself: the image, and a grey (DIM) frame just outside its edge."""
    im = ImageMobject(A1P + name)
    im.set_width(w)
    im.move_to([cx, cy, 0])
    fr = Rectangle(width=w + 0.1, height=im.height + 0.1, stroke_color=DIM, stroke_width=4).move_to([cx, cy, 0])
    return im, fr


def a1_clip(prefix, n, fps, w, cx, cy):
    """A real recorded clip as a window: a pantry frame sequence stepped in time by an updater (starts when added)."""
    im = ImageMobject(A1P + f"{prefix}001.jpg")
    im.set_width(w)
    im.move_to([cx, cy, 0])
    im.a1c = dict(t=0.0, last=0)

    def tick(m, dt):
        a = m.a1c
        a["t"] += dt
        i = min(n - 1, int(a["t"] * fps))
        if i != a["last"]:
            a["last"] = i
            m.pixel_array = a1_rgba(f"{prefix}{i + 1:03d}.jpg")
    im.add_updater(tick)
    fr = Rectangle(width=w + 0.1, height=im.height + 0.1, stroke_color=DIM, stroke_width=4).move_to([cx, cy, 0])
    return im, fr


def a1_t(s, x, y, size=32, color=INK):
    return T(s, size, color).move_to([x, y, 0])


def a1_left(mob, x_left, y):
    """Place a mob so its left edge is at x_left (explicit coordinate; width is the mob's own)."""
    mob.move_to([x_left + mob.width / 2.0, y, 0])
    return mob


def a1_no(x, y, r=0.3, sw=6):
    """A prohibition mark in grey (DIM): ring + bar. Sits beside text, never around it."""
    ring = Circle(radius=r, stroke_color=DIM, stroke_width=sw).move_to([x, y, 0])
    d = r * 0.7071
    bar = Line([x - d, y + d, 0], [x + d, y - d, 0], color=DIM, stroke_width=sw)
    return VGroup(ring, bar)


# ═════════════════════════════ B01 · what Godot is ═════════════════════════════
class B01_WhatGodotIs(Scene):
    def construct(self):
        title = T("What Godot Is", 40).to_corner(UL, buff=0.95)
        pimg, pfr = a1_clip("a1_pong_", 105, 15, 5.4, -3.1, 0.3)
        pl1 = a1_t("a game running in Godot", -3.1, -1.72)
        pl2 = a1_t("recorded run, scripted input", -3.1, -2.22)
        self.add(title, pimg)
        self.play(FadeIn(pfr), FadeIn(pl1), FadeIn(pl2), run_time=0.5)
        # the four things the engine runs, one word at a time on the spoken word (one Text so the baseline is shared)
        row = T("graphics         physics         input         sound", 36).move_to([0.3, -2.92, 0])
        spans = [(0, 8), (8, 15), (15, 20), (20, 25)]
        for (a, b), ph in zip(spans, ("graphics", "physics", "input", "sound")):
            wd = VGroup(*row[a:b])
            dot = Dot([wd.get_center()[0] - wd.width / 2.0 - 0.3, -2.92, 0], radius=0.09, color=INK)
            until(self, ph, lead=0.1)
            self.play(GrowFromCenter(dot), FadeIn(wd), run_time=0.35)
        # with an editor to build it in: a REAL Godot 4.7.2 editor window (it lands after the midpoint: its dark UI fails GATE T at the 50% sample)
        himg, hfr = a1_window("a1_editor.png", 6.0, 3.1, 0.3)
        hl1 = a1_t("the Godot editor", 3.1, -1.72)
        hl2 = a1_t("captured 9 Oct 2026", 3.1, -2.22)
        until(self, "with an editor", lead=0.2)
        self.play(FadeIn(himg), FadeIn(hfr), FadeIn(hl1), FadeIn(hl2), run_time=0.5)
        done(self)


# ═════════════════════════════ B02 · free, open source, MIT ═════════════════════════════
class B02_FreeOpenSource(Scene):
    def construct(self):
        wimg, wfr = a1_window("a1_license_crop.png", 7.0, -2.3, 0.2)
        wl1 = a1_t("godotengine.org/license", -2.3, -2.2)
        wl2 = a1_t("captured 9 Oct 2026", -2.3, -2.72)
        self.play(FadeIn(wimg), FadeIn(wfr), FadeIn(wl1), FadeIn(wl2), run_time=0.6)
        until(self, "under the M I T licence", lead=0.2)
        # the row of the page that says "MIT license" sits at y = +1.47 in the window; the dot marks that row outside the frame
        dot = Dot([1.75, 1.47, 0], radius=0.11, color=TERRA)
        mit = a1_left(T("MIT license", 40), 2.15, 1.47)
        self.play(GrowFromCenter(dot), FadeIn(mit), run_time=0.4)
        rows = []
        for i, (wd, ph) in enumerate((("No account", "No account"), ("No fee", "No fee"), ("No royalty", "No royalty"))):
            y = 0.5 - 0.95 * i
            mark = a1_no(1.75, y)
            lab = a1_left(T(wd, 40), 2.3, y)
            rows.append((mark, lab, ph))
        for mark, lab, ph in rows:
            until(self, ph, lead=0.15)
            self.play(Create(mark), FadeIn(lab), run_time=0.4)
        done(self)


# ═════════════════════════════ B03 · stewardship, not ownership ═════════════════════════════
class B03_LooksAfterNotOwns(Scene):
    def construct(self):
        cl = RoundedRectangle(width=5.2, height=3.2, corner_radius=0.2, stroke_color=DIM, stroke_width=4).move_to([-3.3, 0.95, 0])
        cr = RoundedRectangle(width=5.2, height=3.2, corner_radius=0.2, stroke_color=DIM, stroke_width=4).move_to([3.3, 0.95, 0])
        hl = a1_t("Godot Foundation", -3.3, 2.05, 36)
        hr = a1_t("Contributors", 3.3, 2.05, 36)
        sub = a1_t("a non-profit", -3.3, 1.55)
        self.play(Create(cl), Create(cr), FadeIn(hl), FadeIn(hr), FadeIn(sub), run_time=0.7)
        # its name: a tag
        tag = VGroup(Polygon([-0.32, 0.2, 0], [0.12, 0.2, 0], [0.36, 0, 0], [0.12, -0.2, 0], [-0.32, -0.2, 0],
                             stroke_color=INK, stroke_width=5, fill_opacity=0),
                     Dot([-0.14, 0, 0], radius=0.06, color=INK)).move_to([-5.2, 0.8, 0])
        name = a1_left(T("its name", 36), -4.75, 0.8)
        # its money: a coin
        coin = VGroup(Circle(radius=0.27, stroke_color=INK, stroke_width=5), Dot(radius=0.07, color=INK)).move_to([-5.2, 0.05, 0])
        money = a1_left(T("its money", 36), -4.75, 0.05)
        until(self, "its name", lead=0.2)
        self.play(GrowFromCenter(tag), FadeIn(name), run_time=0.4)
        until(self, "its money", lead=0.2)
        self.play(GrowFromCenter(coin), FadeIn(money), run_time=0.4)
        # it does not own the engine: an ownership arrow across the gap, struck out
        arr = Arrow([-0.62, 0.95, 0], [0.62, 0.95, 0], buff=0, color=DIM, stroke_width=5, tip_length=0.2)
        own = a1_t("owns", 0, 1.5, 32)
        no = a1_no(0, 0.95, r=0.3, sw=6)
        until(self, "It does not own", lead=0.2)
        self.play(Create(arr), FadeIn(own), run_time=0.4)
        self.play(Create(no), run_time=0.3)
        # the code belongs to its contributors: the real copyright line printed by `godot --help`
        c1 = M("(c) 2014-present", 32)
        c2 = M("Godot Engine", 32)
        c3 = M("contributors.", 32)
        code = VGroup(c1, c2, c3).arrange(DOWN, buff=0.22).move_to([3.3, 0.55, 0])
        cap = a1_t("printed by godot --help", 3.3, -1.1)
        until(self, "The code belongs", lead=0.2)
        self.play(FadeIn(code), FadeIn(cap), run_time=0.5)
        # no company can buy it: Godot's own governance words, quoted (not captured)
        q = T("“Godot can't be sold or purchased by any company.”", 36).move_to([0, -2.0, 0])
        qa = a1_t("quoted, not captured: godotengine.org/governance", 0, -2.65)
        until(self, "no company can buy it", lead=0.3)
        self.play(FadeIn(q), FadeIn(qa), run_time=0.5)
        done(self)


# ═════════════════════════════ B04 · version and size ═════════════════════════════
class B04_VersionAndSize(Scene):
    def construct(self):
        # right: Godot's own Mac download page as itself (only the buttons are cropped in: the page's dark artwork fails GATE T)
        dimg, dfr = a1_window("a1_download_btn.jpg", 6.0, 3.1, 0.7)
        dl1 = a1_t("godotengine.org/download/macos", 3.1, -0.75)
        dl2 = a1_t("captured 9 Oct 2026", 3.1, -1.25)
        hero = T("4.7.2", 88).move_to([-3.0, 2.55, 0])
        self.add(hero)
        self.play(FadeIn(dimg), FadeIn(dfr), FadeIn(dl1), FadeIn(dl2), run_time=0.6)
        until(self, "released on", lead=0.2)
        dstamp = a1_t("stable, 18 August 2026", -3.0, 1.7, 36)
        self.play(FadeIn(dstamp), run_time=0.4)
        # sizes: bars in greys, in BYTES (1 MB = 1e6 B = 0.0143 scene units), left edge x = -5.9. GitHub says 170,622,178 B = 170.6 MB;
        # du -sh prints 337M, which is MiB (337 x 1,048,576 B = 353.4 MB), so the second bar is drawn 353.4 MB long, not 337.
        S = 0.0143
        l1 = a1_left(T("170.6 MB: GitHub release zip", 32), -5.9, 0.85)
        b1 = Rectangle(width=170.6 * S, height=0.4, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([-5.9 + 170.6 * S / 2, 0.35, 0])
        l2 = a1_left(T("337M: du -sh on this Mac", 32), -5.9, -0.5)
        b2 = Rectangle(width=353.4 * S, height=0.4, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([-5.9 + 353.4 * S / 2, -1.0, 0])
        until(self, "The Mac download", lead=0.2)
        self.play(FadeIn(l1), run_time=0.3)
        self.play(GrowFromEdge(b1, LEFT), run_time=0.7)
        until(self, "Installed on this Mac", lead=0.2)
        self.play(FadeIn(l2), run_time=0.3)
        self.play(GrowFromEdge(b2, LEFT), run_time=0.9)
        # one application file: a tile and its name
        tile = VGroup(RoundedRectangle(width=0.8, height=0.8, corner_radius=0.14, stroke_color=INK, stroke_width=5),
                      Dot(radius=0.08, color=TERRA)).move_to([-5.5, -2.15, 0])
        tl = a1_left(T("one application file", 32), -4.85, -2.15)
        until(self, "One application file", lead=0.2)
        self.play(GrowFromCenter(tile), FadeIn(tl), run_time=0.5)
        done(self)


# ═════════════════════════════ B05 · GDScript ═════════════════════════════
class B05_GDScriptAndCSharp(Scene):
    def construct(self):
        XL = -6.0
        # GDScript: three real lines of walker-claude/godot/features/player/player.gd (lines 33-35), tab-indented in the file
        d1 = Dot([XL + 0.1, 2.95, 0], radius=0.09, color=TERRA)
        g_lab = a1_left(T("GDScript: real code from the Claude Walker project", 32), XL + 0.4, 2.95)
        g_h = a1_left(M("func reset_at(spawn: Vector2) -> void:", 32), XL, 2.2)
        g_1 = a1_left(M("position = spawn", 32), XL + 0.9, 1.65)
        g_2 = a1_left(M("velocity = Vector2.ZERO", 32), XL + 0.9, 1.1)
        self.play(FadeIn(g_lab), GrowFromCenter(d1), run_time=0.4)
        until(self, "Games are written", lead=0.1)
        self.play(FadeIn(g_h), FadeIn(g_1), FadeIn(g_2), run_time=0.5)
        # Python: the same idea, illustrative
        until(self, "built for Godot", lead=0.4)
        d2 = Dot([XL + 0.1, 0.35, 0], radius=0.09, color=TERRA)
        p_lab = a1_left(T("Python: the same idea, illustrative (not Godot code)", 32), XL + 0.4, 0.35)
        p_h = a1_left(M("def reset_at(spawn: Vector2) -> None:", 32), XL, -0.4)
        p_1 = a1_left(M("position = spawn", 32), XL + 0.9, -0.95)
        p_2 = a1_left(M("velocity = Vector2.ZERO", 32), XL + 0.9, -1.5)
        self.play(FadeIn(p_lab), GrowFromCenter(d2), FadeIn(p_h), FadeIn(p_1), FadeIn(p_2), run_time=0.6)
        # reads a lot like Python: the same indent guide down both blocks
        until(self, "reads a lot like Python", lead=0.2)
        gu1 = Line([XL + 0.4, 1.9, 0], [XL + 0.4, 0.85, 0], color=DIM, stroke_width=5)
        gu2 = Line([XL + 0.4, -0.65, 0], [XL + 0.4, -1.75, 0], color=DIM, stroke_width=5)
        self.play(Create(gu1), Create(gu2), run_time=0.5)
        # or in C sharp: the .NET build, as a chip; the example project: all scripts are .gd
        until(self, "or in C sharp", lead=0.2)
        chip = a1_left(T("C#: needs the .NET build", 32), 1.4, -2.55)
        cd = Dot([1.05, -2.55, 0], radius=0.09, color=INK)
        self.play(GrowFromCenter(cd), FadeIn(chip), run_time=0.4)
        until(self, "The example games", lead=0.2)
        ex = a1_left(T("Claude Walker: 11 scripts, all .gd", 32), XL + 0.4, -2.55)
        ed = Dot([XL + 0.1, -2.55, 0], radius=0.09, color=INK)
        self.play(GrowFromCenter(ed), FadeIn(ex), run_time=0.4)
        done(self)
