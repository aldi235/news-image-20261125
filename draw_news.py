#!/usr/bin/env python3
"""Render 'The World in One Page' — a dense 1024x1024 newspaper front page
summarising the world news of Wednesday 25 November 2026.

Run:  python3 draw_news.py        -> writes entry.png next to this script.
Only the Python standard library plus Pillow is used; fonts are the system
DejaVu faces. Everything on the page is drawn from the story tables below.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = "entry.png"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

PAPER = (250, 246, 238)
INK = (22, 26, 34)
BODY = (52, 56, 64)
NAVY = (18, 33, 62)
RED = (178, 34, 34)
GREY = (96, 100, 108)
CARD = (255, 255, 255)
EDGE = (203, 196, 184)
OCEAN = (172, 206, 224)
LAND = (233, 215, 165)
LEAF = (150, 184, 130)
GREEN = (39, 124, 74)


def fnt(size, bold=False):
    return ImageFont.truetype(BOLD if bold else REG, size)


def wrap_text(draw, text, font, max_w):
    """Greedy word wrap measured with the real font; returns a list of lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


class Sheet:
    """The page plus the small drawing helpers every panel shares."""

    def __init__(self):
        self.img = Image.new("RGB", (W, H), PAPER)
        self.d = ImageDraw.Draw(self.img)

    def text(self, xy, s, size, bold=False, fill=INK):
        self.d.text(xy, s, font=fnt(size, bold), fill=fill)

    def centred(self, y, s, size, bold=False, fill=INK, cx=W // 2):
        w = self.d.textlength(s, font=fnt(size, bold))
        self.d.text((cx - w / 2, y), s, font=fnt(size, bold), fill=fill)

    def para(self, x, y, w, s, size, fill=BODY, leading=None, bold=False):
        """Draw a wrapped paragraph; return the y just below it."""
        font = fnt(size, bold)
        step = leading if leading is not None else size + 3
        for line in wrap_text(self.d, s, font, w):
            self.d.text((x, y), line, font=font, fill=fill)
            y += step
        return y

    def save(self):
        self.img.save(OUT)
        print(f"wrote {OUT} {W}x{H}")


class Column:
    """One vertical stack of region sections: coloured header bars with
    short headline + one-line body stories underneath."""

    def __init__(self, sheet, x, y, w, bottom):
        self.s = sheet
        self.x, self.y, self.w, self.bottom = x, y, w, bottom

    def header(self, title, colour):
        d = self.s.d
        d.rectangle([self.x, self.y, self.x + self.w, self.y + 20], fill=colour)
        d.text((self.x + 8, self.y + 4), title, font=fnt(11, True),
               fill=(255, 255, 255))
        self.y += 23

    def story(self, head, body, tag):
        d = self.s.d
        x, w = self.x + 2, self.w - 4
        for line in wrap_text(d, head, fnt(10, True), w):
            d.text((x, self.y), line, font=fnt(10, True), fill=INK)
            self.y += 12
        lines = wrap_text(d, body, fnt(9), w)
        tag_font = fnt(8, True)
        tag_w = d.textlength(" " + tag, font=tag_font)
        for i, line in enumerate(lines):
            d.text((x, self.y), line, font=fnt(9), fill=BODY)
            self.y += 11
            if i == len(lines) - 1:  # red source tag at the end of the story
                lw = d.textlength(line, font=fnt(9))
                if lw + tag_w <= w:
                    d.text((x + lw, self.y - 11), " " + tag,
                           font=tag_font, fill=RED)
                else:
                    d.text((x, self.y), tag, font=tag_font, fill=RED)
                    self.y += 10
        self.y += 2
        if self.y > self.bottom:
            print(f"WARNING: column overflow past y={self.bottom} "
                  f"(now {self.y})")


# ---------------------------------------------------------------- content
LEADS = [
    ("LEAD 1 — MARKETS",
     "Nvidia rally fizzles as Huang comeback fades",
     "Shares slide ~6% to $155.38 on Tue 25 Nov, a day after a +31.5% surge "
     "added $952bn. WSJ: Huang disclosed more affairs to the board; he "
     "testifies to Congress in early Dec. — NY POST / WSJ"),
    ("LEAD 2 — YEMEN / SAUDI ARABIA",
     "Houthis hit Riyadh's tallest tower — again",
     "The PIF Tower is struck for the 2nd time in under a week; 11 wounded, "
     "incl. 2 Saudis, 2 Indians, 3 Nepalis and 4 Egyptians. Houthis now "
     "~60 km from Aden; the coalition vows a decisive response. — REUTERS"),
    ("LEAD 3 — CLIMATE",
     "COP31 ends with no deal — first failure since 2009",
     "~40 countries rejected a text with no fossil-fuel phase-out. 90 nations "
     "sign a voluntary electrification pledge instead; COP32 goes to Addis "
     "Ababa. — REUTERS"),
]

TIMELINE = [
    ("24 NOV 11:40", "Israel kills Hamas security chief in Gaza City"),
    ("14:27", "PIF Tower hit in Riyadh — 11 wounded"),
    ("16:51", "Yemen military: Houthis 60 km from Aden"),
    ("EVENING", "Huawei guilty verdict in New York"),
    ("25 NOV 01:00", "700,000 Russian soldiers killed in Ukraine war"),
]

# (panel title, colour, [(headline, body, source tag), ...])
REGIONS_LEFT = [
    ("AMERICAS", (21, 101, 160), [
        ("Trump pardons turkeys \u201cFreedom\u201d and \u201cFeathers\u201d",
         "Annual White House ceremony ahead of Thanksgiving.", "REUTERS"),
        ("Giuliani awarded the Medal of Freedom",
         "Trump honours the former New York mayor at the White House.", "REUTERS"),
        ("Fort Hood shooter seeks stay of execution",
         "Nidal Hasan asks a court to halt next week's execution.", "REUTERS"),
        ("Cyberattack hits CIA and ODNI",
         "Attack affects classified information, CNN reports on 25 Nov.", "CNN"),
        ("Huawei guilty on 10 of 12 counts",
         "Trade-secret theft and bank fraud after a 3-month New York trial.", "US DOJ"),
        ("Radar outage delays flights at O'Hare",
         "FAA says arrivals may halt as delays mount in Chicago.", "REUTERS"),
        ("Wall Street fades on Tuesday",
         "Nasdaq -1.5%, S&P 500 -0.5%, Dow +423 (+0.9%).", "NY POST"),
    ]),
    ("EUROPE", (108, 52, 131), [
        ("Zelensky confirms Gulf of Finland ship strike",
         "Ukraine hit a Russian cargo ship; ally Norway urges caution.", "REUTERS"),
        ("Sarkozy corruption case ordered to trial",
         "Ex-president and wife Carla Bruni face a hearing on 1 Apr 2027.", "REUTERS"),
        ("NATO to deploy early-warning jets in Poland",
         "Move follows missiles landing on Polish territory.", "REUTERS"),
        ("700,000+ Russian soldiers killed in Ukraine",
         "New analysis puts the toll past 700,000 since the invasion.", "RFE/RL"),
        ("Russian strike kills 11 near Kyiv",
         "Apartment block hit; rescuers race to find survivors.", "RFE/RL"),
        ("Swedish MPs to vote on Kristersson as PM",
         "Parliament decides whether the Moderates leader stays on.", "REUTERS"),
    ]),
    ("MIDDLE EAST", (185, 119, 14), [
        ("Israel kills Hamas security chief in Gaza",
         "Naeem Abu Mohammed Nahel dies in Gaza City; six others killed.", "REUTERS"),
        ("Meningitis epidemic alert in Gaza",
         "272 cases in October — eight times the normal monthly rate.", "GAZA HEALTH MINISTRY"),
        ("Iran braces for winter gas shortages",
         "War damage deepens the energy crisis; rationing began 22 Nov.", "RFE/RL"),
        ("Three tankers hit mines in Hormuz, Iran says",
         "IRGC Navy reports the strikes in the Strait of Hormuz.", "IRGC NAVY"),
        ("Saudi strikes in Yemen's Lahj kill 25",
         "Buses and trucks hit; 25 dead or missing, Saba reports.", "SABA"),
        ("Israeli military suicides hit 16-year high",
         "23 soldiers took their lives in 2026, the most since 2010.", "HAARETZ"),
    ]),
]

REGIONS_RIGHT = [
    ("AFRICA", (30, 132, 73), [
        ("WHO evacuates staff in DRC's Ituri",
         "Workers sheltered 3 days from fighting in Akwe; Ebola toll 5,775 of 11,762.", "WHO"),
        ("Benghazi sinking risks Libya instability",
         "Ukraine's sinking of a Russian vessel stirs the frozen conflict.", "REUTERS"),
        ("COP32 goes to Ethiopia",
         "Addis Ababa hosts the next climate summit in Nov 2027.", "REUTERS"),
    ]),
    ("ASIA-PACIFIC", (202, 111, 30), [
        ("GTA 6 out worldwide on 19 Nov",
         "Rockstar's blockbuster launches for PS5 and Xbox Series X|S.", "PRESS"),
        ("Asian stocks surge on Huang's return",
         "Taiwan Taiex +9%, Kospi +6.3%, Nikkei +3.9% on Tuesday.", "CNN"),
        ("Anthropic sinks below its $83 IPO price",
         "Shares fall under the listing price for the first time since Thursday.", "NY POST"),
        ("Nepal PM makes first state visit to India",
         "Balendra Shah holds talks with Modi in New Delhi, 22\u201323 Nov.", "PRESS"),
    ]),
    ("SOUTH ASIA", (125, 60, 152), [
        ("BJP and Akali Dal reunite for Punjab 2027",
         "Alliance announced after a six-year split.", "PRESS"),
        ("RFE/RL returns to shortwave for Afghan girls",
         "Educational radio for girls barred from school.", "RFE/RL"),
        ("Denmark upholds \u201cghetto\u201d evictions",
         "Supreme Court backs the controversial housing policy.", "PRESS"),
    ]),
    ("TECH / SCIENCE / SPORT", (46, 64, 83), [
        ("Nvidia -5.8% as rally cools",
         "One-month implied volatility hits 68% after Monday's surge.", "NY POST / REUTERS"),
        ("Dell reports Q3 after the bell",
         "AI-server margins in focus for investors today.", "STOCKTWITS"),
        ("Eclipse caught as asteroid shadows asteroid",
         "Spacecraft watches Didymos shadow Dimorphos.", "PRESS"),
        ("Coral species \u201cresurrected\u201d on Great Barrier Reef",
         "Genetic analysis revives 12 Acropora species.", "PRESS"),
        ("Verstappen wins chaotic Las Vegas GP",
         "Ferraris collide in a dramatic night race.", "REUTERS"),
        ("Alcaraz wins first ATP Finals title",
         "Beats Zverev 6\u20132, 7\u20136 in Turin.", "PRESS"),
    ]),
]

NUMBERS = [
    ("$952bn", "added by Nvidia on Monday"),
    ("+31.5%", "Nvidia's Monday jump"),
    ("11", "wounded in the Riyadh tower strike"),
    ("60 km", "Houthis from Aden"),
    ("700,000", "Russian soldiers killed"),
    ("5,775", "Ebola deaths in DRC"),
]

# (label, value %, colour) for the markets bars
BARS = [
    ("NVDA Mon", 31.5, GREEN),
    ("Nasdaq Mon", 6.5, GREEN),
    ("S&P 500 Mon", 4.7, GREEN),
    ("Dow Mon", 3.0, GREEN),
    ("NVDA Tue", -5.8, RED),
]

# schematic map: (label, dot x, dot y, label dx, label dy) in panel coords
MAP_DOTS = [
    ("Las Vegas", 78, 52, 8, -4),
    ("Kyiv", 288, 30, -8, -14),
    ("Gaza", 300, 52, -40, -4),
    ("Benghazi", 276, 62, -62, 8),
    ("Riyadh", 332, 58, 8, -4),
    ("Aden", 338, 76, 8, -4),
    ("Banten", 468, 82, -48, 10),
]


def draw_masthead(s):
    d = s.d
    d.rectangle([0, 0, W, 62], fill=NAVY)
    s.centred(7, "THE WORLD IN ONE PAGE", 30, bold=True, fill=(255, 255, 255))
    s.centred(42, "WEDNESDAY 25 NOVEMBER 2026  \u2022  WORLD NEWS IN A SINGLE IMAGE",
              11, fill=(205, 214, 228))
    d.rectangle([0, 62, W, 65], fill=RED)


def draw_leads(s):
    y, h, w, gap = 70, 112, 328, 12
    for i, (kicker, head, body) in enumerate(LEADS):
        x = 8 + i * (w + gap)
        s.d.rectangle([x, y, x + w, y + h], fill=CARD, outline=EDGE)
        s.d.rectangle([x, y, x + w, y + 3], fill=RED)
        yy = s.para(x + 10, y + 9, w - 20, kicker, 9, fill=RED, bold=True)
        yy = s.para(x + 10, yy + 1, w - 20, head, 13, fill=INK,
                    leading=16, bold=True)
        s.para(x + 10, yy + 2, w - 20, body, 10, leading=13)


def draw_timeline(s):
    d = s.d
    y = 188
    s.text((8, y), "WEDNESDAY 25 NOV \u2014 AS THE DAY UNFOLDED", 11,
           bold=True, fill=NAVY)
    d.line([8, y + 18, W - 8, y + 18], fill=RED, width=2)
    col_w = 199
    for i, (when, what) in enumerate(TIMELINE):
        x = 8 + i * col_w
        d.text((x, y + 22), when, font=fnt(10, True), fill=RED)
        s.para(x, y + 36, col_w - 8, what, 9, leading=11)


def draw_map(s):
    px, py, pw, ph = 8, 248, 548, 120
    d = s.d
    d.rectangle([px, py, px + pw, py + ph], fill=OCEAN, outline=EDGE)
    s.text((px + 8, py + 4), "WHERE THE NEWS HAPPENED", 10, bold=True, fill=NAVY)
    # rough continent blobs (schematic, not to scale)
    blobs = [
        (18, 26, 128, 62, LAND), (96, 66, 138, 104, LAND),
        (238, 20, 288, 44, LAND), (246, 48, 296, 92, LEAF),
        (300, 16, 470, 62, LAND), (428, 84, 486, 104, LAND),
    ]
    for (x0, y0, x1, y1, col) in blobs:
        d.ellipse([px + x0, py + y0, px + x1, py + y1], fill=col)
    for label, dx, dy, lx, ly in MAP_DOTS:
        cx, cy = px + dx, py + dy
        d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=RED,
                  outline=(255, 255, 255))
        tx, ty = cx + lx, cy + ly
        for ox, oy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            d.text((tx + ox, ty + oy), label, font=fnt(9, True),
                   fill=(255, 255, 255))
        d.text((tx, ty), label, font=fnt(9, True), fill=INK)


