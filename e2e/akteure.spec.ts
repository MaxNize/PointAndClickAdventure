// Akteure im Testraum: FA-E-02 Zeichenreihenfolge, FA-E-03 Spielstart, FA-E-04 Platzierung.
import { expect, test, type Page } from "@playwright/test";

/** Mitte des aktiven Ankers eines Akteurs in Raumeinheiten (viewBox des Raums). */
async function anchorOf(page: Page, actor: string) {
  return page.locator(`svg[data-room] > g[data-actor="${actor}"] [data-active-anchor]`).evaluate((a) => {
    const room = a.closest("svg[data-room]") as SVGSVGElement;
    const r = a.getBoundingClientRect();
    const p = new DOMPoint(r.x + r.width / 2, r.y + r.height / 2).matrixTransform(room.getScreenCTM()!.inverse());
    return { x: p.x, y: p.y };
  });
}

const distance = (a: { x: number; y: number }, b: { x: number; y: number }) => Math.hypot(a.x - b.x, a.y - b.y);

test.beforeEach(async ({ page }) => {
  await page.goto("/");
  await expect(page.locator('svg[data-room="testraum"] > g[data-actor="player"]')).toBeAttached();
});

test("FA-E-03: nach dem Start ist startRoom aktiv und die Spielfigur steht am Spawn startSpawn", async ({ page }) => {
  await expect(page.locator("svg[data-room]")).toHaveAttribute("data-room", "testraum");
  expect(distance(await anchorOf(page, "player"), { x: 300, y: 950 })).toBeLessThanOrEqual(2);
});

test("FA-E-04: Anker jedes Akteurs höchstens 2 Einheiten von seiner Position", async ({ page }) => {
  const positions = { player: { x: 300, y: 950 }, "figur-figur-b": { x: 1400, y: 980 }, "gegenstand-kugel": { x: 1200, y: 800 } };
  const shown = await page.locator("svg[data-room] > g[data-actor]").evaluateAll((gs) => gs.map((g) => g.getAttribute("data-actor")));
  expect(shown.sort()).toEqual(Object.keys(positions).sort());
  for (const [actor, pos] of Object.entries(positions))
    expect(distance(await anchorOf(page, actor), pos), actor).toBeLessThanOrEqual(2);
});

test("FA-E-04: Akteure mit nicht erfüllter visibleIf-Bedingung werden nicht angezeigt", async ({ page }) => {
  await expect(page.locator('[data-character="figur-c"]')).toHaveCount(0);
});

test("FA-E-02: Figur mit Fußpunkt unter der Basislinie einer Mittelebene liegt im DOM nach dieser Ebene", async ({ page }) => {
  const order = await page.locator("svg[data-room] > g").evaluateAll((gs) => gs.map((g) => g.id || g.getAttribute("data-actor")));
  expect(order).toEqual([
    "layer-background", "hotspots",
    "layer-mid-saeule", // Basislinie 750
    "gegenstand-kugel", // y 800
    "layer-mid-block", // Basislinie 900
    "player", // y 950
    "figur-figur-b", // y 980
    "layer-foreground",
  ]);
});

test("FA-E-04: Figur mit Blickrichtung links zeigt die gespiegelte Seitenansicht", async ({ page }) => {
  const b = page.locator('g[data-actor="figur-figur-b"]');
  await expect(b.locator('[id="figur-figur-b--view-side"]')).toBeVisible();
  await expect(b.locator('[id="figur-figur-b--view-front"]')).toBeHidden();
  expect(await b.getAttribute("transform")).toMatch(/scale\(-/);
});

test("FA-E-04: IDs eingebetteter Figuren sind präfixt, Verweise zeigen auf die eigene Kopie", async ({ page }) => {
  const fills = await page.locator('g[data-actor="player"] [data-part="bein-links"] rect').first().getAttribute("fill");
  expect(fills).toBe("url(#player--hose)");
  await expect(page.locator('[id="player--hose"]')).toHaveCount(1);
});
