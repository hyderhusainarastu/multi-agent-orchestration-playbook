#!/usr/bin/env python3
"""Stop a loop at its caps. Usage: check_caps.py STATE_JSON

Reads state["caps"], a map of name -> {"max": int, "used": int}
(for example rounds, secondary_loops, chain_depth, hops).
Exit 0: all caps have headroom. Exit 3: at least one cap is reached; escalate to a human.
Exit 2: unreadable or malformed state.
"""
import json
import sys


def reached(state):
    caps = state.get("caps")
    if not isinstance(caps, dict) or not caps:
        raise ValueError("state has no 'caps' map")
    out = []
    for name, c in caps.items():
        if not isinstance(c, dict) or not isinstance(c.get("max"), int) or not isinstance(c.get("used"), int):
            raise ValueError(f"cap '{name}' needs integer 'max' and 'used'")
        if c["used"] >= c["max"]:
            out.append((name, c["used"], c["max"]))
    return out


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 1:
        print(__doc__, file=sys.stderr)
        return 2
    try:
        with open(argv[0], encoding="utf-8") as f:
            hit = reached(json.load(f))
    except (OSError, ValueError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    if hit:
        for n, u, m in hit:
            print(f"CAP REACHED: {n} {u}/{m}; stop and escalate to a human")
        return 3
    print("OK: all caps have headroom")
    return 0


if __name__ == "__main__":
    sys.exit(main())
