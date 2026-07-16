#!/usr/bin/env python3
"""Submit or resume one audited Seedance Alpha candidate."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from seedance_alpha_client import (
    HARD_TOTAL_CALLS, INHERITED_CALLS, MAX_NEW_CALLS, MODEL, PROMPTS,
    assert_budget, build_request, create_task, download_result, extract_video_url, poll_task,
)

ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
LOG_PATH = HERE / "call-log-alpha.json"
CONFIG = {
    "S01_SINGLE_DROP": {"duration": 5, "reference": None, "file": "S01-single-drop-candidate.mp4"},
    "S01_SINGLE_DROP_R2": {"duration": 5, "reference": HERE / "references/s01-r1-first-frame.jpg", "file": "S01-single-drop-candidate-r2.mp4"},
    "MECHANISM_A": {"duration": 10, "reference": None, "file": "mechanism-a-candidate.mp4"},
    "MECHANISM_A_R2": {"duration": 10, "reference": HERE / "references/mechanism-a-first-frame.jpg", "file": "mechanism-a-candidate-r2.mp4"},
    "S12_FIRST_RAIN": {"duration": 5, "reference": HERE / "references/s12-first-frame.jpg", "file": "S12-first-rain-candidate.mp4"},
}


def load_env(path: Path) -> None:
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if line and not line.startswith("#") and "=" in line:
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def load_log() -> dict:
    if LOG_PATH.exists():
        return json.loads(LOG_PATH.read_text(encoding="utf-8"))
    return {
        "task_id": "petrichor-alpha-finalization-001",
        "authorization": "User override: total Seedance ceiling raised from 4 to 10",
        "model": MODEL,
        "hard_total_calls": HARD_TOTAL_CALLS,
        "inherited_calls": INHERITED_CALLS,
        "max_new_calls": MAX_NEW_CALLS,
        "total_calls": INHERITED_CALLS,
        "new_calls": 0,
        "calls": [],
    }


def save(log: dict) -> None:
    clean = json.loads(json.dumps(log))
    for call in clean.get("calls", []):
        response = call.get("provider_response")
        if isinstance(response, dict) and isinstance(response.get("content"), dict):
            if response["content"].get("video_url"):
                response["content"]["video_url"] = "[redacted_after_download]"
    LOG_PATH.write_text(json.dumps(clean, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def duration(path: Path) -> float:
    result = subprocess.run([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=nw=1:nk=1", str(path),
    ], check=True, capture_output=True, text=True)
    return float(result.stdout.strip())


def finish_record(api_key: str, log: dict, record: dict, output: Path) -> None:
    result = poll_task(api_key, record["task_id"])
    record["status"] = str(result.get("status", "unknown"))
    record["provider_response"] = result
    record.pop("error", None)
    if record["status"].lower() in {"succeeded", "success", "completed"}:
        download_result(extract_video_url(result), output)
        record["original_duration"] = duration(output)
        record["output_sha256"] = hashlib.sha256(output.read_bytes()).hexdigest()
    save(log)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("group", choices=sorted(CONFIG))
    parser.add_argument("--env-file", required=True, type=Path)
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()
    load_env(args.env_file)
    api_key = os.getenv("SEEDANCE_API_KEY") or os.getenv("ARK_API_KEY") or os.getenv("VOLCENGINE_ARK_API_KEY")
    if not api_key:
        raise SystemExit("Missing Seedance API key")
    log = load_log()
    config = CONFIG[args.group]
    output = HERE / "outputs" / config["file"]

    if args.resume:
        records = [call for call in log["calls"] if call["shot_group"] == args.group]
        if not records or not records[-1].get("task_id"):
            raise SystemExit("No task id available to resume for this group")
        finish_record(api_key, log, records[-1], output)
        print(json.dumps({"task_id": records[-1]["task_id"], "status": records[-1]["status"], "resumed": True}, ensure_ascii=False))
        return

    assert_budget(LOG_PATH)
    reference = config["reference"]
    if reference is not None and not reference.exists():
        raise FileNotFoundError(reference)
    payload = build_request(PROMPTS[args.group], config["duration"], reference)
    record = {
        "call_number": log["total_calls"] + 1,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "shot_group": args.group,
        "prompt_revision": "alpha-r1-diagnosis-driven",
        "task_id": None,
        "status": "requesting",
        "model": MODEL,
        "parameters": {
            "ratio": "9:16", "resolution": "720p", "duration": config["duration"],
            "generate_audio": False, "first_frame_used": reference is not None,
            "first_frame_path": str(reference.relative_to(ROOT)) if reference else None,
        },
        "prompt": PROMPTS[args.group],
        "output_path": str(output.relative_to(ROOT)),
        "original_duration": None,
        "cost": "unknown",
        "qa_decision": "pending",
        "decision_reason": "Prompt revised against prior reviewer evidence before this call.",
    }
    log["calls"].append(record)
    save(log)
    try:
        record["task_id"] = create_task(api_key, payload)
        record["status"] = "queued"
        log["new_calls"] += 1
        log["total_calls"] += 1
        save(log)
        finish_record(api_key, log, record, output)
    except Exception as exc:
        record["status"] = "request_failed" if record["task_id"] is None else "processing_failed"
        record["error"] = str(exc)
        save(log)
        raise
    print(json.dumps({"task_id": record["task_id"], "status": record["status"], "output": record["output_path"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
