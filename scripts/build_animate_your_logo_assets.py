#!/usr/bin/env python3
"""Build the repository-hosted Animate Your Logo demonstration assets."""

from __future__ import annotations

import json
import math
import zipfile
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "site" / "assets" / "animate-your-logo"
PARTS = OUTPUT / "starter-parts"
SCENE_SIZE = 1000
PREVIEW_SIZE = 720
BACKGROUND = "#0f172a"
COMMONS_EMBLEM = ROOT / "site" / "assets" / "branding" / "emblem" / "technology-commons-hands.png"
AA_LOGO = ROOT / "site" / "assets" / "branding" / "logo" / "aa-logo-transparent.png"


def clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


def ease_out_cubic(value: float) -> float:
    value = clamp(value)
    return 1 - (1 - value) ** 3


def ease_out_back(value: float) -> float:
    value = clamp(value)
    c1 = 1.70158
    c3 = c1 + 1
    return 1 + c3 * (value - 1) ** 3 + c1 * (value - 1) ** 2


def make_part_images() -> dict[str, tuple[Image.Image, tuple[int, int]]]:
    """Draw the four existing AA SVG parts as cropped transparent PNGs."""
    parts: dict[str, tuple[Image.Image, tuple[int, int]]] = {}

    sun = Image.new("RGBA", (238, 238), (0, 0, 0, 0))
    ImageDraw.Draw(sun).ellipse((0, 0, 237, 237), fill="#f6b52d")
    parts["sun"] = (sun, (685, 128))

    left = Image.new("RGBA", (398, 330), (0, 0, 0, 0))
    ImageDraw.Draw(left).polygon([(0, 330), (222, 0), (398, 330)], fill="#216147")
    parts["left-peak"] = (left, (159, 389))

    right = Image.new("RGBA", (412, 355), (0, 0, 0, 0))
    ImageDraw.Draw(right).polygon([(0, 355), (199, 0), (412, 355)], fill="#398260")
    parts["right-peak"] = (right, (467, 364))

    river = Image.new("RGBA", (660, 100), (0, 0, 0, 0))
    points = [(0, 66), (165, 16), (337, 0), (502, 16), (660, 66), (652, 100), (502, 54), (337, 37), (165, 54), (8, 100)]
    ImageDraw.Draw(river).polygon(points, fill="#2679b7")
    parts["river"] = (river, (182, 724))

    PARTS.mkdir(parents=True, exist_ok=True)
    for name, (image, _position) in parts.items():
        image.save(PARTS / f"{name}.png", optimize=True)
    return parts


