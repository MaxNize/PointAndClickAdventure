// Tests der Inhalts-Schemas (NF-V-01). Die Beispiele im Asset-Vertrag sind Testfälle: Weichen Doku und Schema
// voneinander ab, wird der Test rot. So bleibt der Vertrag die lesbare Fassung der Schemas.
import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { repoRoot } from "../../../../tools/check/docs/lib.mjs";
import { EFFECT_TYPES, parseContent } from "./index.ts";

const CONTRACT = path.join(repoRoot(), "docs", "architektur", "asset-vertrag");

// Überschrift im Vertrag → Schema. Andere JSON-Beispiele (Gegenstand, Rezept, Ablauf) haben noch kein Schema.
const KIND_BY_HEADING = {
  "README.md#Spiel": "game",
  "raum.md#room.json": "room",
  "figur.md#character.json": "character",
  "figur.md#animations.json": "animations",
  "aktionen.md#Dialog": "dialog",
  "aktionen.md#Zwischensequenz": "cutscene",
};

function contractExamples() {
  const out = [];
  for (const file of fs.readdirSync(CONTRACT).filter((f) => f.endsWith(".md"))) {
    let heading = "";
    const re = /^## (.+)$|^```json\n([\s\S]*?)^```$/gm;
    for (const m of fs.readFileSync(path.join(CONTRACT, file), "utf8").replace(/\r/g, "").matchAll(re)) {
      if (m[1]) heading = m[1].trim();
      else if (KIND_BY_HEADING[`${file}#${heading}`]) out.push({ where: `${file}#${heading}`, kind: KIND_BY_HEADING[`${file}#${heading}`], json: m[2] });
    }
  }
  return out;
}

const examples = contractExamples();
const example = (kind) => structuredClone(JSON.parse(examples.find((e) => e.kind === kind).json));

function rejects(kind, data, pattern) {
  const r = parseContent(kind, data, `test/${kind}.json`);
  assert.equal(r.ok, false, `${kind} wurde fälschlich angenommen`);
  assert.ok(r.errors.every((e) => e.code === "content.schema" && e.file === `test/${kind}.json`));
  assert.match(r.errors.map((e) => e.message).join("\n"), pattern);
}

test("NF-V-01: jedes Schema hat ein Beispiel im Asset-Vertrag", () => {
  assert.deepEqual([...new Set(examples.map((e) => e.kind))].sort(), Object.values(KIND_BY_HEADING).sort());
});

test("NF-V-01: alle Beispiele aus dem Asset-Vertrag bestehen ihr Schema", () => {
  for (const { where, kind, json } of examples) {
    const r = parseContent(kind, JSON.parse(json), where);
    assert.ok(r.ok, `${where}: ${r.ok ? "" : r.errors.map((e) => e.message).join("; ")}`);
  }
});

test("NF-V-01: unbekannter Effekt-Typ wird mit Feldpfad abgelehnt", () => {
  const room = example("room");
  room.hotspots["hotspot-kiste"].verbs.look = [{ type: "sagen", text: "Hallo" }];
  rejects("room", room, /hotspots\.hotspot-kiste\.verbs\.look\.0/);
});

test("NF-V-01: Hotspot ohne verbs.look wird abgelehnt", () => {
  const room = example("room");
  delete room.hotspots["hotspot-kiste"].verbs.look;
  rejects("room", room, /verbs\.look/);
});

test("NF-V-01: IDs mit Großbuchstaben oder Unterstrich werden abgelehnt", () => {
  rejects("room", { ...example("room"), id: "side_leg" }, /^id: ID-Format/m);
  rejects("character", { ...example("character"), id: "Figur" }, /^id: ID-Format/m);
});

test("NF-V-01: Hotspot-Schlüssel ohne Präfix hotspot- wird abgelehnt", () => {
  const room = example("room");
  room.hotspots = { kiste: room.hotspots["hotspot-kiste"] };
  rejects("room", room, /hotspot-/);
});

test("NF-V-01: unbekanntes Feld wird abgelehnt, damit Tippfehler auffallen", () => {
  rejects("game", { ...example("game"), startraum: "testraum" }, /startraum/);
});

test("NF-V-01: Bedingung mit zwei Schlüsseln wird abgelehnt", () => {
  const room = example("room");
  room.parts["kiste-zu"].visibleIf = { flag: "a", hasItem: "b" };
  rejects("room", room, /parts\.kiste-zu\.visibleIf/);
});

test("NF-V-01: verschachtelte Bedingungen und if-Effekte werden angenommen", () => {
  const room = example("room");
  room.onEnter = [{ type: "if", cond: { all: [{ not: { flag: "a.b" } }, { any: [{ hasItem: "kugel" }] }] },
    then: [{ type: "if", cond: { flag: "x" }, then: [{ type: "say", text: "Tief verschachtelt." }] }] }];
  assert.ok(parseContent("room", room, "test").ok);
});

test("NF-V-01: depth.near.y muss größer als depth.far.y sein", () => {
  const room = example("room");
  room.depth.near.y = room.depth.far.y;
  rejects("room", room, /depth\.near\.y/);
});

test("NF-V-01: walkTo-Effekt braucht entweder Punkt oder Hotspot", () => {
  const steps = (s) => ({ ...example("cutscene"), steps: [s] });
  rejects("cutscene", steps({ type: "walkTo", x: 1, y: 2, hotspot: "hotspot-tuer" }), /walkTo/);
  rejects("cutscene", steps({ type: "walkTo", x: 1 }), /walkTo/);
  assert.ok(parseContent("cutscene", steps({ type: "walkTo", hotspot: "tuer" }), "test").ok);
});

test("NF-V-01: Dialog-Option braucht entweder next oder end", () => {
  const dialog = example("dialog");
  dialog.nodes.hallo.options[0].end = true;
  rejects("dialog", dialog, /next oder end/);
});

test("NF-V-01: Keyframe mit opacity über 1 wird abgelehnt", () => {
  const anims = example("animations");
  anims.idle.views.side.tracks[0].keyframes[0].opacity = 2;
  rejects("animations", anims, /idle\.views\.side\.tracks\.0\.keyframes\.0\.opacity/);
});

test("NF-V-01: Effekt-Vokabular entspricht dem Asset-Vertrag", () => {
  const doc = fs.readFileSync(path.join(CONTRACT, "aktionen.md"), "utf8").replace(/\r/g, "");
  const section = doc.split("### Effekte")[1].split(/^##/m)[0];
  const documented = [...section.matchAll(/^\| `(\w+)` \|/gm)].map((m) => m[1]).filter((t) => t !== "type");
  assert.deepEqual([...EFFECT_TYPES].sort(), documented.sort());
});
