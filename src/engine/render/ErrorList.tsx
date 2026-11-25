// Zeigt Inhaltsfehler mit Code und Datei, damit Creative sie ohne Konsole findet (Asset-Vertrag: Fehlercodes).
import type { ContentError } from "../core/schema/index.ts";

export function ErrorList({ errors }: { errors: readonly ContentError[] }) {
  if (errors.length === 0) return null;
  return (
    <section className="content-errors" role="alert" aria-label="Fehler im Inhalt">
      <h2>{errors.length === 1 ? "1 Fehler im Inhalt" : `${errors.length} Fehler im Inhalt`}</h2>
      <ul>
        {errors.map((e, i) => (
          <li key={i} data-code={e.code}>
            <code>{e.code}</code> <span className="file">{e.file}</span> {e.message}
          </li>
        ))}
      </ul>
    </section>
  );
}
