// EP-24: ordnet jedes geschlossene Ticket dem Sprint zu, in dem es geschlossen wurde.
// Das Schließdatum entscheidet (nicht der Zeitpunkt des Laufs). Ein zweiter Lauf ändert nichts.
//   node tools/project/sync-sprint.mjs [--check | --dry-run] [--best-effort]
//   --check        meldet falsch zugeordnete Tickets (project.sprint_mismatch), Exit-Code 1 bei Funden
//   --dry-run      zeigt, was verschoben würde
//   --best-effort  für den Hook: jeder Fehler wird zur Warnung, Exit-Code immer 0
import { execFileSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
export const loadConfig = () => JSON.parse(fs.readFileSync(path.join(here, "sprint-sync.config.json"), "utf8"));

export function berlinDate(iso, timeZone) {
  return new Intl.DateTimeFormat("en-CA", { timeZone, year: "numeric", month: "2-digit", day: "2-digit" }).format(new Date(iso));
}

const addDays = (date, n) => new Date(Date.parse(`${date}T00:00:00Z`) + n * 864e5).toISOString().slice(0, 10);

// Ein Sprint gilt von startDate (einschließlich) bis startDate + duration (ausschließlich).
export function sprintOn(date, iterations) {
  return iterations.find((i) => i.startDate <= date && date < addDays(i.startDate, i.duration));
}

export function planMoves(items, iterations, timeZone) {
  const moves = [];
  for (const it of items) {
    if (!it.number || !it.closedAt || it.stateReason === "NOT_PLANNED") continue;
    const target = sprintOn(berlinDate(it.closedAt, timeZone), iterations);
    if (target && target.id !== it.sprintId) moves.push({ ...it, to: target });
  }
  return moves;
}

export function syncSprint({ load, apply, mode = "apply", log = console.log }) {
  const { iterations, items, timeZone } = load();
  const moves = planMoves(items, iterations, timeZone);
  for (const m of moves) {
    const text = `#${m.number} ${m.title}: ${m.to.title} statt ${m.sprintTitle ?? "kein Sprint"}`;
    if (mode === "check") log(`project.sprint_mismatch ${text}`);
    else if (mode === "dry-run") log(`würde verschieben: ${text}`);
    else { apply(m); log(`verschoben: ${text}`); }
  }
  return mode === "check" && moves.length ? 1 : 0;
}

// --- GitHub-Zugriff über `gh` (nur in main, von den Tests nicht benutzt) ---
const ITEMS = `query($p:ID!,$a:String){node(id:$p){... on ProjectV2{items(first:100,after:$a){pageInfo{hasNextPage endCursor} nodes{id
  sprint:fieldValueByName(name:"Sprint"){... on ProjectV2ItemFieldIterationValue{iterationId title}}
  content{... on Issue{number title closedAt stateReason}}}}}}}`;
const PROJECT = `query($o:String!,$n:Int!){user(login:$o){projectV2(number:$n){id field(name:"Sprint"){... on ProjectV2IterationField{id
  configuration{iterations{id title startDate duration} completedIterations{id title startDate duration}}}}}}}`;
const MOVE = `mutation($p:ID!,$i:ID!,$f:ID!,$v:String!){updateProjectV2ItemFieldValue(input:{projectId:$p,itemId:$i,fieldId:$f,value:{iterationId:$v}}){projectV2Item{id}}}`;

export function ghLoader(cfg, run = (args) => execFileSync("gh", args, { encoding: "utf8", timeout: cfg.timeoutMs, stdio: ["ignore", "pipe", "pipe"] })) {
  const gql = (query, vars) => JSON.parse(run(["api", "graphql", "-f", `query=${query}`, ...Object.entries(vars).flatMap(([k, v]) => [typeof v === "number" ? "-F" : "-f", `${k}=${v}`])])).data;
  const p = gql(PROJECT, { o: cfg.owner, n: cfg.project }).user.projectV2;
  const conf = p.field.configuration;
  const state = { projectId: p.id, fieldId: p.field.id };
  const load = () => {
    const items = [];
    for (let after = ""; ; ) {
      const page = gql(ITEMS, { p: p.id, a: after }).node.items;
      for (const n of page.nodes) items.push({ ...n.content, itemId: n.id, sprintId: n.sprint?.iterationId, sprintTitle: n.sprint?.title });
      if (!page.pageInfo.hasNextPage) break;
      after = page.pageInfo.endCursor;
    }
    return { items, iterations: [...conf.iterations, ...conf.completedIterations], timeZone: cfg.timeZone };
  };
  const apply = (m) => gql(MOVE, { p: state.projectId, i: m.itemId, f: state.fieldId, v: m.to.id });
  return { load, apply };
}

export function main(argv, deps = {}) {
  const mode = argv.includes("--check") ? "check" : argv.includes("--dry-run") ? "dry-run" : "apply";
  const bestEffort = argv.includes("--best-effort");
  try {
    const cfg = loadConfig();
    const { load, apply } = (deps.loader ?? ghLoader)(cfg);
    return syncSprint({ load, apply, mode, log: deps.log });
  } catch (e) {
    if (!bestEffort) throw e;
    const detail = String(e.stderr || e.message).trim().split("\n")[0].slice(0, 120);
    console.error(`Sprint-Zuordnung übersprungen: ${detail}`);
    return 0;
  }
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) process.exit(main(process.argv.slice(2)));
