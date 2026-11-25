// SVG-Dateien lesen und in den gemeinsamen DOM einbetten (Engine-Konzept: SVG einbetten und ID-Namensraum).
import type { ContentError } from "../core/schema/index.ts";

export const SVG_NS = "http://www.w3.org/2000/svg";

export function parseSvg(text: string, file: string): { root?: SVGSVGElement; error?: ContentError } {
  const doc = new DOMParser().parseFromString(text, "image/svg+xml");
  const root = doc.documentElement;
  if (doc.querySelector("parsererror") || root.localName !== "svg")
    return { error: { code: "svg.parse", file, message: "Datei ist kein gültiges SVG" } };
  return { root: root as unknown as SVGSVGElement };
}

/** viewBox als Zahlen, `undefined` wenn sie fehlt oder kaputt ist. */
export function viewBoxOf(root: Element): { x: number; y: number; width: number; height: number } | undefined {
  const v = (root.getAttribute("viewBox") ?? "").trim().split(/[\s,]+/).map(Number);
  if (v.length !== 4 || v.some((n) => !Number.isFinite(n)) || v[3]! <= 0) return undefined;
  return { x: v[0]!, y: v[1]!, width: v[2]!, height: v[3]! };
}

/** Jede ID wird zu `<instanz>--<id>`, Verweise in `url(#…)`, `href` und `xlink:href` werden mit umgeschrieben. */
export function prefixIds(root: Element, instance: string): void {
  const ids = new Set([...root.querySelectorAll("[id]")].map((e) => e.id));
  const map = (id: string) => (ids.has(id) ? `${instance}--${id}` : id);
  for (const el of [root, ...root.querySelectorAll("*")]) {
    for (const attr of [...el.attributes]) {
      if (attr.name === "id") attr.value = map(attr.value);
      else if ((attr.name === "href" || attr.name === "xlink:href") && attr.value.startsWith("#"))
        attr.value = `#${map(attr.value.slice(1))}`;
      else if (attr.value.includes("url(#")) attr.value = attr.value.replace(/url\(#([^)]+)\)/g, (_, id: string) => `url(#${map(id)})`);
    }
  }
}
