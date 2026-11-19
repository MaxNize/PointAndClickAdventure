import test from "node:test";
import assert from "node:assert/strict";
import { berlinDate, ghLoader, main, planMoves, sprintOn, syncSprint } from "./sync-sprint.mjs";

const TZ = "Europe/Berlin";
const S1 = { id: "i1", title: "Sprint 1", startDate: "2026-11-19", duration: 7 };
const S2 = { id: "i2", title: "Sprint 2", startDate: "2026-11-26", duration: 7 };
const S3 = { id: "i3", title: "Sprint 3", startDate: "2026-12-03", duration: 14 };
const iterations = [S1, S2, S3];
const item = (n, closedAt, sprint, extra = {}) => ({ itemId: `it${n}`, number: n, title: `T${n}`, closedAt, sprintId: sprint?.id, sprintTitle: sprint?.title, ...extra });
const moves = (items) => planMoves(items, iterations, TZ).map((m) => `#${m.number}->${m.to.title}`);

test("EP-24: Ticket ohne Sprint erhält den Sprint, in dem es geschlossen wurde", () => {
  assert.deepEqual(moves([item(1, "2026-11-20T10:00:00Z")]), ["#1->Sprint 1"]);
});
test("EP-24: Ticket aus einem späteren Sprint wandert in den Sprint des Schließens", () => {
  assert.deepEqual(moves([item(2, "2026-11-21T10:00:00Z", S3)]), ["#2->Sprint 1"]);
});
test("EP-24: Ticket aus einem früheren Sprint wandert in den Sprint des Schließens", () => {
  assert.deepEqual(moves([item(3, "2026-11-28T10:00:00Z", S1)]), ["#3->Sprint 2"]);
});
test("EP-24: richtig zugeordnetes Ticket bleibt unverändert", () => {
  assert.deepEqual(moves([item(4, "2026-11-20T10:00:00Z", S1)]), []);
});
test("EP-24: ein zweiter Lauf ändert 0 Tickets", () => {
  const items = [item(1, "2026-11-20T10:00:00Z"), item(2, "2026-11-28T10:00:00Z", S1)];
  const applied = [];
  const run = () => syncSprint({ load: () => ({ items, iterations, timeZone: TZ }), apply: (m) => { applied.push(m.number); items.find((i) => i.number === m.number).sprintId = m.to.id; }, log: () => {} });
  run(); run();
  assert.deepEqual(applied, [1, 2]);
});
test("EP-24: Sprint-Grenzen: Start gilt, Ende nicht", () => {
  assert.equal(sprintOn("2026-11-26", iterations).title, "Sprint 2");
  assert.equal(sprintOn("2026-11-25", iterations).title, "Sprint 1");
  assert.equal(sprintOn("2026-11-18", iterations), undefined);
  assert.equal(sprintOn("2026-12-17", iterations), undefined);
});
test("EP-24: das Datum zählt in deutscher Zeit", () => {
  assert.equal(berlinDate("2026-11-25T23:30:00Z", TZ), "2026-11-26");
  assert.deepEqual(moves([item(5, "2026-11-25T23:30:00Z", S1)]), ["#5->Sprint 2"]);
});
test("EP-24: offene, wieder geöffnete, nicht geplante und außerhalb liegende Tickets werden übersprungen", () => {
  const skipped = [item(6, null), item(7, "2026-11-20T10:00:00Z", undefined, { stateReason: "NOT_PLANNED" }), item(8, "2026-11-01T10:00:00Z"), item(9, "2027-05-01T10:00:00Z"), { closedAt: "2026-11-20T10:00:00Z" }];
  assert.deepEqual(moves(skipped), []);
});
test("EP-24: --check meldet falsch zugeordnete Tickets mit Code und Nummer, Exit-Code 1", () => {
  const out = [];
  const code = syncSprint({ load: () => ({ items: [item(10, "2026-11-20T10:00:00Z", S3)], iterations, timeZone: TZ }), apply: () => assert.fail(), mode: "check", log: (l) => out.push(l) });
  assert.equal(code, 1);
  assert.match(out[0], /^project\.sprint_mismatch #10 T10: Sprint 1 statt Sprint 3/);
});
test("EP-24: --check ohne Funde endet mit Exit-Code 0, --dry-run ändert nichts", () => {
  const ok = { load: () => ({ items: [item(11, "2026-11-20T10:00:00Z", S1)], iterations, timeZone: TZ }), apply: () => assert.fail(), log: () => {} };
  assert.equal(syncSprint({ ...ok, mode: "check" }), 0);
  const dry = { ...ok, load: () => ({ items: [item(12, "2026-11-20T10:00:00Z")], iterations, timeZone: TZ }) };
  assert.equal(syncSprint({ ...dry, mode: "dry-run" }), 0);
});
test("EP-24: --best-effort macht aus jedem Fehler eine Warnung mit Exit-Code 0", () => {
  const warnings = [];
  const orig = console.error;
  console.error = (m) => warnings.push(m);
  try {
    const failing = () => { throw new Error("Netz weg\nzweite Zeile"); };
    assert.equal(main(["--best-effort"], { loader: failing }), 0);
    assert.throws(() => main([], { loader: failing }), /Netz weg/);
  } finally { console.error = orig; }
  assert.match(warnings[0], /übersprungen: Netz weg$/);
});
test("EP-24: abgeschlossene Sprints werden aus completedIterations mitgelesen", () => {
  const calls = [];
  const reply = (q) => (q.includes("ProjectV2IterationField")
    ? { data: { user: { projectV2: { id: "P", field: { id: "F", configuration: { iterations: [S2], completedIterations: [S1] } } } } } }
    : { data: { node: { items: { pageInfo: { hasNextPage: false }, nodes: [] } } } });
  const { load } = ghLoader({ owner: "o", project: 1, timeZone: TZ, timeoutMs: 1 }, (args) => { calls.push(args); return JSON.stringify(reply(args.find((a) => a.startsWith("query=")))); });
  assert.deepEqual(load().iterations.map((i) => i.title), ["Sprint 2", "Sprint 1"]);
  assert.ok(calls[0].includes("-F") && calls[0].includes("n=1"), "Zahl wird mit -F übergeben");
  assert.ok(calls[0].includes("-f") && calls[0].includes("o=o"), "Text wird mit -f übergeben");
});
