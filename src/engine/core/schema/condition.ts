// Bedingungen (Asset-Vertrag: Aktionen). Ein Objekt mit genau einem Schlüssel, beliebig verschachtelbar.
import { z } from "zod";
import { flag, id } from "./common.ts";

export type Condition =
  | { flag: string }
  | { hasItem: string }
  | { not: Condition }
  | { all: Condition[] }
  | { any: Condition[] };

export const condition: z.ZodType<Condition> = z.lazy(() =>
  z.union([
    z.strictObject({ flag }),
    z.strictObject({ hasItem: id }),
    z.strictObject({ not: condition }),
    z.strictObject({ all: z.array(condition).min(1) }),
    z.strictObject({ any: z.array(condition).min(1) }),
  ], { error: "Bedingung braucht genau einen Schlüssel: flag, hasItem, not, all oder any" }),
);
