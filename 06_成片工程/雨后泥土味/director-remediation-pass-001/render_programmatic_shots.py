#!/usr/bin/env python3
"""Render the non-Seedance remediation shots for the petrichor dynamic preview."""

from __future__ import annotations

import argparse
import json
import math
import random
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parents[2]
BOARD = PROJECT / "06_成片工程/雨后泥土味/asset-board-v1"
OUT_DIR = ROOT / "programmatic"
QA_DIR = ROOT / "qa/programmatic"
WIDTH, HEIGHT, FPS = 540, 960, 24
SHOT_FRAMES = {"S01": 29, "S05": 87, "S07": 103, "S08": 70, "S12": 113}
SHOT_EVENTS = {
    "S01": ["fall", "impact", "wet_spot"],
    "S05": ["surface", "descent", "pore_entry"],
    "S07": ["dormant", "water_wake", "geosmin"],
    "S08": ["approach", "impact"],
    "S12": ["same_composition", "wetting_spread", "rain"],
}
FONT_PATH = Path("/System/Library/Fonts/PingFang.ttc")


def font(size: int):
    return ImageFont.truetype(str(FONT_PATH), size) if FONT_PATH.exists() else ImageFont.load_default()


def cover(path: Path) -> Image.Image:
    image = Image.open(path).convert("RGB")
    scale = max(WIDTH / image.width, HEIGHT / image.height)
    resized = image.resize((round(image.width * scale), round(image.height * scale)), Image.Resampling.LANCZOS)
    left = (resized.width - WIDTH) // 2
    top = (resized.height - HEIGHT) // 2
    return resized.crop((left, top, left + WIDTH, top + HEIGHT))


def documentary_grade(image: Image.Image, underground: bool = False) -> Image.Image:
    image = ImageEnhance.Color(image).enhance(0.72)
    image = ImageEnhance.Contrast(image).enhance(1.08)
    if underground:
        tint = Image.new("RGB", image.size, (49, 35, 24))
        image = Image.blend(image, tint, 0.18)
    return image


def draw_preview_mark(image: Image.Image, shot_id: str) -> None:
    draw = ImageDraw.Draw(image, "RGBA")
    draw.rounded_rectangle((18, 18, 310, 66), 10, fill=(18, 27, 21, 175))
    draw.text((34, 30), f"{shot_id}  动态验证 · 非成片", font=font(19), fill=(239, 235, 218, 245))


def render_s01(index: int, total: int) -> Image.Image:
    base = documentary_grade(cover(BOARD / "assets/real-proxy/R07-pexels-5597653-dry-cracked-soil.jpg"))
    t = index / max(total - 1, 1)
    draw = ImageDraw.Draw(base, "RGBA")
    impact_x, impact_y = 286, 520
    if t < 0.48:
        p = t / 0.48
        y = -70 + (impact_y + 40) * (p ** 1.7)
        draw.ellipse((impact_x - 9, y - 28, impact_x + 9, y + 28), fill=(198, 218, 218, 210), outline=(244, 250, 245, 210), width=2)
        draw.line((impact_x, y - 70, impact_x, y - 28), fill=(195, 215, 210, 75), width=3)
    else:
        p = min(1.0, (t - 0.48) / 0.52)
        rx, ry = 18 + 78 * p, 7 + 34 * p
        draw.ellipse((impact_x-rx, impact_y-ry, impact_x+rx, impact_y+ry), fill=(31, 31, 24, int(105 + 65*p)))
        ring = 16 + 120 * min(p, 0.55)
        if p < 0.62:
            draw.ellipse((impact_x-ring, impact_y-ring*.32, impact_x+ring, impact_y+ring*.32), outline=(218, 225, 211, int(220*(1-p))), width=4)
        for k in range(11):
            angle = (k / 11) * math.pi * 2
            flight = math.sin(min(p / 0.55, 1) * math.pi)
            px = impact_x + math.cos(angle) * (18 + 72 * flight)
            py = impact_y - abs(math.sin(angle)) * 70 * flight + 8 * p
            radius = max(1, round(4 * (1-p)))
            draw.ellipse((px-radius, py-radius, px+radius, py+radius), fill=(213, 221, 209, int(220*(1-p))))
    draw_preview_mark(base, "S01")
    return base


