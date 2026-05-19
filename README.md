# StorySpec

**Write the story once. Run it as a test.**

User stories as living specifications - one markdown file, three audiences:
product owner, developer, CI pipeline.

→ [Full specification](SPEC.md)
→ [Getting started](docs/getting-started.md)
→ [Examples](examples/)

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

## Quick start

```bash
# 1. Copy the templates into your project
cp templates/stories-README.md yourproject/stories/README.md
cp templates/story.md yourproject/stories/S001-your-first-story.md
cp scripts/extract_features.py yourproject/scripts/

# 2. Write the story, fill in the Acceptance Criteria

# 3. Generate .feature files before running your BDD suite
python3 scripts/extract_features.py

# 4. Run Behat / Cucumber as usual
```

## Scripts

| Script | Language | Purpose |
|---|---|---|
| `scripts/extract_features.py` | Python 3 (stdlib) | Story → `.feature` generator |
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
