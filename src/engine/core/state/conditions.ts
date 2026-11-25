// Spielzustand, soweit ihn die Darstellung braucht, und Auswertung von Bedingungen (Asset-Vertrag: Aktionen).
import type { Condition } from "../schema/index.ts";

export type WorldState = {
  flags: ReadonlySet<string>;
  inventory: ReadonlyMap<string, number>;
};

export const initialState = (): WorldState => ({ flags: new Set(), inventory: new Map() });

export function evalCondition(cond: Condition, state: WorldState): boolean {
  if ("flag" in cond) return state.flags.has(cond.flag);
  if ("hasItem" in cond) return (state.inventory.get(cond.hasItem) ?? 0) > 0;
  if ("not" in cond) return !evalCondition(cond.not, state);
  if ("all" in cond) return cond.all.every((c) => evalCondition(c, state));
  return cond.any.some((c) => evalCondition(c, state));
}

/** Ohne Bedingung ist etwas immer sichtbar. */
export const isVisible = (visibleIf: Condition | undefined, state: WorldState) =>
  visibleIf === undefined || evalCondition(visibleIf, state);