def draw_markets(s):
    px, py, pw, ph = 564, 248, 452, 120
    d = s.d
    d.rectangle([px, py, px + pw, py + ph], fill=CARD, outline=EDGE)
    s.text((px + 10, py + 5), "MARKETS \u2014 MONDAY RALLY, TUESDAY FADE",
           10, bold=True, fill=NAVY)
    axis = px + 112
    top = py + 26
    scale = 230.0 / 31.5
    for i, (label, val, col) in enumerate(BARS):
        yy = top + i * 15
        d.text((px + 10, yy), label, font=fnt(9), fill=BODY)
        d.line([axis, top - 4, axis, top + 5 * 15 - 6], fill=EDGE, width=1)
        bar = int(abs(val) * scale)
        if val >= 0:
            d.rectangle([axis, yy + 1, axis + bar, yy + 11], fill=col)
            d.text((axis + bar + 5, yy), f"+{val}%", font=fnt(9, True), fill=col)
        else:
            d.rectangle([axis - bar, yy + 1, axis, yy + 11], fill=col)
            d.text((axis + 6, yy), f"{val}%", font=fnt(9, True), fill=col)
    s.para(px + 10, top + 5 * 15 + 2, pw - 20,
           "Asia Tue: Taiex +9% \u00b7 Kospi +6.3% \u00b7 Nikkei +3.9%. "
           "$12tn wiped from global stocks since 6 Oct. \u2014 AJ BELL / LSEG",
           8, fill=GREY, leading=10)


