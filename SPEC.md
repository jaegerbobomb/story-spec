# StorySpec — Format Specification

## File naming

Each story is a markdown file named `S<NNN>-<slug>.md` (e.g. `S006-user-login.md`),
placed in a `stories/` directory at the root of the project.

| Part | Rule |
|---|---|
| `S<NNN>` | Sequential integer, zero-padded to 3 digits, never reused |
| `<suffix>` | Optional sub-story marker: one lowercase letter (`S006a`) — see *Sub-stories* |
| `<slug>` | kebab-case, ≤ 5 words, descriptive |

### Choosing the number

A number is **never reused**, so it must be free across the whole repository — not
just in the branch you happen to be on. A story being written on another branch owns
its number already, and looking only at `stories/` in the working tree is exactly how
two authors pick the same number on the same day.

```bash
python3 scripts/next_story_id.py             # the next free number
python3 scripts/next_story_id.py --verbose   # + which git ref holds which number
```

Do **not** keep a hand-written "reserved ids" list. It drifts the moment nobody
updates it, it cannot see branches — so it never catches the collision it exists to
prevent — and a list that is wrong is worse than no list at all.

### Sub-stories

When a story is split (see *Workflow*), the children take the parent's number plus one
lowercase letter: `S006` → `S006a`, `S006b`. The letter consumes **no new number** —
`S006` and `S006a` are the same number, one of them decomposed.

The parent keeps its file and moves to `status: split`. It is no longer implemented
directly: it holds the framing and the decision log, the children hold the work.

A second level (`S006a1`) is accepted by the tooling but reported as a warning — it
usually means the parent was split too coarsely.

---

## Frontmatter (required)

```yaml
---
id: S006                        # Unique identifier, never reused
title: "Short title"            # Human-readable, ≤ 8 words
epic: auth                      # Logical group (one word or kebab-case)
depends_on: [S001, S002]        # Prerequisite stories (empty array if none)
status: proposed                # See status values below
estimate: M                     # Planning field — see Estimate values below
bdd: true                       # true → generates a .feature | false → unit test only
updated: "2026-06-21"           # Date the story file was last revised (ISO 8601)
---
```

### Status values

The lifecycle uses **eight** statuses. Only `done` stories are extracted to
`.feature` (strict mode); a story in any other status must never break CI
(local override: `extract_features --all`).

| Value | Meaning | BDD extraction |
|---|---|---|
| `proposed` | Written, **awaiting human validation** — the state a new story is born in. Nothing is implemented from it yet. | no |
| `todo` | Validated, not started | no |
| `in_progress` | Being implemented (open branch) | no |
| `done` | Implemented, tests green, merged | **yes** |
| `split` | Decomposed into sub-stories (`S006a`, `S006b`…). The file stays as framing and decision log; the children carry the implementation. | no |
| `to_extend` | Delivered and merged (`done`), but scoped follow-ups/fixes are pending; the file no longer matches the target (new criteria listed under a "To complete" section). | no |
| `deferred` | Scoped but postponed (priority or external dependency); stays visible in the backlog. | no |
| `archived` | Abandoned or obsolete — kept for history. | no |

`proposed` exists because the core rule is *propose the story and wait for human
validation*: without it, a story that has not been validated yet is indistinguishable
from one that has, and the wait the spec mandates cannot be represented.

`split` exists because a split parent has no honest state otherwise — `done` would
claim work that was never implemented, `archived` would bury a file that is still the
living frame for its children.

### Lifecycle

```
proposed ──► todo ──► in_progress ──► done
   │                                   │
   │                                   ├──► to_extend ──► in_progress ──► done
   │                                   │
   │                      deferred ◄───┘   (postpone)
   │                         │
   │                         └──► todo   (reactivation)
   │
   └──► split ──► (children S00Na, S00Nb… run their own cycle)

(any state) ──► archived
```

A story may also be split later, from `todo` or `in_progress`, when its size becomes
apparent during implementation.

### Optional module fields

Some modules add optional frontmatter fields (they live in the module, never in the
core block above):

