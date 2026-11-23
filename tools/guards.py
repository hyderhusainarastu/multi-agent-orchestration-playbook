"""Pipeline guards: argument checks, stage count logs, empty-output guard, rule screen.

Standard library only. Import with: sys.path.insert(0, "tools"); import guards
"""
import json
import sys
import time


class GuardError(RuntimeError):
    """Raised when a guard trips. Let it stop the run."""


def require_args(args, names):
    """Raise GuardError if any name is missing, None or an empty string/list."""
    args = args or {}
    missing = [n for n in names if args.get(n) in (None, "", [], {})]
    if missing:
        raise GuardError("missing required args: " + ", ".join(missing))
    return args


def stage_log(log, stage, items_in, items_out, note=""):
    """Append a counts record for a stage and return it. `log` is a list."""
    rec = {"stage": stage, "items_in": items_in, "items_out": items_out,
           "note": note, "ts": round(time.time(), 3)}
    log.append(rec)
    return rec


def guard_non_empty(stage, items_in, items_out):
    """Throw when input > 0 and output == 0: the silent-drop signature."""
    if items_in > 0 and items_out == 0:
        raise GuardError(
            f"stage '{stage}' took {items_in} items and produced 0; refusing to continue")
    return True


def screen(items, rules):
    """Split items by named rules.

    rules: list of (reason, predicate); predicate(item) is True when the item must be dropped.
    The first matching rule wins. Items are dicts with an "id" key.
    Returns {"kept": [...], "dropped": {reason: [ids]}}.
    """
    kept, dropped = [], {}
    for it in items:
        for reason, pred in rules:
            if pred(it):
                dropped.setdefault(reason, []).append(it.get("id"))
                break
        else:
            kept.append(it)
    return {"kept": kept, "dropped": dropped}


# camelCase aliases so Python and Node call sites read the same.
requireArgs, stageLog, guardNonEmpty = require_args, stage_log, guard_non_empty


def run_stage(log, name, items, fn):
    """Run fn(items) -> list, log counts, and apply the empty-output guard."""
    out = fn(items)
    stage_log(log, name, len(items), len(out))
    guard_non_empty(name, len(items), len(out))
    return out


if __name__ == "__main__":
    print(json.dumps({"usage": "import guards; see docs/silent-drop.md"}), file=sys.stderr)
