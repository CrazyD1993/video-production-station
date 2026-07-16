#!/usr/bin/env python3
"""Seedance client with the user-overridden ten-call project ceiling."""

from __future__ import annotations

import base64
import json
import mimetypes
import time
import urllib.error
import urllib.request
from pathlib import Path

MODEL = "doubao-seedance-2-0-fast-260128"
BASE_URL = "https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks"
INHERITED_CALLS = 4
HARD_TOTAL_CALLS = 10
MAX_NEW_CALLS = HARD_TOTAL_CALLS - INHERITED_CALLS

PROMPTS = {
    "S01_SINGLE_DROP": (
        "Photoreal high-speed macro nature documentary, vertical 9:16, one continuous fixed side-view shot. "
        "The frame is filled with dry loose soil whose individual brown soil grains are clearly visible; it is not a puddle, stone, asphalt, or cracked clay plate. "
        "Within the first 1.2 seconds show one single water drop falling from above, the same drop making impact at one clear point, a short restrained splash with several real soil grains lifting, and an immediate dark wet spot spreading only around that impact point. "
        "After the event, hold on the same freshly wetted spot with a few grains settling. Natural cool overcast light, shallow depth of field, physically plausible gravity and scale, realistic transparent water. "
        "No rain shower, no second drop, no multiple ripple rings, no pre-existing puddle, no cut, no camera move, no slow floating drop, no oversized jelly drop, no text, no arrows, no HUD, no glow, no CGI or cartoon look."
    ),
    "S01_SINGLE_DROP_R2": (
        "Photoreal high-speed macro nature documentary, vertical 9:16, one continuous fixed side-view shot beginning from the supplied dry loose soil frame. Individual brown soil grains must stay sharp and physically real. "
        "Timing is mandatory: at 0.00-0.20 seconds hold the empty dry soil; at 0.20-0.55 seconds one single transparent water drop falls from above toward one clear impact point; at 0.55-0.75 seconds that same drop contacts the soil and forms a low restrained water crown; at 0.75-1.10 seconds several separate real soil grains and a few tiny water droplets visibly travel upward and outward from that exact impact point; by 1.20 seconds a dark irregular wet patch is clearly visible around the impact point while the lifted grains settle. Hold the same wet patch afterward. "
        "The water drop must not simply vanish into a clean circular drilled hole. Show contact, splash response, moving soil grains, and wetting as four distinct continuous stages. Natural cool overcast light, shallow depth of field, realistic gravity, surface tension, scale and transparent water. "
        "No rain shower, no second drop, no puddle, no ripple rings, no stone, no asphalt, no cracked clay plate, no cut, no camera move, no oversized jelly drop, no explosion, no text, no arrows, no HUD, no glow, no CGI or cartoon look."
    ),
    "MECHANISM_A": (
        "One continuous photoreal macro documentary view of the exact same vertical natural soil cross-section, fixed camera, no cuts. Real dark-brown soil grains, a few fine roots and a very small amount of pale natural mycelia remain in the same positions. "
        "Phase 1: rainwater enters from the top and visibly follows several irregular existing pores downward; this is infiltration, with the real soil remaining dominant. "
        "Phase 2: a very small amount of subdued brown organic material travels inside the thin water film, approaches nearby soil grains, then adsorbs onto their surfaces and stops; show approach, attachment, and remaining attached. "
        "Phase 3: water reaches one local patch of previously still faint mycelia; the same mycelia gently hydrate, become slightly fuller and show only subtle local activity, while a few extremely fine neutral particles appear nearby. "
        "Natural cool damp earth palette, realistic microscopic documentary texture, stable geometry, restrained motion, no text, no labels, no arrows, no neon, no fluorescent color, no glowing bacteria, no science-fiction world, no rectangular collage, no cartoon microbes, no camera transition."
    ),
    "MECHANISM_A_R2": (
        "One continuous photoreal macro nature documentary shot beginning from the supplied real root-and-soil first frame. Preserve the exact natural soil texture, irregular clumps, fine roots, root hairs, perspective and cool low light from that frame for the entire shot; fixed camera, no cuts and no scene replacement. "
        "Timing is mandatory. At 0-3 seconds, small amounts of rainwater enter from the upper edge and darken several existing irregular pore routes downward between the real clumps; never create one straight channel. At 3-7 seconds, a few tiny subdued brown organic specks move slowly within the thin water films, approach actual soil-grain surfaces, visibly attach to those surfaces and remain attached. At 7-10 seconds, water reaches one small local patch of fine pale root hairs and naturally faint mycelia; the same threads hydrate, become only slightly fuller and show restrained local activity, with several extremely fine neutral particles nearby. "
        "The real soil and roots must remain the dominant image. Physically plausible capillary water, natural dark-brown earth palette, stable geometry, documentary realism. "
        "No uniform round pellets, no bead pack, no straight central trench, no blue channel, no blue liquid, no white wire, no geometric tubes, no rectangular collage, no glowing organism, no neon, no fluorescent color, no text, no labels, no arrows, no HUD, no science-fiction look, no cartoon microbes, no camera transition."
    ),
    "S12_FIRST_RAIN": (
        "Photoreal macro nature documentary using the same cracked soil composition from the supplied first frame, fixed camera and no cut. A gentle first rain begins on drought-dry earth. "
        "Water first gathers along crack edges and low depressions, then the soil darkens irregularly along those crack edges and around individual grains; the wetting spreads unevenly by capillary action rather than as a uniform color wipe. "
        "Add only restrained real water-film reflections in a few low areas. At the end, dry and wet areas coexist clearly in the same frame. Cool overcast natural light, realistic soil texture and water. "
        "No orange, no glow, no fire, no lava, no luminous cracks, no warm golden light, no uniform full-frame color change, no text, no arrows, no HUD, no fantasy or cartoon look."
    ),
}