| Field | Module | Meaning |
|---|---|---|
| `adr` | `adr` | List of ADR numbers governing this story, e.g. `adr: [1, 7]`. The story↔decision back-reference (the ADR lists `Related stories`). |
| `released_in` | `release-versioning` | The version/tag the story shipped in. |

When the `adr` module is enabled, **a story whose behaviour is shaped by a structural
decision must reference that ADR** via `adr: [...]` (or cite it under `## Notes`), so
the trace story → decision is never lost.

### Estimate values (T-shirt sizing)

`XS` · `S` · `M` · `L` · `XL`

`estimate` is a **planning** field, so it is **required only** where someone is about
to plan or do the work: `proposed`, `todo`, `in_progress`. On a story that is finished,
decomposed, abandoned or parked (`done`, `split`, `to_extend`, `deferred`, `archived`)
it is optional.

That is not a licence to skip it — it is a refusal to **reconstruct** it. Filling an
estimate after delivery produces a number that reads like a forecast nobody made; it
informs no one and it corrupts any later reading of how the project estimates. A
missing estimate on a delivered story is the honest record. (`released_in`, from the
`release-versioning` module, is optional for the same reason.)

The field stays **allowed on every status** and is validated wherever it appears: a
story parked in `deferred` with an estimate keeps it, and it becomes required again the
moment the story returns to `in_progress`.

---

## Sections

### `## User story` (required)

Classic role / need / value format:

> **As a** `<role>`, **I want** `<need>`, **so that** `<business value>`.

Language (EN/FR/other) is free; stay consistent within a project.

---

### `## Diagram` (recommended)

Mermaid (preferred) or PlantUML diagram.
Mermaid renders natively in GitHub and most IDEs — no plugin required.

| Context | Recommended type |
|---|---|
| API call flow (request → response) | `sequenceDiagram` |
| Algorithm or business decision | `flowchart TD` |
| Entity lifecycle | `stateDiagram-v2` |
| Relationships between entities | `erDiagram` |
| Class structure | `classDiagram` |

Omit if the story is trivial or purely technical.

---

### `## Technical description` (recommended)

3–10 lines specifying:
- Layers affected (e.g. Domain / Infrastructure / Presentation)
- Files or classes touched
- Architecture constraints imposed by the project

No pseudo-code. The developer decides the implementation.

---

### `## Acceptance Criteria` (required when `bdd: true`)

Gherkin embedded in markdown:

```markdown
## Acceptance Criteria

### Scenario: Descriptive title

* **Given** <context>
* **And** <additional context>
* **When** <action>
* **Then** <expected result>
* **And** <additional assertion>
```

Valid keywords: `Given` · `When` · `Then` · `And` · `But`

The parser (`extract_features.py`) recognises exactly this format.
Any other formatting (missing `**...**`, missing leading `* `) is silently ignored.

---

### `## Notes` (optional)

Deferred decisions, considered alternatives, cross-references to other stories.

---

## Generated `.feature` format

```gherkin
Feature: [S001] User registration

  Scenario: Successful registration
    Given no account exists with email `alice@example.com`
    When `POST /api/users` is sent with email and password
    Then the response status is 201
    And a confirmation email is sent
```

Feature files are **build artifacts**. Add them to `.gitignore`:

```
tests/features/*.feature
```

---

## Workflow

1. Pick the number (`next_story_id.py`) and create `stories/S<NNN>-<slug>.md` with
   `status: proposed`
2. Get the story validated, then move it to `status: todo` — no implementation before that
3. Check `depends_on` stories are `done`
4. If `bdd: true`: generate `.feature` → write step definitions → red
5. If `bdd: false`: write unit tests directly → red
6. Implement (green)
7. Refactor (still green)
8. Run quality checks
9. Single commit: `feat(S<NNN>): <short slug>`
10. Set `status: done`

**If a story grows beyond one effective day or 300 lines of production code:**
stop, propose a split into sub-stories (`S<NNN>a`, `S<NNN>b`), wait for validation,
then move the parent to `status: split`.
