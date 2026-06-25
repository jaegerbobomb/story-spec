# Changelog

All notable changes to the StorySpec kit are documented here.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and the kit adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.0] - 2026-06-24

Agent-first framing, story↔ADR traceability, and a cleaner repo layout.

### Added
- **Story → ADR traceability**: optional `adr: [NNNN]` frontmatter field
  (provided by the `adr` module) documented in `SPEC.md`, added to the story
  template and examples, and checked by `story-lint`. Back-reference: ADRs carry
  a `Related stories` field.
- **ADR-0003**: group the distributable catalog under `kit/`.

### Changed
- **Repo layout (ADR-0003)**: everything vendored into a project is grouped under
  `kit/` (`core/`, `modules/`, `agents/`, `skills/`, `templates/`,
  `CLAUDE.dist.md`, `manifest.example.yaml`). `scripts/` stays at the root.
  `.story-spec/` now exists **only** in a consumer project.
- **Agent-first framing**: README and `core/CLAUDE.core.md` make explicit that the
  `kit/` fragments are an *operating contract* that forces an agent to follow the
  method (story → red→green → ADR → changelog → docs), not mere documentation.
  New "Why agent-first" section under `docs/explanation/`.
- **Tooling paths**: `scripts/init.sh` resolves its source as `$STORY_SPEC_DIST` →
  `.story-spec/dist` → `<repo>/kit`; `install.sh` and the CI path filters updated
  for the `kit/` layout.

## [0.1.0] - 2026-06-23

First release of StorySpec as a **modular kit** (core + opt-in modules).
Dogfoods its own [ADR](docs/adr/) and release discipline.

### Added
- **Modular kit architecture**: mandatory `core/` + opt-in `modules/`, composed
  per project from a `.story-spec/manifest.yaml` ([ADR-0001](docs/adr/0001-modular-story-spec.md)).
- **`scripts/init.sh`**: composer / scaffolder / autonomy linter (`--dry-run`,
  `--sync`, `--check`); auto-detects a vendored kit at `.story-spec/dist`.
- **`scripts/install.sh`**: one-line installer that vendors the kit into another
  repo and bootstraps it.
- **`scripts/lint_stories.py`**: story-file validator (the `story-lint` module).
- **`CLAUDE.dist.md`**: composition template aggregating core + enabled modules
  via `@import` ([ADR-0002](docs/adr/0002-claude-md-import-composition.md)).
- **Module catalog**: `adr`, `github-piloting`, `release-versioning`, `story-lint`,
  `claude-code`, `docs-diataxis`, `visual-review`.
- **Agents**: `story-author`, `story-implementer`, `spec-guardian`.
- **Skills**: `release-bump` (+ `adr-new`, shipped by the `adr` module).
- **Architecture Decision Records** under `docs/adr/`.
- **CI**: module-autonomy check (`init.sh --check`) and `story-lint` wired into
  `validate.yml`.
- **Migration guide** for non-modular projects: [docs/how-to/migrating-to-modular.md](docs/how-to/migrating-to-modular.md).

### Changed
- **Story lifecycle: 4 → 6 statuses** — added `to_extend` and `deferred`
  alongside `todo`, `in_progress`, `done`, `archived` (`SPEC.md`).
- **New frontmatter field `updated`** (ISO 8601, last revision date).
- **Core per-story loop** now points to enabled-module obligations (ADR, release,
  docs, visual-review) before closing a story (`core/CLAUDE.core.md`).
- **README** rewritten around the modular kit; docs reorganized along Diátaxis.

[Unreleased]: https://github.com/jaegerbobomb/story-spec/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/jaegerbobomb/story-spec/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/jaegerbobomb/story-spec/releases/tag/v0.1.0
