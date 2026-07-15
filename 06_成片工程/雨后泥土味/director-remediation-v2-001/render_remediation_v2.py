#!/usr/bin/env python3
"""Render the locked petrichor V2 dynamic validation package (never a final film)."""

from __future__ import annotations

import hashlib
import json
import math
import random
import shutil
import subprocess
from functools import lru_cache
from pathlib import Path


ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parents[2]
BOARD = PROJECT / "06_成片工程/雨后泥土味/asset-board-v1"
PRIOR = PROJECT / "06_成片工程/雨后泥土味/director-remediation-pass-001"
WIDTH, HEIGHT, FPS = 540, 960, 24

SCENE_IDS = {
    "S05": "soil-column-R05-v2",
    "S06": "soil-column-R05-v2",
    "S07": "soil-column-R05-v2",
}
SHOT_EVENTS = {
    "S01": ["real_impact_motion", "dry_soil", "first_drop"],
    "S05": ["surface", "traceable_infiltration", "enter_soil"],
    "S06": ["free_particles", "adsorption", "attached_particles"],
    "S07": ["water_arrival", "subtle_microbe_motion", "geosmin"],
    "S08": ["approach", "credible_impact", "pore_entry"],
    "S09": ["water_enters_pore", "air_compresses", "air_surrounded", "same_bubble_forms", "rise_begins"],
    "S10": ["same_bubble_rises", "surface_approach"],
    "S11": ["surface_contact", "film_pop", "fine_aerosol", "rapid_fade"],
    "S12": ["crack_led_wetting", "asynchronous_darkening", "multiple_impacts"],
    "S13": ["real_rain_leaves", "real_misty_forest", "slow_pullback"],
}
ALLOWED_GENERATED_ASSETS = {
    "B1_S09_v2-candidate-4.mp4",
    "B2_S10_S11-candidate-2.mp4",
}
S10_SPEED_RATIO = 1.0
G02_BRIDGE_FRAME_SHA256 = "361749783e721d34e3504c4f33a68da1ee44689d992377e801f688aa1219e3b6"

SHOT_TIMELINE = [
    ("S01", 0.00, 1.20), ("S02", 1.20, 3.85), ("S03", 3.85, 5.69),
    ("S04", 5.69, 8.70), ("S05", 8.70, 12.32), ("S06", 12.32, 17.10),
    ("S07", 17.10, 21.38), ("S08", 21.38, 24.30), ("S09", 24.30, 27.35),
    ("S10", 27.35, 30.50), ("S11", 30.50, 35.06), ("S12", 35.06, 39.77),
    ("S13", 39.77, 46.80),
]

PROGRAMMATIC = {
    "S05": 3.62, "S06": 4.78, "S07": 4.28,
    "S08": 2.92, "S11": 4.56, "S12": 4.71,
}


def reference_pack_hash(path: Path) -> str:
    data = json.loads(path.read_text(encoding="utf-8"))
    frame = path.parent / data["bridge_frame"]["file"]
    digest = hashlib.sha256(frame.read_bytes()).hexdigest()
    if digest != data["bridge_frame"]["sha256"]:
        raise ValueError("mechanism B bridge frame hash mismatch")
    return digest


def _pil():
    from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont
    return Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont


def _font(size: int):
    Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont = _pil()
    paths = [Path("/System/Library/Fonts/PingFang.ttc"), Path("/System/Library/Fonts/STHeiti Light.ttc")]
    for path in paths:
        if path.exists():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


def _cover(path: Path, size: tuple[int, int] = (WIDTH, HEIGHT)):
    Image, *_ = _pil()
    image = Image.open(path).convert("RGB")
    width, height = size
    scale = max(width / image.width, height / image.height)
    resized = image.resize((round(image.width * scale), round(image.height * scale)), Image.Resampling.LANCZOS)
    left = (resized.width - width) // 2
    top = (resized.height - height) // 2
    return resized.crop((left, top, left + width, top + height))


def _grade(image, underground: bool = False):
    Image, ImageDraw, ImageEnhance, *_ = _pil()
    image = ImageEnhance.Color(image).enhance(0.78)
    image = ImageEnhance.Contrast(image).enhance(1.10)
    if underground:
        image = Image.blend(image, Image.new("RGB", image.size, (54, 38, 25)), 0.18)
    return image


