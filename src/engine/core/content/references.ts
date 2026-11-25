// Prüfungen über Dateien hinweg (NF-V-01): content.ref-missing und content.flag-never-set (Asset-Vertrag: Aktionen).
import type { ContentError, Room } from "../schema/index.ts";
import type { ContentIndex } from "./load.ts";
import { at, emptyUses, ref, walkCondition, walkEffects, walkTarget, type At, type RefKind, type Uses } from "./uses.ts";

function walkRoom(room: Room, a: At) {
  walkEffects(room.onEnter, at(a, "onEnter"));
  for (const [name, h] of Object.entries(room.hotspots ?? {})) {
    const ha = at(a, `hotspots.${name}`);
    walkTarget(h, ha, h.useItem);
    if (h.exit) {
      ref(at(ha, "exit"), "room", h.exit.room);
      a.uses.spawns.push({ room: h.exit.room, spawn: h.exit.spawn, file: a.file, where: `${ha.where}.exit` });
      walkCondition(h.exit.if, at(ha, "exit.if"));
      walkEffects(h.exit.else, at(ha, "exit.else"));
    }
  }
  for (const [name, p] of Object.entries(room.parts ?? {})) walkCondition(p.visibleIf, at(a, `parts.${name}.visibleIf`));
  room.items?.forEach((p, i) => {
    ref(at(a, `items.${i}`), "item", p.item);
    walkTarget(p, at(a, `items.${i}`));
  });
  room.characters?.forEach((p, i) => {
    ref(at(a, `characters.${i}`), "character", p.character);
    walkTarget(p, at(a, `characters.${i}`), p.give);
  });
}

function collect(content: ContentIndex): Uses {
  const uses = emptyUses();
  const start = (file: string): At => ({ uses, file, where: "" });
  if (content.game) ref(at(start("content/game.json"), "player"), "character", content.game.player);
  for (const [, r] of content.rooms) walkRoom(r.def, start(r.file));
  for (const [id, d] of content.dialogs) {
    const a = start(`content/dialogs/${id}.json`);
    for (const [nid, n] of Object.entries(d.nodes)) {
      n.lines.forEach((l, i) => l.speaker !== "player" && ref(at(a, `nodes.${nid}.lines.${i}.speaker`), "character", l.speaker));
      walkEffects(n.effects, at(a, `nodes.${nid}.effects`));
      n.options?.forEach((o, i) => {
        walkCondition(o.if, at(a, `nodes.${nid}.options.${i}.if`));
        walkEffects(o.effects, at(a, `nodes.${nid}.options.${i}.effects`));
      });
    }
  }
  for (const [id, c] of content.cutscenes) walkEffects(c.steps, at(start(`content/cutscenes/${id}.json`), "steps"));
  return uses;
}

const NAMES: Record<RefKind, string> = { room: "Raum", character: "Figur", item: "Gegenstand", dialog: "Dialog", cutscene: "Zwischensequenz" };
const TAKEN = /^item\.[^.]+\.[^.]+\.taken$/;

export function referenceErrors(content: ContentIndex): ContentError[] {
  const uses = collect(content);
  const known: Record<RefKind, { has(id: string): boolean }> = {
    room: content.rooms, character: content.characters, item: content.items, dialog: content.dialogs, cutscene: content.cutscenes,
  };
  const errors: ContentError[] = [];
  const add = (code: string, file: string, message: string) => errors.push({ code, file, message });
  for (const r of uses.refs)
    if (!known[r.kind].has(r.id)) add("content.ref-missing", r.file, `${r.where}: ${NAMES[r.kind]} „${r.id}“ gibt es nicht`);
  for (const s of uses.spawns) {
    const room = content.rooms.get(s.room);
    if (room && !room.def.spawns[s.spawn]) add("content.ref-missing", s.file, `${s.where}: Spawn „${s.spawn}“ gibt es in „${s.room}“ nicht`);
  }
  for (const f of uses.flagsRead)
    if (!uses.flagsSet.has(f.flag) && !TAKEN.test(f.flag)) add("content.flag-never-set", f.file, `${f.where}: Flag „${f.flag}“ wird nirgends gesetzt`);
  return errors;
}
