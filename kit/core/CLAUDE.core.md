# Core — CLAUDE fragment (always imported)

> Imported at the top of `CLAUDE.dist.md`. This is your **operating contract**, not
> reference docs: follow it on every turn. It holds the invariant — propose the story,
> red→green loop, bug doctrine. Project/language specifics come from the modules.

## Absolute rule — propose the story first

Before any feature development, propose a `stories/S<NNN>-<slug>.md` story
in story-spec format with **`status: proposed`**, and **wait for human validation**
(validation moves it to `todo`). Only exceptions: urgent bug fixes and micro-refactors
with no functional impact.

**Take the number with the tool, never from memory or from a list:**

```bash
git fetch --all --prune && python3 scripts/next_story_id.py --verbose
```

It reads the story files of **every git ref**, not just the working tree. A story
being written on another branch already owns its number; deducing the free number
from `main` alone is how two sessions on the same day pick the same one.

## Per-story loop

1. Read the story in full.
2. Check `depends_on` (flag any dependency not `done`).
3. Short plan (5–10 lines): classes/files, layers involved.
4. **Tests first (red)**: `bdd: true` → feature + steps; `bdd: false` → unit tests.
5. Implement the minimum (green).
6. Refactor (tests still green).
7. Quality (lint + static analysis per the language module).
8. **Enabled-module obligations (before closing)**: apply the end-of-story rules of any
   active module — record an **ADR** if the change is structural (`adr`), bump
   **CHANGELOG + version** in the same commit (`release-versioning`), update the
   **Diátaxis docs** for user-facing changes (`docs-diataxis`), sync **screenshots**
   (`visual-review`). See each module's section below.
9. Single commit: `feat(S<NNN>): <short slug>`.
10. Move the story to `status: done`.

**Size**: if the story exceeds ~1 day or ~300 lines of prod code, **stop without committing**
and propose a split (`S<NNN>a`, `S<NNN>b`). The children take the parent's number plus a
letter — no new number is consumed — and the parent moves to **`status: split`**: it keeps
the framing and the decision log, the children carry the work.

**Validation inherits when the split changes nothing**: if the children add up to the
parent's scope **and** the split decided nothing new, they are born `todo` and carry the
parent's validation note in their `## Notes`. Both conditions, not either. At the
slightest change of scope, or any choice the split made on its own, they are `proposed`
and wait for a human. Re-validating an unchanged perimeter costs a review round and
protects nobody.

**Ambiguity**: ask a question before coding; record the answer under `## Notes`.

## Bug doctrine (core)

There is **no** "BUG" story type. Two cases:

| Situation | Action |
|---|---|
| Behavior already specified by an existing story | Fix it and **complete the original story** (missing criteria/tests). |
| Behavior not covered | Create a **normal story** (definition + criteria + tests). |

Never name a story `S<NNN>-bug-…` nor give it `type: bug`.

### Bug fix — red → green test MANDATORY

Every fix comes with a test (BDD *or* unit) that:

1. **fails first** on the uncorrected code (red) — proof it targets the bug;
2. **passes** after the fix (green).

Write the test **first**, observe the failure (paste the red output in the PR), apply the
fix, observe the green. The PR explicitly mentions "red → green test" + the name of the
test. A test already green before the fix proves nothing: no red→green, no merge.

**Micro-fix exception** (typo, broken link, label): direct commit without a story, with
a reference to the issue (`fix: back button label (#42)`).

## Commits (core)

`type(scope): short description` — types: `feat, fix, docs, chore, refactor, test, ci`.
Scope = story id (`S006`) or component. Closing an issue: `fix #NNN`/`close #NNN` in the
**body** (not the title).