def _small_label(image, text: str):
    Image, ImageDraw, *_ = _pil()
    draw = ImageDraw.Draw(image, "RGBA")
    box = draw.textbbox((0, 0), text, font=_font(18))
    width = box[2] - box[0]
    draw.rounded_rectangle((WIDTH - width - 44, HEIGHT - 58, WIDTH - 16, HEIGHT - 17), 9, fill=(19, 22, 18, 150))
    draw.text((WIDTH - width - 30, HEIGHT - 49), text, font=_font(18), fill=(239, 234, 216, 235))


@lru_cache(maxsize=1)
def _soil_column():
    Image, ImageDraw, ImageEnhance, ImageFilter, _ = _pil()
    soil_path = BOARD / "assets/real-proxy/R04-pexels-7232905-wet-soil-macro.jpg"
    root_path = BOARD / "assets/real-proxy/R05-pexels-12763908-tree-roots-soil.jpg"
    dry_path = BOARD / "assets/real-proxy/R07-pexels-5597653-dry-cracked-soil.jpg"
    soil = _grade(_cover(soil_path), underground=True)
    dry = _grade(_cover(dry_path))
    roots = _grade(_cover(root_path), underground=True)
    canvas = Image.new("RGB", (WIDTH, 1800))
    canvas.paste(dry.crop((0, 0, WIDTH, 360)), (0, 0))
    for y in range(360, 1800, HEIGHT):
        tile = soil if (y // HEIGHT) % 2 == 0 else soil.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        canvas.paste(tile, (0, y))
    top_roots = roots.crop((0, 0, WIDTH, 760))
    region = canvas.crop((0, 120, WIDTH, 880))
    canvas.paste(Image.blend(region, top_roots, 0.64), (0, 120))
    draw = ImageDraw.Draw(canvas, "RGBA")
    root_paths = [
        [(88, 210), (130, 430), (112, 670), (156, 930), (138, 1280)],
        [(405, 180), (380, 410), (420, 690), (374, 950), (404, 1390)],
        [(248, 290), (278, 515), (246, 740), (290, 1010), (264, 1560)],
    ]
    for points in root_paths:
        draw.line(points, fill=(35, 25, 17, 210), width=18, joint="curve")
        draw.line(points, fill=(105, 82, 55, 125), width=8, joint="curve")
        draw.line([(x - 2, y) for x, y in points], fill=(158, 128, 88, 55), width=2, joint="curve")
    rng = random.Random(507)
    for _ in range(620):
        x = rng.randrange(WIDTH)
        y = rng.randrange(1800)
        r = rng.choice([1, 1, 2, 2, 3])
        color = rng.choice([(62, 44, 30, 120), (123, 92, 55, 95), (175, 139, 85, 65), (37, 29, 23, 130)])
        draw.ellipse((x-r, y-r, x+r, y+r), fill=color)
    shade = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shade, "RGBA")
    for y in range(1800):
        alpha = int(58 * min(1, y / 1100))
        sdraw.line((0, y, WIDTH, y), fill=(28, 20, 14, alpha))
    return Image.alpha_composite(canvas.convert("RGBA"), shade).convert("RGB")


def _soil_crop(y: int):
    return _soil_column().crop((0, y, WIDTH, y + HEIGHT)).copy()


def _render_s05(index: int, total: int):
    Image, ImageDraw, *_ = _pil()
    t = index / max(1, total - 1)
    crop_y = round(10 + 560 * (t * t * (3 - 2 * t)))
    frame = _soil_crop(crop_y)
    draw = ImageDraw.Draw(frame, "RGBA")
    paths = [
        [(112, 140), (126, 300), (104, 470), (146, 660), (130, 850)],
        [(274, 118), (258, 270), (288, 430), (264, 610), (290, 820)],
        [(430, 158), (408, 320), (438, 505), (405, 690), (425, 890)],
    ]
    front = 115 + 1280 * t
    for path in paths:
        translated = [(x, y - crop_y) for x, y in path if y <= front + 80 and -80 <= y - crop_y <= HEIGHT + 80]
        if len(translated) >= 2:
            draw.line(translated, fill=(38, 55, 49, 165), width=15, joint="curve")
            draw.line(translated, fill=(112, 139, 128, 115), width=4, joint="curve")
            x, y = translated[-1]
            draw.ellipse((x-8, y-5, x+8, y+5), fill=(124, 148, 137, 130))
    _small_label(frame, "水沿孔隙向下渗入")
    return frame


