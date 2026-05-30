#!/usr/bin/env python3
"""Generate the Kindle cover for BELIEVER.

Concept: the wordmark fractures along a fault line -- the word itself cracking
under a lie -- with a thin oxblood seam, on deep ink. Original art, no third-party imagery.
Output: 1600x2560 (KDP 1.6:1), rendered at 2x and downsampled for crisp edges.
"""
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

random.seed(1111)

SS = 2                      # supersample factor
W, H = 1600, 2560
W2, H2 = W * SS, H * SS

NOTO = "/usr/share/fonts/truetype/noto"
def serif(weight, size):
    return ImageFont.truetype(f"{NOTO}/NotoSerif-{weight}.ttf", size * SS)
def sans(weight, size):
    return ImageFont.truetype(f"{NOTO}/NotoSans-{weight}.ttf", size * SS)

# palette
INK_TOP   = (13, 17, 22)
INK_BOT   = (5, 7, 10)
BONE      = (236, 230, 216)
BONE_DIM  = (150, 148, 140)
OXBLOOD   = (158, 43, 37)
OXBLOOD_HOT = (201, 66, 58)

# ---------- background: vertical gradient + cold vignette + grain ----------
base = Image.new("RGB", (W2, H2), INK_BOT)
px = base.load()
for y in range(H2):
    t = y / (H2 - 1)
    # ease toward bottom
    t = t ** 1.15
    r = int(INK_TOP[0] + (INK_BOT[0] - INK_TOP[0]) * t)
    g = int(INK_TOP[1] + (INK_BOT[1] - INK_TOP[1]) * t)
    b = int(INK_TOP[2] + (INK_BOT[2] - INK_TOP[2]) * t)
    for x in range(W2):
        px[x, y] = (r, g, b)

