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


# Panel 1: Real Estate Agent (welcome state)
px = panel_x[0]
draw_panel_head(px, "Real Estate Agent", "Ready to help you 24/7 with instant information.")
cx = px + PW // 2
cy_av = PANEL_TOP + 230
draw_avatar(cx, cy_av, 28)
title = "Hi, I'm Sandesh AI Assistant"
bb = d.textbbox((0, 0), title, font=f(15, bold=True))
d.text((cx - (bb[2] - bb[0]) // 2, cy_av + 50), title, fill=TEXT, font=f(15, bold=True))
d.text((cx + (bb[2] - bb[0]) // 2 + 6, cy_av + 48), "👋", fill=TEXT, font=f(16))
for j, ln in enumerate([
    "Ask me about property advice, investment tips, or",
    "any of your real estate related questions.",
]):
    bb = d.textbbox((0, 0), ln, font=f(12))
    d.text((cx - (bb[2] - bb[0]) // 2, cy_av + 80 + j * 18), ln, fill=MUTED, font=f(12))
draw_input(px, "Ask a Question")
draw_foot(px, "Agent by", "A2V2.ai")

# Panel 2: Companion with tabs (Forum / Notes / AI Connection — Notes active)
px = panel_x[1]
d.rectangle((px, PANEL_TOP, px + PW, PANEL_BOTTOM), fill=(250, 250, 251))

# Tab bar
TAB_H = 56
d.rectangle((px, PANEL_TOP, px + PW, PANEL_TOP + TAB_H), fill=WHITE)
d.line((px, PANEL_TOP + TAB_H, px + PW, PANEL_TOP + TAB_H), fill=LIGHT, width=1)
tabs = [("Forum", False), ("Notes", True), ("AI Connection", False)]
tab_w = PW // 3
for i, (label, active) in enumerate(tabs):
    tx = px + i * tab_w
    color = BLUE if active else (138, 138, 142)
    weight_font = f(11, bold=True)
    bb = d.textbbox((0, 0), label, font=weight_font)
    d.text((tx + tab_w // 2 - (bb[2] - bb[0]) // 2, PANEL_TOP + 30), label, fill=color, font=weight_font)
    icon_color = BLUE if active else (170, 170, 175)
    d.ellipse((tx + tab_w // 2 - 4, PANEL_TOP + 14, tx + tab_w // 2 + 4, PANEL_TOP + 22), fill=icon_color)
    if active:
        d.rectangle((tx + 12, PANEL_TOP + TAB_H - 2, tx + tab_w - 12, PANEL_TOP + TAB_H), fill=BLUE)

# Body content
cy = PANEL_TOP + TAB_H + 14
left_pad = px + 18
right_pad = px + PW - 18
body_w = PW - 36

# Header row: title + count + new note button
d.text((left_pad, cy + 4), "My Notes", fill=TEXT, font=f(15, bold=True))
count_text = "23 notes"
bb = d.textbbox((0, 0), count_text, font=f(11))
title_w = d.textbbox((0, 0), "My Notes", font=f(15, bold=True))[2]
d.text((left_pad + title_w + 10, cy + 8), count_text, fill=(150, 150, 153), font=f(11))
# New Note button (right)
nn_text = "+ New Note"
bb = d.textbbox((0, 0), nn_text, font=f(11, bold=True))
nn_w = bb[2] - bb[0] + 22
nn_x = right_pad - nn_w
d.rounded_rectangle((nn_x, cy, nn_x + nn_w, cy + 26), 8, fill=BLUE)
d.text((nn_x + 11, cy + 7), nn_text, fill=WHITE, font=f(11, bold=True))
cy += 36

# Filter chips row (All, John 3 active, Romans, ...)
filters = [("All", False), ("John 3", True), ("Romans", False), ("Psalms", False)]
fx = left_pad
ft_fc = f(11, bold=True)
for label, active in filters:
    bb = d.textbbox((0, 0), label, font=ft_fc)
    cw = bb[2] - bb[0] + 18
    if active:
        d.rounded_rectangle((fx, cy, fx + cw, cy + 24), 12, fill=BLUE)
        d.text((fx + 9, cy + 5), label, fill=WHITE, font=ft_fc)
    else:
        d.rounded_rectangle((fx, cy, fx + cw, cy + 24), 12, fill=WHITE, outline=LIGHT, width=1)
        d.text((fx + 9, cy + 5), label, fill=(107, 107, 110), font=ft_fc)
    fx += cw + 6
cy += 34

# Section header
d.text((left_pad, cy), "RECENT", fill=(107, 107, 110), font=f(10, bold=True))
cy += 18


def wrap_text(text, font, max_w):
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


def note_card(stripe_color, ref, body, when, tag=None):
    global cy
    ft_body = f(11)
    inner_left = left_pad + 14
    body_max = right_pad - 14 - inner_left
    body_lines = wrap_text(body, ft_body, body_max)
    h = 12 + 16 + 4 + len(body_lines) * 16 + (24 if tag else 0) + 10
    # base card
    d.rounded_rectangle((left_pad, cy, right_pad, cy + h), 10, fill=WHITE, outline=LIGHT, width=1)
    # color stripe on left
    d.rectangle((left_pad, cy, left_pad + 4, cy + h), fill=stripe_color)
    # header: ref left, date right
    d.text((inner_left, cy + 10), ref, fill=BLUE, font=f(12, bold=True))
    bb = d.textbbox((0, 0), when, font=f(10))
    d.text((right_pad - 12 - (bb[2] - bb[0]), cy + 12), when, fill=(150, 150, 153), font=f(10))
    # body
    yy = cy + 32
    for ln in body_lines:
        d.text((inner_left, yy), ln, fill=TEXT, font=ft_body)
        yy += 16
    # tag pill
    if tag:
        bb = d.textbbox((0, 0), tag, font=f(9))
        tw = bb[2] - bb[0] + 14
        d.rounded_rectangle((inner_left, yy + 6, inner_left + tw, yy + 22), 8, fill=(243, 243, 244))
        d.text((inner_left + 7, yy + 8), tag, fill=(120, 120, 122), font=f(9))
    cy += h + 8


# Highlight colors
YELLOW = (250, 211, 92)
GREEN = (62, 178, 122)
BLUE_ST = (29, 108, 243)
PURPLE = (192, 132, 252)
ORANGE = (255, 154, 60)

note_card(
    YELLOW,
    "John 3:16",
    "Memorized this in 4th grade VBS. Reading it now as an adult, the word “whoever” hits different — the gospel really is for everyone.",
    "Today",
    tag="Reflection",
)
note_card(
    PURPLE,
    "John 3:8",
    "Spirit like wind — can't see it but you see its effect. Beautiful imagery for how the Spirit works invisibly in a person's life.",
    "Yesterday",
    tag="Imagery",
)
note_card(
    GREEN,
    "John 3:5",
    "Look up: “water” = baptism vs. physical-birth interpretation. Ask Pastor Mike at Tuesday study.",
    "2 days ago",
    tag="Question",
)
note_card(
    BLUE_ST,
    "John 3:1-2",
    "Nicodemus comes by night — fear of being seen with Jesus, or symbolic of the spiritual darkness he's coming out of? Probably both.",
    "3 days ago",
    tag="Observation",
)
note_card(
    ORANGE,
    "Romans 5:8",
    "Cross-reference for John 3:16. God's love demonstrated, not just declared. Action over words.",
    "Last week",
    tag="Cross-ref",
)

# Bottom composer
ib_h = 60
ib_y = PANEL_BOTTOM - ib_h
d.rectangle((px, ib_y, px + PW, PANEL_BOTTOM), fill=WHITE)
d.line((px, ib_y, px + PW, ib_y), fill=LIGHT, width=1)
inp_y = ib_y + 14
d.rounded_rectangle((left_pad, inp_y, right_pad, inp_y + 32), 8, outline=(229, 229, 229), width=1)
d.text((left_pad + 12, inp_y + 8), "Jot a quick note on this passage…", fill=(180, 180, 180), font=f(12))
d.text((right_pad - 22, inp_y + 8), "➤", fill=BLUE, font=f(13))

# Panel 3: YouVersion-style Bible reader
px = panel_x[2]

# Top bar (replaces panel-head)
TOP_H = 56
d.rectangle((px, PANEL_TOP, px + PW, PANEL_TOP + TOP_H), fill=WHITE)
d.line((px, PANEL_TOP + TOP_H, px + PW, PANEL_TOP + TOP_H), fill=LIGHT, width=1)

# hamburger
d.text((px + 16, PANEL_TOP + 18), "≡", fill=(40, 40, 42), font=f(22))

# pickers (centered)
pick_y = PANEL_TOP + 14
pick_book_text = "John 3"
pick_trans_text = "WEB"
ft_pick = f(12, bold=True)
bb = d.textbbox((0, 0), pick_book_text, font=ft_pick)
book_w = bb[2] - bb[0] + 30
bb = d.textbbox((0, 0), pick_trans_text, font=ft_pick)
trans_w = bb[2] - bb[0] + 30
total = book_w + trans_w + 8
start_x = px + PW // 2 - total // 2
# book pill (gray)
d.rounded_rectangle((start_x, pick_y, start_x + book_w, pick_y + 28), 14, fill=(243, 243, 244))
d.text((start_x + 12, pick_y + 7), pick_book_text, fill=(40, 40, 42), font=ft_pick)
d.text((start_x + book_w - 16, pick_y + 11), "▾", fill=(140, 140, 140), font=f(9, bold=True))
# translation pill (orange)
tx = start_x + book_w + 8
d.rounded_rectangle((tx, pick_y, tx + trans_w, pick_y + 28), 14, fill=(255, 231, 194))
d.text((tx + 12, pick_y + 7), pick_trans_text, fill=(255, 122, 0), font=ft_pick)
d.text((tx + trans_w - 16, pick_y + 11), "▾", fill=(255, 122, 0), font=f(9, bold=True))

# search icon
d.text((px + PW - 32, PANEL_TOP + 18), "⌕", fill=(40, 40, 42), font=f(20))

# Reader area
ACTION_H = 50
reader_top = PANEL_TOP + TOP_H
reader_bottom = PANEL_BOTTOM - ACTION_H
left_pad = px + 28
right_pad = px + PW - 28
text_w = PW - 56

# CHAPTER label
ft_lbl = f(10, bold=True)
lbl = "CHAPTER"
bb = d.textbbox((0, 0), lbl, font=ft_lbl)
d.text((px + PW // 2 - (bb[2] - bb[0]) // 2, reader_top + 16), lbl, fill=(176, 176, 179), font=ft_lbl)

# Big chapter number
ft_num = f(72)
nbb = d.textbbox((0, 0), "3", font=ft_num)
d.text((px + PW // 2 - (nbb[2] - nbb[0]) // 2, reader_top + 30), "3", fill=TEXT, font=ft_num)

cy = reader_top + 130


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


def section(title):
    global cy
    ft = f(11, bold=True)
    cy += 6
    d.text((left_pad, cy), title.upper(), fill=(107, 107, 110), font=ft)
    cy += 22


# Render verse paragraph: tokens are (kind, content). We layout in flowing line.
def render_paragraph(verses, highlight_set=None):
    """verses: list of (verse_num, text). Optionally highlight a set of verse numbers."""
    global cy
    if highlight_set is None:
        highlight_set = set()
    ft_text = f(13)
    ft_vn = f(8, bold=True)
    line_h = 22
    # tokenize
    tokens = []
    for vn, text in verses:
        tokens.append(("vn", str(vn), vn))
        for word in text.split(" "):
            tokens.append(("word", word, vn))

    # layout
    x = left_pad
    line_tokens = []  # list of (type, content, vnum, w, x_start)

    def flush_line(last=False):
        nonlocal x, line_tokens
        global cy
        # draw highlight backgrounds first per verse run
        i = 0
        while i < len(line_tokens):
            t, c, vn, w, sx = line_tokens[i]
            if vn in highlight_set and t == "word":
                # find run end
                j = i
                run_x1 = sx
                run_x2 = sx + w
                while j + 1 < len(line_tokens) and line_tokens[j + 1][2] in highlight_set and line_tokens[j + 1][0] == "word":
                    j += 1
                    run_x2 = line_tokens[j][4] + line_tokens[j][3]
                d.rounded_rectangle((run_x1 - 2, cy + 1, run_x2 + 2, cy + line_h - 3), 2, fill=(255, 243, 168))
                i = j + 1
            else:
                i += 1
        # draw glyphs
        for t, c, vn, w, sx in line_tokens:
            if t == "vn":
                d.text((sx, cy + 1), c, fill=(176, 176, 179), font=ft_vn)
            else:
                d.text((sx, cy + 4), c, fill=TEXT, font=ft_text)
        cy += line_h
        x = left_pad
        line_tokens = []

    for tok in tokens:
        kind, content, vn = tok
        if kind == "vn":
            ft = ft_vn
            extra = " "
            tw = d.textbbox((0, 0), content, font=ft)[2] + 6
        else:
            ft = ft_text
            tw = d.textbbox((0, 0), content + " ", font=ft)[2]
        if x + tw > right_pad and line_tokens:
            flush_line()
        if kind == "vn":
            line_tokens.append(("vn", content, vn, tw - 4, x))
        else:
            line_tokens.append(("word", content, vn, tw - 4, x))
        x += tw
    if line_tokens:
        flush_line(last=True)
    cy += 4


# Section 1
section("Jesus Teaches Nicodemus")
render_paragraph([
    (1, "Now there was a man of the Pharisees named Nicodemus, a ruler of the Jews."),
    (2, "He came to Jesus by night and said to him, “Rabbi, we know that you are a teacher come from God.”"),
    (3, "Jesus answered him, “Most certainly I tell you, unless one is born anew, he can’t see God’s Kingdom.”"),
    (4, "Nicodemus said to him, “How can a man be born when he is old?”"),
])

# Section 2
section("For God So Loved the World")
render_paragraph(
    [
        (16, "For God so loved the world, that he gave his one and only Son, that whoever believes in him should not perish, but have eternal life."),
        (17, "For God didn’t send his Son into the world to judge the world, but that the world should be saved through him."),
    ],
    highlight_set={16},
)

# Action bar at bottom
ab_y = reader_bottom
d.rectangle((px, ab_y, px + PW, ab_y + ACTION_H), fill=WHITE)
d.line((px, ab_y, px + PW, ab_y), fill=LIGHT, width=1)
actions = ["▶", "Aa", "🔖", "✎", "↗"]
slot = PW // len(actions)
for i, a in enumerate(actions):
    cx = px + slot * i + slot // 2
    ft_a = f(13, bold=True) if a == "Aa" else f(15)
    bb = d.textbbox((0, 0), a, font=ft_a)
    d.text((cx - (bb[2] - bb[0]) // 2, ab_y + 14), a, fill=(107, 107, 110), font=ft_a)

img.save("/home/user/churches/preview-notes.png")
print("saved preview-notes.png", img.size)
