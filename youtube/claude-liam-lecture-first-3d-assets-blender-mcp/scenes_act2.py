"""ACT II · Learn the Window First  (B15–B20, all Manim)

One cast for the act: ONE real Blender 5.1.2 window with the lantern selected (Blender's own screenshot operator, run by a
script: pantry/ev_bl_object_mode.png and the Act II captures pantry/a2_bl_*, all the same 3456 x 2006 layout; part boxes from
evidence/gui/NOTES.md), seen through a fixed viewer frame on the cream stage (x -2.95..6.3, y -3.5..3.5). The sidebar is
closed until B18, where "Press N" opens it (two real windows, before and after). The camera moves INSIDE the frame: four cream
masks hide the rest of the capture, so the screenshot is cropped and zoomed, never shrunk (s = 4K pixels per screenshot
pixel; every held view is s >= 1.25, which puts Blender's 33-px capitals at >= 41 px, the GATE T floor). One terracotta ring
marks the part the sentence names; labels sit on the cream column to the left; six step dots count the six parts. Nothing is
drawn on a Blender screen except that ring and a spark. Camera numbers were chosen so every MIDPOINT frame passes GATE T
(see evidence/act2/qa/check_midpoints.sh: Blender's small dark UI shapes are read as text runs at some zooms). Cue times are
faster-whisper word times of the measured audio (evidence/act2/word_times.json), rescaled if a beat is re-voiced.
"""

# ── viewer frame (scene units) and the screenshot grid ──────────────────────────────────────────────────────────────
A2_WX0, A2_WY0, A2_WX1, A2_WY1 = -2.95, -3.5, 6.3, 3.5
A2_WCX, A2_WCY = (A2_WX0 + A2_WX1) / 2.0, (A2_WY0 + A2_WY1) / 2.0
A2_WW, A2_WH = A2_WX1 - A2_WX0, A2_WY1 - A2_WY0
A2_IW, A2_IH = 3456.0, 2006.0                      # every Blender window capture used here
A2_PX = 270.0                                       # 4K pixels per scene unit (3840 / 14.222)
A2_LX = -6.2                                        # left edge of the label column

# the captures (real windows; see evidence/gui/NOTES.md and evidence/act2/)
A2_IMG = {
    "object": "pantry/ev_bl_object_mode.png",        # the finished lantern, selected, sidebar open
    "closed": "pantry/a2_bl_sidebar_closed.png",     # the same window with the sidebar hidden (Act II capture)
    "orbit1": "pantry/a2_bl_orbit1_closed.png",      # front view, sidebar closed (= ev_bl_orbit_1.png minus the sidebar)
    "orbit3": "pantry/a2_bl_orbit3_closed.png",      # top view, sidebar closed
    "orbit4": "pantry/a2_bl_orbit4_closed.png",      # three-quarter, zoomed in, sidebar closed
    "parts_c": "pantry/a2_bl_parts_closed.png",      # the five-object lantern, sidebar closed (Act II capture)
    "ledit":   "pantry/a2_bl_lantern_edit_closed.png",  # the lantern in EDIT Mode, roof selected, sidebar closed (Act II capture)
}

# camera states: (cx, cy) = screenshot pixel at the frame centre, s = 4K px per screenshot px
A2_CAM = {
    "V":     (999.0, 956.0, 1.25),      # the free viewport + toolbar (B16, B17)
    "O":     (2675.0, 640.0, 1.6),      # the Outliner
    "O2":    (2900.0, 560.0, 2.0),      # the Outliner, closer (the tree)
    "P":     (2624.0, 1376.0, 1.5),     # the Properties editor
    "S":     (2026.5, 760.0, 1.6),      # the sidebar (N): Transform, Location, Rotation (the navigation gizmo just out of view)
    "S4":    (2026.5, 1415.0, 1.6),     # the sidebar, lower: Scale, Dimensions
    "M":     (960.0, 797.0, 1.3),       # the header + the lantern (mode selector)
}

