// Lädt alle Inhaltsdateien (FA-E-01, NF-W-01). Reiner Kern: Die Dateien liefert ein Adapter (Browser oder Node),
// dieser Code kennt weder Dateisystem noch import.meta.glob.
import type { Animations, Character, ContentError, ContentKind, Cutscene, Dialog, Game, Room } from "../schema/index.ts";
import { parseContent } from "../schema/index.ts";
import { classifyPath, type ContentFileKind } from "./paths.ts";

/** Pfad (`content/…`) → Inhalt: JSON bereits geparst, SVG als Text. */
export type ContentFiles = Record<string, unknown>;

export type RoomEntry = { def: Room; svg: string; file: string };
export type CharacterEntry = { def: Character; svg?: string; animations?: Animations; file: string };
/** Gegenstand. item.json wird erst mit dem Schema für Gegenstände geprüft, bis dahin zählt nur, dass es ihn gibt. */
export type ItemEntry = { worldSvg?: string; file: string };

export type ContentIndex = {
  game?: Game;
  rooms: Map<string, RoomEntry>;
  characters: Map<string, CharacterEntry>;
  items: Map<string, ItemEntry>;
  dialogs: Map<string, Dialog>;
  cutscenes: Map<string, Cutscene>;
};

export type LoadResult = { content: ContentIndex; errors: ContentError[] };

type Ctx = { files: ContentFiles; content: ContentIndex; errors: ContentError[] };
type Handler = (ctx: Ctx, id: string, file: string) => void;

const err = (code: string, file: string, message: string): ContentError => ({ code, file, message });

/** Parst eine JSON-Datei und prüft, ob ihre `id` zum Ordner- oder Dateinamen passt. */
function parse<K extends ContentKind>(ctx: Ctx, kind: K, id: string, file: string) {
  const r = parseContent(kind, ctx.files[file], file);
  if (!r.ok) {
    ctx.errors.push(...r.errors);
    return undefined;
  }
  const value = r.value as { id?: unknown };
  if (typeof value.id === "string" && value.id !== id) {
    ctx.errors.push(err("content.id-mismatch", file, `id „${value.id}“ weicht vom Namen „${id}“ ab`));
    return undefined;
  }
  return r.value;
}

const siblingSvg = (ctx: Ctx, file: string, name: string) => {
  const svg = ctx.files[file.replace(/[^/]+$/, name)];
  return typeof svg === "string" ? svg : undefined;
};

const HANDLERS: Record<ContentFileKind, Handler | undefined> = {
  game: (ctx, _id, file) => {
    ctx.content.game = parse(ctx, "game", "", file);
  },
  room: (ctx, id, file) => {
    const def = parse(ctx, "room", id, file);
    const svg = siblingSvg(ctx, file, "room.svg");
    if (def && svg === undefined) ctx.errors.push(err("room.svg-missing", file, "room.svg fehlt neben room.json"));
    if (def && svg !== undefined) ctx.content.rooms.set(id, { def, svg, file });
  },
  character: (ctx, id, file) => {
    const def = parse(ctx, "character", id, file);
    if (!def) return;
    const animFile = file.replace(/[^/]+$/, "animations.json");
    const animations = animFile in ctx.files ? parse(ctx, "animations", id, animFile) : undefined;
    ctx.content.characters.set(id, { def, svg: siblingSvg(ctx, file, "character.svg"), animations, file });
  },
  dialog: (ctx, id, file) => {
    const def = parse(ctx, "dialog", id, file);
    if (def) ctx.content.dialogs.set(id, def);
  },
  cutscene: (ctx, id, file) => {
    const def = parse(ctx, "cutscene", id, file);
    if (def) ctx.content.cutscenes.set(id, def);
  },
  item: (ctx, id, file) => {
    ctx.content.items.set(id, { ...ctx.content.items.get(id), file });
  },
  itemWorld: (ctx, id, file) => {
    const svg = ctx.files[file];
    if (typeof svg === "string") ctx.content.items.set(id, { file, ...ctx.content.items.get(id), worldSvg: svg });
  },
  // Raum- und Figuren-SVG sowie animations.json lädt der zugehörige JSON-Handler mit.
  roomSvg: undefined,
  characterSvg: undefined,
  animations: undefined,
};

function checkGame(ctx: Ctx) {
  const { game, rooms } = ctx.content;
  if (!game) {
    if (!("content/game.json" in ctx.files)) ctx.errors.push(err("content.game-missing", "content/game.json", "game.json fehlt"));
    return;
  }
  const start = rooms.get(game.startRoom);
  if (!start) ctx.errors.push(err("content.ref-missing", "content/game.json", `startRoom „${game.startRoom}“ gibt es nicht`));
  else if (!start.def.spawns[game.startSpawn])
    ctx.errors.push(err("content.ref-missing", "content/game.json", `startSpawn „${game.startSpawn}“ gibt es in „${game.startRoom}“ nicht`));
}

export function loadContent(files: ContentFiles): LoadResult {
  const content: ContentIndex = {
    rooms: new Map(), characters: new Map(), items: new Map(), dialogs: new Map(), cutscenes: new Map(),
  };
  const ctx: Ctx = { files, content, errors: [] };
  for (const file of Object.keys(files).sort()) {
    const c = classifyPath(file);
    if (c.kind === "unknown") ctx.errors.push(err("content.unknown-file", file, "Datei passt nicht ins Verzeichnisschema"));
    else if (c.kind !== "later") HANDLERS[c.kind]?.(ctx, c.id, file);
  }
  checkGame(ctx);
  return { content, errors: ctx.errors };
}
