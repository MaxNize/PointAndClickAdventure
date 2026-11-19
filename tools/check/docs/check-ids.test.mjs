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

test("EP-19: ID aus der Baseline ist erlaubt, eine neue undefinierte ID nicht", () => {
  const files = { [CATALOG]: catalog("FA-E-01"), "docs/a.md": "FA-E-03 und NF-W-09" };
  const problems = findIdProblems(files, ["FA-E-03"]);
  assert.deepEqual(problems.map((p) => p.rule), ["docs.id_undefined"]);
  assert.match(problems[0].message, /NF-W-09/);
});
test("EP-19: ID in der Baseline, die jetzt im Katalog steht, ist ein Fund (Baseline schrumpft)", () => {
  const files = { [CATALOG]: catalog("FA-E-01", "FA-E-03"), "docs/a.md": "FA-E-03" };
  const [p] = findIdProblems(files, ["FA-E-03"]);
  assert.equal(p.rule, "docs.id_baseline_stale");
  assert.match(p.message, /im Katalog definiert/);
});
test("EP-19: ID in der Baseline, die nirgends mehr verwiesen wird, ist ein Fund", () => {
  const [p] = findIdProblems({ [CATALOG]: catalog("FA-E-01"), "docs/a.md": "nichts" }, ["FA-E-03"]);
  assert.equal(p.rule, "docs.id_baseline_stale");
  assert.match(p.message, /nirgends mehr verwiesen/);
});