# part boxes in screenshot pixels (x0, y0, x1, y1), from evidence/gui/NOTES.md (rings sit just inside or round them)
A2_BOX = {
    "viewport":   (244, 228, 1940, 1690),     # the 3D viewport's free area (sidebar closed), as far as the frame shows it
    "toolbar":    (22, 236, 250, 1568),       # the toolbar's icon strip
    "outliner":   (2462, 122, 3430, 924),
    "properties": (2462, 962, 3430, 1896),
    "sidebar":    (1316, 240, 2440, 1100),    # the sidebar's top: tab strip + Transform, Location, Rotation (the part camera S frames)
    "location":   (1366, 352, 2312, 684),
    "rotation":   (1366, 690, 2312, 1104),
    "scale":      (1366, 1096, 2312, 1418),
    "dimensions": (1366, 1430, 2312, 1756),
    "header":     (24, 112, 1900, 206),
    "selector":   (178, 110, 628, 206),
    "roof":       (486, 538, 1006, 860),      # the lantern's roof: 12 selected faces and their points (Edit Mode)
    "lantern":    (492, 538, 1038, 1430),
}

# measured audio length when the cue times were taken (cues are rescaled if a beat is re-voiced)
A2_DUR = {"B15": 8.81, "B16": 7.04, "B17": 7.91, "B18": 10.11, "B19": 9.32, "B20": 6.44}


def a2_at(self, t):
    """Wait until t seconds into the beat (a faster-whisper word time, rescaled to the current audio)."""
    bid = type(self).__name__.split("_")[0]
    tgt = _TARGET.get(bid, 0)
    if not tgt:
        return
    gap = t * tgt / A2_DUR.get(bid, tgt) - _elapsed(self)
    if gap > 0.02:
        self.wait(gap)


def a2_view(cam):
    """Clamp a camera so the frame never shows past the screenshot's edges. Returns (cx, cy, u) with u = scene units per px."""
    cx, cy, s = cam
    u = s / A2_PX
    vw, vh = A2_WW / u, A2_WH / u
    cx = min(max(cx, vw / 2.0), A2_IW - vw / 2.0)
    cy = min(max(cy, vh / 2.0), A2_IH - vh / 2.0)
    return cx, cy, u


def a2_pt(cam, x, y):
    """A screenshot pixel -> its scene point under camera cam."""
    cx, cy, u = a2_view(cam)
    return np.array([A2_WCX + (x - cx) * u, A2_WCY - (y - cy) * u, 0.0])


def a2_place(cam):
    """(height, centre offset from the frame centre) of a full screenshot under camera cam."""
    cx, cy, u = a2_view(cam)
    return A2_IH * u, np.array([(A2_IW / 2.0 - cx) * u, -(A2_IH / 2.0 - cy) * u, 0.0])


def a2_img(key, cam):
    """A real capture under camera cam (positioned by a shift from the frame centre)."""
    h, off = a2_place(cam)
    im = ImageMobject(A2_IMG[key]).set_height(h)
    im.move_to([A2_WCX, A2_WCY, 0])
    im.shift(off)
    im.set_z_index(0)
    return im


def a2_cam_anims(imgs, cam):
    """Camera move: every capture layer goes to camera cam (same similarity transform for all)."""
    h, off = a2_place(cam)
    c = np.array([A2_WCX, A2_WCY, 0.0]) + off
    return [im.animate.set_height(h).move_to(c) for im in imgs]


def a2_ring(cam, part, sw=8):
    """The one terracotta ring: a closed rounded rectangle round a part, thick stroke, no fill."""
    x0, y0, x1, y1 = A2_BOX[part]
    cx, cy, u = a2_view(cam)
    r = RoundedRectangle(width=(x1 - x0) * u, height=(y1 - y0) * u, corner_radius=0.16, stroke_color=TERRA,
                         stroke_width=sw, fill_opacity=0)
    r.move_to(a2_pt(cam, (x0 + x1) / 2.0, (y0 + y1) / 2.0))
    r.set_z_index(2)
    return r


def a2_stage(self):
    """Four cream masks round the viewer frame (they crop the capture) and its ink outline."""
    m_l = Rectangle(width=A2_WX0 + 7.111 + 0.02, height=8.2, fill_color=STAGE, fill_opacity=1, stroke_width=0).to_edge(LEFT, buff=0)
    m_r = Rectangle(width=7.111 - A2_WX1 + 0.02, height=8.2, fill_color=STAGE, fill_opacity=1, stroke_width=0).to_edge(RIGHT, buff=0)
    m_t = Rectangle(width=14.4, height=4.0 - A2_WY1 + 0.02, fill_color=STAGE, fill_opacity=1, stroke_width=0).to_edge(UP, buff=0)
    m_b = Rectangle(width=14.4, height=4.0 + A2_WY0 + 0.02, fill_color=STAGE, fill_opacity=1, stroke_width=0).to_edge(DOWN, buff=0)
    masks = VGroup(m_l, m_r, m_t, m_b).set_z_index(5)
    frame = Rectangle(width=A2_WW, height=A2_WH, stroke_color=INK, stroke_width=4, fill_opacity=0)
    frame.move_to([A2_WCX, A2_WCY, 0]).set_z_index(6)
    self.add(masks, frame)
    return masks, frame


