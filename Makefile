# Einstiegspunkt für Aufgaben, lokal und in der CI. Dieses Makefile ist ein Anfang:
# EP-01 ergänzt `ci`, EP-14 `worktree`, das Projektgerüst die Installation der Abhängigkeiten.
.DEFAULT_GOAL := help
.PHONY: help setup hooks

help: ## Alle Ziele mit Kurzbeschreibung
	@grep -E '^[a-z-]+:.*## ' $(MAKEFILE_LIST) | awk -F':.*## ' '{printf "  %-8s %s\n", $$1, $$2}'

setup: hooks ## Klon einrichten: Git-Hooks aktivieren (Abhängigkeiten kommen mit dem Projektgerüst)

hooks: ## Git-Hooks aus .githooks/ aktivieren (pre-push, EP-24)
	git config core.hooksPath .githooks
