// Sichtbare Akteure eines Raums (FA-E-03, FA-E-04): Spielfigur am Spawn, platzierte Figuren und Gegenstände.
import type { ContentIndex, RoomEntry } from "../content/load.ts";
import type { ContentError, Facing } from "../schema/index.ts";
import { isVisible, type WorldState } from "../state/conditions.ts";

export type Actor = {
  /** eindeutig im Raum, dient als ID-Präfix beim Einbetten */
  key: string;
  kind: "character" | "item";
  /** Figur- bzw. Gegenstands-ID */
  ref: string;
  x: number;
  y: number;
  facing: Facing;
  /** Basislinie für die Zeichenreihenfolge (Fußpunkt bzw. Platzierung y) */
  baseline: number;
};

export type SceneActors = { actors: Actor[]; errors: ContentError[] };

type Collect = { content: ContentIndex; room: RoomEntry; state: WorldState; out: SceneActors };

const missing = (c: Collect, code: string, message: string) => c.out.errors.push({ code, file: c.room.file, message });

function addPlayer(c: Collect, spawn: string) {
  const player = c.content.game?.player;
  const at = c.room.def.spawns[spawn];
  if (!player || !at) return;
  if (!c.content.characters.has(player)) return missing(c, "content.ref-missing", `Spielfigur „${player}“ gibt es nicht`);
  c.out.actors.push({ key: "player", kind: "character", ref: player, ...at, baseline: at.y });
}

function addCharacters(c: Collect) {
  for (const p of c.room.def.characters ?? []) {
    if (!isVisible(p.visibleIf, c.state)) continue;
    if (!c.content.characters.has(p.character)) missing(c, "content.ref-missing", `Figur „${p.character}“ gibt es nicht`);
    else c.out.actors.push({ key: `figur-${p.character}`, kind: "character", ref: p.character, x: p.x, y: p.y, facing: p.facing, baseline: p.y });
  }
}

function addItems(c: Collect) {
  const roomId = c.room.def.id;
  for (const p of c.room.def.items ?? []) {
    if (!isVisible(p.visibleIf, c.state) || c.state.flags.has(`item.${roomId}.${p.item}.taken`)) continue;
    if (!c.content.items.has(p.item)) missing(c, "item.world-missing", `Gegenstand „${p.item}“ hat kein world.svg`);
    else c.out.actors.push({ key: `gegenstand-${p.item}`, kind: "item", ref: p.item, x: p.x, y: p.y, facing: "front", baseline: p.y });
  }
}

export function sceneActors(content: ContentIndex, roomId: string, spawn: string, state: WorldState): SceneActors {
  const room = content.rooms.get(roomId);
  const out: SceneActors = { actors: [], errors: [] };
  if (!room) return out;
  const c: Collect = { content, room, state, out };
  addPlayer(c, spawn);
  addCharacters(c);
  addItems(c);
  return out;
}
