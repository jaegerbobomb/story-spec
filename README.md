# StorySpec

**Write the story once. Run it as a test. Compose the rest as modules.**

User stories as living specifications - one markdown file, three audiences:
product owner, developer, CI pipeline. StorySpec is now a **modular kit**: a
small mandatory core plus opt-in modules you compose per project.

→ [Full specification](SPEC.md)
→ [Getting started](docs/tutorials/getting-started.md)
→ [Migrating to the modular kit](docs/how-to/migrating-to-modular.md)
→ [Examples](examples/)
→ [Architecture decisions](docs/adr/)
→ [Changelog](CHANGELOG.md)

---

## The problem

**User stories** capture the *who* and *why*, but stay vague on the *what*.
**Use cases** capture the *what* in detail, but drift away from the code.
**BDD feature files** capture the *what* as executable tests, but are a chore to maintain separately.

Keeping all three in sync is permanent friction. In practice, only one survives :
usually the test file, which ends up as the only real documentation,
but unreadable by a non-developer.

## The solution

A StorySpec file is all three at once:

~~~markdown
---
id: S001
title: "User registration"
epic: auth
status: done
estimate: S
bdd: true
updated: "2026-06-21"
---

## User story

> As a **visitor**, I want to **create an account** so that I can **access the application**.

## Acceptance Criteria

### Scenario: Successful registration

* **Given** no account exists with email `alice@example.com`
* **When** `POST /api/users` is sent with email and password
* **Then** the response status is 201
* **And** a confirmation email is sent
~~~

A single script (`extract_features.py`) reads the `## Acceptance Criteria` section
and generates a `.feature` file for Behat, Cucumber, or any BDD framework.
The markdown file stays the single source of truth.
Generated `.feature` files are build artifacts - gitignored.

## Principles

1. **One file, three audiences.** Readable by a product owner, a developer, and a CI pipeline.
2. **Generated artifacts are disposable.** `.feature` files are generated at test time and gitignored.
3. **YAML frontmatter carries metadata.** Status, estimate, dependencies - all machine-readable.
4. **Diagrams live with the story.** Mermaid renders natively in GitHub and most IDEs - no external tools.
5. **Framework-agnostic format.** The extraction script is the only implementation detail; the format works with any BDD runner.
6. **Core + opt-in modules.** The lifecycle is mandatory; everything else (ADR, release, GitHub piloting…) is a module you turn on per project. See [ADR-0001](docs/adr/0001-modular-story-spec.md).

## The modular kit

StorySpec moved from *"templates to copy"* to a *"kit to compose"*. A project
declares the modules it wants in a manifest, and `story-spec init` composes the
`CLAUDE.md`, the SPEC and the scaffolding from the core plus those modules.

```
story-spec/
├── CLAUDE.dist.md          # composition template (@import of core + enabled modules)
├── SPEC.md                 # format spec (lifecycle: 6 statuses, `updated` field)
├── core/                   # mandatory: core CLAUDE fragment (lifecycle lives in SPEC.md)
│   └── CLAUDE.core.md
├── modules/<name>/         # opt-in: CLAUDE.md, SPEC.section.md, templates/, skills/
├── agents/                 # story-author, story-implementer, spec-guardian
├── skills/                 # release-bump (+ adr-new shipped by the adr module)
├── scripts/init.sh         # composer / scaffolder / autonomy linter
└── .story-spec/
    └── manifest.example.yaml   # declares enabled modules for a project
```

### Available modules

| Module | Purpose |
|---|---|
| `adr` | Architecture Decision Records (+ `adr-new` skill) |
| `github-piloting` | epics + sub-issues + session log |
| `release-versioning` | CHANGELOG + version + README kept in sync |
| `story-lint` | CI gate: `lint_stories.py` validates every story file |
| `claude-code` | `session-start` hook, `settings.json`, agents & skills |
| `docs-diataxis` | organize the app's product docs along the four Diátaxis modes |
| `visual-review` | screenshots synced to delivered UI stories (tool-agnostic) |

**Module autonomy (ADR-0002):** each `modules/<name>/CLAUDE.md` fragment is
self-contained — no cross-module `@import`. Only `CLAUDE.dist.md` aggregates.
That is what keeps a module copy-pasteable into a plain `AGENTS.md`.
`scripts/init.sh --check` enforces this invariant (lint only, non-zero exit on
violation) and runs in CI.

## Install into your repo

From the root of your project, one line vendors the kit and bootstraps it:

```bash
curl -fsSL https://raw.githubusercontent.com/jaegerbobomb/story-spec/main/scripts/install.sh | bash
```

It downloads the kit, vendors the full catalog under `.story-spec/dist/`, copies the
runtime scripts into `scripts/`, creates `.story-spec/manifest.yaml`, and composes
`CLAUDE.md`. The project is then self-contained — `init.sh` auto-detects the vendored
kit, so you never need the source checkout again.

```bash
# pin a version, or vendor without the initial compose
curl -fsSL .../install.sh | STORY_SPEC_REF=v0.1.0 bash
curl -fsSL .../install.sh | STORY_SPEC_NO_INIT=1 bash
```

Prefer not to pipe to a shell? Alternatives:

- **git subtree** — `git subtree add --prefix .story-spec/dist https://github.com/jaegerbobomb/story-spec main --squash`, then copy the scripts you need and run `bash .story-spec/dist/scripts/init.sh`.
- **Manual** — download/clone the repo and run `STORY_SPEC_DIST=path/to/story-spec bash path/to/story-spec/scripts/init.sh` from your project root.

## Quick start

After installing (or from a clone of this repo):

```bash
# 1. Declare the modules you want for your project
$EDITOR .story-spec/manifest.yaml      # pick modules, agents, skills, test adapter

# 2. Preview what would be scaffolded, then compose
bash scripts/init.sh --dry-run
bash scripts/init.sh

# 3. Write the story, fill in the Acceptance Criteria, then lint it
python3 scripts/lint_stories.py --stories-dir=stories

# 4. Generate .feature files before running your BDD suite
python3 scripts/extract_features.py

# 5. Run Behat / Cucumber as usual
```

Re-run `bash scripts/init.sh --sync` after editing the manifest to recompose
`CLAUDE.md`.

## Scripts

| Script | Language | Purpose |
|---|---|---|
| `scripts/install.sh` | Bash | Vendor the kit into another repo and bootstrap it |
| `scripts/init.sh` | Bash | Compose `CLAUDE.md` + scaffold core/modules from the manifest (`--dry-run`, `--sync`, `--check`) |
| `scripts/extract_features.py` | Python 3 (stdlib) | Story → `.feature` generator |
| `scripts/lint_stories.py` | Python 3 (stdlib) | Validate story files (`story-lint`; `--strict`) |
| `scripts/generate_report.py` | Python 3 (stdlib) | Markdown status report for GitHub Pages |
| `scripts/stories_status.sh` | Bash | Colour-coded terminal dashboard |
| `scripts/ports/php/extract_features.php` | PHP 8+ | PHP port for projects that already have PHP |

## Credits

This methodology builds on **Dan North**'s foundational work on
[Behavior-Driven Development](https://dannorth.net/introducing-bdd/) (2006)
and **Gojko Adzic**'s [Specification by Example](https://gojko.net/books/specification-by-example/) (2011).

The intuition of treating a user story's acceptance criteria as a functional specification -
and using them directly as executable tests - was inspired by **Tony Heap**'s
["An Agile Functional Specification"](https://www.its-all-design.com/an-agile-functional-specification/),
which showed how user stories, use cases, and acceptance criteria can all be the same artefact.
