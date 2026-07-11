import re
import os

input_file = r"e:\WorkSpace\Projects\UNKNOWNAR\.html"

with open(input_file, "r", encoding="utf-8") as f:
    content = f.read()

tokens = re.findall(r'<b\s+style=["\']?color:([^>"\']+)["\']?>([^<]+)</b>', content)
if not tokens:
    tokens = re.findall(r'<b\s+style=color:([^>"\']+)>(([^<]+))</b>', content)

def hex_to_rgb(hx):
    hx = hx.lstrip('#')
    if len(hx) != 6: return 0,0,0
    try:
        return int(hx[0:2], 16), int(hx[2:4], 16), int(hx[4:6], 16)
    except:
        return 0,0,0

colors = {}
for color, text in tokens:
    if isinstance(text, tuple): text = text[0]
    colors[color] = colors.get(color, 0) + len(text)

# Sort colors by frequency
sorted_colors = sorted(colors.items(), key=lambda x: x[1], reverse=True)
print("Top 20 most frequent colors:")
for c, count in sorted_colors[:20]:
    r,g,b = hex_to_rgb(c)
    brightness = (r * 0.299 + g * 0.587 + b * 0.114)
    print(f"{c}: {count} chars, brightness: {brightness:.1f}")
