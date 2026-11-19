import test from "node:test";
import assert from "node:assert/strict";
import { anchors, findLinkProblems, slug } from "./check-links.mjs";

const tracked = new Set(["README.md", "docs/a.md", "docs/b.md", "docs/dir/x.md", ".github/ISSUE_TEMPLATE/story.yml"]);
const run = (files) => findLinkProblems(files, tracked);

test("EP-17: Link auf vorhandene Datei ist ok", () => {
  assert.deepEqual(run({ "docs/a.md": "[b](b.md) [x](dir/x.md) [t](../.github/ISSUE_TEMPLATE/story.yml)" }), []);
});
test("EP-17: Link auf fehlende Datei wird mit Zeile gemeldet", () => {
  const [p] = run({ "docs/a.md": "Text\n[b](fehlt.md)" });
  assert.equal(p.rule, "docs.link_broken");
  assert.equal(p.file, "docs/a.md");
  assert.equal(p.line, 2);
});
test("EP-17: Link auf Ordner ist ok", () => {
  assert.deepEqual(run({ "README.md": "[d](docs/dir/)" }), []);
});
test("EP-17: Anker mit Umlaut wird nach der GitHub-Regel aufgelöst", () => {
  const files = { "docs/a.md": "[q](b.md#qualitätskriterien)", "docs/b.md": "## Qualitätskriterien\n" };
  assert.deepEqual(run(files), []);
});
test("EP-17: fehlender Anker wird gemeldet", () => {
  const files = { "docs/a.md": "[q](b.md#gibt-es-nicht)", "docs/b.md": "# Titel\n" };
  assert.equal(run(files)[0].rule, "docs.link_broken");
});
test("EP-17: Anker in derselben Datei und doppelte Überschrift", () => {
  const text = "# A\n## Teil\n## Teil\n[1](#teil) [2](#teil-1) [3](#teil-2)";
  assert.equal(run({ "README.md": text }).length, 1);
});
test("EP-17: externe Links, Codeblöcke und Inline-Code werden ignoriert", () => {
  const text = "[w](https://example.org/x) [m](mailto:a@b.de)\n```\n[k](fehlt.md)\n```\n`[i](fehlt.md)`";
  assert.deepEqual(run({ "README.md": text }), []);
});
test("EP-17: slug entfernt Satzzeichen und Formatierung", () => {
  assert.equal(slug("Was ist **das**? (Test)"), "was-ist-das-test");
  assert.ok(anchors("# Eins\n").has("eins"));
});
