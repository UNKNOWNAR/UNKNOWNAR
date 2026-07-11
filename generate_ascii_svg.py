"""
Generate an animated terminal-style SVG for GitHub profile README.
Uses SMIL animations (<animate> tags) which GitHub reliably supports.
ASCII art on the left, terminal info typing in on the right.
"""
import html
import os
import json
import urllib.request

BASEDIR = os.path.dirname(__file__)
BG_COLOR = "#0d1117"
TEXT_COLOR = "#8b949e"
HIGHLIGHT_COLOR = "#c9d1d9"
ACCENT_COLOR = "#58a6ff"
DOT_COLOR = "#151b23"
KEY_COLOR = "#ffa657"       # Orange
VAL_COLOR = "#a5d6ff"       # Light Blue
SEP_COLOR = "#616e7f"


def fetch_github_stats(username):
    """Fetch user stats from GitHub API and scrape contribution graph for streaks."""
    stats = {"followers": 0, "public_repos": 0, "total_contribs": "0", "current_streak": 0, "longest_streak": 0}
    try:
        # Fetch basic stats
        url = f"https://api.github.com/users/{username}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        token = os.environ.get("GITHUB_TOKEN")
        is_ci = os.environ.get("GITHUB_ACTIONS") == "true"
        if token and is_ci:
            req.add_header("Authorization", f"token {token}")
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            stats["followers"] = data.get("followers", 0)
            stats["public_repos"] = data.get("public_repos", 0)
            
        # Scrape contribution graph
        import re
        contrib_url = f"https://github.com/users/{username}/contributions"
        req_contrib = urllib.request.Request(contrib_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req_contrib) as response:
            html = response.read().decode()
            match = re.search(r'(\d+(?:,\d+)?)\s+contributions\s+in\s+the\s+last\s+year', html, re.IGNORECASE)
            if match:
                stats["total_contribs"] = match.group(1)
                
            tooltips = re.findall(r'<tool-tip [^>]*>([^<]+)</tool-tip>', html)
            counts = []
            for tip in tooltips:
                m = re.match(r'^(No|\d+) contributions? on ', tip)
                if m:
                    counts.append(0 if m.group(1) == "No" else int(m.group(1)))
            
            temp_streak = 0
            longest_streak = 0
            for count in counts:
                if count > 0:
                    temp_streak += 1
                    if temp_streak > longest_streak:
                        longest_streak = temp_streak
                else:
                    temp_streak = 0
            stats["longest_streak"] = longest_streak
            
            curr = 0
            for count in reversed(counts):
                if count > 0:
                    curr += 1
                else:
                    break
            stats["current_streak"] = curr

    except Exception as e:
        print(f"Failed to fetch GitHub stats: {e}")
    return stats


