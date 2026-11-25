// Content-Validator als Befehl (NF-V-01): `npm run validate` prüft content/, `npm run validate -- <ordner>` einen
// anderen Ordner. Ein Fund steht als `<code> <datei> <meldung>` auf stderr, Exit-Code 1. SVG-Regeln prüft bisher
// nur das Spiel im Browser.
import path from "node:path";
import { pathToFileURL } from "node:url";
import { validateContent } from "../../src/engine/core/content/validate.ts";
import { readContent } from "./readContent.mjs";

export function validateDir(dir) {
  const read = readContent(dir);
  const { errors } = validateContent(read.files);
  return { errors: [...read.errors, ...errors], count: Object.keys(read.files).length };
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  const dir = path.resolve(process.argv[2] ?? "content");
  const { errors, count } = validateDir(dir);
  for (const e of errors) console.error(`${e.code} ${e.file} ${e.message}`);
  console.log(`validate ${path.relative(process.cwd(), dir) || "."}: ${count} Dateien, ${errors.length} Fehler`);
  process.exit(errors.length ? 1 : 0);
}
