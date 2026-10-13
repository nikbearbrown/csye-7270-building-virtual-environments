"""ACT IV · What Godot Builds From a File  (B33A–B41, B43, B44 Manim; B42 is a Remotion BrowserCapture, see lanes/act4.json)

One cast for the act, one story: FILE -> IMPORT SETTINGS -> NAMES -> COLLIDERS.
  * the checkpoint post: the real Blender renders (pantry/a4_post.png, a4_post_hull.png) and its side-view silhouette
    (base 0.6 x 0.1 m, pole 0.16 m wide, 1.8 m tall: the real geometry of the post's final script);
  * the Godot icon as the destination of every file;
  * ONE import file: the demo's enemy.glb.import, quoted line for line (its lines 24 and 25 are the two that matter).
Everything typed in Menlo is real: lines of enemy.glb.import, lines of a recorded glTF export, recorded git output, the
recorded import trees of Godot 4.7.2 (evidence/act4/out/*.log), or the real scene text of enemy.tscn. Nothing is invented.
"""

A4_K = 2.0                                     # side-view silhouette: scene units per metre


# ═════════════════════════════ helpers ═════════════════════════════
def a4_mw(s, size=32):
    """Menlo width of a string, exact at the sizes used (Pango quantises the size: 32 -> 0.2483, 34-38 -> 0.297, 40-44 -> 0.347)."""
    per = 0.2483 if size <= 32 else 0.2975 if size <= 38 else 0.347 if size <= 44 else 0.396
    return per * len(s)


def a4_put(mob, x, y):
    """Place a Text/Group so its LEFT edge sits at x (measured width, never get_left())."""
    return mob.move_to([x + mob.width / 2, y, 0])


def a4_chip(s, x, y, size=36, mono=True, color=INK, sw=4, padx=0.34, hgt=None, dash=False):
    """An outline-only chip with its text. Returns VGroup(box, text). No fill behind text."""
    t = (M(s, size, color) if mono else T(s, size, color)).move_to([x, y, 0])
    w = t.width + 2 * padx
    h = hgt if hgt else 0.0125 * size + 0.55
    if dash:
        box = DashedVMobject(RoundedRectangle(width=w, height=h, corner_radius=0.2, stroke_color=color, stroke_width=sw),
                             num_dashes=26, dashed_ratio=0.55)
    else:
        box = RoundedRectangle(width=w, height=h, corner_radius=0.2, stroke_color=color, stroke_width=sw, fill_opacity=0)
    box.move_to([x, y, 0])
    return VGroup(box, t)


def a4_arrow(a, b, color=INK, w=5, tip=0.2):
    return Arrow(np.array(a, dtype=float), np.array(b, dtype=float), buff=0, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.5)


def a4_x(x, y, s=0.17, color=INK, w=7):
    """A cross mark (two lines) centred on (x, y)."""
    return VGroup(Line([x - s, y - s, 0], [x + s, y + s, 0], color=color, stroke_width=w),
                  Line([x - s, y + s, 0], [x + s, y - s, 0], color=color, stroke_width=w))


def a4_godot(x=5.3, y=0.1, h=1.7):
    ic = ImageMobject("pantry/icon_godot.png").set_height(h).move_to([x, y, 0])
    lb = T("Godot", 34).move_to([x, y - h / 2 - 0.2, 0])
    return ic, lb


# --- side-view silhouette of the post's base + pole, and its colliders (metres -> scene units) ---
A4_MESH = [(-0.3, 0.0), (0.3, 0.0), (0.3, 0.1), (0.08, 0.1), (0.08, 1.8), (-0.08, 1.8), (-0.08, 0.1), (-0.3, 0.1)]
A4_CONCAVE = [(-0.37, -0.07), (0.37, -0.07), (0.37, 0.17), (0.15, 0.17), (0.15, 1.87), (-0.15, 1.87),
              (-0.15, 0.17), (-0.37, 0.17)]                          # the same outline, offset 7 cm so it can be seen
A4_HULL = [(-0.3, 0.0), (0.3, 0.0), (0.3, 0.1), (0.08, 1.8), (-0.08, 1.8), (-0.3, 0.1)]    # the real convex hull of the silhouette


def a4_offset_convex(pts, d):
    """Offset a convex polygon (counter-clockwise or clockwise) outward by d: intersect the shifted neighbouring edges."""
    P = [np.array(p, dtype=float) for p in pts]
    n = len(P)
    area = sum(P[i][0] * P[(i + 1) % n][1] - P[(i + 1) % n][0] * P[i][1] for i in range(n))
    sgn = 1.0 if area > 0 else -1.0                                   # +1 = counter-clockwise
    lines = []
    for i in range(n):
        a, b = P[i], P[(i + 1) % n]
        e = (b - a) / np.linalg.norm(b - a)
        nrm = np.array([e[1], -e[0]]) * sgn                           # outward normal
        lines.append((a + nrm * d, e))
    out = []
    for i in range(n):
        (p1, e1), (p2, e2) = lines[i - 1], lines[i]
        m = np.array([[e1[0], -e2[0]], [e1[1], -e2[1]]])
        t = np.linalg.solve(m, p2 - p1)
        out.append(tuple(p1 + e1 * t[0]))
    return out


