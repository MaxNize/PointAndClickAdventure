// Browser-Adapter für Inhalte (Engine-Konzept: Schichten). Sammelt alle Dateien unter content/ per import.meta.glob,
// ein neuer Raum braucht deshalb keinen Eintrag im Code (NF-W-01). `@content` zeigt standardmäßig auf content/,
// für Tests über die Umgebungsvariable CONTENT_DIR auf einen anderen Ordner (vite.config.ts).
import type { ContentFiles } from "../core/content/load.ts";

const json = import.meta.glob("@content/**/*.json", { eager: true, import: "default" });
const svg = import.meta.glob("@content/**/*.svg", { eager: true, query: "?raw", import: "default" });

/** Schlüssel von Vite, z. B. `/e2e/fixtures/content/rooms/a/room.json` → `content/rooms/a/room.json`. */
function normalize(key: string): string {
  const at = key.indexOf(__CONTENT_DIR__);
  return at >= 0 ? `content/${key.slice(at + __CONTENT_DIR__.length)}` : key;
}

export function browserContentFiles(): ContentFiles {
  const files: ContentFiles = {};
  for (const [key, value] of [...Object.entries(json), ...Object.entries(svg)]) files[normalize(key)] = value;
  return files;
}
