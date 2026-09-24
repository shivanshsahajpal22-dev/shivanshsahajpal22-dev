#!/usr/bin/env python3
"""Terminal typewriter GIF: clean identity + boot sequence (no mask)."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"

# Cool, dark, desaturated — not neon / not warm amber
BG = (5, 8, 12)
CHROME = (10, 16, 22)
BORDER = (26, 40, 54)
DIM = (74, 102, 118)
CYAN = (86, 176, 214)       # cooler ice cyan
ICE = (168, 214, 232)       # cool body text
MASK = (120, 188, 255)      # cool fsociety mask cyan
RED = (70, 28, 42)          # dark window buttons, not candy
YELLOW = (42, 78, 108)      # cool steel, not warm
OK = (28, 132, 176)         # cool scanline accent
CURSOR = (86, 176, 214)

W, H = 820, 578
PAD_X = 24
PAD_Y = 44
LH = 15
FS = 12

# mask removed: terminal GIF is now clean identity + boot/apt sequence only.
mask = []

name = [
    "   root@fsociety:~$",
    "   Shivansh Sahajpal",
    "   (ready to execute)",
    "",
]

boot = [
    "[*] hello, friend.",
    "[*] loading operator profile .............. OK",
    "[*] initializing toolchain ............... OK",
    "[*] sudo apt update ........................ OK",
    "[*] installing: nmap burpsuite sqlmap .... OK",
    "[*] ready to go now..",
    "",
]


footer = [
    "",
    "  [ PROFESSIONAL HACKER ]   [ TOOL DESIGNER ]",
    "  building offensive tooling  |  write-ups: rare",
    "",
    "root@fsociety:~$ whoami",
    "shivanshsahajpal22-dev",
]

lines = []
for s in boot:
    if s.startswith("[*]"):
        lines.append((s, DIM))
    else:
        lines.append((s, CYAN))
# mask removed
# (intentionally no mask lines added)
for s in name:
    lines.append((s, CYAN))
for s in footer:
    if s.startswith("root@"):
        lines.append((s, CYAN))
    elif s == "shivanshsahajpal22-dev":
        lines.append((s, ICE))
    else:
        lines.append((s, ICE))


def chrome(draw, font_ui):
    draw.rounded_rectangle((1, 1, W - 2, H - 2), radius=10, outline=BORDER, width=1)
    draw.rounded_rectangle((1, 1, W - 2, 28), radius=10, fill=CHROME)
    draw.rectangle((1, 18, W - 2, 28), fill=CHROME)
    draw.ellipse((12, 9, 22, 19), fill=RED)
    draw.ellipse((28, 9, 38, 19), fill=YELLOW)
    draw.ellipse((44, 9, 54, 19), fill=OK)
    draw.text((66, 8), "root@fsociety: ~/identity \u2014 bash", font=font_ui, fill=DIM)


def paint_lines(draw, font, font_b, upto):
    for i, (text, color) in enumerate(lines[:upto]):
        y = PAD_Y + i * LH
        use = font_b if color in (MASK, CYAN) and not text.startswith("[*]") else font
        draw.text((PAD_X, y), text, font=use, fill=color)


def main():
    # Render: mask only (no extra banner text).
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
    durations.append(220)

    for n in range(1, len(lines) + 1):
        img, draw = new_frame()
        paint_lines(draw, font, font_b, n)
        last = lines[n - 1][0]
        tw = draw.textlength(last, font=font)
        cy = PAD_Y + (n - 1) * LH
        draw.rectangle((PAD_X + int(tw) + 2, cy + 1, PAD_X + int(tw) + 8, cy + FS), fill=CURSOR)
        frames.append(img)
        durations.append(60)

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
    print(f"wrote {out} ({out.stat().st_size / 1024:.1f} KB, {len(qframes)} frames, H={H}, lines={len(lines)}")
    last_y = PAD_Y + len(lines) * LH
    print(f"last text y~{last_y} canvas H={H}")


if __name__ == "__main__":
    main()
