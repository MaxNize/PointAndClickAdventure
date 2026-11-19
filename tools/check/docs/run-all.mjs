// Führt alle Doku-Gates der Reihe nach aus und bricht beim ersten Fund ab.
// `--offline` lässt den Backlog-Abgleich (EP-21) aus, weil er das Netz braucht.
import { format, repoRoot } from "./lib.mjs";

const GATES = [
  ["EP-17", "./check-links.mjs"],
  ["EP-18/19", "./check-ids.mjs"],
  ["EP-20", "./check-counts.mjs"],
  ["EP-22", "./check-doc-size.mjs"],
  ["EP-23", "./check-root.mjs"],
  ["EP-21", "./check-backlog.mjs"],
];
const offline = process.argv.includes("--offline");

for (const [name, file] of GATES) {
  if (offline && file.includes("backlog")) { console.log(`${name}: übersprungen (--offline)`); continue; }
  const { check } = await import(file);
  const findings = check(repoRoot());
  if (findings.length) {
    findings.forEach((f) => console.error(format(f)));
    console.error(`${name}: ${findings.length} Fund(e). Abbruch.`);
    process.exit(1);
  }
  console.log(`${name}: ok`);
}
