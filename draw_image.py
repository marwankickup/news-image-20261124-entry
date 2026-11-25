#!/usr/bin/env python3
"""Draw "The World on Tuesday" — a newspaper front page summing up the
world news of Tuesday 24 November 2026. Deterministic: fixed fonts,
fixed geometry, no timestamps, no randomness. Output: 1024x1024 PNG.
"""
import sys
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (247, 243, 232)
INK = (26, 26, 26)
RED = (178, 34, 34)
BLUE = (30, 64, 120)
GREY = (110, 105, 95)
LIGHT = (232, 226, 210)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"


def font(name, size):
    try:
        return ImageFont.truetype(FONT_DIR + name, size)
    except OSError:
        return ImageFont.load_default()


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_panel(d, x, y, w, h, tag, tag_color, headline, sub, picto):
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255),
                outline=(200, 192, 172), width=2)
    # tag bar
    d.rectangle([x, y, x + w, y + 34], fill=tag_color)
    d.text((x + 12, y + 7), tag, font=SANS_B(20), fill=(255, 255, 255))
    # pictogram zone on the right
    px, py = x + w - 118, y + 46
    picto(d, px, py)
    # headline + sub on the left
    tx = x + 12
    tw = w - 150
    lines = wrap(d, headline, SANS_B(27), tw)
    cy = y + 48
    for ln in lines:
        d.text((tx, cy), ln, font=SANS_B(27), fill=INK)
        cy += 32
    cy += 6
    for ln in wrap(d, sub, SANS(19), tw):
        d.text((tx, cy), ln, font=SANS(19), fill=(70, 66, 58))
        cy += 24


# ---- pictograms (simple flat shapes, drawn in a ~110x110 box) ----

def pic_gaza(d, x, y):
    # burst star over a rooftop line
    cx, cy = x + 55, y + 42
    for k in range(8):
        import math
        a = math.pi * k / 4
        x2 = cx + int(48 * math.cos(a))
        y2 = cy + int(48 * math.sin(a))
        d.line([cx, cy, x2, y2], fill=RED, width=5)
    d.ellipse([cx - 13, cy - 13, cx + 13, cy + 13], fill=RED)
    # clearer skyline: two taller blocks with lit windows
    d.rectangle([x + 8, y + 78, x + 102, y + 100], fill=INK)
    d.rectangle([x + 16, y + 60, x + 46, y + 78], fill=INK)
    d.rectangle([x + 62, y + 66, x + 94, y + 78], fill=INK)
    d.rectangle([x + 24, y + 66, x + 30, y + 72], fill=(255, 196, 0))
    d.rectangle([x + 34, y + 66, x + 40, y + 72], fill=(255, 196, 0))
    d.rectangle([x + 70, y + 70, x + 76, y + 76], fill=(255, 196, 0))


def pic_zaporizhzhia(d, x, y):
    # cracked building with a lightning bolt
    d.rectangle([x + 14, y + 22, x + 66, y + 100], fill=(70, 70, 70))
    d.rectangle([x + 70, y + 48, x + 100, y + 100], fill=(150, 145, 135))
    # wider, brighter crack across the facade
    d.line([x + 20, y + 30, x + 40, y + 52, x + 30, y + 62, x + 52, y + 92],
           fill=(255, 255, 255), width=6)
    d.line([x + 44, y + 26, x + 54, y + 46], fill=(255, 255, 255), width=4)
    d.polygon([(x + 84, y + 6), (x + 62, y + 48), (x + 76, y + 48),
               (x + 58, y + 92), (x + 96, y + 40), (x + 80, y + 40)],
              fill=(255, 196, 0))


def pic_korea(d, x, y):
    # fighter jet over radar arcs
    d.arc([x + 4, y + 30, x + 106, y + 132], 180, 360, fill=BLUE, width=4)
    d.arc([x + 20, y + 46, x + 90, y + 116], 180, 360, fill=BLUE, width=3)
    d.polygon([(x + 8, y + 52), (x + 102, y + 52), (x + 88, y + 62),
               (x + 22, y + 62)], fill=INK)
    d.polygon([(x + 52, y + 30), (x + 62, y + 52), (x + 48, y + 52)],
              fill=INK)
    d.polygon([(x + 30, y + 62), (x + 40, y + 62), (x + 34, y + 76)],
              fill=INK)
    d.polygon([(x + 70, y + 62), (x + 80, y + 62), (x + 76, y + 76)],
              fill=INK)
    d.ellipse([x + 48, y + 8, x + 62, y + 22], fill=RED)


