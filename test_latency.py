import copy
import json
from pathlib import Path
import unittest

from latency import jitter_window_ms, measure


TRACES = json.loads(Path(__file__).with_name("traces.json").read_text())


class LatencyTests(unittest.TestCase):
    def test_three_different_waits_with_same_model(self):
        results = [measure(t) for t in TRACES]
        self.assertEqual([r["llm_ttft_ms"] for r in results], [180, 180, 180])
        self.assertEqual([r["first_playback_ms"] for r in results], [680, 1130, 1050])
        self.assertEqual([r["useful_playback_ms"] for r in results], [680, 1130, 1700])

    def test_missing_is_not_zero(self):
        trace = copy.deepcopy(TRACES[0])
        trace["events"] = [e for e in trace["events"] if e["name"] != "playback_stopped"]
        with self.assertRaises(ValueError):
            measure(trace)

    def test_mixed_clocks_rejected(self):
        trace = copy.deepcopy(TRACES[0])
        trace["events"][-1]["clock"] = "server"
        with self.assertRaises(ValueError):
            measure(trace)

    def test_duplicate_rejected(self):
        trace = copy.deepcopy(TRACES[0])
        trace["events"].append(trace["events"][-1])
        with self.assertRaises(ValueError):
            measure(trace)

    def test_unordered_and_invalid_rejected(self):
        for value in (-1, float("nan"), float("inf"), "5", True):
            trace = copy.deepcopy(TRACES[0])
            trace["events"][-1]["ms"] = value
            with self.assertRaises(ValueError):
                measure(trace)

    def test_window_uses_counter_differences(self):
        self.assertAlmostEqual(jitter_window_ms(
            {"id": "audio", "delay_s": 12, "count": 1000},
            {"id": "audio", "delay_s": 15, "count": 1100}), 30)

    def test_no_samples_is_unknown(self):
        point = {"id": "audio", "delay_s": 12, "count": 1000}
        self.assertIsNone(jitter_window_ms(point, point))

    def test_counter_reset_and_changed_object_rejected(self):
        before = {"id": "audio", "delay_s": 12, "count": 1000}
        for after in ({"id": "audio", "delay_s": 1, "count": 1},
                      {"id": "new", "delay_s": 15, "count": 1100}):
            with self.assertRaises(ValueError):
                jitter_window_ms(before, after)


if __name__ == "__main__":
    unittest.main()
