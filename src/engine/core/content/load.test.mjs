// Tests des Loaders (FA-E-01). Der Testraum liegt unter e2e/fixtures/content und dient auch dem E2E-Test.
import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { repoRoot } from "../../../../tools/check/docs/lib.mjs";
import { loadContent } from "./load.ts";
import { classifyPath } from "./paths.ts";

const FIXTURE = path.join(repoRoot(), "e2e", "fixtures", "content");

/** Liest einen Inhaltsordner wie der Browser-Adapter: JSON geparst, SVG als Text, Schlüssel `content/…`. */
function readContent(dir) {
  const files = {};
  for (const rel of fs.readdirSync(dir, { recursive: true })) {
    const full = path.join(dir, rel);
    if (fs.statSync(full).isDirectory()) continue;
    const text = fs.readFileSync(full, "utf8");
    files[`content/${rel.split(path.sep).join("/")}`] = rel.endsWith(".json") ? JSON.parse(text) : text;
  }
  return files;
}

const codes = (r) => r.errors.map((e) => `${e.code} ${e.file}`);

test("FA-E-01: Testraum wird aus room.json und room.svg geladen", () => {
  const r = loadContent(readContent(FIXTURE));
  assert.deepEqual(r.errors, []);
  assert.equal(r.content.game?.startRoom, "testraum");
  const room = r.content.rooms.get("testraum");
  assert.equal(room?.def.name, "Testraum für E2E-Tests");
  assert.match(room?.svg ?? "", /<g id="layer-background">/);
});

test("FA-E-01: fehlende game.json meldet content.game-missing", () => {
  const files = readContent(FIXTURE);
  delete files["content/game.json"];
  assert.deepEqual(codes(loadContent(files)), ["content.game-missing content/game.json"]);
});

test("FA-E-01: Raum ohne room.svg meldet room.svg-missing", () => {
  const files = readContent(FIXTURE);
  delete files["content/rooms/testraum/room.svg"];
  const r = loadContent(files);
  assert.ok(codes(r).includes("room.svg-missing content/rooms/testraum/room.json"));
  assert.ok(codes(r).includes("content.ref-missing content/game.json"), "startRoom fehlt dann ebenfalls");
});

test("FA-E-01: id, die vom Ordnernamen abweicht, meldet content.id-mismatch", () => {
  const files = readContent(FIXTURE);
  files["content/rooms/anderer/room.json"] = files["content/rooms/testraum/room.json"];
  files["content/rooms/anderer/room.svg"] = files["content/rooms/testraum/room.svg"];
  assert.deepEqual(codes(loadContent(files)), ["content.id-mismatch content/rooms/anderer/room.json"]);
});

test("FA-E-01: Schemafehler nennt Datei und Feld, der Rest wird trotzdem geladen", () => {
  const files = readContent(FIXTURE);
  files["content/dialogs/kaputt.json"] = { schemaVersion: 1, id: "kaputt", start: "a" };
  const r = loadContent(files);
  assert.deepEqual(r.errors.map((e) => `${e.code} ${e.file} ${e.message}`), [
    "content.schema content/dialogs/kaputt.json nodes: Invalid input: expected record, received undefined",
  ]);
  assert.ok(r.content.rooms.has("testraum"));
});

test("FA-E-01: unbekannte Dateien werden gemeldet, vorgesehene ohne Schema übersprungen", () => {
  const files = readContent(FIXTURE);
  files["content/rooms/testraum/notizen.txt"] = "x";
  files["content/items/kugel/item.json"] = {};
  assert.deepEqual(codes(loadContent(files)), ["content.unknown-file content/rooms/testraum/notizen.txt"]);
});

test("FA-E-01: startRoom und startSpawn müssen existieren", () => {
  const files = readContent(FIXTURE);
  files["content/game.json"] = { ...files["content/game.json"], startSpawn: "nirgends" };
  assert.deepEqual(codes(loadContent(files)), ["content.ref-missing content/game.json"]);
});

test("FA-E-01: Pfade werden den Dateiarten aus dem Asset-Vertrag zugeordnet", () => {
  assert.deepEqual(classifyPath("content/rooms/halle/room.svg"), { kind: "roomSvg", id: "halle" });
  assert.deepEqual(classifyPath("content/characters/lehrling/animations.json"), { kind: "animations", id: "lehrling" });
  assert.deepEqual(classifyPath("content/dialogs/begruessung.json"), { kind: "dialog", id: "begruessung" });
  assert.deepEqual(classifyPath("content/states/manual/x.json"), { kind: "later" });
  assert.deepEqual(classifyPath("content/rooms/halle/extra/room.json"), { kind: "unknown" });
});
