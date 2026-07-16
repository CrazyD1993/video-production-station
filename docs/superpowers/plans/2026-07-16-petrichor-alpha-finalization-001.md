# Petrichor Alpha Finalization Implementation Plan

> **For Codex:** Execute sequentially with test-first changes. The user-approved relay is the design authority.

**Goal:** Produce a complete, audible 46.80-second Alpha with corrected visuals, traceable licensing, CFR 24fps media, and independent A/B/C review without new paid generation.

**Architecture:** A small Python renderer owns the locked 1123-frame timeline, deterministic mechanism scenes, subtitles, manifest, and QA. FFmpeg performs source normalization and final H.264/AAC assembly. Tests own the frame budget, source graph, audio invariants, scene behavior metadata, and zero-paid-call gate.

**Tech Stack:** Python 3, Pillow, NumPy, OpenCV when available, FFmpeg/FFprobe, unittest/pytest, YAML/CSV/JSON.

---

### Task 1: Establish contract tests

**Files:**
- Create: `06_成片工程/雨后泥土味/petrichor-alpha-finalization-001/tests/test_alpha_contract.py`
- Create: `06_成片工程/雨后泥土味/petrichor-alpha-finalization-001/tests/test_manifest_contract.py`
- Create: `06_成片工程/雨后泥土味/petrichor-alpha-finalization-001/tests/test_renderer_contract.py`

**Steps:**
1. Write tests for 13 locked shots, exact per-shot frame counts summing 1123, 24fps, 720×1280, narration hash/duration, 0.20s narration offset, and forbidden paid-call strings.
2. Write tests for recursive dependency rows, corrected CSV column count, R14 license evidence, source/use timecodes, speed ratios, and scene-group reuse disclosure.
3. Write tests for required mechanism event metadata: S01 three phases, mechanism A continuity, S09 cavity origin, S10 speed 1.000, S11 2–4 rupture frames, S12 no warm glow and retained dry fraction.
4. Run tests and verify RED because implementation modules/files do not exist.

### Task 2: Implement timeline and source graph

**Files:**
- Create: `06_成片工程/雨后泥土味/petrichor-alpha-finalization-001/alpha_config.py`
- Create: `06_成片工程/雨后泥土味/petrichor-alpha-finalization-001/build_manifest.py`
- Create: `06_成片工程/雨后泥土味/petrichor-alpha-finalization-001/licenses/*.md`

**Steps:**
1. Implement only the constants and source-graph API required by the failing tests.
2. Record the two newly selected free sources with direct page URL, author, platform, license type, access date, and evidence snapshot.
3. Expand all derived IDs to underlying source IDs and actual appearances.
4. Run contract and manifest tests until GREEN.

### Task 3: Acquire and normalize two allowed real sources

**Files:**
- Local-only raw: `/private/tmp/petrichor-alpha-sources/*`
- Create ignored normalized intermediates under `.../petrichor-alpha-finalization-001/work/`

**Steps:**
1. Download one CC/free real single-drop soil-impact source and one free real vertical soil-profile source only after license verification.
2. Inspect frames and reject any source that does not visibly satisfy the assigned action.
3. Normalize selected excerpts to CFR 24fps without altering locked narration.
4. Record SHA-256, original/use timecodes, crop, and speed ratio; never commit raw source files.

### Task 4: Implement deterministic visual repairs

**Files:**
- Create: `06_成片工程/雨后泥土味/petrichor-alpha-finalization-001/render_alpha.py`
- Create: `06_成片工程/雨后泥土味/petrichor-alpha-finalization-001/render_mechanisms.py`

**Steps:**
1. Implement S01 extraction/crop so fall, contact, and response remain visible within 29 frames.
2. Implement one continuous S05–S07 scene using real soil as base and restrained deterministic infiltration/adsorption/local wake overlays.
3. Implement S09 prestate and S11 rupture/rebound around the fixed S10/G02 geometry; preserve G02 at speed 1.000.
4. Implement S12 irregular crack-following darkening with cool specular highlights and dry/wet coexistence.
5. Implement restrictive grade normalization for retained shots.
6. Run renderer behavior tests until GREEN.

### Task 5: Build audible Alpha and QA evidence

**Files:**
- Create: `.../petrichor-alpha-v1.mp4`
- Create: `.../mechanism-a-final.mp4`
- Create: `.../mechanism-b-final.mp4`
- Create: `.../temporary-review-subtitles.srt`
- Create: `.../asset-dependency-manifest.csv`
- Create: `.../dependencies.yaml`
- Create: `.../qa/*`

**Steps:**
1. Render all 1123 video frames and CFR mechanism deliverables.
2. Derive unchanged subtitle text/times from the locked timestamp JSON with +0.20s offset.
3. Mix original-speed locked narration with existing low-level ambience and mux H.264/AAC Alpha to 46.80s.
4. Run FFprobe, full decode, packet PTS continuity, narration comparison, SHA-256, midpoint contact sheet, and dense evidence sheets for S01/S05–S07/S09–S12.
5. Run full tests and verify all required outputs.

### Task 6: Production commit and independent review

**Files:**
- Create/update production report/status in Alpha directory.
- Create: `06_成片工程/雨后泥土味/reviews/petrichor-alpha-finalization-001/*`

**Steps:**
1. Re-read the relay checklist, verify no paid calls/new Seedance outputs, then commit and push `production_commit`.
2. Provide Reviewer A and Reviewer B an immutable snapshot of that commit; require independent reports before either sees production self-evaluation or the other report.
3. Require Reviewer B to view the audible Alpha at normal speed and inspect dense evidence frames.
4. After A/B finish, give only their reports and the snapshot to Reviewer C for arbitration.
5. Record review decision without auto-fixing production assets.

### Task 7: Relay and final verification

**Files:**
- Update: `00_项目总控/AI协作中继/CHATGPT_TO_CODEX.md`
- Overwrite: `00_项目总控/AI协作中继/CODEX_TO_CHATGPT.md`
- Update: `00_项目总控/AI协作中继/STATE.yaml`

**Steps:**
1. Keep `human_final_decision: pending` and `release_master_started: false`.
2. Set relay status to completed and include both production/review SHAs and output/report paths.
3. Run fresh tests, media decode/PTS checks, UTF-8 checks, `git diff --check`, and branch-status verification.
4. Commit review/relay files, push `experiment/openmontage-pilot`, verify remote SHA and UTF-8 Chinese readability, then stop.