class BudgetExceeded(RuntimeError):
    pass


def image_data_url(path: Path) -> str:
    mime = mimetypes.guess_type(path.name)[0] or "image/jpeg"
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{encoded}"


def build_request(prompt: str, duration: int, first_frame: Path | None = None) -> dict:
    content: list[dict] = [{"type": "text", "text": prompt}]
    if first_frame is not None:
        content.append({"type": "image_url", "image_url": {"url": image_data_url(first_frame)}})
    return {
        "model": MODEL,
        "content": content,
        "ratio": "9:16",
        "resolution": "720p",
        "duration": duration,
        "generate_audio": False,
    }


def assert_budget(log_path: Path) -> None:
    if not log_path.exists():
        return
    data = json.loads(log_path.read_text(encoding="utf-8"))
    if int(data.get("total_calls", INHERITED_CALLS)) >= HARD_TOTAL_CALLS:
        raise BudgetExceeded(f"Seedance hard total limit reached: {HARD_TOTAL_CALLS}")
    if int(data.get("new_calls", 0)) >= MAX_NEW_CALLS:
        raise BudgetExceeded(f"Seedance Alpha new-call limit reached: {MAX_NEW_CALLS}")


def _request(api_key: str, url: str, method: str = "GET", payload: dict | None = None) -> dict:
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    request = urllib.request.Request(url, data=data, method=method, headers={
        "Authorization": f"Bearer {api_key}", "Content-Type": "application/json",
    })
    try:
        with urllib.request.urlopen(request, timeout=90) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Ark HTTP {exc.code}: {body}") from exc


def create_task(api_key: str, payload: dict) -> str:
    result = _request(api_key, BASE_URL, method="POST", payload=payload)
    task_id = result.get("id")
    if not task_id:
        raise RuntimeError(f"Ark response missing task id: {result}")
    return task_id


def poll_task(api_key: str, task_id: str, max_wait_seconds: int = 1200) -> dict:
    deadline = time.monotonic() + max_wait_seconds
    while time.monotonic() < deadline:
        result = _request(api_key, f"{BASE_URL}/{task_id}")
        status = str(result.get("status", "")).lower()
        if status in {"succeeded", "success", "completed", "failed", "cancelled", "canceled"}:
            return result
        time.sleep(8)
    raise TimeoutError(f"Seedance task timed out: {task_id}")


def extract_video_url(result: dict) -> str:
    content = result.get("content") or result.get("output") or result
    candidates = []
    if isinstance(content, dict):
        candidates.extend([content.get("video_url"), content.get("url")])
        if isinstance(content.get("video"), dict):
            candidates.append(content["video"].get("url"))
    if isinstance(content, list):
        for item in content:
            if isinstance(item, dict):
                candidates.extend([item.get("video_url"), item.get("url")])
    for candidate in candidates:
        if isinstance(candidate, str) and candidate.startswith("http"):
            return candidate
        if isinstance(candidate, dict) and isinstance(candidate.get("url"), str):
            return candidate["url"]
    raise RuntimeError(f"Seedance result missing video URL: {result}")


def download_result(url: str, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(url, headers={"User-Agent": "petrichor-alpha/1.0"})
    with urllib.request.urlopen(request, timeout=180) as response, output.open("wb") as handle:
        while chunk := response.read(1024 * 1024):
            handle.write(chunk)
