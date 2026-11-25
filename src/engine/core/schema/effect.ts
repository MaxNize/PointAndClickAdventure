// Effekte (Asset-Vertrag: Aktionen). Fest definiertes Vokabular, Erweiterung nur per Story.
import { z } from "zod";
import { facing, flag, id, positive, text } from "./common.ts";
import { condition, type Condition } from "./condition.ts";

const say = z.strictObject({ type: z.literal("say"), text, speaker: id.optional() });
const setFlag = z.strictObject({ type: z.literal("setFlag"), flag });
const clearFlag = z.strictObject({ type: z.literal("clearFlag"), flag });
const addItem = z.strictObject({ type: z.literal("addItem"), item: id });
const removeItem = z.strictObject({ type: z.literal("removeItem"), item: id });
const pickUp = z.strictObject({ type: z.literal("pickUp"), item: id });
const face = z.strictObject({ type: z.literal("face"), facing, character: id.optional() });
const playAnimation = z.strictObject({ type: z.literal("playAnimation"), animation: id, character: id.optional() });
const changeRoom = z.strictObject({ type: z.literal("changeRoom"), room: id, spawn: id });
const startDialog = z.strictObject({ type: z.literal("startDialog"), dialog: id });
const startCutscene = z.strictObject({ type: z.literal("startCutscene"), cutscene: id });
const wait = z.strictObject({ type: z.literal("wait"), ms: positive });
const endGame = z.strictObject({ type: z.literal("endGame") });

/** Ziel ist entweder ein Punkt (`x`, `y`) oder ein Hotspot, nie beides. */
const walkTo = z
  .strictObject({
    type: z.literal("walkTo"),
    x: z.number().optional(),
    y: z.number().optional(),
    hotspot: id.optional(),
    character: id.optional(),
  })
  .refine((e) => (e.hotspot === undefined) === (e.x !== undefined && e.y !== undefined), {
    message: "walkTo braucht entweder x und y oder hotspot",
  })
  .refine((e) => (e.x === undefined) === (e.y === undefined), { message: "walkTo braucht x und y zusammen" });

const simpleEffects = [
  say, setFlag, clearFlag, addItem, removeItem, pickUp, walkTo, face,
  playAnimation, changeRoom, startDialog, startCutscene, wait, endGame,
] as const;

type SimpleEffect = z.infer<(typeof simpleEffects)[number]>;
export type IfEffect = { type: "if"; cond: Condition; then: Effect[]; else?: Effect[] | undefined };
export type Effect = SimpleEffect | IfEffect;

const effectRef: z.ZodType<Effect> = z.lazy(() => effect);

const ifEffect = z.strictObject({
  type: z.literal("if"),
  cond: condition,
  then: z.array(effectRef),
  else: z.array(effectRef).optional(),
});

export const effect: z.ZodType<Effect> = z.discriminatedUnion("type", [...simpleEffects, ifEffect]);
export const effectList = z.array(effect);

/** Alle Effekt-Typen, z. B. für Agenten-Skills und Fehlermeldungen. */
export const EFFECT_TYPES = [...simpleEffects, ifEffect].map((s) => s.shape.type.value);
