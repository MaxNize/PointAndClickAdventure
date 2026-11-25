import test from "node:test";
import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { steps } from "./run-ci.mjs";
import { repoRoot, trackedFiles } from "../check/docs/lib.mjs";

const RUNNER = path.join(path.dirname(fileURLToPath(import.meta.url)), "run-ci.mjs");
const NODE = process.execPath;
const step = (file, code, extra = {}) => ({ id: `Schritt ${file}`, rule: "ci.step_failed", file, cmd: [NODE, "-e", code], ...extra });

// Startet die echte CLI mit Fixture-Schritten, nie mit der echten Liste (sonst Rekursion).
function runCli(list) {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), "run-ci-"));
  const file = path.join(dir, "steps.json");
  fs.writeFileSync(file, JSON.stringify(list));
  const r = spawnSync(NODE, [RUNNER, "--steps", file], { encoding: "utf8" });
  return { ...r, dir };
}

test("EP-01: alle Schritte grün ergibt Exit-Code 0", () => {
  const r = runCli([step("a.mjs", "process.exit(0)"), step("b.mjs", "process.exit(0)")]);
  assert.equal(r.status, 0, r.stderr);
  assert.match(r.stdout, /alle 2 Schritte ok/);
});

test("EP-01: erster Fehler bricht ab, spätere Schritte laufen nicht", () => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), "run-ci-marker-"));
  const marker = path.join(dir, "gelaufen");
  const r = runCli([
    step("a.mjs", "process.exit(0)"),
    step("b.mjs", "process.exit(3)"),
    step("c.mjs", `require("node:fs").writeFileSync(${JSON.stringify(marker)}, "x")`),
  ]);
  assert.equal(r.status, 3);
  assert.equal(fs.existsSync(marker), false, "Schritt nach dem Fehler darf nicht laufen");
});

test("EP-01: Fehlermeldung nennt Regel-ID und Datei", () => {
  const r = runCli([step("tools/x/check-y.mjs", "process.exit(1)", { rule: "ci.step_failed" })]);
  assert.notEqual(r.status, 0);
  assert.match(r.stderr, /^ci\.step_failed tools\/x\/check-y\.mjs /m);
});

test("EP-01: abweichende Ausgabe bei erwartetem Wert bricht mit Regel-ID und Hinweis ab", () => {
  const r = runCli([step(".githooks", "console.log('anders')", { rule: "ci.hooks_missing", expect: ".githooks", hint: "`make setup` ausführen" })]);
  assert.equal(r.status, 1);
  assert.match(r.stderr, /^ci\.hooks_missing \.githooks .*make setup/m);
});

test("EP-01: nicht startbarer Schritt bricht mit Regel-ID und Datei ab", () => {
  const r = runCli([{ id: "X", rule: "ci.step_failed", file: "fehlt.mjs", cmd: ["gibt-es-nicht-ep01"] }]);
  assert.equal(r.status, 1);
  assert.match(r.stderr, /^ci\.step_failed fehlt\.mjs X: nicht startbar/m);
});

test("EP-01: Schrittliste deckt Hooks, alle Testdateien und die Doku-Gates ab", () => {
  const root = repoRoot();
  const list = steps(root);
  const hooks = list.find((s) => s.rule === "ci.hooks_missing");
  assert.ok(hooks, "Hook-Prüfung (EP-24) fehlt");
  assert.equal(hooks.expect, ".githooks");
  const tests = trackedFiles(root).filter((f) => f.endsWith(".test.mjs"));
  assert.ok(tests.length > 0);
  for (const f of tests) assert.ok(list.some((s) => s.file === f && s.cmd.includes("--test")), `Test fehlt: ${f}`);
  assert.ok(list.some((s) => s.file === "tools/check/docs/run-all.mjs"), "Doku-Gates (EP-17 bis EP-23) fehlen");
});