def draw_regions(s):
    left = Column(s, 8, 374, 496, 934)
    for title, colour, stories in REGIONS_LEFT:
        left.header(title, colour)
        for head, body, tag in stories:
            left.story(head, body, tag)
    right = Column(s, 520, 374, 496, 934)
    for title, colour, stories in REGIONS_RIGHT:
        right.header(title, colour)
        for head, body, tag in stories:
            right.story(head, body, tag)
    print(f"region columns end at y={left.y} (left) / {right.y} (right)")


def draw_numbers(s):
    d = s.d
    y = 940
    d.rectangle([8, y, W - 8, 1016], fill=CARD, outline=EDGE)
    s.text((16, y + 6), "BY THE NUMBERS", 11, bold=True, fill=NAVY)
    col_w = (W - 32) // 6
    for i, (val, label) in enumerate(NUMBERS):
        x = 16 + i * col_w
        d.text((x, y + 24), val, font=fnt(15, True), fill=RED)
        s.para(x, y + 44, col_w - 10, label, 8, fill=GREY, leading=10)


def main():
    s = Sheet()
    draw_masthead(s)
    draw_leads(s)
    draw_timeline(s)
    draw_map(s)
    draw_markets(s)
    draw_regions(s)
    draw_numbers(s)
    s.save()
    total = sum(len(stories) for _, _, stories in REGIONS_LEFT + REGIONS_RIGHT)
    print(f"stories: {len(LEADS)} leads + {total} region stories = "
          f"{len(LEADS) + total} total")


if __name__ == "__main__":
    main()
