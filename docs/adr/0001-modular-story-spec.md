# ADR-0001 — story-spec goes modular (core + opt-in modules)

- **Status** : proposed
- **Date** : 2026-06-21
- **Deciders** : story-spec maintainer
- **Proving ground** : an internal production application (~105 stories)

## Context

story-spec is currently distributed as a set of **templates to copy** :
`CLAUDE.dist.md` (monolith), `SPEC.md`, `templates/story.md`, and four extraction scripts
(`extract_features.py`, PHP port, `stories_status.sh`, `generate_report.py`). Only four
statuses (`todo, in_progress, done, archived`).

Three limits block the goal of "quickly bootstrapping apps with very high-quality
agents" :

1. **Coupled monolith** — `CLAUDE.dist.md` mixes the universal (story lifecycle, BDD) and the
   implicit (choices of a given project). Copying = importing irrelevant noise.
2. **Gains stuck downstream** — the proving ground (internal production application) matured practices that
   never came back upstream : `to_extend`/`deferred` statuses, **red→green TDD** bug doctrine,
   release discipline (CHANGELOG + version + README in one commit), epic/sub-issue tracking,
   and visual review.
3. **No extensibility and no agents** — no module mechanism, no sub-agent/skill,
   no ADR, no init command.

## Decision

Rebuild story-spec into an **invariant core + opt-in modules** :

- **Core** (always present) : story format, **6-status lifecycle**, extraction
  scripts, dashboard, **red→green TDD** bug doctrine, `updated` frontmatter.
- **Manifest** `.story-spec/manifest.yaml` declaring the enabled modules.
- **Modules** `modules/<name>/` — each = `CLAUDE.md` fragment + optional `SPEC` section
  + tooling + agents/skills. Initial catalog : `adr` *(new)*, `release-versioning`,
  `github-piloting`, `story-lint` *(new)*, `visual-review`, `docs-diataxis` *(new)*,
  `claude-code`, plus the `bdd-behat`/`bdd-pytest`/`bdd-vitest` test adapters.
- **`CLAUDE.dist.md` composed by `@import`** of the chosen modules' fragments (no more monolith).
- **Agents & skills** shipped with the kit : `story-author`, `story-implementer`, `spec-guardian`,
  `release-bump`, `adr-new`.
- **`story-spec init` command** that scaffolds and writes only the selected modules.

First module created : **`adr`** — and the first decision recorded is this very ADR
(dogfooding).

## Consequences

**Positive**
- Composability : a new project only ships what it needs.
- Agent quality : sub-agents/skills standardize the story → red/green → release loop.
- The proving ground's gains come back upstream and benefit all downstream projects.

**Costs / risks**
- Reworking `CLAUDE.dist.md` (monolith → composition) ; migrating the scripts into per-BDD-module
  adapters.
- Increased maintenance surface (several modules).
- Need for a stable "module fragment" contract to avoid drift (cf. SPEC §Modules).

## Rejected alternatives

- **Keep the monolith and pile on options** : retains the coupling, does not solve agent
  quality.
- **One repo per module** : too much fragmentation for a bootstrap kit ; a monorepo of modules
  versioned together is preferable at this stage.

## Follow-up

- [ ] Core : 6 statuses, bug doctrine, `updated` frontmatter.
- [ ] `adr` module + `adr-new` skill.
- [ ] Manifest + composed `CLAUDE.dist` + `scripts/init.sh`.
- [ ] `story-author`, `story-implementer`, `spec-guardian` agents ; `release-bump` skill.
