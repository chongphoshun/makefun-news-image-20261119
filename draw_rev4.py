#!/usr/bin/env python3
"""Draw the rev4 front page for make.fun news-image-20261119.

One image, 1024x1024, summing up the world's news of Thursday
19 November 2026: 34 date-checked stories (3 heroes, 12 grid cards,
19 briefs), every story carrying a REPORTED / CLAIM / FORECAST badge.

What changed against rev3 (47 stories, rank #2140):
- Briefs cut from 32 to 19, and each brief now gets a full 28 px row
  with 15 px type wrapped over two lines, so the list reads instead
  of squinting. The 13 weakest briefs are gone; three verified
  19-Nov stories join as briefs (Jepchirchir's EPO ban, Colombia's
  national strike, Korea passing $1 trillion in exports).
- The footer now names what was left out on purpose: the EU 45bn
  Ukraine loan, the Jeffries Speaker vote and the Iran strikes are
  18-Nov news, and the Fed minutes are too, so they are listed as
  left out rather than silently dropped.
- The stats strip swaps the Odisha evacuation figure for the COP31
  $120bn adaptation-aid goal, matching hero 3.
- Heroes and grid cards are a touch shorter so the briefs band and
  the two-line footer fit without squeezing the type.

Palette: cream paper + vermilion. Layout: masthead, region bar,
stats strip, 3 illustrated heroes, illustrated grid, numbered
world map + also-list, two-line footer.

Deterministic: PIL only, no network, no clock, no randomness.
Run:  python3 draw_rev4.py   (writes entry.png beside this file)
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
HERE = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- palette
CREAM = (246, 239, 224)    # page
PAPER = (255, 253, 246)    # cards
INK = (25, 25, 25)
RED = (180, 35, 24)        # vermilion
NAVY = (27, 42, 74)
GOLD = (196, 122, 18)
GREEN = (30, 122, 52)      # REPORTED
AMBER = (183, 121, 31)     # CLAIM
BLUE = (29, 78, 216)       # FORECAST
SLATE = (71, 85, 105)      # GLOBAL
TEAL = (14, 116, 144)      # OCEANIA
PURPLE = (107, 33, 168)    # AMERICAS
TAN = (217, 201, 163)      # land
SEA = (221, 234, 242)      # map sea
RULE = (180, 35, 24)

REGION_COLORS = {
    "ASIA": RED, "MIDDLE EAST": GOLD, "EUROPE": BLUE, "AFRICA": GREEN,
    "AMERICAS": PURPLE, "OCEANIA": TEAL, "GLOBAL": SLATE,
}
# Story counts per region for the 34 stories in this image.
REGION_COUNTS = [("ASIA", 9), ("MIDDLE EAST", 3), ("EUROPE", 6),
                 ("AFRICA", 4), ("AMERICAS", 8), ("OCEANIA", 2),
                 ("GLOBAL", 2)]
BADGE_FILL = {"REPORTED": GREEN, "CLAIM": AMBER, "FORECAST": BLUE}

# ---------------------------------------------------------------- fonts
def font(name, size):
    paths = {
        "serif_b": "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
        "serif": "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
        "serif_i": "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf",
        "sans_b": "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "sans": "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "sans_i": "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf",
    }
    try:
        return ImageFont.truetype(paths[name], size)
    except OSError:
        return ImageFont.truetype(paths["sans"], size)

def wrap(draw, s, f, maxw):
    """Greedy word wrap by pixel width; returns list of lines."""
    words, lines, cur = s.split(), [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=f) <= maxw or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines

def badge_pill(draw, x, y, label, right=False):
    """Small rounded badge; (x, y) is the top-left unless right=True
    (then x is the right edge). Returns the pill's left edge."""
    f = font("sans_b", 10)
    w = int(draw.textlength(label, font=f)) + 12
    x0 = x - w if right else x
    draw.rounded_rectangle([x0, y, x0 + w, y + 15], radius=7,
                           fill=BADGE_FILL[label])
    draw.text((x0 + 6, y + 2), label, font=f, fill=(255, 255, 255))
    return x0

# ---------------------------------------------------------------- data
# Heroes: (number, place, caption, headline, why, badge)
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

