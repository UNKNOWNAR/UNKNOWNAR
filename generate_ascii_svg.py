"""
Generate all SVG assets for a terminal-styled GitHub profile README.
Creates: ascii_art.svg + terminal_info.svg
Matching the grey-on-dark terminal aesthetic from the reference.
"""
import html
import os

BASEDIR = os.path.dirname(__file__)
BG_COLOR = "#0d1117"
TEXT_COLOR = "#8b949e"
HIGHLIGHT_COLOR = "#c9d1d9"
ACCENT_COLOR = "#58a6ff"
DOT_COLOR = "#151b23"

FONT_SIZE = 5.5
LINE_HEIGHT = 7.2
CHAR_WIDTH = 3.3
PADDING_X = 20
PADDING_Y = 25


def generate_ascii_svg():
    """Generate the ASCII art SVG."""
    input_file = os.path.join(BASEDIR, "ascii_final.txt")
    output_file = os.path.join(BASEDIR, "ascii_art.svg")

    with open(input_file, "r", encoding="utf-8") as f:
        lines = [line.rstrip('\n').rstrip('\r') for line in f.readlines()]

    max_line_len = max(len(line) for line in lines)
    svg_width = int(max_line_len * CHAR_WIDTH + PADDING_X * 2)
    svg_height = int(len(lines) * LINE_HEIGHT + PADDING_Y * 2)

    parts = []
    parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{svg_width}" height="{svg_height}" viewBox="0 0 {svg_width} {svg_height}">\n')
    parts.append(f'  <rect width="100%" height="100%" fill="{BG_COLOR}" rx="8" ry="8"/>\n')
    parts.append(f'  <rect x="1" y="1" width="{svg_width - 2}" height="{svg_height - 2}" fill="none" stroke="#30363d" stroke-width="1" rx="8" ry="8"/>\n\n')

    for i, line in enumerate(lines):
        y = PADDING_Y + i * LINE_HEIGHT + FONT_SIZE

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

        x_pos = PADDING_X
        for seg_text, is_dot in segments:
            color = DOT_COLOR if is_dot else TEXT_COLOR
            escaped = html.escape(seg_text)
            parts.append(
                f'  <text x="{x_pos}" y="{y}" '
                f'font-family="Courier New,monospace" '
                f'font-size="{FONT_SIZE}px" '
                f'fill="{color}" '
                f'xml:space="preserve">{escaped}</text>\n'
            )
            x_pos += len(seg_text) * CHAR_WIDTH

    parts.append('</svg>\n')

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(''.join(parts))
    print(f"Generated: {output_file} ({svg_width}x{svg_height})")


