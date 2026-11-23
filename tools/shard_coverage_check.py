#!/usr/bin/env python3
"""Prove shard coverage with a set difference over explicit ids.

Usage: shard_coverage_check.py --expected IDS SHARD [SHARD ...]
Each file is one id per line (blank lines and # comments ignored) or a JSON list.
Exit 0: every expected id appears in exactly one shard, and no unknown ids.
Exit 1: gaps, duplicates or extras (listed). Exit 2: usage error.
"""
import argparse
import json
import os
import sys


def read_ids(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    s = text.strip()
    if s.startswith("["):
        return [str(x) for x in json.loads(s)]
    return [ln.strip() for ln in text.splitlines() if ln.strip() and not ln.lstrip().startswith("#")]


def check(expected, shards):
    """shards: {name: [ids]}. Returns (gaps, duplicates, extras)."""
    exp = set(expected)
    seen = {}
    for name, ids in shards.items():
        for i in ids:
            seen.setdefault(i, []).append(name)
    gaps = sorted(exp - set(seen))
    extras = sorted(set(seen) - exp)
    dups = {i: sorted(set(n)) if len(set(n)) > 1 else n for i, n in seen.items() if len(n) > 1}
    return gaps, dups, extras


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--expected", required=True)
    ap.add_argument("shards", nargs="+")
    try:
        a = ap.parse_args(argv)
    except SystemExit as e:
        return 2 if e.code else 0
    try:
        expected = read_ids(a.expected)
        shards = {os.path.basename(p): read_ids(p) for p in a.shards}
    except (OSError, ValueError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    gaps, dups, extras = check(expected, shards)
    if gaps:
        print(f"GAPS ({len(gaps)}): " + ", ".join(gaps))
    if dups:
        print(f"DUPLICATES ({len(dups)}): " + "; ".join(f"{i} (in {', '.join(n)})" for i, n in sorted(dups.items())))
    if extras:
        print(f"EXTRAS ({len(extras)}): " + ", ".join(extras))
    if gaps or dups or extras:
        return 1
    print(f"OK: {len(expected)} ids covered exactly once by {len(shards)} shards")
    return 0


if __name__ == "__main__":
    sys.exit(main())
