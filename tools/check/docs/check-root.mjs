// EP-23: im Repo-Root stehen nur Einträge aus root-allowlist.json (docs.root_unexpected).
import { finding, loadJson, runIfMain, trackedFiles } from "./lib.mjs";

const toRegExp = (entry) => new RegExp(`^${entry.replace(/[.+^${}()|[\]\\]/g, "\\$&").replace(/\*/g, ".*")}$`);

export function findRootProblems(tracked, allowlist) {
  const allowed = allowlist.entries.map(toRegExp);
  const roots = new Set(tracked.map((f) => f.split("/")[0]));
  return [...roots].filter((r) => !allowed.some((re) => re.test(r))).sort()
    .map((r) => finding("docs.root_unexpected", r, 0, "Eintrag steht nicht in root-allowlist.json"));
}

export const check = (root) => findRootProblems(trackedFiles(root), loadJson(root, "root-allowlist.json"));
runIfMain(import.meta.url, check);
