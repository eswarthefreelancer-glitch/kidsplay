"""Generate ready-to-post PNG promo graphics for KidsPlay (no external services)."""

from pathlib import Path
import math
import random

from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent
INK = "#343a40"
WHITE = "#ffffff"
FONT_BOLD = r"C:\Windows\Fonts\comicbd.ttf"
FONT_REG = r"C:\Windows\Fonts\comic.ttf"


def font(size, bold=True):
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REG, size)


def rgb(hex_color):
    h = hex_color.lstrip("#")
    return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))


def gradient(size, top, bottom):
    """Vertical gradient background."""
    w, h = size
    img = Image.new("RGB", size)
    d = ImageDraw.Draw(img)
    c1, c2 = rgb(top), rgb(bottom)
    for y in range(h):
        t = y / max(1, h - 1)
        color = tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))
        d.line((0, y, w, y), fill=color)
    return img


def text(d, xy, value, size, fill=INK, bold=True, anchor="mm", stroke=0, stroke_fill=WHITE):
    f = font(size, bold)
    d.text(xy, value, font=f, fill=fill, anchor=anchor,
           stroke_width=stroke, stroke_fill=stroke_fill)
    return d.textbbox(xy, value, font=f, anchor=anchor)


def fit_text(d, xy, value, size, max_width, **kwargs):
    while size > 12:
        box = text(d, xy, value, size, **kwargs)
        if box[2] - box[0] <= max_width:
            return
        size -= 2
    text(d, xy, value, size, **kwargs)


def rrect(d, box, fill=WHITE, outline=INK, width=8, radius=36):
    d.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def poly(d, pts, fill, outline=INK, width=6):
    d.polygon(pts, fill=fill)
    if width:
        d.line(list(pts) + [pts[0]], fill=outline, width=width, joint="curve")


def star(d, cx, cy, r, fill="#ffd43b", points=5, inner=0.45, outline=INK, width=4):
    pts = []
    for i in range(points * 2):
        angle = -math.pi / 2 + i * math.pi / points
        rr = r if i % 2 == 0 else r * inner
        pts.append((cx + rr * math.cos(angle), cy + rr * math.sin(angle)))
    poly(d, pts, fill, outline, width)


