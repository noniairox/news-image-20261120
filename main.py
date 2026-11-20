#!/usr/bin/env python3
"""The World Today - 20 November 2026 front page.

Draws a deterministic 1024x1024 newspaper front page PNG (entry.png)
from the day's world news. No network access, no timestamps, no
randomness: the same run always produces the same bytes.

Usage:
    MAKEFUN_OUTPUT_DIR=/tmp/out1 python3 main.py
"""

import hashlib
import os

from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------- paths

FONT_DIR = "/usr/share/fonts/truetype"
SERIF = FONT_DIR + "/liberation/LiberationSerif-Regular.ttf"
SERIF_BOLD = FONT_DIR + "/liberation/LiberationSerif-Bold.ttf"
SERIF_ITALIC = FONT_DIR + "/liberation/LiberationSerif-Italic.ttf"
SANS = FONT_DIR + "/liberation/LiberationSans-Regular.ttf"
SANS_BOLD = FONT_DIR + "/liberation/LiberationSans-Bold.ttf"

PAGE_W = 1024
PAGE_H = 1024
MARGIN = 36
INK = (17, 17, 17)
PAPER = (255, 255, 255)
GREY = (90, 90, 90)

# ---------------------------------------------------------------- fonts


def font(path, size):
    return ImageFont.truetype(path, size)


F_MASTHEAD = font(SERIF_BOLD, 78)
F_DATE = font(SANS_BOLD, 17)
F_KICKER = font(SANS_BOLD, 20)
F_HEADLINE = font(SERIF_BOLD, 45)
F_DECK = font(SERIF_ITALIC, 21)
F_BODY = font(SERIF, 19)
F_SUBHEAD = font(SERIF_BOLD, 23)
F_SUBBODY = font(SERIF, 16)
F_LABEL = font(SANS_BOLD, 15)
F_FOOT = font(SANS, 14)
F_ALSO = font(SERIF_ITALIC, 16)

# ---------------------------------------------------------------- content

MASTHEAD = "THE WORLD TODAY"
DATE_LINE = "FRIDAY, 20 NOVEMBER 2026"
DATE_RIGHT = "ONE PAGE  •  THE WORLD IN BRIEF"

LEAD_KICKER = "THE HAGUE  —  INTERNATIONAL COURT OF JUSTICE"
LEAD_HEADLINE = "MYANMAR COMMITTED GENOCIDE AGAINST THE ROHINGYA, WORLD COURT RULES"
LEAD_DECK = (
    "First genocide finding against a state: a nine-to-six vote holds "
    "Myanmar responsible for its 2017 campaign in Rakhine."
)
LEAD_BODY = (
    "The International Court of Justice ruled on Thursday that Myanmar "
    "committed genocide against the Rohingya minority in its 2017 military "
    "campaign in northern Rakhine, the first time the world court has found "
    "a state responsible for genocide. The nine-to-six decision, read out in "
    "The Hague, held Myanmar responsible for killings, serious bodily harm "
    "and measures intended to prevent births within the group. More than "
    "700,000 Rohingya fled to Bangladesh during the crackdown, and refugees "
    "in the camps at Cox's Bazar cheered as the verdict was read. Myanmar "
    "has long denied the charge. The ruling is binding, though the court "
    "has no force of its own to enforce it."
)

SECONDARIES = [
    (
        "ANTHROPIC SHARES JUMP 17% IN RECORD $81.3BN IPO",
        "The AI company behind the Claude chatbot closed about 17% above "
        "its $83 offer price on its first day of trading, the largest "
        "initial public offering on record. The wider market fell anyway: "
        "the S&P 500 dropped 2.0%, its fifth straight loss.",
    ),
    (
        "TRUMP, XI AND PUTIN ISSUE PEACE DECLARATION IN SHENZHEN",
        "The leaders of the United States, China and Russia held their "
        "first three-way summit and signed a four-point peace declaration, "
        "while APEC leaders adopted the Shenzhen Outlook on trade, data "
        "and AI risks.",
    ),
    (
        "UKRAINE HITS CRIMEAN BRIDGE FOR THIRD TIME IN FOUR DAYS",
        "Kyiv struck the bridge linking Russia to occupied Crimea again, "
        "the third attack in four days, as Moscow vowed a harsher "
        "response and European allies met in Berlin to agree a united "
        "position for talks with Russia.",
    ),
    (
        "CYCLONE AKVAN MAKES LANDFALL ON INDIA'S EAST COAST",
        "Severe Cyclonic Storm Akvan began its landfall on the Odisha "
        "coast, bringing heavy rain and winds of 90-100 km/h to Andhra "
        "Pradesh and Odisha, with several districts on alert for flooding.",
    ),
]

ALSO_LINE = (
    "Also: Houthi missile hits Riyadh's tallest tower  •  Iran escalates "
    "tanker attacks in the Strait of Hormuz  •  Nvidia faces California probe"
)
FOOTER = (
    "Sources: International Court of Justice  •  BBC  •  Reuters  •  AP  •  "
    "The New York Times  —  Drawn by code, 20 November 2026"
)

# ---------------------------------------------------------------- helpers


