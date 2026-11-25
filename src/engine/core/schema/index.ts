// Einstieg in die Inhalts-Schemas (NF-V-01). Renderer, Validator und Agenten nutzen dieselben Schemas.
// Gegenstände und Rezepte folgen nach der Entscheidung zur Alchemie-Mechanik.
import type { z } from "zod";
import { animations, character } from "./character.ts";
import { cutscene, dialog } from "./dialog.ts";
import { game } from "./game.ts";
import { room } from "./room.ts";

export const contentSchemas = { game, room, character, animations, dialog, cutscene } as const;

export type ContentKind = keyof typeof contentSchemas;
export type ContentOf<K extends ContentKind> = z.infer<(typeof contentSchemas)[K]>;

/** Fehler mit stabilem Code `<bereich>.<grund>` (Asset-Vertrag: Fehlercodes). */
export type ContentError = { code: string; file: string; message: string };

export type ParseResult<T> = { ok: true; value: T } | { ok: false; errors: ContentError[] };

const pathOf = (path: readonly PropertyKey[]) => (path.length ? path.map(String).join(".") : "(Datei)");

/** Prüft eine Inhaltsdatei gegen ihr Schema. Jede Abweichung wird ein Fehler `content.schema` mit Feldpfad. */
export function parseContent<K extends ContentKind>(kind: K, data: unknown, file: string): ParseResult<ContentOf<K>> {
  const result = contentSchemas[kind].safeParse(data);
  if (result.success) return { ok: true, value: result.data as ContentOf<K> };
  const errors = result.error.issues.map((issue) => ({
    code: "content.schema",
    file,
    message: `${pathOf(issue.path)}: ${describe(issue)}`,
  }));
  return { ok: false, errors };
}

// Zod meldet bei falschen Schlüsseln nur „Invalid key in record“. Der eigentliche Grund steckt im inneren Fehler.
function describe(issue: z.core.$ZodIssue): string {
  if (issue.code === "invalid_key" && issue.issues[0]) return `ungültiger Schlüssel: ${issue.issues[0].message}`;
  return issue.message;
}

export type { Animation, Animations, Character } from "./character.ts";
export type { Facing, Keyframe, Point, Position } from "./common.ts";
export type { Condition } from "./condition.ts";
export type { Cutscene, Dialog, DialogNode } from "./dialog.ts";
export type { Effect, IfEffect } from "./effect.ts";
export { EFFECT_TYPES } from "./effect.ts";
export type { Game } from "./game.ts";
export type { CharacterPlacement, Hotspot, ItemPlacement, Room, RoomAnimation } from "./room.ts";
