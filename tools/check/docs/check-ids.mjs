// EP-18: jede Katalog-ID genau einmal definiert (docs.id_duplicate).
// EP-19: jeder Verweis auf eine Projekt-ID zeigt auf eine definierte ID (docs.id_undefined).
// Ausnahme: vorläufige IDs in ids.baseline.json. Die Baseline darf nur schrumpfen:
// eine definierte oder nirgends mehr verwiesene ID in der Baseline ist ein Fund (docs.id_baseline_stale).
import { CATALOG, ID_PATTERN, catalogRows, finding, loadJson, readMarkdown, runIfMain } from "./lib.mjs";

const BASELINE = "tools/check/docs/ids.baseline.json";

function definitions(text) {
  const problems = [];
  const defined = new Map();
  for (const row of catalogRows(text)) {
    if (defined.has(row.id)) problems.push(finding("docs.id_duplicate", CATALOG, row.line, `${row.id} auch in Zeile ${defined.get(row.id)}`));
    else defined.set(row.id, row.line);
  }
  return { defined, problems };
}

function staleEntries(baseline, defined, used) {
  const problems = [];
  for (const id of baseline) {
    if (defined.has(id)) problems.push(finding("docs.id_baseline_stale", BASELINE, 0, `${id} ist jetzt im Katalog definiert, aus der Baseline entfernen`));
    else if (!used.has(id)) problems.push(finding("docs.id_baseline_stale", BASELINE, 0, `${id} wird nirgends mehr verwiesen, aus der Baseline entfernen`));
  }
  return problems;
}

export function findIdProblems(files, baseline = []) {
  const { defined, problems } = definitions(files[CATALOG] ?? "");
  const allowed = new Set(baseline);
  const used = new Set();
  const ref = new RegExp(`\\b${ID_PATTERN}\\b`, "g");
  for (const [file, text] of Object.entries(files))
    text.split("\n").forEach((line, i) => {
      for (const m of line.matchAll(ref)) {
        if (defined.has(m[0])) continue;
        if (allowed.has(m[0])) used.add(m[0]);
        else problems.push(finding("docs.id_undefined", file, i + 1, `${m[0]} ist nicht definiert`));
      }
    });
  return [...problems, ...staleEntries(baseline, defined, used)];
}

export const check = (root) => findIdProblems(readMarkdown(root), loadJson(root, "ids.baseline.json").provisional);
runIfMain(import.meta.url, check);