def a2_lab(s, y, size=40, x=A2_LX):
    """A label on the cream column, left-aligned at x."""
    return T(s, size).move_to([x, y, 0], aligned_edge=LEFT).set_z_index(7)


def a2_rlab(s, y, size=36, x=-3.45):
    """A label right-aligned at x (beside the frame's left edge, level with what it names)."""
    return T(s, size).move_to([x, y, 0], aligned_edge=RIGHT).set_z_index(7)


A2_TY = -3.0                                       # the six step dots
A2_TX = [-6.05 + 0.42 * i for i in range(6)]


def a2_dots():
    return VGroup(*[Circle(radius=0.12, stroke_color=DIM, stroke_width=4, fill_opacity=0).move_to([x, A2_TY, 0])
                    for x in A2_TX]).set_z_index(7)


def a2_fill(i):
    return Dot([A2_TX[i], A2_TY, 0], radius=0.12, color=INK).set_z_index(8)


def a2_tracker(self, n):
    """Six step dots with the first n already filled (continuity from the previous beat)."""
    d = a2_dots()
    f = [a2_fill(i) for i in range(n)]
    self.add(d, *f)
    return d, f


A2_PARTY = -2.3                                    # the part-name label sits just above the dots


# ── B15 marks: orbit, pan, zoom (drawn ideas of the three gestures, ink, beside their words) ──────────────────────────
def a2_orbit_mark(x, y):
    a = Arc(radius=0.27, start_angle=PI * 0.8, angle=-PI * 1.55, stroke_color=INK, stroke_width=6).move_arc_center_to([x, y, 0])
    a.add_tip(tip_length=0.16, tip_width=0.16)
    return VGroup(a, Dot([x, y, 0], radius=0.06, color=INK)).set_z_index(7)


def a2_pan_mark(x, y):
    arms = VGroup(*[Arrow([x, y, 0], [x + 0.32 * dx, y + 0.32 * dy, 0], buff=0, stroke_width=6, color=INK, tip_length=0.13,
                          max_tip_length_to_length_ratio=0.5) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))])
    return arms.set_z_index(7)


def a2_zoom_mark(x, y):
    lens = Circle(radius=0.2, stroke_color=INK, stroke_width=6).move_to([x - 0.06, y + 0.06, 0])
    handle = Line([x + 0.09, y - 0.09, 0], [x + 0.3, y - 0.3, 0], color=INK, stroke_width=8)
    plus = VGroup(Line([x - 0.15, y + 0.06, 0], [x + 0.03, y + 0.06, 0], color=INK, stroke_width=5),
                  Line([x - 0.06, y - 0.03, 0], [x - 0.06, y + 0.15, 0], color=INK, stroke_width=5))
    return VGroup(lens, handle, plus).set_z_index(7)


# ── B15 · open Blender and just look: orbit, pan, zoom (carries the act title) ────────────────────────────────────────
class B15_LookFirst(Scene):
    def construct(self):
        a2_stage(self)
        cam = A2_CAM["V"]
        t1 = a2_lab("Learn the", 2.85)
        t2 = a2_lab("Window First", 2.25)
        icon = ImageMobject("pantry/ev_icon_blender.png").set_height(1.9).move_to([A2_WCX, A2_WCY, 0]).set_z_index(1)
        self.add(t1, t2, icon)
        a2_at(self, 1.55)                                            # "open Blender"
        img = a2_img("orbit1", cam)
        self.play(FadeOut(icon), FadeIn(img), run_time=0.5)
        a2_at(self, 3.45)                                            # "Orbit": a real second viewpoint
        img2 = a2_img("closed", cam)
        m1, l1 = a2_orbit_mark(-5.85, 0.95), a2_lab("orbit", 0.95, 36, -5.15)
        self.play(FadeIn(img2), Create(m1), FadeIn(l1), run_time=0.45)
        self.remove(img)
        a2_at(self, 3.9)                                             # "pan"
        m2, l2 = a2_pan_mark(-5.85, -0.15), a2_lab("pan", -0.15, 36, -5.15)
        self.play(Create(m2), FadeIn(l2), run_time=0.35)
        a2_at(self, 4.5)                                             # "and zoom" (just after the clip's midpoint)
        img3 = a2_img("orbit4", cam)
        m3, l3 = a2_zoom_mark(-5.85, -1.25), a2_lab("zoom", -1.25, 36, -5.15)
        self.play(FadeIn(img3), Create(m3), FadeIn(l3), run_time=0.45)
        self.remove(img2)
        a2_at(self, 5.75)                                            # "spend a short session"
        img4 = a2_img("orbit3", cam)
        self.play(FadeIn(img4), run_time=0.5)
        self.remove(img3)
        a2_at(self, 6.95)                                            # "with no prompting at all"
        img5 = a2_img("closed", cam)
        self.play(FadeIn(img5), run_time=0.5)
        self.remove(img4)
        done(self)


