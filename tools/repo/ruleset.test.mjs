// Prüft das versionierte Ruleset für `main` (.github/rulesets/main.json), ohne Netz.
// Ob GitHub es wirklich anwendet, zeigt `gh api repos/<owner>/<repo>/rules/branches/main`.
import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..");
const ruleset = JSON.parse(fs.readFileSync(path.join(root, ".github/rulesets/main.json"), "utf8"));
const rule = (type) => ruleset.rules.find((r) => r.type === type);

test("EP-03: Ruleset verlangt 1 Approval vor dem Merge in main", () => {
  assert.equal(ruleset.target, "branch");
  assert.equal(ruleset.enforcement, "active");
  assert.ok(ruleset.conditions.ref_name.include.includes("~DEFAULT_BRANCH"));
  assert.deepEqual(ruleset.conditions.ref_name.exclude, []);
  const pr = rule("pull_request");
  assert.ok(pr, "Regel pull_request fehlt");
  assert.ok(pr.parameters.required_approving_review_count >= 1);
});

test("EP-03: nach einem neuen Push muss eine andere Person freigeben", () => {
  const { parameters } = rule("pull_request");
  assert.equal(parameters.require_last_push_approval, true);
  assert.equal(parameters.dismiss_stale_reviews_on_push, true);
});

test("EP-04: Ruleset lehnt Force-Pushes auf main ab", () => {
  assert.ok(rule("non_fast_forward"), "Regel non_fast_forward fehlt");
});

test("EP-03, EP-04: niemand darf das Ruleset umgehen", () => {
  assert.deepEqual(ruleset.bypass_actors, []);
});