def a4_poly(pts, ox, oy, k=A4_K, fill=None, stroke=INK, sw=6, op=1.0):
    """A polygon from metre coordinates; (ox, oy) is where (0, 0) lands (the base's underside centre)."""
    P = [[ox + x * k, oy + y * k, 0] for x, y in pts]
    if fill is None:
        return Polygon(*P, stroke_color=stroke, stroke_width=sw, fill_opacity=0)
    return Polygon(*P, stroke_color=stroke, stroke_width=sw, fill_color=fill, fill_opacity=op)


# ═════════════════════════════ B33A · glTF is the recommended format, in two forms ═════════════════════════════
class B33A_Formats(Scene):
    def construct(self):
        # act title (Title Case serif), as Act I's first picture carries its own
        act = a4_put(T("What  Godot  Builds From a  File", 40), -6.0, 3.0)
        post = ImageMobject("pantry/a4_post.png").set_height(4.1).move_to([-5.3, -0.85, 0])
        gd, gdl = a4_godot(5.3, -0.5, 1.7)
        self.add(act, post, gd, gdl)
        until(self, "Godot lists", lead=0.1)
        title = T("glTF 2.0", 48).move_to([-1.6, 2.0, 0])
        self.play(FadeIn(title), run_time=0.4)
        until(self, "recommended", lead=0.2)
        dot = Dot([0.15, 2.0, 0], radius=0.13, color=TERRA)
        rec = T("recommended", 36).move_to([1.9, 2.0, 0])
        self.play(FadeIn(dot), FadeIn(rec), run_time=0.4)
        until(self, "text form", lead=0.25)
        c1 = a4_chip(".gltf", -0.2, 0.4, 42)
        t1 = T("text", 36).move_to([-0.2, 1.25, 0])
        a1 = a4_arrow([-4.15, -0.6, 0], [-1.7, 0.35, 0])
        a1b = a4_arrow([1.3, 0.35, 0], [4.15, -0.4, 0])
        self.play(FadeIn(c1), FadeIn(t1), Create(a1), Create(a1b), run_time=0.5)
        until(self, "binary form", lead=0.3)
        c2 = a4_chip(".glb", -0.2, -1.7, 42)
        t2 = T("binary", 36).move_to([-0.2, -0.85, 0])
        a2 = a4_arrow([-4.15, -1.2, 0], [-1.7, -1.65, 0])
        a2b = a4_arrow([1.3, -1.65, 0], [4.15, -0.9, 0])
        self.play(FadeIn(c2), FadeIn(t2), Create(a2), Create(a2b), run_time=0.5)
        done(self)


# ═════════════════════════════ B33B · .blend, only through Blender's own exporter ═════════════════════════════
class B33B_Blend(Scene):
    def construct(self):
        chip = a4_chip(".blend", -5.0, 0.1, 44)
        gd, gdl = a4_godot(5.3, 0.1, 1.7)
        self.add(chip, gd, gdl)
        until(self, "directly", lead=0.8)
        left = Line([-3.55, 0.1, 0], [-1.45, 0.1, 0], color=INK, stroke_width=5)           # a line with a gap in the middle
        right = a4_arrow([1.5, 0.1, 0], [4.2, 0.1, 0])
        self.play(Create(left), Create(right), run_time=0.5)
        until(self, "Blender's own exporter", lead=0.3)
        bl = ImageMobject("pantry/icon_blender.png").set_height(1.6).move_to([0.0, 0.1, 0])
        lab = T("its own exporter", 36).move_to([0.0, -1.15, 0])
        self.play(FadeIn(bl, shift=DOWN * 0.3), run_time=0.45)
        self.play(FadeIn(lab), run_time=0.3)
        until(self, "has to be installed", lead=0.3)
        ins = T("installed", 36).move_to([0.45, -1.9, 0])
        ck = check(-0.65, -1.9, 0.2, INK, 8)
        self.play(FadeIn(ins), Create(ck), run_time=0.4)
        done(self)


