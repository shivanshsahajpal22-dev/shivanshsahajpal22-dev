from pathlib import Path

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
    lines.append(("boot", s))
for s in octocat:
    lines.append(("art", s))
for s in name:
    lines.append(("name", s))
for s in footer:
    if s.startswith("root@") or s == "shivanshsahajpal22-dev":
        kind = "prompt"
    else:
        kind = "meta"
    lines.append((kind, s))

W, H = 900, 720
X = 36
Y0 = 34
LH = 16


def esc(t: str) -> str:
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


parts = []
parts.append(
    f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="terminal ascii identity">
  <defs>
    <pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse">
      <rect width="4" height="2" fill="#000" opacity="0.18"/>
    </pattern>
    <linearGradient id="glow" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#00ff41" stop-opacity="0.12"/>
      <stop offset="100%" stop-color="#00ff41" stop-opacity="0"/>
    </linearGradient>
  </defs>

  <rect width="100%" height="100%" rx="10" fill="#070806"/>
  <rect x="1" y="1" width="{W-2}" height="{H-2}" rx="9" fill="none" stroke="#1f2a1c" stroke-width="1.5"/>
  <rect x="1" y="1" width="{W-2}" height="28" rx="9" fill="#10140f"/>
  <rect x="1" y="22" width="{W-2}" height="8" fill="#10140f"/>
  <circle cx="18" cy="15" r="5" fill="#ff5c4d"/>
  <circle cx="34" cy="15" r="5" fill="#ffb300"/>
  <circle cx="50" cy="15" r="5" fill="#3ddc84"/>
  <text x="70" y="19" fill="#6e7b68" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="11">root@offsec: ~/identity — bash</text>

  <rect x="8" y="34" width="{W-16}" height="{H-42}" rx="4" fill="url(#glow)"/>
'''
)

parts.append(
    """  <style>
    .t { font-family: ui-monospace, 'JetBrains Mono', 'IBM Plex Mono', SFMono-Regular, Menlo, Consolas, monospace; white-space: pre; }
    .boot { fill: #8a9a82; font-size: 12px; }
    .art  { fill: #3ddc84; font-size: 12.5px; font-weight: 700; }
    .name { fill: #ffb300; font-size: 13.5px; font-weight: 700; }
    .meta { fill: #c8d4c0; font-size: 12.5px; }
    .prompt { fill: #ffb300; font-size: 12.5px; }
    .who { fill: #3ddc84; font-size: 12.5px; font-weight: 700; }
    .cursor { fill: #3ddc84; }
  </style>
"""
)

delay = 0.12
step = 0.07
for i, (kind, s) in enumerate(lines):
    y = Y0 + 22 + i * LH
    begin = round(delay + i * step, 3)
    cls = "who" if s == "shivanshsahajpal22-dev" else kind
    parts.append(
        f'  <text class="t {cls}" x="{X}" y="{y}" xml:space="preserve" opacity="0">{esc(s)}'
        f'<animate attributeName="opacity" from="0" to="1" begin="{begin}s" dur="0.08s" fill="freeze"/>'
        f"</text>\n"
    )

last_y = Y0 + 22 + (len(lines) - 1) * LH
cursor_begin = round(delay + (len(lines) - 1) * step + 0.2, 3)
parts.append(
    f'''
  <rect class="cursor" x="{X}" y="{last_y + 8}" width="8" height="13" opacity="0">
    <animate attributeName="opacity" values="0;1;1;0;0" keyTimes="0;0.02;0.5;0.52;1" dur="1s" begin="{cursor_begin}s" repeatCount="indefinite"/>
  </rect>

  <rect width="100%" height="100%" fill="url(#scan)" pointer-events="none" opacity="0.35"/>
</svg>
'''
)

out = Path(__file__).with_name("github-ascii.svg")
out.write_text("".join(parts), encoding="utf-8")
print(f"wrote {out} ({out.stat().st_size} bytes, {len(lines)} lines)")
