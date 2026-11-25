// Baut das Raum-<svg> für die Darstellung (FA-E-01). Die Ebenen des Raum-SVG werden unverändert übernommen, nur in
// die Zeichenreihenfolge aus dem Kern gebracht (Engine-Konzept: Zeichenreihenfolge, SVG einbetten).
import type { RoomEntry } from "../core/content/load.ts";
import { HOTSPOTS, roomLayerOrder } from "../core/scene/layers.ts";
import type { ContentError } from "../core/schema/index.ts";

const SVG_NS = "http://www.w3.org/2000/svg";
const ROOM_VIEWBOX = "0 0 1920 1080";

export type BuiltRoom = { element: SVGSVGElement; errors: ContentError[] };

function parseSvg(text: string, file: string): { root?: SVGSVGElement; error?: ContentError } {
  const doc = new DOMParser().parseFromString(text, "image/svg+xml");
  const root = doc.documentElement;
  if (doc.querySelector("parsererror") || root.localName !== "svg")
    return { error: { code: "svg.parse", file, message: "Datei ist kein gültiges SVG" } };
  return { root: root as unknown as SVGSVGElement };
}

export function buildRoomSvg(entry: RoomEntry): BuiltRoom {
  const file = entry.file.replace(/room\.json$/, "room.svg");
  const element = document.createElementNS(SVG_NS, "svg");
  element.setAttribute("viewBox", ROOM_VIEWBOX);
  element.setAttribute("data-room", entry.def.id);
  const { root, error } = parseSvg(entry.svg, file);
  if (!root) return { element, errors: error ? [error] : [] };

  const errors: ContentError[] = [];
  if (root.getAttribute("viewBox") !== ROOM_VIEWBOX)
    errors.push({ code: "svg.viewbox", file, message: `viewBox muss „${ROOM_VIEWBOX}“ sein` });

  const children = [...root.children];
  const groups = children.filter((c) => c.localName === "g");
  const { order, errors: layerErrors } = roomLayerOrder(groups.map((g) => g.getAttribute("id")), entry.def, file);
  errors.push(...layerErrors);

  // Nicht-Gruppen (z. B. <defs>) zuerst, dann die Ebenen in Zeichenreihenfolge.
  for (const c of children) if (c.localName !== "g") element.append(document.importNode(c, true));
  for (const id of order) {
    const layer = document.importNode(groups.find((g) => g.getAttribute("id") === id)!, true);
    if (id === HOTSPOTS) layer.setAttribute("pointer-events", "all");
    element.append(layer);
  }
  return { element, errors };
}
