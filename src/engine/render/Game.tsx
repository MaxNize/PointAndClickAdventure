// Einstieg der Darstellung: lädt alle Inhalte und zeigt den Startraum aus game.json (FA-E-01).
import { useMemo } from "react";
import { browserContentFiles } from "../adapters/browserContent.ts";
import { loadContent } from "../core/content/load.ts";
import { ErrorList } from "./ErrorList.tsx";
import { RoomView } from "./RoomView.tsx";
import { buildRoomSvg } from "./roomSvg.ts";
import "./game.css";

const { content, errors: loadErrors } = loadContent(browserContentFiles());

export function Game() {
  const start = content.game ? content.rooms.get(content.game.startRoom) : undefined;
  const room = useMemo(() => (start ? buildRoomSvg(start) : undefined), [start]);
  return (
    <main className="game" data-testid="game">
      {room ? <RoomView element={room.element} /> : <p className="no-room">Kein Startraum. Details in der Fehlerliste.</p>}
      <ErrorList errors={[...loadErrors, ...(room?.errors ?? [])]} />
    </main>
  );
}
