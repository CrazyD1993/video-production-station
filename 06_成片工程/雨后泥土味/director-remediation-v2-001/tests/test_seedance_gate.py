import importlib.util
import json
import tempfile
import unittest
import urllib.error
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "seedance/seedance_client_v2.py"


def load_client(testcase):
    testcase.assertTrue(MODULE.is_file(), "seedance_client_v2.py 尚未实现")
    spec = importlib.util.spec_from_file_location("seedance_client_v2", MODULE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class SeedanceGateTests(unittest.TestCase):
    def test_b1_prompt_covers_locked_physics_and_prohibitions(self):
        path = ROOT / "seedance/prompts-v2.yaml"
        self.assertTrue(path.is_file(), "B1 v2 提示词尚未实现")
        text = path.read_text(encoding="utf-8")
        lower = text.lower()
        for phrase in ["water enters", "air volume shrinks", "surrounded by water", "same single bubble", "begins to rise"]:
            self.assertIn(phrase, lower)
        for phrase in ["No arrows", "No HUD", "No fluorescent", "No large bubble"]:
            self.assertIn(phrase, text)

    def test_first_new_call_is_b1_and_request_is_locked(self):
        client = load_client(self)
        request = client.build_request("water enters one soil pore", 5)
        self.assertEqual("doubao-seedance-2-0-fast-260128", request["model"])
        self.assertEqual("9:16", request["ratio"])
        self.assertEqual("720p", request["resolution"])
        self.assertEqual(5, request["duration"])
        self.assertFalse(request["generate_audio"])
        self.assertEqual([{"type": "text", "text": "water enters one soil pore"}], request["content"])

    def test_retry_can_use_official_first_frame_form_without_false_role_claim(self):
        client = load_client(self)
        reference = ROOT / "mechanism-b-reference-pack-v2/bridge-start.png"
        request = client.build_request("form one bubble", 5, reference_image=reference, image_role=None)
        image_item = request["content"][1]
        self.assertEqual("image_url", image_item["type"])
        self.assertNotIn("role", image_item)
        self.assertTrue(image_item["image_url"]["url"].startswith("data:image/png;base64,"))

    def test_budget_counts_two_previous_calls_and_allows_at_most_two_new(self):
        client = load_client(self)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "log.json"
            path.write_text(json.dumps({
                "previous_calls": 2,
                "new_calls": 2,
                "total_calls": 4,
                "calls": [{}, {}, {}, {}],
            }), encoding="utf-8")
            with self.assertRaises(client.BudgetExceeded):
                client.assert_budget(path)

    def test_poll_resumes_same_task_after_transient_network_error(self):
        client = load_client(self)
        with mock.patch.object(client, "get_task", side_effect=[
            urllib.error.URLError("temporary proxy failure"),
            {"id": "same-task", "status": "succeeded"},
        ]) as getter:
            result = client.poll_task("secret", "same-task", max_wait_seconds=2, poll_interval_seconds=0)
        self.assertEqual("succeeded", result["status"])
        self.assertEqual(2, getter.call_count)

    def test_call_log_records_real_fields_and_no_false_reference_claim(self):
        path = ROOT / "seedance/call-log-v2.json"
        self.assertTrue(path.is_file(), "call-log-v2.json 尚未实现")
        data = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(2, data["previous_calls"])
        self.assertLessEqual(data["new_calls"], 2)
        self.assertLessEqual(data["total_calls"], 4)
        self.assertGreaterEqual(len(data["calls"]), 3, "B1 v2 首次新增调用尚未执行")
        first_new = data["calls"][2]
        self.assertEqual("B1_S09_v2", first_new["shot_group"])
        for call in data["calls"]:
            for key in ["task_id", "status", "model", "parameters", "output_path", "original_duration", "decision_reason", "cost"]:
                self.assertIn(key, call)
            if call["parameters"].get("reference_frame_used"):
                self.assertTrue(call["parameters"].get("reference_frame_api_field"))


if __name__ == "__main__":
    unittest.main()
