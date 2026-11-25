# Einstiegspunkt für Aufgaben, lokal und in der CI. `ci` ist der Gate-Lauf (EP-01).
# EP-14 ergänzt `worktree`, das Projektgerüst die Installation der Abhängigkeiten.
.DEFAULT_GOAL := help
.PHONY: help setup hooks ci

help: ## Alle Ziele mit Kurzbeschreibung
	@grep -E '^[a-z-]+:.*## ' $(MAKEFILE_LIST) | awk -F':.*## ' '{printf "  %-8s %s\n", $$1, $$2}'

setup: hooks ## Klon einrichten: Git-Hooks aktivieren (Abhängigkeiten kommen mit dem Projektgerüst)

hooks: ## Git-Hooks aus .githooks/ aktivieren (pre-push, EP-24)
	git config core.hooksPath .githooks

ci: ## Alle Prüfungen, Abbruch beim ersten Fehler (EP-01)
	node tools/ci/run-ci.mjs
