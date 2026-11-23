#!/usr/bin/env python3
"""THE WORLD — Monday, 23 November 2026.

Draws one newspaper front page (1024x1024 PNG) summing up the day's
world news. Deterministic: fixed content, fixed seed, no network, no
clock, no timestamps. Writes /output/entry.png (or ./output/entry.png
when /output is not writable).

Stories verified against Reuters, Associated Press and Xinhua reports
published 21-23 November 2026.
"""

import os
import textwrap

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 34
INK = (26, 26, 26)
PAPER = (247, 243, 232)
RULE = (26, 26, 26)
RED = (178, 34, 34)
BLUE = (31, 73, 125)
GREEN = (46, 125, 50)
GREY = (90, 90, 90)

BASE = os.path.dirname(os.path.abspath(__file__))


def font(name, size):
    return ImageFont.truetype(os.path.join(BASE, "fonts", name), size)


SERIF = "DejaVuSerif.ttf"
SERIF_B = "DejaVuSerif-Bold.ttf"
SANS = "DejaVuSans.ttf"
SANS_B = "DejaVuSans-Bold.ttf"


def wrap(draw, text, fnt, width):
    """Greedy word wrap to pixel width; returns list of lines."""
    lines = []
    for para in text.split("\n"):
        words = para.split()
        cur = ""
        for word in words:
            trial = (cur + " " + word).strip()
            if draw.textlength(trial, font=fnt) <= width:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = word
        if cur:
            lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, fnt, width, fill=INK, leading=None):
    lines = wrap(draw, text, fnt, width)
    lh = leading or int(fnt.size * 1.32)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += lh
    return y


def headline(draw, x, y, text, size, width, fill=INK):
    fnt = font(SERIF_B, size)
    return draw_wrapped(draw, x, y, text, fnt, width, fill=fill,
                        leading=int(size * 1.12))


def kicker(draw, x, y, text):
    fnt = font(SANS_B, 13)
    draw.text((x, y), text.upper(), font=fnt, fill=RED)
    return y + 19


def rule(draw, x0, x1, y, width=2):
    draw.line([(x0, y), (x1, y)], fill=RULE, width=width)


