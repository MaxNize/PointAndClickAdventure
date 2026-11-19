import test from "node:test";
import assert from "node:assert/strict";
import { findIdProblems } from "./check-ids.mjs";
import { CATALOG } from "./lib.mjs";

const row = (id) => `| ${id} | Bereich | Team | Das System muss x. | y |`;
const catalog = (...ids) => ids.map(row).join("\n");

test("EP-18: eindeutige IDs sind ok", () => {
  assert.deepEqual(findIdProblems({ [CATALOG]: catalog("FA-E-01", "EP-01") }), []);
});
test("EP-18: doppelt definierte ID wird mit beiden Zeilen gemeldet", () => {
  const [p] = findIdProblems({ [CATALOG]: catalog("FA-E-01", "EP-01", "FA-E-01") });
  assert.equal(p.rule, "docs.id_duplicate");
  assert.equal(p.line, 3);
  assert.match(p.message, /Zeile 1/);
});
test("EP-19: Verweis auf definierte ID ist ok", () => {
  assert.deepEqual(findIdProblems({ [CATALOG]: catalog("FA-E-01"), "docs/a.md": "siehe FA-E-01" }), []);
});
test("EP-19: Verweis auf nicht definierte ID wird gemeldet", () => {
  const [p] = findIdProblems({ [CATALOG]: catalog("FA-E-01"), "docs/a.md": "x\nsiehe NF-W-09" });
  assert.equal(p.rule, "docs.id_undefined");
  assert.equal(p.file, "docs/a.md");
  assert.equal(p.line, 2);
});
test("EP-19: fremde IDs (Creative-Original, Architektur, PflanzenDex) sind keine Projekt-IDs", () => {
  const text = "FA-01 E-01 N-04 QG-T1 FA-DEV-ohne-Nummer FA-G-xx";
  assert.deepEqual(findIdProblems({ [CATALOG]: catalog("FA-E-01"), "docs/a.md": text }), []);
});
test("EP-19: ID-Bereiche in Tabellenzeilen anderer Dateien definieren nichts", () => {
  const files = { [CATALOG]: catalog("FA-E-01"), "docs/b.md": "| FA-G-01 | Tabelle |" };
  assert.equal(findIdProblems(files)[0].rule, "docs.id_undefined");
});
