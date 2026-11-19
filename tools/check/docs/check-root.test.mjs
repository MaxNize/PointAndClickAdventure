import test from "node:test";
import assert from "node:assert/strict";
import { findRootProblems } from "./check-root.mjs";

const allow = { entries: ["README.md", "docs", "tsconfig*.json", "vite.config.*", ".github"] };

test("EP-23: erlaubte Einträge und Platzhalter sind ok", () => {
  const tracked = ["README.md", "docs/a/b.md", "tsconfig.json", "tsconfig.node.json", "vite.config.ts", ".github/x.yml"];
  assert.deepEqual(findRootProblems(tracked, allow), []);
});
test("EP-23: nicht erlaubter Eintrag wird gemeldet, auch als Ordner", () => {
  const problems = findRootProblems(["README.md", "notizen.txt", "tmp/a.txt", "tmp/b.txt"], allow);
  assert.deepEqual(problems.map((p) => p.file), ["notizen.txt", "tmp"]);
  assert.equal(problems[0].rule, "docs.root_unexpected");
});
test("EP-23: Platzhalter erlaubt keinen Eintrag mit anderem Präfix", () => {
  assert.equal(findRootProblems(["xtsconfig.json"], allow).length, 1);
});