def _render_s06(index: int, total: int):
    Image, ImageDraw, *_ = _pil()
    t = index / max(1, total - 1)
    frame = _soil_crop(570)
    draw = ImageDraw.Draw(frame, "RGBA")
    rng = random.Random(606)
    for n in range(14):
        sx, sy = rng.randrange(70, 470), rng.randrange(140, 780)
        tx = sx + rng.randrange(-58, 59)
        ty = sy + rng.randrange(-45, 46)
        delay = n * 0.025
        p = max(0.0, min(1.0, (t - delay) / 0.72))
        eased = 1 - (1 - p) ** 3
        x = sx + (tx - sx) * eased + math.sin(t * 10 + n) * 4 * (1 - p)
        y = sy + (ty - sy) * eased
        r = 3.5 - 1.5 * p
        alpha = int(195 - 60 * p)
        draw.ellipse((x-r, y-r, x+r, y+r), fill=(185, 139, 70, alpha), outline=(225, 191, 123, alpha), width=1)
        if p > 0.82:
            draw.arc((tx-7, ty-4, tx+7, ty+4), 185, 355, fill=(205, 162, 92, 130), width=2)
    _small_label(frame, "游离物质被土粒吸附")
    return frame


def _render_s07(index: int, total: int):
    Image, ImageDraw, *_ = _pil()
    t = index / max(1, total - 1)
    frame = _soil_crop(570)
    overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay, "RGBA")
    front = 80 + 760 * min(1, t / 0.58)
    wet_paths = [[(120, 0), (132, 180), (108, 360), (146, 610)], [(280, 0), (266, 210), (292, 430), (270, 720)], [(420, 0), (405, 190), (430, 390), (410, 680)]]
    for path in wet_paths:
        visible = [(x, y) for x, y in path if y <= front]
        if len(visible) >= 2:
            draw.line(visible, fill=(57, 76, 68, 105), width=28, joint="curve")
    wake = max(0.0, min(1.0, (t - 0.30) / 0.55))
    mycelia = [((125, 650), (205, 585)), ((205, 585), (280, 628)), ((205, 585), (228, 486)), ((280, 628), (378, 554)), ((228, 486), (338, 420)), ((228, 486), (158, 392))]
    visible = round(len(mycelia) * wake)
    for start, end in mycelia[:visible]:
        draw.line((*start, *end), fill=(165, 157, 125, int(55 + 75*wake)), width=1)
    rng = random.Random(707)
    for n in range(28):
        x = 70 + rng.random() * 400 + math.sin(t * 8 + n) * 2.5 * wake
        y = 260 + rng.random() * 520 + math.cos(t * 7 + n) * 2 * wake
        r = 1.2 + rng.random() * 1.7
        alpha = int(30 + 95 * wake)
        draw.ellipse((x-r, y-r, x+r, y+r), fill=(153, 135, 96, alpha))
    frame = Image.alpha_composite(frame.convert("RGBA"), overlay).convert("RGB")
    _small_label(frame, "土臭素  Geosmin")
    return frame


