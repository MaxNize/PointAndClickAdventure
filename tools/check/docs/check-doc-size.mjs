// EP-22: keine Markdown-Datei über der Zeilengrenze aus limits.json (docs.file_too_long).
import { finding, loadJson, readMarkdown, runIfMain } from "./lib.mjs";

export function findSizeProblems(files, maxLines) {
  const problems = [];
  for (const [file, text] of Object.entries(files)) {
    const lines = text.replace(/\n$/, "").split("\n").length;
    if (lines > maxLines) problems.push(finding("docs.file_too_long", file, 0, `${lines} Zeilen, erlaubt sind ${maxLines}`));
  }
  return problems;
}

export const check = (root) => findSizeProblems(readMarkdown(root), loadJson(root, "limits.json").maxMarkdownLines);
runIfMain(import.meta.url, check);
