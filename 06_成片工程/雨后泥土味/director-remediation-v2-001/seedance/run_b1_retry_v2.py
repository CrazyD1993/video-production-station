#!/usr/bin/env python3
"""Use the final authorized call only for the B1 mechanism retry."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from seedance_client_v2 import assert_budget, build_request, create_task, download_result, extract_video_url, poll_task


ROOT = Path(__file__).resolve().parents[1]
LOG_PATH = ROOT / "seedance/call-log-v2.json"
PROMPT_PATH = ROOT / "seedance/prompts-b1-retry-v2.yaml"
FIRST_FRAME = ROOT / "mechanism-b-reference-pack-v2/b1-prestate-first-frame.png"
OUTPUT = ROOT / "seedance/outputs/B1_S09_v2-candidate-4.mp4"


def load_env(path: Path) -> None:
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if line and not line.startswith("#") and "=" in line:
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def load_prompt() -> str:
    lines = PROMPT_PATH.read_text(encoding="utf-8").splitlines()
    marker = lines.index("prompt: |")
    return " ".join(line.strip() for line in lines[marker + 1:] if line.strip())


def duration(path: Path) -> float:
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", str(path)], check=True, capture_output=True, text=True)
    return float(result.stdout.strip())


def redact(result: dict) -> dict:
    clean = json.loads(json.dumps(result))
    if isinstance(clean.get("content"), dict) and clean["content"].get("video_url"):
        clean["content"]["video_url"] = "[redacted_after_download]"
    return clean


def save(log: dict) -> None:
    LOG_PATH.write_text(json.dumps(log, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--env-file", required=True, type=Path)
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()
    load_env(args.env_file)
    api_key = os.getenv("SEEDANCE_API_KEY") or os.getenv("ARK_API_KEY") or os.getenv("VOLCENGINE_ARK_API_KEY")
    if not api_key:
        raise SystemExit("Missing Seedance API key")
    log = json.loads(LOG_PATH.read_text(encoding="utf-8"))

    if args.resume:
        record = log["calls"][-1]
        if not record.get("task_id"):
            raise SystemExit("Latest retry record has no task id")
        result = poll_task(api_key, record["task_id"])
        record["status"] = str(result.get("status", "unknown"))
        record["provider_response"] = redact(result)
        record.pop("error", None)
        if record["status"].lower() in {"succeeded", "success", "completed"}:
            download_result(extract_video_url(result), OUTPUT)
            record["original_duration"] = duration(OUTPUT)
        save(log)
        print(json.dumps({"task_id": record["task_id"], "status": record["status"], "resumed": True}, ensure_ascii=False))
        return

    assert_budget(LOG_PATH)
    prior = log["calls"][-1]
    prior["qa_decision"] = "rejected_retry_authorized"
    prior["qa_reason"] = "Geometry and rise were stable, but the result began with an existing bubble and omitted water entry, air-volume shrinkage and enclosure."
    prompt = load_prompt()
    payload = build_request(prompt, 5, reference_image=FIRST_FRAME, image_role=None)
    record = {
        "call_number": log["total_calls"] + 1,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "shot_group": "B1_S09_v2_retry",
        "task_id": None,
        "status": "requesting",
        "model": payload["model"],
        "parameters": {
            "ratio": payload["ratio"], "resolution": payload["resolution"], "duration": 5,
            "generate_audio": False, "reference_frame_used": True,
            "reference_frame_api_field": "content[].image_url (role omitted; official first-frame form)",
            "reference_frame_path": "mechanism-b-reference-pack-v2/b1-prestate-first-frame.png",
            "reference_frame_sha256": hashlib.sha256(FIRST_FRAME.read_bytes()).hexdigest()
        },
        "prompt": prompt,
        "output_path": "seedance/outputs/B1_S09_v2-candidate-4.mp4",
        "original_duration": None,
        "decision_reason": "Final authorized call used only because candidate 3 omitted the three core pre-bubble stages.",
        "cost": "unknown"
    }
    log["calls"].append(record)
    save(log)
    try:
        record["task_id"] = create_task(api_key, payload)
        record["status"] = "queued"
        log["new_calls"] += 1
        log["total_calls"] += 1
        save(log)
        result = poll_task(api_key, record["task_id"])
        record["status"] = str(result.get("status", "unknown"))
        record["provider_response"] = redact(result)
        if record["status"].lower() in {"succeeded", "success", "completed"}:
            download_result(extract_video_url(result), OUTPUT)
            record["original_duration"] = duration(OUTPUT)
        save(log)
    except Exception as exc:
        record["status"] = "request_failed" if record["task_id"] is None else "processing_failed"
        record["error"] = str(exc)
        save(log)
        raise
    print(json.dumps({"task_id": record["task_id"], "status": record["status"], "output": record["output_path"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
