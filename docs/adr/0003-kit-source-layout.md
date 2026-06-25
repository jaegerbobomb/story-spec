# ADR-0003 — group the distributable catalog under `kit/`

- **Status**: accepted
- **Date**: 2026-06-24
- **Deciders**: story-spec maintainer
- **Related to**: ADR-0001 (modular mechanics), ADR-0002 (`@import` composition)

## Context

After ADR-0001 the repository root mixed three unrelated concerns: the
**distributable catalog** (`core/`, `modules/`, `agents/`, `skills/`, `templates/`,
`CLAUDE.dist.md`), the **tooling** (`scripts/`), and the **repo's own docs/meta**
(`README.md`, `SPEC.md`, `docs/`, `examples/`). On top of that, a `.story-spec/`
directory held only `manifest.example.yaml` — confusing, because `.story-spec/` is
the *consumer's* configuration directory (manifest + vendored `dist/`), not something
the kit repo is itself a consumer of. "What exactly gets vendored into my project?"
had no obvious answer.

## Decision

Group everything that is vendored into a consuming project under a single **`kit/`**
directory:

```
kit/{core,modules,agents,skills,templates}/  kit/CLAUDE.dist.md  kit/manifest.example.yaml
```

- `scripts/` stays at the root: it is **tooling** (installer, composer, extractors),
  not composable doctrine.
- `.story-spec/` is **removed from the kit repo**. It now exists *only* in a consumer
  project, where `install.sh` creates `.story-spec/manifest.yaml` and vendors the
  catalog into `.story-spec/dist/`.
- `scripts/init.sh` resolves its source (`DIST`) in order: `$STORY_SPEC_DIST` →
  `$ROOT/.story-spec/dist` (installed project) → `<repo>/kit` (running from this repo).

## Consequences

**Positive**
- The root is legible; `kit/` answers "what gets vendored" at a glance.
- `.story-spec/` has one meaning only — the consumer's config dir — removing the
  earlier ambiguity.
- The `install.sh` raw URL (`scripts/install.sh`) is unchanged, so existing install
  instructions keep working.

**Costs / risks**
- Path churn: `init.sh`/`install.sh` source paths, CI path filters, and README/tree
  references had to be updated in lockstep.
- Anyone who pinned internal paths (e.g. `STORY_SPEC_DIST=…/story-spec`) must now point
  at `…/story-spec/kit`.

## Rejected alternatives

- **Keep a flat root, just move the manifest out of `.story-spec/`**: removes the
  hidden-dir confusion but leaves the root cluttered and still mixes catalog with meta.
- **Move `scripts/` under `kit/` too**: would change the public installer URL and
  blurs the tooling-vs-doctrine line for no real gain.
