import re
import os
import html

import urllib.request
url = "https://share.text-image.com/875070e8ebc9a923"
output_file = r"e:\WorkSpace\Projects\UNKNOWNAR\colored_binary_art.svg"

req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as response:
    content = response.read().decode()

# Find the content inside <pre id="tiresult"...> ... </pre>
match = re.search(r'<pre id="tiresult"[^>]*>(.*?)</pre>', content, re.DOTALL)
if not match:
    # Try just grabbing lines with <b style=color
    lines = [line for line in content.split('\n') if '<b style=color' in line]
    if not lines:
        print("Could not find pre tag with id tiresult or binary lines")
        exit(1)
else:
    pre_content = match.group(1)
    lines = pre_content.strip().split('\n')


# SVG parameters
font_size = 5
line_height = 6
char_width = 3
pad = 20

# Calculate max line length to determine SVG width
max_chars = 0
for line in lines:
    # Remove HTML tags to get raw text length
    text_only = re.sub(r'<[^>]+>', '', line)
    if len(text_only) > max_chars:
        max_chars = len(text_only)

svg_width = pad * 2 + max_chars * char_width
svg_height = pad * 2 + len(lines) * line_height

parts = []
parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{svg_width}" height="{svg_height}" viewBox="0 0 {svg_width} {svg_height}">\n')
# Removed background rect for transparent background
parts.append(f'  <g font-family="Courier New,monospace" font-size="{font_size}px" font-weight="bold">\n')

for i, line in enumerate(lines):
    y = pad + i * line_height + font_size
    parts.append(f'    <text x="{pad}" y="{y}" xml:space="preserve">')
    
    # Parse <b> tags: <b style=color:#838383>01</b>
    # Some parts might be plain text? Usually it's all wrapped in <b>
    # We can split by <b> or use regex
    # Regex to find all (color, text) pairs
    # Note: style=color:#HEX or style="color:#HEX"
    tokens = re.findall(r'<b\s+style=?["\']?color:([^>"\']+)["\']?>([^<]+)</b>', line)
    
    if not tokens:
        # If no tokens, maybe it's just text
        text_only = re.sub(r'<[^>]+>', '', line)
        parts.append(html.escape(text_only))
    else:
        for color, text in tokens:
            escaped = html.escape(text)
            parts.append(f'<tspan fill="{color}">{escaped}</tspan>')
            
    parts.append('</text>\n')

parts.append('  </g>\n')
parts.append('</svg>\n')

with open(output_file, "w", encoding="utf-8") as f:
    f.write("".join(parts))

print(f"Generated: {output_file} ({svg_width}x{svg_height})")
