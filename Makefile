# Einstiegspunkt für Aufgaben, lokal und in der CI. `ci` ist der Gate-Lauf (EP-01).
# EP-14 ergänzt `worktree`. `deps` installiert die Abhängigkeiten des Projektgerüsts (EP-16).
.DEFAULT_GOAL := help
.PHONY: help setup hooks deps ci

help: ## Alle Ziele mit Kurzbeschreibung
	@grep -E '^[a-z-]+:.*## ' $(MAKEFILE_LIST) | awk -F':.*## ' '{printf "  %-8s %s\n", $$1, $$2}'

setup: hooks deps ## Klon einrichten: Git-Hooks aktivieren, Abhängigkeiten installieren

hooks: ## Git-Hooks aus .githooks/ aktivieren (pre-push, EP-24)
	git config core.hooksPath .githooks

deps: ## Abhängigkeiten exakt nach package-lock.json installieren (EP-16), Chromium für die E2E-Tests
	npm ci
	npx playwright install $(if $(CI),--with-deps) chromium

ci: ## Alle Prüfungen, Abbruch beim ersten Fehler (EP-01)
	node tools/ci/run-ci.mjs