def generate_combined_svg():
    """Generate an animated terminal SVG with SMIL animations."""
    gh_stats = fetch_github_stats("unknownar")
    
    input_file = os.path.join(BASEDIR, ".html")
    output_file = os.path.join(BASEDIR, "terminal_hero.svg")

    # --- Read Colored Binary HTML art ---
    with open(input_file, "r", encoding="utf-8") as f:
        html_content = f.read()
    
    import re
    match = re.search(r'<pre id="tiresult"[^>]*>(.*?)</pre>', html_content, re.DOTALL)
    if not match:
        ascii_lines = [line for line in html_content.split('\n') if '<b style="color:' in line or '<b style=color' in line]
    else:
        ascii_lines = match.group(1).strip().split('\n')

    # --- ASCII art sizing ---
    ascii_font = 5.2
    ascii_lh = 6.8
    ascii_cw = 3.1
    ascii_max_len = max(len(re.sub(r'<[^>]+>', '', line)) for line in ascii_lines)
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
    content_h = max(ascii_block_h + 90, info_block_h)
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

    def hex_to_rgb(hx):
        hx = hx.lstrip('#')
        if len(hx) != 6: return 0,0,0
        try:
            return int(hx[0:2], 16), int(hx[2:4], 16), int(hx[4:6], 16)
        except:
            return 0,0,0

    def rgb_to_hex(r, g, b):
        return f"#{r:02x}{g:02x}{b:02x}"

    for i, line in enumerate(ascii_lines):
        y = ascii_start_y + i * ascii_lh + ascii_font
        parts.append(f'    <text x="{ascii_start_x}" y="{y}" font-family="Courier New,monospace" font-size="{ascii_font}px" font-weight="bold" xml:space="preserve">')
        
        tokens = re.findall(r'<b\s+style=["\']?color:([^>"\']+)["\']?>([^<]+)</b>', line)
        if not tokens:
            tokens = re.findall(r'<b\s+style=color:([^>"\']+)>(([^<]+))</b>', line)
            if not tokens:
                text_only = re.sub(r'<[^>]+>', '', line)
                parts.append(html.escape(text_only))
                
        for color, text in tokens:
            if isinstance(text, tuple): text = text[0]
            
            # Use the original colors for everything! No background removal.
            parts.append(f'<tspan fill="{color}">{html.escape(text)}</tspan>')
                
        parts.append('</text>\n')

    # Add name and stats under ASCII art
    name_y = ascii_start_y + len(ascii_lines) * ascii_lh + 20
    name_x = ascii_start_x + (ascii_block_w / 2)
    parts.append(
        f'    <text x="{name_x}" y="{name_y}" '
        f'font-family="Courier New,monospace" '
        f'font-size="16px" font-weight="bold" '
        f'fill="{HIGHLIGHT_COLOR}" text-anchor="middle">Arinjay Sarkar</text>\n'
    )
    
    def format_dots_left(k1, v1, k2, v2):
        d1 = max(1, 23 - len(k1) - len(str(v1)))
        d2 = max(1, 24 - len(k2) - len(str(v2)))
        return [
            (k1 + ": ", KEY_COLOR),
            ("." * d1 + " ", SEP_COLOR),
            (str(v1), VAL_COLOR),
            (" | ", HIGHLIGHT_COLOR),
            (k2 + ": ", KEY_COLOR),
            ("." * d2 + " ", SEP_COLOR),
            (str(v2), VAL_COLOR)
        ]

    repos = str(gh_stats.get('public_repos', 0))
    followers = str(gh_stats.get('followers', 0))
    contribs = str(gh_stats.get('total_contribs', 0))
    c_streak = str(gh_stats.get('current_streak', 0))
    l_streak = str(gh_stats.get('longest_streak', 0))
    lines_of_code = "142,305"

    left_lines = [
        [("GitHub Stats ", KEY_COLOR), ("-" * 41, SEP_COLOR)],
        format_dots_left("Repos", repos, "Followers", followers),
        format_dots_left("Contribs", contribs, "Current Streak", c_streak),
        format_dots_left("Longest Streak", l_streak, "Lines of Code", lines_of_code),
        [("", SEP_COLOR)],
        [("Contact ", KEY_COLOR), ("-" * 48, SEP_COLOR)],
        [("Email: ", KEY_COLOR), ("....... ", SEP_COLOR), ("amiarinjaysarkar@gmail.com", VAL_COLOR)],
        [("LinkedIn: ", KEY_COLOR), (".... ", SEP_COLOR), ("in/amiarinjaysarkar", VAL_COLOR)],
    ]
    
    # Render left lines under name
    left_y = name_y + 30
    left_x_start = ascii_start_x
    for row in left_lines:
        parts.append(f'    <text x="{left_x_start}" y="{left_y}" font-family="Courier New,monospace" font-size="11px" font-weight="bold" xml:space="preserve">')
        for t, c in row:
            parts.append(f'<tspan fill="{c}">{html.escape(t)}</tspan>')
        parts.append('</text>\n')
        left_y += 15

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
