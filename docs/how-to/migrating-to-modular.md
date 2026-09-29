# Migration — from StorySpec "templates to copy" to the modular kit

This guide moves a project that uses the old StorySpec distribution
(monolithic `CLAUDE.dist.md` + 4-status `SPEC.md`, hand-copied templates)
over to the **modular kit** (core + opt-in modules composed by `scripts/init.sh`).

The migration is **non-destructive and incremental** : no existing story is
invalidated, and you can stop after any step.

## What changes

| Before (non-modular) | After (modular) |
|---|---|
| monolithic `CLAUDE.dist.md` copied as-is | `CLAUDE.md` **composed** from the core + declared modules |
| Universal and specific conventions mixed | Invariant core + opt-in modules + "Project-specific" block |
| 4 statuses (`todo, in_progress, done, archived`) | 8 statuses (+ `proposed`, `split`, `to_extend`, `deferred`) |
| No date field | `updated` frontmatter field (ISO 8601) |
| No manifest | `.story-spec/manifest.yaml` declares modules/agents/skills |
| Implicit tooling choice | explicit `test_adapter` (behat/pytest/vitest/none) |

Unchanged : the **story format**, `extract_features.py` extraction, the dashboard,
and the status of `.feature` files (still gitignored artifacts).

## Step 0 — Back up the existing setup

```bash
cp CLAUDE.md CLAUDE.md.bak   # if you have one derived from CLAUDE.dist.md
git switch -c chore/migrate-storyspec-modular
```

## Step 1 — Declare the manifest

```bash
mkdir -p .story-spec
cp kit/manifest.example.yaml .story-spec/manifest.yaml
$EDITOR .story-spec/manifest.yaml
```

Choose the modules that formalize what you **already do** (don't enable anything "just in case") :

- CHANGELOG/version discipline → `release-versioning`
- backlog tracked in GitHub issues → `github-piloting`
- architecture decisions recorded → `adr`
- Claude Code bootstrap (hook, agents, skills) → `claude-code`
- product docs organized along Diátaxis → `docs-diataxis`
- screenshots synced to stories → `visual-review`

Also fill in `test_adapter`, `project.language` and `project.quality_check`.

## Step 2 — Compose (dry-run first)

```bash
bash scripts/init.sh --dry-run   # lists what would be written, without touching anything
bash scripts/init.sh             # composes CLAUDE.md + scaffolds core/modules/agents/skills
```

`init` writes the core and the chosen modules under `.story-spec/`, copies agents/skills
under `.claude/`, and regenerates the `@import` block of `CLAUDE.md` between the
`<!-- BEGIN/END story-spec:modules -->` markers. Existing files are not overwritten
(`cp -n`).

## Step 3 — Bring over the project-specific bits

Open your old `CLAUDE.md.bak` and move **only** what is specific to the project
(stack, versions, `make` commands, in-house rules) under the **"Project-specific"**
section of the new `CLAUDE.md`. Everything that was universal (red→green loop,
bug doctrine, commit conventions) now comes from the **core** — do not duplicate it.

After any manifest change, recompose :

```bash
bash scripts/init.sh --sync
```

## Step 4 — Migrate the statuses (non-blocking)

The 4 old statuses remain valid ; nothing to rename. You **gain** two statuses :

- `to_extend` — a delivered (`done`) story whose evolutions/fixes are scoped and
  pending (criteria added in a "To complete" section).
- `deferred` — a scoped but postponed story, which stays visible in the backlog.

Adopt them incrementally. Extraction reminder : **only `done` stories** are extracted
to `.feature` (strict mode) — a `to_extend`/`deferred` never breaks CI.

## Step 5 — Backfill the `updated` field (optional)

Add `updated: "<YYYY-MM-DD>"` to the frontmatter of the stories you touch. No need
to redo everything at once : the field is required going forward, tolerated absent on old ones.

## Step 6 — CI : module autonomy invariant

If you vendor the modules into your repo, add the autonomy lint (ADR-0002) to your CI :

```yaml
- name: Check module autonomy (ADR-0002)
  run: bash scripts/init.sh --check
```

It fails (exit ≠ 0) if a module fragment contains a cross `@import` — the guarantee
that makes a module copyable as-is into a plain `AGENTS.md`.

## Step 7 — Verify

```bash
bash scripts/init.sh --check          # module autonomy : OK
python3 scripts/extract_features.py   # the .feature files still generate
git diff --stat
```

## Rollback

As long as you haven't merged : `git switch -` then delete the branch. The old
`CLAUDE.md.bak` restores your initial state. The migration deletes no story and no
existing script.
