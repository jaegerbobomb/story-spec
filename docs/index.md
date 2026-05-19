---
layout: home
---

# StorySpec

**Write the story once. Run it as a test.**

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

## Get started

→ [Getting started guide](getting-started.md)
→ [Format reference](format.md)
→ [Story status](status.md)
→ [GitHub repository](https://github.com/jaegerbobomb/story-spec)
