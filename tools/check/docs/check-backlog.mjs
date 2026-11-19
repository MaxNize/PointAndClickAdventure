// EP-21: jede Katalogzeile hat genau ein Issue mit unverändertem Wortlaut.
// docs.backlog_missing, docs.backlog_duplicate, docs.backlog_drift, docs.backlog_orphan.
// Braucht die GitHub-CLI `gh` mit Zugriff auf das Repo. Issues mit Label `prozess` sind ausgenommen.
import { execFileSync } from "node:child_process";
import { CATALOG, ID_PATTERN, catalogRows, finding, readMarkdown, runIfMain } from "./lib.mjs";

const TITLE_ID = new RegExp(`^(${ID_PATTERN})\\b`);
const norm = (s) => s.replace(/\r/g, "").replace(/\s+/g, " ").trim();

export function section(body, name) {
  const m = new RegExp(`^### ${name}\\s*\\n([\\s\\S]*?)(?=^### |^---\\s*$|(?![\\s\\S]))`, "m").exec(body.replace(/\r/g, ""));
  return m ? norm(m[1]) : "";
}

function compare(row, issue) {
  const [, , , anf, kri] = row.cells;
  const out = [];
  if (section(issue.body ?? "", "Anforderung") !== norm(anf)) out.push("Anforderung");
  if (section(issue.body ?? "", "Akzeptanzkriterium") !== norm(kri)) out.push("Akzeptanzkriterium");
  return out.length ? [finding("docs.backlog_drift", row.id, 0, `#${issue.number}: ${out.join(" und ")} weicht vom Katalog ab`)] : [];
}

export function findBacklogProblems(rows, issues) {
  const byId = new Map();
  for (const i of issues.filter((x) => !x.labels.includes("prozess"))) {
    const id = TITLE_ID.exec(i.title)?.[1];
    if (id) byId.set(id, [...(byId.get(id) ?? []), i]);
  }
  const problems = [];
  const catalog = new Set(rows.filter((r) => !r.struck).map((r) => r.id));
  for (const row of rows.filter((r) => !r.struck)) {
    const found = byId.get(row.id) ?? [];
    if (!found.length) problems.push(finding("docs.backlog_missing", row.id, 0, "kein Issue"));
    else if (found.length > 1) problems.push(finding("docs.backlog_duplicate", row.id, 0, `Issues ${found.map((i) => `#${i.number}`).join(", ")}`));
    else problems.push(...compare(row, found[0]));
  }
  for (const [id, list] of byId)
    if (!catalog.has(id)) problems.push(finding("docs.backlog_orphan", id, 0, `#${list[0].number} steht nicht im Katalog`));
  return problems;
}

export function fetchIssues(root) {
  const jq = ".[] | select(.pull_request | not) | {number, title, body, labels: [.labels[].name]}";
  const out = execFileSync("gh", ["api", "--paginate", "repos/{owner}/{repo}/issues?state=all&per_page=100", "--jq", jq], { cwd: root, encoding: "utf8", maxBuffer: 1 << 26 });
  return out.split("\n").filter(Boolean).map((l) => JSON.parse(l));
}

export function check(root) {
  let issues;
  try { issues = fetchIssues(root); } catch (e) { return [finding("docs.backlog_unavailable", "gh", 0, `Issues nicht lesbar: ${String(e.message).split("\n")[0]}`)]; }
  return findBacklogProblems(catalogRows(readMarkdown(root)[CATALOG] ?? ""), issues);
}
runIfMain(import.meta.url, check);
