#!/usr/bin/env python3
"""Create one auditable, budget-guarded Seedance candidate."""

from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path

from seedance_client import (
    MAX_CALLS,
    assert_budget,
    build_request,
    create_task,
    download_result,
    extract_video_url,
    poll_task,
)


ROOT = Path(__file__).resolve().parents[1]
LOG_PATH = ROOT / "seedance" / "call-log.json"
PROMPTS = {
    "B1_S09": (
        "Photoreal macro documentary shot of a compact porous brown soil cross-section. "
        "A raindrop has just struck the surface; water pushes into one narrow pore and traps "
        "a tiny pocket of air. The air pocket closes into one small transparent bubble. "
        "End with that same bubble only beginning to rise inside the water-filled pore. "
        "Fixed camera, fixed soil geometry, restrained realistic motion, low-saturation "
        "natural earth colors, physically plausible fluid behavior. No text, no arrows, "
        "no HUD, no fluorescent particles, no science-fiction glow, no cartoon style."
    ),
    "B2_S10_S11": (
        "Continue the exact same photoreal macro documentary view of the same compact porous "
        "brown soil cross-section and the same tiny transparent bubble. The bubble starts "
        "low in the same water-filled pore, rises slowly to the wet surface, reaches the "
        "air-water boundary, then makes one subtle natural pop. The pop releases an extremely "
        "fine barely visible mist of aerosol upward, not colored molecules. Fixed camera, "
        "fixed soil geometry, restrained realistic motion, low-saturation natural earth "
        "colors, physically plausible fluid behavior. No text, no arrows, no HUD, "
        "no fluorescent particles, no science-fiction glow, no cartoon style."
    ),
}


def load_env_file(path: Path) -> None:
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        value = value.strip().strip("\"").strip("'")
        os.environ.setdefault(key.strip(), value)


def load_log() -> dict:
    if LOG_PATH.exists():
        return json.loads(LOG_PATH.read_text(encoding="utf-8"))
    return {
        "model_scope": "S09-S11 only",
        "hard_limit": MAX_CALLS,
        "total_calls": 0,
        "calls": [],
    }


def save_log(data: dict) -> None:
    for call in data.get("calls", []):
        response = call.get("provider_response")
        if isinstance(response, dict):
            content = response.get("content")
            if isinstance(content, dict) and "video_url" in content:
                content["video_url"] = "[redacted_after_download]"
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    LOG_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("shot_group", nargs="?", choices=sorted(PROMPTS))
    parser.add_argument("--env-file", type=Path)
    parser.add_argument("--duration", type=int, default=5)
    parser.add_argument("--sanitize-log", action="store_true")
    args = parser.parse_args()

    if args.sanitize_log:
        save_log(load_log())
        print("sanitized")
        return
    if not args.shot_group:
        parser.error("shot_group is required unless --sanitize-log is used")

    if args.env_file:
        load_env_file(args.env_file)
    api_key = (
        os.getenv("SEEDANCE_API_KEY")
        or os.getenv("ARK_API_KEY")
        or os.getenv("VOLCENGINE_ARK_API_KEY")
    )
    if not api_key:
        raise SystemExit("Missing SEEDANCE_API_KEY, ARK_API_KEY or VOLCENGINE_ARK_API_KEY")

    assert_budget(LOG_PATH)
    log = load_log()
    payload = build_request(PROMPTS[args.shot_group], args.duration)
    output = ROOT / "seedance" / "outputs" / f"{args.shot_group}-candidate-{log['total_calls'] + 1}.mp4"
    record = {
        "call_number": log["total_calls"] + 1,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "shot_group": args.shot_group,
        "model": payload["model"],
        "ratio": payload["ratio"],
        "resolution": payload["resolution"],
        "duration_seconds": payload["duration"],
        "generate_audio": payload["generate_audio"],
        "prompt": PROMPTS[args.shot_group],
        "task_id": None,
        "status": "requesting",
        "output_path": str(output.relative_to(ROOT)),
        "cost": "unknown",
        "decision_reason": "first-round candidate",
    }
    log["calls"].append(record)
    log["total_calls"] = len(log["calls"])
    save_log(log)

    try:
        record["task_id"] = create_task(api_key, payload)
        record["status"] = "queued"
        save_log(log)
        result = poll_task(api_key, record["task_id"])
        record["status"] = str(result.get("status", "unknown"))
        record["provider_response"] = result
        if record["status"].lower() in {"succeeded", "success", "completed"}:
            url = extract_video_url(result)
            download_result(url, output)
        save_log(log)
    except Exception as exc:
        record["status"] = "request_failed" if record["task_id"] is None else "processing_failed"
        record["error"] = str(exc)
        save_log(log)
        raise

    print(json.dumps({
        "shot_group": record["shot_group"],
        "task_id": record["task_id"],
        "status": record["status"],
        "output_path": record["output_path"],
        "cost": record["cost"],
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
