"""
Generate a single combined terminal SVG for GitHub profile README.
ASCII art on the left, terminal info on the right — all in one panel.
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
    """Generate a single terminal SVG with ASCII art left + info right."""
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
        [("  AI & Software Engineer", TEXT_COLOR)],
        [("  Data Science @ Jadavpur University", TEXT_COLOR)],
        [],
        [("$ ", ACCENT_COLOR), ("ls ", HIGHLIGHT_COLOR), ("languages/", ACCENT_COLOR)],
        [("  Python  Java  C++  JavaScript  SQL", TEXT_COLOR)],
        [],
        [("$ ", ACCENT_COLOR), ("ls ", HIGHLIGHT_COLOR), ("ai-ml/", ACCENT_COLOR)],
        [("  PyTorch  TensorFlow  Scikit-Learn", TEXT_COLOR)],
        [("  OpenCV   NumPy      Pandas", TEXT_COLOR)],
        [],
        [("$ ", ACCENT_COLOR), ("ls ", HIGHLIGHT_COLOR), ("frameworks/", ACCENT_COLOR)],
        [("  Flask    FastAPI  Spring Boot", TEXT_COLOR)],
        [("  React    HTML5   CSS3", TEXT_COLOR)],
        [],
        [("$ ", ACCENT_COLOR), ("ls ", HIGHLIGHT_COLOR), ("databases/", ACCENT_COLOR)],
        [("  PostgreSQL  MongoDB", TEXT_COLOR)],
        [],
        [("$ ", ACCENT_COLOR), ("ls ", HIGHLIGHT_COLOR), ("devops/", ACCENT_COLOR)],
        [("  Docker  Kubernetes  Git", TEXT_COLOR)],
        [],
        [("$ ", ACCENT_COLOR), ("cat ", HIGHLIGHT_COLOR), ("achievements.log", ACCENT_COLOR)],
        [("  [+] Hacktoberfest Supercontributor", TEXT_COLOR)],
        [("  [+] SETV Global Intern", TEXT_COLOR)],
        [],
        [("$ ", ACCENT_COLOR), ("cat ", HIGHLIGHT_COLOR), ("interests.txt", ACCENT_COLOR)],
        [("  >> Computer Vision & Facial AI", TEXT_COLOR)],
        [("  >> NLP & RAG Systems", TEXT_COLOR)],
        [("  >> Deep Learning Research", TEXT_COLOR)],
        [("  >> Open Source", TEXT_COLOR)],
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

    # Ensure minimum width
    svg_width = max(svg_width, 850)

    parts = []
    parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{svg_width}" height="{svg_height}" viewBox="0 0 {svg_width} {svg_height}">\n')

    # Background
    parts.append(f'  <rect width="100%" height="100%" fill="{BG_COLOR}" rx="10" ry="10"/>\n')
    parts.append(f'  <rect x="1" y="1" width="{svg_width-2}" height="{svg_height-2}" fill="none" stroke="#30363d" stroke-width="1" rx="10" ry="10"/>\n')

    # Terminal title bar
    parts.append(f'  <circle cx="20" cy="16" r="5" fill="#ff5f57"/>\n')
    parts.append(f'  <circle cx="36" cy="16" r="5" fill="#febc2e"/>\n')
    parts.append(f'  <circle cx="52" cy="16" r="5" fill="#28c840"/>\n')
    parts.append(
        f'  <text x="{svg_width // 2}" y="20" '
        f'font-family="Courier New,monospace" font-size="11px" '
        f'fill="#8b949e" text-anchor="middle">unknownar@github:~$</text>\n'
    )

    # Divider line under title bar
    parts.append(f'  <line x1="0" y1="{title_bar_h}" x2="{svg_width}" y2="{title_bar_h}" stroke="#30363d" stroke-width="0.5"/>\n')

    # --- ASCII art (left side) ---
    ascii_start_x = pad
    ascii_start_y = pad + title_bar_h

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
                f'  <text x="{x_pos}" y="{y}" '
                f'font-family="Courier New,monospace" '
                f'font-size="{ascii_font}px" '
                f'fill="{color}" '
                f'xml:space="preserve">{escaped}</text>\n'
            )
            x_pos += len(seg_text) * ascii_cw

    # --- Vertical divider ---
    div_x = pad + ascii_block_w + gap // 2
    parts.append(f'  <line x1="{div_x}" y1="{title_bar_h + 10}" x2="{div_x}" y2="{svg_height - 10}" stroke="#30363d" stroke-width="0.5"/>\n')

    # --- Info panel (right side) ---
    info_start_x = pad + ascii_block_w + gap
    info_start_y = pad + title_bar_h

    for i, line_parts in enumerate(info_lines):
        y = info_start_y + i * info_lh + info_font
        x_pos = info_start_x

        for text, color in line_parts:
            escaped = html.escape(text)
            parts.append(
                f'  <text x="{x_pos}" y="{y}" '
                f'font-family="Courier New,monospace" '
                f'font-size="{info_font}px" '
                f'fill="{color}" '
                f'xml:space="preserve">{escaped}</text>\n'
            )
            x_pos += len(text) * info_cw

    parts.append('</svg>\n')

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(''.join(parts))
    print(f"Generated: {output_file} ({svg_width}x{svg_height})")


if __name__ == "__main__":
    generate_combined_svg()
