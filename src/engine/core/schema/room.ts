// content/rooms/<raum-id>/room.json (Asset-Vertrag: Raum). Prüfungen gegen das SVG und über Dateien hinweg
// macht der Validator, nicht dieses Schema.
import { z } from "zod";
import { facing, id, keyframe, point, position, positive, prefixedId, schemaVersion, text } from "./common.ts";
import { condition } from "./condition.ts";
import { effectList } from "./effect.ts";

const optionalVerbs = {
  take: effectList.optional(),
  use: effectList.optional(),
  open: effectList.optional(),
  talk: effectList.optional(),
};
/** Verben eines Interaktionsziels, `look` ist Pflicht. */
const verbs = z.strictObject({ look: effectList, ...optionalVerbs });
const itemEffects = z.record(id, effectList);

const hotspot = z.strictObject({
  name: text,
  visibleIf: condition.optional(),
  walkTo: position,
  facing: facing.optional(),
  exit: z
    .strictObject({ room: id, spawn: id, if: condition.optional(), else: effectList.optional() })
    .optional(),
  verbs,
  useItem: itemEffects.optional(),
});

const itemPlacement = z.strictObject({
  item: id,
  x: z.number(),
  y: z.number(),
  walkTo: position,
  visibleIf: condition.optional(),
  verbs: z.strictObject({ look: effectList.optional(), ...optionalVerbs }).optional(),
});

const characterPlacement = z.strictObject({
  character: id,
  x: z.number(),
  y: z.number(),
  facing,
  walkTo: position,
  visibleIf: condition.optional(),
  verbs,
  give: itemEffects.optional(),
});

const roomAnimation = z.strictObject({
  part: id,
  duration: positive,
  delay: z.number().min(0).optional(),
  origin: point.optional(),
  keyframes: z.array(keyframe).min(1),
});

const depthPoint = z.strictObject({ y: z.number(), scale: positive });
const spawn = z.strictObject({ x: z.number(), y: z.number(), facing });

export const room = z.strictObject({
  schemaVersion,
  id,
  name: text,
  walkable: z.strictObject({
    outer: z.array(point).min(3),
    holes: z.array(z.array(point).min(3)).optional(),
  }),
  depth: z
    .strictObject({ far: depthPoint, near: depthPoint })
    .refine((d) => d.near.y > d.far.y, { message: "depth.near.y muss größer sein als depth.far.y" }),
  spawns: z
    .record(id, spawn)
    .refine((s) => Object.keys(s).length > 0, { message: "mindestens ein Spawn" }),
  layers: z.record(prefixedId("layer-mid-"), z.strictObject({ baseline: z.number() })).optional(),
  hotspots: z.record(prefixedId("hotspot-"), hotspot).optional(),
  parts: z.record(id, z.strictObject({ visibleIf: condition })).optional(),
  animations: z.array(roomAnimation).optional(),
  items: z.array(itemPlacement).optional(),
  characters: z.array(characterPlacement).optional(),
  onEnter: effectList.optional(),
});

export type Room = z.infer<typeof room>;
export type Hotspot = z.infer<typeof hotspot>;
export type CharacterPlacement = z.infer<typeof characterPlacement>;
export type ItemPlacement = z.infer<typeof itemPlacement>;
export type RoomAnimation = z.infer<typeof roomAnimation>;
