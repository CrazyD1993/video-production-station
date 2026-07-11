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
        self.assertEqual("phase4-keyframe-contact-sheet-review-001", data["task_id"])
        self.assertEqual("partially_completed", data["status"])
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
        self.assertEqual("keyframe_contact_sheet_ready", data["project_stage"])
        self.assertEqual("actual_image_contact_sheet_approval", data["blocking_gate"])
        self.assertEqual("User", data["next_actor"])
        self.assertEqual(6, data["technical_validation"]["passed"])
        self.assertEqual(0, data["technical_validation"]["failed"])
        self.assertEqual("reject_regenerate", data["candidate_review"]["KF2-01"])
        self.assertEqual("reject_regenerate", data["candidate_review"]["KF3-02"])

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


if __name__ == "__main__":
    unittest.main()