def _render_s08(index: int, total: int):
    Image, ImageDraw, ImageEnhance, ImageFilter, _ = _pil()
    t = index / max(1, total - 1)
    bridge = _cover(ROOT / "mechanism-b-reference-pack-v2/b1-prestate-first-frame.png")
    zoom = 1.0 + 0.018 * math.sin(math.pi * t)
    zw, zh = round(WIDTH * zoom), round(HEIGHT * zoom)
    base = bridge.resize((zw, zh), Image.Resampling.LANCZOS).crop(((zw-WIDTH)//2, (zh-HEIGHT)//2, (zw+WIDTH)//2, (zh+HEIGHT)//2))
    layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer, "RGBA")
    impact_y = 245
    if t < 0.62:
        p = t / 0.62
        y = -65 + (impact_y + 65) * (p ** 1.5)
        w = 12 + 6 * p
        h = 25 + 11 * p
        for ring in range(5, 0, -1):
            alpha = 12 + ring * 9
            draw.ellipse((270-w-ring, y-h-ring, 270+w+ring, y+h+ring), fill=(108, 139, 150, alpha))
        draw.ellipse((270-w, y-h, 270+w, y+h), fill=(90, 118, 126, 85), outline=(222, 230, 222, 155), width=2)
        draw.arc((272-w*.7, y-h*.75, 272+w*.2, y-h*.05), 195, 325, fill=(247, 247, 238, 195), width=2)
    else:
        p = min(1.0, (t - 0.62) / 0.38)
        draw.arc((205-95*p, impact_y-24-18*p, 335+95*p, impact_y+24+18*p), 195, 345, fill=(224, 231, 219, int(165*(1-p))), width=2)
        tongue = 30 + 260 * p
        alpha = int(118 * math.sin(math.pi * p))
        points = [(270, impact_y+5), (265, impact_y+tongue*.34), (274, impact_y+tongue*.72), (268, impact_y+tongue)]
        draw.line(points, fill=(95, 121, 119, alpha), width=11, joint="curve")
        draw.line(points, fill=(211, 223, 215, alpha//3), width=2, joint="curve")
    return Image.alpha_composite(base.convert("RGBA"), layer).convert("RGB")


def _render_s11(index: int, total: int):
    Image, ImageDraw, *_ = _pil()
    t = index / max(1, total - 1)
    contact = _cover(ROOT / "mechanism-b-reference-pack-v2/surface-contact.png")
    after = _cover(ROOT / "mechanism-b-reference-pack-v2/surface-after.png")
    fade = max(0.0, min(1.0, (t - 0.18) / 0.34))
    fade = fade * fade * (3 - 2 * fade)
    source = Image.blend(contact, after, fade)
    zoom = 1 + 0.012 * t
    zw, zh = round(WIDTH*zoom), round(HEIGHT*zoom)
    frame = source.resize((zw, zh), Image.Resampling.LANCZOS).crop(((zw-WIDTH)//2, (zh-HEIGHT)//2, (zw+WIDTH)//2, (zh+HEIGHT)//2))
    layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer, "RGBA")
    cx, cy = 270, 255
    if t < 0.18:
        p = t / 0.18
        draw.arc((cx-62-10*p, cy-26-5*p, cx+62+10*p, cy+30+5*p), 185, 355, fill=(245, 245, 236, int(150*(1-p))), width=2)
    else:
        p = min(1.0, (t-0.18)/0.82)
        ring = 20 + 125 * min(1, p/0.45)
        draw.arc((cx-ring, cy-12-ring*.16, cx+ring, cy+12+ring*.16), 185, 355, fill=(232, 236, 225, int(125*(1-p))), width=2)
        rng = random.Random(1111)
        for n in range(34):
            launch = 0.03 * (n % 8)
            q = max(0.0, min(1.0, (p-launch)/0.72))
            if q <= 0:
                continue
            angle = rng.uniform(-1.18, -0.38)
            speed = rng.uniform(85, 230)
            x = cx + math.cos(angle)*speed*q + rng.uniform(-10, 10)
            y = cy + math.sin(angle)*speed*q + 60*q*q
            r = rng.choice([1.0, 1.2, 1.5, 2.0]) * (1-q*.35)
            alpha = int(130 * (1-q) * min(1, q*8))
            draw.ellipse((x-r, y-r, x+r, y+r), fill=(220, 228, 222, alpha))
    return Image.alpha_composite(frame.convert("RGBA"), layer).convert("RGB")


@lru_cache(maxsize=1)
def _s12_arrays():
    import numpy as np
    Image, ImageDraw, ImageEnhance, ImageFilter, _ = _pil()
    dry_image = _grade(_cover(BOARD / "assets/real-proxy/R07-pexels-5597653-dry-cracked-soil.jpg"))
    gray = dry_image.convert("L")
    crack = gray.point(lambda value: 255 if value < 72 else 0).filter(ImageFilter.MaxFilter(17))
    crack_arr = np.asarray(crack).astype(np.float32) / 255.0
    dry = np.asarray(dry_image).astype(np.float32)
    yy, xx = np.mgrid[0:HEIGHT, 0:WIDTH]
    noise = (np.sin(xx*0.071 + yy*0.023) + np.sin(xx*0.019 - yy*0.047) + 2) / 4
    arrival = 0.18 + 0.56*(yy/HEIGHT) + 0.26*noise - 0.30*crack_arr
    wet = dry * np.array([0.54, 0.58, 0.60], dtype=np.float32) + np.array([5, 6, 5], dtype=np.float32)
    return dry, wet, crack_arr, arrival


def _render_s12(index: int, total: int):
    import numpy as np
    Image, ImageDraw, *_ = _pil()
    t = index / max(1, total - 1)
    dry, wet, crack_arr, arrival = _s12_arrays()
    edge = np.clip((t - arrival + 0.10) / 0.20, 0, 1)
    edge = np.maximum(edge, crack_arr * np.clip((t-0.08)/0.42, 0, 1))
    result = dry*(1-edge[..., None]) + wet*edge[..., None]
    frame = Image.fromarray(np.uint8(np.clip(result, 0, 255)), "RGB")
    draw = ImageDraw.Draw(frame, "RGBA")
    rng = random.Random(1212)
    for n in range(26):
        delay = (n % 9) * 0.08
        q = max(0.0, min(1.0, (t-delay)/0.45))
        if q <= 0:
            continue
        x = rng.randrange(15, WIDTH-15)
        y = rng.randrange(20, HEIGHT-80)
        draw.line((x+7, y-24, x, y), fill=(195, 210, 204, int(95*(1-q))), width=1)
        if q < 0.42:
            r = 2 + 18*q
            draw.arc((x-r, y-r*.25, x+r, y+r*.25), 185, 355, fill=(210, 219, 210, int(125*(1-q))), width=1)
    _small_label(frame, "雨水先沿裂缝与低处扩散")
    return frame


FRAME_RENDERERS = {
    "S05": _render_s05, "S06": _render_s06, "S07": _render_s07,
    "S08": _render_s08, "S11": _render_s11, "S12": _render_s12,
}


def render_frame(shot_id: str, index: int, total: int):
    return FRAME_RENDERERS[shot_id](index, total)


def _run(command: list[str]) -> None:
    subprocess.run(command, check=True)


def render_programmatic_shot(shot_id: str, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    duration = PROGRAMMATIC[shot_id]
    total = round(duration * FPS)
    command = [
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{WIDTH}x{HEIGHT}",
        "-r", str(FPS), "-i", "-", "-an", "-c:v", "libx264",
        "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p", str(output),
    ]
    process = subprocess.Popen(command, stdin=subprocess.PIPE)
    for index in range(total):
        process.stdin.write(render_frame(shot_id, index, total).tobytes())
    process.stdin.close()
    if process.wait() != 0:
        raise RuntimeError(f"ffmpeg failed for {shot_id}")


def render_all_programmatic() -> None:
    for shot_id in PROGRAMMATIC:
        render_programmatic_shot(shot_id, ROOT / "work/shots" / f"{shot_id}.mp4")


def _fit(extra: str = "") -> str:
    chain = f"scale={WIDTH}:{HEIGHT}:force_original_aspect_ratio=increase,crop={WIDTH}:{HEIGHT},fps={FPS},setsar=1"
    if extra:
        chain += "," + extra
    return chain + ",format=yuv420p"


def _encode_source(source: Path, output: Path, duration: float, start: float = 0.0,
                   image: bool = False, extra_filter: str = "") -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    command = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error"]
    if image:
        command += ["-loop", "1"]
    elif start:
        command += ["-ss", f"{start:.3f}"]
    command += ["-i", str(source), "-vf", _fit(extra_filter), "-an", "-t", f"{duration:.3f}",
                "-r", str(FPS), "-c:v", "libx264", "-preset", "medium", "-crf", "20",
                "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(output)]
    _run(command)


def _concat(parts: list[Path], output: Path, duration: float) -> None:
    listing = ROOT / "work" / f"{output.stem}-concat.txt"
    listing.write_text("".join(f"file '{part.resolve()}'\n" for part in parts), encoding="utf-8")
    _run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-f", "concat", "-safe", "0",
        "-i", str(listing), "-an", "-vf", f"fps={FPS},format=yuv420p",
        "-t", f"{duration:.3f}", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
        "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(output),
    ])


def _build_s01(output: Path) -> None:
    dry = BOARD / "assets/real-proxy/R07-pexels-5597653-dry-cracked-soil.jpg"
    impact = PRIOR / "assets/real-proxy/R11-pexels-4171514-ground-rain-impact-proxy.mp4"
    _run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-loop", "1", "-i", str(dry),
        "-i", str(impact), "-filter_complex",
        f"[0:v]{_fit('eq=saturation=0.82:contrast=1.08')}[dry];"
        f"[1:v]{_fit('eq=saturation=0.55:contrast=1.12')}[rain];"
        "[dry][rain]blend=all_expr='A*0.78+B*0.22',eq=brightness=-0.015:contrast=1.04[out]",
        "-map", "[out]", "-an", "-t", "1.200", "-r", str(FPS), "-c:v", "libx264",
        "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p", str(output),
    ])


def _build_s02(output: Path) -> None:
    assets = BOARD / "assets/real-proxy"
    pieces = [
        (assets / "R01-pexels-13444705-rain-leaves-proxy.mp4", False, 0.00),
        (assets / "R09-pexels-2905149-wet-cobblestone.jpg", True, 0.00),
        (assets / "R03-pexels-7234789-wet-soil-proxy.mp4", False, 0.40),
    ]
    durations = [0.88, 0.88, 0.89]
    parts = []
    for index, ((source, image, start), duration) in enumerate(zip(pieces, durations)):
        part = ROOT / "work/montage" / f"S02-{index}.mp4"
        _encode_source(source, part, duration, start=start, image=image)
        parts.append(part)
    _concat(parts, output, 2.65)


def _build_s09(output: Path) -> None:
    b1 = ROOT / "seedance/outputs/B1_S09_v2-candidate-4.mp4"
    bridge = ROOT / "mechanism-b-reference-pack-v2/bridge-start.png"
    _run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(b1), "-loop", "1", "-i", str(bridge),
        "-filter_complex",
        f"[0:v]trim=start=0:end=3.05,setpts=PTS-STARTPTS,{_fit()}[a];"
        f"[1:v]trim=duration=0.375,setpts=PTS-STARTPTS,{_fit()}[b];"
        "[a][b]xfade=transition=fade:duration=0.375:offset=2.675[out]",
        "-map", "[out]", "-an", "-t", "3.050", "-r", str(FPS), "-c:v", "libx264",
        "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p", str(output),
    ])


