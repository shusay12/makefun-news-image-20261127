#!/usr/bin/env python3
"""Draw the front page for Friday 27 November 2026.

Renders a 1024x1024 newspaper front page with Pillow and saves it as
entry.png next to this file. All news copy is baked in as constants so
the render is fully deterministic: same code, same bytes, every run.

Layout is cursor-based: every block advances a running y position and
the rules between sections sit after the tallest column, so no text
can run into the next section. Section bottoms are printed so the
fit can be checked from the log.
"""

import math
import os
import random

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
PAPER = (248, 244, 233)
INK = (18, 18, 18)
GREY = (92, 88, 80)
RED = (158, 27, 27)
BLUE = (29, 78, 137)
YELLOW = (242, 194, 0)
RULE = (18, 18, 18)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def text_w(d, s, f):
    return d.textlength(s, font=f)


def wrap(d, text, f, width):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if text_w(d, trial, f) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_line(d, text, path, max_size, width):
    """Largest size (down to 18) that fits text on one line."""
    size = max_size
    while size > 18:
        f = font(path, size)
        if text_w(d, text, f) <= width:
            return f
        size -= 1
    return font(path, 18)


def para(d, lines, x, y, f, fill, leading):
    for line in lines:
        d.text((x, y), line, font=f, fill=fill)
        y += leading
    return y


def hrule(d, x0, x1, y, width=2):
    d.line([(x0, y), (x1, y)], fill=RULE, width=width)


def kicker(d, x, y, label):
    d.text((x, y), label, font=font(SANS_B, 16), fill=RED)
    return y + 23


def accent_bar(d, x, y, color=RED):
    d.rectangle([x, y, x + 64, y + 4], fill=color)
    return y + 12


