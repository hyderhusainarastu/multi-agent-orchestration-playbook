# Pilot before scale

Use this when you do not yet know which method will find what you need. Spend a small, scored pilot first. Scale only the method that earns it.

## The sequence

1. **Define the target and a gold set.** Write down what counts as a hit. Collect a small gold set of known hits (10 to 30) and a set of negative controls: items that look relevant but are not.
2. **Blind explorers.** Several explorers each propose a method without seeing the others. They label themselves with a neutral id, not the model name. Each fills `templates/explorer-proposal.schema.json`.
3. **Red team.** A separate agent attacks each proposal: where does it miss, where does it flag false positives, what does it cost? Notes go into `red_team_notes`.
4. **Judge shortlists.** A judge reads proposals and attacks, then keeps a short list (2 to 3) of methods to pilot. It states why each dropped method dropped.
5. **Pilot.** Run each shortlisted method on the gold set and the negative controls only. Score with `templates/pilot-scorecard.schema.json`:
   - recall = `gold_found / gold_total`
   - false-positive rate = `negatives_flagged / negatives_total`
   Compute both with a script, never by eye.
6. **Independent skeptic.** An agent that took no part reads the scorecards and the missed ids and gives a verdict per method: `scale`, `revise` or `drop`.
7. **Scout-first lanes.** Scale in lanes. Each lane first runs a small scout slice (for example 5 percent of its items) and logs counts in and out. Only if the scout slice passes the guards does the lane run in full.

## Rules

- Never run a full pass with an unscored method.
- The gold set is hidden from explorers while they propose.
- The agent that built a method never scores it.
- Record rejected methods and why. They save the next run a pilot.
- Keep the thresholds in the contract (for example recall at or above 0.7 and false positives at or below 0.2) and set them before the pilot, not after.

## Toy example: open datasets about public libraries

Goal: find open datasets about public libraries (branch locations, circulation, opening hours).

- Gold set: 10 datasets already known to exist. Negative controls: 6 datasets about museums or schools that mention "library" in a column name.
- Explorer A proposes keyword search on a dataset aggregator. Explorer B proposes a facet search on city portals (see `examples/library-datasets/proposal.json`). Explorer C proposes crawling the sitemap of one national portal.
- Red team notes that B's facet name differs between portals, and that C only covers one country.
- Judge shortlists A and B.
- Pilot scores (invented numbers for the toy case; see `examples/library-datasets/scorecard.json`): B found 7 of 10 gold and flagged 1 of 6 negatives. Its three misses were filed under a "culture" facet.
- Skeptic verdict for B: `revise` (add the facet synonym), then re-pilot once. Verdict for A: `scale`, in lanes by country, scout slice first.

The numbers in this example are made up to show the arithmetic. They are not results.