def paste_part(
    canvas: Image.Image,
    part: Image.Image,
    base_position: tuple[int, int],
    *,
    progress: float,
    offset: tuple[float, float] = (0, 0),
    scale_from: float = 1.0,
    rotation_from: float = 0.0,
    global_alpha: float = 1.0,
) -> None:
    progress = clamp(progress)
    eased = ease_out_back(progress) if scale_from != 1.0 else ease_out_cubic(progress)
    scale = scale_from + (1 - scale_from) * eased
    angle = rotation_from * (1 - ease_out_cubic(progress))
    alpha = int(255 * clamp(progress * 1.8) * clamp(global_alpha))

    width = max(1, round(part.width * scale))
    height = max(1, round(part.height * scale))
    transformed = part.resize((width, height), Image.Resampling.LANCZOS)
    if abs(angle) > 0.1:
        transformed = transformed.rotate(angle, expand=True, resample=Image.Resampling.BICUBIC)
    if alpha < 255:
        transformed.putalpha(transformed.getchannel("A").point(lambda value: value * alpha // 255))

    final_x = base_position[0] + offset[0] * (1 - ease_out_cubic(progress))
    final_y = base_position[1] + offset[1] * (1 - ease_out_cubic(progress))
    x = round(final_x - (transformed.width - part.width) / 2)
    y = round(final_y - (transformed.height - part.height) / 2)
    canvas.alpha_composite(transformed, (x, y))


def animation_state(time_s: float) -> dict[str, tuple[float, tuple[float, float], float, float]]:
    return {
        "sun": (clamp(time_s / 0.8), (0, -90), 0.35, -160),
        "left-peak": (clamp((time_s - 0.45) / 0.9), (-180, 130), 1.0, 0),
        "right-peak": (clamp((time_s - 0.8) / 0.9), (180, 130), 1.0, 0),
        "river": (clamp((time_s - 1.25) / 0.8), (-260, 0), 1.0, 0),
    }


def draw_animation_frame(
    parts: dict[str, tuple[Image.Image, tuple[int, int]]], time_s: float
) -> Image.Image:
    canvas = Image.new("RGBA", (SCENE_SIZE, SCENE_SIZE), BACKGROUND)
    state = animation_state(time_s)
    fade = 1.0 if time_s < 5.2 else clamp((6.0 - time_s) / 0.8)
    float_y = 0 if time_s < 2.2 else 7 * math.sin((time_s - 2.2) * math.pi / 1.4)
    for name in ("sun", "left-peak", "right-peak", "river"):
        part, position = parts[name]
        progress, offset, scale_from, rotation_from = state[name]
        paste_part(
            canvas,
            part,
            (position[0], round(position[1] + float_y)),
            progress=progress,
            offset=offset,
            scale_from=scale_from,
            rotation_from=rotation_from,
            global_alpha=fade,
        )
    return canvas


def build_previews(parts: dict[str, tuple[Image.Image, tuple[int, int]]]) -> None:
    frames: list[Image.Image] = []
    for index in range(60):
        frame = draw_animation_frame(parts, index / 10)
        frame = frame.resize((PREVIEW_SIZE, PREVIEW_SIZE), Image.Resampling.LANCZOS).convert("P", palette=Image.Palette.ADAPTIVE, colors=128)
        frames.append(frame)
    frames[0].save(
        OUTPUT / "aa-logo-motion-example.gif",
        save_all=True,
        append_images=frames[1:],
        duration=100,
        loop=0,
        optimize=True,
        disposal=2,
    )

    # Google Slides shows the first GIF frame while editing. Start the deck
    # variant with one completed-logo frame so the example remains visible
    # before presentation mode begins playing the loop.
    slide_frames = [frames[30].copy(), *[frame.copy() for frame in frames]]
    slide_frames[0].save(
        OUTPUT / "aa-logo-motion-slides.gif",
        save_all=True,
        append_images=slide_frames[1:],
        duration=[150, *([100] * len(frames))],
        loop=0,
        optimize=True,
        disposal=2,
    )

    final = draw_animation_frame(parts, 3.0).resize((PREVIEW_SIZE, PREVIEW_SIZE), Image.Resampling.LANCZOS).convert("RGB")
    final.save(OUTPUT / "aa-logo-motion-still.png", optimize=True)

    comparison = Image.new("RGB", (1440, 720), "#f8fafc")
    before = draw_animation_frame(parts, 0.9).resize((640, 640), Image.Resampling.LANCZOS).convert("RGB")
    after = draw_animation_frame(parts, 3.0).resize((640, 640), Image.Resampling.LANCZOS).convert("RGB")
    comparison.paste(before, (40, 40))
    comparison.paste(after, (760, 40))
    draw = ImageDraw.Draw(comparison)
    draw.rounded_rectangle((24, 24, 696, 696), radius=24, outline="#94a3b8", width=4)
    draw.rounded_rectangle((744, 24, 1416, 696), radius=24, outline="#216147", width=4)
    comparison.save(OUTPUT / "aa-logo-motion-before-after.png", optimize=True)


def build_commons_emblem_motion() -> None:
    """Build the emblem piece by piece: AA, lighthouse, ecology, then hands."""
    import numpy as np
    from scipy import ndimage

    source = Image.open(COMMONS_EMBLEM).convert("RGBA")
    source_array = np.array(source)
    red, green, blue, alpha = [source_array[:, :, channel] for channel in range(4)]
    visible = alpha > 24

    yellow = (red > 165) & (green > 85) & (green < 230) & (blue < 115) & visible
    coral = (red > 175) & (green < 160) & (blue < 145) & (red > green * 1.35) & visible
    cream = (red > 175) & (green > 145) & (blue > 110) & visible
    cyan = (blue > 125) & (green > 85) & (red < 145) & visible
    navy = (blue > 48) & (blue > red * 1.22) & (green < 175) & visible

    def components(mask: np.ndarray, keep) -> np.ndarray:
        labelled, _count = ndimage.label(mask)
        selected = np.zeros(mask.shape, dtype=bool)
        for index, bounds in enumerate(ndimage.find_objects(labelled), start=1):
            if bounds is None:
                continue
            y_slice, x_slice = bounds
            component = labelled[bounds] == index
            area = int(component.sum())
            bbox = (x_slice.start, y_slice.start, x_slice.stop, y_slice.stop)
            centre = ((bbox[0] + bbox[2]) / 2, (bbox[1] + bbox[3]) / 2)
            if keep(area, bbox, centre):
                selected[bounds] |= component
        return selected

    top_hand = components(
        navy,
        lambda area, bbox, centre: area > 250 and centre[1] < 305 and bbox[3] <= 325,
    )
    lighthouse = components(
        navy,
        lambda area, bbox, centre: area > 700
        and 360 < centre[0] < 900
        and bbox[1] < 760
        and bbox[3] > 345,
    )
    waves = components(
        navy,
        lambda area, bbox, centre: area > 1800 and bbox[1] >= 735 and bbox[3] <= 920,
    )

    y_grid, x_grid = np.indices(alpha.shape)
    left_support = lighthouse & (x_grid < 590) & (y_grid > 430)
    right_support = lighthouse & (x_grid > 665) & (y_grid > 430)
    tower = lighthouse & ~(left_support | right_support)
    beams = yellow & (y_grid < 550)
    leaves = yellow & (y_grid >= 530) & (y_grid < 830)
    roots = yellow & (y_grid >= 800)

    yellow_family = (green > 90) & (green > red * 0.42) & (blue < 145) & visible
    blue_family = (blue > 42) & (blue > red * 1.08) & (blue > green * 0.82) & visible
    coral_family = (red > 150) & (red > green * 1.22) & (blue < 165) & visible
    cream_family = (red > 160) & (green > 125) & (blue > 95) & visible
    cyan_family = (blue > 105) & (green > 70) & (red < 165) & (green > red * 1.05) & visible

    def layer_from_mask(mask: np.ndarray, family: np.ndarray) -> Image.Image:
        # Expand into the antialiased fringe, then retain the original pixels.
        expanded = ndimage.binary_dilation(mask, iterations=2) & family
        result = source_array.copy()
        result[:, :, 3] = np.where(expanded, alpha, 0)
        return Image.fromarray(result).resize((720, 720), Image.Resampling.LANCZOS)

    layers = {
        "tower": layer_from_mask(tower, blue_family),
        "left_support": layer_from_mask(left_support, blue_family),
        "right_support": layer_from_mask(right_support, blue_family),
        "beams": layer_from_mask(beams, yellow_family),
        "leaves": layer_from_mask(leaves, yellow_family),
        "roots": layer_from_mask(roots, yellow_family),
        "waves": layer_from_mask(waves, blue_family),
        "top": layer_from_mask(top_hand, blue_family),
        "right": layer_from_mask(cream, cream_family),
        "bottom": layer_from_mask(coral, coral_family),
        "left": layer_from_mask(cyan, cyan_family),
    }

    def with_opacity(image: Image.Image, opacity: float) -> Image.Image:
        if opacity >= 0.999:
            return image
        faded = image.copy()
        faded.putalpha(faded.getchannel("A").point(lambda value: round(value * max(0.0, opacity))))
        return faded

    def scale_from_anchor(image: Image.Image, sx: float, sy: float, anchor: str) -> Image.Image:
        bbox = image.getbbox()
        if bbox is None:
            return image
        crop = image.crop(bbox)
        resized = crop.resize(
            (max(1, round(crop.width * sx)), max(1, round(crop.height * sy))),
            Image.Resampling.LANCZOS,
        )
        if anchor == "bottom":
            position = ((720 - resized.width) // 2, bbox[3] - resized.height)
        elif anchor == "top":
            position = ((720 - resized.width) // 2, bbox[1])
        else:
            position = ((720 - resized.width) // 2, (bbox[1] + bbox[3] - resized.height) // 2)
        result = Image.new("RGBA", (720, 720), (0, 0, 0, 0))
        result.alpha_composite(resized, position)
        return result

    def horizontal_reveal(image: Image.Image, progress: float) -> Image.Image:
        reveal = Image.new("L", (720, 720), 0)
        half_width = round(360 * max(0.0, min(1.0, progress)))
        ImageDraw.Draw(reveal).rectangle((360 - half_width, 0, 360 + half_width, 720), fill=255)
        shown = image.copy()
        shown.putalpha(Image.composite(shown.getchannel("A"), Image.new("L", (720, 720), 0), reveal))
        return shown

    def vertical_reveal(image: Image.Image, progress: float, direction: str) -> Image.Image:
        bbox = image.getbbox()
        if bbox is None or progress <= 0:
            return Image.new("RGBA", (720, 720), (0, 0, 0, 0))
        progress = max(0.0, min(1.0, progress))
        reveal = Image.new("L", (720, 720), 0)
        if direction == "up":
            edge = round(bbox[3] - (bbox[3] - bbox[1]) * progress)
            region = (bbox[0], edge, bbox[2], bbox[3])
        else:
            edge = round(bbox[1] + (bbox[3] - bbox[1]) * progress)
            region = (bbox[0], bbox[1], bbox[2], edge)
        ImageDraw.Draw(reveal).rectangle(region, fill=255)
        shown = image.copy()
        shown.putalpha(Image.composite(shown.getchannel("A"), Image.new("L", (720, 720), 0), reveal))
        return shown

    def grow_hand(image: Image.Image, angle: float, progress: float) -> Image.Image:
        settled = ease_out_back(max(0.0, min(1.0, progress)))
        bbox = image.getbbox()
        if bbox is None:
            return image
        crop = image.crop(bbox)
        scale = 0.12 + 0.88 * settled
        crop = crop.resize(
            (max(1, round(crop.width * scale)), max(1, round(crop.height * scale))),
            Image.Resampling.LANCZOS,
        )
        rotation = angle * (1 - settled)
        if abs(rotation) > 0.05:
            crop = crop.rotate(rotation, expand=True, resample=Image.Resampling.BICUBIC)
        final_centre = ((bbox[0] + bbox[2]) / 2, (bbox[1] + bbox[3]) / 2)
        centre = (
            360 + (final_centre[0] - 360) * settled,
            360 + (final_centre[1] - 360) * settled,
        )
        result = Image.new("RGBA", (720, 720), (0, 0, 0, 0))
        result.alpha_composite(
            crop,
            (round(centre[0] - crop.width / 2), round(centre[1] - crop.height / 2)),
        )
        return result

    def split_arrow(image: Image.Image, progress: float) -> Image.Image:
        progress = ease_out_cubic(max(0.0, min(1.0, progress)))
        result = Image.new("RGBA", (720, 720), (0, 0, 0, 0))
        for side, bounds, dx, rotation in (
            ("left", (0, 0, 360, 720), -30, -6),
            ("right", (360, 0, 720, 720), 30, 6),
        ):
            piece = Image.new("RGBA", (720, 720), (0, 0, 0, 0))
            piece.alpha_composite(image.crop(bounds), (bounds[0], bounds[1]))
            bbox = piece.getbbox()
            if bbox is None:
                continue
            crop = piece.crop(bbox)
            angle = rotation * progress
            if abs(angle) > 0.05:
                crop = crop.rotate(angle, expand=True, resample=Image.Resampling.BICUBIC)
            centre = (
                (bbox[0] + bbox[2]) / 2 + dx * progress,
                (bbox[1] + bbox[3]) / 2 + 52 * progress,
            )
            # Hand the two AA halves to the growing supports quickly so the
            # thin centre stroke never hangs below the lighthouse.
            arrow_fade = max(0.0, min(1.0, (progress - 0.64) / 0.14))
            result.alpha_composite(
                with_opacity(crop, 1.0 - ease_out_cubic(arrow_fade)),
                (round(centre[0] - crop.width / 2), round(centre[1] - crop.height / 2)),
            )
        return result

    aa_source = Image.open(AA_LOGO).convert("RGBA").resize((330, 330), Image.Resampling.LANCZOS)
    aa_mask = Image.new("L", (720, 720), 0)
    aa_mask.paste(aa_source.getchannel("A"), (195, 175))
    aa_gradient = Image.new("RGBA", (720, 720), (0, 0, 0, 0))
    gradient_pixels = aa_gradient.load()
    for y in range(720):
        mix = y / 719
        colour = (round(25 - 18 * mix), round(123 - 77 * mix), round(205 - 97 * mix), 255)
        for x in range(720):
            gradient_pixels[x, y] = colour
    aa_gradient.putalpha(aa_mask)

    slide_background = (23, 23, 23, 255)
    completed = Image.new("RGBA", (720, 720), slide_background)
    for name in ("beams", "tower", "left_support", "right_support", "leaves", "roots", "waves", "top", "right", "bottom", "left"):
        completed.alpha_composite(layers[name])
    completed.convert("RGB").save(
        COMMONS_EMBLEM.with_name("technology-commons-emblem-motion-still.png"),
        optimize=True,
    )

    frames: list[Image.Image] = []
    frame_count = 60
    for index in range(frame_count):
        time = index / (frame_count - 1) * 6.2
        frame = Image.new("RGBA", (720, 720), slide_background)

        morph = max(0.0, min(1.0, (time - 0.88) / 0.82))
        aa = scale_from_anchor(aa_gradient, 1.06, 1.06, "centre")
        split_progress = max(0.0, min(1.0, (time - 1.72) / 0.82))
        if split_progress <= 0:
            frame.alpha_composite(aa)
        else:
            frame.alpha_composite(split_arrow(scale_from_anchor(aa_gradient, 1.06, 1.06, "centre"), split_progress))

        if time >= 0.88:
            lighthouse_progress = ease_out_cubic(morph)
            frame.alpha_composite(vertical_reveal(layers["tower"], lighthouse_progress, "up"))

        support_progress = max(0.0, min(1.0, (split_progress - 0.32) / 0.68))
        if support_progress > 0:
            support_reveal = ease_out_cubic(support_progress)
            frame.alpha_composite(vertical_reveal(layers["left_support"], support_reveal, "down"))
            frame.alpha_composite(vertical_reveal(layers["right_support"], support_reveal, "down"))

        if time >= 2.38:
            beam_progress = ease_out_cubic(max(0.0, min(1.0, (time - 2.38) / 0.58)))
            frame.alpha_composite(horizontal_reveal(layers["beams"], beam_progress))

        if time >= 2.86:
            root_progress = ease_out_cubic(max(0.0, min(1.0, (time - 2.86) / 0.66)))
            frame.alpha_composite(vertical_reveal(layers["roots"], root_progress, "down"))

        if time >= 3.30:
            nature_progress = ease_out_back(max(0.0, min(1.0, (time - 3.30) / 0.70)))
            frame.alpha_composite(scale_from_anchor(layers["leaves"], 0.10 + 0.90 * nature_progress, 0.78 + 0.22 * nature_progress, "centre"))
            frame.alpha_composite(scale_from_anchor(layers["waves"], 0.08 + 0.92 * nature_progress, 0.82 + 0.18 * nature_progress, "centre"))

        hand_moves = (
            ("top", -8, 3.85),
            ("right", -8, 4.25),
            ("bottom", -8, 4.65),
            ("left", -8, 5.05),
        )
        for name, angle, start in hand_moves:
            hand_progress = max(0.0, min(1.0, (time - start) / 0.85))
            if hand_progress > 0:
                frame.alpha_composite(grow_hand(layers[name], angle, hand_progress))

        frames.append(frame)

    output = COMMONS_EMBLEM.with_name("technology-commons-emblem-motion.gif")
    gif_frames = [frame.resize((480, 480), Image.Resampling.LANCZOS) for frame in frames]
    gif_frames[0].save(
        output,
        save_all=True,
        append_images=gif_frames[1:],
        duration=[103] * (len(gif_frames) - 1) + [1200],
        loop=0,
        optimize=True,
        disposal=2,
    )


def image_element(
    number: int,
    name: str,
    start: int,
    duration: int,
    x: float,
    y: float,
    width: int,
    height: int,
    in_animation: dict[str, object],
) -> dict[str, object]:
    return {
        "type": "image",
        "id": f"aa-logo-motion-starter-{number}",
        "name": name,
        "start": start,
        "duration": duration,
        "data": {
            "src": f"/files/{name}.png",
            "x": x,
            "y": y,
            "width": width,
            "height": height,
            "anchorX": 0.5,
            "anchorY": 0.5,
            "fit": "cover",
            "alpha": 1,
            "angle": 0,
            "radius": 0,
            "strokeStyle": "#000000",
            "lineWidth": 0,
            "blur": 0,
            "brightness": 1,
            "contrast": 1,
            "grayscale": 0,
            "hueRotate": 0,
            "saturate": 1,
            "sepia": 0,
        },
        "animations": {
            "in": in_animation,
            "out": {"animation": "fade", "duration": 500},
        },
        "keyframes": [],
    }


def build_smooth_project(parts: dict[str, tuple[Image.Image, tuple[int, int]]]) -> None:
    elements = [
        image_element(1, "sun", 0, 6000, 804, 247, 238, 238, {"animation": "rotate", "duration": 800, "angle": 160}),
        image_element(2, "left-peak", 450, 5550, 358, 554, 398, 330, {"animation": "slide", "duration": 900, "direction": "left", "distance": 180}),
        image_element(3, "right-peak", 800, 5200, 673, 542, 412, 355, {"animation": "slide", "duration": 900, "direction": "right", "distance": 180}),
        image_element(4, "river", 1250, 4750, 512, 774, 660, 100, {"animation": "slide", "duration": 800, "direction": "down", "distance": 120}),
    ]
    elements[0]["data"]["scale"] = 1
    elements[0]["keyframes"] = [
        {"timestamp": 2400, "easing": "linear", "data": {"scale": 1}},
        {"timestamp": 3000, "easing": "easeOutCubic", "data": {"scale": 1.08}},
        {"timestamp": 3600, "easing": "easeInOutSine", "data": {"scale": 1}},
    ]
    elements[3]["keyframes"] = [
        {"timestamp": 1800, "easing": "linear", "data": {"x": 512}},
        {"timestamp": 2400, "easing": "easeInOutSine", "data": {"x": 540}},
        {"timestamp": 3000, "easing": "easeInOutSine", "data": {"x": 512}},
    ]
    scene = {
        "settings": {"fps": 60, "color": BACKGROUND, "width": 1000, "height": 1000},
        "elements": elements,
    }
    data_path = OUTPUT / "aa-logo-motion-starter-data.json"
    data_path.write_text(json.dumps(scene, indent=2) + "\n", encoding="utf-8")

    project_path = OUTPUT / "aa-logo-motion-starter.smooth"
    with zipfile.ZipFile(project_path, "w", zipfile.ZIP_DEFLATED) as archive:
        archive.write(data_path, "data.json")
        for name in parts:
            archive.writestr(f"/files/{name}.png", (PARTS / f"{name}.png").read_bytes())


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    parts = make_part_images()
    build_previews(parts)
    build_commons_emblem_motion()
    build_smooth_project(parts)
    print(f"Built Animate Your Logo assets in {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
