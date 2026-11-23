# Brief header (paste at the top of every sub-agent brief)

```
ROLE: <builder | reviewer | designer | fixer | verifier>   TIER: <small | medium | large>
TASK: <one sentence>
READ: <explicit list of paths; everything else is off limits>
WRITE ONLY: <one write root>
CONTRACT: <path to the frozen stage contract>
INPUT FILE: <path>   (bulk data comes from this file, not from this message)
OUTPUT FILE: <path>  (write results here; reply with counts only)
DONE WHEN: <testable condition>
COUNTS TO REPORT: items_in, items_out, items_failed
NEVER: self-approve; edit outside the write root; take facts from memory; message other agents
IF STUCK: stop and write a failure brief to <path>; do not guess
```