# Grid cards, numeric order: (num, place, beat, headline, dek, badge,
#                               illo kind, illo big text, illo bg)
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

# Briefs 16-34: (num, headline, badge). Nineteen briefs, each set in
# 15 px type over up to two lines in a 28 px row — the whole point of
# rev4 is that this list can actually be read. The last three are the
# new verified 19-Nov stories; the sixteen weakest rev3 briefs
# (Waymo, Pew 2035, LSU debut, Leicester sponsor, BBC probe, Delhi
# schools, US-Venezuela, Canada sanctions, Microsoft-ByteDance,
# Libya seizure, COPD Day, Nvidia-Huang, Musk spending, Carney-Trump,
# Bluenami, US-Philippines loan) were cut to make room.
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

# Map markers: (num, lon, lat, callout dx, callout dy). Dots sit on the
# true spot; the numbered circle is offset with a leader line, so
# crowded places (Washington, New York, Brussels, the Gulf) never
# overlap.
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
# Grey dots for briefs (no number): (lon, lat)
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

# ---------------------------------------------------------------- icons
def illo_icon(draw, kind, x, y, w, h, big, bg, badge):
    """Mini scene strip for a grid card: coloured ground, a simple
    vector icon on the left, the big figure in the middle, the
    credibility badge pill on the right."""
    draw.rectangle([x, y, x + w, y + h], fill=bg)
    pill_w = 0
    if badge:
        bf = font("sans_b", 10)
        pill_w = int(draw.textlength(badge, font=bf)) + 12
        draw.rounded_rectangle([x + w - 5 - pill_w, y + 5,
                                x + w - 5, y + 19], radius=7,
                               fill=BADGE_FILL[badge])
        draw.text((x + w - 5 - pill_w + 6, y + 7), badge, font=bf,
                  fill=(255, 255, 255))
    cx, cy = x + 30, y + h // 2
    cream = (255, 253, 246)
    if kind == "gamepad":
        draw.rounded_rectangle([cx - 18, cy - 7, cx + 18, cy + 8],
                               radius=6, fill=cream)
        draw.ellipse([cx - 12, cy - 2, cx - 7, cy + 3], fill=bg)
        draw.ellipse([cx + 7, cy - 2, cx + 12, cy + 3], fill=(180, 35, 24))
        draw.line([cx + 2, cy - 4, cx + 2, cy + 4], fill=bg, width=2)
        draw.line([cx - 2, cy, cx + 6, cy], fill=bg, width=2)
    elif kind == "chart":
        pts = [(cx - 20, cy + 7), (cx - 10, cy + 2), (cx, cy + 4),
               (cx + 10, cy - 3), (cx + 20, cy - 9)]
        draw.line(pts, fill=(120, 220, 140), width=3)
        draw.polygon([(cx + 20, cy - 9), (cx + 14, cy - 9),
                      (cx + 20, cy - 3)], fill=(180, 35, 24))
        for px, py in pts:
            draw.ellipse([px - 2, py - 2, px + 2, py + 2], fill=cream)
    elif kind == "ship":
        draw.polygon([(cx - 20, cy + 2), (cx + 20, cy + 2), (cx + 14, cy + 10),
                      (cx - 14, cy + 10)], fill=(200, 60, 50))
        draw.rectangle([cx - 13, cy - 7, cx - 4, cy + 2], fill=cream)
        draw.rectangle([cx - 2, cy - 7, cx + 7, cy + 2], fill=(255, 200, 60))
        draw.rectangle([cx + 9, cy - 7, cx + 16, cy + 2], fill=cream)
        draw.line([cx - 22, cy + 12, cx + 22, cy + 12], fill=cream, width=2)
    elif kind == "line":
        draw.line([cx - 20, cy + 3, cx + 20, cy - 3], fill=(255, 220, 0),
                  width=4)
        draw.polygon([(cx, cy - 11), (cx - 5, cy + 2), (cx + 5, cy + 2)],
                     fill=cream)
    elif kind == "bridge":
        draw.line([cx - 22, cy + 5, cx + 22, cy + 5], fill=cream, width=3)
        draw.arc([cx - 16, cy - 11, cx + 16, cy + 7], 180, 360,
                 fill=cream, width=2)
        draw.line([cx - 16, cy + 5, cx - 16, cy - 7], fill=cream, width=2)
        draw.line([cx + 16, cy + 5, cx + 16, cy - 7], fill=cream, width=2)
        for sx, sy in [(cx, cy - 12), (cx - 4, cy - 9), (cx + 4, cy - 9)]:
            draw.line([sx - 3, sy, sx + 3, sy], fill=(255, 200, 60), width=2)
            draw.line([sx, sy - 3, sx, sy + 3], fill=(255, 200, 60), width=2)
    elif kind == "pact":
        # Denmark (red, white cross) + US (stripes, blue canton)
        draw.rectangle([cx - 22, cy - 9, cx - 3, cy + 9],
                       fill=(200, 16, 46))
        draw.rectangle([cx - 14, cy - 9, cx - 10, cy + 9], fill=cream)
        draw.rectangle([cx - 22, cy - 2, cx - 3, cy + 1], fill=cream)
        for i in range(5):
            draw.rectangle([cx + 3, cy - 9 + i * 4, cx + 22,
                            cy - 6 + i * 4],
                           fill=(180, 35, 24) if i % 2 == 0 else cream)
        draw.rectangle([cx + 3, cy - 9, cx + 10, cy - 2],
                       fill=(27, 42, 74))
    elif kind == "gavel":
        draw.line([cx - 14, cy + 10, cx + 9, cy - 8], fill=cream, width=3)
        draw.polygon([(cx + 2, cy - 13), (cx + 16, cy - 5),
                      (cx + 12, cy + 2), (cx - 2, cy - 5)],
                     fill=(220, 180, 90))
        draw.rectangle([cx - 18, cy + 10, cx + 18, cy + 13], fill=cream)
    elif kind == "talks":
        # Japan (white, red disc) + Russia (white/blue/red) + two heads
        draw.rectangle([cx - 22, cy - 12, cx - 4, cy - 4], fill=cream)
        draw.ellipse([cx - 17, cy - 10, cx - 9, cy - 5], fill=(188, 0, 45))
        for i, col in enumerate([(255, 255, 255), (0, 57, 166),
                                 (213, 0, 50)]):
            draw.rectangle([cx + 4, cy - 12 + i * 3, cx + 22,
                            cy - 9 + i * 3], fill=col)
        draw.ellipse([cx - 17, cy - 1, cx - 10, cy + 6], fill=(232, 190, 150))
        draw.ellipse([cx + 10, cy - 1, cx + 17, cy + 6], fill=(232, 190, 150))
        draw.rectangle([cx - 19, cy + 7, cx - 8, cy + 12], fill=(27, 42, 74))
        draw.rectangle([cx + 8, cy + 7, cx + 19, cy + 12], fill=(90, 30, 30))
    elif kind == "space":
        for sx, sy in [(cx - 18, cy - 9), (cx - 7, cy + 7), (cx + 13, cy - 11),
                       (cx + 18, cy + 5)]:
            draw.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=cream)
        draw.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=cream)
        draw.line([cx + 4, cy - 4, cx + 14, cy - 12], fill=cream, width=2)
        draw.line([cx - 4, cy + 4, cx - 12, cy + 11], fill=cream, width=2)
    elif kind == "flower":
        for a in range(0, 360, 45):
            import math
            px = cx + int(10 * math.cos(math.radians(a)))
            py = cy + int(10 * math.sin(math.radians(a)))
            draw.ellipse([px - 4, py - 4, px + 4, py + 4],
                         fill=(255, 200, 60))
        draw.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=(120, 60, 20))
        draw.line([cx, cy + 6, cx, cy + 12], fill=(30, 122, 52), width=2)
    elif kind == "cyclone":
        for r in (4, 8, 12):
            draw.arc([cx - r, cy - r, cx + r, cy + r], 20, 300,
                     fill=cream, width=2)
        draw.line([cx + 12, cy - 5, cx + 20, cy - 9], fill=(255, 200, 60),
                  width=2)
        draw.polygon([(cx + 20, cy - 9), (cx + 14, cy - 10),
                      (cx + 18, cy - 3)], fill=(255, 200, 60))
    if big:
        f = font("serif_b", 15 if len(big) > 7 else 17)
        tw = draw.textlength(big, font=f)
        right = x + w - 7 - pill_w - (6 if pill_w else 0)
        draw.text((right - tw, y + (h - 17) // 2), big, font=f,
                  fill=cream)

def hero_summit(draw, x, y, w, h):
    """Three leaders at one table in Shenzhen; flags of the US, China
    and Russia on the wall behind them. Illustration height is 80."""
    draw.rectangle([x, y, x + w, y + h], fill=(220, 233, 242))
    for fx, flag in [(x + 16, "us"), (x + 134, "cn"), (x + 250, "ru")]:
        if flag == "us":
            for i in range(7):
                draw.rectangle([fx, y + 6 + i * 3, fx + 52, y + 9 + i * 3],
                               fill=(180, 35, 24) if i % 2 == 0 else (255, 255, 255))
            draw.rectangle([fx, y + 6, fx + 22, y + 16], fill=(27, 42, 74))
        elif flag == "cn":
            draw.rectangle([fx, y + 6, fx + 52, y + 28], fill=(222, 41, 16))
            for sx, sy in [(8, 7), (18, 5), (20, 13), (14, 19)]:
                draw.ellipse([fx + sx, y + sy, fx + sx + 4, y + sy + 4],
                             fill=(255, 220, 0))
        else:
            for i, c in enumerate([(255, 255, 255), (0, 57, 166), (213, 0, 50)]):
                draw.rectangle([fx, y + 6 + i * 7, fx + 52, y + 13 + i * 7],
                               fill=c)
    draw.rectangle([x, y + 52, x + w, y + h], fill=(122, 82, 48))
    draw.rectangle([x, y + 52, x + w, y + 55], fill=(90, 60, 34))
    people = [(x + 58, (27, 42, 74), (180, 35, 24), (242, 200, 120), "blond"),
              (x + 160, (25, 25, 25), (29, 78, 216), (240, 200, 160), "black"),
              (x + 262, (27, 42, 74), (180, 35, 24), (235, 205, 180), "grey")]
    for px, suit, tie, skin, hair in people:
        draw.ellipse([px - 13, y + 16, px + 13, y + 40], fill=skin)
        fill = {"blond": (240, 210, 110), "black": (20, 20, 20),
                "grey": (200, 200, 200)}[hair]
        draw.pieslice([px - 13, y + 16, px + 13, y + 32], 180, 360,
                      fill=fill)
        draw.rectangle([px - 19, y + 40, px + 19, y + 52], fill=suit)
        draw.polygon([(px - 4, y + 40), (px + 4, y + 40), (px, y + 52)],
                     fill=tie)
    f = font("sans_b", 10)
    for px, name in [(x + 58, "TRUMP"), (x + 160, "XI"), (x + 262, "PUTIN")]:
        tw = draw.textlength(name, font=f)
        draw.rectangle([px - tw // 2 - 6, y + 56, px + tw // 2 + 6, y + 70],
                       fill=(255, 253, 246))
        draw.text((px - tw // 2, y + 59), name, font=f, fill=INK)

def hero_icj(draw, x, y, w, h):
    """The World Court in The Hague, scales of justice, and the 9-6
    verdict in a red box. Illustration height is 80."""
    draw.rectangle([x, y, x + w, y + h], fill=(242, 227, 198))
    draw.rectangle([x + 28, y + 38, x + 178, y + 72], fill=(201, 168, 106))
    draw.polygon([(x + 24, y + 38), (x + 182, y + 38), (x + 103, y + 20)],
                 fill=(180, 140, 80))
    draw.pieslice([x + 90, y + 6, x + 116, y + 32], 180, 360,
                  fill=(201, 168, 106))
    draw.rectangle([x + 101, y + 16, x + 105, y + 22], fill=(201, 168, 106))
    for i in range(5):
        cx = x + 44 + i * 30
        draw.rectangle([cx - 5, y + 42, cx + 5, y + 66], fill=(255, 253, 246))
    draw.rectangle([x + 28, y + 66, x + 178, y + 72], fill=(160, 120, 70))
    sx = x + 250
    draw.line([sx, y + 24, sx, y + 70], fill=(150, 110, 20), width=3)
    draw.line([sx - 28, y + 32, sx + 28, y + 32], fill=(150, 110, 20), width=3)
    for dx in (-28, 28):
        draw.line([sx + dx, y + 32, sx + dx - 9, y + 48],
                  fill=(150, 110, 20), width=2)
        draw.line([sx + dx, y + 32, sx + dx + 9, y + 48],
                  fill=(150, 110, 20), width=2)
        draw.pieslice([sx + dx - 10, y + 44, sx + dx + 10, y + 56], 0, 180,
                      fill=(184, 134, 11))
    draw.ellipse([sx - 4, y + 20, sx + 4, y + 28], fill=(184, 134, 11))
    f = font("serif_b", 24)
    draw.rounded_rectangle([x + 230, y + 4, x + 306, y + 28], radius=6,
                           fill=RED)
    tw = draw.textlength("9–6", font=f)
    draw.text((x + 230 + (76 - tw) / 2, y + 5), "9–6", font=f,
              fill=(255, 255, 255))

def hero_cop31(draw, x, y, w, h):
    """A globe, a rising thermometer, and the draft paper with the
    fossil-fuel lines struck out. Illustration height is 80."""
    draw.rectangle([x, y, x + w, y + h], fill=(216, 234, 217))
    gx, gy, gr = x + 58, y + 42, 34
    draw.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], fill=(46, 127, 194))
    draw.ellipse([gx - 22, gy - 24, gx + 2, gy - 5], fill=(80, 170, 90))
    draw.ellipse([gx - 5, gy + 3, gx + 24, gy + 24], fill=(80, 170, 90))
    draw.ellipse([gx + 7, gy - 28, gx + 26, gy - 13], fill=(80, 170, 90))
    draw.arc([gx - gr, gy - gr, gx + gr, gy + gr], 200, 330,
             fill=(255, 255, 255), width=3)
    tx = x + 132
    draw.rounded_rectangle([tx, y + 8, tx + 14, y + 62], radius=7,
                           fill=(255, 255, 255), outline=INK, width=2)
    draw.ellipse([tx - 5, y + 58, tx + 19, y + 78], fill=(255, 255, 255),
                 outline=INK, width=2)
    draw.rectangle([tx + 4, y + 26, tx + 10, y + 62], fill=RED)
    draw.ellipse([tx - 1, y + 62, tx + 15, y + 76], fill=RED)
    for i in range(3):
        ly = y + 18 + i * 12
        draw.line([tx + 14, ly, tx + 20, ly], fill=INK, width=2)
    px, py = x + 178, y + 8
    draw.rectangle([px, py, px + 122, py + 66], fill=(255, 253, 246),
                   outline=INK, width=2)
    f = font("sans_b", 12)
    draw.text((px + 10, py + 7), "FOSSIL", font=f, fill=INK)
    draw.text((px + 10, py + 24), "FUELS", font=f, fill=INK)
    draw.line([px + 6, py + 15, px + 76, py + 12], fill=RED, width=4)
    draw.line([px + 6, py + 32, px + 70, py + 29], fill=RED, width=4)
    draw.rounded_rectangle([px + 16, py + 42, px + 90, py + 62], radius=4,
                           outline=RED, width=3)
    f2 = font("sans_b", 17)
    draw.text((px + 28, py + 44), "CUT", font=f2, fill=RED)

# ---------------------------------------------------------------- page
def draw_page():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    MX = 18
    CW = W - 2 * MX  # 988

    # eyebrow
    d.text((MX, 8), "THE WORLD IN ONE DAY", font=font("sans_b", 13), fill=RED)
    right = "34 STORIES · EVERY CONTINENT · ALL FROM THIS ONE DAY"
    d.text((W - MX - d.textlength(right, font=font("sans_b", 12)), 9),
           right, font=font("sans_b", 12), fill=INK)
    d.line([MX, 26, W - MX, 26], fill=INK, width=2)

    # masthead
    d.text((MX, 30), "Thursday 19 November 2026",
           font=font("serif_b", 48), fill=INK)
    d.text((MX, 84),
           "Xi, Trump and Putin share one table · The World Court finds "
           "genocide in Myanmar · COP31 drops fossil fuels",
           font=font("serif_i", 16), fill=RED)

    # region bar: 7 equal segments with story counts
    ry, rh = 110, 20
    seg = CW / 7
    for i, (name, count) in enumerate(REGION_COUNTS):
        x0 = MX + int(i * seg)
        x1 = MX + int((i + 1) * seg) if i < 6 else W - MX
        d.rectangle([x0, ry, x1, ry + rh], fill=REGION_COLORS[name])
        label = "%s · %d" % (name, count)
        f = font("sans_b", 13)
        tw = d.textlength(label, font=f)
        d.text((x0 + (x1 - x0 - tw) / 2, ry + 3), label, font=f,
               fill=(255, 255, 255))

    # stats strip
    sy = 136
    d.line([MX, sy, W - MX, sy], fill=RULE, width=2)
    colw = CW / 6
    for i, (num, label) in enumerate(STATS):
        cx = MX + int(i * colw)
        if i:
            d.line([cx, sy + 6, cx, sy + 46], fill=(200, 190, 170), width=1)
        f = font("serif_b", 26)
        tw = d.textlength(num, font=f)
        d.text((cx + (colw - tw) / 2, sy + 5), num, font=f,
               fill=RED if num in ("9–6",) else NAVY)
        f2 = font("sans", 12)
        tw2 = d.textlength(label, font=f2)
        d.text((cx + (colw - tw2) / 2, sy + 35), label, font=f2, fill=INK)
    d.line([MX, sy + 50, W - MX, sy + 50], fill=RULE, width=2)

    # heroes: shorter than rev3 (160 instead of 196) to fund the
    # briefs band below.
    hy, hh, hw, gap = 192, 160, 322, 11
    hero_draw = [hero_summit, hero_icj, hero_cop31]
    for i, (num, caption, headline, why, badge) in enumerate(HEROES):
        x = MX + i * (hw + gap)
        d.rectangle([x, hy, x + hw, hy + hh], fill=PAPER,
                    outline=(190, 180, 160), width=1)
        hero_draw[i](d, x + 1, hy + 1, hw - 2, 80)
        # caption bar
        d.rectangle([x + 1, hy + 81, x + hw - 1, hy + 99], fill=NAVY)
        d.text((x + 8, hy + 84), caption, font=font("sans_b", 12),
               fill=(255, 255, 255))
        # badge pill on the illustration (top-right; top-left for ICJ,
        # where the 9-6 box already sits top-right)
        if i == 1:
            badge_pill(d, x + 8, hy + 8, badge)
        else:
            badge_pill(d, x + hw - 8, hy + 8, badge, right=True)
        # headline + why it matters
        lines = wrap(d, headline, font("serif_b", 19), hw - 16)
        assert len(lines) <= 2, headline
        yy = hy + 102
        for ln in lines:
            d.text((x + 8, yy), ln, font=font("serif_b", 19), fill=INK)
            yy += 21
        d.text((x + 8, hy + 148), "WHY: " + why, font=font("sans_i", 12),
               fill=(90, 40, 35))

    # grid: 12 cards, 4 columns x 3 rows, 100 tall each
    gy, gh, gw, gx_gap, gy_gap = 360, 100, 241, 8, 7
    for i, (num, place, beat, headline, dek, badge, kind, big, bg) in \
            enumerate(GRID):
        r, c = divmod(i, 4)
        x = MX + c * (gw + gx_gap)
        y = gy + r * (gh + gy_gap)
        d.rectangle([x, y, x + gw, y + gh], fill=PAPER,
                    outline=(190, 180, 160), width=1)
        illo_icon(d, kind, x + 1, y + 1, gw - 2, 24, big, bg, badge)
        # kicker: number, place, beat — badge now lives in the strip
        d.text((x + 8, y + 28), "%d · %s · %s" % (num, place, beat),
               font=font("sans_b", 11), fill=RED)
        # headline, 2 lines max
        lines = wrap(d, headline, font("sans_b", 15), gw - 16)
        assert len(lines) <= 2, headline
        yy = y + 43
        for ln in lines:
            d.text((x + 8, yy), ln, font=font("sans_b", 15), fill=INK)
            yy += 16
        # dek, 2 lines max
        dlines = wrap(d, dek, font("sans", 12), gw - 16)
        assert len(dlines) <= 2, dek
        yy = y + 76
        for ln in dlines:
            d.text((x + 8, yy), ln, font=font("sans", 12), fill=(60, 60, 60))
            yy += 12

    # ---- bottom band: map (left) + also-list (right)
    by = 682
    # map panel
    d.text((MX, by), "WHERE IT HAPPENED", font=font("sans_b", 13), fill=RED)
    map_x, map_y, map_w, map_h = MX, by + 20, 296, 176
    d.rounded_rectangle([map_x, map_y, map_x + map_w, map_y + map_h],
                        radius=8, fill=SEA)
    def project(lon, lat):
        px = map_x + 6 + (lon + 168) / 360.0 * (map_w - 12)
        py = map_y + 6 + (74 - lat) / 132.0 * (map_h - 12)
        return px, py
    for poly in CONTINENTS:
        d.polygon([project(lon, lat) for lon, lat in poly],
                  fill=TAN, outline=(191, 168, 122))
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
        f = font("sans_b", 11)
        s = str(num)
        tw = d.textlength(s, font=f)
        d.text((cx - tw / 2, cy - 6), s, font=f, fill=(255, 255, 255))
    d.text((MX, by + 200), "Red numbers mark stories 1–15.",
           font=font("sans", 11), fill=(60, 60, 60))
    d.text((MX, by + 214), "2 GTA VI — worldwide · 13 Voyager 1 — deep space.",
           font=font("sans", 11), fill=(60, 60, 60))

    # also-list panel: 19 briefs, 15 px type, two lines each, 28 px rows.
    # Ten rows in the left column, nine in the right.
    ax = MX + 304
    d.text((ax, by), "ALSO ON THURSDAY 19 NOVEMBER 2026",
           font=font("sans_b", 13), fill=RED)
    lx = W - MX
    for label, color in [("REPORTED", GREEN), ("CLAIM", AMBER),
                         ("FORECAST", BLUE)]:
        f = font("sans_b", 10)
        tw = d.textlength(label, font=f)
        d.text((lx - tw, by + 2), label, font=f, fill=color)
        d.ellipse([lx - tw - 10, by + 4, lx - tw - 4, by + 10], fill=color)
        lx -= tw + 16
    cols = [(ax, 322), (ax + 338, 346)]
    fnum = font("sans_b", 15)
    ftext = font("sans", 15)
    fbadge = font("sans_b", 10)
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
            lines = wrap(d, headline, ftext, avail)
            assert len(lines) <= 2, headline
            for li, ln in enumerate(lines):
                d.text((colx + 28, yy + li * 13), ln, font=ftext, fill=INK)

    # footer: date check first, then the left-out list.
    d.line([MX, 988, W - MX, 988], fill=RULE, width=2)
    footer = ("DATE CHECK ✓  All 34 stories checked against same-day "
              "reporting, 19 Nov 2026 · Sources: Reuters, AP, BBC, NASA, "
              "UN News · Claims attributed")
    assert d.textlength(footer, font=font("sans", 12)) <= CW, "footer long"
    d.text((MX, 992), footer, font=font("sans", 12), fill=INK)
    leftout = ("LEFT OUT AS OTHER DAYS' NEWS: EU €45bn Ukraine loan "
               "(18 Nov) · Jeffries Speaker vote 251–11 (18 Nov) · Iran "
               "strikes on Kuwait/Bahrain (18 Nov) · Fed minutes (18 Nov)")
    assert d.textlength(leftout, font=font("sans", 11)) <= CW, "leftout long"
    d.text((MX, 1006), leftout, font=font("sans", 11), fill=INK)
    return img

def main():
    img = draw_page()
    assert img.size == (1024, 1024)
    out = os.path.join(HERE, "entry.png")
    img.save(out, optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")

if __name__ == "__main__":
    main()
