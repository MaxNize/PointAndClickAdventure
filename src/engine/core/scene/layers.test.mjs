// Tests der Ebenenreihenfolge eines Raums (FA-E-01).
import test from "node:test";
import assert from "node:assert/strict";
import { roomLayerOrder } from "./layers.ts";

const room = (layers) => ({ layers });
const F = "content/rooms/r/room.svg";

test("FA-E-01: Ebenen in der Reihenfolge Hintergrund, Hotspots, Mittelebenen nach Basislinie, Vordergrund", () => {
  const ids = ["layer-foreground", "layer-mid-b", "hotspots", "layer-mid-a", "layer-background"];
  const r = roomLayerOrder(ids, room({ "layer-mid-a": { baseline: 900 }, "layer-mid-b": { baseline: 700 } }), F);
  assert.deepEqual(r.errors, []);
  assert.deepEqual(r.order, ["layer-background", "hotspots", "layer-mid-b", "layer-mid-a", "layer-foreground"]);
});

test("FA-E-01: nur vorhandene Ebenen erscheinen, Hintergrund allein genügt", () => {
  assert.deepEqual(roomLayerOrder(["layer-background"], room(undefined), F), { order: ["layer-background"], errors: [] });
});

test("FA-E-01: fehlender Hintergrund meldet room.layer-missing", () => {
  assert.deepEqual(roomLayerOrder(["layer-foreground"], room(undefined), F).errors.map((e) => e.code), ["room.layer-missing"]);
});

test("FA-E-01: unbekannte oder namenlose oberste Gruppe meldet room.unknown-layer", () => {
  const r = roomLayerOrder(["layer-background", "deko", null], room(undefined), F);
  assert.deepEqual(r.errors.map((e) => e.code), ["room.unknown-layer", "room.unknown-layer"]);
  assert.deepEqual(r.order, ["layer-background"]);
});

test("FA-E-01: Mittelebene ohne Basislinie und Basislinie ohne Ebene melden room.layer-unmapped", () => {
  const r = roomLayerOrder(["layer-background", "layer-mid-a"], room({ "layer-mid-x": { baseline: 1 } }), F);
  assert.deepEqual(r.errors.map((e) => e.message), [
    "„layer-mid-a“ hat keine Basislinie in room.json",
    "Basislinie für „layer-mid-x“, aber keine Gruppe im SVG",
  ]);
});
