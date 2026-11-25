// Tests zum Projektgerüst (EP-16): `npm run build` und `npm run dev` enden bzw. starten fehlerfrei.
// Voraussetzung: Abhängigkeiten sind installiert (`make setup` führt `npm ci` aus). In der CI ist das ein frischer Klon.
import test from "node:test";
import assert from "node:assert/strict";
import { spawn, spawnSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import { repoRoot } from "../check/docs/lib.mjs";

const ROOT = repoRoot();
const WIN = process.platform === "win32";
const ENV = { ...process.env, NO_COLOR: "1", FORCE_COLOR: "0" };
const START_TIMEOUT_MS = 60_000;

// npm ist unter Windows eine .cmd-Datei und braucht dort eine Shell. Die Argumente sind fest im Test,
// deshalb als eine Befehlszeile (vermeidet DEP0190).
const npmCmd = (args) => (WIN ? [`npm ${args.join(" ")}`, []] : ["npm", args]);
const OPTS = { cwd: ROOT, env: ENV, shell: WIN };
const npm = (args) => spawn(...npmCmd(args), { ...OPTS, detached: !WIN });

function killTree(child) {
  if (child.exitCode !== null) return;
  if (WIN) spawnSync("taskkill", ["/pid", String(child.pid), "/T", "/F"], { stdio: "ignore" });
  else process.kill(-child.pid, "SIGTERM");
}

// Wartet, bis der Dev-Server seine lokale Adresse meldet, und gibt sie zurück.
function waitForUrl(child) {
  return new Promise((resolve, reject) => {
    let out = "";
    const timer = setTimeout(() => reject(new Error(`Dev-Server meldet keine Adresse:\n${out}`)), START_TIMEOUT_MS);
    const onData = (chunk) => {
      out += chunk;
      const m = out.match(/Local:\s+(http:\/\/\S+)/);
      if (m) { clearTimeout(timer); resolve(m[1]); }
    };
    child.stdout.on("data", onData);
    child.stderr.on("data", onData);
    child.on("exit", (code) => { clearTimeout(timer); reject(new Error(`Dev-Server beendet (Exit-Code ${code}):\n${out}`)); });
  });
}

test("EP-16: Abhängigkeiten sind installiert", () => {
  assert.ok(fs.existsSync(path.join(ROOT, "node_modules", ".package-lock.json")), "node_modules fehlt: `make setup` ausführen");
});

test("EP-16: npm run build endet mit Exit-Code 0 und erzeugt dist/index.html", { timeout: 180_000 }, () => {
  const r = spawnSync(...npmCmd(["run", "build"]), { ...OPTS, encoding: "utf8" });
  assert.equal(r.status, 0, `${r.stdout}\n${r.stderr}`);
  assert.ok(fs.existsSync(path.join(ROOT, "dist", "index.html")), "dist/index.html fehlt");
});

test("EP-16: npm run dev startet und liefert die Startseite aus", { timeout: 120_000 }, async () => {
  const child = npm(["run", "dev", "--", "--host", "127.0.0.1"]);
  child.stdout.setEncoding("utf8");
  child.stderr.setEncoding("utf8");
  try {
    const url = await waitForUrl(child);
    const res = await fetch(url);
    assert.equal(res.status, 200);
    assert.match(await res.text(), /<div id="root"><\/div>/);
  } finally {
    killTree(child);
  }
});
