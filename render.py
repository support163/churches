from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1400, 900
BG = (47, 48, 50)
WHITE = (255, 255, 255)
TEXT = (29, 29, 31)
MUTED = (138, 138, 138)
LIGHT = (236, 236, 236)
BLUE = (29, 108, 243)
BLUE2 = (47, 140, 255)
CHIP_BG = (240, 244, 255)
CHIP_BD = (216, 227, 255)
BUBBLE_BG = (243, 244, 246)

R = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
I = "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf"


def f(size, bold=False, italic=False):
    if bold:
        path = B
    elif italic:
        path = I
    else:
        path = R
    return ImageFont.truetype(path, size)


img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

# Header
d.text((26, 14), "Church", fill=(185, 185, 187), font=f(15))

# Window with shadow
WX, WY, WW, WH = 22, 44, W - 44, H - 66
shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
sd = ImageDraw.Draw(shadow)
sd.rounded_rectangle((WX + 4, WY + 8, WX + WW + 4, WY + WH + 8), 14, fill=(0, 0, 0, 110))
shadow = shadow.filter(ImageFilter.GaussianBlur(10))
img.paste(shadow, (0, 0), shadow)

d.rounded_rectangle((WX, WY, WX + WW, WY + WH), 14, fill=WHITE)

# Window bar
BAR_H = 50
d.rounded_rectangle((WX, WY, WX + WW, WY + BAR_H), 14, fill=(250, 250, 250))
d.rectangle((WX, WY + BAR_H - 14, WX + WW, WY + BAR_H), fill=(250, 250, 250))
d.line((WX, WY + BAR_H, WX + WW, WY + BAR_H), fill=LIGHT, width=1)

# Traffic lights
cy = WY + BAR_H // 2
for i, color in enumerate([(255, 95, 87), (254, 188, 46), (40, 200, 64)]):
    cx = WX + 24 + i * 22
    d.ellipse((cx - 7, cy - 7, cx + 7, cy + 7), fill=color)