# ═════════════════════════════ B34 · FBX through ufbx; OBJ cannot carry four things ═════════════════════════════
class B34_FbxObj(Scene):
    def construct(self):
        fbx = a4_chip(".fbx", -5.1, 1.65, 42)
        gd, gdl = a4_godot(5.3, 0.55, 1.6)
        self.add(fbx, gd, gdl)
        until(self, "goes through", lead=0.2)
        l1 = a4_arrow([-3.9, 1.65, 0], [-2.0, 1.65, 0])
        self.play(Create(l1), run_time=0.35)
        uf = a4_chip("ufbx", -0.3, 1.65, 42)
        self.play(FadeIn(uf), run_time=0.35)
        l2 = a4_arrow([1.5, 1.65, 0], [4.2, 0.95, 0])
        self.play(Create(l2), run_time=0.35)
        until(self, "O B J", lead=0.3)
        obj = a4_chip(".obj", -5.1, -1.45, 42)
        self.play(FadeIn(obj), run_time=0.4)
        until(self, "skinning", lead=0.35)
        # (cross x, label left edge, y, text): a cross, then the missing thing
        items = [(-3.2, -2.75, -0.75, "skinning"), (0.6, 1.05, -0.75, "animation"),
                 (-3.2, -2.75, -2.15, "UV2"), (0.6, 1.05, -2.15, "PBR materials")]
        for i, (mx, lx, y, s) in enumerate(items):
            if i == 1:
                until(self, "animation,", lead=0.3)
            if i == 2:
                until(self, "a second U V set", lead=0.3)
            if i == 3:
                until(self, "physically based", lead=0.3)
            self.play(Create(a4_x(mx, y, 0.17)), FadeIn(a4_put(T(s, 36), lx, y)), run_time=0.3)
        done(self)


# ═════════════════════════════ B35 · GLB for a prop, the text form for diffs, the script is the source ═════════════════════════════
A4_DIFF_M = '"metallicFactor":0.800000011920929,'                 # recorded: git diff of the two .gltf exports (evidence/act4/out/forms.log)
A4_DIFF_P = '"metallicFactor":0.20000000298023224,'
A4_DIFF_B = 'Binary files a/old.glb and b/new.glb differ'


class B35_ScriptSource(Scene):
    def construct(self):
        # tableau 1: one file against loose files
        glb = a4_chip(".glb", -3.4, 0.9, 48, sw=5)
        one = T("one file", 40).move_to([-3.4, -0.45, 0])
        self.add(glb)
        until(self, "use G L B", lead=0.2)
        self.play(FadeIn(one), run_time=0.35)
        until(self, "no loose textures", lead=0.35)
        gl = a4_chip(".gltf", 0.7, 0.9, 36)
        bn = a4_chip(".bin", 3.0, 0.9, 36)
        png = a4_chip(".png", 5.1, 0.9, 36, color=DIM, dash=True)
        loose = T("loose files", 40).move_to([3.0, -0.45, 0])
        self.play(FadeIn(gl), FadeIn(bn), FadeIn(png), FadeIn(loose), run_time=0.5)
        # tableau 2: what version control shows
        until(self, "Use the text form", lead=0.05)
        self.play(FadeOut(VGroup(glb, one, gl, bn, png, loose)), run_time=0.3)
        h1 = a4_chip(".gltf", -4.9, 1.75, 36)
        m1 = M("-", 32).move_to([-3.45, 2.05, 0])
        d1 = a4_put(M(A4_DIFF_M, 32), -3.1, 2.05)
        m2 = M("+", 32).move_to([-3.45, 1.45, 0])
        d2 = a4_put(M(A4_DIFF_P, 32), -3.1, 1.45)
        h2 = a4_chip(".glb", -4.9, -0.45, 36)
        d3 = a4_put(M(A4_DIFF_B, 32), -6.0, -1.45)
        self.play(FadeIn(h1), FadeIn(m1), FadeIn(d1), FadeIn(m2), FadeIn(d2), run_time=0.4)
        self.play(FadeIn(h2), FadeIn(d3), run_time=0.4)
        # tableau 3: the script is the source of truth
        until(self, "Either way", lead=0.3)
        self.play(FadeOut(VGroup(h1, m1, d1, m2, d2, h2, d3)), run_time=0.3)
        sc = a4_chip("build_checkpoint_post.py", 0.0, 2.35, 32, sw=5)
        dot = Dot([-3.85, 2.35, 0], radius=0.14, color=TERRA)
        o1 = a4_chip(".glb", -3.2, -0.6, 44)
        o2 = a4_chip(".gltf", 3.2, -0.6, 44)
        ar1 = a4_arrow([-1.3, 1.75, 0], [-2.9, 0.1, 0])
        ar2 = a4_arrow([1.3, 1.75, 0], [2.9, 0.1, 0])
        truth = T("source of truth", 40).move_to([0.0, 0.9, 0])
        self.play(FadeIn(sc), FadeIn(dot), run_time=0.4)
        self.play(Create(ar1), Create(ar2), FadeIn(o1), FadeIn(o2), run_time=0.5)
        self.play(FadeIn(truth), run_time=0.3)
        done(self)


