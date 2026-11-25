// Figuren und Gegenstände im Raum (FA-E-04, FA-E-10). Position und Skalierung kommen aus dem Kern. Der Anker wird erst
// nach dem Einhängen gemessen, damit Transforms in der Figur (z. B. an der Ansichtsgruppe) richtig mitzählen.
import type { ContentIndex } from "../core/content/load.ts";
import type { Actor } from "../core/scene/actors.ts";
import { depthScale } from "../core/scene/depth.ts";
import type { ContentError, Room } from "../core/schema/index.ts";
import { parseSvg, prefixIds, SVG_NS, viewBoxOf } from "./svgEmbed.ts";

export type BuiltActor = { element?: SVGGElement; errors: ContentError[]; layout: () => void };

const VIEW_OF = { left: "view-side", right: "view-side", front: "view-front", back: "view-back" } as const;
const VIEWS = Object.values(VIEW_OF);

type Source = { svg: string; file: string; /** Raumeinheiten je Einheit der viewBox bei Skalierung 1 */ unit: (vbHeight: number) => number };

function sourceOf(actor: Actor, content: ContentIndex): Source | ContentError {
  if (actor.kind === "item") {
    const item = content.items.get(actor.ref)!;
    return { svg: item.worldSvg, file: item.file, unit: () => 1 };
  }
  const c = content.characters.get(actor.ref)!;
  const file = c.file.replace(/character\.json$/, "character.svg");
  if (c.svg === undefined) return { code: "character.svg-missing", file: c.file, message: "character.svg fehlt neben character.json" };
  return { svg: c.svg, file, unit: (h) => c.def.height / h };
}

/** Zeigt nur die Ansicht der Blickrichtung. Figuren ohne passende Ansicht melden character.view-missing. */
function selectView(root: Element, actor: Actor, file: string): Element | ContentError {
  if (actor.kind === "item") return root;
  const wanted = VIEW_OF[actor.facing];
  const views = [...root.children].filter((c) => VIEWS.includes(c.id as (typeof VIEWS)[number]));
  for (const v of views) if (v.id !== wanted) v.setAttribute("display", "none");
  const view = views.find((v) => v.id === wanted);
  return view ?? { code: "character.view-missing", file, message: `Ansichtsgruppe „${wanted}“ fehlt` };
}

const isError = (x: unknown): x is ContentError => typeof x === "object" && x !== null && "code" in x;
const none = (errors: ContentError[]): BuiltActor => ({ errors, layout: () => {} });

export function buildActor(actor: Actor, content: ContentIndex, room: Room): BuiltActor {
  const source = sourceOf(actor, content);
  if (isError(source)) return none([source]);
  const { root, error } = parseSvg(source.svg, source.file);
  if (!root) return none(error ? [error] : []);
  const view = selectView(root, actor, source.file);
  if (isError(view)) return none([view]);
  const anchor = view.querySelector<SVGGraphicsElement>('[data-part="anchor"]');
  if (!anchor) return none([{ code: `${actor.kind}.anchor-missing`, file: source.file, message: "Anker data-part=\"anchor\" fehlt" }]);

  anchor.setAttribute("data-active-anchor", "");
  const outer = document.createElementNS(SVG_NS, "g");
  outer.setAttribute("data-actor", actor.key);
  outer.setAttribute(`data-${actor.kind}`, actor.ref);
  const body = document.createElementNS(SVG_NS, "g");
  body.append(...[...root.childNodes].map((n) => document.importNode(n, true)));
  outer.append(body);
  prefixIds(body, actor.key);

  const scale = depthScale(actor.y, room.depth) * source.unit(viewBoxOf(root)?.height ?? 1);
  const layout = () => {
    const a = body.querySelector<SVGGraphicsElement>("[data-active-anchor]")!;
    const box = a.getBBox();
    const m = body.getCTM()!.inverse().multiply(a.getCTM()!);
    const p = new DOMPoint(box.x + box.width / 2, box.y + box.height / 2).matrixTransform(m);
    const sx = actor.facing === "left" ? -scale : scale;
    outer.setAttribute("transform", `translate(${actor.x} ${actor.y}) scale(${sx} ${scale}) translate(${-p.x} ${-p.y})`);
  };
  return { element: outer, errors: [], layout };
}
