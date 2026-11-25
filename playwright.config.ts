// E2E-Tests im Browser. Der Dev-Server lädt die Testinhalte aus e2e/fixtures/content, nicht aus content/.
import { defineConfig, devices } from "@playwright/test";

const PORT = 5180;

export default defineConfig({
  testDir: "e2e",
  forbidOnly: !!process.env.CI,
  retries: 0,
  reporter: process.env.CI ? "list" : [["list"]],
  use: { baseURL: `http://127.0.0.1:${PORT}`, trace: "retain-on-failure" },
  projects: [{ name: "chromium", use: { ...devices["Desktop Chrome"] } }],
  webServer: {
    command: `npm run dev -- --port ${PORT} --strictPort --host 127.0.0.1`,
    url: `http://127.0.0.1:${PORT}`,
    env: { CONTENT_DIR: "e2e/fixtures/content" },
    reuseExistingServer: false,
    timeout: 60_000,
  },
});