# ═════════════════════════════ B36 · materials cross; shader nodes and lights do not ═════════════════════════════
def a4_lamp(x, y, r=0.3):
    rays = VGroup(*[Line([x + 1.45 * r * np.cos(a), y + 1.45 * r * np.sin(a), 0], [x + 2.0 * r * np.cos(a), y + 2.0 * r * np.sin(a), 0],
                         color=INK, stroke_width=6) for a in [i * PI / 4 for i in range(8)]])
    return VGroup(Circle(radius=r, stroke_color=INK, stroke_width=6, fill_opacity=0).move_to([x, y, 0]), rays)


def a4_nodes(x, y):
    n1 = RoundedRectangle(width=0.8, height=0.55, corner_radius=0.1, stroke_color=INK, stroke_width=5, fill_opacity=0).move_to([x - 0.7, y + 0.15, 0])
    n2 = RoundedRectangle(width=0.8, height=0.55, corner_radius=0.1, stroke_color=INK, stroke_width=5, fill_opacity=0).move_to([x + 0.7, y - 0.15, 0])
    wire = Line([x - 0.3, y + 0.15, 0], [x + 0.3, y - 0.15, 0], color=INK, stroke_width=5)
    return VGroup(n1, wire, n2)


class B36_Materials(Scene):
    def construct(self):
        # tableau 1: one name, three places (recorded: the glTF export's JSON, Godot's import log)
        bl = ImageMobject("pantry/icon_blender.png").set_height(1.5).move_to([-4.3, 2.3, 0])
        nm = a4_put(M("PostMetal", 44), -3.0, 2.3)
        self.add(bl, nm)
        until(self, "metallic-roughness", lead=0.2)
        a1 = a4_arrow([-4.3, 1.45, 0], [-4.3, 1.0, 0])
        gt = T("glTF", 46).move_to([-4.3, 0.55, 0])
        j1 = a4_put(M('"name":"PostMetal",', 36), -3.0, 0.9)
        j2 = a4_put(M('"pbrMetallicRoughness":{', 36), -3.0, 0.2)
        self.play(Create(a1), FadeIn(gt), FadeIn(j1), FadeIn(j2), run_time=0.6)
        until(self, "arrives as a standard material", lead=0.3)
        a2 = a4_arrow([-4.3, 0.05, 0], [-4.3, -0.5, 0])
        gd = ImageMobject("pantry/icon_godot.png").set_height(1.5).move_to([-4.3, -1.5, 0])
        l1 = a4_put(M("StandardMaterial3D", 36), -3.0, -1.2)
        l2 = a4_put(M("resource_name=PostMetal", 36), -3.0, -1.9)
        self.play(Create(a2), FadeIn(gd), FadeIn(l1), FadeIn(l2), run_time=0.6)
        # tableau 2: what stays behind
        until(self, "Blender-only shader nodes", lead=0.45)
        self.play(FadeOut(Group(bl, nm, a1, gt, j1, j2, a2, gd, l1, l2)), run_time=0.3)
        bl2 = ImageMobject("pantry/icon_blender.png").set_height(1.6).move_to([-5.5, 0.5, 0])
        gd2 = ImageMobject("pantry/icon_godot.png").set_height(1.6).move_to([5.5, 0.5, 0])
        wall = Line([1.3, 2.3, 0], [1.3, -2.0, 0], color=INK, stroke_width=9)
        gl = T("glTF", 40).move_to([1.3, 2.75, 0])
        ndg = VGroup(a4_nodes(-3.0, 1.3), T("shader nodes", 36).move_to([-3.0, 0.5, 0]))
        lp = a4_lamp(-3.0, -0.9, 0.3)
        lpl = T("lights", 36).move_to([-3.0, -2.0, 0])
        self.play(FadeIn(bl2), FadeIn(gd2), Create(wall), FadeIn(gl), FadeIn(ndg), FadeIn(lp), FadeIn(lpl), run_time=0.4)
        until(self, "don't cross", lead=0.2)
        self.play(ndg.animate.shift(RIGHT * 2.4), run_time=0.55)
        self.play(ndg.animate.shift(LEFT * 1.0), run_time=0.3)
        until(self, "lights don't", lead=0.2)
        self.play(lp.animate.shift(RIGHT * 2.4), run_time=0.55)
        self.play(lp.animate.shift(LEFT * 1.0), run_time=0.3)
        until(self, "unless you ask", lead=0.2)
        sw = RoundedRectangle(width=1.2, height=0.6, corner_radius=0.3, stroke_color=INK, stroke_width=5, fill_opacity=0).move_to([-2.4, -2.75, 0])
        knob = Dot([-2.65, -2.75, 0], radius=0.2, color=DIM)
        swl = a4_put(T("Punctual Lights", 34), -1.5, -2.75)
        self.play(FadeIn(sw), FadeIn(knob), FadeIn(swl), run_time=0.3)
        on = Dot([-2.15, -2.75, 0], radius=0.2, color=TERRA)
        self.play(FadeOut(knob), FadeIn(on), lp.animate.shift(RIGHT * 4.8), run_time=0.6)
        om = M("OmniLight3D", 32).move_to([3.3, -2.0, 0])
        self.play(FadeIn(om), run_time=0.3)
        done(self)


