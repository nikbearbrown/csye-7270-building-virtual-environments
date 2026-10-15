#!/usr/bin/env python3
"""Writes greybox 16:9 storyboard panels (1920x1080 SVG). Pre-generation: shapes only, no generated art."""
from pathlib import Path

OUT = Path(__file__).resolve().parent
W, H = 1920, 1080
INK, FOG, MIST, GOLD, CREAM, RED = "#14121C", "#3B4A6B", "#C7D0E0", "#F2B84B", "#FFF1C9", "#B5523B"

def courier(x, y, s=1.0, pose="idle"):
    arm = {"cheer": f'<line x1="{x+8*s}" y1="{y-10*s}" x2="{x+26*s}" y2="{y-40*s}" stroke="{INK}" stroke-width="{5*s}"/>',
           "cast": f'<line x1="{x+10*s}" y1="{y-6*s}" x2="{x+40*s}" y2="{y-6*s}" stroke="{INK}" stroke-width="{5*s}"/>'}.get(pose, "")
    tilt = ' transform="rotate(80 %d %d)"' % (x, y) if pose == "down" else ""
    return (f'<g{tilt}><rect x="{x-14*s}" y="{y-10*s}" width="{28*s}" height="{36*s}" fill="{FOG}" stroke="{INK}" stroke-width="{3*s}"/>'
            f'<rect x="{x-26*s}" y="{y}" width="{12*s}" height="{16*s}" fill="#8A5A3C" stroke="{INK}" stroke-width="{2*s}"/>'
            f'<circle cx="{x}" cy="{y-30*s}" r="{20*s}" fill="{GOLD if pose != "down" else FOG}" stroke="{INK}" stroke-width="{3*s}"/>{arm}</g>')

def moth(x, y, s=1.0):
    return f'<ellipse cx="{x}" cy="{y}" rx="{16*s}" ry="{9*s}" fill="{MIST}" stroke="{INK}" stroke-width="2"/>'

def wraith(x, y, s=1.0):
    return f'<path d="M{x-30*s},{y+30*s} Q{x},{y-60*s} {x+30*s},{y+30*s} Z" fill="{FOG}" stroke="{INK}" stroke-width="3" opacity="0.9"/>'

def arrow(x1, y1, x2, y2, color=INK):
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="8" marker-end="url(#ah)" stroke-dasharray="24 12"/>')

def card(x, y, title):
    return (f'<rect x="{x}" y="{y}" width="380" height="520" rx="18" fill="{CREAM}" stroke="{INK}" stroke-width="6"/>'
            f'<text x="{x+190}" y="{y+80}" font-size="40" text-anchor="middle" fill="{INK}">{title}</text>')

