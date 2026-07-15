# Production verification evidence

Date: 2026-07-15  
Scope: `petrichor-director-remediation-pass-001` production package only

## Automated tests

Command:

```sh
'06_成片工程/雨后泥土味/director-remediation-pass-001/.venv/bin/python' -m unittest discover -s '06_成片工程/雨后泥土味/director-remediation-pass-001/tests' -p 'test_*.py' -v
```

Result: `PASS` — 8 tests, 0 failures, 0 errors.

Covered contracts:

- locked S01—S13 timeline and allowed statuses;
- preview dimensions, frame rate, duration and non-final declaration;
- Seedance model/scope/specs/call budget/log fields;
- programmatic frame counts, event contracts and repository path resolution.

## Media decode

Command:

```sh
ffmpeg -v error -i '06_成片工程/雨后泥土味/director-remediation-pass-001/petrichor-director-remediation-preview-v1.mp4' -f null -
```

Result: `PASS` — exit 0, no decode error output.

FFprobe result: 46.800000 seconds, 540×960, H.264, 24/1 fps; AAC mono at 48000 Hz. Full JSON: `preview-ffprobe.json`.

## Structured files

Command: Ruby `YAML.load_file` for `shot-status.yaml` and `production-status.yaml`.  
Result: `YAML_OK`.

## Repository safety

- Secret/signed-URL value scan: `PASS`; no API key, temporary `X-Tos` credential or signature is stored.
- `.github/` diff scope: `PASS`; no GitHub Actions file changed.
- prior `reviews/asset-board-v1/` deletion check: `PASS`; no prior review evidence deleted.
- raw external downloads remain outside the repository under `/private/tmp`; only review proxies are versioned.
