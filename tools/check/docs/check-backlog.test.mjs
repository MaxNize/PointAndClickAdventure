import test from "node:test";
import assert from "node:assert/strict";
import { findBacklogProblems, section } from "./check-backlog.mjs";

const row = (id, anf = "Das System muss a.", kri = "Test b.") => ({ id, line: 1, struck: false, cells: [id, "B", "Team", anf, kri] });
const body = (anf, kri) => `### Story-ID\n\nX\n\n### Anforderung\n\n${anf}\n\n### Akzeptanzkriterium\n\n${kri}\n\n### Abhängigkeiten\n\n**Blockiert durch:**\n\n---\nFuß`;
const issue = (n, title, b = body("Das System muss a.", "Test b."), labels = ["story"]) => ({ number: n, title, body: b, labels });
const rules = (rows, issues) => findBacklogProblems(rows, issues).map((p) => p.rule);

test("EP-21: passendes Issue (mit @Name im Titel) ist ok", () => {
  assert.deepEqual(rules([row("FA-E-01")], [issue(1, "FA-E-01 Raum laden @Ivan")]), []);
});
test("EP-21: Katalogzeile ohne Issue wird gemeldet", () => {
  assert.deepEqual(rules([row("FA-E-01")], []), ["docs.backlog_missing"]);
});
test("EP-21: zwei Issues zur selben ID werden gemeldet", () => {
  const two = [issue(1, "FA-E-01 A"), issue(2, "FA-E-01 B")];
  assert.deepEqual(rules([row("FA-E-01")], two), ["docs.backlog_duplicate"]);
});
test("EP-21: geänderter Wortlaut im Issue wird gemeldet", () => {
  const drift = issue(1, "FA-E-01 A", body("Das System muss etwas anderes.", "Test b."));
  const [p] = findBacklogProblems([row("FA-E-01")], [drift]);
  assert.equal(p.rule, "docs.backlog_drift");
  assert.match(p.message, /^#1: Anforderung weicht/);
});
test("EP-21: geändertes Akzeptanzkriterium wird gemeldet", () => {
  const drift = issue(1, "FA-E-01 A", body("Das System muss a.", "anders"));
  assert.match(findBacklogProblems([row("FA-E-01")], [drift])[0].message, /Akzeptanzkriterium/);
});
test("EP-21: Issue mit ID, die nicht im Katalog steht, wird gemeldet", () => {
  assert.deepEqual(rules([], [issue(1, "FA-E-09 X")]), ["docs.backlog_orphan"]);
});
test("EP-21: Prozess-Issues und Issues ohne ID sind ausgenommen", () => {
  const skip = [issue(1, "FA-E-77 X", "", ["prozess"]), issue(2, "Ein Fehler", "", ["bug"])];
  assert.deepEqual(rules([], skip), []);
});
test("EP-21: Zeilenumbrüche und Leerraum spielen keine Rolle", () => {
  const crlf = issue(1, "FA-E-01 A", body("Das System\r\nmuss   a.", "Test b.").replace(/\n/g, "\r\n"));
  assert.deepEqual(rules([row("FA-E-01")], [crlf]), []);
  assert.equal(section("### X\n\ntext\n\n### Y\n\nz", "X"), "text");
});
