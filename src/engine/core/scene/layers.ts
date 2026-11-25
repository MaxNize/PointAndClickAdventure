// Reihenfolge der obersten Ebenen eines Raums (Engine-Konzept: Zeichenreihenfolge, Asset-Vertrag: room.svg).
// Akteure kommen mit FA-E-02 und FA-E-04 zwischen die Mittelebenen.
import type { ContentError, Room } from "../schema/index.ts";

export const BACKGROUND = "layer-background";
export const HOTSPOTS = "hotspots";
export const FOREGROUND = "layer-foreground";
const MID = /^layer-mid-/;
const FIXED = new Set([BACKGROUND, HOTSPOTS, FOREGROUND]);

export type LayerOrder = { order: string[]; errors: ContentError[] };
type Baselines = NonNullable<Room["layers"]>;

const isMid = (g: string | null): g is string => g !== null && MID.test(g);

function layerErrors(groupIds: ReadonlyArray<string | null>, baselines: Baselines, file: string): ContentError[] {
  const errors: ContentError[] = [];
  const add = (code: string, message: string) => errors.push({ code, file, message });
  const mids = groupIds.filter(isMid);
  if (!groupIds.includes(BACKGROUND)) add("room.layer-missing", "Gruppe layer-background fehlt");
  for (const g of groupIds)
    if (!isMid(g) && !FIXED.has(g ?? "")) add("room.unknown-layer", `unbekannte oberste Gruppe „${g ?? "(ohne id)"}“`);
  for (const g of mids) if (!baselines[g]) add("room.layer-unmapped", `„${g}“ hat keine Basislinie in room.json`);
  for (const g of Object.keys(baselines))
    if (!mids.includes(g)) add("room.layer-unmapped", `Basislinie für „${g}“, aber keine Gruppe im SVG`);
  return errors;
}

/**
 * @param groupIds IDs der obersten Gruppen im Raum-SVG, in Dateireihenfolge (`null` für Gruppen ohne ID)
 * @returns Zeichenreihenfolge: Hintergrund, Hotspots, Mittelebenen aufsteigend nach Basislinie, Vordergrund
 */
export function roomLayerOrder(groupIds: ReadonlyArray<string | null>, room: Room, file: string): LayerOrder {
  const baselines = room.layers ?? {};
  const baseline = (g: string) => baselines[g]?.baseline ?? 0;
  const mids = groupIds.filter(isMid).sort((a, b) => baseline(a) - baseline(b));
  const order = [BACKGROUND, HOTSPOTS, ...mids, FOREGROUND].filter((g) => groupIds.includes(g));
  return { order, errors: layerErrors(groupIds, baselines, file) };
}