def skyline(d, x, y, w, h):
    rnd = random.Random(27)
    pts = [(x, y + h)]
    cx = x
    while cx < x + w:
        bw = rnd.randint(18, 44)
        bh = rnd.randint(int(h * 0.4), h)
        pts.append((cx, y + h - bh))
        pts.append((cx + bw, y + h - bh))
        pts.append((cx + bw, y + h))
        cx += bw
    pts.append((x + w, y + h))
    d.polygon(pts, fill=(30, 29, 28))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 36
    right = W - mx
    full = right - mx

    # ---- Masthead -------------------------------------------------
    d.text((W // 2, 20), "THE WORLD IN ONE DAY", font=font(SERIF_B, 52),
           fill=INK, anchor="ma")
    hrule(d, mx, right, 88, 3)
    d.text((W // 2, 98), "FRIDAY 27 NOVEMBER 2026",
           font=font(SERIF_B, 30), fill=RED, anchor="ma")
    d.text((W // 2, 136),
           "EARLY EDITION  •  NEWS FIRST REPORTED TODAY  •  VERIFIED ~01:00 UTC",
           font=font(SANS_B, 14), fill=GREY, anchor="ma")
    hrule(d, mx, right, 162, 3)
    hrule(d, mx, right, 167, 1)

    # ---- Lead story: Zelenskyy / BBC ------------------------------
    y = 182
    y = kicker(d, mx, y, "UKRAINE  •  LEAD STORY")
    f_h = fit_line(d, "ZELENSKYY: US TOO FOCUSED", SERIF_B, 42, full)
    d.text((mx, y), "ZELENSKYY: US TOO FOCUSED", font=f_h, fill=INK)
    y += 48
    f_h2 = fit_line(d, "ON MIDDLE EAST", SERIF_B, 42, full)
    d.text((mx, y), "ON MIDDLE EAST", font=f_h2, fill=INK)
    y += 50

    # Art panel, right of the deck and body. All art stays inside it.
    art_x, art_y, art_w, art_h = 668, y, 320, 168
    d.rectangle([art_x, art_y, art_x + art_w, art_y + art_h], fill=BLUE)
    band_y = art_y + art_h - 56
    # White interceptor trails rising inside the blue field.
    for (x0, y0, x1, y1) in [(692, band_y - 8, 800, art_y + 34),
                             (762, band_y - 8, 880, art_y + 44),
                             (832, band_y - 8, 948, art_y + 58)]:
        d.line([(x0, y0), (x1, y1)], fill=(255, 255, 255), width=4)
        d.ellipse([x1 - 5, y1 - 5, x1 + 5, y1 + 5], fill=(255, 255, 255))
    # Launcher triangle at the foot of the blue field.
    d.polygon([(700, band_y - 6), (724, band_y - 6), (712, band_y - 28)],
              fill=(255, 255, 255))
    d.rectangle([art_x, band_y, art_x + art_w, art_y + art_h], fill=YELLOW)
    d.text((art_x + 14, band_y + 8), "KYIV  •  AIR DEFENCE",
           font=font(SANS_B, 15), fill=INK)
    d.text((art_x + 14, band_y + 30),
           "70% of fastest drones downed", font=font(SANS, 14), fill=INK)

    text_wd = 600
    f_deck = font(SERIF, 21)
    deck = ("Kyiv says Patriot delays are costing lives — and calls "
            "Trump's \"my friend\" photo with Putin \"strange\".")
    y = para(d, wrap(d, deck, f_deck, text_wd), mx, y, f_deck, INK, 27)
    y += 6
    f_body = font(SERIF, 18)
    body = ("In a BBC interview in Kyiv, President Volodymyr Zelenskyy "
            "said the US is not pushing Russia hard enough in peace "
            "talks. He also warned of another major attack on the "
            "power grid.")
    y = para(d, wrap(d, body, f_body, text_wd), mx, y, f_body, INK, 24)
    y += 6
    d.text((mx, y), "BBC  •  27 NOV", font=font(SANS, 13), fill=GREY)
    lead_bottom = max(y + 19, art_y + art_h)
    print("lead_bottom", lead_bottom)
    hrule(d, mx, right, lead_bottom + 8, 2)

    # ---- Row 2: Gaza (left) and EU (right) -----------------------
    col_w = 464
    gap = 24
    y = lead_bottom + 22
    row2_top = y
    f_h3 = font(SERIF_B, 29)

    # Gaza column.
    gy = kicker(d, mx, row2_top, "GAZA  •  MIDDLE EAST")
    gy = para(d, ["ISRAEL KILLS 10 IN GAZA,", "HAMAS WEIGHS RESPONSE"],
              mx, gy, f_h3, INK, 36)
    gy = accent_bar(d, mx, gy + 4)
    gaza = ("Third night of strikes despite the ceasefire; 10 dead, "
            "including a Hamas deputy minister.")
    gy = para(d, wrap(d, gaza, f_body, col_w), mx, gy, f_body, INK, 24)
    gy += 4
    d.text((mx, gy), "REUTERS  •  27 NOV", font=font(SANS, 13), fill=GREY)
    gy += 12

    # EU column.
    ex = mx + col_w + gap
    ey = kicker(d, ex, row2_top, "EUROPE  •  BRUSSELS")
    ey = para(d, ["EU SPLIT OVER €45BN", "UKRAINE LOAN"],
              ex, ey, f_h3, INK, 36)
    ey = accent_bar(d, ex, ey + 4, color=BLUE)
    eu = ("Leaders haggle over a €1.7tn budget as financing for Kyiv "
          "next year divides the bloc.")
    ey = para(d, wrap(d, eu, f_body, col_w), ex, ey, f_body, INK, 24)
    ey += 4
    d.text((ex, ey), "27 NOV BRIEFING", font=font(SANS, 13), fill=GREY)
    ey += 12

    row2_bottom = max(gy, ey)
    print("row2_bottom", row2_bottom)
    hrule(d, mx, right, row2_bottom + 8, 2)

    # ---- Row 3: Chess (left) and Black Friday (right) ------------
    y = row2_bottom + 20
    row3_top = y

    # Chess column: one-line headline, fitted.
    cy = kicker(d, mx, row3_top, "SPORT  •  CHESS")
    f_c = fit_line(d, "GUKESH, SINDAROV DRAW AGAIN", SERIF_B, 27, col_w)
    d.text((mx, cy), "GUKESH, SINDAROV DRAW AGAIN", font=f_c, fill=INK)
    cy += f_c.size + 10
    bx, by = mx, cy
    sq = 22
    for r in range(2):
        for c in range(8):
            fill = INK if (r + c) % 2 == 0 else (255, 255, 255)
            d.rectangle([bx + c * sq, by + r * sq,
                         bx + (c + 1) * sq, by + (r + 1) * sq],
                        fill=fill, outline=INK)
    d.text((bx + 8 * sq + 12, by + 9), "60-move draw  •  1.5–1.5",
           font=font(SERIF_B, 19), fill=INK)
    cy += 2 * sq + 8
    chess = ("Game 3 of the world title match in Geneva ends level after "
             "60 moves. Friday is a rest day.")
    cy = para(d, wrap(d, chess, f_body, col_w), mx, cy, f_body, INK, 24)
    cy += 4
    d.text((mx, cy), "CHESS.COM  •  27 NOV", font=font(SANS, 13), fill=GREY)
    cy += 12

    # Black Friday column: one-line headline, fitted.
    fx = mx + col_w + gap
    fy = kicker(d, fx, row3_top, "BUSINESS  •  SHOPPING")
    f_b = fit_line(d, "BLACK FRIDAY: SHOPPERS HUNT DEALS", SERIF_B, 27, col_w)
    d.text((fx, fy), "BLACK FRIDAY: SHOPPERS HUNT DEALS", font=f_b, fill=INK)
    fy += f_b.size + 10
    tx, ty = fx, fy
    for i, pct in enumerate(["-30%", "-50%", "-20%"]):
        x0 = tx + i * 150
        d.polygon([(x0, ty), (x0 + 118, ty), (x0 + 136, ty + 22),
                   (x0 + 118, ty + 44), (x0, ty + 44)],
                  fill=RED if i == 1 else YELLOW)
        d.ellipse([x0 + 10, ty + 16, x0 + 22, ty + 28], fill=PAPER)
        d.text((x0 + 32, ty + 10), pct, font=font(SANS_B, 21),
               fill=(255, 255, 255) if i == 1 else INK)
    fy += 44 + 8
    bf = ("Salesforce reports bigger November discounts than last year.")
    fy = para(d, wrap(d, bf, f_body, col_w), fx, fy, f_body, INK, 24)
    fy += 4
    d.text((fx, fy), "27 NOV BRIEFING", font=font(SANS, 13), fill=GREY)
    fy += 12

    row3_bottom = max(cy, fy)
    print("row3_bottom", row3_bottom)
    hrule(d, mx, right, row3_bottom + 8, 2)

    # ---- Briefs strips (two rows) ---------------------------------
    y = row3_bottom + 16
    brief_rows = [
        [
            ("IBIZA — ", "A diesel tanker capsizes off the island; one dead."),
            ("LONDON — ", "UK net migration falls to its lowest since 1997."),
            ("HEALTH — ", "NHS warns of a flu surge as admissions climb."),
        ],
        [
            ("SERBIA — ", "Presidential election set for 27 December."),
            ("BRUSSELS — ", "ECB picks Hernández de Cos as next chief."),
            ("US — ", "Washington approves a possible F-16 sale to Ukraine."),
        ],
    ]
    bw = (full - 48) // 3
    f_brief = font(SERIF, 17)
    f_brief_b = font(SERIF_B, 17)
    brief_bottom = y
    for briefs in brief_rows:
        for i, (lead, rest) in enumerate(briefs):
            bx = mx + i * (bw + 24)
            lines = wrap(d, lead + rest, f_brief, bw)
            yy = y
            for li, line in enumerate(lines):
                if li == 0:
                    d.text((bx, yy), lead, font=f_brief_b, fill=RED)
                    d.text((bx + text_w(d, lead, f_brief_b), yy),
                           line[len(lead):], font=f_brief, fill=INK)
                else:
                    d.text((bx, yy), line, font=f_brief, fill=INK)
                yy += 21
            brief_bottom = max(brief_bottom, yy)
        y = brief_bottom + 6
    print("brief_bottom", brief_bottom)

    # ---- Footer ----------------------------------------------------
    hrule(d, mx, right, 984, 1)
    d.text((W // 2, 992),
           "All stories first reported Friday 27 November 2026  •  make.fun news-image-20261127",
           font=font(SANS, 13), fill=GREY, anchor="ma")

    img.save(OUT, format="PNG", optimize=True)
    print(f"wrote {OUT} {os.path.getsize(OUT)} bytes")


if __name__ == "__main__":
    main()
