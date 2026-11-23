#!/usr/bin/env python3
"""Build the GTA 6 meme-x v2 image: a WANTED poster for Rockstar Games.

Concept (fresh, different from v1's HOA fine): Rockstar is WANTED, 6 stars,
for the crime of making 200 million people wait 13 years for GTA 6.
1080x1080, PIL only, deterministic.
"""
import math
import random
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1080
CREAM = (245, 233, 200)
INK = (26, 22, 18)
RED = (139, 0, 0)
GOLD = (255, 193, 7)
GOLD_DARK = (176, 124, 0)
GRAY_BG = (201, 201, 201)
DARK_BAND = (22, 20, 18)

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def star_points(cx, cy, r_outer, r_inner, rot=-90):
    pts = []
    for i in range(10):
        r = r_outer if i % 2 == 0 else r_inner
        ang = math.radians(rot + i * 36)
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    return pts


def draw_star(d, cx, cy, r):
    d.polygon(star_points(cx, cy, r, r * 0.42), fill=GOLD, outline=GOLD_DARK)
    d.polygon(star_points(cx, cy, r * 0.55, r * 0.23), fill=(255, 214, 64))


def center_text(d, y, text, fnt, fill):
    w = d.textlength(text, font=fnt)
    d.text(((W - w) / 2, y), text, font=fnt, fill=fill)
    return y + fnt.size


def wrap_center(d, y, text, fnt, fill, max_w, line_gap=6):
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    for line in lines:
        y = center_text(d, y, line, fnt, fill)
        y += line_gap
    return y


img = Image.new("RGB", (W, H), CREAM)
d = ImageDraw.Draw(img)

# subtle paper speckle (deterministic)
rng = random.Random(6)
for _ in range(900):
    x, y = rng.randint(0, W - 1), rng.randint(0, H - 1)
    shade = rng.choice([(238, 224, 186), (250, 240, 210), (228, 210, 164)])
    d.point((x, y), fill=shade)

# double border frame
d.rectangle([14, 14, W - 15, H - 15], outline=INK, width=6)
d.rectangle([30, 30, W - 31, H - 31], outline=RED, width=3)

# WANTED headline
y = 48
y = center_text(d, y, "WANTED", font(BOLD, 140), RED)
d.line([(140, y + 8), (W - 140, y + 8)], fill=INK, width=5)

# six gold stars
star_y = 250
star_r = 40
gap = 108
x0 = (W - (6 * gap - (gap - 2 * star_r))) / 2 + star_r
for i in range(6):
    draw_star(d, x0 + i * gap, star_y, star_r)

# mugshot box (police lineup style)
box = (330, 310, 750, 560)
d.rectangle(box, fill=GRAY_BG, outline=INK, width=5)
# height marker lines on the left edge of the box
for hy in range(330, 550, 44):
    d.line([(box[0] + 8, hy), (box[0] + 28, hy)], fill=(120, 120, 120), width=3)
# caption top-left inside the box (clear of the silhouette)
d.text((box[0] + 24, box[1] + 10), "SUSPECT: THE DELAY", font=font(BOLD, 20), fill=(90, 90, 90))
# silhouette: head + shoulders
d.ellipse([488, 340, 592, 444], fill=INK)                       # head
d.pieslice([440, 440, 640, 560], 180, 360, fill=INK)            # shoulders
d.rectangle([440, 510, 640, 560], fill=INK)
# suit details: shirt V + tie
d.polygon([(540, 505), (512, 560), (568, 560)], fill=CREAM)
d.polygon([(540, 510), (530, 532), (540, 560), (550, 532)], fill=RED)

# name
y = 580
y = center_text(d, y, "ROCKSTAR GAMES", font(BOLD, 58), INK)

# charge lines
y += 14
y = wrap_center(d, y, "CRIME: Making 200 million people", font(BOLD, 36), INK, 920)
y = wrap_center(d, y, "wait 13 years for GTA 6.", font(BOLD, 36), INK, 920)
y += 8
y = wrap_center(d, y, 'LAST SEEN: Saying "Fall 2025"...', font(REG, 32), INK, 920)
y = wrap_center(d, y, 'then "May 2026".', font(REG, 32), INK, 920)
y += 8
y = wrap_center(d, y, "REWARD: $2,000,000,000 in pre-orders.", font(BOLD, 32), RED, 920)
y += 6
y = wrap_center(d, y, "WARNING: Do NOT approach —", font(BOLD, 30), INK, 920)
y = wrap_center(d, y, "they will delay again.", font(BOLD, 30), INK, 920)

# bottom dark band
d.rectangle([30, 990, W - 31, H - 31], fill=DARK_BAND)
center_text(d, 1008, "GTA VI  •  MAY 26, 2026  (ALLEGEDLY)", font(BOLD, 38), GOLD)

img.save("/home/hatch/workspace/makefun/gta6-meme-x-01-v2/meme.png")
print("saved meme.png", img.size)