# ── B16 · six parts; the first: the 3D viewport ───────────────────────────────────────────────────────────────────────
class B16_Viewport(Scene):
    def construct(self):
        a2_stage(self)
        img = a2_img("closed", A2_CAM["V"])
        self.add(img)
        a2_at(self, 0.95)                                            # "name six parts"
        dots = a2_dots()
        six = a2_lab("six parts", A2_PARTY)
        self.play(LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.3), FadeIn(six), run_time=0.8)
        a2_at(self, 2.7)                                             # "First, the 3D viewport"
        name = a2_lab("3D viewport", A2_PARTY)
        self.play(FadeOut(six), FadeIn(name), GrowFromCenter(a2_fill(0)), run_time=0.45)
        a2_at(self, 3.62)                                            # ring on "viewport" (after the midpoint: a ring round
        ring = a2_ring(A2_CAM["V"], "viewport")                      # viewport pixels must not be in GATE T's frame)
        self.play(Create(ring), run_time=0.5)
        a2_at(self, 4.9)                                             # "where your three-D model lives"
        self.play(Transform(ring, a2_ring(A2_CAM["V"], "lantern")), run_time=0.6)
        done(self)


# ── B17 · the toolbar (move, rotate, scale); the Outliner (every object, as a tree) ────────────────────────────────────
class B17_ToolbarOutliner(Scene):
    def construct(self):
        a2_stage(self)
        img = a2_img("closed", A2_CAM["V"])
        ring = a2_ring(A2_CAM["V"], "lantern")
        name = a2_lab("3D viewport", A2_PARTY)
        self.add(img, ring, name)
        dots, fills = a2_tracker(self, 1)
        # "The toolbar"
        n2 = a2_lab("toolbar", A2_PARTY)
        self.play(Transform(ring, a2_ring(A2_CAM["V"], "toolbar")), FadeOut(name), FadeIn(n2), GrowFromCenter(a2_fill(1)),
                  run_time=0.45)
        tools = []
        for word, t, ys in (("move", 1.65, 612), ("rotate", 2.15, 750), ("scale", 2.8, 891)):
            a2_at(self, t)
            lab = a2_rlab(word, a2_pt(A2_CAM["V"], 0, ys)[1])
            tools.append(lab)
            self.play(FadeIn(lab, shift=RIGHT * 0.15), run_time=0.3)
        a2_at(self, 4.15)                                            # "The Outliner"
        n3 = a2_lab("Outliner", A2_PARTY)
        self.play(*a2_cam_anims([img], A2_CAM["O"]), Transform(ring, a2_ring(A2_CAM["O"], "outliner")),
                  FadeOut(VGroup(*tools)), FadeOut(n2), FadeIn(n3), GrowFromCenter(a2_fill(2)), run_time=0.7)
        a2_at(self, 5.0)                                             # "lists every object": the same scene before its parts were joined
        img3 = a2_img("parts_c", A2_CAM["O"])
        self.play(FadeIn(img3), run_time=0.5)
        self.remove(img)
        a2_at(self, 6.3)                                             # "in the scene, as a tree"
        self.play(*a2_cam_anims([img3], A2_CAM["O2"]), Transform(ring, a2_ring(A2_CAM["O2"], "outliner")), run_time=0.6)
        done(self)