# ═════════════════════════════ B37 / B38 · the import file ═════════════════════════════
A4_IMPORT = [(23, "nodes/import_as_skeleton_bones=false"), (24, "nodes/use_name_suffixes=false"),
             (25, "nodes/use_node_type_suffixes=false"), (26, "meshes/ensure_tangents=true"),
             (27, "meshes/generate_lods=true")]                       # enemy.glb.import, lines 23-27, verbatim
A4_Y = [1.55, 0.6, -0.35, -1.3, -2.25]                              # line y positions in the card


class B37_ImportFile(Scene):
    def construct(self):
        glb = a4_chip("enemy.glb", -4.35, 2.72, 32, sw=4)
        imp = a4_chip("enemy.glb.import", -0.2, 2.72, 32, sw=4)
        self.add(glb, imp)
        until(self, "with import settings", lead=0.25)
        card = RoundedRectangle(width=11.9, height=5.5, corner_radius=0.25, stroke_color=DIM, stroke_width=4, fill_opacity=0).move_to([-0.05, -0.68, 0])
        self.play(Create(card), run_time=0.4)
        until(self, "These lines decide", lead=0.2)
        rows = []
        for (n, s), y in zip(A4_IMPORT, A4_Y):
            num = M(str(n), 32, DIM).move_to([-4.55, y, 0])
            ln = a4_put(M(s, 32), -3.9, y)
            rows.append(VGroup(num, ln))
        self.play(LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.18), run_time=1.0)
        until(self, "use name suffixes", lead=0.35)
        ring = RoundedRectangle(width=10.6, height=0.72, corner_radius=0.2, stroke_color=INK, stroke_width=6, fill_opacity=0).move_to([0.2, A4_Y[1], 0])
        dot = Dot([-5.55, A4_Y[1], 0], radius=0.13, color=TERRA)
        self.play(Create(ring), FadeIn(dot), run_time=0.35)
        until(self, "use node type suffixes", lead=0.35)
        ring2 = RoundedRectangle(width=10.6, height=0.72, corner_radius=0.2, stroke_color=INK, stroke_width=6, fill_opacity=0).move_to([0.2, A4_Y[2], 0])
        dot2 = Dot([-5.55, A4_Y[2], 0], radius=0.13, color=TERRA)
        self.play(Create(ring2), FadeIn(dot2), run_time=0.35)
        done(self)


def a4_pair(y, lines, x0=-3.0):
    """A two-line card of key=value lines (Menlo 32, the value bold). Returns (card, lines VGroup)."""
    card = RoundedRectangle(width=9.5, height=1.6, corner_radius=0.22, stroke_color=DIM, stroke_width=4, fill_opacity=0).move_to([x0 + 4.4, y, 0])
    g = VGroup()
    for i, (key, val) in enumerate(lines):
        yy = y + 0.38 - 0.76 * i
        k = M(key, 32).move_to([x0 + a4_mw(key) / 2, yy, 0])
        v = Text(val, font=MONO, color=INK, font_size=32, weight="BOLD").move_to([x0 + a4_mw(key) + a4_mw(val) / 2, yy, 0])
        g.add(VGroup(k, v))
    return card, g


