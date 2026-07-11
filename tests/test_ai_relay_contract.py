import re
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
RELAY = ROOT / "00_项目总控" / "AI协作中继"


def front_matter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        raise AssertionError(f"{path} 缺少 YAML front matter")
    return yaml.safe_load(match.group(1))


class AIRelayContractTests(unittest.TestCase):
    def test_relay_files_exist(self):
        self.assertEqual(
            {"CHATGPT_TO_CODEX.md", "CODEX_TO_CHATGPT.md", "STATE.yaml"},
            {path.name for path in RELAY.iterdir() if path.is_file()},
        )

    def test_chatgpt_task_file_starts_empty(self):
        data = front_matter(RELAY / "CHATGPT_TO_CODEX.md")
        self.assertEqual(
            {
                "task_id": None,
                "status": "empty",
                "created_by": "ChatGPT",
                "target_branch": "experiment/openmontage-pilot",
                "completed_commit": None,
            },
            data,
        )

    def test_codex_receipt_has_required_sections(self):
        path = RELAY / "CODEX_TO_CHATGPT.md"
        data = front_matter(path)
        self.assertEqual("typhoon-eye-sample-planning-001", data["task_id"])
        self.assertEqual("completed", data["status"])
        self.assertEqual("experiment/openmontage-pilot", data["branch"])
        for heading in (
            "# 执行摘要", "# 修改文件", "# 实际执行的命令",
            "# 测试与验证", "# 与任务要求的差异", "# 当前阻塞点",
            "# 需要ChatGPT判断的问题", "# 完整回答",
        ):
            self.assertIn(heading, path.read_text(encoding="utf-8"))

    def test_state_contract(self):
        data = yaml.safe_load((RELAY / "STATE.yaml").read_text(encoding="utf-8"))
        self.assertEqual("experiment/openmontage-pilot", data["current_branch"])
        self.assertEqual("typhoon_eye_keyframe_plan_complete", data["project_stage"])
        self.assertEqual("keyframe_generation_approval", data["blocking_gate"])
        self.assertEqual("User", data["next_actor"])
        self.assertEqual("typhoon_eye_calm", data["approved_topic"])
        self.assertEqual("paused_no_more_image_generation", data["aircraft_window_pilot"])

    def test_three_topic_hook_packages_exist(self):
        folder = ROOT / "08_OpenMontage试验/三题并行钩子测试"
        expected = {
            "00-三题对比报告.md",
            "01-海底巨大下沉水流.md",
            "02-手指泡水起皱.md",
            "03-台风眼突然平静.md",
        }
        self.assertEqual(expected, {path.name for path in folder.glob("*.md")})
        for filename in expected - {"00-三题对比报告.md"}:
            text = (folder / filename).read_text(encoding="utf-8")
            for heading in (
                "## 事实核查清单", "## 前5秒钩子", "## 25秒高密度脚本",
                "## 三个核心镜头合同", "## 图片生成可行性", "## 风险",
                "## 推荐优先级",
            ):
                self.assertIn(heading, text)
        report = (folder / "00-三题对比报告.md").read_text(encoding="utf-8")
        self.assertIn("台风眼里为什么会突然平静", report)
        self.assertIn("选题审批门禁", report)

    def test_typhoon_eye_sample_planning_package(self):
        folder = ROOT / "08_OpenMontage试验/三题并行钩子测试/台风眼12秒样片"
        director = (folder / "00-导演方案.md").read_text(encoding="utf-8")
        candidates = (folder / "01-关键帧候选生成方案.md").read_text(encoding="utf-8")
        for shot in ("TE-S01", "TE-S02", "TE-S03"):
            self.assertIn(shot, director)
        for keyframe in ("TE-KF1", "TE-KF2", "TE-KF3"):
            self.assertIn(keyframe, director)
        self.assertIn("相对平静", director)
        self.assertIn("不声称它完整解释台风眼形成", director)
        self.assertIn("真实卫星资料：结构锚定", candidates)
        self.assertIn("ImageGen：环境质感重建", candidates)
        self.assertIn("可控图层：事实结构", candidates)
        self.assertIn("不得调用Seedance", candidates)

    def test_phase4b_manifest_and_contract_exist(self):
        handoff = ROOT / "08_OpenMontage试验/001-飞机舷窗小孔/keyframe-handoff"
        manifest = yaml.safe_load((handoff / "candidate-manifest.yaml").read_text(encoding="utf-8"))
        self.assertEqual(6, len(manifest["candidates"]))
        self.assertTrue(all(len(item["sha256"]) == 64 for item in manifest["candidates"]))
        contract = (handoff / "PHASE4B_R2_PRODUCTION_CONTRACT.md").read_text(encoding="utf-8")
        self.assertIn("KF1-R2-01", contract)
        self.assertIn("可控图层合成", contract)
        self.assertIn("完整真实舷窗", contract)

    def test_phase4_manual_generation_package(self):
        path = (
            ROOT
            / "08_OpenMontage试验/001-飞机舷窗小孔/keyframe-handoff/PHASE4_MANUAL_GENERATION.md"
        )
        text = path.read_text(encoding="utf-8")
        self.assertIn("OpenMontage 图片 Provider：0/11 configured", text)
        self.assertIn("ChatGPT 图片生成", text)
        self.assertIn("没有合规的真实客机舷窗小孔参考图", text)
        for candidate in ("KF1-01", "KF1-02", "KF2-01", "KF2-02", "KF3-01", "KF3-02"):
            self.assertIn(candidate, text)

    def test_agents_declares_relay_entrypoint(self):
        text = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("读取GitHub中继任务", text)
        self.assertIn("00_项目总控/AI协作中继/CHATGPT_TO_CODEX.md", text)
        self.assertIn("STATE.yaml", text)
        self.assertIn("archived", text)
        self.assertIn("当前阶段、当前任务、阻塞门禁、明确排除的路线", text)


if __name__ == "__main__":
    unittest.main()
