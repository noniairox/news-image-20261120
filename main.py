"""The World Today - 20 November 2026 front page.

Renders a single 1024x1024 newspaper front page as a PNG. All text is
drawn with a self-contained 5x8 bitmap font defined in this file: no
system fonts, no network, no timestamps, no randomness. The output is
fully deterministic: the same pixels on every run.

Usage: MAKEFUN_OUTPUT_DIR=<dir> python3 -P -s main.py
Writes <dir>/entry.png and prints its size and sha256.
"""

import hashlib
import os

from PIL import Image, ImageDraw

W, H = 1024, 1024
PAPER = (255, 255, 255)
INK = (17, 17, 17)

# 5x8 bitmap font. Each glyph is 8 rows of 5 cells ('#' ink, '.' blank).
# Row 7 is the descender row (g, j, p, q, y). The 'g' is single-storey:
# a closed bowl at x-height (rows 2-5) and an open lower bowl with a
# hook curving left (rows 6-7), so it reads as 'g', never as '9' or 's'.
FONT = {
    "A": (
        ".###.",
        "#...#",
        "#...#",
        "#####",
        "#...#",
        "#...#",
        "#...#",
        ".....",
    ),
    "B": (
        "####.",
        "#...#",
        "#...#",
        "####.",
        "#...#",
        "#...#",
        "####.",
        ".....",
    ),
    "C": (
        ".####",
        "#....",
        "#....",
        "#....",
        "#....",
        "#....",
        ".####",
        ".....",
    ),
    "D": (
        "####.",
        "#...#",
        "#...#",
        "#...#",
        "#...#",
        "#...#",
        "####.",
        ".....",
    ),
    "E": (
        "#####",
        "#....",
        "#....",
        "####.",
        "#....",
        "#....",
        "#####",
        ".....",
    ),
    "F": (
        "#####",
        "#....",
        "#....",
        "####.",
        "#....",
        "#....",
        "#....",
        ".....",
    ),
    "G": (
        ".####",
        "#....",
        "#....",
        "#.###",
        "#...#",
        "#...#",
        ".###.",
        ".....",
    ),
    "H": (
        "#...#",
        "#...#",
        "#...#",
        "#####",
        "#...#",
        "#...#",
        "#...#",
        ".....",
    ),
    "I": (
        ".###.",
        "..#..",
        "..#..",
        "..#..",
        "..#..",
        "..#..",
        ".###.",
        ".....",
    ),
    "J": (
        "..###",
        "...#.",
        "...#.",
        "...#.",
        "...#.",
        "#..#.",
        ".##..",
        ".....",
    ),
    "K": (
        "#...#",
        "#..#.",
        "#.#..",
        "##...",
        "#.#..",
        "#..#.",
        "#...#",
        ".....",
    ),
    "L": (
        "#....",
        "#....",
        "#....",
        "#....",
        "#....",
        "#....",
        "#####",
        ".....",
    ),
    "M": (
        "#...#",
        "##.##",
        "#.#.#",
        "#.#.#",
        "#...#",
        "#...#",
        "#...#",
        ".....",
    ),
    "N": (
        "#...#",
        "##..#",
        "#.#.#",
        "#..##",
        "#...#",
        "#...#",
        "#...#",
        ".....",
    ),
    "O": (
        ".###.",
        "#...#",
        "#...#",
        "#...#",
        "#...#",
        "#...#",
        ".###.",
        ".....",
    ),
    "P": (
        "####.",
        "#...#",
        "#...#",
        "####.",
        "#....",
        "#....",
        "#....",
        ".....",
    ),
    "Q": (
        ".###.",
        "#...#",
        "#...#",
        "#...#",
        "#.#.#",
        "#..#.",
        ".##.#",
        ".....",
    ),
    "R": (
        "####.",
        "#...#",
        "#...#",
        "####.",
        "#.#..",
        "#..#.",
        "#...#",
        ".....",
    ),
    "S": (
        ".####",
        "#....",
        "#....",
        ".###.",
        "....#",
        "....#",
        "####.",
        ".....",
    ),
    "T": (
        "#####",
        "..#..",
        "..#..",
        "..#..",
        "..#..",
        "..#..",
        "..#..",
        ".....",
    ),
    "U": (
        "#...#",
        "#...#",
        "#...#",
        "#...#",
        "#...#",
        "#...#",
        ".###.",
        ".....",
    ),
    "V": (
        "#...#",
        "#...#",
        "#...#",
        "#...#",
        "#...#",
        ".#.#.",
        "..#..",
        ".....",
    ),
    "W": (
        "#...#",
        "#...#",
        "#...#",
        "#.#.#",
        "#.#.#",
        "##.##",
        "#...#",
        ".....",
    ),
    "X": (
        "#...#",
        "#...#",
        ".#.#.",
        "..#..",
        ".#.#.",
        "#...#",
        "#...#",
        ".....",
    ),
    "Y": (
        "#...#",
        "#...#",
        ".#.#.",
        "..#..",
        "..#..",
        "..#..",
        "..#..",
        ".....",
    ),
    "Z": (
        "#####",
        "....#",
        "...#.",
        "..#..",
        ".#...",
        "#....",
        "#####",
        ".....",
    ),
    "a": (
        ".....",
        ".....",
        ".###.",
        "....#",
        ".####",
        "#...#",
        ".####",
        ".....",
    ),
    "b": (
        "#....",
        "#....",
        "####.",
        "#...#",
        "#...#",
        "#...#",
        "####.",
        ".....",
    ),
    "c": (
        ".....",
        ".....",
        ".####",
        "#....",
        "#....",
        "#....",
        ".####",
        ".....",
    ),
    "d": (
        "....#",
        "....#",
        ".####",
        "#...#",
        "#...#",
        "#...#",
        ".####",
        ".....",
    ),
    "e": (
        ".....",
        ".....",
        ".###.",
        "#...#",
        "#####",
        "#....",
        ".###.",
        ".....",
    ),
    "f": (
        "..##.",
        ".#...",
        "#....",
        "####.",
        "#....",
        "#....",
        "#....",
        ".....",
    ),
    "g": (
        ".....",
        ".....",
        ".###.",
        "#...#",
        "#...#",
        ".###.",
        ".#.##",
        ".##..",
    ),
    "h": (
        "#....",
        "#....",
        "####.",
        "#...#",
        "#...#",
        "#...#",
        "#...#",
        ".....",
    ),
    "i": (
        ".....",
        "..#..",
        ".....",
        "..#..",
        "..#..",
        "..#..",
        ".###.",
        ".....",
    ),
    "j": (
        ".....",
        "...#.",
        ".....",
        "...#.",
        "...#.",
        "...#.",
        "...#.",
        ".##..",
    ),
    "k": (
        "#....",
        "#....",
        "#.#..",
        "##...",
        "#.#..",
        "#..#.",
        "#...#",
        ".....",
    ),
    "l": (
        ".#...",
        ".#...",
        ".#...",
        ".#...",
        ".#...",
        ".#...",
        ".###.",
        ".....",
    ),
    "m": (
        ".....",
        ".....",
        "##.##",
        "#.#.#",
        "#.#.#",
        "#.#.#",
        "#.#.#",
        ".....",
    ),
    "n": (
        ".....",
        ".....",
        "####.",
        "#...#",
        "#...#",
        "#...#",
        "#...#",
        ".....",
    ),
    "o": (
        ".....",
        ".....",
        ".###.",
        "#...#",
        "#...#",
        "#...#",
        ".###.",
        ".....",
    ),
    "p": (
        ".....",
        ".....",
        "####.",
        "#...#",
        "#...#",
        "####.",
        "#....",
        "#....",
    ),
    "q": (
        ".....",
        ".....",
        ".###.",
        "#...#",
        "#...#",
        ".###.",
        "....#",
        "....#",
    ),
    "r": (
        ".....",
        ".....",
        "#.##.",
        "##...",
        "#....",
        "#....",
        "#....",
        ".....",
    ),
    "s": (
        ".....",
        ".....",
        ".####",
        "#....",
        ".###.",
        "....#",
        "####.",
        ".....",
    ),
    "t": (
        ".#...",
        ".#...",
        "####.",
        ".#...",
        ".#...",
        ".#...",
        ".##..",
        ".....",
    ),
    "u": (
        ".....",
        ".....",
        "#...#",
        "#...#",
        "#...#",
        "#...#",
        ".###.",
        ".....",
    ),
    "v": (
        ".....",
        ".....",
        "#...#",
        "#...#",
        "#...#",
        ".#.#.",
        "..#..",
        ".....",
    ),
    "w": (
        ".....",
        ".....",
        "#...#",
        "#.#.#",
        "#.#.#",
        "#.#.#",
        ".#.#.",
        ".....",
    ),
    "x": (
        ".....",
        ".....",
        "#...#",
        ".#.#.",
        "..#..",
        ".#.#.",
        "#...#",
        ".....",
    ),
    "y": (
        ".....",
        ".....",
        "#...#",
        "#...#",
        "#...#",
        ".###.",
        "...#.",
        ".##..",
    ),
    "z": (
        ".....",
        ".....",
        "#####",
        "...#.",
        "..#..",
        ".#...",
        "#####",
        ".....",
    ),
    "0": (
        ".###.",
        "#...#",
        "#..##",
        "#.#.#",
        "##..#",
        "#...#",
        ".###.",
        ".....",
    ),
    "1": (
        "..#..",
        ".##..",
        "..#..",
        "..#..",
        "..#..",
        "..#..",
        ".###.",
        ".....",
    ),
    "2": (
        ".###.",
        "#...#",
        "....#",
        "...#.",
        "..#..",
        ".#...",
        "#####",
        ".....",
    ),
    "3": (
        "####.",
        "....#",
        "....#",
        ".###.",
        "....#",
        "....#",
        "####.",
        ".....",
    ),
    "4": (
        "...#.",
        "..##.",
        ".#.#.",
        "#..#.",
        "#####",
        "...#.",
        "...#.",
        ".....",
    ),
    "5": (
        "#####",
        "#....",
        "####.",
        "....#",
        "....#",
        "#...#",
        ".###.",
        ".....",
    ),
    "6": (
        ".###.",
        "#....",
        "#....",
        "####.",
        "#...#",
        "#...#",
        ".###.",
        ".....",
    ),
    "7": (
        "#####",
        "....#",
        "...#.",
        "..#..",
        "..#..",
        "..#..",
        "..#..",
        ".....",
    ),
    "8": (
        ".###.",
        "#...#",
        "#...#",
        ".###.",
        "#...#",
        "#...#",
        ".###.",
        ".....",
    ),
    "9": (
        ".###.",
        "#...#",
        "#...#",
        ".####",
        "....#",
        "....#",
        ".###.",
        ".....",
    ),
    ".": (
        ".....",
        ".....",
        ".....",
        ".....",
        ".....",
        ".....",
        ".##..",
        ".....",
    ),
    ",": (
        ".....",
        ".....",
        ".....",
        ".....",
        ".....",
        ".....",
        ".##..",
        ".#...",
    ),
    "'": (
        "..#..",
        "..#..",
        ".#...",
        ".....",
        ".....",
        ".....",
        ".....",
        ".....",
    ),
    "-": (
        ".....",
        ".....",
        ".....",
        ".###.",
        ".....",
        ".....",
        ".....",
        ".....",
    ),
    ":": (
        ".....",
        ".....",
        ".##..",
        ".....",
        ".....",
        ".##..",
        ".....",
        ".....",
    ),
    ";": (
        ".....",
        ".....",
        ".##..",
        ".....",
        ".....",
        ".##..",
        ".#...",
        ".....",
    ),
    "(": (
        "...#.",
        "..#..",
        ".#...",
        ".#...",
        ".#...",
        "..#..",
        "...#.",
        ".....",
    ),
    ")": (
        ".#...",
        "..#..",
        "...#.",
        "...#.",
        "...#.",
        "..#..",
        ".#...",
        ".....",
    ),
    "%": (
        "##...",
        "##...",
        "...#.",
        "..#..",
        ".#...",
        "...##",
        "...##",
        ".....",
    ),
    "$": (
        "..#..",
        ".####",
        "#.#..",
        ".###.",
        "..#.#",
        "####.",
        "..#..",
        ".....",
    ),
    "+": (
        ".....",
        ".....",
        "..#..",
        "..#..",
        "#####",
        "..#..",
        "..#..",
        ".....",
    ),
    "/": (
        "....#",
        "...#.",
        "...#.",
        "..#..",
        "..#..",
        ".#...",
        "#....",
        ".....",
    ),
    "|": (
        "..#..",
        "..#..",
        "..#..",
        "..#..",
        "..#..",
        "..#..",
        "..#..",
        ".....",
    ),
    "!": (
        "..#..",
        "..#..",
        "..#..",
        "..#..",
        "..#..",
        ".....",
        "..#..",
        ".....",
    ),
    "?": (
        ".###.",
        "#...#",
        "....#",
        "...#.",
        "..#..",
        ".....",
        "..#..",
        ".....",
    ),
    "=": (
        ".....",
        ".....",
        "#####",
        ".....",
        "#####",
        ".....",
        ".....",
        ".....",
    ),
    '"': (
        ".#.#.",
        ".#.#.",
        ".....",
        ".....",
        ".....",
        ".....",
        ".....",
        ".....",
    ),
    " ": (
        ".....",
        ".....",
        ".....",
        ".....",
        ".....",
        ".....",
        ".....",
        ".....",
    ),
}


