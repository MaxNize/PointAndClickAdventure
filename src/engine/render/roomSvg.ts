// Baut das Raum-<svg> für die Darstellung (FA-E-01, FA-E-02). Die Ebenen des Raum-SVG werden unverändert übernommen
// und mit den Akteuren in die Zeichenreihenfolge aus dem Kern gebracht (Engine-Konzept: Zeichenreihenfolge).
import type { ContentIndex, RoomEntry } from "../core/content/load.ts";
import type { Actor } from "../core/scene/actors.ts";
import { drawOrder } from "../core/scene/drawOrder.ts";
import { HOTSPOTS, roomLayerOrder } from "../core/scene/layers.ts";
import type { ContentError } from "../core/schema/index.ts";
import { buildActor } from "./actorSvg.ts";
import { parseSvg, SVG_NS } from "./svgEmbed.ts";

const ROOM_VIEWBOX = "0 0 1920 1080";

/** `layout` aufrufen, sobald `element` im Dokument hängt: setzt die Akteure auf ihre Position. */
export type BuiltRoom = { element: SVGSVGElement; errors: ContentError[]; layout: () => void };

export function buildRoomSvg(entry: RoomEntry, content: ContentIndex, actors: readonly Actor[]): BuiltRoom {
  const file = entry.file.replace(/room\.json$/, "room.svg");
  const element = document.createElementNS(SVG_NS, "svg");
  element.setAttribute("viewBox", ROOM_VIEWBOX);
  element.setAttribute("data-room", entry.def.id);
  const { root, error } = parseSvg(entry.svg, file);
  if (!root) return { element, errors: error ? [error] : [], layout: () => {} };

  const errors: ContentError[] = [];
  if (root.getAttribute("viewBox") !== ROOM_VIEWBOX)
    errors.push({ code: "svg.viewbox", file, message: `viewBox muss „${ROOM_VIEWBOX}“ sein` });

  const children = [...root.children];
  const groups = children.filter((c) => c.localName === "g");
  const { order, errors: layerErrors } = roomLayerOrder(groups.map((g) => g.getAttribute("id")), entry.def, file);
  errors.push(...layerErrors);

  // Nicht-Gruppen (z. B. <defs>) zuerst, dann Ebenen und Akteure in Zeichenreihenfolge.
  for (const c of children) if (c.localName !== "g") element.append(document.importNode(c, true));
  const layouts: Array<() => void> = [];
  for (const item of drawOrder(order, entry.def, actors)) {
    if ("actor" in item) {
      const built = buildActor(item.actor, content, entry.def);
      errors.push(...built.errors);
      if (built.element) element.append(built.element);
      layouts.push(built.layout);
      continue;
    }
    const layer = document.importNode(groups.find((g) => g.getAttribute("id") === item.layer)!, true);
    if (item.layer === HOTSPOTS) layer.setAttribute("pointer-events", "all");
    element.append(layer);
  }
  return { element, errors, layout: () => layouts.forEach((l) => l()) };
}
