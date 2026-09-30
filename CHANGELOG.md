# Changelog

All notable changes to the StorySpec kit are documented here.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and the kit adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.4.0] - 2026-09-30

### Changed
- **`estimate` is a planning field: required only on `proposed`, `todo` and
  `in_progress`.** It becomes optional on `done`, `split`, `to_extend`, `deferred` and
  `archived`, while staying allowed — and validated — on every status. See
  [ADR-0005](docs/adr/0005-estimate-is-planning-only.md).

  Requiring it everywhere meant requiring someone to invent a figure for work already
  delivered. That figure is worse than the missing field: it reads like a forecast, it
  sits in the same column as real forecasts, and it corrupts any later reading of how a
  project estimates. The kit had already reached this conclusion for `released_in`
  without generalising it.

  The error now names the status, so the reason is visible:
  `missing required frontmatter key `estimate` (status `todo`)`.

  **Relaxation only** — no story that passed before fails now, and there is nothing to
  migrate. Measured on a 291-story consumer project: 51 errors → **0**, with no story
  file edited. A project that does estimate retrospectively can keep filling the field.

  CI carries both directions: the five non-required statuses must pass without an
  estimate, and each of the three required statuses must fail without one, checked one
  status at a time. The step fails on the previous linter.

## [0.3.1] - 2026-09-29

### Fixed
- **A story that mentions `## Acceptance Criteria` in prose lost every scenario.**
  Both extractors and the linter located the section with a plain substring search, so
  the first *mention* of the heading — inside a sentence or inside a Gherkin step —
  truncated the section before the real heading. The extractor then wrote nothing and
  reported `[skip] … (no scenarios found)`; the linter reported `bdd: true but no
  scenario`. Both are now anchored to the start of a line, and when several headings
  match, the first non-empty section wins. Fixed in `scripts/extract_features.py`,
  `scripts/lint_stories.py` and the PHP port, which stay in parity.

  A story *about* the extraction script trips this by nature — which is how it was
  found, on a consumer project whose `S041` silently lost its 8 scenarios to the
  upstream extractor while the project's own implementation produced them correctly.

  CI now carries the case: a fixture story naming the heading in prose must keep its
  scenario, through the linter *and* the extractor. The step fails on the previous
  code.

## [0.3.0] - 2026-09-28

Sub-stories become legal, the lifecycle gains the two states it was missing, and the
story number is computed instead of reserved. See
[ADR-0004](docs/adr/0004-substories-proposed-split-and-id-allocation.md).

### Added
- **Sub-story ids**: `S<NNN>` may carry one lowercase letter (`S006a`), reusing the
  parent's number rather than consuming a new one. The core fragment and
  `story-author` already *prescribed* this naming for a split; `SPEC.md` and
  `lint_stories.py` forbade it. They now agree. A second level (`S006a1`) is accepted
  with a warning.
- **`status: proposed`** — written, awaiting human validation; the state a story is
  born in. Core's first rule is "propose the story and wait for validation", and until
  now the format had no way to say a story was still waiting: `todo` also means
  *validated, not started*.
- **`status: split`** — decomposed into sub-stories. The parent keeps its file as
  framing and decision log; the children carry the work. Previously a split parent had
  no honest status: `done` claims work that was never implemented, `archived` buries a
  file that is still live.
- **`scripts/next_story_id.py`** — prints the next free story number, reading the story
  files of **every git ref** (`git ls-tree` over `refs/heads` and `refs/remotes`, no
  network). `--verbose` names which ref holds which number. Shipped by `install.sh` and
  documented in `SPEC.md`, the core fragment, the `story-lint` module and the
  `stories/README.md` template.
- **CI**: `validate.yml` now asserts that every one of the eight statuses and the
  sub-story grammar pass the linter, and that an unknown status still fails it.

### Changed
- **A new story is born `proposed`, not `todo`.** The story template and the
  `story-author` agent emit `status: proposed`; validation moves it to `todo`. **This
  is the one change consumers must notice**: tooling that switches on status, or CI
  that asserts a new story is `todo`, needs to learn the value.
