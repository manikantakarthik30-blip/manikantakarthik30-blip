#!/usr/bin/env python3
"""Generate a professional animated profile banner with rotating technology logos."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import cairosvg
import io, math, os, random, re, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "technology-skills-banner.gif")
W, H, FRAMES, DURATION = 1200, 360, 36, 70
random.seed(24)

# Cinematic, art-directed background. No grid overlay: the source artwork carries the visual weight.
background_path = os.path.join(ROOT, "assets", "technology-banner-background.jpg")
background = Image.open(background_path).convert("RGB").resize((W, H), Image.Resampling.LANCZOS).convert("RGBA")

# Deepen the left side so the name and headline remain crisp against the brighter space art.
shade = Image.new("RGBA", (W, H), (0, 0, 0, 0))
shade_px = shade.load()
for x in range(W):
    strength = max(0.0, 1.0 - x / 760.0)
    alpha = int(205 * strength ** 1.35)
    if alpha:
        for y in range(H):
            shade_px[x, y] = (1, 3, 12, alpha)
background = Image.alpha_composite(background, shade)

def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()

title_font = font("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 42)
sub_font = font("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 15)
pill_font = font("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 13)
logo_font = font("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 31)

# Official technology marks from Simple Icons.
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
cx, cy = 910, 145
frames = []
icon_images = {}
for label, hex_color, slug, revision in TOOLS:
    url = f"https://raw.githubusercontent.com/simple-icons/simple-icons/{revision}/icons/{slug}.svg"
    request = urllib.request.Request(url, headers={"User-Agent": "professional-profile-banner/1.0"})
    with urllib.request.urlopen(request, timeout=20) as response:
        svg = response.read().decode("utf-8")
    svg = re.sub(r"<path", f'<path fill="#{hex_color}"', svg, count=1)
    png = cairosvg.svg2png(bytestring=svg.encode("utf-8"), output_width=96, output_height=96)
    icon_images[label] = Image.open(io.BytesIO(png)).convert("RGBA")

def ellipse_points(rx, ry, rotation, count=180):
    points = []
    for j in range(count + 1):
        a = 2 * math.pi * j / count
        xx, yy = rx * math.cos(a), ry * math.sin(a)
        points.append((cx + xx * math.cos(rotation) - yy * math.sin(rotation),
                       cy + xx * math.sin(rotation) + yy * math.cos(rotation)))
    return points

for f in range(FRAMES):
    phase = 2 * math.pi * f / FRAMES
    pulse = (math.sin(phase * 2) + 1) / 2
    frame = background.copy()

    # A breathing halo around the center mark.
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow, "RGBA")
    halo = 94 + int(16 * pulse)
    gd.ellipse((cx-halo, cy-halo, cx+halo, cy+halo), fill=(27, 109, 255, 65))
    gd.ellipse((cx-65, cy-65, cx+65, cy+65), fill=(149, 62, 255, 65))
    frame = Image.alpha_composite(frame, glow.filter(ImageFilter.GaussianBlur(30)))

    # Fast, luminous energy arcs sweep around the planet; each arc has a different phase.
    energy = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ed = ImageDraw.Draw(energy, "RGBA")
    for arc in range(4):
        points = []
        offset = phase * (1.15 if arc % 2 == 0 else -0.82) + arc * math.pi / 2
        for j in range(64):
            t = offset + j / 63 * 1.15
            rx = 252 + 10 * math.sin(phase + arc)
            ry = 126 + 7 * math.cos(phase * 1.2 + arc)
            points.append((cx + rx * math.cos(t), cy + ry * math.sin(t)))
        color = [(56, 189, 248, 190), (167, 139, 250, 190),
                 (96, 165, 250, 170), (232, 121, 249, 155)][arc]
        ed.line(points, fill=color, width=3 if arc < 2 else 2)
        tx, ty = points[-1]
        ed.ellipse((tx-4, ty-4, tx+4, ty+4), fill=(225, 247, 255, 240))
    frame = Image.alpha_composite(frame, energy.filter(ImageFilter.GaussianBlur(8)))
    frame = Image.alpha_composite(frame, energy)

    d = ImageDraw.Draw(frame, "RGBA")

    # Moving sparks outside the logo path add motion without obscuring the name.
    for k in range(42):
        a = 2 * math.pi * k / 42 + phase * (1.8 if k % 2 == 0 else -1.25)
        rx = 278 + 13 * math.sin(k * 1.3)
        ry = 135 + 9 * math.cos(k * 0.7)
        x = cx + rx * math.cos(a)
        y = cy + ry * math.sin(a)
        r = 1 + (1 if k % 5 == 0 else 0)
        color = (130, 225, 255, 180) if k % 2 == 0 else (201, 170, 255, 180)
        d.ellipse((x-r, y-r, x+r, y+r), fill=color)

    # Subtle outer ring, with independently moving luminous markers.
    d.ellipse((cx-218, cy-106, cx+218, cy+106), outline=(130, 177, 255, 92), width=1)
    d.ellipse((cx-174, cy-79, cx+174, cy+79), outline=(190, 157, 255, 58), width=1)
    for k in range(16):
        a = 2 * math.pi * k / 16 + phase * 1.9
        x, y = cx + 220 * math.cos(a), cy + 108 * math.sin(a)
        radius = 3 if k % 4 == 0 else 1.8
        d.ellipse((x-radius, y-radius, x+radius, y+radius),
                  fill=(110, 230, 255, 235) if k % 2 == 0 else (194, 156, 255, 235))

    # Center emblem.
    core_r = 43 + int(2 * pulse)
    d.ellipse((cx-core_r, cy-core_r, cx+core_r, cy+core_r),
              fill=(3, 7, 22, 245), outline=(100, 224, 255, 255), width=3)
    d.ellipse((cx-core_r+8, cy-core_r+8, cx+core_r-8, cy+core_r-8),
              outline=(167, 139, 250, 225), width=2)
    d.ellipse((cx-17, cy-17, cx+17, cy+17), fill=(54, 113, 255, 170))
    box = d.textbbox((0, 0), "MB", font=logo_font)
    d.text((cx-(box[2]-box[0])/2, cy-(box[3]-box[1])/2-3), "MB",
           font=logo_font, fill=(248, 251, 255, 255))

    # True brand marks rotate themselves while their nodes travel around the center.
    for i, (label, hex_color, _slug, _revision) in enumerate(TOOLS):
        a = 2 * math.pi * i / len(TOOLS) + phase
        x = cx + 204 * math.cos(a)
        y = cy + 92 * math.sin(a)
        color = tuple(bytes.fromhex(hex_color))
        r = 28
        d.ellipse((x-r-5, y-r-5, x+r+5, y+r+5), fill=(3, 7, 22, 232),
                  outline=color+(240,), width=2)
        d.ellipse((x-r, y-r, x+r, y+r), outline=(217, 230, 255, 105), width=1)
        icon = icon_images[label].rotate(-360 * f / FRAMES + i * 19,
                                          resample=Image.Resampling.BICUBIC, expand=False)
        icon = icon.resize((40, 40), Image.Resampling.LANCZOS)
        frame.alpha_composite(icon, (int(x-20), int(y-20)))
        box = d.textbbox((0, 0), label, font=pill_font)
        tw = box[2] - box[0]
        label_w = max(tw+16, 48)
        d.rounded_rectangle((x-label_w/2, y+32, x+label_w/2, y+53),
                            radius=7, fill=(2, 6, 18, 230), outline=color+(210,), width=1)
        d.text((x-tw/2, y+35), label, font=pill_font, fill=color+(255,))

    # Typography stays still so the visual energy never harms readability.
    d.text((68, 101), "MANIKANTA BALAGA", font=title_font, fill=(248, 250, 255, 255))
    d.rounded_rectangle((72, 151, 125, 155), radius=2, fill=(103, 232, 249, 255))
    d.rounded_rectangle((132, 151, 160, 155), radius=2, fill=(167, 139, 250, 255))
    d.text((72, 176), "SOFTWARE ENGINEERING  /  AI  /  DATA SCIENCE",
           font=sub_font, fill=(229, 238, 255, 250))
    d.text((72, 207), "Building practical software across disciplines",
           font=sub_font, fill=(151, 176, 224, 250))
    d.text((72, 319), "PYTHON   ·   WEB   ·   DATA   ·   SECURITY",
           font=pill_font, fill=(202, 215, 244, 235))

    # 128-color frames preserve the glow gradients while keeping the GIF reasonably small.
    frames.append(frame.convert("RGB").quantize(colors=128, method=Image.Quantize.FASTOCTREE,
                                                dither=Image.Dither.NONE))

os.makedirs(os.path.dirname(OUT), exist_ok=True)
frames[0].save(OUT, save_all=True, append_images=frames[1:], duration=DURATION, loop=0, optimize=True, disposal=1)
print(f"Generated {OUT} ({os.path.getsize(OUT):,} bytes; {FRAMES} frames)")
