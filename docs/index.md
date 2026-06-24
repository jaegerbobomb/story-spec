---
layout: home
---

# StorySpec

**Write the story once. Run it as a test. Compose the rest as modules.**

User stories as living specifications - one markdown file, three audiences:
product owner, developer, CI pipeline.

---

## How it works

A StorySpec file is a standard markdown file with a YAML frontmatter header
and a `## Acceptance Criteria` section written in Gherkin:

~~~markdown
---
id: S001
title: "User registration"
epic: auth
status: done
estimate: S
bdd: true
updated: "2026-06-21"
---

## User story

> As a **visitor**, I want to **create an account**
> so that I can **access the application**.

## Acceptance Criteria

### Scenario: Successful registration

* **Given** no account exists with email `alice@example.com`
* **When** `POST /api/users` is sent with email and password
* **Then** the response status is 201
~~~

Running `python3 scripts/extract_features.py` generates:

~~~gherkin
Feature: [S001] User registration

  Scenario: Successful registration
    Given no account exists with email `alice@example.com`
    When `POST /api/users` is sent with email and password
    Then the response status is 201
~~~

The `.feature` file is a build artifact - gitignored.
The markdown story is the single source of truth.

---

## Documentation

This documentation follows the [Diátaxis](https://diataxis.fr) framework — four
modes, each serving a different need:

| Mode | When you want to… | Start here |
|---|---|---|
| **Tutorial** | learn by doing, step by step | [Getting started](tutorials/getting-started.md) |
| **How-to** | accomplish a specific task | [Migrating to the modular kit](how-to/migrating-to-modular.md) |
| **Reference** | look up exact details | [Format reference](reference/format.md) · [Full spec](https://github.com/jaegerbobomb/story-spec/blob/main/SPEC.md) |
| **Explanation** | understand the why | [Design & decisions](explanation/) |

→ [Story status](status.md)
→ [GitHub repository](https://github.com/jaegerbobomb/story-spec)
