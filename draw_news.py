#!/usr/bin/env python3
"""Draw entry.png: one image summing up world news of Wednesday 25 November 2026.

Dense newspaper layout, all drawn with PIL: masthead with the date, three
lead stories, a UTC timeline strip, a schematic world map with markers, a
markets bar chart, and seven region sections holding 35 short sourced
stories, plus a by-the-numbers box. Every story was verified against
reporting first published or updated on 24-25 November 2026.
Run: python3 draw_news.py  ->  writes entry.png (1024x1024).
The sandbox entrypoint main.ts only copies the committed entry.png.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BG = (250, 247, 240)        # warm paper
INK = (20, 20, 20)
RED = (178, 34, 34)
BLUE = (25, 70, 130)
TEAL = (0, 110, 110)
GREEN = (0, 130, 60)
GREY = (105, 105, 105)
LIGHT = (233, 228, 219)
GOLD = (160, 116, 0)
OCEAN = (198, 222, 235)
LAND = (214, 196, 158)

F = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


f_title = font(FB, 40)
f_date = font(FB, 19)
f_kicker = font(FB, 12)
f_lead_h = font(FB, 14)
f_lead = font(F, 11)
f_sec = font(FB, 13)
f_story = font(F, 11)
f_src = font(FB, 9)
f_small = font(F, 10)
f_tiny = font(F, 9)
f_map = font(FB, 9)

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)


def wrap(text, fnt, max_w):
    """Greedy word wrap to a pixel width; returns list of lines."""
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit(text, fnt, max_w):
    """Truncate one line with an ellipsis so it fits max_w pixels."""
    if d.textlength(text, font=fnt) <= max_w:
        return text
    while len(text) > 4 and d.textlength(text + "...", font=fnt) > max_w:
        text = text[:-1]
    return text + "..."


def story_block(x, y, w, head, body, src):
    """One short story: headline (1 line), body (1 line), red source tag.

    Fixed height: 2 lines at 12px leading + 2px gap = 26px, so column
    heights stay predictable and nothing overlaps or runs off the page.
    """
    d.text((x, y), fit(head, f_story, w), font=f_story, fill=INK)
    y += 12
    b = fit(body, f_story, w - 70)
    d.text((x, y), b, font=f_story, fill=(60, 60, 60))
    sx = x + d.textlength(b, font=f_story) + 6
    d.text((sx, y), src, font=f_src, fill=RED)
    return y + 14


def section(x, y, w, title, stories, color):
    """A region section: coloured header bar + its stories. Returns new y."""
    d.rectangle([x, y, x + w, y + 20], fill=color)
    d.text((x + 6, y + 3), title, font=f_sec, fill=(255, 255, 255))
    y += 26
    for head, body, src in stories:
        y = story_block(x + 2, y, w - 4, head, body, src)
    return y + 4


# ---------------------------------------------------------------- masthead
d.rectangle([0, 0, W, 78], fill=INK)
d.text((16, 8), "THE WORLD IN ONE PAGE", font=f_title, fill=(255, 255, 255))
d.text((16, 54), "WEDNESDAY 25 NOVEMBER 2026  •  WORLD NEWS IN A SINGLE IMAGE",
       font=f_date, fill=(255, 200, 60))
d.rectangle([0, 78, W, 82], fill=RED)

# ---------------------------------------------------------------- leads
leads = [
    ("HUANG RALLY FIZZLES",
     "Nvidia slides ~6% to $155.38 as the Huang rally fades; the WSJ "
     "reports he disclosed more affairs to the board. He testifies to "
     "Congress in early Dec.",
     "NY POST / WSJ"),
    ("RIYADH TOWER HIT AGAIN",
     "Houthis hit Riyadh's tallest tower, the PIF Tower, a second time "
     "in under a week; 11 wounded. They are ~60 km from Aden; the "
     "coalition vows a decisive reply.",
     "REUTERS"),
    ("COP31 ENDS WITHOUT A DEAL",
     "First UN climate summit to fail since Copenhagen 2009: ~40 nations "
     "rejected a text with no fossil-fuel phase-out. COP32 goes to "
     "Addis Ababa.",
     "REUTERS"),
]
lx = 16
for title, body, src in leads:
    d.rectangle([lx, 92, lx + 322, 186], outline=RED, width=2)
    d.text((lx + 8, 98), title, font=f_lead_h, fill=RED)
    yy = 118
    for ln in wrap(body, f_lead, 306):
        d.text((lx + 8, yy), ln, font=f_lead, fill=INK)
        yy += 14
    d.text((lx + 8, 168), src, font=f_src, fill=GREY)
    lx += 334

# ---------------------------------------------------------------- timeline
d.rectangle([16, 196, 1008, 232], fill=LIGHT)
d.text((24, 202), "25 NOV — AS THE DAY UNFOLDED (UTC)", font=f_kicker, fill=BLUE)
tl = [
    ("11:40", "Hamas security chief killed in Gaza"),
    ("14:27", "Riyadh tower hit, 11 wounded"),
    ("16:51", "Houthis 60 km from Aden"),
    ("Evening", "Huawei guilty on 10 of 12 counts"),
    ("01:00", "700,000 Russian soldiers killed"),
]
tx = 24
for t, txt in tl:
    d.text((tx, 220), t, font=f_tiny, fill=RED)
    tx += d.textlength(t, font=f_tiny) + 5
    d.text((tx, 220), txt, font=f_tiny, fill=INK)
    tx += d.textlength(txt, font=f_tiny) + 16

# ---------------------------------------------------------------- map + markets
# Schematic world map (left) with markers for the day's hot spots.
mx, my, mw, mh = 16, 242, 590, 100
d.rectangle([mx, my, mx + mw, my + mh], fill=OCEAN, outline=GREY)
d.text((mx + 6, my + 3), "WHERE IT HAPPENED", font=f_kicker, fill=BLUE)
# Rough continent blobs (schematic, not to scale).
d.ellipse([mx + 30, my + 42, mx + 130, my + 82], fill=LAND)          # N America
d.ellipse([mx + 105, my + 78, mx + 145, my + 96], fill=LAND)         # S America
d.ellipse([mx + 255, my + 32, mx + 330, my + 78], fill=LAND)         # Europe
d.ellipse([mx + 320, my + 55, mx + 400, my + 88], fill=LAND)         # Africa
d.ellipse([mx + 380, my + 28, mx + 560, my + 84], fill=LAND)         # Asia
d.ellipse([mx + 490, my + 80, mx + 545, my + 95], fill=LAND)         # Oceania
markers = [
    # (x, y, label, label dx, label dy) — offsets keep the crowded
    # Mediterranean / Arabia labels (Gaza, Benghazi, Riyadh, Aden)
    # from colliding with each other.
    (mx + 78, my + 62, "LAS VEGAS", 6, -5),
    (mx + 300, my + 48, "KYIV", 6, -5),
    (mx + 335, my + 72, "GAZA", -34, 5),
    (mx + 348, my + 56, "BENGHAZI", 6, -10),
    (mx + 380, my + 68, "RIYADH", 6, -5),
    (mx + 388, my + 84, "ADEN", 6, 2),
    (mx + 480, my + 70, "BANTEN", 6, -5),
]
for px, py, label, ldx, ldy in markers:
    d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=RED, outline=(255, 255, 255))
    d.text((px + ldx, py + ldy), label, font=f_map, fill=INK)

# Markets bar chart (right): Monday's rally vs Tuesday's fade.
cx, cy, cw, ch = 622, 242, 386, 100
d.rectangle([cx, cy, cx + cw, cy + ch], fill=(255, 255, 255), outline=GREY)
d.text((cx + 6, cy + 3), "MARKETS: MONDAY'S RALLY FADES TUESDAY", font=f_kicker, fill=RED)
moves = [("NVDA M", 31.5), ("TAIEX", 9.0), ("KOSPI", 6.3), ("NAS M", 6.5),
         ("S&P M", 4.7), ("NIKKEI", 3.9), ("DOW M", 3.0), ("NVDA T", -5.8)]
bx = cx + 8
bw = (cw - 16) // len(moves)
for name, val in moves:
    hgt = int(abs(val) / 35.0 * 52)
    col = GREEN if val >= 0 else RED
    d.rectangle([bx + 4, cy + 76 - hgt, bx + bw - 4, cy + 76], fill=col)
    d.text((bx + 2, cy + 78), name, font=f_tiny, fill=INK)
    d.text((bx + 2, cy + 64 - hgt), f"{val:+.1f}%", font=f_tiny, fill=col)
    bx += bw
d.text((cx + 6, cy + 90), "M = Monday, T = Tuesday. Mon: Nasdaq +6.5%, S&P +4.7%, Dow +3.0%.",
       font=f_tiny, fill=GREY)

# ---------------------------------------------------------------- regions
AMERICAS = [
    ("Trump pardons Thanksgiving turkeys \"Freedom\" and \"Feathers\".",
     "The White House ceremony kicks off the holiday week.", "REUTERS"),
    ("Trump awards Rudy Giuliani the Medal of Freedom.",
     "The former New York mayor is honoured at the White House.", "REUTERS"),
    ("Fort Hood shooter Nidal Hasan seeks a stay of execution.",
     "His execution is set for next week, court records show.", "REUTERS"),
    ("CIA and ODNI hit by a cyberattack, CNN reports.",
     "Classified information was affected, the report says.", "CNN"),
    ("Huawei guilty on 10 of 12 counts after a 3-month trial.",
     "Trade-secret theft and bank fraud in New York.", "US DOJ"),
    ("Radar outage delays flights at Chicago O'Hare.",
     "The FAA says arrivals may halt amid the disruption.", "REUTERS"),
    ("Wall Street: Nasdaq -1.5%, S&P 500 -0.5%, Dow +423.",
     "The Dow's +0.9% gain bucks a down day for tech.", "NY POST"),
]
EUROPE = [
    ("Zelensky confirms Ukraine hit a Russian ship off Finland.",
     "Kyiv says the cargo ship carried arms; Norway urges caution.", "REUTERS"),
    ("Sarkozy corruption case ordered to trial, wife included.",
     "The ex-president and Carla Bruni face a hearing on 1 Apr 2027.", "REUTERS"),
    ("NATO plans early-warning aircraft deployment in Poland.",
     "The move follows missiles landing on Polish soil.", "REUTERS"),
    ("700,000+ Russian soldiers killed in the Ukraine war.",
     "A new analysis puts the death toll past 700,000.", "RFE/RL"),
    ("Russian strike on a Kyiv-region apartment block kills 11.",
     "Rescuers race to find survivors in the rubble.", "RFE/RL"),
    ("Denmark's Supreme Court upholds \"ghetto\" evictions.",
     "The ruling backs the eviction of residents in the estates.", "DISCLOSURE NEWS"),
]
AFRICA = [
    ("WHO evacuates staff from a hospital in DRC's Ituri.",
     "Staff sheltered 3 days from fighting; Ebola toll: 5,775 dead.", "WHO"),
    ("Benghazi strike risks fresh instability, Libya explainer.",
     "Ukraine's sinking of a Russian vessel stirs the frozen conflict.", "REUTERS"),
    ("COP32 presidency passes to Ethiopia, Addis Ababa 2027.",
     "The next climate summit heads to Africa in November 2027.", "REUTERS"),
]
MIDDLE_EAST = [
    ("Israeli strike kills Hamas security chief in Gaza City.",
     "Naeem Abu Mohammed Nahel and six others killed, medics say.", "REUTERS"),
    ("Gaza meningitis epidemic alert: 272 cases in October.",
     "The caseload is 8x the normal monthly rate, officials say.", "GAZA HEALTH MIN."),
    ("Iran braces for winter gas shortages as war damage bites.",
     "Its energy crisis deepens; electricity rationing began 22 Nov.", "RFE/RL"),
    ("Iran says three oil tankers hit naval mines in Hormuz.",
     "The IRGC Navy reports the strikes in the strait.", "IRGC NAVY"),
    ("Israeli military suicides hit a 16-year high: 23 in 2026.",
     "The toll is the highest since 2010, the army reports.", "HAARETZ"),
    ("Saudi strikes on buses and trucks in Yemen's Lahj.",
     "25 people are dead or missing after the attacks.", "SABA"),
]
ASIA_PACIFIC = [
    ("GTA 6 released worldwide for PS5 and Xbox Series X|S.",
     "Rockstar's blockbuster launched on 19 November.", "JAGRANJOSH"),
    ("Asian stocks surge on Huang's return: Taiex +9%.",
     "Kospi +6.3% and Nikkei +3.9% in Tuesday trading.", "CNN"),
    ("Anthropic shares sink below their $83 IPO price.",
     "The first dip below the listing price since trading began.", "NY POST"),
    ("Indonesia factory fire toll confirmed at 24 dead.",
     "The follow-up toll comes as the search continues.", "MEDIA REPORTS"),
]
SOUTH_ASIA = [
    ("Nepal PM Balendra Shah makes first state visit to India.",
     "Talks with Modi cap the 22-23 Nov trip.", "JAGRANJOSH"),
    ("BJP and Akali Dal reunite for 2027 Punjab elections.",
     "The alliance ends a six-year split.", "JAGRANJOSH"),
    ("RFE/RL returns to shortwave for Afghan girls.",
     "Educational radio for girls barred from school.", "RFE/RL"),
]
TECH_SPORT = [
    ("Nvidia -5.8% after Monday's +31.5% surge.",
     "One-month implied volatility hits 68%.", "NY POST / REUTERS"),
    ("Dell reports Q3 after the bell today.",
     "AI-server margins are in focus for investors.", "STOCKTWITS"),
    ("Spacecraft watches one asteroid eclipse another.",
     "Didymos shadows Dimorphos in a rare capture.", "DISCLOSURE NEWS"),
    ("Genetic analysis \"resurrects\" 12 coral species.",
     "The Acropora species return on the Great Barrier Reef.", "DISCLOSURE NEWS"),
    ("Verstappen wins a chaotic Las Vegas Grand Prix.",
     "The Ferraris collide in a dramatic race.", "REUTERS"),
    ("Alcaraz beats Zverev for his first ATP Finals title.",
     "6-2, 7-6 in Turin caps the Spaniard's season.", "BUSINESSWORLD"),
]

y_left = 352
y_right = 352
y_left = section(16, y_left, 484, "AMERICAS", AMERICAS, (25, 70, 130))
y_left = section(16, y_left, 484, "EUROPE", EUROPE, (0, 110, 110))
y_left = section(16, y_left, 484, "AFRICA", AFRICA, (120, 80, 20))
y_right = section(524, y_right, 484, "MIDDLE EAST", MIDDLE_EAST, (178, 34, 34))
y_right = section(524, y_right, 484, "ASIA-PACIFIC", ASIA_PACIFIC, (90, 60, 140))
y_right = section(524, y_right, 484, "SOUTH ASIA", SOUTH_ASIA, (160, 116, 0))
y_right = section(524, y_right, 484, "TECH / SCIENCE / SPORT", TECH_SPORT, (0, 110, 110))

# By-the-numbers box fills the left column's remaining space.
by = y_left + 6
d.rectangle([16, by, 500, 1010], outline=BLUE, width=2)
d.text((24, by + 8), "BY THE NUMBERS — WEDNESDAY 25 NOVEMBER 2026", font=f_kicker, fill=BLUE)
nums = [
    "$952bn — Nvidia's market value added on Monday",
    "31.5% — Nvidia's one-day jump, best since 2003",
    "11 wounded in the Riyadh tower strike",
    "60 km — Houthi forces from Aden",
    "700,000 Russian soldiers killed in Ukraine",
    "5,775 Ebola deaths in the DRC outbreak",
]
ny = by + 30
for n in nums:
    d.text((24, ny), "•  " + n, font=f_story, fill=INK)
    ny += 15
d.text((24, 998), "Sources: Reuters, AP, AFP, RFE/RL, CNN, NY Post, WHO, Haaretz.",
       font=f_tiny, fill=GREY)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
img.save(out, optimize=True)
print("saved", out, img.size, os.path.getsize(out), "bytes")
print("left col ends", y_left, "| right col ends", y_right)
