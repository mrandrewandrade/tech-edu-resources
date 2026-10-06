"""Build clean, annotated Photopea walkthrough screenshots for the personal-logo lesson.

The guide reuses genuine Photopea interface captures from the name-tag lesson,
removes distracting advertisement space, and places the personal-logo example
inside the editor so every image focuses on the student action being taught.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "site" / "assets" / "name-tag-photopea"
OUT = ROOT / "site" / "assets" / "personal-logo-photopea"
CLEAN_NAME_TAG = SOURCE / "clean"
FONT = ROOT / "site" / "assets" / "fonts" / "SourceSans3-VariableFont_wght.ttf"
BOLD = ROOT / "site" / "assets" / "fonts" / "SourceSans3-Bold.ttf"

W, H = 1600, 1000
NAVY = "#0b2e4f"
CYAN = "#22a6cc"
GOLD = "#f7b733"
GREEN = "#2f6f52"
DARK = "#202124"
PANEL = "#303134"
INK = "#111820"
LIGHT = "#eef4f7"


def font(size, bold=False):
    return ImageFont.truetype(str(BOLD if bold else FONT), size)


def fit_text(draw, text, box, size=34, bold=False, fill=INK, spacing=8):
    x1, y1, x2, y2 = box
    f = font(size, bold)
    words = text.split()
    lines, current = [], ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if draw.textbbox((0, 0), candidate, font=f)[2] <= x2 - x1:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    y = y1
    for line in lines:
        draw.text((x1, y), line, font=f, fill=fill)
        y += size + spacing
    return y


def add_number(draw, number, x, y):
    draw.ellipse((x, y, x + 62, y + 62), fill=CYAN)
    draw.text((x + 31, y + 29), str(number), font=font(34, True), fill="white", anchor="mm")


def footer(draw):
    draw.text((35, 962), "Technology Commons • Photopea interface may change slightly", font=font(22), fill="#647582")


def callout_panel(image, number, title, instruction, checks):
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((1075, 35, 1565, 940), radius=24, fill="white", outline="#b8c7d1", width=3)
    add_number(draw, number, 1110, 75)
    fit_text(draw, title, (1190, 78, 1530, 190), size=38, bold=True, fill=NAVY)
    y = fit_text(draw, instruction, (1115, 220, 1525, 520), size=31, fill=INK, spacing=10)
    y += 26
    for check in checks:
        draw.rounded_rectangle((1115, y, 1149, y + 34), radius=5, outline=CYAN, width=3)
        y = fit_text(draw, check, (1170, y - 2, 1525, y + 115), size=27, fill=INK, spacing=5) + 18
    footer(draw)


def editor_base():
    source = Image.open(SOURCE / "03-place-transparent-pngs.jpg").convert("RGB")
    canvas = Image.new("RGB", (W, H), DARK)
    top = source.crop((0, 0, 560, 96)).resize((1040, 178), Image.Resampling.LANCZOS)
    tools = source.crop((0, 85, 48, 845)).resize((72, 822), Image.Resampling.LANCZOS)
    canvas.paste(top, (0, 0))
    canvas.paste(tools, (0, 178))
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle((74, 108, 420, 174), radius=8, fill="#303134")
    draw.text((102, 122), "PERSONAL LOGO *", font=font(26, True), fill="#e8eaed")
    draw.rectangle((72, 178, 1040, 960), fill="#252525")
    draw.rounded_rectangle((205, 205, 905, 905), radius=8, fill="white", outline="#747474", width=3)
    draw.rectangle((920, 200, 1030, 905), fill=PANEL)
    draw.text((940, 220), "LAYERS", font=font(22, True), fill="white")
    return canvas


def draw_sketch(draw, opacity=255):
    colour = (93, 104, 113, opacity)
    draw.ellipse((385, 320, 505, 440), outline=colour, width=12)
    draw.line((325, 635, 455, 440, 560, 590, 680, 395, 805, 635), fill=colour, width=14, joint="curve")
    draw.arc((305, 565, 815, 805), 205, 335, fill=colour, width=15)


def draw_clean_logo(draw, colour_mode=False):
    sun = GOLD if colour_mode else INK
    mountain = GREEN if colour_mode else INK
    river = "#2382b5" if colour_mode else INK
    draw.ellipse((365, 315, 505, 455), fill=sun)
    draw.polygon([(455, 690), (610, 405), (795, 690)], fill=mountain)
    draw.arc((300, 565, 835, 835), 205, 335, fill=river, width=28)
    draw.ellipse((330, 275, 850, 795), outline=NAVY if colour_mode else INK, width=16)


def layer_row(draw, y, name, visible=True, selected=False, lock=False):
    if selected:
        draw.rectangle((930, y - 6, 1025, y + 44), fill="#4b5964")
    draw.text((935, y), "●" if visible else "○", font=font(18), fill="#e8eaed")
    draw.text((960, y), name[:8], font=font(18, True), fill="#e8eaed")
    if lock:
        draw.text((1005, y), "L", font=font(17, True), fill=GOLD)


def step1():
    canvas = Image.new("RGB", (W, H), DARK)
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle((85, 45, 955, 930), radius=18, fill="#3b3b3b", outline="#606266", width=3)
    draw.text((120, 75), "New Project", font=font(38, True), fill="white")
    draw.line((85, 132, 955, 132), fill="#595b5f", width=3)

    def field(label, value, box, value_size=32):
        x1, y1, x2, y2 = box
        draw.text((x1, y1 - 38), label, font=font(25), fill="#e1e4e8")
        draw.rounded_rectangle(box, radius=7, fill="#2f3032", outline="#515358", width=2)
        draw.text((x1 + 18, y1 + 13), value, font=font(value_size, True), fill="white")

    field("Name", "PERSONAL LOGO", (120, 200, 915, 275), 34)
    field("Width", "1000", (120, 350, 365, 425))
    field("Height", "1000", (390, 350, 635, 425))
    field("Units", "Pixels", (660, 350, 915, 425), 30)
    field("Resolution", "300 Pixels / Inch", (120, 500, 500, 575), 29)
    field("Background", "Transparent", (530, 500, 915, 575), 29)
    field("Mode", "RGB · 8 bit", (120, 650, 500, 725), 29)
    field("Profile", "sRGB", (530, 650, 915, 725), 29)
    draw.rounded_rectangle((120, 810, 915, 875), radius=7, fill="#65676b")
    draw.text((518, 843), "Create", font=font(30, True), fill="white", anchor="mm")
    callout_panel(canvas, 1, "Create a square file", "Choose File > New. A square master is easy to reuse and does not represent the physical name-tag size.", ["Width: 1000 px", "Height: 1000 px", "Background: Transparent"])
    return canvas


def step2():
    canvas = editor_base()
    overlay = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    draw_sketch(draw, 255)
    layer_row(draw, 275, "REFERENCE", selected=True)
    canvas = Image.alpha_composite(canvas.convert("RGBA"), overlay).convert("RGB")
    callout_panel(canvas, 2, "Place the sketch", "Choose File > Open & Place. Select the photo or scan of the sketch you chose on the handout.", ["Rename the layer REFERENCE", "Resize it to fill most of the square", "Keep the proportions locked"])
    return canvas


def step3():
    canvas = editor_base().convert("RGBA")
    overlay = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    draw_sketch(draw, 78)
    layer_row(draw, 275, "REFERENCE", selected=True, lock=True)
    draw.text((936, 330), "Opacity", font=font(18), fill="white")
    draw.rounded_rectangle((936, 360, 1018, 402), radius=4, fill="#202124", outline=CYAN, width=3)
    draw.text((956, 367), "30%", font=font(20, True), fill="white")
    canvas = Image.alpha_composite(canvas, overlay).convert("RGB")
    callout_panel(canvas, 3, "Fade and lock it", "The sketch is only a guide. Lower its opacity so the clean shapes are easy to see, then lock it so it cannot move.", ["Opacity: 30%", "Select the lock icon", "Do not draw on REFERENCE"])
    return canvas


def step4():
    canvas = editor_base().convert("RGBA")
    overlay = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    draw_sketch(draw, 45)
    draw_clean_logo(draw, False)
    layer_row(draw, 275, "SUN", selected=True)
    layer_row(draw, 325, "MOUNTAIN")
    layer_row(draw, 375, "RIVER")
    layer_row(draw, 425, "REFERENCE", lock=True)
    canvas = Image.alpha_composite(canvas, overlay).convert("RGB")
    callout_panel(canvas, 4, "Rebuild with shapes", "Create one named layer for each part. Use U for circles and rectangles. Use P for a custom mountain or curve.", ["Fill: black", "Stroke: none", "Close every Pen-tool path"])
    return canvas


def step5():
    canvas = editor_base().convert("RGBA")
    overlay = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    draw_clean_logo(draw, False)
    layer_row(draw, 275, "SUN")
    layer_row(draw, 325, "MOUNTAIN")
    layer_row(draw, 375, "RIVER", selected=True)
    layer_row(draw, 425, "REFERENCE", visible=False, lock=True)
    draw.rounded_rectangle((245, 825, 470, 875), radius=10, fill=LIGHT, outline=CYAN, width=3)
    draw.text((265, 836), "25 mm test", font=font(24, True), fill=NAVY)
    canvas = Image.alpha_composite(canvas, overlay).convert("RGB")
    callout_panel(canvas, 5, "Run the black test", "Hide REFERENCE. Shrink the mark on screen. If it becomes confusing, remove details or open narrow gaps.", ["Readable at about 25 mm", "No tiny floating parts", "Strong black silhouette"])
    return canvas


def step6():
    canvas = editor_base().convert("RGBA")
    overlay = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    draw_clean_logo(draw, True)
    layer_row(draw, 275, "SUN")
    layer_row(draw, 325, "MOUNTAIN")
    layer_row(draw, 375, "RIVER", selected=True)
    layer_row(draw, 425, "REFERENCE", visible=False, lock=True)
    draw.rounded_rectangle((555, 675, 890, 880), radius=12, fill="#f8fafb", outline="#8ea1ae", width=3)
    draw.text((580, 700), "File > Export As", font=font(28, True), fill=NAVY)
    draw.text((580, 750), "SVG   vector master", font=font(24), fill=INK)
    draw.text((580, 790), "PNG   transparent copy", font=font(24), fill=INK)
    draw.text((580, 830), "PSD   editable source", font=font(24), fill=INK)
    canvas = Image.alpha_composite(canvas, overlay).convert("RGB")
    callout_panel(canvas, 6, "Colour and export", "Add only two or three colours after the black version works. Keep the editable source and export the formats needed later.", ["Save the PSD first", "Export SVG for scaling", "Export transparent PNG for the name tag"])
    return canvas


def crop_name_tag_screenshots():
    """Remove Photopea's advertising rail without recreating the interface."""
    CLEAN_NAME_TAG.mkdir(parents=True, exist_ok=True)
    crops = {
        "02-safe-margin-guides.jpg": (0, 0, 560, 862),
        "03-place-transparent-pngs.jpg": (0, 0, 560, 862),
        "04-add-readable-name.jpg": (0, 0, 560, 862),
        "05-final-layout.jpg": (0, 0, 560, 862),
        "06-export-png.jpg": (0, 0, 545, 862),
    }
    for filename, crop_box in crops.items():
        source = Image.open(SOURCE / filename).convert("RGB")
        cropped = source.crop(crop_box)
        cropped.save(CLEAN_NAME_TAG / filename, quality=92, subsampling=0)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    builders = [step1, step2, step3, step4, step5, step6]
    for index, builder in enumerate(builders, start=1):
        image = builder()
        image.save(OUT / f"{index:02d}-photopea-personal-logo.jpg", quality=92, subsampling=0)
    crop_name_tag_screenshots()


if __name__ == "__main__":
    main()