def render_s05(index: int, total: int) -> Image.Image:
    t = index / max(total - 1, 1)
    surface = documentary_grade(cover(BOARD / "assets/real-proxy/R07-pexels-5597653-dry-cracked-soil.jpg"))
    roots = documentary_grade(cover(BOARD / "assets/real-proxy/R05-pexels-12763908-tree-roots-soil.jpg"), underground=True)
    blend = max(0.0, min(1.0, (t - 0.15) / 0.55))
    frame = Image.blend(surface, roots, blend)
    if t > 0.32:
        zoom = 1 + 0.28 * ((t - 0.32) / 0.68)
        crop_w, crop_h = round(WIDTH / zoom), round(HEIGHT / zoom)
        cx, cy = WIDTH // 2, round(HEIGHT * (0.46 + 0.18 * t))
        frame = frame.crop((cx-crop_w//2, cy-crop_h//2, cx+crop_w//2, cy+crop_h//2)).resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
    draw = ImageDraw.Draw(frame, "RGBA")
    water_p = max(0.0, min(1.0, (t - 0.18) / 0.72))
    surface_y = round(310 - 170 * min(t / 0.6, 1))
    draw.line((0, surface_y, WIDTH, surface_y), fill=(168, 185, 176, 95), width=5)
    for x, phase in [(154, 0.0), (268, 0.10), (384, 0.20)]:
        p = max(0.0, min(1.0, water_p - phase))
        end_y = surface_y + 540 * p
        points = [(x, surface_y), (x-18, surface_y+120*p), (x+14, surface_y+250*p), (x-8, end_y)]
        if p > 0:
            draw.line(points, fill=(130, 163, 161, 175), width=7, joint="curve")
            draw.ellipse((x-15, end_y-8, x+15, end_y+8), fill=(156, 183, 177, 110))
    if t > 0.55:
        draw.rounded_rectangle((175, 820, 365, 872), 12, fill=(26, 32, 25, 170))
        draw.text((202, 832), "水进入土壤孔隙", font=font(20), fill=(231, 229, 212, 245))
    draw_preview_mark(frame, "S05")
    return frame


def render_s07(index: int, total: int) -> Image.Image:
    t = index / max(total - 1, 1)
    base = documentary_grade(cover(BOARD / "mechanism/mechanism-a-geosmin-v1.png"), underground=True).filter(ImageFilter.GaussianBlur(0.35))
    draw = ImageDraw.Draw(base, "RGBA")
    wake = max(0.0, min(1.0, (t - 0.22) / 0.55))
    water_radius = 40 + 330 * wake
    water = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    wdraw = ImageDraw.Draw(water, "RGBA")
    wdraw.ellipse((270-water_radius, 515-water_radius*.7, 270+water_radius, 515+water_radius*.7), fill=(93, 125, 116, int(45*wake)))
    base = Image.alpha_composite(base.convert("RGBA"), water).convert("RGB")
    draw = ImageDraw.Draw(base, "RGBA")
    branches = [((130, 610), (225, 560)), ((225, 560), (305, 625)), ((225, 560), (250, 455)), ((305, 625), (405, 550)), ((250, 455), (360, 395)), ((250, 455), (170, 360))]
    visible = round(len(branches) * (0.25 + 0.75 * wake))
    for start, end in branches[:visible]:
        draw.line((*start, *end), fill=(181, 177, 145, int(95 + 80*wake)), width=2)
    rng = random.Random(707)
    particle_count = round(5 + 20 * wake)
    for i in range(particle_count):
        x = 115 + rng.random() * 330
        y = 330 + rng.random() * 350 - wake * (12 + rng.random() * 34)
        r = 1 + rng.random() * 2
        draw.ellipse((x-r, y-r, x+r, y+r), fill=(196, 183, 146, int(80 + 110*wake)))
    state = "休眠" if t < 0.28 else "被水唤醒"
    draw.rounded_rectangle((42, 790, 498, 886), 18, fill=(26, 31, 24, 185))
    draw.text((68, 808), state, font=font(21), fill=(174, 190, 177, 235))
    draw.text((68, 842), "土臭素  Geosmin", font=font(27), fill=(238, 231, 203, 250))
    draw_preview_mark(base, "S07")
    return base


def render_s08(index: int, total: int) -> Image.Image:
    t = index / max(total - 1, 1)
    base = documentary_grade(cover(BOARD / "assets/real-proxy/R07-pexels-5597653-dry-cracked-soil.jpg"), underground=True)
    draw = ImageDraw.Draw(base, "RGBA")
    impact_x, impact_y = 278, 592
    if t < 0.82:
        p = t / 0.82
        y = -80 + (impact_y + 80) * (p ** 1.45)
        size = 18 + 24 * p
        draw.ellipse((impact_x-size*.55, y-size, impact_x+size*.55, y+size), fill=(182, 207, 203, 205), outline=(231, 239, 230, 220), width=3)
        draw.line((impact_x, y-100, impact_x, y-size), fill=(173, 197, 191, 65), width=5)
    else:
        p = (t - 0.82) / 0.18
        ring = 18 + 78 * p
        draw.ellipse((impact_x-ring, impact_y-ring*.30, impact_x+ring, impact_y+ring*.30), outline=(219, 229, 215, int(220*(1-p))), width=5)
        draw.ellipse((impact_x-54, impact_y-14, impact_x+54, impact_y+30), fill=(54, 69, 59, 120))
    draw.rounded_rectangle((144, 820, 396, 872), 12, fill=(26, 32, 25, 175))
    draw.text((174, 831), "雨滴接近并撞击", font=font(21), fill=(236, 232, 215, 245))
    draw_preview_mark(base, "S08")
    return base


def render_s12(index: int, total: int) -> Image.Image:
    t = index / max(total - 1, 1)
    dry = np.array(documentary_grade(cover(BOARD / "assets/real-proxy/R07-pexels-5597653-dry-cracked-soil.jpg"))).astype(np.float32)
    yy, xx = np.mgrid[0:HEIGHT, 0:WIDTH]
    centers = [(220, 330, 0.00), (360, 565, 0.15), (145, 720, 0.28), (415, 260, 0.36)]
    mask = np.zeros((HEIGHT, WIDTH), dtype=np.float32)
    for cx, cy, delay in centers:
        p = max(0.0, min(1.0, (t-delay)/(0.78-delay))) if delay < 0.78 else 0
        radius = 18 + 380 * p
        distance = np.sqrt((xx-cx)**2 + ((yy-cy)*0.78)**2)
        mask = np.maximum(mask, np.clip((radius-distance)/70, 0, 1))
    wet = dry * np.array([0.58, 0.62, 0.64], dtype=np.float32)
    wet += np.array([2, 8, 8], dtype=np.float32)
    result = dry*(1-mask[..., None]) + wet*mask[..., None]
    frame = Image.fromarray(np.uint8(np.clip(result, 0, 255)), "RGB")
    draw = ImageDraw.Draw(frame, "RGBA")
    rng = random.Random(1212)
    rain_alpha = int(40 + 120 * min(t/0.35, 1))
    for i in range(38):
        x = (rng.randrange(-100, WIDTH+100) + index*17 + i*31) % (WIDTH+100) - 50
        y = (rng.randrange(-200, HEIGHT) + index*39 + i*47) % (HEIGHT+240) - 120
        length = 18 + rng.randrange(26)
        draw.line((x, y, x-5, y+length), fill=(200, 214, 207, rain_alpha), width=2)
    if t > 0.18:
        p = min(1.0, (t-0.18)/0.45)
        draw.ellipse((190-28*p, 310-10*p, 190+28*p, 310+10*p), fill=(177, 196, 188, int(100*p)))
    draw_preview_mark(frame, "S12")
    return frame


RENDERERS = {"S01": render_s01, "S05": render_s05, "S07": render_s07, "S08": render_s08, "S12": render_s12}


def render_shot(shot_id: str, output: Path) -> dict:
    output.parent.mkdir(parents=True, exist_ok=True)
    QA_DIR.mkdir(parents=True, exist_ok=True)
    total = SHOT_FRAMES[shot_id]
    command = [
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{WIDTH}x{HEIGHT}",
        "-r", str(FPS), "-i", "-", "-an", "-c:v", "libx264",
        "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p", str(output),
    ]
    process = subprocess.Popen(command, stdin=subprocess.PIPE)
    samples = {0, total // 2, total - 1}
    for index in range(total):
        frame = RENDERERS[shot_id](index, total)
        if index in samples:
            frame.save(QA_DIR / f"{shot_id}-{index:03d}.jpg", quality=91)
        process.stdin.write(frame.tobytes())
    process.stdin.close()
    if process.wait() != 0:
        raise RuntimeError(f"ffmpeg failed for {shot_id}")
    return {
        "shot_id": shot_id,
        "frames": total,
        "duration_seconds": total / FPS,
        "width": WIDTH,
        "height": HEIGHT,
        "fps": FPS,
        "events": SHOT_EVENTS[shot_id],
        "output": str(output.relative_to(ROOT)),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("shots", nargs="*", choices=sorted(RENDERERS), default=sorted(RENDERERS))
    args = parser.parse_args()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    records = [render_shot(shot_id, OUT_DIR / f"{shot_id}.mp4") for shot_id in args.shots]
    (QA_DIR / "render-record.json").write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(records, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
