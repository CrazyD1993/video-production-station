import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "seedance/seedance_client.py"


def load_client():
    spec = importlib.util.spec_from_file_location("seedance_client", MODULE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class SeedanceClientTests(unittest.TestCase):
    def test_request_is_locked_to_authorized_model_and_specs(self):
        client = load_client()
        request = client.build_request("physical bubble motion", 5)
        self.assertEqual("doubao-seedance-2-0-fast-260128", request["model"])
        self.assertEqual("9:16", request["ratio"])
        self.assertEqual("720p", request["resolution"])
        self.assertEqual(5, request["duration"])
        self.assertFalse(request["generate_audio"])
        self.assertEqual([{"type": "text", "text": "physical bubble motion"}], request["content"])

    def test_budget_refuses_fifth_call(self):
        client = load_client()
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "log.json"
            path.write_text(json.dumps({"total_calls": 4, "calls": [{}, {}, {}, {}]}), encoding="utf-8")
            with self.assertRaises(client.BudgetExceeded):
                client.assert_budget(path)


if __name__ == "__main__":
    unittest.main()
