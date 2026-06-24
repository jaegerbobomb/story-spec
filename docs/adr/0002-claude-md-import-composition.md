# ADR-0002 — Composition via `@import` in CLAUDE.md (no generated AGENTS.md)

- **Status** : accepted
- **Date** : 2026-06-22
- **Deciders** : story-spec maintainer
- **Related to** : ADR-0001 (modular mechanics)

## Context

ADR-0001 established modular mechanics whose composed output is `CLAUDE.dist.md`,
aggregated by `@import` of module fragments. This raises multi-tool portability :
`AGENTS.md` is an open convention (Cursor, Codex, Jules, Aider…) but **without standardized
`@import`** across tools. Three possible targets : CLAUDE.md via `@import` (current),
AGENTS.md inlined by `init`, or both generated in parallel.

## Decision

Keep **`CLAUDE.md` composed by `@import`** as the sole composition target.

- **Module separation comes first.** Each `modules/<name>/CLAUDE.md` is a **self-contained**
  fragment (constraint : no cross `@import` between modules). This is the value-bearing
  invariant ; the rest is just aggregation.
- **No `AGENTS.md` generation.** Whoever wants AGENTS usage copies the desired fragments —
  a trivial operation since they are self-contained. We do **not** introduce an inlining script to
  maintain nor a dual output to keep in sync.
- Deliberate bet : `AGENTS.md` is likely to adopt an import mechanism ; if so, the
  switch will be mechanical and free of accumulated debt.

## Consequences

**Positive**
- Minimal maintenance surface (a single target, no inliner).
- Modules reusable as-is by copy, to any tool.
- `@import` preserves hierarchical discovery and Claude-specific references (`.claude/`).

**Costs / risks**
- No "turnkey" portability : a non-Claude project must copy manually.
- **Constraint to uphold** : no `@import` between module fragments — to be checked in
  review (otherwise the "copy for AGENTS" path breaks).

## Rejected alternatives

- **`AGENTS.md` inlined by `init`** : portable by default, but imposes a concatenation script
  to maintain and keep in sync — rejected (cost > benefit at this stage).
- **Dual output (AGENTS.md + CLAUDE.dist.md)** : risk of divergence between two files
  meant to say the same thing — rejected.
