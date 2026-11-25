// content/characters/<figur-id>/character.json und animations.json (Asset-Vertrag: Figur).
import { z } from "zod";
import { color, id, keyframe, point, positive, schemaVersion, text } from "./common.ts";

const pivotsOfView = z.record(id, point);

export const character = z.strictObject({
  schemaVersion,
  id,
  name: text,
  height: positive,
  speed: positive,
  textColor: color,
  pivots: z.strictObject({ side: pivotsOfView, front: pivotsOfView, back: pivotsOfView }),
});

const track = z.strictObject({ part: id, keyframes: z.array(keyframe).min(1) });
const view = z.strictObject({ tracks: z.array(track) });

const animation = z.strictObject({
  loop: z.boolean(),
  duration: positive,
  views: z.strictObject({ side: view.optional(), front: view.optional(), back: view.optional() }),
});

/** animations.json: Objekt Animationsname → Animation. Pflicht-Animationen prüft der Validator. */
export const animations = z.record(id, animation);

export type Character = z.infer<typeof character>;
export type Animation = z.infer<typeof animation>;
export type Animations = z.infer<typeof animations>;
