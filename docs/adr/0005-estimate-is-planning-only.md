# ADR-0005 — `estimate` is a planning field, not a record

- **Status**: accepted
- **Date**: 2026-09-30
- **Deciders**: story-spec maintainer
- **Related to**: ADR-0004 (lifecycle and id grammar)

## Context

`estimate` was required on every story, in every status. Applied to a real backlog that
means requiring it on stories that are finished, decomposed, abandoned or parked.

On a consumer project (Didascale), 51 stories had no `estimate`. All 51 were `done`
(47) or `split` (4). There was nothing to fix there: nobody estimated those stories at
the time, and the lint error demanded that someone now invent a figure for work already
delivered.

That figure would be worse than the missing field. It reads like a forecast, it sits in
the same column as real forecasts, and it silently corrupts any later reading of how the
project estimates — the one thing an estimate corpus is good for. A `done` story with no
`estimate` is an honest record; a `done` story with a reconstructed `M` is a fabricated
one.

The project had already reached the same conclusion for the neighbouring field, without
generalising it: the `release-versioning` module's `released_in` was deliberately **not**
backfilled onto its 157 delivered stories, on the grounds that it "would have been
reconstruction". The same argument applies to `estimate`; the spec just never said so.

## Decision

`estimate` is **required only** where someone is about to plan or do the work:
`proposed`, `todo`, `in_progress`.

It is **optional** on `done`, `split`, `to_extend`, `deferred` and `archived` — and it
stays **allowed and validated** on every status. A story parked in `deferred` with an
estimate keeps it, and the field becomes required again the moment the story returns to
`in_progress`.

The required set is the answer to "who is about to use this number?", not a judgement
about which statuses are terminal. That is why `deferred` and `to_extend` sit on the
optional side even though work may resume from them: the requirement re-applies at the
transition back into `in_progress`, which is when the estimate is actually needed. A
story parked for six months does not owe anybody a size.

`REQUIRED` in `lint_stories.py` therefore loses `estimate`, which gets its own
status-aware check, and the error names the status so the reason is visible:

```
missing required frontmatter key `estimate` (status `todo`)
```

## Consequences

**Relaxation only.** No story that passed before fails now: the check is strictly
narrower. Hence **0.4.0** (MINOR), not a major — and nothing for a consumer to migrate.

**Measured effect.** On Didascale's 291 live stories the error count goes from 51 to
**0**, together with the extractor fix released in 0.3.1. No story file was edited to
get there.

**A consumer that wants the old strictness has no switch.** Deliberate: a per-project
"require estimate everywhere" flag would reintroduce the demand to reconstruct, which is
the thing being rejected. A project that genuinely estimates retrospectively can fill
the field — it stays allowed.

**The rule is stated where it is enforced.** `SPEC.md` § *Estimate values*,
`docs/reference/format.md`, the `story-lint` fragment and the `stories/README.md`
template all say it, and CI carries both directions: the five non-required statuses must
pass without an estimate, and each of the three required statuses must fail without one
— checked one status at a time so a lenient status cannot hide behind a strict
neighbour. The step fails on the previous linter.

## Alternatives considered

- **Backfill the 51 estimates.** Rejected: that is the fabrication the decision exists
  to prevent.
- **Drop `estimate` from the required set entirely.** Rejected: on a story about to be
  planned, the size is exactly the information the field is for, and making it optional
  everywhere would let it rot away where it matters.
- **A warning instead of an error on terminal statuses.** Rejected: a warning that can
  never be legitimately fixed is noise, and `--strict` would turn it back into a gate.
- **A `sized` boolean, or moving `estimate` into a module.** Rejected: it is a core
  planning field with a clear meaning; the problem was never where it lived, only when
  it was demanded.
