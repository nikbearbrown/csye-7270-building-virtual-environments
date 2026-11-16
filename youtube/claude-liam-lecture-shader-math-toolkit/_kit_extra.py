# ═════════════════ _kit_extra.py: this film's four helpers (pasted above the scenes by assemble_scenes.py) ═════════════════
# The standard plot (SHOTLIST.md): square axes, a curve, a terracotta dot riding it, a dashed drop line to a ramp strip of 64 narrow tiles in TRUE grays
# (value v drawn as gray v) under the axes at the same x scale. Curves come from evidence/planning-checks/plot_data.py (the shader's own formulas).
import sys as _sys
_sys.path.insert(0, "evidence/planning-checks")
try:
    import plot_data as PD
except Exception:
    PD = None


def plot_with_strip(fn, x=0.0, y=0.5, size=4.4, y_range=(0.0, 1.0), strip=True, n=64, tracker=None):
    """fn: numpy function of x in 0..1 (use PD.CURVES[name][1]). Returns VGroup with .axes, .curve, .dot, .drop, .tiles, .tracker (ValueTracker of x),
    .pt(xv) -> point on the curve, .x0/.x1/.ystrip (strip geometry). Animate with g.tracker.animate.set_value(v); dot and drop follow by updaters."""
    h = size
    x0, y0 = x - size / 2, y - h / 2
    axes = VGroup(Line([x0, y0, 0], [x0 + size, y0, 0], color=INK, stroke_width=5), Line([x0, y0, 0], [x0, y0 + h, 0], color=INK, stroke_width=5))
    lo, hi = y_range

    def pt(xv):
        return np.array([x0 + xv * size, y0 + (float(fn(np.array([xv]))[0]) - lo) / (hi - lo) * h, 0.0])
    xs = np.linspace(0, 1, 120)
    curve = VMobject(stroke_color=DIM, stroke_width=7).set_points_smoothly([pt(v) for v in xs]) if False else VMobject(stroke_color="#6B6760", stroke_width=7)
    curve.set_points_as_corners([pt(v) for v in xs])
    tr = tracker or ValueTracker(0.0)
    dot = Dot(pt(0.0), radius=0.14, color=TERRA).set_stroke(DIM, width=3)
    dot.add_updater(lambda m: m.move_to(pt(tr.get_value())))
    ystrip = y0 - 0.95
    drop = DashedLine(pt(0.0), [x0, ystrip + 0.25, 0], color=DIM, stroke_width=3, dash_length=0.1)
    drop.add_updater(lambda m: m.become(DashedLine(pt(tr.get_value()), [x0 + tr.get_value() * size, ystrip + 0.25, 0], color=DIM, stroke_width=3, dash_length=0.1)))
    tiles = VGroup()
    if strip:
        pitch = size / n
        for i in range(n):
            v = i / (n - 1)
            g = int(round(255 * v))
            tiles.add(Rectangle(width=pitch * 0.78, height=0.5, fill_color="#%02x%02x%02x" % (g, g, g), fill_opacity=1, stroke_width=0).move_to([x0 + pitch * (i + 0.5), ystrip, 0]))
    l0 = T("0", 32).move_to([x0, y0 - 0.38, 0]); l1 = T("1", 32).move_to([x0 + size, y0 - 0.38, 0])
    lab = VGroup(l0, l1, T("input", 32).move_to([x + 0.0, y0 - 0.38, 0]))
    out = VGroup(axes, curve, tiles, lab)
    out.axes = axes; out.curve = curve; out.dot = dot; out.drop = drop; out.tiles = tiles; out.tracker = tr; out.pt = pt
    out.x0 = x0; out.x1 = x0 + size; out.ystrip = ystrip; out.y0 = y0; out.size = size
    return out


def number_line(x0, x1, y, lo=0.0, hi=1.0, ticks=(0.0, 1.0), color=INK, size=32):
    """A horizontal number line with labelled ticks. Returns VGroup with .at(v) -> scene point."""
    line = Line([x0, y, 0], [x1, y, 0], color=color, stroke_width=5)
    g = VGroup(line)
    at = lambda v: np.array([x0 + (v - lo) / (hi - lo) * (x1 - x0), y, 0.0])
    for t in ticks:
        p = at(t)
        g.add(Line(p + [0, 0.12, 0], p - [0, 0.12, 0], color=color, stroke_width=5), T(("%g" % t), size).move_to(p - [0, 0.45, 0]))
    g.at = at
    return g


def vec_arrow(a, b, color=INK, w=6):
    """An arrow from a to b (scene points) drawn as a shape."""
    return Arrow(np.array(a, dtype=float), np.array(b, dtype=float), buff=0, color=color, stroke_width=w, tip_length=0.22, max_tip_length_to_length_ratio=0.45)


def chip(text, x, y, size=32):
    """A mono function-name chip: outlined rounded box (no fill behind text), Menlo text."""
    t = M(text, size)
    box_ = RoundedRectangle(width=t.width + 0.5, height=t.height + 0.35, corner_radius=0.14, stroke_color=INK, stroke_width=3)
    g = VGroup(box_, t).move_to([x, y, 0])
    g.box = box_; g.label = t
    return g