class B38_Template(Scene):
    def construct(self):
        k1, k2 = "nodes/use_name_suffixes=", "nodes/use_node_type_suffixes="
        c1, g1 = a4_pair(1.95, [(k1, "false"), (k2, "false")])
        l1 = T("enemy and\nplayer files", 34).move_to([-5.0, 1.95, 0])
        self.add(c1, g1, l1)
        d1 = VGroup(Dot([4.55, 2.33, 0], radius=0.11, color=TERRA), Dot([5.75, 1.57, 0], radius=0.11, color=TERRA))
        until(self, "those two lines are false", lead=0.3)
        self.play(FadeIn(d1), run_time=0.3)
        until(self, "A fresh import", lead=0.2)
        c2, g2 = a4_pair(0.05, [(k1, "true"), (k2, "true")])
        l2 = T("fresh\nimport", 34).move_to([-5.0, 0.05, 0])
        self.play(Create(c2), FadeIn(g2), FadeIn(l2), run_time=0.5)
        until(self, "Copy the demo's import file", lead=0.2)
        l3 = T("your post", 34).move_to([-5.0, -1.85, 0])
        c3, g3 = a4_pair(-1.85, [(k1, "false"), (k2, "false")])
        cp = VGroup(c1.copy(), g1.copy())
        self.play(FadeIn(l3), run_time=0.25)
        self.play(cp.animate.shift(DOWN * 3.8), run_time=0.8)
        self.remove(cp)
        self.add(c3, g3)
        until(self, "collision hints", lead=0.5)
        d3 = VGroup(Dot([4.55, -1.47, 0], radius=0.11, color=TERRA), Dot([5.75, -2.23, 0], radius=0.11, color=TERRA))
        ig = T("naming hints ignored", 36).move_to([1.7, -3.05, 0])
        self.play(FadeIn(d3), FadeIn(ig), run_time=0.4)
        done(self)


# ═════════════════════════════ B39 / B40 · what each suffix builds from one mesh ═════════════════════════════
# The silhouette is the post's base + pole in side view (metres). Recorded in Godot 4.7.2 (evidence/act4/out/suffix-probe.log, fresh import):
#   -col -> MeshInstance3D kept + StaticBody3D/CollisionShape3D ConcavePolygonShape3D;  -convcol -> same, ConvexPolygonShape3D
#   -colonly -> StaticBody3D, ConcavePolygonShape3D (mesh gone);  -convcolonly -> StaticBody3D, ConvexPolygonShape3D;  -noimp -> node gone
def a4_post_mesh(ox, oy, k, faded=False):
    return a4_poly(A4_MESH, ox, oy, k, fill=BAR2, stroke=DIM, sw=4)


class B39_Keeps(Scene):
    def construct(self):
        k, oy = 2.0, -2.75
        ax, bx = -4.7, 1.2
        mA, mB = a4_post_mesh(ax, oy, k), a4_post_mesh(bx, oy, k)
        tA = M("Mesh1-col", 34).move_to([ax, 1.95, 0])
        tB = M("Mesh2-convcol", 34).move_to([bx, 1.95, 0])
        self.add(mA, mB, tA, tB)
        until(self, "keeps its mesh", lead=0.3)
        kept = a4_put(T("mesh kept", 36), -3.3, 0.4)
        self.play(FadeIn(kept), run_time=0.3)
        until(self, "gains a static collision body", lead=0.25)
        oA = a4_poly(A4_CONCAVE, ax, oy, k, stroke=INK, sw=8)
        self.play(Create(oA), run_time=0.7)
        sb = a4_put(T("static body", 36), -3.3, -0.15)
        self.play(FadeIn(sb), run_time=0.25)
        until(self, "same geometry", lead=0.3)
        cv = a4_put(T("concave", 36), -3.3, -0.7)
        self.play(FadeIn(cv), run_time=0.25)
        until(self, "Dash conv col", lead=0.3)
        oB = a4_poly(a4_offset_convex(A4_HULL, 0.07), bx, oy, k, stroke=INK, sw=8)
        self.play(Create(oB), run_time=0.7)
        until(self, "convex shape", lead=0.35)
        kept2 = a4_put(T("mesh kept", 36), 2.7, 0.4)
        sb2 = a4_put(T("static body", 36), 2.7, -0.15)
        cx = a4_put(T("convex", 36), 2.7, -0.7)
        self.play(FadeIn(kept2), FadeIn(sb2), FadeIn(cx), run_time=0.35)
        done(self)


class B40_Removes(Scene):
    def construct(self):
        k, oy = 1.45, -1.55
        xs = [-4.4, 0.1, 4.3]
        m = [a4_post_mesh(x, oy, k) for x in xs]
        tg = [M("Mesh3-colonly", 32).move_to([-4.3, 2.55, 0]), M("Mesh4-convcolonly", 32).move_to([0.15, 2.55, 0]),
              M("Mesh5-noimp", 32).move_to([4.3, 2.55, 0])]
        self.add(*m, *tg)
        until(self, "Dash col only removes", lead=0.2)
        o1 = a4_poly(A4_CONCAVE, xs[0], oy, k, stroke=INK, sw=8)
        self.play(Create(o1), FadeOut(m[0]), run_time=0.7)
        l1 = T("mesh removed", 34).move_to([xs[0], -2.35, 0])
        l1b = T("concave body", 34).move_to([xs[0], -2.9, 0])
        self.play(FadeIn(l1), FadeIn(l1b), run_time=0.3)
        until(self, "Dash conv col only removes", lead=0.2)
        o2 = a4_poly(a4_offset_convex(A4_HULL, 0.07), xs[1], oy, k, stroke=INK, sw=8)
        self.play(Create(o2), FadeOut(m[1]), run_time=0.7)
        l2 = T("mesh removed", 34).move_to([xs[1], -2.35, 0])
        l2b = T("convex body", 34).move_to([xs[1], -2.9, 0])
        self.play(FadeIn(l2), FadeIn(l2b), run_time=0.3)
        until(self, "dash no imp", lead=0.2)
        self.play(FadeOut(m[2]), run_time=0.4)
        xm = a4_x(xs[2], oy + 1.0, 0.45, w=9)
        l3 = T("node removed", 34).move_to([xs[2], -2.35, 0])
        self.play(Create(xm), FadeIn(l3), run_time=0.4)
        done(self)


