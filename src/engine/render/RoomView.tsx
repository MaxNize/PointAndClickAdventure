// Zeigt einen Raum (FA-E-01). Das SVG wird außerhalb von React gebaut und eingehängt, damit spätere Bewegungen
// Transforms direkt setzen können, ohne React-Re-Render pro Frame (Engine-Konzept: Zeitmodell).
import { useLayoutEffect, useRef } from "react";

export function RoomView({ element }: { element: SVGSVGElement }) {
  const host = useRef<HTMLDivElement>(null);
  useLayoutEffect(() => {
    host.current?.replaceChildren(element);
  }, [element]);
  return <div ref={host} className="room" />;
}
