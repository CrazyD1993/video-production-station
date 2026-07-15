#!/usr/bin/env python3
"""Run the first and normally only new Seedance call authorized by remediation V2."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from seedance_client_v2 import (
    assert_budget,
    build_request,
    create_task,
    download_result,
    extract_video_url,
    poll_task,
)


ROOT = Path(__file__).resolve().parents[1]
LOG_PATH = ROOT / "seedance/call-log-v2.json"
PROMPT_PATH = ROOT / "seedance/prompts-v2.yaml"
REFERENCE = ROOT / "mechanism-b-reference-pack-v2/bridge-start.png"
OUTPUT = ROOT / "seedance/outputs/B1_S09_v2-candidate-3.mp4"


def load_env(path: Path) -> None:
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def load_prompt() -> str:
    lines = PROMPT_PATH.read_text(encoding="utf-8").splitlines()
    marker = lines.index("prompt: |")
    return " ".join(line.strip() for line in lines[marker + 1:] if line.strip())


def redact_response(result: dict) -> dict:
    clean = json.loads(json.dumps(result))
    content = clean.get("content")
    if isinstance(content, dict) and content.get("video_url"):
        content["video_url"] = "[redacted_after_download]"
    return clean


def media_duration(path: Path) -> float:
    result = subprocess.run([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(path),
    ], check=True, capture_output=True, text=True)
    return float(result.stdout.strip())


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--env-file", required=True, type=Path)
    parser.add_argument("--resume", action="store_true", help="resume the existing task id without creating a new call")
    args = parser.parse_args()
    load_env(args.env_file)
    api_key = os.getenv("SEEDANCE_API_KEY") or os.getenv("ARK_API_KEY") or os.getenv("VOLCENGINE_ARK_API_KEY")
    if not api_key:
        raise SystemExit("Missing Seedance API key")

    log = json.loads(LOG_PATH.read_text(encoding="utf-8"))
    if args.resume:
        record = log["calls"][-1]
        task_id = record.get("task_id")
        if not task_id:
            raise SystemExit("Latest log record has no task id to resume")
        try:
            result = poll_task(api_key, task_id)
            record["status"] = str(result.get("status", "unknown"))
            record["provider_response"] = redact_response(result)
            record.pop("error", None)
            if record["status"].lower() in {"succeeded", "success", "completed"}:
                download_result(extract_video_url(result), OUTPUT)
                record["original_duration"] = media_duration(OUTPUT)
            LOG_PATH.write_text(json.dumps(log, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        except Exception as exc:
            record["status"] = "processing_failed"
            record["error"] = str(exc)
            LOG_PATH.write_text(json.dumps(log, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            raise
        print(json.dumps({"task_id": task_id, "status": record["status"], "output": record["output_path"], "resumed": True}, ensure_ascii=False))
        return

    assert_budget(LOG_PATH)
    prompt = load_prompt()
    payload = build_request(prompt, 5, reference_image=REFERENCE)
    record = {
        "call_number": log["total_calls"] + 1,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "shot_group": "B1_S09_v2",
        "task_id": None,
        "status": "requesting",
        "model": payload["model"],
        "parameters": {
            "ratio": payload["ratio"], "resolution": payload["resolution"],
            "duration": payload["duration"], "generate_audio": payload["generate_audio"],
            "reference_frame_used": True,
            "reference_frame_api_field": "content[].role=reference_image",
            "reference_frame_path": "mechanism-b-reference-pack-v2/bridge-start.png",
            "reference_frame_sha256": "361749783e721d34e3504c4f33a68da1ee44689d992377e801f688aa1219e3b6"
        },
        "prompt": prompt,
        "output_path": "seedance/outputs/B1_S09_v2-candidate-3.mp4",
        "original_duration": None,
        "decision_reason": "First new call mandated by remediation V2: rebuild B1 before any optional retry or S11 call.",
        "cost": "unknown"
    }
    log["calls"].append(record)
    LOG_PATH.write_text(json.dumps(log, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    try:
        task_id = create_task(api_key, payload)
        record["task_id"] = task_id
        record["status"] = "queued"
        log["new_calls"] = int(log.get("new_calls", 0)) + 1
        log["total_calls"] = int(log.get("total_calls", 0)) + 1
        LOG_PATH.write_text(json.dumps(log, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        result = poll_task(api_key, task_id)
        record["status"] = str(result.get("status", "unknown"))
        record["provider_response"] = redact_response(result)
        if record["status"].lower() in {"succeeded", "success", "completed"}:
            download_result(extract_video_url(result), OUTPUT)
            record["original_duration"] = media_duration(OUTPUT)
        LOG_PATH.write_text(json.dumps(log, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    except Exception as exc:
        record["status"] = "request_failed" if record["task_id"] is None else "processing_failed"
        record["error"] = str(exc)
        LOG_PATH.write_text(json.dumps(log, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        raise
    print(json.dumps({"task_id": record["task_id"], "status": record["status"], "output": record["output_path"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
