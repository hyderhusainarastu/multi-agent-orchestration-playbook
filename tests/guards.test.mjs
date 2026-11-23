import test from "node:test";
import assert from "node:assert/strict";
import { requireArgs, stageLog, guardNonEmpty, screen, GuardError } from "../tools/guards.mjs";

test("requireArgs", () => {
  assert.deepEqual(requireArgs({ a: 1 }, ["a"]), { a: 1 });
  assert.throws(() => requireArgs({ a: "" }, ["a", "b"]), /a, b/);
  assert.throws(() => requireArgs(undefined, ["a"]), GuardError);
});

test("guardNonEmpty trips only on in>0 and out==0", () => {
  assert.equal(guardNonEmpty("s", 0, 0), true);
  assert.equal(guardNonEmpty("s", 3, 1), true);
  assert.throws(() => guardNonEmpty("s", 3, 0), GuardError);
});

test("stageLog appends", () => {
  const log = [];
  const rec = stageLog(log, "trim", 5, 4);
  assert.equal(log.length, 1);
  assert.equal(rec.items_out, 4);
});

test("screen returns kept and dropped by reason", () => {
  const items = [{ id: "a", t: "" }, { id: "b", t: "x" }, { id: "c", t: "x", dup: 1 }];
  const r = screen(items, [["empty", (i) => !i.t], ["dup", (i) => i.dup]]);
  assert.deepEqual(r.kept.map((i) => i.id), ["b"]);
  assert.deepEqual(r.dropped, { empty: ["a"], dup: ["c"] });
});