def pic_germany_ukraine(d, x, y):
    # two flags side by side over a document
    d.rectangle([x + 8, y + 12, x + 50, y + 24], fill=(0, 0, 0))
    d.rectangle([x + 8, y + 24, x + 50, y + 36], fill=(221, 0, 0))
    d.rectangle([x + 8, y + 36, x + 50, y + 48], fill=(255, 206, 0))
    d.rectangle([x + 60, y + 12, x + 102, y + 30], fill=(0, 87, 184))
    d.rectangle([x + 60, y + 30, x + 102, y + 48], fill=(255, 215, 0))
    d.rectangle([x + 18, y + 58, x + 92, y + 100], fill=(255, 255, 255),
                outline=INK, width=2)
    d.line([x + 26, y + 70, x + 84, y + 70], fill=INK, width=3)
    d.line([x + 26, y + 80, x + 84, y + 80], fill=INK, width=3)
    d.line([x + 26, y + 90, x + 60, y + 90], fill=INK, width=3)


def pic_iraq(d, x, y):
    # oil pumpjack
    d.rectangle([x + 10, y + 92, x + 100, y + 100], fill=(120, 90, 40))
    d.polygon([(x + 34, y + 92), (x + 46, y + 34), (x + 54, y + 34),
               (x + 66, y + 92)], fill=INK)
    d.polygon([(x + 20, y + 40), (x + 96, y + 26), (x + 96, y + 36),
               (x + 20, y + 50)], fill=INK)
    d.line([x + 96, y + 31, x + 96, y + 62], fill=INK, width=4)
    d.rectangle([x + 88, y + 60, x + 104, y + 74], fill=INK)
    d.ellipse([x + 42, y + 28, x + 56, y + 42], fill=RED)


def pic_space(d, x, y):
    # satellite on an orbit ring
    d.ellipse([x + 2, y + 6, x + 108, y + 108], outline=BLUE, width=4)
    d.rectangle([x + 42, y + 42, x + 68, y + 62], fill=(90, 90, 90))
    d.rectangle([x + 14, y + 46, x + 40, y + 58], fill=(30, 64, 120))
    d.rectangle([x + 70, y + 46, x + 96, y + 58], fill=(30, 64, 120))
    d.line([x + 68, y + 52, x + 70, y + 52], fill=INK, width=2)
    d.polygon([(x + 84, y + 8), (x + 88, y + 20), (x + 100, y + 20),
               (x + 90, y + 28), (x + 94, y + 40), (x + 84, y + 32),
               (x + 74, y + 40), (x + 78, y + 28), (x + 68, y + 20),
               (x + 80, y + 20)], fill=RED)
    d.ellipse([x + 84, y + 84, x + 96, y + 96], fill=(255, 196, 0))


PANELS = [
    ("GAZA", RED,
     "Israeli strike kills Hamas security chief",
     "Naeem Abu Nahel and six others killed in Gaza, officials say.",
     pic_gaza),
    ("UKRAINE", (120, 60, 30),
     "Russian strike hits Zaporizhzhia overnight",
     "Two killed and 40 wounded, including four children, officials say.",
     pic_zaporizhzhia),
    ("SOUTH KOREA", BLUE,
     "Russian jets enter air-defence zone",
     "About five aircraft near Ulleung Island; fighters scrambled, a brief alert lifted.",
     pic_korea),
    ("GERMANY \u2013 UKRAINE", (0, 90, 60),
     "Berlin first into Ukraine's DELTA system",
     "Letter of intent signed; interceptor-missile deal agreed. No combat data shared.",
     pic_germany_ukraine),
    ("IRAQ", (90, 60, 10),
     "PM orders federal control of oilfields",
     "Fields in four provinces and Kurdish border crossings seized after smuggling probe.",
     pic_iraq),
    ("NATO / SPACE", (60, 40, 90),
     "Rutte vows to defend space after reports",
     "German media report a possible Russian nuclear-armed satellite, 'Sputnik-S'.",
     pic_space),
]


def main():
    out_path = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # masthead
    d.text((W // 2, 18), "THE WORLD", font=SERIF_B(76), fill=INK, anchor="ma")
    d.text((W // 2, 102), "on Tuesday", font=SERIF(34), fill=RED, anchor="ma")
    d.rectangle([32, 148, W - 32, 150], fill=INK)
    d.text((W // 2, 158), "TUESDAY, 24 NOVEMBER 2026",
           font=SANS_B(30), fill=INK, anchor="ma")
    d.rectangle([32, 196, W - 32, 198], fill=INK)

    # grid: 2 columns x 3 rows
    gx, gy = 32, 214
    pw, ph, gap = 468, 240, 24
    for i, (tag, color, head, sub, picto) in enumerate(PANELS):
        x = gx + (i % 2) * (pw + gap)
        y = gy + (i // 2) * (ph + 14)
        draw_panel(d, x, y, pw, ph, tag, color, head, sub, picto)

    # footer
    d.rectangle([32, 968, W - 32, 970], fill=INK)
    d.text((W // 2, 978), "Six stories from Tuesday 24 November 2026 \u2022 compiled from wire reports",
           font=SANS(18), fill=GREY, anchor="ma")

    img.save(out_path, format="PNG", optimize=True)


if __name__ == "__main__":
    main()
