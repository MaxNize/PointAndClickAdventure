// Node-Adapter für Inhalte (Engine-Konzept: Schichten): liest einen Inhaltsordner wie der Browser-Adapter.
// JSON wird geparst, SVG bleibt Text, Schlüssel sind `content/…` unabhängig vom echten Ordner.
import fs from "node:fs";
import path from "node:path";

/** @returns {{ files: Record<string, unknown>, errors: Array<{ code: string, file: string, message: string }> }} */
export function readContent(dir) {
  const files = {};
  const errors = [];
  if (!fs.existsSync(dir)) return { files, errors };
  for (const rel of fs.readdirSync(dir, { recursive: true })) {
    const full = path.join(dir, rel);
    if (fs.statSync(full).isDirectory()) continue;
    const key = `content/${String(rel).split(path.sep).join("/")}`;
    const text = fs.readFileSync(full, "utf8");
    if (!key.endsWith(".json")) files[key] = text;
    else {
      try {
        files[key] = JSON.parse(text);
      } catch (e) {
        errors.push({ code: "content.json-invalid", file: key, message: `kein gültiges JSON: ${e.message}` });
      }
    }
  }
  return { files, errors };
}