# ═════════════════════════════ B41 · a collider has to be a mesh in glTF; the usual pattern ═════════════════════════════
def a4_wire_cube(x, y, s=0.5):
    """A Blender empty drawn as a cube: twelve edges in isometric, centred on (x, y)."""
    iso = Iso(x, y - s, 1.0)
    c = [(0, 0, 0), (s, 0, 0), (s, s, 0), (0, s, 0), (0, 0, s), (s, 0, s), (s, s, s), (0, s, s)]
    E = [(0, 1), (1, 2), (2, 3), (3, 0), (4, 5), (5, 6), (6, 7), (7, 4), (0, 4), (1, 5), (2, 6), (3, 7)]
    return VGroup(*[Line(iso.p(*c[a]), iso.p(*c[b]), color=INK, stroke_width=5) for a, b in E])


class B41_Empties(Scene):
    def construct(self):
        # tableau 1: three rows. Recorded in Godot 4.7.2 for glTF (a mesh and an empty, both named ...-colonly); the Collada row is Godot's documentation.
        r1, r2, r3 = 2.0, 0.1, -1.8
        tg1 = T("glTF", 40).move_to([-5.2, r1, 0])
        it1 = a4_poly(A4_MESH, -3.35, r1 - 0.58, 0.65, fill=BAR2, stroke=DIM, sw=4)
        ar1 = a4_arrow([-2.4, r1, 0], [-0.9, r1, 0])
        res1 = a4_put(M("StaticBody3D", 36), -0.55, r1)
        self.add(tg1)
        until(self, "a collider has to be a mesh", lead=0.3)
        self.play(FadeIn(it1), Create(ar1), FadeIn(res1), Create(check(4.3, r1, 0.22, INK, 8)), run_time=0.6)
        until(self, "A Blender empty", lead=0.2)
        tg2 = T("glTF", 40).move_to([-5.2, r2, 0])
        it2 = a4_wire_cube(-3.35, r2, 0.5)
        ar2 = a4_arrow([-2.4, r2, 0], [-0.9, r2, 0])
        res2 = a4_put(M("Node3D", 36), -0.55, r2)
        self.play(FadeIn(tg2), FadeIn(it2), Create(ar2), FadeIn(res2), Create(a4_x(4.3, r2, 0.2)), run_time=0.6)
        until(self, "only with Collada", lead=0.3)
        tg3 = T("Collada", 40).move_to([-4.9, r3, 0])
        it3 = a4_wire_cube(-3.35, r3, 0.5)
        ar3 = a4_arrow([-2.4, r3, 0], [-0.9, r3, 0])
        res3 = a4_put(M("BoxShape3D", 36), -0.55, r3)
        doc = a4_put(T("documented, not run", 32, DIM), -0.55, -2.6)
        self.play(FadeIn(tg3), FadeIn(it3), Create(ar3), FadeIn(res3), Create(check(4.3, r3, 0.22, INK, 8)), FadeIn(doc), run_time=0.6)
        # tableau 2: the pattern, on the real Blender renders of the post and its collision hull (after the midpoint: tableau 1 is on screen at 50%)
        until(self, "the usual pattern", lead=0.1)
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.3)
        post = ImageMobject("pantry/a4_post.png").set_height(4.7).move_to([-2.6, -0.5, 0])
        hull = ImageMobject("pantry/a4_post_hull.png").set_height(4.7).move_to([2.9, -0.5, 0])
        tag = a4_chip("Collision-convcolonly", 2.9, 2.75, 32, sw=4)
        self.play(FadeIn(post), run_time=0.3)
        until(self, "a separate, simple mesh", lead=0.0)
        self.play(FadeIn(hull), FadeIn(tag), run_time=0.45)
        until(self, "invisible", lead=0.3)
        self.play(hull.animate.set_opacity(0.35).move_to([-2.6, -0.5, 0]), tag.animate.move_to([-2.6, 2.75, 0]), run_time=0.7)
        lab = [a4_put(T("invisible", 40), 1.6, 1.2), a4_put(T("convex", 40), 1.6, 0.3),
               a4_put(T("cheap", 40), 1.6, -0.6), a4_put(T("shaped by you", 40), 1.6, -1.5)]
        self.play(FadeIn(lab[0]), run_time=0.25)
        until(self, "convex,", lead=0.25)
        self.play(FadeIn(lab[1]), run_time=0.25)
        until(self, "cheap", lead=0.25)
        self.play(FadeIn(lab[2]), run_time=0.25)
        until(self, "shaped by you", lead=0.25)
        self.play(FadeIn(lab[3]), run_time=0.25)
        done(self)


