#!/usr/bin/env python3
"""Budget-guarded Ark Seedance client for the constrained B1 v2 call."""

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
MAX_TOTAL_CALLS = 4
MAX_NEW_CALLS = 2


class BudgetExceeded(RuntimeError):
    pass


def image_data_url(path: Path) -> str:
    mime = mimetypes.guess_type(path.name)[0] or "image/png"
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{encoded}"


def build_request(prompt: str, duration: int, reference_image: Path | None = None,
                  image_role: str | None = "reference_image") -> dict:
    content = [{"type": "text", "text": prompt}]
    if reference_image is not None:
        image_item = {
            "type": "image_url",
            "image_url": {"url": image_data_url(reference_image)},
        }
        if image_role is not None:
            image_item["role"] = image_role
        content.append(image_item)
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
    if int(data.get("total_calls", 0)) >= MAX_TOTAL_CALLS:
        raise BudgetExceeded(f"Seedance hard total limit reached: {MAX_TOTAL_CALLS}")
    if int(data.get("new_calls", 0)) >= MAX_NEW_CALLS:
        raise BudgetExceeded(f"Seedance v2 new-call limit reached: {MAX_NEW_CALLS}")


def _request(api_key: str, url: str, method: str = "GET", payload: dict | None = None) -> dict:
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    request = urllib.request.Request(url, data=data, method=method, headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
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


def get_task(api_key: str, task_id: str) -> dict:
    return _request(api_key, f"{BASE_URL}/{task_id}")


def poll_task(api_key: str, task_id: str, max_wait_seconds: int = 900,
              poll_interval_seconds: float = 8) -> dict:
    deadline = time.monotonic() + max_wait_seconds
    while time.monotonic() < deadline:
        try:
            result = get_task(api_key, task_id)
        except (urllib.error.URLError, TimeoutError):
            time.sleep(poll_interval_seconds)
            continue
        status = str(result.get("status", "")).lower()
        if status in {"succeeded", "success", "completed", "failed", "cancelled", "canceled"}:
            return result
        time.sleep(poll_interval_seconds)
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
    request = urllib.request.Request(url, headers={"User-Agent": "petrichor-remediation-v2/1.0"})
    with urllib.request.urlopen(request, timeout=180) as response, output.open("wb") as handle:
        while chunk := response.read(1024 * 1024):
            handle.write(chunk)