def wrap(draw, text, fnt, max_width):
    """Greedy word wrap; returns a list of lines that fit max_width."""
    lines = []
    for paragraph in text.split("\n"):
        words = paragraph.split()
        current = ""
        for word in words:
            trial = (current + " " + word).strip()
            if draw.textlength(trial, font=fnt) <= max_width:
                current = trial
            else:
                if current:
                    lines.append(current)
                current = word
        if current:
            lines.append(current)
    return lines


def text_width(draw, text, fnt):
    return draw.textlength(text, font=fnt)


def draw_centered(draw, y, text, fnt, fill=INK):
    x = (PAGE_W - text_width(draw, text, fnt)) / 2
    draw.text((x, y), text, font=fnt, fill=fill)
    return y + fnt.size + 6


def draw_rule(draw, y, weight=2):
    draw.line([(MARGIN, y), (PAGE_W - MARGIN, y)], fill=INK, width=weight)


def draw_double_rule(draw, y):
    draw.line([(MARGIN, y), (PAGE_W - MARGIN, y)], fill=INK, width=3)
    draw.line([(MARGIN, y + 5), (PAGE_W - MARGIN, y + 5)], fill=INK, width=1)


def split_half(text):
    """Split a body paragraph into two near-equal halves by word count."""
    words = text.split()
    half = len(words) // 2
    return " ".join(words[:half]), " ".join(words[half:])


# ---------------------------------------------------------------- drawing


def build_page():
    img = Image.new("RGB", (PAGE_W, PAGE_H), PAPER)
    draw = ImageDraw.Draw(img)
    content_w = PAGE_W - 2 * MARGIN
    y = 26

    # Masthead
    y = draw_centered(draw, y, MASTHEAD, F_MASTHEAD)
    y += 2
    draw_double_rule(draw, y)
    y += 12

    # Dateline row
    draw.text((MARGIN, y), DATE_LINE, font=F_DATE, fill=INK)
    right_w = text_width(draw, DATE_RIGHT, F_DATE)
    draw.text((PAGE_W - MARGIN - right_w, y), DATE_RIGHT, font=F_DATE, fill=INK)
    y += 26
    draw_rule(draw, y, 1)
    y += 14

    # Lead kicker
    y = draw_centered(draw, y, LEAD_KICKER, F_KICKER)
    y += 4

    # Lead headline, centered, wrapped
    head_lines = wrap(draw, LEAD_HEADLINE, F_HEADLINE, content_w)
    for line in head_lines:
        y = draw_centered(draw, y, line, F_HEADLINE)
    y += 2

    # Lead deck, centered, wrapped
    deck_lines = wrap(draw, LEAD_DECK, F_DECK, content_w - 60)
    for line in deck_lines:
        y = draw_centered(draw, y, line, F_DECK)
    y += 8

    # Lead body in two columns
    col_w = (content_w - 24) // 2
    left_text, right_text = split_half(LEAD_BODY)
    left_lines = wrap(draw, left_text, F_BODY, col_w)
    right_lines = wrap(draw, right_text, F_BODY, col_w)
    body_top = y
    line_h = 26
    for i, line in enumerate(left_lines):
        draw.text((MARGIN, body_top + i * line_h), line, font=F_BODY, fill=INK)
    for i, line in enumerate(right_lines):
        draw.text(
            (MARGIN + col_w + 24, body_top + i * line_h),
            line,
            font=F_BODY,
            fill=INK,
        )
    y = body_top + max(len(left_lines), len(right_lines)) * line_h + 10

    # Section divider
    draw_rule(draw, y, 2)
    y += 12
    draw.text((MARGIN, y), "MORE FROM AROUND THE WORLD", font=F_LABEL, fill=GREY)
    y += 26

    # Secondary stories: two columns, two stories each
    col_x = [MARGIN, MARGIN + col_w + 24]
    grid_top = y
    row_h = 0
    for idx, (headline, body) in enumerate(SECONDARIES):
        col = idx % 2
        row = idx // 2
        x = col_x[col]
        sy = grid_top + row * 148
        head_lines = wrap(draw, headline, F_SUBHEAD, col_w)
        hy = sy
        for line in head_lines:
            draw.text((x, hy), line, font=F_SUBHEAD, fill=INK)
            hy += 29
        body_lines = wrap(draw, body, F_SUBBODY, col_w)
        by = hy + 2
        for line in body_lines[:4]:
            draw.text((x, by), line, font=F_SUBBODY, fill=INK)
            by += 22
        row_h = max(row_h, by - sy)
    y = grid_top + 2 * 148 + 4

    # Also line
    draw_rule(draw, y, 1)
    y += 8
    also_lines = wrap(draw, ALSO_LINE, F_ALSO, content_w)
    for line in also_lines:
        y = draw_centered(draw, y, line, F_ALSO)
    y += 2

    # Footer
    draw_rule(draw, y, 1)
    y += 8
    foot_lines = wrap(draw, FOOTER, F_FOOT, content_w)
    for line in foot_lines:
        y = draw_centered(draw, y, line, F_FOOT, fill=GREY)

    return img


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", ".")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.png")
    page = build_page()
    page.save(out_path, "PNG")
    with open(out_path, "rb") as handle:
        digest = hashlib.sha256(handle.read()).hexdigest()
    print("wrote", out_path)
    print("size", os.path.getsize(out_path), "bytes")
    print("sha256", digest)


if __name__ == "__main__":
    main()
