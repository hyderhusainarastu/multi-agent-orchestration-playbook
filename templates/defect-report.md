# Defect report

One line per defect, in this exact shape, so the owner can act without a conversation:

```
owner - file:line - what - fix
```

Examples (invented):

```
stage-b-builder - work/stage-b/merge.py:42 - drops rows whose id is empty, no log line - log the drop and count it
stage-c-builder - work/stage-c/out.csv:17 - duplicate id item-007 - dedupe on id before writing
```

Rules:

- The reviewer writes reports; only the owner fixes. No self-approval.
- "What" states the observed fact, not an opinion. "Fix" is the smallest change.
- Group by owner. End with counts: `defects: N, owners: M`.
- A fixed defect is re-checked by the reviewer, not by the fixer.
