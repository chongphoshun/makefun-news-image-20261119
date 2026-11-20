#!/usr/bin/env python3
"""Render the rev4 front page for make.fun news-image-20261119.

Thursday 19 November 2026, summed up in one 1024x1024 image:
34 stories that were checked against same-day reporting — 3 big
illustrated heroes, 12 illustrated grid cards, a numbered world map,
and 19 briefs. Every story wears a REPORTED / CLAIM / FORECAST badge.

Rev4 is a readability rebuild of rev3 (47 stories, rank #2140).
Rev3 crammed 32 briefs into 13 px type on 13 px rows; at 1024 px
wide almost nobody could read them. Rev4 cuts the 13 weakest
briefs, sets the remaining 19 in 15 px type on 28 px rows with
room to wrap, and names in the footer the big 18-Nov stories that
were left out on purpose. The heroes, the grid and the map are
shorter than in rev3 so the taller brief rows still fit the page.

Palette is cream paper with vermilion rules, the same look as the
earlier entries. Drawing is PIL only, deterministic, no network,
no clock, no randomness.

Run:  python3 draw_rev4.py   (writes entry.png beside this file)
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

PAGE_W, PAGE_H = 1024, 1024
HERE = os.path.dirname(os.path.abspath(__file__))

CREAM = (246, 239, 224)
CARD = (255, 253, 246)
INK = (25, 25, 25)
FAINT = (60, 60, 60)
RED = (180, 35, 24)
RED_DARK = (143, 29, 19)
NAVY = (27, 42, 74)
GOLD = (196, 122, 18)
GREEN = (30, 122, 52)
AMBER = (183, 121, 31)
BLUE = (29, 78, 216)
SLATE = (71, 85, 105)
TEAL = (14, 116, 144)
PURPLE = (107, 33, 168)
LAND = (217, 201, 163)
SEA = (221, 234, 242)
CARD_EDGE = (190, 180, 160)

REGION_FILL = {
    "ASIA": RED, "MIDDLE EAST": GOLD, "EUROPE": BLUE, "AFRICA": GREEN,
    "AMERICAS": PURPLE, "OCEANIA": TEAL, "GLOBAL": SLATE,
}
# Rev4 region tally, 34 stories in all.
REGION_TALLY = [("ASIA", 9), ("MIDDLE EAST", 3), ("EUROPE", 6),
                ("AFRICA", 4), ("AMERICAS", 8), ("OCEANIA", 2),
                ("GLOBAL", 2)]
BADGE_FILL = {"REPORTED": GREEN, "CLAIM": AMBER, "FORECAST": BLUE}


def load_font(kind, size):
    """Pick a DejaVu / Liberation face, falling back to plain sans."""
    paths = {
        "serif_b": "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
        "serif": "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
        "serif_i": "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf",
        "sans_b": "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "sans": "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    }
    try:
        return ImageFont.truetype(paths[kind], size)
    except OSError:
        return ImageFont.truetype(paths["sans"], size)


def wrap_text(d, text, f, max_width):
    """Greedy wrap by pixel width."""
    lines, current = [], ""
    for word in text.split():
        trial = (current + " " + word).strip()
        if d.textlength(trial, font=f) <= max_width or not current:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def pill(d, x, y, label, from_right=False):
    """A small rounded badge pill. Returns its left edge."""
    f = load_font("sans_b", 11)
    w = int(d.textlength(label, font=f)) + 12
    x0 = x - w if from_right else x
    d.rounded_rectangle([x0, y, x0 + w, y + 16], radius=8,
                        fill=BADGE_FILL[label])
    d.text((x0 + 6, y + 3), label, font=f, fill=(255, 255, 255))
    return x0


# ------------------------------------------------------------------ data
# Heroes: (number, caption, headline, why-it-matters, badge)
HEROES = [
    (1, "APEC 2026 · SHENZHEN",
     "Trump, Xi and Putin hold first three-way summit",
     "First three-way summit of the nuclear powers.", "REPORTED"),
    (5, "THE HAGUE · JUSTICE",
     "World Court: Myanmar committed genocide",
     "First state ever found guilty of genocide.", "REPORTED"),
    (12, "ANTALYA · CLIMATE",
     "COP31 draft drops fossil fuels and $120bn aid goal",
     "Draft drops the fossil-fuel phase-out vow.", "REPORTED"),
]

# Grid: (num, place, beat, headline, dek, badge, icon, big text, bg)
GRID = [
    (2, "WORLDWIDE", "GAMES", "GTA VI goes on sale after 13 years",
     "Ties the all-time Metacritic record at 99.", "REPORTED",
     "gamepad", "99", (42, 26, 74)),
    (3, "NEW YORK", "MARKETS", "Anthropic starts trading on Nasdaq",
     "Its record $81.3bn sale was priced at $83.", "REPORTED",
     "chart", "$83", (18, 59, 42)),
    (4, "GREENLAND", "SECURITY", "Denmark backs Arctic pact with US",
     "Parliament approves the Greenland security deal 109–0.", "REPORTED",
     "pact", "109–0", (27, 42, 74)),
    (6, "SEOUL", "JUSTICE", "Korea's top court voids ex-PM Han's term",
     "15-year sentence overturned; case sent back for retrial.", "REPORTED",
     "gavel", "RETRIAL", (55, 65, 81)),
    (7, "GULF", "SHIPPING", "Tanker hit in Hormuz; 1 missing, 11 hurt",
     "Navig8 Messi struck off Oman; second in 4 months.", "REPORTED",
     "ship", "1 MISSING", (31, 58, 74)),
    (8, "GAZA", "CONFLICT", "Israel crosses Gaza's Yellow Line",
     "First ground op since Oct 2025 ceasefire; 3 killed.", "REPORTED",
     "line", "3 KILLED", (138, 109, 59)),
    (9, "CRIMEA", "WAR", "Ukraine hits Crimea bridge again",
     "Third strike in a week halts trains to Russia.", "CLAIM",
     "bridge", "3RD STRIKE", (55, 65, 81)),
    (10, "CANBERRA", "ECONOMY", "Australia's jobless rate hits 4.9%",
     "Highest since 2021; 753,700 out of work.", "REPORTED",
     "chart", "4.9%", (14, 116, 144)),
    (11, "CHINA", "DIPLOMACY", "Takaichi meets Putin at APEC",
     "Her only bilateral at APEC: a 30-minute exchange.", "REPORTED",
     "talks", "APEC", (27, 42, 74)),
    (13, "SPACE", "SCIENCE", "Voyager 1 reaches one light-day",
     "16.1bn miles out; radio now takes 24 hours.", "REPORTED",
     "space", "24 HRS", (15, 23, 42)),
    (14, "NEW YORK", "ART", "Van Gogh sells for record $190.4m",
     "Blossoming Chestnut Trees tops artist's record.", "REPORTED",
     "flower", "$190.4m", (180, 83, 9)),
    (15, "ODISHA", "STORM", "Cyclone Akvan nears India's coast",
     "Landfall expected Friday; 50,000 evacuated.", "FORECAST",
     "cyclone", "50,000", (21, 94, 117)),
]

# Briefs 16-34, in print order. The last three are the new rev4
# stories, all verified against 19-Nov reporting: Jepchirchir's
# EPO ban (Reuters / ESPN), Colombia's national strike
# (TravelersToday, citing Semana / El Tiempo), and Korea passing
# $1 trillion in exports (Reuters).
BRIEFS = [
    (16, "Houthi missiles threaten Riyadh", "CLAIM"),
    (17, "India–Japan 2+2 talks in Tokyo", "REPORTED"),
    (18, "Florida floods close schools", "REPORTED"),
    (19, "Peltola wins Alaska Senate 56–44", "REPORTED"),
    (20, "Judge: ICE mocked court orders", "REPORTED"),
    (21, "UK inflation rises to 3.6%", "REPORTED"),
    (22, "Fiji declares disaster in drought", "REPORTED"),
    (23, "US loses measles-free status", "REPORTED"),
    (24, "Sudan court condemns Hemedti", "REPORTED"),
    (25, "S. Africa holds rates at 7.25%", "REPORTED"),
    (26, "Mongolia's president quits", "REPORTED"),
    (27, "Somalia orders UAE envoy out", "REPORTED"),
    (28, "Dutch embassy in Kyiv hit", "REPORTED"),
    (29, "Lula nears finance minister pick", "CLAIM"),
    (30, "IAEA: N. Korea expands enrichment", "CLAIM"),
    (31, "UN: 372-plus killed in Ukraine, Oct", "REPORTED"),
    (32, "Marathon champ banned 3 yrs for EPO", "REPORTED"),
    (33, "Colombia strike blocks Bogotá airport roads", "REPORTED"),
    (34, "Korea exports pass $1 trillion", "REPORTED"),
]

STATS = [
    ("3", "presidents at one table"),
    ("9–6", "ICJ genocide vote"),
    ("$81.3bn", "Anthropic IPO raise"),
    ("$120bn", "COP31 adaptation aid goal"),
    ("109–0", "Denmark Arctic vote"),
    ("4.9%", "Australian jobless rate"),
]

# Map markers: (num, lon, lat, callout dx, callout dy). The dot sits
# on the true spot; the numbered circle is offset with a leader
# line, so crowded places never overlap.
MARKERS = [
    (1, 114.1, 22.5, 22, -30),
    (3, -74.0, 40.7, 18, -34),
    (4, -51.7, 64.2, -36, 20),
    (5, 4.3, 52.1, -36, 6),
    (6, 127.0, 37.5, 28, 8),
    (7, 56.2, 26.2, 28, 30),
    (8, 34.5, 31.5, -32, 14),
    (9, 36.4, 45.3, 30, 2),
    (10, 149.1, -35.3, -30, -22),
    (11, 114.1, 22.5, -34, -8),
    (12, 30.7, 36.9, 24, 28),
    (14, -74.0, 40.7, -34, -28),
    (15, 86.5, 20.0, 30, 6),
]
GREY_DOTS = [(-150, 64), (-48, -16), (105, 47), (46, 5),
             (178, -18), (77, 28)]

# Rough continent outlines in (lon, lat); stylised, drawn in code.
CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80), (-85, 80),
     (-80, 73), (-70, 62), (-55, 52), (-60, 47), (-65, 44), (-70, 42),
     (-75, 35), (-80, 32), (-81, 26), (-84, 30), (-90, 21), (-97, 26),
     (-105, 20), (-110, 23), (-117, 33), (-125, 40), (-125, 49),
     (-135, 58), (-150, 61), (-165, 60)],
    [(-58, 64), (-45, 60), (-40, 70), (-55, 76), (-65, 76), (-60, 70)],
    [(-80, 10), (-75, 10), (-70, 12), (-62, 10), (-52, 5), (-50, 0),
     (-44, -3), (-35, -8), (-40, -20), (-48, -28), (-55, -35), (-62, -41),
     (-68, -50), (-70, -54), (-73, -44), (-73, -30), (-77, -15), (-80, -5)],
    [(-17, 15), (-10, 30), (0, 36), (10, 37), (20, 32), (30, 31),
     (35, 28), (40, 15), (43, 11), (48, 11), (51, 10), (46, 0),
     (40, -10), (35, -20), (32, -28), (26, -34), (20, -35), (15, -27),
     (12, -18), (9, -2), (9, 4), (-8, 5), (-13, 8), (-17, 12)],
    [(-10, 36), (-9, 43), (-2, 48), (-5, 50), (0, 51), (5, 53), (8, 57),
     (10, 59), (18, 56), (21, 55), (24, 58), (28, 60), (30, 62), (35, 66),
     (40, 68), (55, 70), (70, 72), (90, 75), (110, 74), (130, 72),
     (150, 70), (170, 66), (178, 65), (170, 60), (162, 56), (158, 52),
     (150, 59), (142, 55), (140, 50), (135, 43), (130, 42), (127, 40),
     (122, 38), (120, 32), (115, 23), (110, 20), (105, 10), (100, 8),
     (98, 12), (95, 16), (92, 21), (90, 22), (86, 20), (82, 17),
     (80, 13), (77, 8), (75, 12), (72, 20), (68, 23), (62, 25),
     (58, 26), (55, 26), (52, 28), (50, 29), (48, 30), (44, 29),
     (40, 31), (36, 36), (30, 36), (26, 38), (22, 37), (18, 40),
     (12, 44), (8, 44), (3, 43), (-2, 37), (-6, 36)],
    [(113, -22), (114, -30), (115, -35), (124, -33), (130, -32),
     (136, -35), (140, -38), (145, -38), (150, -37), (153, -27),
     (150, -22), (146, -19), (142, -11), (136, -12), (132, -12),
     (126, -14), (122, -17), (118, -20)],
]


# ------------------------------------------------------------------ icons
def draw_icon(d, kind, x, y, w, h, big, bg, badge):
    """The coloured strip at the top of a grid card: a flat vector
    icon on the left, the big figure in the middle, a badge pill
    on the right. Strip height here is 24 px."""
    d.rectangle([x, y, x + w, y + h], fill=bg)
    pill_w = 0
    if badge:
        bf = load_font("sans_b", 10)
        pill_w = int(d.textlength(badge, font=bf)) + 12
        d.rounded_rectangle([x + w - 5 - pill_w, y + 4,
                             x + w - 5, y + 19], radius=7,
                            fill=BADGE_FILL[badge])
        d.text((x + w - 5 - pill_w + 6, y + 6), badge, font=bf,
               fill=(255, 255, 255))
    cx, cy = x + 32, y + h // 2
    paper = (255, 253, 246)
    if kind == "gamepad":
        d.rounded_rectangle([cx - 19, cy - 7, cx + 19, cy + 8],
                            radius=6, fill=paper)
        d.ellipse([cx - 13, cy - 2, cx - 8, cy + 3], fill=bg)
        d.ellipse([cx + 8, cy - 2, cx + 13, cy + 3], fill=RED)
        d.line([cx + 2, cy - 4, cx + 2, cy + 4], fill=bg, width=2)
        d.line([cx - 2, cy, cx + 6, cy], fill=bg, width=2)
    elif kind == "chart":
        pts = [(cx - 21, cy + 7), (cx - 11, cy + 2), (cx, cy + 4),
               (cx + 11, cy - 3), (cx + 21, cy - 9)]
        d.line(pts, fill=(120, 220, 140), width=3)
        d.polygon([(cx + 21, cy - 9), (cx + 15, cy - 9),
                   (cx + 21, cy - 3)], fill=RED)
        for px, py in pts:
            d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=paper)
    elif kind == "pact":
        # Denmark on the left, the US on the right, side by side.
        d.rectangle([cx - 23, cy - 9, cx - 3, cy + 9], fill=(200, 16, 46))
        d.rectangle([cx - 15, cy - 9, cx - 11, cy + 9], fill=paper)
        d.rectangle([cx - 23, cy - 2, cx - 3, cy + 1], fill=paper)
        for i in range(5):
            d.rectangle([cx + 3, cy - 9 + i * 4, cx + 23,
                         cy - 6 + i * 4],
                        fill=RED if i % 2 == 0 else paper)
        d.rectangle([cx + 3, cy - 9, cx + 11, cy - 2], fill=NAVY)
    elif kind == "gavel":
        d.line([cx - 15, cy + 10, cx + 10, cy - 8], fill=paper, width=3)
        d.polygon([(cx + 2, cy - 13), (cx + 17, cy - 5),
                   (cx + 12, cy + 2), (cx - 3, cy - 5)],
                  fill=(220, 180, 90))
        d.rectangle([cx - 19, cy + 10, cx + 19, cy + 13], fill=paper)
    elif kind == "ship":
        d.polygon([(cx - 21, cy + 2), (cx + 21, cy + 2), (cx + 15, cy + 10),
                   (cx - 15, cy + 10)], fill=(200, 60, 50))
        d.rectangle([cx - 13, cy - 7, cx - 4, cy + 2], fill=paper)
        d.rectangle([cx - 2, cy - 7, cx + 7, cy + 2], fill=(255, 200, 60))
        d.rectangle([cx + 9, cy - 7, cx + 17, cy + 2], fill=paper)
        d.line([cx - 23, cy + 12, cx + 23, cy + 12], fill=paper, width=2)
    elif kind == "line":
        d.line([cx - 21, cy + 3, cx + 21, cy - 3], fill=(255, 220, 0),
               width=4)
        d.polygon([(cx, cy - 11), (cx - 6, cy + 2), (cx + 6, cy + 2)],
                  fill=paper)
    elif kind == "bridge":
        d.line([cx - 23, cy + 5, cx + 23, cy + 5], fill=paper, width=3)
        d.arc([cx - 17, cy - 11, cx + 17, cy + 7], 180, 360,
              fill=paper, width=2)
        d.line([cx - 17, cy + 5, cx - 17, cy - 7], fill=paper, width=2)
        d.line([cx + 17, cy + 5, cx + 17, cy - 7], fill=paper, width=2)
        for sx, sy in [(cx, cy - 12), (cx - 4, cy - 9), (cx + 4, cy - 9)]:
            d.line([sx - 3, sy, sx + 3, sy], fill=(255, 200, 60), width=2)
            d.line([sx, sy - 3, sx, sy + 3], fill=(255, 200, 60), width=2)
    elif kind == "talks":
        # Japan's flag above, Russia's below, two heads underneath.
        d.rectangle([cx - 23, cy - 12, cx - 4, cy - 4], fill=paper)
        d.ellipse([cx - 18, cy - 10, cx - 10, cy - 5], fill=(188, 0, 45))
        for i, col in enumerate([(255, 255, 255), (0, 57, 166),
                                 (213, 0, 50)]):
            d.rectangle([cx + 4, cy - 12 + i * 3, cx + 23,
                         cy - 9 + i * 3], fill=col)
        d.ellipse([cx - 18, cy - 1, cx - 11, cy + 6], fill=(232, 190, 150))
        d.ellipse([cx + 11, cy - 1, cx + 18, cy + 6], fill=(232, 190, 150))
        d.rectangle([cx - 20, cy + 7, cx - 9, cy + 12], fill=NAVY)
        d.rectangle([cx + 9, cy + 7, cx + 20, cy + 12], fill=(90, 30, 30))
    elif kind == "space":
        for sx, sy in [(cx - 19, cy - 9), (cx - 8, cy + 7), (cx + 14, cy - 11),
                       (cx + 19, cy + 5)]:
            d.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=paper)
        d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=paper)
        d.line([cx + 4, cy - 4, cx + 15, cy - 13], fill=paper, width=2)
        d.line([cx - 4, cy + 4, cx - 13, cy + 12], fill=paper, width=2)
    elif kind == "flower":
        for a in range(0, 360, 45):
            px = cx + int(11 * math.cos(math.radians(a)))
            py = cy + int(11 * math.sin(math.radians(a)))
            d.ellipse([px - 5, py - 5, px + 5, py + 5],
                      fill=(255, 200, 60))
        d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=(120, 60, 20))
        d.line([cx, cy + 7, cx, cy + 13], fill=GREEN, width=2)
    elif kind == "cyclone":
        for r in (4, 9, 13):
            d.arc([cx - r, cy - r, cx + r, cy + r], 20, 300,
                  fill=paper, width=2)
        d.line([cx + 13, cy - 6, cx + 21, cy - 10], fill=(255, 200, 60),
               width=2)
        d.polygon([(cx + 21, cy - 10), (cx + 15, cy - 11),
                   (cx + 19, cy - 4)], fill=(255, 200, 60))
    if big:
        f = load_font("serif_b", 15 if len(big) > 7 else 17)
        tw = d.textlength(big, font=f)
        right = x + w - 7 - pill_w - (6 if pill_w else 0)
        d.text((right - tw, y + (h - 17) // 2), big, font=f, fill=paper)


def hero_summit(d, x, y, w, h):
    """Three leaders at one table in Shenzhen, flags of the US,
    China and Russia on the wall behind them. Illo height 80."""
    d.rectangle([x, y, x + w, y + h], fill=(220, 233, 242))
    for fx, flag in [(x + 16, "us"), (x + 134, "cn"), (x + 250, "ru")]:
        if flag == "us":
            for i in range(7):
                d.rectangle([fx, y + 6 + i * 3, fx + 52, y + 9 + i * 3],
                            fill=RED if i % 2 == 0 else (255, 255, 255))
            d.rectangle([fx, y + 6, fx + 22, y + 16], fill=NAVY)
        elif flag == "cn":
            d.rectangle([fx, y + 6, fx + 52, y + 28], fill=(222, 41, 16))
            for sx, sy in [(8, 7), (18, 5), (20, 13), (14, 19)]:
                d.ellipse([fx + sx, y + sy, fx + sx + 4, y + sy + 4],
                          fill=(255, 220, 0))
        else:
            for i, c in enumerate([(255, 255, 255), (0, 57, 166),
                                   (213, 0, 50)]):
                d.rectangle([fx, y + 6 + i * 7, fx + 52, y + 13 + i * 7],
                            fill=c)
    d.rectangle([x, y + 52, x + w, y + h], fill=(122, 82, 48))
    d.rectangle([x, y + 52, x + w, y + 55], fill=(90, 60, 34))
    people = [(x + 58, NAVY, RED, (242, 200, 120), "blond"),
              (x + 160, INK, BLUE, (240, 200, 160), "black"),
              (x + 262, NAVY, RED, (235, 205, 180), "grey")]
    for px, suit, tie, skin, hair in people:
        d.ellipse([px - 13, y + 16, px + 13, y + 40], fill=skin)
        hair_fill = {"blond": (240, 210, 110), "black": (20, 20, 20),
                     "grey": (200, 200, 200)}[hair]
        d.pieslice([px - 13, y + 16, px + 13, y + 32], 180, 360,
                   fill=hair_fill)
        d.rectangle([px - 19, y + 40, px + 19, y + 52], fill=suit)
        d.polygon([(px - 4, y + 40), (px + 4, y + 40), (px, y + 52)],
                  fill=tie)
    f = load_font("sans_b", 10)
    for px, name in [(x + 58, "TRUMP"), (x + 160, "XI"), (x + 262, "PUTIN")]:
        tw = d.textlength(name, font=f)
        d.rectangle([px - tw // 2 - 6, y + 56, px + tw // 2 + 6, y + 70],
                    fill=CARD)
        d.text((px - tw // 2, y + 59), name, font=f, fill=INK)


def hero_icj(d, x, y, w, h):
    """The World Court in The Hague, scales of justice, and the
    9-6 verdict in a red box. Illo height 80."""
    d.rectangle([x, y, x + w, y + h], fill=(242, 227, 198))
    d.rectangle([x + 28, y + 38, x + 178, y + 72], fill=(201, 168, 106))
    d.polygon([(x + 24, y + 38), (x + 182, y + 38), (x + 103, y + 20)],
              fill=(180, 140, 80))
    d.pieslice([x + 90, y + 6, x + 116, y + 32], 180, 360,
               fill=(201, 168, 106))
    d.rectangle([x + 101, y + 16, x + 105, y + 22], fill=(201, 168, 106))
    for i in range(5):
        cx = x + 44 + i * 30
        d.rectangle([cx - 5, y + 42, cx + 5, y + 66], fill=CARD)
    d.rectangle([x + 28, y + 66, x + 178, y + 72], fill=(160, 120, 70))
    sx = x + 250
    d.line([sx, y + 24, sx, y + 70], fill=(150, 110, 20), width=3)
    d.line([sx - 28, y + 32, sx + 28, y + 32], fill=(150, 110, 20), width=3)
    for dx in (-28, 28):
        d.line([sx + dx, y + 32, sx + dx - 9, y + 48],
               fill=(150, 110, 20), width=2)
        d.line([sx + dx, y + 32, sx + dx + 9, y + 48],
               fill=(150, 110, 20), width=2)
        d.pieslice([sx + dx - 10, y + 44, sx + dx + 10, y + 56], 0, 180,
                   fill=(184, 134, 11))
    d.ellipse([sx - 4, y + 20, sx + 4, y + 28], fill=(184, 134, 11))
    f = load_font("serif_b", 24)
    d.rounded_rectangle([x + 230, y + 4, x + 306, y + 28], radius=6,
                        fill=RED)
    tw = d.textlength("9–6", font=f)
    d.text((x + 230 + (76 - tw) / 2, y + 5), "9–6", font=f,
           fill=(255, 255, 255))


def hero_cop31(d, x, y, w, h):
    """A globe, a rising thermometer, and the draft paper with the
    fossil-fuel lines struck out. Illo height 80."""
    d.rectangle([x, y, x + w, y + h], fill=(216, 234, 217))
    gx, gy, gr = x + 58, y + 42, 34
    d.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], fill=(46, 127, 194))
    d.ellipse([gx - 22, gy - 24, gx + 2, gy - 5], fill=(80, 170, 90))
    d.ellipse([gx - 5, gy + 3, gx + 24, gy + 24], fill=(80, 170, 90))
    d.ellipse([gx + 7, gy - 28, gx + 26, gy - 13], fill=(80, 170, 90))
    d.arc([gx - gr, gy - gr, gx + gr, gy + gr], 200, 330,
          fill=(255, 255, 255), width=3)
    tx = x + 132
    d.rounded_rectangle([tx, y + 8, tx + 14, y + 62], radius=7,
                        fill=(255, 255, 255), outline=INK, width=2)
    d.ellipse([tx - 5, y + 58, tx + 19, y + 78], fill=(255, 255, 255),
              outline=INK, width=2)
    d.rectangle([tx + 4, y + 26, tx + 10, y + 62], fill=RED)
    d.ellipse([tx - 1, y + 62, tx + 15, y + 76], fill=RED)
    for i in range(3):
        ly = y + 18 + i * 12
        d.line([tx + 14, ly, tx + 20, ly], fill=INK, width=2)
    # Paper sits lower than the badge pill, so the pill (drawn later,
    # top-right) never covers the FOSSIL / FUELS lines.
    px, py = x + 178, y + 20
    d.rectangle([px, py, px + 122, py + 58], fill=CARD,
                outline=INK, width=2)
    f = load_font("sans_b", 12)
    d.text((px + 10, py + 5), "FOSSIL", font=f, fill=INK)
    d.text((px + 10, py + 20), "FUELS", font=f, fill=INK)
    d.line([px + 6, py + 13, px + 76, py + 10], fill=RED, width=4)
    d.line([px + 6, py + 28, px + 70, py + 25], fill=RED, width=4)
    d.rounded_rectangle([px + 16, py + 36, px + 90, py + 54], radius=4,
                        outline=RED, width=3)
    f2 = load_font("sans_b", 17)
    d.text((px + 28, py + 38), "CUT", font=f2, fill=RED)


# ------------------------------------------------------------------ page
def draw_page():
    img = Image.new("RGB", (PAGE_W, PAGE_H), CREAM)
    d = ImageDraw.Draw(img)
    MX = 18
    CW = PAGE_W - 2 * MX  # 988

    # Eyebrow line above the masthead.
    d.text((MX, 8), "THE WORLD IN ONE DAY", font=load_font("sans_b", 13),
           fill=RED)
    right = "34 STORIES · EVERY CONTINENT · ALL FROM THIS ONE DAY"
    d.text((PAGE_W - MX - d.textlength(right, font=load_font("sans_b", 12)), 9),
           right, font=load_font("sans_b", 12), fill=INK)
    d.line([MX, 26, PAGE_W - MX, 26], fill=INK, width=2)

    # Masthead: 48 pt date, then an italic line naming the 3 heroes.
    d.text((MX, 30), "Thursday 19 November 2026",
           font=load_font("serif_b", 48), fill=INK)
    d.text((MX, 84),
           "Xi, Trump and Putin share one table · The World Court finds "
           "genocide in Myanmar · COP31 drops fossil fuels",
           font=load_font("serif_i", 16), fill=RED)

    # Region bar: seven equal segments, each with its story count.
    ry, rh = 110, 20
    seg = CW / 7
    for i, (name, count) in enumerate(REGION_TALLY):
        x0 = MX + int(i * seg)
        x1 = MX + int((i + 1) * seg) if i < 6 else PAGE_W - MX
        d.rectangle([x0, ry, x1, ry + rh], fill=REGION_FILL[name])
        label = "%s · %d" % (name, count)
        f = load_font("sans_b", 13)
        tw = d.textlength(label, font=f)
        d.text((x0 + (x1 - x0 - tw) / 2, ry + 3), label, font=f,
               fill=(255, 255, 255))

    # Stats strip, between two vermilion rules.
    sy = 136
    d.line([MX, sy, PAGE_W - MX, sy], fill=RED, width=2)
    colw = CW / 6
    for i, (num, label) in enumerate(STATS):
        cx = MX + int(i * colw)
        if i:
            d.line([cx, sy + 6, cx, sy + 46], fill=(200, 190, 170), width=1)
        f = load_font("serif_b", 26)
        tw = d.textlength(num, font=f)
        d.text((cx + (colw - tw) / 2, sy + 5), num, font=f,
               fill=RED if num == "9–6" else NAVY)
        f2 = load_font("sans", 12)
        tw2 = d.textlength(label, font=f2)
        d.text((cx + (colw - tw2) / 2, sy + 35), label, font=f2, fill=INK)
    d.line([MX, sy + 50, PAGE_W - MX, sy + 50], fill=RED, width=2)

    # Heroes, 160 tall: 80 of illustration, an 18 px caption bar,
    # a two-line headline, and a WHY line at the bottom.
    hy, hh, hw, gap = 192, 160, 322, 11
    hero_draw = [hero_summit, hero_icj, hero_cop31]
    for i, (num, caption, headline, why, badge) in enumerate(HEROES):
        x = MX + i * (hw + gap)
        d.rectangle([x, hy, x + hw, hy + hh], fill=CARD,
                    outline=CARD_EDGE, width=1)
        hero_draw[i](d, x + 1, hy + 1, hw - 2, 80)
        d.rectangle([x + 1, hy + 81, x + hw - 1, hy + 99], fill=NAVY)
        d.text((x + 8, hy + 84), caption, font=load_font("sans_b", 12),
               fill=(255, 255, 255))
        # Badge pill on the illustration. Top-left for the ICJ hero,
        # where the red 9-6 box already sits top-right.
        if i == 1:
            pill(d, x + 8, hy + 8, badge)
        else:
            pill(d, x + hw - 8, hy + 8, badge, from_right=True)
        lines = wrap_text(d, headline, load_font("serif_b", 19), hw - 16)
        assert len(lines) <= 2, headline
        yy = hy + 102
        for ln in lines:
            d.text((x + 8, yy), ln, font=load_font("serif_b", 19), fill=INK)
            yy += 21
        d.text((x + 8, hy + 148), "WHY: " + why,
               font=load_font("serif_i", 12), fill=(90, 40, 35))

    # Grid: 12 cards, 4 columns by 3 rows, 100 tall each.
    gy, gh, gw, gx_gap, gy_gap = 360, 100, 241, 8, 7
    for i, (num, place, beat, headline, dek, badge, kind, big, bg) in \
            enumerate(GRID):
        r, c = divmod(i, 4)
        x = MX + c * (gw + gx_gap)
        y = gy + r * (gh + gy_gap)
        d.rectangle([x, y, x + gw, y + gh], fill=CARD,
                    outline=CARD_EDGE, width=1)
        draw_icon(d, kind, x + 1, y + 1, gw - 2, 24, big, bg, badge)
        d.text((x + 8, y + 28), "%d · %s · %s" % (num, place, beat),
               font=load_font("sans_b", 11), fill=RED)
        lines = wrap_text(d, headline, load_font("sans_b", 15), gw - 16)
        assert len(lines) <= 2, headline
        yy = y + 43
        for ln in lines:
            d.text((x + 8, yy), ln, font=load_font("sans_b", 15), fill=INK)
            yy += 16
        dlines = wrap_text(d, dek, load_font("sans", 12), gw - 16)
        assert len(dlines) <= 2, dek
        yy = y + 76
        for ln in dlines:
            d.text((x + 8, yy), ln, font=load_font("sans", 12), fill=FAINT)
            yy += 12

    # ---- bottom band: map on the left, also-list on the right
    by = 682
    d.text((MX, by), "WHERE IT HAPPENED", font=load_font("sans_b", 13),
           fill=RED)
    map_x, map_y, map_w, map_h = MX, by + 20, 296, 176
    d.rounded_rectangle([map_x, map_y, map_x + map_w, map_y + map_h],
                        radius=8, fill=SEA)

    def project(lon, lat):
        px = map_x + 6 + (lon + 168) / 360.0 * (map_w - 12)
        py = map_y + 6 + (74 - lat) / 132.0 * (map_h - 12)
        return px, py

    for poly in CONTINENTS:
        d.polygon([project(lon, lat) for lon, lat in poly],
                  fill=LAND, outline=(191, 168, 122))
    for lon, lat in GREY_DOTS:
        px, py = project(lon, lat)
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(120, 120, 120))
    for num, lon, lat, dx, dy in MARKERS:
        px, py = project(lon, lat)
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=INK)
        cx, cy = px + dx, py + dy
        d.line([px, py, cx, cy], fill=INK, width=1)
        d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=RED,
                  outline=(255, 255, 255), width=1)
        f = load_font("sans_b", 11)
        s = str(num)
        tw = d.textlength(s, font=f)
        d.text((cx - tw / 2, cy - 6), s, font=f, fill=(255, 255, 255))
    d.text((MX, by + 200), "Red numbers mark stories 1–15.",
           font=load_font("sans", 11), fill=FAINT)
    d.text((MX, by + 214), "2 GTA VI — worldwide · 13 Voyager 1 — deep space.",
           font=load_font("sans", 11), fill=FAINT)

    # Also-list: 19 briefs in 15 px type, up to two lines each,
    # one 28 px row per brief. Ten rows left, nine right.
    ax = MX + 304
    d.text((ax, by), "ALSO ON THURSDAY 19 NOVEMBER 2026",
           font=load_font("sans_b", 13), fill=RED)
    lx = PAGE_W - MX
    for label, color in [("REPORTED", GREEN), ("CLAIM", AMBER),
                         ("FORECAST", BLUE)]:
        f = load_font("sans_b", 10)
        tw = d.textlength(label, font=f)
        d.text((lx - tw, by + 2), label, font=f, fill=color)
        d.ellipse([lx - tw - 10, by + 4, lx - tw - 4, by + 10], fill=color)
        lx -= tw + 16
    cols = [(ax, 322), (ax + 338, 346)]
    fnum = load_font("sans_b", 15)
    ftext = load_font("sans", 15)
    fbadge = load_font("sans_b", 10)
    for ci, (colx, colw) in enumerate(cols):
        rows = 10 if ci == 0 else 9
        for ri in range(rows):
            num, headline, badge = BRIEFS[ci * 10 + ri]
            yy = by + 18 + ri * 28
            d.text((colx, yy), str(num), font=fnum, fill=RED)
            bw = d.textlength(badge, font=fbadge)
            d.text((colx + colw - bw, yy + 2), badge, font=fbadge,
                   fill=BADGE_FILL[badge])
            avail = colw - 28 - bw - 8
            lines = wrap_text(d, headline, ftext, avail)
            assert len(lines) <= 2, headline
            for li, ln in enumerate(lines):
                d.text((colx + 28, yy + li * 13), ln, font=ftext, fill=INK)

    # Footer: a vermilion rule, then DATE CHECK, then LEFT OUT.
    d.line([MX, 988, PAGE_W - MX, 988], fill=RED, width=2)
    footer = ("DATE CHECK ✓  All 34 stories checked against same-day "
              "reporting, 19 Nov 2026 · Sources: Reuters, AP, BBC, NASA, "
              "UN News · Claims attributed")
    assert d.textlength(footer, font=load_font("sans", 12)) <= CW, "footer long"
    d.text((MX, 992), footer, font=load_font("sans", 12), fill=INK)
    leftout = ("LEFT OUT AS OTHER DAYS' NEWS: EU €45bn Ukraine loan "
               "(18 Nov) · Jeffries Speaker vote 251–11 (18 Nov) · Iran "
               "strikes on Kuwait/Bahrain (18 Nov) · Fed minutes (18 Nov)")
    assert d.textlength(leftout, font=load_font("sans", 11)) <= CW, "leftout long"
    d.text((MX, 1006), leftout, font=load_font("sans", 11), fill=INK)
    return img


def main():
    img = draw_page()
    assert img.size == (1024, 1024)
    out = os.path.join(HERE, "entry.png")
    img.save(out, optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
