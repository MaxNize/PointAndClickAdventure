// Prüfungen eines Dialogs (NF-V-01, Asset-Vertrag: Dialog): Knotenverweise, Erreichbarkeit, Weg zu einem Ende,
// eindeutige Options-IDs.
import type { ContentError, Dialog } from "../schema/index.ts";

const nextOf = (d: Dialog, id: string) => (d.nodes[id]?.options ?? []).flatMap((o) => (o.next ? [o.next] : []));
/** Ein Knoten beendet den Dialog, wenn er keine Optionen hat oder eine Option mit `end`. */
const ends = (d: Dialog, id: string) => {
  const options = d.nodes[id]?.options ?? [];
  return options.length === 0 || options.some((o) => o.end);
};

function reachable(d: Dialog): Set<string> {
  const seen = new Set<string>();
  const todo = d.start in d.nodes ? [d.start] : [];
  for (let id = todo.pop(); id !== undefined; id = todo.pop()) {
    if (seen.has(id) || !(id in d.nodes)) continue;
    seen.add(id);
    todo.push(...nextOf(d, id));
  }
  return seen;
}

/** Knoten, von denen aus ein Ende erreichbar ist (Rücksprünge erlaubt). */
function canEnd(d: Dialog): Set<string> {
  const ok = new Set(Object.keys(d.nodes).filter((id) => ends(d, id)));
  for (let grew = true; grew; ) {
    grew = false;
    for (const id of Object.keys(d.nodes))
      if (!ok.has(id) && nextOf(d, id).some((n) => ok.has(n))) grew = ok.add(id) !== undefined;
  }
  return ok;
}

function referenceErrors(d: Dialog, add: (code: string, message: string) => void) {
  if (!(d.start in d.nodes)) add("dialog.node-unknown", `start: Knoten „${d.start}“ gibt es nicht`);
  for (const [id, node] of Object.entries(d.nodes)) {
    const seen = new Set<string>();
    node.options?.forEach((o, i) => {
      if (o.next && !(o.next in d.nodes)) add("dialog.node-unknown", `nodes.${id}.options.${i}.next: Knoten „${o.next}“ gibt es nicht`);
      if (seen.has(o.id)) add("dialog.option-duplicate", `nodes.${id}.options.${i}: Option „${o.id}“ doppelt`);
      seen.add(o.id);
    });
  }
}

export function dialogErrors(d: Dialog, file: string): ContentError[] {
  const errors: ContentError[] = [];
  const add = (code: string, message: string) => errors.push({ code, file, message });
  referenceErrors(d, add);
  const reach = reachable(d);
  const end = canEnd(d);
  for (const id of Object.keys(d.nodes)) {
    if (!reach.has(id)) add("dialog.unreachable", `nodes.${id}: vom Start „${d.start}“ aus nicht erreichbar`);
    else if (!end.has(id)) add("dialog.no-end", `nodes.${id}: von hier führt kein Weg zu einem Ende`);
  }
  return errors;
}