# ── B18 · the Properties editor; press N, the sidebar opens: location, rotation, scale, dimensions ─────────────────────
def a2_key(x, y, s=0.9):
    """A keyboard key with its letter (the N key): an ink-outlined cap on a grey base."""
    base = RoundedRectangle(width=s, height=s, corner_radius=0.14, fill_color=BAR2, fill_opacity=1, stroke_width=0).move_to([x, y - 0.1, 0])
    cap = RoundedRectangle(width=s, height=s, corner_radius=0.14, fill_color=CARD, fill_opacity=1, stroke_color=INK,
                           stroke_width=5).move_to([x, y, 0])
    letter = T("N", 44).move_to([x, y, 0])
    return base.set_z_index(7), VGroup(cap, letter).set_z_index(8)


class B18_PropertiesSidebar(Scene):
    def construct(self):
        a2_stage(self)
        img = a2_img("closed", A2_CAM["P"])
        self.add(img)
        dots, fills = a2_tracker(self, 3)
        # "The Properties editor"
        ring = a2_ring(A2_CAM["P"], "properties")
        n1 = VGroup(a2_lab("Properties", A2_PARTY + 0.55), a2_lab("editor", A2_PARTY))
        self.play(Create(ring), FadeIn(n1), GrowFromCenter(a2_fill(3)), run_time=0.45)
        a2_at(self, 3.15)                                            # "Press N"
        base, key = a2_key(-4.75, 0.6)
        self.play(FadeIn(base), FadeIn(key), FadeOut(ring), run_time=0.2)
        self.play(key.animate.shift(DOWN * 0.1), run_time=0.12)      # the key goes down on "N"
        self.play(key.animate.shift(UP * 0.1), run_time=0.12)
        self.play(*a2_cam_anims([img], A2_CAM["S"]), run_time=0.4)   # to where the sidebar opens
        a2_at(self, 3.95)                                            # "and the sidebar opens"
        img2 = a2_img("object", A2_CAM["S"])
        self.play(FadeIn(img2), run_time=0.4)
        self.remove(img)
        ring = a2_ring(A2_CAM["S"], "sidebar")
        n2 = a2_lab("sidebar", A2_PARTY)
        self.play(Create(ring), FadeOut(n1), FadeIn(n2), GrowFromCenter(a2_fill(4)), run_time=0.45)
        a2_at(self, 6.25)                                            # "location"
        self.play(Transform(ring, a2_ring(A2_CAM["S"], "location")), run_time=0.3)
        a2_at(self, 7.35)                                            # "rotation"
        self.play(Transform(ring, a2_ring(A2_CAM["S"], "rotation")), run_time=0.3)
        a2_at(self, 8.1)                                             # "scale": the camera follows down the panel
        self.play(*a2_cam_anims([img2], A2_CAM["S4"]), Transform(ring, a2_ring(A2_CAM["S4"], "scale")), run_time=0.35)
        a2_at(self, 8.65)                                            # "and dimensions"
        self.play(Transform(ring, a2_ring(A2_CAM["S4"], "dimensions")), run_time=0.3)
        done(self)


# ── B19 · the mode selector: Object Mode (whole objects) and Edit Mode (points and faces) ─────────────────────────────
class B19_ModeSelector(Scene):
    def construct(self):
        a2_stage(self)
        cam = A2_CAM["M"]
        img = a2_img("closed", cam)
        self.add(img)
        dots, fills = a2_tracker(self, 5)
        a2_at(self, 0.2)                                             # "in the viewport's header"
        ring = a2_ring(cam, "header")
        self.play(Create(ring), run_time=0.45)
        a2_at(self, 1.1)                                             # "the mode selector"
        name = a2_lab("mode selector", A2_PARTY)
        self.play(Transform(ring, a2_ring(cam, "selector")), FadeIn(name), GrowFromCenter(a2_fill(5)), run_time=0.45)
        a2_at(self, 3.7)                                             # "where you work on whole objects"
        spark = Dot(a2_pt(cam, 1095, 985), radius=0.13, color=TERRA).set_z_index(3)
        self.play(FadeOut(ring), GrowFromCenter(spark), run_time=0.45)
        a2_at(self, 5.2)                                             # "and Edit Mode"
        img2 = a2_img("ledit", cam)
        ring = a2_ring(cam, "selector")
        self.play(FadeIn(img2), FadeOut(spark), Create(ring), run_time=0.5)
        self.remove(img)
        a2_at(self, 6.95)                                            # "the points and faces of one"
        self.play(Transform(ring, a2_ring(cam, "roof")), run_time=0.5)
        done(self)