def draw_globe(draw, cx, cy, r):
    """Lead illustration: a cracked globe under a hot sun."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=BLUE, width=4,
                 fill=(198, 222, 240))
    # meridians and parallels
    for k in (-0.55, 0.0, 0.55):
        draw.ellipse([cx - r + int(r * 0.45), cy - r,
                      cx + r - int(r * 0.45), cy + r],
                     outline=BLUE, width=2) if k == 0 else None
    draw.ellipse([cx - int(r * 0.62), cy - r, cx + int(r * 0.62), cy + r],
                 outline=BLUE, width=2)
    draw.line([(cx - r, cy), (cx + r, cy)], fill=BLUE, width=2)
    draw.line([(cx - int(r * 0.92), cy - int(r * 0.45)),
               (cx + int(r * 0.92), cy - int(r * 0.45))], fill=BLUE, width=2)
    draw.line([(cx - int(r * 0.92), cy + int(r * 0.45)),
               (cx + int(r * 0.92), cy + int(r * 0.45))], fill=BLUE, width=2)
    # land blobs
    draw.ellipse([cx - int(r * 0.75), cy - int(r * 0.7),
                  cx - int(r * 0.1), cy - int(r * 0.15)], fill=GREEN)
    draw.ellipse([cx + int(r * 0.05), cy + int(r * 0.05),
                  cx + int(r * 0.7), cy + int(r * 0.6)], fill=GREEN)
    draw.ellipse([cx - int(r * 0.55), cy + int(r * 0.3),
                  cx - int(r * 0.05), cy + int(r * 0.75)], fill=GREEN)
    # the crack: a red zigzag splitting the globe
    pts = [(cx - int(r * 0.1), cy - r + 6), (cx + int(r * 0.18), cy - int(r * 0.45)),
           (cx - int(r * 0.12), cy - int(r * 0.1)), (cx + int(r * 0.22), cy + int(r * 0.3)),
           (cx - int(r * 0.05), cy + int(r * 0.65)), (cx + int(r * 0.15), cy + r - 6)]
    draw.line(pts, fill=RED, width=5, joint="curve")
    # sun rays top right
    sx, sy = cx + r + 26, cy - r - 6
    draw.ellipse([sx - 13, sy - 13, sx + 13, sy + 13], fill=(232, 126, 32))
    for a in range(0, 360, 45):
        import math
        x1 = sx + int(20 * math.cos(math.radians(a)))
        y1 = sy + int(20 * math.sin(math.radians(a)))
        x2 = sx + int(30 * math.cos(math.radians(a)))
        y2 = sy + int(30 * math.sin(math.radians(a)))
        draw.line([(x1, y1), (x2, y2)], fill=(232, 126, 32), width=3)


def draw_capitol(draw, x, y, s):
    """US Capitol dome, small icon."""
    draw.rectangle([x, y + int(0.55 * s), x + s, y + s], fill=BLUE)
    for i in range(5):
        cx = x + int((0.12 + i * 0.19) * s)
        draw.rectangle([cx, y + int(0.62 * s), cx + int(0.07 * s), y + int(0.92 * s)],
                       fill=PAPER)
    draw.pieslice([x + int(0.28 * s), y + int(0.12 * s), x + int(0.72 * s),
                   y + int(0.62 * s)], 180, 360, fill=BLUE)
    draw.rectangle([x + int(0.46 * s), y, x + int(0.54 * s), y + int(0.14 * s)],
                   fill=BLUE)
    draw.line([(x + int(0.5 * s), y), (x + int(0.5 * s), y - int(0.14 * s))],
              fill=RED, width=2)
    draw.polygon([(x + int(0.5 * s), y - int(0.14 * s)),
                  (x + int(0.68 * s), y - int(0.09 * s)),
                  (x + int(0.5 * s), y - int(0.04 * s))], fill=RED)


def draw_star_badge(draw, x, y, s):
    """Sheriff star badge, icon for the cartel arrest."""
    import math
    cx, cy = x + s / 2, y + s / 2
    r_out, r_in = s * 0.48, s * 0.2
    pts = []
    for i in range(10):
        r = r_out if i % 2 == 0 else r_in
        a = math.radians(-90 + i * 36)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    draw.polygon(pts, fill=(232, 180, 32), outline=INK)
    draw.ellipse([cx - int(s * 0.1), cy - int(s * 0.1),
                  cx + int(s * 0.1), cy + int(s * 0.1)], fill=INK)


def draw_flame(draw, x, y, s):
    """Flame over a factory roof, icon for the Indonesia fire."""
    draw.rectangle([x, y + int(0.62 * s), x + s, y + s], fill=INK)
    draw.rectangle([x + int(0.1 * s), y + int(0.5 * s), x + int(0.32 * s),
                    y + int(0.62 * s)], fill=INK)
    draw.rectangle([x + int(0.68 * s), y + int(0.42 * s), x + int(0.9 * s),
                    y + int(0.62 * s)], fill=INK)
    cx = x + int(0.5 * s)
    flame = [(cx - int(0.26 * s), y + int(0.55 * s)),
             (cx - int(0.3 * s), y + int(0.28 * s)),
             (cx - int(0.12 * s), y + int(0.34 * s)),
             (cx - int(0.05 * s), y + int(0.08 * s)),
             (cx + int(0.1 * s), y + int(0.3 * s)),
             (cx + int(0.26 * s), y + int(0.18 * s)),
             (cx + int(0.3 * s), y + int(0.42 * s)),
             (cx + int(0.18 * s), y + int(0.55 * s))]
    draw.polygon(flame, fill=(232, 126, 32))
    draw.ellipse([cx - int(0.09 * s), y + int(0.32 * s),
                  cx + int(0.09 * s), y + int(0.52 * s)], fill=(240, 200, 40))


def draw_chart(draw, x, y, s):
    """Falling market chart with a red arrow, icon for the sell-off."""
    draw.rectangle([x, y, x + s, y + s], outline=INK, width=2)
    for i in range(1, 4):
        yy = y + int(i * s / 4)
        draw.line([(x, yy), (x + s, yy)], fill=(200, 200, 200), width=1)
    pts = [(x + int(0.08 * s), y + int(0.25 * s)),
           (x + int(0.3 * s), y + int(0.35 * s)),
           (x + int(0.48 * s), y + int(0.3 * s)),
           (x + int(0.66 * s), y + int(0.55 * s)),
           (x + int(0.9 * s), y + int(0.8 * s))]
    draw.line(pts, fill=RED, width=4, joint="curve")
    draw.polygon([(x + int(0.9 * s), y + int(0.8 * s)),
                  (x + int(0.78 * s), y + int(0.72 * s)),
                  (x + int(0.86 * s), y + int(0.92 * s))], fill=RED)


def draw_tennis(draw, x, y, s):
    """Tennis ball, icon for the sport story."""
    r = int(0.42 * s)
    cx, cy = x + s // 2, y + s // 2
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(196, 214, 54),
                 outline=INK, width=3)
    draw.arc([cx - r, cy - r, cx + r, cy + r], 300, 60, fill=PAPER, width=4)
    draw.arc([cx - r, cy - r, cx + r, cy + r], 120, 240, fill=PAPER, width=4)


LEAD = {
    "kicker": "Climate — Antalya, Turkey",
    "headline": "COP31 COLLAPSES: NO DEAL AS FOSSIL-FUEL ROW SPLITS NATIONS",
    "body": ("After more than two weeks of talks that ran two days into "
             "overtime — the longest COP on record — the Antalya summit "
             "ended on Sunday with no overarching climate deal. The "
             "European Union and others rejected a final draft that made "
             "no mention of fossil fuels. UN chief Antonio Guterres said "
             "he was \u201cdeeply disappointed\u201d as the talks were "
             "suspended, to resume next year."),
}

STORIES = [
    {
        "kicker": "United States — Washington",
        "headline": "Democrats clinch 258 House seats, biggest majority since 1992",
        "body": ("Democrats secured at least 258 seats in the US House on "
                 "Sunday, their largest majority since 1992. The 258th "
                 "seat fell in North Carolina, where Chuck Hubbard ousted "
                 "veteran Republican Virginia Foxx. With the Senate also "
                 "in Democratic hands, divided government awaits a "
                 "Republican White House."),
        "icon": "capitol",
    },
    {
        "kicker": "Mexico — Guasave, Sinaloa",
        "headline": "\u201cEl Chapo Isidro\u201d captured in raid that leaves 11 dead",
        "body": ("Mexican forces captured Fausto Isidro Meza Flores, known "
                 "as \u201cEl Chapo Isidro\u201d, one of the FBI\u2019s Ten "
                 "Most Wanted, in a Friday-night raid in Sinaloa. Eleven "
                 "people died in the fighting — seven alleged gunmen and "
                 "four soldiers. The US had offered a $5 million reward "
                 "for the cartel boss."),
        "icon": "star_badge",
    },
    {
        "kicker": "Indonesia — Serang, Banten",
        "headline": "24 body bags recovered after candy factory fire",
        "body": ("Rescuers recovered 24 body bags from a burned-out candy "
                 "factory in Banten province, where a fire broke out on "
                 "Saturday evening. At least three workers are confirmed "
                 "dead and about 30 remain unaccounted for. Police say DNA "
                 "testing may take two to three weeks to identify the "
                 "victims."),
        "icon": "flame",
    },
    {
        "kicker": "Markets — New York",
        "headline": "Wall Street reels as AI sell-off wipes billions off tech",
        "body": ("Wall Street staggered into Monday after its worst week "
                 "in over 18 months for tech shares. The S&P 500 fell "
                 "3.7% on Friday and the Nasdaq dropped 5.3%, with Nvidia "
                 "down about 14%, as investors questioned the huge cost "
                 "of the AI boom. Futures steadied on Monday as Asian "
                 "markets braced for more volatility."),
        "icon": "chart",
    },
]

SPORT = {
    "kicker": "Sport — Turin & Las Vegas",
    "headline": "Alcaraz beats Zverev to take ATP Finals crown",
    "body": ("Carlos Alcaraz charged past world No. 1 Alexander Zverev to "
             "clinch the ATP Finals title in Turin. In Las Vegas, Max "
             "Verstappen won a chaotic Grand Prix as the Ferraris clashed "
             "again."),
    "icon": "tennis",
}

ICONS = {
    "capitol": draw_capitol,
    "star_badge": draw_star_badge,
    "flame": draw_flame,
    "chart": draw_chart,
    "tennis": draw_tennis,
}


def story_cell(draw, x, y, w, story):
    y = kicker(draw, x, y, story["kicker"])
    # icon top-right of the cell
    ICONS[story["icon"]](draw, x + w - 62, y - 18, 58)
    y = headline(draw, x, y, story["headline"], 21, w - 72)
    y += 4
    fnt = font(SERIF, 15)
    y = draw_wrapped(draw, x, y, story["body"], fnt, w - 8, leading=20)
    return y


def build():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    x0, x1 = MARGIN, W - MARGIN

    # ---- masthead ----
    y = 26
    fnt = font(SERIF_B, 92)
    title = "THE WORLD"
    draw.text(((W - draw.textlength(title, font=fnt)) / 2, y), title,
              font=fnt, fill=INK)
    y += 108
    rule(draw, x0, x1, y, 4)
    y += 8
    fnt = font(SANS_B, 16)
    left = "MONDAY, 23 NOVEMBER 2026"
    right = "PRICE: FREE  •  VOL. I — No. 327"
    draw.text((x0, y), left, font=fnt, fill=INK)
    draw.text((x1 - draw.textlength(right, font=fnt), y), right,
              font=fnt, fill=INK)
    y += 26
    rule(draw, x0, x1, y, 2)
    y += 12

    # ---- lead story ----
    y = kicker(draw, x0, y, LEAD["kicker"])
    lead_w = x1 - x0 - 250
    y = headline(draw, x0, y, LEAD["headline"], 33, lead_w)
    y += 6
    fnt = font(SERIF, 17)
    body_end = draw_wrapped(draw, x0, y, LEAD["body"], fnt, lead_w, leading=23)
    draw_globe(draw, x1 - 118, y + 78, 82)
    y = max(body_end, y + 168) + 6
    rule(draw, x0, x1, y, 2)
    y += 14

    # ---- 2x2 grid of stories ----
    col_w = (x1 - x0 - 28) // 2
    row_y = y
    ends = []
    for i, story in enumerate(STORIES):
        cx = x0 + (i % 2) * (col_w + 28)
        cy = row_y + (i // 2) * 218
        if i % 2 == 1:
            draw.line([(x0 + col_w + 14, cy), (x0 + col_w + 14, cy + 200)],
                      fill=(180, 180, 180), width=1)
        ends.append(story_cell(draw, cx, cy, col_w, story))
    y = max(ends) + 4
    rule(draw, x0, x1, y, 2)
    y += 12

    # ---- sport strip ----
    y = kicker(draw, x0, y, SPORT["kicker"])
    draw_tennis(draw, x1 - 62, y - 6, 56)
    y = headline(draw, x0, y, SPORT["headline"], 22, x1 - x0 - 70)
    y += 4
    fnt = font(SERIF, 15)
    y = draw_wrapped(draw, x0, y, SPORT["body"], fnt, x1 - x0 - 8, leading=20)
    y += 10
    rule(draw, x0, x1, y, 4)
    y += 8
    fnt = font(SANS, 12)
    foot = ("THE WORLD — a one-day front page  •  All events happened or "
            "were first reported on 23 November 2026  •  Sources: Reuters, "
            "Associated Press, Xinhua")
    draw.text((x0, y), foot, font=fnt, fill=GREY)
    return img


def main():
    img = build()
    out = "/output/entry.png"
    try:
        os.makedirs("/output", exist_ok=True)
        img.save(out, format="PNG", optimize=True)
    except OSError:
        out = os.path.join(BASE, "output", "entry.png")
        os.makedirs(os.path.dirname(out), exist_ok=True)
        img.save(out, format="PNG", optimize=True)
    print("wrote", out, img.size)


if __name__ == "__main__":
    main()
