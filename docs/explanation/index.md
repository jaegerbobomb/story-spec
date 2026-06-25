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

## Why agent-first

StorySpec is usable by a human team, but it is **designed for AI coding agents** —
that is where it pays off most.

An LLM agent, left to itself, will write code first and rationalize it later: skip
the spec, skip the failing test, never record why a structural choice was made,
forget the changelog and the docs. StorySpec removes that freedom. `SPEC.md` is the
*format* (the *what*); the `kit/` fragments are the **operating contract** — they are
loaded into the agent's `CLAUDE.md` (or copied into an `AGENTS.md`) and read on every
turn, so the agent is constrained to:

- propose a **story and wait for validation** before writing any feature code;
- write a **failing test first**, then make it pass (red → green);
- record an **ADR** for any structural decision, and reference it from the story;
- bump the **changelog/version** and update the **Diátaxis docs** on delivery.

The fragments are not documentation *about* a process — they are the *instructions
that enforce it*. The result is the same thing a senior reviewer would demand:
**quality work with end-to-end traceability** (story → ADR → test → commit →
changelog → docs), produced by an agent that would otherwise cut every corner. The
modular kit exists so each project loads exactly the obligations it wants and no
more.

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
