// content/dialogs/<id>.json und content/cutscenes/<id>.json (Asset-Vertrag: Dialog, Zwischensequenz).
// Erreichbarkeit der Knoten und Wege zum Ende prüft der Validator.
import { z } from "zod";
import { id, schemaVersion, text } from "./common.ts";
import { condition } from "./condition.ts";
import { effectList } from "./effect.ts";

const option = z
  .strictObject({
    id,
    text,
    if: condition.optional(),
    effects: effectList.optional(),
    next: id.optional(),
    end: z.literal(true).optional(),
  })
  .refine((o) => (o.next === undefined) !== (o.end === undefined), {
    message: "Option braucht entweder next oder end",
  });

const node = z.strictObject({
  lines: z.array(z.strictObject({ speaker: id, text })).min(1),
  effects: effectList.optional(),
  options: z.array(option).optional(),
});

export const dialog = z.strictObject({
  schemaVersion,
  id,
  start: id,
  nodes: z.record(id, node),
});

export const cutscene = z.strictObject({ schemaVersion, id, steps: effectList.min(1) });

export type Dialog = z.infer<typeof dialog>;
export type DialogNode = z.infer<typeof node>;
export type Cutscene = z.infer<typeof cutscene>;
