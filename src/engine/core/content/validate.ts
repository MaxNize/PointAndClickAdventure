// Content-Validator (NF-V-01): Laden mit Schemas plus Prüfungen über Dateien hinweg. Dieselbe Funktion nutzen das
// Spiel im Browser und der Befehl `npm run validate`. SVG-Prüfungen laufen bisher nur im Browser (Darstellung).
import { dialogErrors } from "./dialogGraph.ts";
import { loadContent, type ContentFiles, type LoadResult } from "./load.ts";
import { referenceErrors } from "./references.ts";

export function validateContent(files: ContentFiles): LoadResult {
  const { content, errors } = loadContent(files);
  errors.push(...referenceErrors(content));
  for (const [id, d] of content.dialogs) errors.push(...dialogErrors(d, `content/dialogs/${id}.json`));
  return { content, errors };
}
