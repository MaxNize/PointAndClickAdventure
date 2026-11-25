// Zeigt einen Raum (FA-E-01). Das SVG wird außerhalb von React gebaut und eingehängt, damit spätere Bewegungen
// Transforms direkt setzen können, ohne React-Re-Render pro Frame (Engine-Konzept: Zeitmodell).
import { useLayoutEffect, useRef } from "react";
import type { BuiltRoom } from "./roomSvg.ts";

export function RoomView({ room }: { room: BuiltRoom }) {
  const host = useRef<HTMLDivElement>(null);
  useLayoutEffect(() => {
    host.current?.replaceChildren(room.element);
    room.layout();
  }, [room]);
  return <div ref={host} className="room" />;
}
