// Gate-Lauf (EP-01): führt alle Prüfungen der Reihe nach aus und bricht beim ersten Fehler ab.
// Aufruf über `make ci`, lokal und in der CI gleich. Neue Gates kommen als Eintrag in `steps()` dazu.
// Ein Fehler steht als `<regel> <datei> <meldung>` auf stderr, Exit-Code ungleich 0.
// `--steps <datei.json>` ersetzt die Schrittliste, nur für die Tests in run-ci.test.mjs.
import { spawnSync } from "node:child_process";
import fs from "node:fs";
import { pathToFileURL } from "node:url";
import { finding, format, repoRoot, trackedFiles } from "../check/docs/lib.mjs";

const NODE = process.execPath;

// Ein Schritt: `id` (Story oder Gate), `rule` (Fehlercode), `file` (geprüfte Datei),
// `cmd` (Programm und Argumente), optional `expect` (erwartete Ausgabe) und `hint`.
export function steps(root) {
  const tests = trackedFiles(root).filter((f) => f.endsWith(".test.mjs")).sort();
  return [
    {
      id: "EP-24 Hooks", rule: "ci.hooks_missing", file: ".githooks",
      cmd: ["git", "config", "core.hooksPath"], expect: ".githooks", hint: "`make setup` ausführen",
    },
    ...tests.map((file) => ({ id: "Test", rule: "ci.test_failed", file, cmd: [NODE, "--test", file] })),
    {
      id: "EP-17 bis EP-23 Doku-Gates", rule: "ci.step_failed", file: "tools/check/docs/run-all.mjs",
      cmd: [NODE, "tools/check/docs/run-all.mjs"],
    },
    {
      id: "E2E-Tests", rule: "ci.e2e_failed", file: "playwright.config.ts",
      cmd: [NODE, "node_modules/@playwright/test/cli.js", "test"], hint: "Browser fehlt? `make setup` ausführen",
    },
  ];
}

function exec(step, cwd) {
  const capture = step.expect !== undefined;
  const r = spawnSync(step.cmd[0], step.cmd.slice(1), {
    cwd, encoding: "utf8", stdio: capture ? ["ignore", "pipe", "inherit"] : "inherit",
  });
  return { status: r.error ? null : r.status, stdout: r.stdout ?? "", error: r.error };
}

// Führt die Schritte aus und gibt den Exit-Code zurück: 0, wenn alle grün sind.
export function runSteps(list, { cwd = repoRoot(), run = exec } = {}) {
  for (const step of list) {
    const r = run(step, cwd);
    let reason = null;
    const got = r.status === 0 ? r.stdout.trim() : "";
    if (r.error) reason = `nicht startbar (${r.error.code ?? r.error.message})`;
    else if (step.expect !== undefined && got !== step.expect) {
      reason = `erwartet „${step.expect}“, gefunden „${got || "nicht gesetzt"}“`;
    } else if (r.status !== 0) reason = `Exit-Code ${r.status}`;
    if (reason) {
      const hint = step.hint ? `. ${step.hint}` : "";
      console.error(format(finding(step.rule, step.file, 0, `${step.id}: ${reason}${hint}`)));
      console.error(`make ci: Abbruch bei ${step.id} (${step.file}).`);
      return Number.isInteger(r.status) && r.status !== 0 && step.expect === undefined ? r.status : 1;
    }
    console.log(`${step.id} ${step.file}: ok`);
  }
  console.log(`make ci: alle ${list.length} Schritte ok.`);
  return 0;
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  const i = process.argv.indexOf("--steps");
  const list = i > 0 ? JSON.parse(fs.readFileSync(process.argv[i + 1], "utf8")) : steps(repoRoot());
  process.exit(runSteps(list));
}
