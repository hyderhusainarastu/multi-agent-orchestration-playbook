import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
import guards  # noqa: E402


class GuardTests(unittest.TestCase):
    def test_require_args(self):
        self.assertEqual(guards.require_args({"a": 1}, ["a"]), {"a": 1})
        with self.assertRaises(guards.GuardError) as c:
            guards.require_args({"a": ""}, ["a", "b"])
        self.assertIn("a, b", str(c.exception))

    def test_guard_non_empty(self):
        self.assertTrue(guards.guard_non_empty("s", 0, 0))
        self.assertTrue(guards.guard_non_empty("s", 3, 1))
        with self.assertRaises(guards.GuardError):
            guards.guard_non_empty("s", 3, 0)

    def test_stage_log(self):
        log = []
        rec = guards.stage_log(log, "trim", 5, 4, "note")
        self.assertEqual(log, [rec])
        self.assertEqual((rec["items_in"], rec["items_out"]), (5, 4))

    def test_screen(self):
        items = [{"id": "a", "t": ""}, {"id": "b", "t": "x"}, {"id": "c", "t": "x", "dup": 1}]
        r = guards.screen(items, [("empty", lambda i: not i["t"]), ("dup", lambda i: i.get("dup"))])
        self.assertEqual([i["id"] for i in r["kept"]], ["b"])
        self.assertEqual(r["dropped"], {"empty": ["a"], "dup": ["c"]})

    def test_silent_drop_is_caught(self):
        # A stage that trims everything must abort the run, not report success.
        log = []
        with self.assertRaises(guards.GuardError):
            guards.run_stage(log, "trim", [{"id": 1}, {"id": 2}], lambda xs: [])
        self.assertEqual(log[0]["items_out"], 0)

    def test_run_stage_ok(self):
        log = []
        out = guards.run_stage(log, "keep", [1, 2], lambda xs: xs[:1])
        self.assertEqual(out, [1])


if __name__ == "__main__":
    unittest.main()