# ═════════════════════════════ B43 / B44 · the demo's enemy: names against shapes ═════════════════════════════
# enemy.tscn: the five CollisionShape3D nodes sit at lines 472, 476, 480, 484, 488; their shapes are sub-resources at lines 416-423:
#   SubResource("11") SphereShape3D radius 0.68 | ("12") SphereShape3D radius 0.4 | ("13") BoxShape3D size (1.14506, 0.776818, 1.12102)
A4_ENEMY = [("Sphere1", "SphereShape3D"), ("Sphere2", "SphereShape3D"), ("Sphere3", "SphereShape3D"),
            ("Sphere4", "BoxShape3D"), ("Box", "SphereShape3D")]
A4_EY = [1.75, 0.75, -0.25, -1.25, -2.25]


def a4_glyph(kind, x, y, s=0.7):
    if kind == "SphereShape3D":
        return Circle(radius=s / 2, stroke_color=INK, stroke_width=6, fill_color=BAR3, fill_opacity=1).move_to([x, y, 0])
    return Square(side_length=s, stroke_color=INK, stroke_width=6, fill_color=BAR3, fill_opacity=1).move_to([x, y, 0])


class B43_Enemy(Scene):
    def construct(self):
        hdr = a4_put(M("enemy.tscn", 32), -5.9, 2.85)
        self.add(hdr)
        until(self, "wrapper scene", lead=0.2)
        rows = []
        for (name, shape), y in zip(A4_ENEMY, A4_EY):
            chip = a4_put(a4_chip(name, 0.0, y, 34, sw=4, hgt=0.72), -5.9, y)
            ar = a4_arrow([-5.9 + chip.width + 0.2, y, 0], [-2.5, y, 0])
            gl = a4_glyph(shape, -1.8, y)
            tx = a4_put(M(shape, 34), -1.1, y)
            rows.append(VGroup(chip, ar, gl, tx))
        self.play(LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.2), run_time=1.1)
        until(self, "five collision shapes", lead=0.2)
        five = T("5", 110).move_to([5.1, -0.2, 0])
        cite = a4_put(M("lines 472-490", 32, DIM), -5.9, -3.1)
        self.play(FadeIn(five), FadeIn(cite), run_time=0.35)
        until(self, "named Box", lead=0.1)
        d5 = Dot([3.4, A4_EY[4], 0], radius=0.14, color=TERRA)
        self.play(FadeIn(d5), run_time=0.3)
        until(self, "Sphere four", lead=0.1)
        d4 = Dot([3.4, A4_EY[3], 0], radius=0.14, color=TERRA)
        self.play(FadeIn(d4), run_time=0.3)
        done(self)


class B44_Names(Scene):
    def construct(self):
        cx = [-3.1, 3.1]
        kinds = ["SphereShape3D", "BoxShape3D"]
        tags = [a4_chip("Box", cx[0], 2.2, 38), a4_chip("Sphere4", cx[1], 2.2, 38)]
        gl = [a4_glyph("SphereShape3D", cx[0], 0.2, 1.7), a4_glyph("BoxShape3D", cx[1], 0.2, 1.7)]
        self.add(*tags, *gl)
        until(self, "The shape is the fact", lead=0.1)
        cls = [M(kinds[0], 34).move_to([cx[0] + 0.3, -1.35, 0]), M(kinds[1], 34).move_to([cx[1] + 0.3, -1.35, 0])]
        cks = [check(cx[0] - 1.95, -1.35, 0.2, INK, 8), check(cx[1] - 1.55, -1.35, 0.2, INK, 8)]
        self.play(FadeIn(cls[0]), FadeIn(cls[1]), Create(cks[0]), Create(cks[1]), run_time=0.45)
        until(self, "finds collision by name", lead=0.15)
        cur = cursor(5.0, 1.0, 0.5)
        self.add(cur)
        self.play(cur.animate.move_to([cx[0] + 1.0, 1.55, 0]), run_time=0.5)
        until(self, "trusting a label", lead=0.1)
        tl = a4_put(T("a label", 40), -1.6, 2.2)
        self.play(FadeIn(tl), run_time=0.3)
        done(self)