# Nav buttons
nx = WX + 110
for ch in ["▤", "‹", "›"]:
    d.rounded_rectangle((nx, cy - 14, nx + 28, cy + 14), 4, outline=(220, 220, 220), width=1)
    bb = d.textbbox((0, 0), ch, font=f(16))
    d.text((nx + 14 - (bb[2] - bb[0]) // 2, cy - (bb[3] - bb[1]) // 2 - 2), ch, fill=(120, 120, 120), font=f(16))
    nx += 34

# URL pill
url_w = 380
url_x = WX + WW // 2 - url_w // 2
d.rounded_rectangle((url_x, cy - 14, url_x + url_w, cy + 14), 8, fill=(236, 236, 236))
d.text((url_x + 24, cy - 9), "🔒", fill=(80, 80, 80), font=f(13))
d.text((url_x + url_w // 2 - 30, cy - 9), "A2V2.ai", fill=(85, 85, 85), font=f(13))
d.text((url_x + url_w - 28, cy - 9), "⟳", fill=(120, 120, 120), font=f(15))

# Action icons
ax = WX + WW - 110
for ch in ["⇪", "+", "⧉"]:
    d.text((ax, cy - 9), ch, fill=(120, 120, 120), font=f(15))
    ax += 32

# Three panels
PANEL_TOP = WY + BAR_H
PANEL_BOTTOM = WY + WH
PW = WW // 3

panel_x = [WX, WX + PW, WX + 2 * PW]
for px in panel_x[1:]:
    d.line((px, PANEL_TOP, px, PANEL_BOTTOM), fill=LIGHT, width=1)


def draw_avatar(cx, cy, r, glyph=""):
    # gradient circle
    grad = Image.new("RGB", (r * 2, r * 2), BLUE)
    gd = ImageDraw.Draw(grad)
    for i in range(r * 2):
        ratio = i / (r * 2)
        col = (
            int(BLUE[0] + (BLUE2[0] - BLUE[0]) * ratio),
            int(BLUE[1] + (BLUE2[1] - BLUE[1]) * ratio),
            int(BLUE[2] + (BLUE2[2] - BLUE[2]) * ratio),
        )
        gd.line((0, i, r * 2, i), fill=col)
    mask = Image.new("L", (r * 2, r * 2), 0)
    md = ImageDraw.Draw(mask)
    md.ellipse((0, 0, r * 2, r * 2), fill=255)
    img.paste(grad, (cx - r, cy - r), mask)
    if glyph:
        ft = f(int(r * 1.1), bold=True)
        bb = d.textbbox((0, 0), glyph, font=ft)
        d.text((cx - (bb[2] - bb[0]) // 2, cy - (bb[3] - bb[1]) // 2 - 2), glyph, fill=WHITE, font=ft)


def draw_panel_head(px, title, subtitle, glyph=""):
    head_y = PANEL_TOP + 30
    # menu icon
    d.text((px + 18, head_y - 10), "≡", fill=(85, 85, 85), font=f(20))
    # avatar
    draw_avatar(px + 60, head_y, 18, glyph)
    # text
    d.text((px + 86, head_y - 12), title, fill=TEXT, font=f(14, bold=True))
    d.text((px + 86, head_y + 6), subtitle, fill=MUTED, font=f(11))
    d.line((px, PANEL_TOP + 64, px + PW, PANEL_TOP + 64), fill=(241, 241, 241), width=1)


def draw_input(px, placeholder):
    iy = PANEL_BOTTOM - 80
    d.rounded_rectangle((px + 16, iy, px + PW - 16, iy + 32), 8, outline=(229, 229, 229), width=1)
    d.text((px + 26, iy + 8), placeholder, fill=(180, 180, 180), font=f(12))
    d.text((px + PW - 36, iy + 8), "➤", fill=BLUE, font=f(13))
    # tools
    d.text((px + 22, iy + 42), "🔗  ☺  🎤", fill=(170, 170, 170), font=f(12))


def draw_foot(px, text, brand):
    fy = PANEL_BOTTOM - 22
    full = text + " " + brand
    bb = d.textbbox((0, 0), full, font=f(11))
    tw = bb[2] - bb[0]
    fx = px + PW // 2 - tw // 2
    d.text((fx, fy), text + " ", fill=(155, 155, 155), font=f(11))
    bb2 = d.textbbox((0, 0), text + " ", font=f(11))
    d.text((fx + (bb2[2] - bb2[0]), fy), brand, fill=(85, 85, 85), font=f(11, bold=True))


# Panel 1 & 2: Real Estate Agent (welcome state)
for i in range(2):
    px = panel_x[i]
    draw_panel_head(px, "Real Estate Agent", "Ready to help you 24/7 with instant information.")
    cx = px + PW // 2
    cy_av = PANEL_TOP + 230
    draw_avatar(cx, cy_av, 28)
    # Heading
    title = "Hi, I'm Sandesh AI Assistant"
    bb = d.textbbox((0, 0), title, font=f(15, bold=True))
    d.text((cx - (bb[2] - bb[0]) // 2, cy_av + 50), title, fill=TEXT, font=f(15, bold=True))
    # wave emoji-ish
    d.text((cx + (bb[2] - bb[0]) // 2 + 6, cy_av + 48), "👋", fill=TEXT, font=f(16))
    # subtitle
    line1 = "Ask me about property advice, investment tips, or"
    line2 = "any of your real estate related questions."
    for j, ln in enumerate([line1, line2]):
        bb = d.textbbox((0, 0), ln, font=f(12))
        d.text((cx - (bb[2] - bb[0]) // 2, cy_av + 80 + j * 18), ln, fill=MUTED, font=f(12))
    draw_input(px, "Ask a Question")
    draw_foot(px, "Agent by", "A2V2.ai")

# Panel 3: Bible (chat state)
px = panel_x[2]
draw_panel_head(px, "Bible", "Look up any passage by reference, instantly.", "✝")

cy = PANEL_TOP + 84
left_pad = px + 22
right_pad = px + PW - 22
chat_w = PW - 44

# Intro row
draw_avatar(left_pad + 14, cy + 10, 14, "✝")
d.text((left_pad + 36, cy), "Hi, I'm your Bible reference tool 📖", fill=TEXT, font=f(13, bold=True))
intro = "Type a reference like John 3:16 or Psalm 23 and I'll pull up the passage."
d.text((left_pad + 36, cy + 18), intro, fill=(110, 110, 110), font=f(11))
cy += 56


def wrap(text, font, max_w):
    words = text.split(" ")
    lines = []
    cur = ""
    for w in words:
        test = (cur + " " + w).strip()
        if d.textbbox((0, 0), test, font=font)[2] <= max_w:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def user_bubble(text):
    global cy
    ft = f(12)
    bb = d.textbbox((0, 0), text, font=ft)
    bw = bb[2] - bb[0] + 24
    bh = bb[3] - bb[1] + 18
    bx2 = right_pad
    bx1 = bx2 - bw
    d.rounded_rectangle((bx1, cy, bx2, cy + bh), 12, fill=BLUE)
    d.text((bx1 + 12, cy + 8), text, fill=WHITE, font=ft)
    cy += bh + 10


def bot_bubble(ref, body, translation, verses=False):
    global cy
    ft = f(12)
    ftref = f(10, bold=True)
    max_w = int(chat_w * 0.86) - 24
    lines = wrap(body, ft, max_w)
    bw = max_w + 24
    bh = 12 + 18 + len(lines) * 18 + 6 + 16 + 8
    d.rounded_rectangle((left_pad, cy, left_pad + bw, cy + bh), 12, fill=BUBBLE_BG)
    d.text((left_pad + 12, cy + 10), ref.upper(), fill=BLUE, font=ftref)
    yy = cy + 30
    for ln in lines:
        d.text((left_pad + 12, yy), ln, fill=TEXT, font=ft)
        yy += 18
    d.text((left_pad + 12, yy + 4), "— " + translation, fill=(140, 140, 140), font=f(10))
    cy += bh + 10


user_bubble("John 3:16")
bot_bubble(
    "John 3:16",
    "For God so loved the world, that he gave his one and only Son, that whoever believes in him should not perish, but have eternal life.",
    "World English Bible",
)
user_bubble("Psalm 23:1-3")
bot_bubble(
    "Psalm 23:1-3",
    "1 Yahweh is my shepherd: I shall lack nothing. 2 He makes me lie down in green pastures. He leads me beside still waters. 3 He restores my soul.",
    "World English Bible",
)

# Quick chips
chips = ["John 3:16", "Psalm 23", "Genesis 1:1-5", "Romans 8:28"]
chip_y = cy + 8
chip_x = left_pad
ft = f(11)
for c in chips:
    bb = d.textbbox((0, 0), c, font=ft)
    cw = bb[2] - bb[0] + 18
    if chip_x + cw > right_pad:
        chip_x = left_pad
        chip_y += 26
    d.rounded_rectangle((chip_x, chip_y, chip_x + cw, chip_y + 22), 11, fill=CHIP_BG, outline=CHIP_BD, width=1)
    d.text((chip_x + 9, chip_y + 4), c, fill=BLUE, font=ft)
    chip_x += cw + 6

draw_input(px, "Enter a reference (e.g. John 3:16)")
draw_foot(px, "Powered by", "bible-api.com")

img.save("/home/user/churches/preview.png")
print("saved preview.png", img.size)