def text_width(text, scale):
    """Pixel width of text at the given scale (no trailing advance)."""
    if not text:
        return 0
    return len(text) * 6 * scale - scale


def draw_text(d, x, y, text, scale, ink=INK):
    """Draw text left-aligned at (x, y); returns the pixel width drawn."""
    cx = x
    for ch in text:
        glyph = FONT.get(ch, FONT[" "])
        for r, row in enumerate(glyph):
            for c, bit in enumerate(row):
                if bit == "#":
                    d.rectangle(
                        [
                            cx + c * scale,
                            y + r * scale,
                            cx + (c + 1) * scale - 1,
                            y + (r + 1) * scale - 1,
                        ],
                        fill=ink,
                    )
        cx += 6 * scale
    return cx - scale - x


def draw_centered(d, cx, y, text, scale, ink=INK):
    draw_text(d, cx - text_width(text, scale) // 2, y, text, scale, ink)


def wrap(text, scale, max_w):
    """Word-wrap text to lines no wider than max_w at the given scale."""
    lines = []
    cur = ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if text_width(trial, scale) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(d, x, y, text, scale, max_w, leading, ink=INK):
    """Draw word-wrapped text; returns the number of lines drawn."""
    lines = wrap(text, scale, max_w)
    for i, line in enumerate(lines):
        draw_text(d, x, y + i * leading, line, scale, ink)
    return len(lines)


MASTHEAD = "THE WORLD TODAY"
DATE_LINE = "Friday, 20 November 2026"
HEADLINE = [
    "ICJ RULES MYANMAR",
    "COMMITTED GENOCIDE",
    "AGAINST THE ROHINGYA",
]
DECK = "A 9-6 verdict in The Hague finds Myanmar breached the Genocide Convention"
LEAD = (
    "The International Court of Justice ruled on Thursday that Myanmar "
    "committed genocide against the Rohingya. Judges found mass killings, "
    "systematic rape and the burning of hundreds of villages in a 2017 "
    "campaign aimed at destroying the group, the findings said. The court "
    "found Myanmar guilty of violating the Genocide Convention. The 9-6 "
    "ruling is binding. More than 700,000 Rohingya fled to Bangladesh. "
    "Myanmar denies the charges and says its operations targeted militants."
)
VERDICT_LINE1 = "9-6 | 700,000+ ROHINGYA FLED SINCE 2017"
VERDICT_LINE2 = "THE VERDICT, READ IN THE HAGUE"
SUBS = [
    (
        "ANTHROPIC SOARS 17% ON $81.3BN IPO DEBUT",
        "Shares jumped 17 percent in the year's biggest listing.",
    ),
    (
        "TRUMP, XI AND PUTIN AGREE PEACE PLAN IN SHENZHEN",
        "The three leaders signed a joint declaration at the APEC summit.",
    ),
    (
        "UKRAINE HITS CRIMEAN BRIDGE FOR THIRD TIME",
        "Kyiv said the strike shut the crossing again, bringing new pressure.",
    ),
    (
        "CYCLONE AKVAN SLAMS INTO ODISHA COAST",
        "Winds of 90 to 100 km/h tore roofs from homes as people fled to shelter.",
    ),
]
MORE_HEAD = "MORE FROM AROUND THE WORLD"
MORE_ITEMS = [
    "Houthi missile hits Riyadh's tallest tower.",
    "Iran escalates Hormuz tanker attacks.",
    "Nvidia faces California probe.",
]
FOOTER = "THE WORLD TODAY - 20 NOVEMBER 2026 - PAGE 1"


def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Page border.
    d.rectangle([14, 14, W - 15, H - 15], outline=INK, width=2)

    # Masthead.
    draw_centered(d, W // 2, 34, MASTHEAD, 8)

    # Date line.
    draw_centered(d, W // 2, 112, DATE_LINE, 3)

    # Thick rule under the date line.
    d.rectangle([36, 140, W - 37, 143], fill=INK)

    # Headline, three lines.
    hy = 158
    for line in HEADLINE:
        draw_centered(d, W // 2, hy, line, 5)
        hy += 48

    # Deck.
    draw_centered(d, W // 2, 312, DECK, 2)

    # Rule under the deck.
    d.rectangle([36, 340, W - 37, 341], fill=INK)

    # Lead body, three columns.
    col_w = 300
    col_x = [36, 360, 684]
    body_lines = wrap(LEAD, 2, col_w)
    per_col = (len(body_lines) + 2) // 3
    for ci, x in enumerate(col_x):
        chunk = body_lines[ci * per_col:(ci + 1) * per_col]
        for i, line in enumerate(chunk):
            draw_text(d, x, 356 + i * 21, line, 2)

    # Verdict strip: black band, white text.
    d.rectangle([36, 538, W - 37, 592], fill=INK)
    draw_centered(d, W // 2, 546, VERDICT_LINE1, 3, ink=PAPER)
    draw_centered(d, W // 2, 574, VERDICT_LINE2, 2, ink=PAPER)

    # Rule above the sub-stories.
    d.rectangle([36, 606, W - 37, 607], fill=INK)

    # Sub-stories, 2x2 grid.
    cell_x = [36, 528]
    cell_w = 460
    row_y = [620, 740]
    for idx, (head, body) in enumerate(SUBS):
        x = cell_x[idx % 2]
        y = row_y[idx // 2]
        n_head = draw_wrapped(d, x, y, head, 2, cell_w, 21)
        draw_wrapped(d, x, y + n_head * 21 + 6, body, 2, cell_w, 21)
    # Dividers between the sub-story cells.
    d.rectangle([511, 618, 512, 838], fill=INK)
    d.rectangle([36, 729, W - 37, 730], fill=INK)

    # More from around the world.
    draw_text(d, 36, 856, MORE_HEAD, 2)
    my = 882
    for item in MORE_ITEMS:
        d.rectangle([36, my + 5, 41, my + 10], fill=INK)
        draw_text(d, 52, my, item, 2)
        my += 21

    # Footer.
    d.rectangle([36, 946, W - 37, 947], fill=INK)
    draw_centered(d, W // 2, 958, FOOTER, 2)

    return img


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", ".")
    os.makedirs(out_dir, exist_ok=True)
    img = render()
    path = os.path.join(out_dir, "entry.png")
    img.save(path, "PNG")
    data = open(path, "rb").read()
    print("wrote " + path)
    print("size " + str(len(data)) + " bytes")
    print("sha256 " + hashlib.sha256(data).hexdigest())


if __name__ == "__main__":
    main()
