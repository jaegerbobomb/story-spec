# ADR-0006 — validation is inherited by a split that changes nothing

- **Status**: accepted
- **Date**: 2026-09-30
- **Deciders**: story-spec maintainer
- **Related to**: ADR-0004 (sub-stories, `proposed`/`split`)

## Context

Two rules of the core fragment meet badly.

The first: *propose the story and wait for human validation* — encoded since 0.3.0 as
`status: proposed`, the state a story is born in.

The second: *if a story exceeds ~1 day or ~300 lines, stop and propose a split.*

Followed to the letter, a story validated on Monday and split on Tuesday produces
children that are `proposed`, and the human is asked to validate again — a perimeter they
approved the day before, with nothing new in front of them.

That is what happened on a consumer project (Didascale, 2026-09-30). `S198` was validated
with four arbitrations recorded in its notes. The session then split it, correctly: the
scope exceeded a day. Following the spec, it set `S198a` and `S198b` to `proposed`. The
split had changed nothing — the two children add up to the parent, and no choice had been
made that the parent did not already settle — so the round trip bought a re-validation of
an unchanged perimeter and delayed work that was already cleared.

The gate is there to catch splits that **drift**: a split is a moment where scope
quietly grows, where a decision gets made under cover of "just organising". That risk is
real and the gate is right to exist. But at constant scope it protects nobody and taxes
everybody — and a gate that fires where there is nothing to decide is the kind people
learn to click through where there is.

## Decision

A split **inherits the parent's validation** when two conditions hold together:

1. the children add up to the parent's scope, **exactly** — nothing added, nothing dropped;
2. the split introduced **no new decision**.

Conjunctive, not either. Then the children are born **`status: todo`**, not `proposed`,
and the parent's validation note is carried into their `## Notes`:

```markdown
## Notes

- **Validated on 2026-09-30** (inherited from S198): scope identical to the parent,
  no new decision.
```

At the slightest change of scope, or any choice the split had to make on its own, the
normal rule applies: children are `proposed` and wait for a human.

## Consequences

**No tooling change, and that is worth stating.** `todo` was already a valid status for
any story, sub-story included, so `lint_stories.py` needs no change and gains no check.
It cannot gain one: whether a split preserved scope is a judgement about two documents'
meaning, not a property of a file. No status encodes it either — and inventing one
(`inherited`) would push a claim about *why* a story is `todo` into the lifecycle, where
it would be asserted by the same session that made the split.

What makes the rule auditable is therefore the **validation note in the children**: a
child born `todo` without one is the thing to question in review. That is a review
convention, not a gate, and the ADR says so rather than pretending otherwise.

**The relaxation is narrow by construction.** It applies only where a human has already
validated the parent. A split of a `proposed` parent inherits nothing, because there is
nothing to inherit.

**It cuts the wrong way if the two conditions are read loosely.** "The scope is basically
the same" is not condition 1, and "I only had to decide how to cut it" may well be a new
decision — if the cut line itself is a design choice with consequences, it is one. The
wording is deliberately strict so that the honest answer to "am I sure?" is usually
*ask*.

## Alternatives considered

- **Keep re-validating every split.** Rejected on evidence: it cost a full round trip on
  S198 for nothing, and its cost is paid on exactly the splits that are least risky.
- **Never re-validate a split.** Rejected: a split is a classic place for scope to grow,
  and the parent's validation says nothing about children that are not the parent.
- **A `inherited` or `revalidate: false` field.** Rejected: it encodes in metadata a
  claim the splitting session makes about its own work, and the linter still could not
  check it. The note in `## Notes` carries the same information where a reviewer reads
  it, without pretending it is machine-verified.
- **Let the parent stay `todo` and skip `split`.** Rejected: it would undo ADR-0004 — a
  parent that is not implemented directly has no business claiming a status that says
  someone will pick it up.
