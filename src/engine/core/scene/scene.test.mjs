// Tests der Szene: FA-E-10 Tiefenskalierung, FA-E-02 Zeichenreihenfolge, FA-E-03/FA-E-04 Akteure.
import test from "node:test";
import assert from "node:assert/strict";
import { sceneActors } from "./actors.ts";
import { depthScale } from "./depth.ts";
import { drawOrder } from "./drawOrder.ts";
import { evalCondition, initialState } from "../state/conditions.ts";

const depth = { far: { y: 700, scale: 0.6 }, near: { y: 1060, scale: 1.0 } };
const within1Percent = (actual, expected) => assert.ok(Math.abs(actual - expected) <= 0.01 * expected, `${actual} statt ${expected}`);

test("FA-E-10: Skalierung am oberen und unteren Rand der begehbaren Fläche höchstens 1 % vom Sollwert", () => {
  within1Percent(depthScale(700, depth), 0.6);
  within1Percent(depthScale(1060, depth), 1.0);
});

test("FA-E-10: Skalierung dazwischen linear, außerhalb geklemmt", () => {
  within1Percent(depthScale(880, depth), 0.8);
  assert.equal(depthScale(100, depth), 0.6);
  assert.equal(depthScale(2000, depth), 1.0);
});

const actor = (key, baseline) => ({ key, kind: "character", ref: key, x: 0, y: baseline, facing: "front", baseline });
const names = (entries) => entries.map((e) => ("layer" in e ? e.layer : e.actor.key));

test("FA-E-02: Zeichenreihenfolge im Testraum aufsteigend nach Basislinie", () => {
  const room = { layers: { "layer-mid-block": { baseline: 900 }, "layer-mid-saeule": { baseline: 750 } } };
  const layers = ["layer-background", "hotspots", "layer-mid-saeule", "layer-mid-block", "layer-foreground"];
  const order = drawOrder(layers, room, [actor("vorn", 980), actor("kugel", 800), actor("player", 950)]);
  assert.deepEqual(names(order), [
    "layer-background", "hotspots", "layer-mid-saeule", "kugel", "layer-mid-block", "player", "vorn", "layer-foreground",
  ]);
});

test("FA-E-02: bei gleicher Basislinie liegt der Akteur vor der Ebene", () => {
  const order = drawOrder(["layer-background", "layer-mid-a"], { layers: { "layer-mid-a": { baseline: 900 } } }, [actor("a", 900)]);
  assert.deepEqual(names(order), ["layer-background", "layer-mid-a", "a"]);
});

function content(roomPatch = {}) {
  const look = { look: [{ type: "say", text: "x" }] };
  const def = {
    id: "r", depth, spawns: { start: { x: 300, y: 950, facing: "right" } },
    characters: [
      { character: "b", x: 1, y: 2, facing: "left", walkTo: { x: 1, y: 2 }, verbs: look },
      { character: "c", x: 1, y: 2, facing: "front", walkTo: { x: 1, y: 2 }, visibleIf: { flag: "nie" }, verbs: look },
    ],
    items: [{ item: "kugel", x: 5, y: 6, walkTo: { x: 5, y: 6 } }],
    ...roomPatch,
  };
  return {
    game: { player: "a" },
    rooms: new Map([["r", { def, svg: "", file: "content/rooms/r/room.json" }]]),
    characters: new Map(["a", "b", "c"].map((id) => [id, { def: { id } }])),
    items: new Map([["kugel", { worldSvg: "", file: "" }]]),
  };
}

test("FA-E-03: Spielfigur steht am Startspawn mit dessen Blickrichtung", () => {
  const { actors } = sceneActors(content(), "r", "start", initialState());
  assert.deepEqual(actors.find((a) => a.key === "player"), {
    key: "player", kind: "character", ref: "a", x: 300, y: 950, facing: "right", baseline: 950,
  });
});

test("FA-E-04: sichtbare Akteure an ihrer Position, nicht erfüllte visibleIf-Bedingung: 0 angezeigt", () => {
  const { actors, errors } = sceneActors(content(), "r", "start", initialState());
  assert.deepEqual(errors, []);
  assert.deepEqual(actors.map((a) => `${a.key} ${a.x},${a.y}`), ["player 300,950", "figur-b 1,2", "gegenstand-kugel 5,6"]);
});

test("FA-E-04: aufgenommener Gegenstand und erfüllte Bedingung ändern die Akteure", () => {
  const state = { flags: new Set(["nie", "item.r.kugel.taken"]), inventory: new Map() };
  assert.deepEqual(sceneActors(content(), "r", "start", state).actors.map((a) => a.key), ["player", "figur-b", "figur-c"]);
});

test("FA-E-04: fehlende Figur oder fehlendes world.svg werden gemeldet statt angezeigt", () => {
  const c = content({ characters: [{ character: "x", x: 1, y: 2, facing: "left", walkTo: { x: 1, y: 2 }, verbs: {} }], items: [{ item: "y", x: 1, y: 1, walkTo: { x: 1, y: 1 } }] });
  const { actors, errors } = sceneActors(c, "r", "start", initialState());
  assert.deepEqual(actors.map((a) => a.key), ["player"]);
  assert.deepEqual(errors.map((e) => e.code), ["content.ref-missing", "item.world-missing"]);
});

test("FA-E-04: Bedingungen werten Flags, Inventar und Verknüpfungen aus", () => {
  const s = { flags: new Set(["a"]), inventory: new Map([["kugel", 1], ["leer", 0]]) };
  assert.equal(evalCondition({ flag: "a" }, s), true);
  assert.equal(evalCondition({ hasItem: "kugel" }, s), true);
  assert.equal(evalCondition({ hasItem: "leer" }, s), false);
  assert.equal(evalCondition({ all: [{ flag: "a" }, { not: { flag: "b" } }] }, s), true);
  assert.equal(evalCondition({ any: [{ flag: "b" }, { hasItem: "leer" }] }, s), false);
});
