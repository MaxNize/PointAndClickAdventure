# Projektsteckbrief

Stand: 2026-11-17, Entwurf. Teil des Anforderungskatalogs laut [Vorgaben aus dem Modul](vorgaben-modul.md).

| Punkt | Inhalt |
|---|---|
| **Projektname** | Point-and-Click-Adventure (Arbeitstitel) |
| **Ausgangssituation / Problem** | Klassische Adventures brauchen meist eine Installation, und fehlerhafte Rätsel oder Sackgassen blockieren den Fortschritt. Für das Team kommt hinzu: Arbeiten sieben Personen und KI-Agenten gleichzeitig an Code und Inhalten, bleibt ein Spiel nur dann konsistent und lösbar, wenn das automatisch geprüft wird. |
| **Ziel** | Am Semesterende steht ein kurzes Point-and-Click-Adventure, das im Desktop-Browser ohne Installation von Anfang bis Ende lösbar ist. Es läuft auf einer eigenen Engine, die neue Inhalte als SVG- und JSON-Dateien ohne Codeänderung aufnimmt. Jede zugesagte Anforderung wird von einem automatischen Gate geprüft. |
| **Zielgruppe** | Gelegenheitsspieler, die kurz und ohne Installation spielen ([P-01](voranalyse/02-personas.md)), und Genre-Fans, die faire Rätsel ohne Sackgassen erwarten ([P-02](voranalyse/02-personas.md)). |
| **Nutzerrollen** | **Spieler:** jede Person im Desktop-Browser, ohne Konto, über die URL. **Entwickler:** Teammitglied oder Agent, nutzt den Entwicklungsmodus im Entwicklungs-Build. Admin, Gast und Kontorollen gibt es nicht ([Systemrollen](voranalyse/01-stakeholder-und-rollen.md#systemrollen)). |
| **Abgrenzung** | Die Software kann ausdrücklich nicht: auf Smartphone oder Tablet laufen (keine Responsiveness), als installierbare Desktop-Anwendung laufen, Benutzerkonten oder ein Backend bieten, Barrierefreiheit zusichern, fremde oder lizenzierte Assets verwenden. |
| **Tech-Stack (vorläufig)** | React, TypeScript, Vite. Räume und Figuren als SVG, Definitionen als JSON mit Zod-Validierung, Animation mit GSAP. Prüfwerkzeuge: Vitest, Playwright, Lighthouse, ESLint, jscpd, knip. Details: [Engine-Konzept](architektur/engine-konzept.md). |

## Entscheidungsbegründung (Modul-Schritt 2, Projektentscheidung)

Neben dem Point-and-Click-Adventure standen ein AI-Detektiv, eine Physics Engine und eine Döner-App zur Auswahl. Wir haben uns für das Adventure entschieden, weil sich die Arbeit dort klar in verschiedenartige Teilbereiche aufteilen lässt: Creative (Story, Assets, Animationen), Projektmanagement (Product Owner, Scrum Master), Coding (Engine) und Qualitätssicherung. Bei den anderen Projekten wäre der Codeanteil sehr hoch gewesen, was die Parallelisierung der Arbeit stark erschwert hätte. Zudem erschien uns der Umfang der Döner-App für unsere Teamgröße zu klein, und der AI-Detektiv hätte einen kostenpflichtigen API-Schlüssel mit Guthaben erfordert.
