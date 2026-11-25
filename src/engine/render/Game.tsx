// Einstieg der Darstellung: lädt alle Inhalte und zeigt den Startraum aus game.json mit der Spielfigur am Startspawn
// (FA-E-01, FA-E-03).
import { useMemo } from "react";
import { browserContentFiles } from "../adapters/browserContent.ts";
import { loadContent } from "../core/content/load.ts";
import { sceneActors } from "../core/scene/actors.ts";
import { initialState } from "../core/state/conditions.ts";
import { ErrorList } from "./ErrorList.tsx";
import { RoomView } from "./RoomView.tsx";
import { buildRoomSvg } from "./roomSvg.ts";
import "./game.css";

const { content, errors: loadErrors } = loadContent(browserContentFiles());

export function Game() {
  const game = content.game;
  const start = game ? content.rooms.get(game.startRoom) : undefined;
  const scene = useMemo(() => {
    if (!game || !start) return undefined;
    const { actors, errors } = sceneActors(content, game.startRoom, game.startSpawn, initialState());
    const room = buildRoomSvg(start, content, actors);
    return { room, errors: [...errors, ...room.errors] };
  }, [game, start]);
  return (
    <main className="game" data-testid="game">
      {scene ? <RoomView room={scene.room} /> : <p className="no-room">Kein Startraum. Details in der Fehlerliste.</p>}
      <ErrorList errors={[...loadErrors, ...(scene?.errors ?? [])]} />
    </main>
  );
}