- **Taking a number**: core and `story-author` now say to run `next_story_id.py` and
  say explicitly **not** to keep a hand-written "reserved ids" list. `story-author`
  gains the `Bash` tool to run it, with a documented fallback of asking the operator.
  The previous instruction — "next free `S<NNN>` in `stories/`" — looked only at the
  working tree, so a story being authored on another branch was invisible and two
  authors picked the same number.
- **8-state lifecycle** propagated to `SPEC.md`, `docs/reference/format.md`, the
  `story-lint` module fragment and the `stories/README.md` template.

### Fixed
- **`generate_report.py` under-counted the total.** `total` summed only the four
  statuses it knew, so stories in any other status vanished from the denominator and
  the advertised "X/Y done (Z%)" was wrong. Measured on a 291-story project: it
  reported **237/243 (98%)** where the truth is **237/291 (81%)**. All statuses are now
  counted, and an unrecognised status is listed as `❓` *and* counted rather than
  dropped.
- **Stale status lists from v0.1.0.** The lifecycle went 4 → 6 statuses in v0.1.0 but
  `kit/templates/stories-README.md`, `docs/reference/format.md`,
  `scripts/generate_report.py` and `scripts/stories_status.sh` were never updated —
  `stories_status.sh` printed `to_extend` and `deferred` in red, as if they were
  errors. Red is now reserved for a status the lifecycle does not define.
- **`kit/templates/stories-README.md`** pointed at `https://github.com/TODO/storyspec`.

### Upgrade notes (for consumers)

This release is **additive to existing data**: no story file that was valid under
v0.2.0 becomes invalid. The id grammar is relaxed, never tightened, and the two
statuses extend an enum — hence MINOR, not MAJOR.

But the two halves move together: **an old vendored `lint_stories.py` rejects
`proposed`, `split` and `S006a`.** A project that adopts the new statuses must take the
new linter in the same change.

To update a project that installed the kit:

```bash
# re-vendor the kit, pinned to this release, then recompose CLAUDE.md
curl -fsSL https://raw.githubusercontent.com/jaegerbobomb/story-spec/main/scripts/install.sh \
  | STORY_SPEC_REF=v0.3.0 STORY_SPEC_NO_INIT=1 bash
bash scripts/init.sh --sync
```

By `git subtree`: `git subtree pull --prefix vendor/story-spec <url> v0.3.0 --squash`,
then `STORY_SPEC_DIST=vendor/story-spec/kit bash vendor/story-spec/scripts/init.sh`.

Then, in the project:

1. **Check the story files still lint**: `python3 scripts/lint_stories.py --stories-dir=stories`.
2. **Retire any hand-written "reserved ids" list** in `stories/README.md` and point at
   `next_story_id.py` instead. If that list carried backlog topics, move them to issues
   before deleting it — the list itself is what drifts, the topics are worth keeping.
3. **Re-check any dashboard built on story statuses**: a completion percentage computed
   like the old `generate_report.py` was over-reporting, and will drop when fixed.
4. **Decide whether new stories are born `proposed`.** Taking the new template and
   agent means they are. A project that does not want the validation gate can keep
   emitting `todo` — `proposed` is available, never mandatory.

A project that only vendors `SPEC.md` by hand (no `.story-spec/`) replaces that file and
updates the provenance comment to `v0.3.0`.

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

[Unreleased]: https://github.com/jaegerbobomb/story-spec/compare/v0.4.0...HEAD
[0.4.0]: https://github.com/jaegerbobomb/story-spec/compare/v0.3.1...v0.4.0
[0.3.1]: https://github.com/jaegerbobomb/story-spec/compare/v0.3.0...v0.3.1
[0.3.0]: https://github.com/jaegerbobomb/story-spec/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/jaegerbobomb/story-spec/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/jaegerbobomb/story-spec/releases/tag/v0.1.0
