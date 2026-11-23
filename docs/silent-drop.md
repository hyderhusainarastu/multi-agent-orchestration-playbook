# Silent drop

## What happened (anonymised)

A pipeline had three stages: fetch items, shape them with an agent, then process them with plain code. One run's agent stage trimmed its output down to an empty list. The next code stage looped over nothing, skipped every item, and exited normally. The run reported success with zero results. Nobody saw a failure because nothing failed: every stage did what it was told with the input it got.

## Why it is dangerous

- Empty is a valid value, so no type check catches it.
- Each stage looks correct in isolation.
- The only symptom is a result that is too small, and a reader cannot tell that from "nothing to find".

## The guard

Log item counts into and out of every stage. Throw when input is above zero and output is zero.

```python
import sys; sys.path.insert(0, "tools")
import guards

log = []
items = load_items()                       # 40 items
shaped = agent_shape(items)                # returns []
guards.stage_log(log, "shape", len(items), len(shaped))
guards.guard_non_empty("shape", len(items), len(shaped))   # raises GuardError
```

```js
import { stageLog, guardNonEmpty } from "./tools/guards.mjs";
stageLog(log, "shape", items.length, shaped.length);
guardNonEmpty("shape", items.length, shaped.length);
```

## Rules around the guard

1. Wrap every stage, including the ones that "cannot" return empty.
2. Persist the log to disk (`logs/<stage>.json`) so a resume can read it.
3. Use `screen(items, rules)` for filters. It returns `{kept, dropped: {reason: [ids]}}`, so a drop always has a named reason and a list of ids. Log both.
4. A partial drop is also worth a look: alert when `items_out / items_in` falls under a threshold you set in the contract.
5. Treat a null or empty agent reply as a failure, not as "no findings".
6. Never let an agent re-emit bulk data to pass it along. Pass a file path; the next stage reads the file and counts it.

## Test it

`tests/test_guards.py::test_silent_drop_is_caught` reproduces the failure with a stage that returns `[]` and asserts the run aborts.
