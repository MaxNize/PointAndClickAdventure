import react from "@vitejs/plugin-react";
import path from "node:path";
import { defineConfig } from "vite";

// Inhalte liegen unter content/. Tests setzen CONTENT_DIR auf einen eigenen Ordner, z. B. e2e/fixtures/content.
const contentDir = (process.env.CONTENT_DIR ?? "content").split(path.sep).join("/").replace(/\/+$/, "");

export default defineConfig({
  plugins: [react()],
  resolve: { alias: { "@content": path.resolve(import.meta.dirname, contentDir) } },
  define: { __CONTENT_DIR__: JSON.stringify(`/${contentDir}/`) },
});
