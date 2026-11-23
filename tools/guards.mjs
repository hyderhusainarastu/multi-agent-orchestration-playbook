// Pipeline guards for Node 20+. No dependencies.
// import { requireArgs, stageLog, guardNonEmpty, screen } from "./guards.mjs";

export class GuardError extends Error {}

export function requireArgs(args, names) {
  const a = args ?? {};
  const missing = names.filter((n) => {
    const v = a[n];
    return v === undefined || v === null || v === "" ||
      (Array.isArray(v) && v.length === 0);
  });
  if (missing.length) throw new GuardError(`missing required args: ${missing.join(", ")}`);
  return a;
}

export function stageLog(log, stage, itemsIn, itemsOut, note = "") {
  const rec = { stage, items_in: itemsIn, items_out: itemsOut, note, ts: Date.now() / 1000 };
  log.push(rec);
  return rec;
}

export function guardNonEmpty(stage, itemsIn, itemsOut) {
  if (itemsIn > 0 && itemsOut === 0) {
    throw new GuardError(`stage '${stage}' took ${itemsIn} items and produced 0; refusing to continue`);
  }
  return true;
}

// rules: array of [reason, predicate]; first match wins; predicate true means drop.
export function screen(items, rules) {
  const kept = [];
  const dropped = {};
  for (const it of items) {
    const hit = rules.find(([, pred]) => pred(it));
    if (hit) (dropped[hit[0]] ??= []).push(it.id);
    else kept.push(it);
  }
  return { kept, dropped };
}
