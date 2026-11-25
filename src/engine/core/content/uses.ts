// Sammelt, worauf Inhalte verweisen und welche Flags sie lesen oder setzen (Asset-Vertrag: Aktionen).
import type { Condition, Effect } from "../schema/index.ts";

export type RefKind = "room" | "character" | "item" | "dialog" | "cutscene";

export type Uses = {
  refs: Array<{ kind: RefKind; id: string; file: string; where: string }>;
  spawns: Array<{ room: string; spawn: string; file: string; where: string }>;
  flagsRead: Array<{ flag: string; file: string; where: string }>;
  flagsSet: Set<string>;
};

export const emptyUses = (): Uses => ({ refs: [], spawns: [], flagsRead: [], flagsSet: new Set() });

/** Ort in einer Datei, an dem gerade gesammelt wird, z. B. `hotspots.hotspot-kiste.verbs.look`. */
export type At = { uses: Uses; file: string; where: string };

export const at = (a: At, where: string): At => ({ ...a, where: a.where ? `${a.where}.${where}` : where });
export const ref = (a: At, kind: RefKind, id: string | undefined) => {
  if (id !== undefined) a.uses.refs.push({ kind, id, file: a.file, where: a.where });
};

export function walkCondition(cond: Condition | undefined, a: At): void {
  if (cond === undefined) return;
  if ("flag" in cond) a.uses.flagsRead.push({ flag: cond.flag, file: a.file, where: a.where });
  else if ("hasItem" in cond) ref(a, "item", cond.hasItem);
  else if ("not" in cond) walkCondition(cond.not, a);
  else for (const c of "all" in cond ? cond.all : cond.any) walkCondition(c, a);
}

type Visitor<T extends Effect["type"]> = (e: Extract<Effect, { type: T }>, a: At) => void;
const character = (e: { character?: string | undefined }, a: At) => ref(a, "character", e.character);
const item = (e: { item: string }, a: At) => ref(a, "item", e.item);

const VISIT: { [T in Effect["type"]]?: Visitor<T> } = {
  say: (e, a) => ref(a, "character", e.speaker),
  setFlag: (e, a) => void a.uses.flagsSet.add(e.flag),
  addItem: item,
  removeItem: item,
  pickUp: item,
  walkTo: character,
  face: character,
  playAnimation: character,
  changeRoom: (e, a) => {
    ref(a, "room", e.room);
    a.uses.spawns.push({ room: e.room, spawn: e.spawn, file: a.file, where: a.where });
  },
  startDialog: (e, a) => ref(a, "dialog", e.dialog),
  startCutscene: (e, a) => ref(a, "cutscene", e.cutscene),
  if: (e, a) => {
    walkCondition(e.cond, at(a, "cond"));
    walkEffects(e.then, at(a, "then"));
    walkEffects(e.else, at(a, "else"));
  },
};

export function walkEffects(effects: readonly Effect[] | undefined, a: At): void {
  effects?.forEach((e, i) => (VISIT[e.type] as Visitor<typeof e.type> | undefined)?.(e as never, at(a, String(i))));
}

/** Verben, `useItem` bzw. `give` (Schlüssel sind Gegenstands-IDs) eines Interaktionsziels. */
export function walkTarget(t: { visibleIf?: Condition; verbs?: Record<string, Effect[] | undefined> }, a: At, items?: Record<string, Effect[]>) {
  walkCondition(t.visibleIf, at(a, "visibleIf"));
  for (const [verb, list] of Object.entries(t.verbs ?? {})) walkEffects(list, at(a, `verbs.${verb}`));
  for (const [id, list] of Object.entries(items ?? {})) {
    ref(at(a, id), "item", id);
    walkEffects(list, at(a, id));
  }
}
