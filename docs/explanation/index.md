---
layout: page
title: Explanation
permalink: /explanation/
---

# Explanation — design & decisions

Background and rationale: *why* StorySpec is shaped the way it is. For step-by-step
help see the [tutorial](../tutorials/getting-started.md) or the
[how-to guides](../how-to/migrating-to-modular.md); for exact field rules see the
[reference](../reference/format.md).

## Why one file, three audiences

User stories capture the *who* and *why* but stay vague on the *what*. Use cases
capture the *what* but drift from the code. BDD feature files capture the *what* as
tests but are a chore to keep in sync. StorySpec collapses all three into one
markdown file, and generates the `.feature` from the acceptance criteria so the
story stays the single source of truth.

## Why a modular kit

StorySpec is distributed as a small mandatory **core** plus opt-in **modules**, so a
project ships only what it needs. The rationale and the alternatives considered are
recorded as Architecture Decision Records:

- [ADR-0001 — story-spec goes modular (core + opt-in modules)](../adr/0001-modular-story-spec.md)
- [ADR-0002 — composition via `@import` in CLAUDE.md](../adr/0002-claude-md-import-composition.md)

See the full [ADR index](../adr/).
