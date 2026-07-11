"""
Generate an animated terminal-style SVG for GitHub profile README.
Uses SMIL animations (<animate> tags) which GitHub reliably supports.
ASCII art on the left, terminal info typing in on the right.
"""
import html
import os

BASEDIR = os.path.dirname(__file__)
BG_COLOR = "#0d1117"
TEXT_COLOR = "#8b949e"
HIGHLIGHT_COLOR = "#c9d1d9"
ACCENT_COLOR = "#58a6ff"
DOT_COLOR = "#151b23"


def generate_combined_svg():
    """Generate an animated terminal SVG with SMIL animations."""
    input_file = os.path.join(BASEDIR, "ascii_final.txt")
    output_file = os.path.join(BASEDIR, "terminal_hero.svg")

    # --- Read ASCII art ---
    with open(input_file, "r", encoding="utf-8") as f:
        ascii_lines = [line.rstrip('\n').rstrip('\r') for line in f.readlines()]

    # --- ASCII art sizing ---
    ascii_font = 5.2
    ascii_lh = 6.8
    ascii_cw = 3.1
    ascii_max_len = max(len(line) for line in ascii_lines)
    ascii_block_w = int(ascii_max_len * ascii_cw)
    ascii_block_h = int(len(ascii_lines) * ascii_lh)

    # --- Info panel content ---
    info_lines = [
        [("$ ", ACCENT_COLOR), ("whoami", HIGHLIGHT_COLOR)],
        [("  Arinjay Sarkar", HIGHLIGHT_COLOR)],
        [],
        [("$ ", ACCENT_COLOR), ("cat ", HIGHLIGHT_COLOR), ("role.txt", ACCENT_COLOR)],
        [("  Instrumentation & Electronics @ JU", TEXT_COLOR)],
        [("  Data Science & Apps @ IIT Madras", TEXT_COLOR)],
        [],
        [("$ ", ACCENT_COLOR), ("ls ", HIGHLIGHT_COLOR), ("languages/", ACCENT_COLOR)],
        [("  Java  Python  C++  JavaScript  SQL", TEXT_COLOR)],
        [],
        [("$ ", ACCENT_COLOR), ("ls ", HIGHLIGHT_COLOR), ("ai-ml/", ACCENT_COLOR)],
        [("  PyTorch  LangChain  LightGBM  Groq", TEXT_COLOR)],
        [("  Computer Vision  RAG  Deep Learning", TEXT_COLOR)],
        [],
        [("$ ", ACCENT_COLOR), ("ls ", HIGHLIGHT_COLOR), ("frameworks/", ACCENT_COLOR)],
        [("  Spring Boot  Flask  FastAPI  Vue.js", TEXT_COLOR)],
        [],
        [("$ ", ACCENT_COLOR), ("ls ", HIGHLIGHT_COLOR), ("cloud/", ACCENT_COLOR)],
        [("  AWS (EC2, RDS, Lambda, S3)", TEXT_COLOR)],
        [("  Azure (Blob, Functions, AI Search)", TEXT_COLOR)],
        [],
        [("$ ", ACCENT_COLOR), ("ls ", HIGHLIGHT_COLOR), ("databases/", ACCENT_COLOR)],
        [("  PostgreSQL  MongoDB  pgvector  FAISS", TEXT_COLOR)],
        [],
        [("$ ", ACCENT_COLOR), ("ls ", HIGHLIGHT_COLOR), ("devops/", ACCENT_COLOR)],
        [("  Docker  Git  CI/CD  REST APIs", TEXT_COLOR)],
        [],
        [("$ ", ACCENT_COLOR), ("cat ", HIGHLIGHT_COLOR), ("experience.log", ACCENT_COLOR)],
        [("  [+] Research Intern @ ISI Kolkata", TEXT_COLOR)],
        [("  [+] SWE Intern (AI/ML) @ SETV Global", TEXT_COLOR)],
        [],
        [("$ ", ACCENT_COLOR), ("cat ", HIGHLIGHT_COLOR), ("achievements.log", ACCENT_COLOR)],
        [("  [*] LeetCode Knight  | Rating 1877", TEXT_COLOR)],
        [("  [*] Codeforces Specialist | 1200+", TEXT_COLOR)],
        [("  [*] Hacktoberfest Supercontributor", TEXT_COLOR)],
        [("  [*] AWS AI for Bharat | Finalist", TEXT_COLOR)],
        [("  [*] Google Cloud Arcade Legend Tier", TEXT_COLOR)],
        [],
        [("$ ", ACCENT_COLOR), ("cat ", HIGHLIGHT_COLOR), ("connect.txt", ACCENT_COLOR)],
        [("  LinkedIn ", TEXT_COLOR), (": ", "#30363d"), ("amiarinjaysarkar", ACCENT_COLOR)],
        [("  Email    ", TEXT_COLOR), (": ", "#30363d"), ("amiarinjaysarkar@gmail.com", ACCENT_COLOR)],
        [],
        [("$ ", ACCENT_COLOR), ("_", HIGHLIGHT_COLOR)],
    ]

    # --- Info panel sizing ---
    info_font = 11
    info_lh = 15
    info_cw = 6.6
    info_max_len = 0
    for lp in info_lines:
        ll = sum(len(t) for t, _ in lp)
        info_max_len = max(info_max_len, ll)
    info_block_w = int(info_max_len * info_cw)
    info_block_h = int(len(info_lines) * info_lh)

    # --- Overall layout ---
    pad = 20
    title_bar_h = 30
    gap = 30
    content_h = max(ascii_block_h, info_block_h)
    svg_width = pad + ascii_block_w + gap + info_block_w + pad
    svg_height = pad + title_bar_h + content_h + pad
    svg_width = max(svg_width, 850)

    # --- Animation timing ---
    ascii_appear = 0.5       # ASCII art appears at 0.5s
    ascii_dur = 1.0          # fades in over 1s
    line_delay = 0.18        # each info line appears 0.18s after previous
    info_start = 1.0         # info lines start appearing at 1s

    parts = []
    parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{svg_width}" height="{svg_height}" viewBox="0 0 {svg_width} {svg_height}">\n\n')

    # Background
    parts.append(f'  <rect width="100%" height="100%" fill="{BG_COLOR}" rx="10" ry="10"/>\n')
    parts.append(f'  <rect x="1" y="1" width="{svg_width-2}" height="{svg_height-2}" fill="none" stroke="#30363d" stroke-width="1" rx="10" ry="10"/>\n\n')

    # Terminal title bar
    parts.append(f'  <circle cx="20" cy="16" r="5" fill="#ff5f57"/>\n')
    parts.append(f'  <circle cx="36" cy="16" r="5" fill="#febc2e"/>\n')
    parts.append(f'  <circle cx="52" cy="16" r="5" fill="#28c840"/>\n')
    parts.append(
        f'  <text x="{svg_width // 2}" y="20" '
        f'font-family="Courier New,monospace" font-size="11px" '
        f'fill="#8b949e" text-anchor="middle">unknownar@github:~$</text>\n\n'
    )

    # Divider line under title bar
    parts.append(f'  <line x1="0" y1="{title_bar_h}" x2="{svg_width}" y2="{title_bar_h}" stroke="#30363d" stroke-width="0.5"/>\n\n')

    # --- ASCII art (left side) with SMIL fade-in ---
    ascii_start_x = pad
    ascii_start_y = pad + title_bar_h

    parts.append(f'  <g opacity="0">\n')
    parts.append(f'    <animate attributeName="opacity" from="0" to="1" begin="{ascii_appear}s" dur="{ascii_dur}s" fill="freeze"/>\n')

    for i, line in enumerate(ascii_lines):
        y = ascii_start_y + i * ascii_lh + ascii_font

        segments = []
        current_segment = ""
        current_is_dot = None
        for ch in line:
            is_dot = (ch == '.')
            if is_dot != current_is_dot and current_segment:
                segments.append((current_segment, current_is_dot))
                current_segment = ""
            current_segment += ch
            current_is_dot = is_dot
        if current_segment:
            segments.append((current_segment, current_is_dot))

        x_pos = ascii_start_x
        for seg_text, is_dot in segments:
            color = DOT_COLOR if is_dot else TEXT_COLOR
            escaped = html.escape(seg_text)
            parts.append(
                f'    <text x="{x_pos}" y="{y}" '
                f'font-family="Courier New,monospace" '
                f'font-size="{ascii_font}px" '
                f'fill="{color}" '
                f'xml:space="preserve">{escaped}</text>\n'
            )
            x_pos += len(seg_text) * ascii_cw

    parts.append('  </g>\n\n')

    # --- Vertical divider ---
    div_x = pad + ascii_block_w + gap // 2
    parts.append(f'  <line x1="{div_x}" y1="{title_bar_h + 10}" x2="{div_x}" y2="{svg_height - 10}" stroke="#30363d" stroke-width="0.5"/>\n\n')

    # --- Info panel (right side) with SMIL line-by-line animation ---
    info_start_x = pad + ascii_block_w + gap
    info_start_y = pad + title_bar_h

    for i, line_parts in enumerate(info_lines):
        y = info_start_y + i * info_lh + info_font
        x_pos = info_start_x
        begin_time = info_start + i * line_delay
        is_last = (i == len(info_lines) - 1)

        parts.append(f'  <g opacity="0">\n')
        parts.append(f'    <animate attributeName="opacity" from="0" to="1" begin="{begin_time:.2f}s" dur="0.2s" fill="freeze"/>\n')

        for text, color in line_parts:
            escaped = html.escape(text)
            parts.append(
                f'    <text x="{x_pos}" y="{y}" '
                f'font-family="Courier New,monospace" '
                f'font-size="{info_font}px" '
                f'fill="{color}" '
                f'xml:space="preserve">{escaped}</text>\n'
            )
            x_pos += len(text) * info_cw

        parts.append(f'  </g>\n')

    # --- Blinking cursor (separate element) ---
    cursor_begin = info_start + (len(info_lines) - 1) * line_delay + 0.3
    cursor_y = info_start_y + (len(info_lines) - 1) * info_lh + info_font
    parts.append(f'\n  <text x="{info_start_x + 2 * info_cw}" y="{cursor_y}" '
                 f'font-family="Courier New,monospace" font-size="{info_font}px" '
                 f'fill="{HIGHLIGHT_COLOR}" opacity="0">\n')
    parts.append(f'    <animate attributeName="opacity" values="0;0;1;1;0;0" '
                 f'keyTimes="0;{cursor_begin/20:.3f};{(cursor_begin+0.01)/20:.3f};{(cursor_begin+0.5)/20:.3f};{(cursor_begin+0.51)/20:.3f};1" '
                 f'dur="20s" repeatCount="indefinite"/>\n')
    parts.append(f'    _\n')
    parts.append(f'  </text>\n')

    # --- Simpler blinking cursor overlay ---
    # Override with a clean blink that starts after all lines appear
    parts.append(f'\n  <!-- Blinking cursor -->\n')
    parts.append(f'  <rect x="{info_start_x + 2 * info_cw}" y="{cursor_y - info_font + 2}" '
                 f'width="{info_cw}" height="{info_font + 2}" fill="{HIGHLIGHT_COLOR}" opacity="0">\n')
    parts.append(f'    <animate attributeName="opacity" values="0;1;0" '
                 f'dur="1s" begin="{cursor_begin:.2f}s" repeatCount="indefinite"/>\n')
    parts.append(f'  </rect>\n')

    parts.append('\n</svg>\n')

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(''.join(parts))
    print(f"Generated: {output_file} ({svg_width}x{svg_height})")


if __name__ == "__main__":
    generate_combined_svg()
