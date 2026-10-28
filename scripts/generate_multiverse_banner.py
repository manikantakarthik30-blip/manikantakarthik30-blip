#!/usr/bin/env python3
"""Build an animated GitHub profile banner with official tool logos orbiting a cosmic core."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import cairosvg
import io, math, os, random, re, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "multiverse-tools-orbit.gif")
W, H, FRAMES, DURATION = 1200, 360, 24, 85
random.seed(24)

# Deep-space gradient with blue/violet nebulae, generated locally (no external assets).
background = Image.new("RGB", (W, H))
px = background.load()
for y in range(H):
    for x in range(W):
        nx = x / W
        blue = math.exp(-(((x - 870) / 300) ** 2 + ((y - 170) / 180) ** 2))
        violet = math.exp(-(((x - 1080) / 230) ** 2 + ((y - 135) / 200) ** 2))
        px[x, y] = (
            5 + int(4 * nx + 13 * blue + 12 * violet),
            8 + int(3 * nx + 43 * blue + 8 * violet),
            20 + int(12 * nx + 100 * blue + 40 * violet),
        )

clouds = Image.new("RGBA", (W, H), (0, 0, 0, 0))
cd = ImageDraw.Draw(clouds, "RGBA")
cd.ellipse((590, -70, 1120, 400), fill=(16, 111, 242, 56))
cd.ellipse((830, -90, 1280, 340), fill=(131, 55, 255, 54))
cd.ellipse((760, 75, 1180, 390), fill=(32, 205, 255, 26))
background = Image.alpha_composite(background.convert("RGBA"), clouds.filter(ImageFilter.GaussianBlur(48)))
draw = ImageDraw.Draw(background, "RGBA")

# Restrained HUD grid and static stars.
for x in range(0, W, 40):
    draw.line((x, 0, x, H), fill=(100, 145, 220, 13), width=1)
for y in range(0, H, 40):
    draw.line((0, y, W, y), fill=(100, 145, 220, 13), width=1)
for _ in range(155):
    x, y = random.randrange(W), random.randrange(H)
    r = random.choice([1, 1, 1, 2])
    col = random.choice([(190, 222, 255, 130), (103, 232, 249, 150), (196, 181, 253, 135)])
    draw.ellipse((x-r, y-r, x+r, y+r), fill=col)
for line in [
    (34, 28, 150, 28), (34, 28, 34, 62), (W-150, 28, W-34, 28), (W-34, 28, W-34, 62),
    (34, H-28, 150, H-28), (34, H-62, 34, H-28), (W-150, H-28, W-34, H-28), (W-34, H-62, W-34, H-28)
]:
    draw.line(line, fill=(103, 232, 249, 100), width=1)

def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()

title_font = font("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 42)
sub_font = font("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 15)
pill_font = font("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 13)
logo_font = font("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 31)

# Official brand marks from Simple Icons. Pinned commit URLs keep artwork reproducible.
TOOLS = [
    ("PYTHON", "3776AB", "python", "develop"),
    ("MYSQL", "4479A1", "mysql", "develop"),
    ("REACT", "61DAFB", "react", "develop"),
    ("FLUTTER", "54C5F8", "flutter", "develop"),
    ("THREE.JS", "FFFFFF", "threedotjs", "develop"),
    ("FASTAPI", "009688", "fastapi", "develop"),
    ("GIT", "F05032", "git", "develop"),
    ("JAVASCRIPT", "F7DF1E", "javascript", "develop"),
]
cx, cy = 925, 178
frames = []
icon_images = {}
for label, hex_color, slug, revision in TOOLS:
    url = f"https://raw.githubusercontent.com/simple-icons/simple-icons/{revision}/icons/{slug}.svg"
    request = urllib.request.Request(url, headers={"User-Agent": "multiverse-profile-banner/1.0"})
    with urllib.request.urlopen(request, timeout=20) as response:
        svg = response.read().decode("utf-8")
    svg = re.sub(r"<path", f'<path fill="#{hex_color}"', svg, count=1)
    png = cairosvg.svg2png(bytestring=svg.encode("utf-8"), output_width=96, output_height=96)
    icon_images[label] = Image.open(io.BytesIO(png)).convert("RGBA")

def orbit_points(rx, ry, rotation, count=180):
    points = []
    for j in range(count + 1):
        a = 2 * math.pi * j / count
        xx, yy = rx * math.cos(a), ry * math.sin(a)
        points.append((cx + xx * math.cos(rotation) - yy * math.sin(rotation),
                       cy + xx * math.sin(rotation) + yy * math.cos(rotation)))
    return points

for f in range(FRAMES):
    phase = 2 * math.pi * f / FRAMES
    frame = background.copy()
    glow = Image.new("RGBA", (W, H), (0,0,0,0))
    gd = ImageDraw.Draw(glow, "RGBA")
    gd.ellipse((cx-86, cy-86, cx+86, cy+86), fill=(30,110,255,55))
    gd.ellipse((cx-57, cy-57, cx+57, cy+57), fill=(112,65,255,42))
    frame = Image.alpha_composite(frame, glow.filter(ImageFilter.GaussianBlur(22)))
    d = ImageDraw.Draw(frame, "RGBA")

    d.ellipse((cx-176, cy-67, cx+176, cy+67), outline=(103,232,249,130), width=2)
    d.line(orbit_points(168, 91, math.radians(-31)), fill=(167,139,250,170), width=2)
    d.line(orbit_points(148, 112, math.radians(35)), fill=(96,165,250,110), width=1)

    for k in range(18):
        a = 2 * math.pi * k / 18 + phase * 1.5
        x, y = cx + 184 * math.cos(a), cy + 72 * math.sin(a)
        r = 3 if k % 3 == 0 else 2
        color = (103,232,249,230) if k % 2 == 0 else (167,139,250,230)
        d.ellipse((x-r, y-r, x+r, y+r), fill=color)

    d.ellipse((cx-54, cy-54, cx+54, cy+54), fill=(5,10,28,244), outline=(103,232,249,235), width=2)
    d.ellipse((cx-44, cy-44, cx+44, cy+44), outline=(167,139,250,210), width=2)
    d.ellipse((cx-33, cy-33, cx+33, cy+33), outline=(96,165,250,135), width=1)
    d.ellipse((cx-8, cy-8, cx+8, cy+8), fill=(223,252,255,255))
    box = d.textbbox((0,0), "MK", font=logo_font)
    d.text((cx-(box[2]-box[0])/2, cy-(box[3]-box[1])/2-3), "MK", font=logo_font, fill=(242,247,255,255))

    # Real brand logos orbit the core and rotate on their own axis.
    for i, (label, hex_color, _slug, _revision) in enumerate(TOOLS):
        a = 2 * math.pi * i / len(TOOLS) + phase
        x, y = cx + 208 * math.cos(a), cy + 116 * math.sin(a)
        bw, bh = 88, 65
        color = tuple(bytes.fromhex(hex_color))
        d.rounded_rectangle((x-bw/2, y-bh/2, x+bw/2, y+bh/2), radius=12,
                            fill=(4,9,24,244), outline=color+(245,), width=2)
        # Rotate just the logo, not its label, so each brand remains easy to identify.
        icon = icon_images[label].rotate(-360 * f / FRAMES + i * 17,
                                          resample=Image.Resampling.BICUBIC, expand=False)
        icon = icon.resize((31,31), Image.Resampling.LANCZOS)
        frame.alpha_composite(icon, (int(x-15.5), int(y-28)))
        text_box = d.textbbox((0,0), label, font=pill_font)
        tw = text_box[2] - text_box[0]
        d.text((x-tw/2, y+12), label, font=pill_font, fill=color+(255,))

    d.text((73,116), "MANIKANTA BALAGA", font=title_font, fill=(242,247,255,255))
    d.rounded_rectangle((76,174,124,178), radius=2, fill=(103,232,249,255))
    d.rounded_rectangle((132,174,157,178), radius=2, fill=(167,139,250,255))
    d.text((76,195), "SOFTWARE  ·  AI  ·  DATA SCIENCE", font=sub_font, fill=(222,232,255,245))
    d.text((76,225), "SKILLS IN ORBIT  /  MULTIVERSE MODE", font=sub_font, fill=(137,165,221,245))
    d.text((1010,320), "TOOLS / 08", font=sub_font, fill=(170,190,235,225))
    frames.append(frame.convert("RGB").quantize(colors=80, method=Image.Quantize.FASTOCTREE, dither=Image.Dither.NONE))

os.makedirs(os.path.dirname(OUT), exist_ok=True)
frames[0].save(OUT, save_all=True, append_images=frames[1:], duration=DURATION, loop=0, optimize=True, disposal=1)
print(f"Generated {OUT} ({os.path.getsize(OUT):,} bytes; {FRAMES} frames)")
