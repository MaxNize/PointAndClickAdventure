// FA-E-01 Raum laden: Akzeptanzkriterium „E2E-Test: Alle Ebenen des Testraums werden angezeigt.“
import { expect, test } from "@playwright/test";

test("FA-E-01: alle Ebenen des Testraums werden angezeigt", async ({ page }) => {
  const consoleErrors: string[] = [];
  page.on("console", (m) => m.type() === "error" && consoleErrors.push(m.text()));
  page.on("pageerror", (e) => consoleErrors.push(e.message));

  await page.goto("/");
  const room = page.locator('svg[data-room="testraum"]');
  await expect(room).toBeVisible();

  for (const id of ["layer-background", "layer-mid-saeule", "layer-mid-block", "layer-foreground"])
    await expect(room.locator(`> g#${id}`), id).toBeVisible();
  await expect(room.locator("> g#hotspots #hotspot-kiste")).toHaveCount(1);

  // Zeichenreihenfolge: Mittelebenen nach Basislinie (Säule 750 vor Block 900), obwohl die Datei sie andersherum hat.
  const order = await room.locator("> g[id]").evaluateAll((gs) => gs.map((g) => g.id));
  expect(order).toEqual(["layer-background", "hotspots", "layer-mid-saeule", "layer-mid-block", "layer-foreground"]);

  await expect(page.getByRole("alert", { name: "Fehler im Inhalt" })).toHaveCount(0);
  expect(consoleErrors).toEqual([]);
});
