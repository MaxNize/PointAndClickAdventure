// Tiefenskalierung (FA-E-10, Engine-Konzept: Raum, Koordinaten und Tiefe). Linear zwischen depth.far und depth.near,
// außerhalb geklemmt.
import type { Room } from "../schema/index.ts";

export function depthScale(y: number, depth: Room["depth"]): number {
  const { far, near } = depth;
  const t = Math.min(1, Math.max(0, (y - far.y) / (near.y - far.y)));
  return far.scale + t * (near.scale - far.scale);
}