# ── B20 · one screenshot of your own session, object selected, into a notes file (a TEMPLATE, nothing typed) ───────
A2_HEADS = [("3D viewport", 0), ("Toolbar", 0), ("Outliner", 0), ("Properties editor", 1), ("Sidebar (N)", 1), ("Mode selector", 1)]
A2_SLOT = (2.75, -2.35, 3.2)                       # the notes file's screenshot slot: centre x, y, width


class B20_NotesFile(Scene):
    def construct(self):
        masks, frame = a2_stage(self)
        cam = A2_CAM["V"]
        img = a2_img("closed", cam)                                  # the act's window, the lantern selected
        self.add(img)
        dots, fills = a2_tracker(self, 6)
        lab = a2_lab("screenshot", A2_PARTY)
        self.add(lab)
        flash = Rectangle(width=A2_WW, height=A2_WH, fill_color=CARD, fill_opacity=1, stroke_width=0).move_to([A2_WCX, A2_WCY, 0]).set_z_index(3)
        a2_at(self, 0.2)                                             # "one screenshot": a shutter flash on the window
        self.add(flash)
        self.play(FadeOut(flash), run_time=0.5)
        a2_at(self, 1.95)                                            # "with an object selected": a spark beside the selected lantern
        spark = Dot(a2_pt(cam, 1095, 985), radius=0.13, color=TERRA).set_z_index(3)
        self.play(GrowFromCenter(spark), run_time=0.4)
        # the notes file (a template: six headings = the six parts; nothing typed in a session)
        card = Rectangle(width=A2_WW, height=A2_WH, fill_color=CARD, fill_opacity=1, stroke_width=0).move_to([A2_WCX, A2_WCY, 0]).set_z_index(3)
        fname = M("BLENDER-NOTES.md", 32).move_to([A2_WX0 + 0.35, 3.0, 0], aligned_edge=LEFT).set_z_index(7)
        tag = T("template", 32).move_to([A2_WX1 - 0.35, 3.0, 0], aligned_edge=RIGHT).set_z_index(7)
        rule = Line([A2_WX0 + 0.3, 2.55, 0], [A2_WX1 - 0.3, 2.55, 0], color=GHOST, stroke_width=4).set_z_index(4)
        heads, ghosts = VGroup(), VGroup()
        for i, (h, col) in enumerate(A2_HEADS):
            hx = A2_WX0 + 0.35 + col * 3.8
            hy = 1.85 - (i % 3) * 1.1
            heads.add(T(h, 32, bold=True).move_to([hx, hy, 0], aligned_edge=LEFT))
            ghosts.add(Line([hx, hy - 0.45, 0], [hx + 2.6, hy - 0.45, 0], color=GHOST, stroke_width=10))
        heads.set_z_index(7); ghosts.set_z_index(4)
        shot_h = T("Screenshot", 32, bold=True).move_to([A2_WX0 + 0.35, -1.55, 0], aligned_edge=LEFT).set_z_index(7)
        sx, sy, sw = A2_SLOT
        thumb = ImageMobject("pantry/a2_b20_screenshot.png").set_width(A2_WW).move_to([A2_WCX, A2_WCY, 0]).set_z_index(4)
        a2_at(self, 3.32)                                            # "to a notes file" (just after the midpoint)
        self.play(FadeIn(card), FadeIn(thumb), FadeOut(spark), FadeOut(lab), run_time=0.3)   # the window becomes one screenshot
        self.remove(img)
        tedge = Rectangle(width=sw, height=sw * A2_IH / A2_IW, stroke_color=INK, stroke_width=4, fill_opacity=0).move_to([sx, sy, 0]).set_z_index(5)
        self.play(thumb.animate.set_width(sw).move_to([sx, sy, 0]), FadeIn(fname), FadeIn(tag), FadeIn(rule), FadeIn(heads),
                  FadeIn(ghosts), FadeIn(shot_h), run_time=0.6)                       # ...and is filed in the notes
        self.play(Create(tedge), FadeIn(a2_lab("notes file", A2_PARTY)), run_time=0.3)
        a2_at(self, 4.6)                                             # "That's your evidence that you looked"
        ok = check(sx + sw / 2 + 0.55, sy + 0.1, 0.22).set_z_index(7)
        self.play(Create(ok), run_time=0.4)
        done(self)
