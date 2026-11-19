import test from "node:test";
import assert from "node:assert/strict";
import { countRows, findCountProblems } from "./check-counts.mjs";
import { CATALOG } from "./lib.mjs";

const row = (id, extra = "") => `| ${id} | B | Team | Das System muss x.${extra} | y |`;
const catalog = [row("NF-A-01"), row("FA-E-01"), row("FA-G-01"), row("EP-01"), row("EP-02", " gestrichen")].join("\n");
const config = { mentions: [{ file: "docs/README.md", pattern: "(\\d+) NF", group: "NF" }, { file: "docs/README.md", pattern: "(\\d+) FA-E", group: "FA-E" }] };

test("EP-20: Zeilen werden je Gruppe gezählt, gestrichene nicht", () => {
  assert.deepEqual(countRows(catalog), { NF: 1, FA: 2, "FA-E": 1, "FA-G": 1, EP: 1 });
});
test("EP-20: übereinstimmende Zahlen sind ok", () => {
  assert.deepEqual(findCountProblems({ [CATALOG]: catalog, "docs/README.md": "1 NF, 1 FA-E" }, config), []);
});
test("EP-20: abweichende Zahl wird mit Zeile gemeldet", () => {
  const [p] = findCountProblems({ [CATALOG]: catalog, "docs/README.md": "x\n16 NF, 1 FA-E" }, config);
  assert.equal(p.rule, "docs.count_mismatch");
  assert.equal(p.line, 2);
  assert.match(p.message, /sagt 16, Katalog hat 1/);
});
test("EP-20: verschwundene Fundstelle ist ein Fund", () => {
  const [p] = findCountProblems({ [CATALOG]: catalog, "docs/README.md": "umformuliert" }, config);
  assert.equal(p.rule, "docs.count_mismatch");
  assert.match(p.message, /Fundstelle fehlt/);
});
