---
layout: page
title: Format reference
permalink: /format/
---

# Format reference

## File naming

```
stories/S<NNN>-<slug>.md
```

| Part | Rule |
|---|---|
| `S<NNN>` | Sequential integer, zero-padded to 3 digits. Never reused, even after deletion. |
| `<letter>` | Optional sub-story marker (`S006a`) — reuses the parent's number |
| `<slug>` | kebab-case, ≤ 5 words (`user-registration`, not `registration`) |

The next free number comes from the tool, which reads every git ref — a story being
written on another branch already owns its number:

```bash
git fetch --all --prune && python3 scripts/next_story_id.py --verbose
```

## Frontmatter

```yaml
---
id: S006
title: "Short title"
epic: auth
depends_on: [S001, S002]
status: proposed
estimate: M
bdd: true
---
```

| Field | Required | Values |
|---|---|---|
| `id` | Yes | `S` + 3 digits, optionally + a sub-story letter |
| `title` | Yes | String, ≤ 8 words |
| `epic` | Yes | one word or kebab-case |
| `depends_on` | Yes | Array of IDs, or `[]` |
| `status` | Yes | `proposed` · `todo` · `in_progress` · `done` · `split` · `to_extend` · `deferred` · `archived` |
| `estimate` | On `proposed` / `todo` / `in_progress` | `XS` · `S` · `M` · `L` · `XL` |
| `bdd` | Yes | `true` · `false` |

`estimate` is a **planning** field: required where the work is about to be planned or
done, optional once the story is finished, decomposed, abandoned or parked. Filling it
after delivery would reconstruct a forecast nobody made. It remains allowed — and
validated — on every status.

## Sections

### `## User story`

```markdown
> **As a** `<role>`, **I want** `<need>`, **so that** `<business value>`.
```

### `## Diagram` *(optional)*

Mermaid is preferred - it renders natively in GitHub and most IDEs.

| Context | Type |
|---|---|
| API call flow | `sequenceDiagram` |
| Algorithm / decision | `flowchart TD` |
| Entity lifecycle | `stateDiagram-v2` |
| Entity relationships | `erDiagram` |
| Class structure | `classDiagram` |

### `## Technical description` *(optional)*

3–10 lines: layers affected, files/classes touched, architecture constraints.
No pseudo-code.

### `## Acceptance Criteria`

Required when `bdd: true`.

```markdown
### Scenario: Descriptive title

* **Given** <context>
* **And** <additional context>
* **When** <action>
* **Then** <expected result>
* **And** <additional assertion>
```

Valid keywords: `Given` · `When` · `Then` · `And` · `But`

The parser recognises exactly `* **Keyword** text`.
Any other formatting is silently ignored.

### `## Notes` *(optional)*

Deferred decisions, alternatives, cross-references.

## Generated `.feature`

```gherkin
Feature: [S001] User registration

  Scenario: Successful registration
    Given no account exists with email `alice@example.com`
    When `POST /api/users` is sent with email and password
    Then the response status is 201
    And a confirmation email is sent
```
