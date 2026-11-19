// EP-17: relative Links und Anker in Markdown-Dateien müssen auflösbar sein (docs.link_broken).
import path from "node:path";
import { finding, readMarkdown, runIfMain, trackedFiles } from "./lib.mjs";

const LINK = /\[[^\]]*\]\(([^)\s]+)(?:\s+"[^"]*")?\)/g;
const SCHEME = /^(?:[a-z][a-z0-9+.-]*:|\/\/)/i;
const HEADING = /^#{1,6}\s+(.*?)\s*#*\s*$/;

// Zeilen mit Nummer, ohne Codeblöcke und ohne Inline-Code.
export function proseLines(text) {
  const out = [];
  let fenced = false;
  text.split("\n").forEach((line, i) => {
    if (/^\s*(```|~~~)/.test(line)) fenced = !fenced;
    else if (!fenced) out.push({ n: i + 1, text: line.replace(/`[^`]*`/g, "") });
  });
  return out;
}

export function slug(heading) {
  const plain = heading.replace(/\[([^\]]*)\]\([^)]*\)/g, "$1");
  return plain.trim().toLowerCase().replace(/[^\p{L}\p{N}\p{M}\s_-]/gu, "").replace(/\s/g, "-");
}

// Anker einer Datei nach der GitHub-Regel, doppelte Überschriften bekommen -1, -2, …
export function anchors(text) {
  const seen = new Map();
  const result = new Set();
  for (const { text: line } of proseLines(text)) {
    const m = line.match(HEADING);
    if (!m) continue;
    const base = slug(m[1]);
    const n = seen.get(base) ?? 0;
    seen.set(base, n + 1);
    result.add(n ? `${base}-${n}` : base);
  }
  return result;
}

function resolveTarget(file, rawPath) {
  const clean = decodeURI(rawPath).replace(/\/$/, "");
  return rawPath === "" ? file : path.posix.normalize(path.posix.join(path.posix.dirname(file), clean));
}

function exists(target, tracked) {
  return tracked.has(target) || [...tracked].some((f) => f.startsWith(`${target}/`));
}

function checkLink(file, n, href, files, tracked) {
  const [rawPath, rawAnchor] = href.split("#");
  const target = resolveTarget(file, rawPath);
  if (!exists(target, tracked)) return finding("docs.link_broken", file, n, `Ziel fehlt: ${href}`);
  if (!rawAnchor || !target.endsWith(".md") || !(target in files)) return null;
  const wanted = decodeURIComponent(rawAnchor).toLowerCase();
  return anchors(files[target]).has(wanted) ? null : finding("docs.link_broken", file, n, `Anker fehlt: ${href}`);
}

export function findLinkProblems(files, tracked) {
  const problems = [];
  for (const [file, text] of Object.entries(files))
    for (const { n, text: line } of proseLines(text))
      for (const m of line.matchAll(LINK)) {
        if (SCHEME.test(m[1])) continue;
        const p = checkLink(file, n, m[1], files, tracked);
        if (p) problems.push(p);
      }
  return problems;
}

export const check = (root) => findLinkProblems(readMarkdown(root), new Set(trackedFiles(root)));
runIfMain(import.meta.url, check);
