// Gemeinsame Bausteine der Inhalts-Schemas (Asset-Vertrag, Begriffe). Zod ist die Quelle, die Doku die lesbare Fassung.
import { z } from "zod";

const ID_PART = "[a-z0-9]+(?:-[a-z0-9]+)*";

/** ID: Kleinbuchstaben, Ziffern, Bindestrich. Umlaute als ae, oe, ue, ss. */
export const id = z.string().regex(new RegExp(`^${ID_PART}$`), "ID-Format: Kleinbuchstaben, Ziffern, Bindestrich");

/** Flag: IDs mit Punkt getrennt, z. B. `kiste-offen` oder `item.testraum.kugel.taken`. */
export const flag = z
  .string()
  .regex(new RegExp(`^${ID_PART}(?:\\.${ID_PART})*$`), "Flag-Format: IDs mit Punkt getrennt");

/** Schlüssel mit festem Präfix, z. B. `hotspot-kiste` oder `layer-mid-block`. */
export const prefixedId = (prefix: string) =>
  z.string().regex(new RegExp(`^${prefix}${ID_PART}$`), `Name beginnt mit „${prefix}“, danach ID-Format`);

export const schemaVersion = z.literal(1);
export const text = z.string().min(1);
export const facing = z.enum(["left", "right", "front", "back"]);
export const point = z.tuple([z.number(), z.number()]);
export const position = z.strictObject({ x: z.number(), y: z.number() });
export const color = z.string().regex(/^#[0-9a-fA-F]{6}$/, "Farbe als #rrggbb");
export const positive = z.number().positive();

/** Keyframe für Figuren- und Raumanimationen. Werte relativ zur Ruhepose. */
export const keyframe = z.strictObject({
  t: z.number().min(0),
  rotate: z.number().optional(),
  x: z.number().optional(),
  y: z.number().optional(),
  scale: z.number().optional(),
  scaleX: z.number().optional(),
  scaleY: z.number().optional(),
  opacity: z.number().min(0).max(1).optional(),
  ease: z.enum(["linear", "in", "out", "inOut"]).optional(),
});

export type Facing = z.infer<typeof facing>;
export type Point = z.infer<typeof point>;
export type Position = z.infer<typeof position>;
export type Keyframe = z.infer<typeof keyframe>;