# subtle cold glow behind the title
glow = Image.new("L", (W2, H2), 0)
gd = ImageDraw.Draw(glow)
cx, cy = W2 // 2, int(H2 * 0.40)
gd.ellipse([cx - W2 // 2, cy - int(H2 * 0.22), cx + W2 // 2, cy + int(H2 * 0.22)], fill=42)
glow = glow.filter(ImageFilter.GaussianBlur(220 * SS // 2))
glow_col = Image.new("RGB", (W2, H2), (30, 40, 52))
base = Image.composite(glow_col, base, glow)

# fine grain
grain = Image.new("L", (W2, H2))
gp = grain.load()
for y in range(H2):
    for x in range(W2):
        gp[x, y] = random.randint(118, 138)
grain = grain.filter(ImageFilter.GaussianBlur(0.5))
base = Image.blend(base, Image.merge("RGB", (grain, grain, grain)), 0.05)

draw = ImageDraw.Draw(base)

# ---------- helpers: letter-tracked text ----------
def tracked_width(text, font, tracking):
    w = 0
    for i, ch in enumerate(text):
        w += draw.textlength(ch, font=font)
        if i < len(text) - 1:
            w += tracking
    return w

def draw_tracked(xy, text, font, fill, tracking, anchor_center=True):
    x, y = xy
    if anchor_center:
        x -= tracked_width(text, font, tracking) / 2
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill)
        x += draw.textlength(ch, font=font) + tracking

def draw_tracked_layer(layer_draw, xy, text, font, fill, tracking):
    x, y = xy
    x -= sum(layer_draw.textlength(c, font=font) for c in text) / 2 + tracking * (len(text) - 1) / 2
    for ch in text:
        layer_draw.text((x, y), ch, font=font, fill=fill)
        x += layer_draw.textlength(ch, font=font) + tracking

# ---------- logline (top) ----------
tag_font = sans("Light", 33)
draw_tracked((W2 // 2, int(H2 * 0.085)), "HE CANNOT TELL A LIE.", tag_font, BONE_DIM, 8 * SS)
draw_tracked((W2 // 2, int(H2 * 0.085) + 52 * SS), "NEITHER CAN YOU.", tag_font, (170, 96, 90), 8 * SS)

# ---------- title wordmark, fractured ----------
title_font = serif("SemiBold", 150)
title = "BELIEVER"
title_tracking = 6 * SS

tl = Image.new("RGBA", (W2, H2), (0, 0, 0, 0))
tld = ImageDraw.Draw(tl)
title_y = int(H2 * 0.40)
draw_tracked_layer(tld, (W2 // 2, title_y), title, title_font, BONE + (255,), title_tracking)

bbox = tl.getbbox()
l, t, r, b = bbox
fault_y = t + int((b - t) * 0.60)

top_part = tl.crop((0, 0, W2, fault_y))
bot_part = tl.crop((0, fault_y, W2, H2))

# offset the lower fragment: slipped along the fault
off_x = 13 * SS
off_y = 4 * SS

frac = Image.new("RGBA", (W2, H2), (0, 0, 0, 0))
frac.alpha_composite(top_part, (0, 0))
frac.alpha_composite(bot_part, (off_x, fault_y + off_y))

# faint drop shadow for the wordmark to seat it on the ink
shadow = frac.split()[3].filter(ImageFilter.GaussianBlur(6 * SS))
sh_img = Image.new("RGBA", (W2, H2), (0, 0, 0, 0))
sh_img.putalpha(shadow)
base.paste((0, 0, 0), (0, 0), sh_img.split()[3].point(lambda a: int(a * 0.55)))

base.paste(frac, (0, 0), frac)

# ---------- the fault: a jagged oxblood seam across the title ----------
crack_pad = 70 * SS
xs0, xs1 = l - crack_pad, r + crack_pad + off_x
pts = []
x = xs0
seg = 26 * SS
while x < xs1:
    jitter = random.randint(-9 * SS, 9 * SS)
    pts.append((x, fault_y + jitter))
    x += random.randint(seg // 2, seg)
pts.append((xs1, fault_y + random.randint(-5 * SS, 5 * SS)))

# outer glow of the crack
crack_layer = Image.new("RGBA", (W2, H2), (0, 0, 0, 0))
cld = ImageDraw.Draw(crack_layer)
cld.line(pts, fill=OXBLOOD + (255,), width=5 * SS, joint="curve")
glow_crack = crack_layer.filter(ImageFilter.GaussianBlur(7 * SS))
base.paste(glow_crack, (0, 0), glow_crack)
# hot core
cld2 = ImageDraw.Draw(base)
cld2.line(pts, fill=OXBLOOD_HOT, width=2 * SS, joint="curve")

# a single bead of red slipping from the fault
bead_x = int((l + r) / 2 + off_x // 2)
bead_top = fault_y + 6 * SS
bead_bottom = fault_y + 120 * SS
bd = ImageDraw.Draw(base)
bd.line([(bead_x, bead_top), (bead_x, bead_bottom)], fill=OXBLOOD, width=2 * SS)
bd.ellipse([bead_x - 9 * SS, bead_bottom - 9 * SS, bead_x + 9 * SS, bead_bottom + 9 * SS], fill=OXBLOOD_HOT)

# ---------- subtitle ----------
sub_font = ImageFont.truetype(f"{NOTO}/NotoSerif-Italic.ttf", 54 * SS)
draw_tracked((W2 // 2, int(H2 * 0.55)), "The truth has a radius.", sub_font, (192, 188, 178), 2 * SS)

# ---------- hairline + author ----------
rule_y = int(H2 * 0.90)
rule_w = int(W2 * 0.20)
draw.line([(W2 // 2 - rule_w, rule_y), (W2 // 2 + rule_w, rule_y)], fill=(90, 88, 82), width=1 * SS)
auth_font = sans("Regular", 40)
draw_tracked((W2 // 2, rule_y + 30 * SS), "OTTO  QUILL", auth_font, BONE, 12 * SS)

# ---------- downsample + save ----------
final = base.resize((W, H), Image.LANCZOS)
final.save("/home/paul/git/ottoquill/believer/art/cover.jpg", "JPEG", quality=92, optimize=True)
final.save("/home/paul/git/ottoquill/believer/art/cover.png", "PNG", optimize=True)
print("cover written:", final.size)
