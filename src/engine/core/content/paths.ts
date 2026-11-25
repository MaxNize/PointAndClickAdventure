// Ordnet einen Pfad unter content/ seiner Dateiart zu (Asset-Vertrag: Verzeichnis). Der Ordner- bzw. Dateiname ist die ID.

export type ContentFileKind =
  | "game"
  | "room"
  | "roomSvg"
  | "character"
  | "characterSvg"
  | "animations"
  | "dialog"
  | "cutscene";

export type ClassifiedPath =
  | { kind: ContentFileKind; id: string }
  /** im Vertrag vorgesehen, aber noch ohne Schema (Gegenstände, Rezepte, Lösungsweg, Zustände) */
  | { kind: "later" }
  | { kind: "unknown" };

const SEG = "([^/]+)";

const RULES: ReadonlyArray<[RegExp, ContentFileKind | "later"]> = [
  [/^content\/game\.json$/, "game"],
  [new RegExp(`^content/rooms/${SEG}/room\\.json$`), "room"],
  [new RegExp(`^content/rooms/${SEG}/room\\.svg$`), "roomSvg"],
  [new RegExp(`^content/characters/${SEG}/character\\.json$`), "character"],
  [new RegExp(`^content/characters/${SEG}/character\\.svg$`), "characterSvg"],
  [new RegExp(`^content/characters/${SEG}/animations\\.json$`), "animations"],
  [new RegExp(`^content/dialogs/${SEG}\\.json$`), "dialog"],
  [new RegExp(`^content/cutscenes/${SEG}\\.json$`), "cutscene"],
  [/^content\/items\/[^/]+\/(item\.json|world\.svg|icon\.svg)$/, "later"],
  [/^content\/recipes\/[^/]+\.json$/, "later"],
  [/^content\/walkthrough\.json$/, "later"],
  [/^content\/states\/(manual\/)?[^/]+\.json$/, "later"],
];

export function classifyPath(path: string): ClassifiedPath {
  for (const [re, kind] of RULES) {
    const m = re.exec(path);
    if (!m) continue;
    return kind === "later" ? { kind } : { kind, id: m[1] ?? "" };
  }
  return { kind: "unknown" };
}