def frame(n, title, shot, angle, move, body):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<defs><marker id="ah" markerWidth="6" markerHeight="6" refX="3" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="{INK}"/></marker></defs>
<rect width="{W}" height="{H}" fill="#1F2540"/>
{body}
<rect x="0" y="0" width="{W}" height="90" fill="{INK}" opacity="0.85"/>
<text x="30" y="60" font-size="44" fill="{CREAM}" font-family="Helvetica">P{n} · {title}</text>
<text x="{W-30}" y="60" font-size="34" fill="{GOLD}" font-family="Helvetica" text-anchor="end">{shot} · {angle} · {move}</text>
<rect x="4" y="4" width="{W-8}" height="{H-8}" fill="none" stroke="{CREAM}" stroke-width="8"/>
</svg>'''

def fog(n=14):
    return "".join(f'<circle cx="{(i*337)%W}" cy="{150+(i*211)%(H-200)}" r="{120+(i*53)%140}" fill="{MIST}" opacity="0.08"/>' for i in range(n))

stalls = "".join(f'<rect x="{x}" y="{y}" width="160" height="110" fill="{RED}" stroke="{INK}" stroke-width="4"/><circle cx="{x+80}" cy="{y-20}" r="18" fill="{GOLD}"/>' for x, y in [(160, 300), (1500, 260), (300, 820), (1380, 780), (900, 200)])

PANELS = [
    ("First look: LANTERNFALL", "Wide", "High angle", "Push-in",
     fog(20) + stalls + courier(960, 620, 1.6) + f'<text x="960" y="420" font-size="120" text-anchor="middle" fill="{GOLD}" font-family="Helvetica">LANTERNFALL</text><text x="960" y="960" font-size="44" text-anchor="middle" fill="{CREAM}">Enter / A to start</text>'
     + '<rect x="300" y="170" width="1320" height="860" fill="none" stroke="#FFF1C9" stroke-width="4" stroke-dasharray="20 14"/>' + arrow(300, 170, 380, 230, CREAM)),
    ("Run begins", "Medium", "Top-down", "Static",
     fog() + courier(960, 560, 2.2) + f'<text x="960" y="160" font-size="56" text-anchor="middle" fill="{CREAM}">0:00</text>' + moth(300, 300) + moth(1650, 850)),
    ("Core action: move, fire, collect", "Medium", "Top-down", "Player motion",
     fog() + courier(760, 560, 2.0, "cast") + arrow(560, 700, 700, 600) + f'<rect x="860" y="540" width="360" height="16" fill="{CREAM}"/>'
     + moth(1300, 548, 1.5) + f'<polygon points="1420,520 1440,548 1420,576 1400,548" fill="{GOLD}"/>' + arrow(1420, 600, 860, 640, GOLD)),
    ("Level up: choose one", "Close-up", "Eye level", "Static",
     f'<rect width="{W}" height="{H}" fill="{INK}" opacity="0.6"/>' + card(260, 300, "Beam: Quick Wick") + card(770, 300, "Moth: Second Wing") + card(1280, 300, "Magnet Satchel")
     + courier(200, 980, 3.0, "cheer")),
    ("Hurt: wraith contact", "Close-up", "Dutch top-down", "Knockback",
     f'<g transform="rotate(-8 960 540)">' + fog() + wraith(1120, 560, 4) + courier(820, 600, 3.2) + arrow(760, 620, 480, 700, RED)
     + f'</g><rect width="{W}" height="{H}" fill="{RED}" opacity="0.18"/>'),
    ("Evolution: Sunflare Lighthouse", "Wide", "High angle", "Zoom-out + ring",
     fog() + "".join(moth(960 + 520 * __import__('math').cos(a / 3), 560 + 360 * __import__('math').sin(a / 3)) for a in range(19))
     + f'<circle cx="960" cy="560" r="330" fill="none" stroke="{GOLD}" stroke-width="18"/>' + courier(960, 600, 1.4, "cheer")
     + f'<text x="960" y="200" font-size="70" text-anchor="middle" fill="{GOLD}">SUNFLARE LIGHTHOUSE</text>' + arrow(700, 300, 560, 220, CREAM)),
    ("Failure: the lamp goes out", "Close-up", "Top-down", "Static",
     fog() + courier(960, 520, 3.4, "down") + f'<rect x="560" y="760" width="800" height="220" fill="{INK}" opacity="0.85"/><text x="960" y="850" font-size="56" text-anchor="middle" fill="{CREAM}">The lamp went out — 2:14</text><text x="960" y="930" font-size="40" text-anchor="middle" fill="{GOLD}">R / Y to retry</text>'),
    ("Retry: straight back in", "Medium", "Top-down", "Hard cut",
     fog() + courier(960, 560, 2.2) + f'<text x="960" y="160" font-size="56" text-anchor="middle" fill="{CREAM}">0:00</text><text x="120" y="1000" font-size="44" fill="{GOLD}">CUT from P7 &lt; 0.2 s</text>'),
    ("End of run: the fog lifts", "Wide", "Low angle", "Fog pull-back",
     f'<rect width="{W}" height="{H}" fill="#6E7FA3"/>' + courier(960, 900, 5.0, "cheer") + f'<text x="960" y="260" font-size="90" text-anchor="middle" fill="{CREAM}">3:00 — The fog lifts</text>' + arrow(1500, 500, 1800, 300, CREAM)),
]

for i, (title, shot, angle, move, body) in enumerate(PANELS, start=1):
    (OUT / f"panel-{i:02d}.svg").write_text(frame(i, title, shot, angle, move, body))
print(f"wrote {len(PANELS)} panels to {OUT}")
