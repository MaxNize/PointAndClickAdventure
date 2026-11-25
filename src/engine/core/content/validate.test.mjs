// Tests des Content-Validators (NF-V-01): Verweise, Flags und Dialoge über Dateien hinweg, dazu der Befehl.
import test from "node:test";
import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { repoRoot } from "../../../../tools/check/docs/lib.mjs";
import { readContent } from "../../../../tools/content/readContent.mjs";
import { validateContent } from "./validate.ts";

const ROOT = repoRoot();
const FIXTURE = path.join(ROOT, "e2e", "fixtures", "content");
const fixture = () => structuredClone(readContent(FIXTURE).files);
const ROOM = "content/rooms/testraum/room.json";
const say = (text) => ({ type: "say", text });
const found = (files) => validateContent(files).errors.map((e) => `${e.code} ${e.file} ${e.message}`);

const dialog = (nodes, start = "a") => ({ schemaVersion: 1, id: "d", start, nodes });
const node = (options) => ({ lines: [{ speaker: "player", text: "…" }], ...(options ? { options } : {}) });

test("NF-V-01: der Testraum besteht den Validator mit 0 Fehlern", () => {
  assert.deepEqual(found(fixture()), []);
});

test("NF-V-01: Verweise auf fehlende Räume, Figuren, Gegenstände, Dialoge und Sequenzen werden gemeldet", () => {
  const files = fixture();
  files[ROOM].hotspots["hotspot-kiste"].verbs.use = [
    { type: "changeRoom", room: "keller", spawn: "start" },
    { type: "if", cond: { hasItem: "schluessel" }, then: [{ type: "startDialog", dialog: "fehlt" }] },
    { type: "startCutscene", cutscene: "auch-fehlt" },
    { type: "say", speaker: "geist", text: "Buh." },
  ];
  assert.deepEqual(found(files), [
    `content.ref-missing ${ROOM} hotspots.hotspot-kiste.verbs.use.0: Raum „keller“ gibt es nicht`,
    `content.ref-missing ${ROOM} hotspots.hotspot-kiste.verbs.use.1.cond: Gegenstand „schluessel“ gibt es nicht`,
    `content.ref-missing ${ROOM} hotspots.hotspot-kiste.verbs.use.1.then.0: Dialog „fehlt“ gibt es nicht`,
    `content.ref-missing ${ROOM} hotspots.hotspot-kiste.verbs.use.2: Zwischensequenz „auch-fehlt“ gibt es nicht`,
    `content.ref-missing ${ROOM} hotspots.hotspot-kiste.verbs.use.3: Figur „geist“ gibt es nicht`,
  ]);
});

test("NF-V-01: Ausgang auf fehlenden Spawn und Gegenstand nur mit item.json werden richtig behandelt", () => {
  const files = fixture();
  files[ROOM].hotspots["hotspot-kiste"].exit = { room: "testraum", spawn: "hinten" };
  files[ROOM].hotspots["hotspot-kiste"].useItem = { trank: [say("Zisch.")] };
  files["content/items/trank/item.json"] = { schemaVersion: 1, id: "trank" };
  assert.deepEqual(found(files), [`content.ref-missing ${ROOM} hotspots.hotspot-kiste.exit: Spawn „hinten“ gibt es in „testraum“ nicht`]);
});

test("NF-V-01: gelesenes, aber nie gesetztes Flag meldet content.flag-never-set, taken-Flags sind ausgenommen", () => {
  const files = fixture();
  files[ROOM].parts = { offen: { visibleIf: { flag: "tuer-auf" } }, weg: { visibleIf: { not: { flag: "item.testraum.kugel.taken" } } } };
  assert.deepEqual(found(files), [`content.flag-never-set ${ROOM} parts.offen.visibleIf: Flag „tuer-auf“ wird nirgends gesetzt`]);
});

test("NF-V-01: Dialog mit fehlendem Knoten, unerreichbarem Knoten, Schleife ohne Ende und doppelter Option", () => {
  const files = fixture();
  files["content/dialogs/d.json"] = dialog({
    a: node([{ id: "x", text: "1", next: "b" }, { id: "x", text: "2", next: "fehlt" }]),
    b: node([{ id: "y", text: "3", next: "a" }]),
    insel: node(),
  });
  assert.deepEqual(found(files).map((l) => l.split(" ").slice(0, 3).join(" ")), [
    "dialog.node-unknown content/dialogs/d.json nodes.a.options.1.next:",
    "dialog.option-duplicate content/dialogs/d.json nodes.a.options.1:",
    "dialog.no-end content/dialogs/d.json nodes.a:",
    "dialog.no-end content/dialogs/d.json nodes.b:",
    "dialog.unreachable content/dialogs/d.json nodes.insel:",
  ]);
});

test("NF-V-01: Dialog mit Rücksprung und Ende ist gültig, Sprecher player ist erlaubt", () => {
  const files = fixture();
  files["content/dialogs/d.json"] = dialog({
    a: node([{ id: "frage", text: "?", next: "b" }, { id: "tschuess", text: "Tschüss", end: true }]),
    b: { lines: [{ speaker: "figur-b", text: "!" }], options: [{ id: "zurueck", text: "…", next: "a" }] },
  });
  assert.deepEqual(found(files), []);
});

test("NF-V-01: npm run validate meldet Fehler mit Code und Datei und endet mit Exit-Code 1", () => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), "validate-"));
  fs.cpSync(FIXTURE, dir, { recursive: true });
  fs.writeFileSync(path.join(dir, "cutscenes.json"), "{ kaputt");
  const run = (d) => spawnSync(process.execPath, [path.join(ROOT, "tools", "content", "validate.mjs"), d], { encoding: "utf8" });
  const bad = run(dir);
  assert.equal(bad.status, 1);
  assert.match(bad.stderr, /^content\.json-invalid content\/cutscenes\.json kein gültiges JSON/m);
  const good = run(FIXTURE);
  assert.equal(good.status, 0, good.stderr);
  assert.match(good.stdout, /0 Fehler/);
});