def confetti(d, seed, area, count=60):
    rng = random.Random(seed)
    colors = ["#ff6b6b", "#ffd43b", "#4dabf7", "#51cf66", "#9775fa", "#f06595"]
    x0, y0, x1, y1 = area
    for _ in range(count):
        x, y = rng.randint(x0, x1), rng.randint(y0, y1)
        r = rng.randint(5, 14)
        if rng.random() < 0.5:
            d.ellipse((x - r, y - r, x + r, y + r), fill=rng.choice(colors))
        else:
            d.rectangle((x - r, y - r // 2, x + r, y + r // 2), fill=rng.choice(colors))


def box_points(box):
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0

    def p(fx, fy):
        return (x0 + int(w * fx), y0 + int(h * fy))

    return p


# ---------- simple cute drawings (drawn inside a box) ----------

def draw_cat(d, box, fur="#ffc9a9"):
    p = box_points(box)
    d.ellipse((*p(0.22, 0.52), *p(0.78, 0.96)), fill=fur, outline=INK, width=6)
    poly(d, [p(0.20, 0.38), p(0.22, 0.10), p(0.40, 0.30)], fur)
    poly(d, [p(0.80, 0.38), p(0.78, 0.10), p(0.60, 0.30)], fur)
    d.ellipse((*p(0.15, 0.26), *p(0.85, 0.82)), fill=fur, outline=INK, width=7)
    d.ellipse((*p(0.31, 0.44), *p(0.39, 0.52)), fill=INK)
    d.ellipse((*p(0.61, 0.44), *p(0.69, 0.52)), fill=INK)
    poly(d, [p(0.46, 0.58), p(0.54, 0.58), p(0.50, 0.65)], "#f06595", INK, 3)
    d.line([p(0.50, 0.66), p(0.50, 0.72)], fill=INK, width=4)
    d.arc((*p(0.42, 0.63), *p(0.58, 0.75)), 0, 180, fill=INK, width=4)
    for dy in (0.60, 0.70):
        d.line([p(0.14, dy), p(0.36, dy - 0.03)], fill=INK, width=3)
        d.line([p(0.86, dy), p(0.64, dy - 0.03)], fill=INK, width=3)
    d.arc((*p(0.78, 0.62), *p(0.98, 0.92)), 250, 80, fill=INK, width=9)


def draw_lion(d, box, mane="#fcc419", face="#ffd43b"):
    p = box_points(box)
    for a in range(0, 360, 45):
        rad = math.radians(a)
        cx = 0.5 + 0.36 * math.cos(rad)
        cy = 0.46 + 0.36 * math.sin(rad)
        d.ellipse((*p(cx - 0.15, cy - 0.15), *p(cx + 0.15, cy + 0.15)), fill=mane, outline=INK, width=4)
    d.ellipse((*p(0.16, 0.14), *p(0.84, 0.80)), fill=mane, outline=INK, width=6)
    d.ellipse((*p(0.24, 0.24), *p(0.76, 0.74)), fill=face, outline=INK, width=5)
    d.ellipse((*p(0.30, 0.36), *p(0.39, 0.45)), fill=INK)
    d.ellipse((*p(0.61, 0.36), *p(0.70, 0.45)), fill=INK)
    poly(d, [p(0.45, 0.52), p(0.55, 0.52), p(0.50, 0.60)], "#a0613a", INK, 3)
    d.arc((*p(0.42, 0.55), *p(0.58, 0.70)), 0, 180, fill=INK, width=4)
    d.ellipse((*p(0.30, 0.74), *p(0.70, 0.98)), fill=face, outline=INK, width=6)


def draw_butterfly(d, box, wing="#9775fa"):
    p = box_points(box)
    d.ellipse((*p(0.08, 0.18), *p(0.48, 0.60)), fill=wing, outline=INK, width=6)
    d.ellipse((*p(0.52, 0.18), *p(0.92, 0.60)), fill=wing, outline=INK, width=6)
    d.ellipse((*p(0.12, 0.52), *p(0.46, 0.86)), fill="#f06595", outline=INK, width=6)
    d.ellipse((*p(0.54, 0.52), *p(0.88, 0.86)), fill="#f06595", outline=INK, width=6)
    d.ellipse((*p(0.44, 0.18), *p(0.56, 0.90)), fill="#343a40", outline=INK, width=4)
    d.line([p(0.49, 0.20), p(0.38, 0.04)], fill=INK, width=4)
    d.line([p(0.51, 0.20), p(0.62, 0.04)], fill=INK, width=4)
    for fx in (0.28, 0.72):
        d.ellipse((*p(fx - 0.06, 0.32), *p(fx + 0.06, 0.44)), fill="#ffd43b", outline=INK, width=3)


def draw_rocket(d, box, body="#4dabf7"):
    p = box_points(box)
    poly(d, [p(0.40, 0.20), p(0.50, 0.02), p(0.60, 0.20)], "#ff6b6b")
    d.rounded_rectangle((*p(0.32, 0.16), *p(0.68, 0.78)), radius=20,
                        fill=body, outline=INK, width=7)
    poly(d, [p(0.32, 0.52), p(0.12, 0.84), p(0.32, 0.74)], "#ff6b6b")
    poly(d, [p(0.68, 0.52), p(0.88, 0.84), p(0.68, 0.74)], "#ff6b6b")
    d.ellipse((*p(0.42, 0.30), *p(0.58, 0.46)), fill="#a5d8ff", outline=INK, width=5)
    poly(d, [p(0.42, 0.78), p(0.58, 0.78), p(0.50, 0.98)], "#ffd43b")
    poly(d, [p(0.46, 0.78), p(0.54, 0.78), p(0.50, 0.92)], "#ff922b", INK, 3)


def draw_fish(d, box, body="#22b8cf"):
    p = box_points(box)
    poly(d, [p(0.16, 0.50), p(0.02, 0.24), p(0.02, 0.76)], body)
    d.ellipse((*p(0.14, 0.22), *p(0.86, 0.78)), fill=body, outline=INK, width=7)
    poly(d, [p(0.48, 0.30), p(0.68, 0.14), p(0.70, 0.40)], "#4dabf7")
    d.ellipse((*p(0.70, 0.38), *p(0.80, 0.48)), fill=WHITE, outline=INK, width=3)
    d.ellipse((*p(0.74, 0.41), *p(0.78, 0.45)), fill=INK)
    d.arc((*p(0.35, 0.42), *p(0.65, 0.66)), 20, 160, fill=INK, width=4)


def draw_robot(d, box, body="#8ce99a"):
    p = box_points(box)
    d.line([p(0.50, 0.04), p(0.50, 0.18)], fill=INK, width=5)
    d.ellipse((*p(0.44, 0.01), *p(0.56, 0.13)), fill="#ff6b6b", outline=INK, width=3)
    d.rounded_rectangle((*p(0.20, 0.16), *p(0.80, 0.54)), radius=16,
                        fill=body, outline=INK, width=7)
    d.ellipse((*p(0.32, 0.26), *p(0.44, 0.38)), fill=WHITE, outline=INK, width=3)
    d.ellipse((*p(0.56, 0.26), *p(0.68, 0.38)), fill=WHITE, outline=INK, width=3)
    d.line([p(0.36, 0.46), p(0.64, 0.46)], fill=INK, width=4)
    d.rounded_rectangle((*p(0.28, 0.56), *p(0.72, 0.86)), radius=12,
                        fill="#a5d8ff", outline=INK, width=7)
    d.line([p(0.28, 0.64), p(0.08, 0.64)], fill=INK, width=9)
    d.line([p(0.72, 0.64), p(0.92, 0.64)], fill=INK, width=9)
    d.line([p(0.40, 0.86), p(0.40, 0.96)], fill=INK, width=9)
    d.line([p(0.60, 0.86), p(0.60, 0.96)], fill=INK, width=9)


def draw_house(d, box, wall="#ffc9a9"):
    p = box_points(box)
    poly(d, [p(0.10, 0.48), p(0.50, 0.12), p(0.90, 0.48)], "#ff6b6b")
    d.rectangle((*p(0.20, 0.46), *p(0.80, 0.92)), fill=wall, outline=INK, width=7)
    d.rectangle((*p(0.42, 0.64), *p(0.58, 0.92)), fill="#a0613a", outline=INK, width=5)
    d.ellipse((*p(0.53, 0.76), *p(0.56, 0.79)), fill="#ffd43b")
    d.rectangle((*p(0.26, 0.56), *p(0.38, 0.68)), fill="#a5d8ff", outline=INK, width=5)
    d.rectangle((*p(0.62, 0.56), *p(0.74, 0.68)), fill="#a5d8ff", outline=INK, width=5)


DRAWINGS = {
    "cat": draw_cat,
    "lion": draw_lion,
    "butterfly": draw_butterfly,
    "rocket": draw_rocket,
    "fish": draw_fish,
    "robot": draw_robot,
    "house": draw_house,
}


def coloring_card(img, box, name, bg="#ffffff"):
    d = ImageDraw.Draw(img)
    rrect(d, box, fill=bg, outline=INK, width=9, radius=34)
    inset = 18
    inner = (box[0] + inset, box[1] + inset, box[2] - inset, box[3] - inset)
    DRAWINGS[name](d, inner)


def crayon(d, x, y, length, angle, color):
    rad = math.radians(angle)
    ex = x + length * math.cos(rad)
    ey = y + length * math.sin(rad)
    d.line([(x, y), (ex, ey)], fill=color, width=26)
    d.line([(ex, ey), (ex + 18 * math.cos(rad), ey + 18 * math.sin(rad))], fill=INK, width=10)
    d.ellipse((x - 13, y - 13, x + 13, y + 13), fill=INK)


def title(d, cy, value, size=120, subtitle=None, sub_size=52, stroke_color="#ffffff"):
    text(d, (540, cy), value, size, fill="#ff6b6b", stroke=12, stroke_fill=stroke_color)
    if subtitle:
        text(d, (540, cy + size * 0.75), subtitle, sub_size, fill=INK, stroke=6,
             stroke_fill=stroke_color)


# ---------- 1. Instagram feed post (square) ----------

def feed_square(path):
    img = gradient((1080, 1080), "#fff3bf", "#b8e8ff")
    d = ImageDraw.Draw(img)
    confetti(d, 1, (0, 0, 1080, 1080), 70)
    title(d, 120, "KidsPlay", 128, "Color  •  Save  •  Smile!", 54)
    cards = [
        ((70, 350, 510, 710), "cat"),
        ((570, 350, 1010, 710), "lion"),
        ((70, 740, 510, 1030), "butterfly"),
        ((570, 740, 1010, 1030), "rocket"),
    ]
    for box, name in cards:
        coloring_card(img, box, name)
    star(d, 535, 370, 38, "#ffd43b")
    star(d, 535, 880, 30, "#f06595")
    crayon(d, 60, 1060, 130, -35, "#ff6b6b")
    crayon(d, 1020, 1060, 130, -145, "#4dabf7")
    img.save(path)


# ---------- 2. Instagram story / reel (vertical) ----------

def story_vertical(path):
    img = gradient((1080, 1920), "#ffe9a8", "#8de0e8")
    d = ImageDraw.Draw(img)
    confetti(d, 2, (0, 0, 1080, 1920), 90)
    title(d, 140, "KidsPlay", 132, "Let's color together!", 60)
    # tablet
    rrect(d, (130, 400, 950, 1330), fill="#f8f9fa", outline=INK, width=16, radius=70)
    rrect(d, (175, 445, 905, 1285), fill="#eaf9ff", outline="#adb5bd", width=6, radius=40)
    d.ellipse((530, 1290, 550, 1310), fill="#adb5bd")
    draw_rocket(d, (360, 540, 720, 1120))
    colors = ["#ff4d4d", "#ff922b", "#ffd43b", "#51cf66", "#22b8cf", "#4dabf7", "#9775fa", "#f06595"]
    for i, c in enumerate(colors):
        cx = 245 + i * 82
        d.ellipse((cx - 31, 1180, cx + 31, 1242), fill=c, outline=INK, width=5)
    # floating stickers
    d.ellipse((60, 1360, 300, 1600), fill="#ffffff", outline=INK, width=8)
    draw_cat(d, (80, 1380, 280, 1580))
    d.ellipse((780, 1360, 1020, 1600), fill="#ffffff", outline=INK, width=8)
    draw_butterfly(d, (800, 1380, 1000, 1580))
    star(d, 540, 1440, 46, "#ffd43b")
    fit_text(d, (540, 1690), "Tap. Color. Save. Smile!", 70, 980, stroke=6)
    fit_text(d, (540, 1790), "Perfect for little artists  •  ages 3–10", 44, 1000, stroke=4)
    img.save(path)


# ---------- 3. WhatsApp status (vertical) ----------

def whatsapp_vertical(path):
    img = gradient((1080, 1920), "#fff6d8", "#ffd6e8")
    d = ImageDraw.Draw(img)
    confetti(d, 3, (0, 0, 1080, 1920), 80)
    title(d, 140, "KidsPlay", 132, "Little hands, big imagination!", 55)
    cards = [
        ((80, 470, 380, 790), "lion"),
        ((400, 470, 700, 790), "butterfly"),
        ((720, 470, 1020, 790), "fish"),
        ((230, 850, 550, 1170), "robot"),
        ((560, 850, 880, 1170), "house"),
    ]
    for box, name in cards:
        coloring_card(img, box, name)
    star(d, 540, 1260, 48, "#ffd43b")
    fit_text(d, (540, 1420), "10 cute pages  •  18 bright colors", 62, 980, stroke=6)
    fit_text(d, (540, 1540), "Surprise Me  •  Start Over  •  Save Picture", 46, 1000, stroke=4)
    rrect(d, (250, 1660, 830, 1790), fill="#ffffff", outline=INK, width=8, radius=50)
    fit_text(d, (540, 1725), "Ask us for the link!", 56, 540)
    crayon(d, 90, 1890, 150, -35, "#51cf66")
    crayon(d, 990, 1890, 150, -145, "#9775fa")
    img.save(path)


# ---------- 4. Features card (square) ----------

def features_square(path):
    img = gradient((1080, 1080), "#dff9fb", "#fff3bf")
    d = ImageDraw.Draw(img)
    confetti(d, 4, (0, 0, 1080, 1080), 55)
    title(d, 110, "KidsPlay", 118, "Tiny buttons, BIG fun!", 54)
    rrect(d, (80, 285, 1000, 620), fill=WHITE, outline=INK, width=9, radius=40)
    colors = ["#ff4d4d", "#ff922b", "#ffd43b", "#51cf66", "#22b8cf", "#4dabf7",
              "#9775fa", "#f06595", "#a0613a", "#343a40", "#adb5bd", "#ffffff",
              "#8ce99a", "#a5d8ff", "#ffc9a9", "#d0bfff", "#fcc419", "#ff8787"]
    for i, c in enumerate(colors):
        row, col = divmod(i, 9)
        cx = 150 + col * 96
        cy = 380 + row * 130
        d.ellipse((cx - 38, cy - 38, cx + 38, cy + 38), fill=c, outline=INK, width=5)

    chips = [(80, 360, "#ffd43b"), (390, 690, "#a5d8ff"), (730, 1000, "#8ce99a")]
    for (x0, x1, color), label in zip(chips, ["Surprise\nMe", "Start\nOver", "Save\nPicture"]):
        rrect(d, (x0, 680, x1, 920), fill=color, outline=INK, width=8, radius=36)
        fit_text(d, ((x0 + x1) // 2, 840), label, 36, x1 - x0 - 20)
    star(d, 218, 750, 34, "#ffffff")
    d.arc((610, 725, 670, 785), 40, 320, fill=INK, width=7)
    poly(d, [(668, 722), (672, 750), (644, 742)], INK, INK, 3)
    d.line([(860, 730), (860, 790)], fill=INK, width=8)
    poly(d, [(840, 774), (880, 774), (860, 800)], INK, INK, 3)
    d.line([(830, 812), (890, 812)], fill=INK, width=7)
    fit_text(d, (540, 1000), "10 coloring pages  •  made for kids under 10", 38, 1000, stroke=4)
    img.save(path)


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    feed_square(OUT / "kidsplay-feed-square.png")
    story_vertical(OUT / "kidsplay-story-vertical.png")
    whatsapp_vertical(OUT / "kidsplay-whatsapp-status.png")
    features_square(OUT / "kidsplay-features-square.png")
    for p in sorted(OUT.glob("*.png")):
        print(p)
