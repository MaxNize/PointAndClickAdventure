import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { Game } from "./engine/render/Game";

const root = document.getElementById("root");
if (!root) throw new Error("render.root_missing: Element #root fehlt in index.html");

createRoot(root).render(
  <StrictMode>
    <Game />
  </StrictMode>,
);
