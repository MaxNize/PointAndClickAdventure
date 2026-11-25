// Zeichenreihenfolge mit Akteuren (FA-E-02, Engine-Konzept: Zeichenreihenfolge). Zwischen Hotspots und Vordergrund
// liegen Mittelebenen und Akteure, aufsteigend nach Basislinie. Größeres y liegt weiter vorn.
import type { Room } from "../schema/index.ts";
import type { Actor } from "./actors.ts";
import { BACKGROUND, FOREGROUND, HOTSPOTS } from "./layers.ts";

export type DrawEntry = { layer: string } | { actor: Actor };

/**
 * @param layerOrder Ebenen aus roomLayerOrder
 * @returns Hintergrund, Hotspots, Mittelebenen und Akteure nach Basislinie, Vordergrund. Bei gleicher Basislinie
 *   liegt die Ebene hinter dem Akteur, Akteure behalten ihre Reihenfolge.
 */
export function drawOrder(layerOrder: readonly string[], room: Room, actors: readonly Actor[]): DrawEntry[] {
  const baselines = room.layers ?? {};
  const fixed = new Set([BACKGROUND, HOTSPOTS, FOREGROUND]);
  const middle = [
    ...layerOrder.filter((id) => !fixed.has(id)).map((id) => ({ y: baselines[id]?.baseline ?? 0, rank: 0, e: { layer: id } })),
    ...actors.map((a) => ({ y: a.baseline, rank: 1, e: { actor: a } })),
  ]
    .sort((a, b) => a.y - b.y || a.rank - b.rank)
    .map((m) => m.e);
  const head = [BACKGROUND, HOTSPOTS].filter((id) => layerOrder.includes(id)).map((id) => ({ layer: id }));
  const tail = layerOrder.includes(FOREGROUND) ? [{ layer: FOREGROUND }] : [];
  return [...head, ...middle, ...tail];
}
