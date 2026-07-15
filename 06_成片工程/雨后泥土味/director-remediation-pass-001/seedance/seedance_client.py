#!/usr/bin/env python3
"""Minimal budget-guarded Volcengine Ark Seedance client."""

from __future__ import annotations

import json
import time
import urllib.error
import urllib.request
from pathlib import Path


MODEL = "doubao-seedance-2-0-fast-260128"
BASE_URL = "https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks"
MAX_CALLS = 4


class BudgetExceeded(RuntimeError):
    pass


def build_request(prompt: str, duration: int) -> dict:
    return {
        "model": MODEL,
        "content": [{"type": "text", "text": prompt}],
        "ratio": "9:16",
        "resolution": "720p",
        "duration": duration,
        "generate_audio": False,
    }


def assert_budget(log_path: Path) -> None:
    if not log_path.exists():
        return
    data = json.loads(log_path.read_text(encoding="utf-8"))
    if int(data.get("total_calls", 0)) >= MAX_CALLS:
        raise BudgetExceeded(f"Seedance hard limit reached: {MAX_CALLS}")


def _request(api_key: str, url: str, method: str = "GET", payload: dict | None = None) -> dict:
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    request = urllib.request.Request(url, data=data, method=method, headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    })
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
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


def get_task(api_key: str, task_id: str) -> dict:
    return _request(api_key, f"{BASE_URL}/{task_id}")


def poll_task(api_key: str, task_id: str, max_wait_seconds: int = 900) -> dict:
    deadline = time.monotonic() + max_wait_seconds
    while time.monotonic() < deadline:
        result = get_task(api_key, task_id)
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
        video = content.get("video")
        if isinstance(video, dict):
            candidates.append(video.get("url"))
    if isinstance(content, list):
        for item in content:
            if isinstance(item, dict):
                candidates.extend([item.get("video_url"), item.get("url")])
                video = item.get("video_url")
                if isinstance(video, dict):
                    candidates.append(video.get("url"))
    for candidate in candidates:
        if isinstance(candidate, str) and candidate.startswith("http"):
            return candidate
        if isinstance(candidate, dict) and isinstance(candidate.get("url"), str):
            return candidate["url"]
    raise RuntimeError(f"Seedance result missing video URL: {result}")


def download_result(url: str, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(url, headers={"User-Agent": "petrichor-remediation/1.0"})
    with urllib.request.urlopen(request, timeout=120) as response, output.open("wb") as handle:
        while chunk := response.read(1024 * 1024):
            handle.write(chunk)
