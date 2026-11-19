import test from "node:test";
import assert from "node:assert/strict";
import { findSizeProblems } from "./check-doc-size.mjs";

const lines = (n) => `${"zeile\n".repeat(n)}`;

test("EP-22: Datei genau an der Grenze ist ok", () => {
  assert.deepEqual(findSizeProblems({ "docs/a.md": lines(200) }, 200), []);
});
test("EP-22: Datei über der Grenze wird mit Zeilenzahl gemeldet", () => {
  const [p] = findSizeProblems({ "docs/a.md": lines(201), "docs/b.md": lines(5) }, 200);
  assert.equal(p.rule, "docs.file_too_long");
  assert.equal(p.file, "docs/a.md");
  assert.match(p.message, /201 Zeilen/);
});
