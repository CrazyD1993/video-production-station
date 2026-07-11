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
        self.assertEqual("relay-bootstrap-001", data["task_id"])
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
        self.assertEqual("ready_for_image_candidate_generation", data["project_stage"])
        self.assertEqual("actual_image_contact_sheet", data["blocking_gate"])
        self.assertEqual("ChatGPT", data["next_actor"])

    def test_agents_declares_relay_entrypoint(self):
        text = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("读取GitHub中继任务", text)
        self.assertIn("00_项目总控/AI协作中继/CHATGPT_TO_CODEX.md", text)


if __name__ == "__main__":
    unittest.main()
