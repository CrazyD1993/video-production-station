#!/usr/bin/env python3
"""Remove the already-formed bubble while preserving the exact G02 pore geometry."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter


ROOT = Path(__file__).resolve().parent
source = Image.open(ROOT / "bridge-start.png").convert("RGB")
sample = source.crop((326, 510, 406, 720)).resize((118, 300), Image.Resampling.LANCZOS)
patch = Image.new("RGB", (118, 540))
patch.paste(sample, (0, 0))
patch.paste(sample.transpose(Image.Transpose.FLIP_TOP_BOTTOM), (0, 240))
patch = Image.blend(patch, Image.new("RGB", patch.size, (33, 26, 22)), 0.22).filter(ImageFilter.GaussianBlur(2.2))
mask = Image.new("L", (158, 580), 0)
mdraw = ImageDraw.Draw(mask)
mdraw.rounded_rectangle((20, 20, 138, 560), 46, fill=255)
mask = mask.filter(ImageFilter.GaussianBlur(18))
source.paste(patch.resize((158, 580), Image.Resampling.LANCZOS), (285, 600), mask)
shade = Image.new("RGBA", source.size, (0, 0, 0, 0))
draw = ImageDraw.Draw(shade, "RGBA")
draw.rounded_rectangle((306, 620, 426, 1160), 42, fill=(26, 20, 17, 18))
source = Image.alpha_composite(source.convert("RGBA"), shade).convert("RGB")
source.save(ROOT / "b1-prestate-first-frame.png", compress_level=2)
