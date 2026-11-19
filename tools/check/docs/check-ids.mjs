// EP-18: jede Katalog-ID genau einmal definiert (docs.id_duplicate).
// EP-19: jeder Verweis auf eine Projekt-ID zeigt auf eine definierte ID (docs.id_undefined).
import { CATALOG, ID_PATTERN, catalogRows, finding, readMarkdown, runIfMain } from "./lib.mjs";

export function findIdProblems(files) {
  const problems = [];
  const defined = new Map();
  for (const row of catalogRows(files[CATALOG] ?? "")) {
    if (defined.has(row.id)) problems.push(finding("docs.id_duplicate", CATALOG, row.line, `${row.id} auch in Zeile ${defined.get(row.id)}`));
    else defined.set(row.id, row.line);
  }
  const ref = new RegExp(`\\b${ID_PATTERN}\\b`, "g");
  for (const [file, text] of Object.entries(files))
    text.split("\n").forEach((line, i) => {
      for (const m of line.matchAll(ref))
        if (!defined.has(m[0])) problems.push(finding("docs.id_undefined", file, i + 1, `${m[0]} ist nicht definiert`));
    });
  return problems;
}

export const check = (root) => findIdProblems(readMarkdown(root));
runIfMain(import.meta.url, check);