def generate_terminal_info_svg():
    """Generate a terminal-style info panel SVG with profile details."""
    output_file = os.path.join(BASEDIR, "terminal_info.svg")

    # Terminal-style content lines
    # Format: (text, color) pairs per line
    info_lines = [
        [("$ ", ACCENT_COLOR), ("cat ", HIGHLIGHT_COLOR), ("about.txt", ACCENT_COLOR)],
        [],
        [("Name           ", TEXT_COLOR), (": ", "#30363d"), ("Arinjay Sarkar", HIGHLIGHT_COLOR)],
        [("Role           ", TEXT_COLOR), (": ", "#30363d"), ("AI & Software Engineer", HIGHLIGHT_COLOR)],
        [("University     ", TEXT_COLOR), (": ", "#30363d"), ("Jadavpur University", HIGHLIGHT_COLOR)],
        [("Location       ", TEXT_COLOR), (": ", "#30363d"), ("India", HIGHLIGHT_COLOR)],
        [],
        [("$ ", ACCENT_COLOR), ("cat ", HIGHLIGHT_COLOR), ("skills.txt", ACCENT_COLOR)],
        [],
        [("Languages      ", TEXT_COLOR), (": ", "#30363d"), ("Python, Java, C++, JavaScript, SQL", HIGHLIGHT_COLOR)],
        [("AI/ML          ", TEXT_COLOR), (": ", "#30363d"), ("PyTorch, TensorFlow, Scikit-Learn, OpenCV", HIGHLIGHT_COLOR)],
        [("Data           ", TEXT_COLOR), (": ", "#30363d"), ("NumPy, Pandas, Matplotlib", HIGHLIGHT_COLOR)],
        [("Backend        ", TEXT_COLOR), (": ", "#30363d"), ("Flask, FastAPI, Spring Boot", HIGHLIGHT_COLOR)],
        [("Frontend       ", TEXT_COLOR), (": ", "#30363d"), ("React, HTML5, CSS3", HIGHLIGHT_COLOR)],
        [("Databases      ", TEXT_COLOR), (": ", "#30363d"), ("PostgreSQL, MongoDB", HIGHLIGHT_COLOR)],
        [("DevOps         ", TEXT_COLOR), (": ", "#30363d"), ("Docker, Kubernetes, Git", HIGHLIGHT_COLOR)],
        [],
        [("$ ", ACCENT_COLOR), ("cat ", HIGHLIGHT_COLOR), ("interests.txt", ACCENT_COLOR)],
        [],
        [(">> ", "#30363d"), ("Computer Vision & Facial Intelligence", TEXT_COLOR)],
        [(">> ", "#30363d"), ("NLP & RAG Systems", TEXT_COLOR)],
        [(">> ", "#30363d"), ("Deep Learning Research", TEXT_COLOR)],
        [(">> ", "#30363d"), ("Open Source Contributions", TEXT_COLOR)],
        [],
        [("$ ", ACCENT_COLOR), ("echo ", HIGHLIGHT_COLOR), ("$STATUS", ACCENT_COLOR)],
        [("   Hacktoberfest Supercontributor | SETV Global Intern", TEXT_COLOR)],
        [],
        [("$ ", ACCENT_COLOR), ("_", HIGHLIGHT_COLOR)],
    ]

    font_size = 12
    line_height = 18
    char_width = 7.2
    pad_x = 25
    pad_y = 25

    max_text_len = 0
    for line_parts in info_lines:
        line_len = sum(len(text) for text, _ in line_parts)
        max_text_len = max(max_text_len, line_len)

    svg_width = int(max_text_len * char_width + pad_x * 2)
    svg_height = int(len(info_lines) * line_height + pad_y * 2)

    parts = []
    parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{svg_width}" height="{svg_height}" viewBox="0 0 {svg_width} {svg_height}">\n')
    parts.append(f'  <rect width="100%" height="100%" fill="{BG_COLOR}" rx="8" ry="8"/>\n')
    parts.append(f'  <rect x="1" y="1" width="{svg_width - 2}" height="{svg_height - 2}" fill="none" stroke="#30363d" stroke-width="1" rx="8" ry="8"/>\n')

    # Terminal title bar dots
    parts.append(f'  <circle cx="18" cy="14" r="5" fill="#ff5f57"/>\n')
    parts.append(f'  <circle cx="34" cy="14" r="5" fill="#febc2e"/>\n')
    parts.append(f'  <circle cx="50" cy="14" r="5" fill="#28c840"/>\n')
    
    title_y = 18
    parts.append(
        f'  <text x="{svg_width // 2}" y="{title_y}" '
        f'font-family="Courier New,monospace" font-size="11px" '
        f'fill="#8b949e" text-anchor="middle">unknownar@github ~ %</text>\n'
    )

    content_start_y = pad_y + 15

    for i, line_parts in enumerate(info_lines):
        y = content_start_y + i * line_height + font_size
        x_pos = pad_x

        for text, color in line_parts:
            escaped = html.escape(text)
            parts.append(
                f'  <text x="{x_pos}" y="{y}" '
                f'font-family="Courier New,monospace" '
                f'font-size="{font_size}px" '
                f'fill="{color}" '
                f'xml:space="preserve">{escaped}</text>\n'
            )
            x_pos += len(text) * char_width

    parts.append('</svg>\n')

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(''.join(parts))
    print(f"Generated: {output_file} ({svg_width}x{svg_height})")


if __name__ == "__main__":
    generate_ascii_svg()
    generate_terminal_info_svg()
    print("All SVG assets generated!")
