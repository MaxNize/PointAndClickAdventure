// EP-20: genannte Anzahlen von NF, FA und EP stimmen mit den Katalogzeilen überein (docs.count_mismatch).
// Fundstellen stehen in counts.config.json. Eine verschwundene Fundstelle ist ebenfalls ein Fund.
import { CATALOG, catalogRows, finding, loadJson, readMarkdown, runIfMain } from "./lib.mjs";

export function countRows(text) {
  const counts = {};
  const bump = (k) => (counts[k] = (counts[k] ?? 0) + 1);
  for (const { id, struck } of catalogRows(text)) {
    if (struck) continue;
    bump(id.split("-")[0]);
    if (id.startsWith("FA-")) bump(id.split("-").slice(0, 2).join("-"));
  }
  return counts;
}

const lineOf = (text, index) => text.slice(0, index).split("\n").length;

export function findCountProblems(files, config) {
  const counts = countRows(files[CATALOG] ?? "");
  const problems = [];
  for (const { file, pattern, group } of config.mentions) {
    const text = files[file] ?? "";
    const m = new RegExp(pattern).exec(text);
    if (!m) problems.push(finding("docs.count_mismatch", file, 0, `Fundstelle fehlt: /${pattern}/`));
    else if (Number(m[1]) !== (counts[group] ?? 0))
      problems.push(finding("docs.count_mismatch", file, lineOf(text, m.index), `${group}: Doku sagt ${m[1]}, Katalog hat ${counts[group] ?? 0}`));
  }
  return problems;
}

export const check = (root) => findCountProblems(readMarkdown(root), loadJson(root, "counts.config.json"));
runIfMain(import.meta.url, check);