def _build_s13(output: Path) -> None:
    r13 = PRIOR / "assets/real-proxy/R13-pexels-32679329-rain-leaves-forest-proxy.mp4"
    r12 = PRIOR / "assets/real-proxy/R12-pexels-32675101-misty-forest-motion-proxy.mp4"
    _run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(r13), "-i", str(r12),
        "-filter_complex",
        f"[0:v]trim=start=0:end=3.715,setpts=PTS-STARTPTS,{_fit('eq=saturation=0.78:contrast=1.04')}[a];"
        f"[1:v]trim=start=0:end=3.715,setpts=PTS-STARTPTS,{_fit('eq=saturation=0.78:contrast=1.04')}[b];"
        "[a][b]xfade=transition=fade:duration=0.400:offset=3.315[out]",
        "-map", "[out]", "-an", "-t", "7.030", "-r", str(FPS), "-c:v", "libx264",
        "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", str(output),
    ])


def build_package_media() -> None:
    shots = ROOT / "work/shots"
    montage = ROOT / "work/montage"
    shots.mkdir(parents=True, exist_ok=True)
    montage.mkdir(parents=True, exist_ok=True)
    assets = BOARD / "assets/real-proxy"

    _build_s01(shots / "S01.mp4")
    _build_s02(shots / "S02.mp4")
    _encode_source(assets / "R04-pexels-7232905-wet-soil-macro.jpg", shots / "S03.mp4", 1.84, image=True,
                   extra_filter="zoompan=z='min(zoom+0.0005,1.035)':d=1:s=540x960")
    _encode_source(ROOT / "assets/real-proxy/R14-mixkit-100912-leaf-tip-droplets-proxy.mp4", shots / "S04.mp4", 3.01)
    for shot_id, duration in [("S05", 3.62), ("S06", 4.78), ("S07", 4.28), ("S08", 2.92), ("S11", 4.56), ("S12", 4.71)]:
        raw = shots / f"{shot_id}.mp4"
        exact = ROOT / "work/exact" / f"{shot_id}.mp4"
        _encode_source(raw, exact, duration)
        shutil.move(exact, raw)
    _build_s09(shots / "S09.mp4")
    _encode_source(PRIOR / "seedance/outputs/B2_S10_S11-candidate-2.mp4", shots / "S10.mp4", 3.15)
    _build_s13(shots / "S13.mp4")

    ordered = [shots / f"S{index:02d}.mp4" for index in range(1, 14)]
    _concat(ordered[4:7], ROOT / "mechanism-a-v2.mp4", 12.68)
    _concat(ordered[7:11], ROOT / "mechanism-b-v2.mp4", 13.68)
    _concat(ordered, ROOT / "petrichor-remediation-v2-clean-preview.mp4", 46.80)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["programmatic", "build", "all"], default="programmatic", nargs="?")
    args = parser.parse_args()
    if args.command == "programmatic":
        render_all_programmatic()
    elif args.command == "build":
        build_package_media()
    else:
        render_all_programmatic()
        build_package_media()
