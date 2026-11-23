import json
import os
import subprocess
import sys
import tempfile
import unittest

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
TOOLS = os.path.join(ROOT, "tools")


def run(script, *args):
    return subprocess.run([sys.executable, os.path.join(TOOLS, script), *args],
                          capture_output=True, text=True)


def write(d, name, text):
    p = os.path.join(d, name)
    with open(p, "w", encoding="utf-8") as f:
        f.write(text)
    return p


class CoverageTests(unittest.TestCase):
    def test_ok(self):
        with tempfile.TemporaryDirectory() as d:
            e = write(d, "e.txt", "a\nb\nc\n")
            r = run("shard_coverage_check.py", "--expected", e,
                    write(d, "s1.txt", "a\nb\n"), write(d, "s2.txt", "c\n"))
            self.assertEqual(r.returncode, 0, r.stdout)

    def test_gap_dup_extra(self):
        with tempfile.TemporaryDirectory() as d:
            e = write(d, "e.txt", "a\nb\nc\nd\n")
            r = run("shard_coverage_check.py", "--expected", e,
                    write(d, "s1.txt", "a\nb\n"), write(d, "s2.txt", "b\nc\nz\n"))
            self.assertEqual(r.returncode, 1)
            self.assertIn("GAPS (1): d", r.stdout)
            self.assertIn("DUPLICATES (1): b", r.stdout)
            self.assertIn("EXTRAS (1): z", r.stdout)

    def test_json_list_and_usage(self):
        with tempfile.TemporaryDirectory() as d:
            e = write(d, "e.json", json.dumps(["a", "b"]))
            r = run("shard_coverage_check.py", "--expected", e, write(d, "s.json", '["a","b"]'))
            self.assertEqual(r.returncode, 0)
            self.assertEqual(run("shard_coverage_check.py").returncode, 2)
            self.assertEqual(run("shard_coverage_check.py", "--expected", "/nonexistent", "x").returncode, 2)

    def test_bundled_example(self):
        ex = os.path.join(ROOT, "examples")
        r = run("shard_coverage_check.py", "--expected", os.path.join(ex, "ids.txt"),
                os.path.join(ex, "shard-a.txt"), os.path.join(ex, "shard-b.txt"))
        self.assertEqual(r.returncode, 1)
        self.assertIn("GAPS (1): item-004", r.stdout)
        self.assertIn("item-002", r.stdout)


class CapsTests(unittest.TestCase):
    def state(self, d, used):
        caps = {"rounds": {"max": 3, "used": used}, "hops": {"max": 5, "used": 0}}
        return write(d, "state.json", json.dumps({"caps": caps}))

    def test_headroom_and_reached(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(run("check_caps.py", self.state(d, 2)).returncode, 0)
            r = run("check_caps.py", self.state(d, 3))
            self.assertEqual(r.returncode, 3)
            self.assertIn("rounds 3/3", r.stdout)

    def test_malformed(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(run("check_caps.py", write(d, "s.json", "{}")).returncode, 2)
            self.assertEqual(run("check_caps.py", write(d, "t.json", "not json")).returncode, 2)

    def test_template_state_has_headroom(self):
        self.assertEqual(run("check_caps.py", os.path.join(ROOT, "templates", "state.json")).returncode, 0)


def conforms(value, schema):
    """Tiny JSON-schema subset: type, required, properties, items, enum, minimum."""
    t = schema.get("type")
    types = {"object": dict, "array": list, "string": str, "integer": int, "number": (int, float), "boolean": bool}
    if t and not (isinstance(value, types[t]) and not (t == "integer" and isinstance(value, bool))):
        return False
    if "enum" in schema and value not in schema["enum"]:
        return False
    if "minimum" in schema and value < schema["minimum"]:
        return False
    if t == "object":
        if any(k not in value for k in schema.get("required", [])):
            return False
        return all(conforms(value[k], s) for k, s in schema.get("properties", {}).items() if k in value)
    if t == "array" and "items" in schema:
        return all(conforms(v, schema["items"]) for v in value)
    return True


class SchemaTests(unittest.TestCase):
    def load(self, name):
        with open(os.path.join(ROOT, "templates", name), encoding="utf-8") as f:
            return json.load(f)

    def test_state_example_conforms(self):
        self.assertTrue(conforms(self.load("state.json"), self.load("state.schema.json")))

    def test_state_bad_rejected(self):
        bad = self.load("state.json")
        bad["stages"][0]["items_in"] = "many"
        self.assertFalse(conforms(bad, self.load("state.schema.json")))

    def test_other_schemas_parse(self):
        for n in ("pilot-scorecard.schema.json", "explorer-proposal.schema.json"):
            s = self.load(n)
            self.assertEqual(s["type"], "object")
            self.assertIn("required", s)

    def test_examples_conform(self):
        ex = os.path.join(ROOT, "examples", "library-datasets")
        for schema, ex_name in (("explorer-proposal.schema.json", "proposal.json"),
                                ("pilot-scorecard.schema.json", "scorecard.json")):
            with open(os.path.join(ex, ex_name), encoding="utf-8") as f:
                self.assertTrue(conforms(json.load(f), self.load(schema)), ex_name)


class PromptSizeTests(unittest.TestCase):
    def size(self, name):
        with open(os.path.join(ROOT, name), encoding="utf-8") as f:
            return len(f.read())

    def test_prompt_limits(self):
        self.assertLessEqual(self.size("PROMPT.md"), 6000)
        self.assertLessEqual(self.size("PROMPT.short.md"), 1400)

    def test_agents_template_limit(self):
        with open(os.path.join(ROOT, "templates", "AGENTS.md"), encoding="utf-8") as f:
            self.assertLessEqual(len(f.read().splitlines()), 120)

    def test_playbook_limit(self):
        with open(os.path.join(ROOT, "PLAYBOOK.md"), encoding="utf-8") as f:
            self.assertLessEqual(len(f.read().splitlines()), 450)


if __name__ == "__main__":
    unittest.main()
