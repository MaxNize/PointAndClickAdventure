// content/game.json (Asset-Vertrag: Spiel). Genau eine Datei.
import { z } from "zod";
import { id, positive, schemaVersion, text } from "./common.ts";

export const game = z.strictObject({
  schemaVersion,
  title: text,
  startRoom: id,
  startSpawn: id,
  player: id,
  defaults: z.strictObject({ look: text, useItem: text, give: text, combine: text }),
  text: z.strictObject({ minMs: positive, msPerChar: positive }),
});

export type Game = z.infer<typeof game>;
