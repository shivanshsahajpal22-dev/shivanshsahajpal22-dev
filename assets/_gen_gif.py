#!/usr/bin/env python3
"""Render a terminal typewriter GIF of the GitHub/octocat ASCII banner."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"

BG = (7, 8, 6)
CHROME = (16, 20, 15)
BORDER = (31, 42, 28)
DIM = (138, 154, 130)
GREEN = (61, 220, 132)
AMBER = (255, 179, 0)
TEXT = (200, 212, 192)
RED = (255, 92, 77)
YELLOW = (255, 179, 0)
OK = (61, 220, 132)

W, H = 820, 600
PAD_X = 24
PAD_Y = 44
LH = 14
FS = 12

octocat = [
    "           MMM.           .MMM",
    "           MMMMMMMMMMMMMMMMMMM",
    "           MMMMMMMMMMMMMMMMMMM",
    "          MMMMMMMMMMMMMMMMMMMMM",
    "         MMMMMMMMMMMMMMMMMMMMMMM",
    "        MMMMMMMMMMMMMMMMMMMMMMMMM",
    "        MMMM::- -:::::::- -::MMMM",
    "         MM~:~ 00~:::::~ 00~:~MM",
    "    .. MMMMM::.00:::+:::.00::MMMMM ..",
    "          .MM::::: ._. :::::MM.",
    "             MMMM;:::::;MMMM",
    "      -MM        MMMMMMM",
    "      ^  M+     MMMMMMMMM",
    "          MMMMMMM MM MM MM",
    "               MM MM MM MM",
    "               MM MM MM MM",
    "            .~~MM~MM~MM~~.",
    "         ~~~~MMMMMMMMMMM~~~~",
    "        ~~~~MMMMMMMMMMMMM~~~~",
    "       ~~~~MMMMMMMMMMMMMMM~~~~",
]

name = [
    "   _____ __  _______    _____    _   _______ __  __",
    "  / ___// / / /  _/ |  / /   |  / | / / ___// / / /",
    r"  \__ \/ /_/ // / | | / / /| | /  |/ /\__ \/ /_/ /",
    " ___/ / __  // /  | |/ / ___ |/ /|  /___/ / __  /",
    "/____/_/ /_/___/  |___/_/  |_/_/ |_//____/_/ /_/",
]

boot = [
    "root@offsec:~$ ./identify.sh",
    "[*] loading operator profile .............. OK",
    "[*] mounting tool chain ................... OK",
    "[*] dropping ascii payload ................ OK",
    "",
]

footer = [
    "",
    "  [ PROFESSIONAL HACKER ]   [ TOOL DESIGNER ]",
    "  building offensive tooling  |  write-ups: rare",
    "",
    "root@offsec:~$ whoami",
    "shivanshsahajpal22-dev",
]

lines = []
for s in boot:
    lines.append((s, DIM if s.startswith("[*]") else AMBER))
for s in octocat:
    lines.append((s, GREEN))
for s in name:
    lines.append((s, AMBER))
for s in footer:
    if s.startswith("root@"):
        lines.append((s, AMBER))
    elif s == "shivanshsahajpal22-dev":
        lines.append((s, GREEN))
    else:
        lines.append((s, TEXT))


def chrome(draw, font_ui):
    draw.rounded_rectangle((1, 1, W - 2, H - 2), radius=10, outline=BORDER, width=1)
    draw.rounded_rectangle((1, 1, W - 2, 28), radius=10, fill=CHROME)
    draw.rectangle((1, 18, W - 2, 28), fill=CHROME)
    draw.ellipse((12, 9, 22, 19), fill=RED)
    draw.ellipse((28, 9, 38, 19), fill=YELLOW)
    draw.ellipse((44, 9, 54, 19), fill=OK)
    draw.text((66, 8), "root@offsec: ~/identity \u2014 bash", font=font_ui, fill=DIM)


def paint_lines(draw, font, font_b, upto):
    for i, (text, color) in enumerate(lines[:upto]):
        y = PAD_Y + i * LH
        use = font_b if color in (GREEN, AMBER) and not text.startswith("[*]") else font
        draw.text((PAD_X, y), text, font=use, fill=color)


def main():
    font = ImageFont.truetype(FONT, FS)
    font_ui = ImageFont.truetype(FONT, 11)
    font_b = ImageFont.truetype(FONT_BOLD, FS)

    frames = []
    durations = []

    def new_frame():
        img = Image.new("RGB", (W, H), BG)
        draw = ImageDraw.Draw(img)
        chrome(draw, font_ui)
        return img, draw

    blank, _ = new_frame()
    frames.append(blank)
    durations.append(200)

    for n in range(1, len(lines) + 1):
        img, draw = new_frame()
        paint_lines(draw, font, font_b, n)
        last = lines[n - 1][0]
        tw = draw.textlength(last, font=font)
        cy = PAD_Y + (n - 1) * LH
        draw.rectangle((PAD_X + int(tw) + 2, cy + 1, PAD_X + int(tw) + 8, cy + FS), fill=GREEN)
        frames.append(img)
        durations.append(65)

    on = frames[-1]
    off, draw = new_frame()
    paint_lines(draw, font, font_b, len(lines))
    for _ in range(5):
        frames.append(on)
        durations.append(450)
        frames.append(off)
        durations.append(450)

    palette_src = frames[-2].quantize(colors=24, method=Image.Quantize.MEDIANCUT)
    qframes = [f.quantize(palette=palette_src, dither=Image.Dither.NONE) for f in frames]

    out = Path(__file__).with_name("github-ascii.gif")
    qframes[0].save(
        out,
        save_all=True,
        append_images=qframes[1:],
        duration=durations,
        loop=0,
        optimize=True,
        disposal=2,
    )
    print(f"wrote {out} ({out.stat().st_size / 1024:.1f} KB, {len(qframes)} frames)")


if __name__ == "__main__":
    main()
