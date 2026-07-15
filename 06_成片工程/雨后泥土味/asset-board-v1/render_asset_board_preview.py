#!/usr/bin/env python3
"""渲染最多 20 秒的无声素材板预览，不生成完整成片。"""

from pathlib import Path
import html
import subprocess


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "petrichor-asset-board-preview-v1.mp4"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
OVERLAY_DIR = ROOT / "preview" / "overlays"


def build_overlay(index, label):
    OVERLAY_DIR.mkdir(parents=True, exist_ok=True)
    svg_path = OVERLAY_DIR / f"overlay-{index:02d}.svg"
    png_path = OVERLAY_DIR / f"overlay-{index:02d}.png"
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="540" height="960" viewBox="0 0 540 960">
<rect x="0" y="0" width="540" height="92" fill="#182019" opacity="0.72"/>
<text x="28" y="58" font-family="Hiragino Sans GB" font-size="26" fill="#F0EAD2">素材板预览 · 非成片</text>
<rect x="0" y="844" width="540" height="116" fill="#182019" opacity="0.78"/>
<text x="28" y="908" font-family="Hiragino Sans GB" font-size="24" fill="#F0EAD2">{html.escape(label)}</text>
</svg>"""
    svg_path.write_text(svg, encoding="utf-8")
    subprocess.run([
        CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--no-sandbox",
        "--default-background-color=00000000", f"--screenshot={png_path}",
        "--window-size=540,960", svg_path.as_uri(),
    ], check=True, capture_output=True)
    return png_path


def render_preview():
    inputs = [
        ("image", ROOT / "assets/real-proxy/R07-pexels-5597653-dry-cracked-soil.jpg", "S01  0.00–1.20  真实·部分取得", "normal"),
        ("video", ROOT / "assets/real-proxy/R01-pexels-13444705-rain-leaves-proxy.mp4", "S02  1.20–3.85  真实·已取得", "normal"),
        ("image", ROOT / "assets/real-proxy/R09-pexels-2905149-wet-cobblestone.jpg", "S02  石板细节  真实·已取得", "normal"),
        ("video", ROOT / "assets/real-proxy/R02-pexels-5210312-leaf-droplet-proxy.mp4", "S04  5.69–8.70  真实·已取得", "normal"),
        ("video", ROOT / "assets/real-proxy/R03-pexels-7234789-wet-soil-proxy.mp4", "S03 / S12  湿土代理  真实·已取得", "normal"),
        ("image", ROOT / "mechanism/mechanism-a-geosmin-v1.png", "S07  机制A草图  Seedance候选A", "normal"),
        ("image", ROOT / "mechanism/mechanism-b-aerosol-v1.png", "S09–S11  机制B草图  Seedance候选B", "pan"),
        ("image", ROOT / "assets/real-proxy/R08-pexels-29579839-misty-forest.jpg", "S13  39.77–46.80  真实·部分取得", "normal"),
    ]
    overlays = [build_overlay(i, item[2]) for i, item in enumerate(inputs)]
    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error"]
    for i, (kind, path, _, _) in enumerate(inputs):
        if kind == "image":
            cmd += ["-loop", "1", "-t", "2.5", "-i", str(path)]
        else:
            cmd += ["-t", "2.5", "-i", str(path)]
        cmd += ["-loop", "1", "-t", "2.5", "-i", str(overlays[i])]

    filters = []
    for i, (_, _, _, mode) in enumerate(inputs):
        if mode == "pan":
            base = "scale=1620:960,crop=540:960:x='(in_w-out_w)*t/2.5':y=0"
        else:
            base = "scale=540:960:force_original_aspect_ratio=increase,crop=540:960"
        filters.append(
            f"[{2*i}:v]{base},setsar=1,fps=24,trim=duration=2.5,setpts=PTS-STARTPTS,settb=AVTB[base{i}];"
            f"[{2*i+1}:v]format=rgba,fps=24,trim=duration=2.5,setpts=PTS-STARTPTS,settb=AVTB[overlay{i}];"
            f"[base{i}][overlay{i}]overlay=0:0:format=auto:shortest=1[v{i}]"
        )

    previous = "v0"
    for i in range(1, len(inputs)):
        current = f"x{i}"
        offset = i * 2.25
        filters.append(f"[{previous}][v{i}]xfade=transition=fade:duration=0.25:offset={offset:.2f}[{current}]")
        previous = current

    cmd += [
        "-filter_complex", ";".join(filters), "-map", f"[{previous}]", "-an",
        "-c:v", "libx264", "-profile:v", "high", "-crf", "25", "-preset", "medium",
        "-pix_fmt", "yuv420p", "-r", "24", "-movflags", "+faststart", str(OUT),
    ]
    subprocess.run(cmd, check=True)


if __name__ == "__main__":
    render_preview()
