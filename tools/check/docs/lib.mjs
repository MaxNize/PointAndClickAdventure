// Gemeinsame Helfer der Doku-Gates (EP-17 bis EP-23). Reines Node, keine Pakete.
import { execFileSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

export const CATALOG = "docs/voranalyse/03-anforderungen.md";
export const ID_PATTERN = "(?:FA-(?:E|G|DEV)|NF-[AVEW]|EP)-\\d{2}";
const ROW = new RegExp(`^\\| (${ID_PATTERN}) \\|`);

export const repoRoot = () => path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../../..");

export function trackedFiles(root) {
  const out = execFileSync("git", ["ls-files", "-z"], { cwd: root, encoding: "utf8" });
  return out.split("\0").filter((f) => f && fs.existsSync(path.join(root, f)));
}

export function readMarkdown(root) {
  const files = {};
  for (const f of trackedFiles(root)) if (f.endsWith(".md")) files[f] = fs.readFileSync(path.join(root, f), "utf8");
  return files;
}

export const finding = (rule, file, line, message) => ({ rule, file, line, message });
export const format = (f) => `${f.rule} ${f.file}${f.line ? `:${f.line}` : ""} ${f.message}`;

// Katalogzeilen: ID, Zeilennummer, Zellen. Als „gestrichen“ markierte Zeilen zählen nicht.
export function catalogRows(text) {
  const rows = [];
  text.split("\n").forEach((line, i) => {
    const m = line.match(ROW);
    if (!m) return;
    const cells = line.trim().replace(/^\|\s*/, "").replace(/\s*\|$/, "").split(" | ");
    rows.push({ id: m[1], line: i + 1, cells, struck: /gestrichen/i.test(line) });
  });
  return rows;
}

// Startet eine Prüfung, wenn die Datei direkt aufgerufen wird. Exit-Code 1 bei Funden.
export function runIfMain(metaUrl, check) {
  if (!process.argv[1] || metaUrl !== pathToFileURL(process.argv[1]).href) return;
  const findings = check(repoRoot());
  for (const f of findings) console.error(format(f));
  process.exit(findings.length ? 1 : 0);
}

export function loadJson(root, name) {
  return JSON.parse(fs.readFileSync(path.join(root, "tools/check/docs", name), "utf8"));
}
