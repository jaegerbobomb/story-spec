# StorySpec — Format Specification

## File naming

Each story is a markdown file named `S<NNN>-<slug>.md` (e.g. `S006-user-login.md`),
placed in a `stories/` directory at the root of the project.

| Part | Rule |
|---|---|
| `S<NNN>` | Sequential integer, zero-padded to 3 digits, never reused |
| `<slug>` | kebab-case, ≤ 5 words, descriptive |

---

## Frontmatter (required)

```yaml
---
id: S006                        # Unique identifier, never reused
title: "Short title"            # Human-readable, ≤ 8 words
epic: auth                      # Logical group (one word or kebab-case)
depends_on: [S001, S002]        # Prerequisite stories (empty array if none)
status: todo                    # See status values below
estimate: M                     # See estimate values below
bdd: true                       # true → generates a .feature | false → unit test only
---
```

### Status values

| Value | Meaning |
|---|---|
| `todo` | Not started |
| `in_progress` | Being implemented (open branch) |
| `done` | Implemented, tests green, merged |
| `archived` | Abandoned or obsolete — kept for history |

### Estimate values (T-shirt sizing)

`XS` · `S` · `M` · `L` · `XL`

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

1. Create `stories/S<NNN>-<slug>.md` with `status: todo`
2. Get the story validated before starting implementation
3. Check `depends_on` stories are `done`
4. If `bdd: true`: generate `.feature` → write step definitions → red
5. If `bdd: false`: write unit tests directly → red
6. Implement (green)
7. Refactor (still green)
8. Run quality checks
9. Single commit: `feat(S<NNN>): <short slug>`
10. Set `status: done`

**If a story grows beyond one effective day or 300 lines of production code:**
stop, propose a split into sub-stories, wait for validation.
