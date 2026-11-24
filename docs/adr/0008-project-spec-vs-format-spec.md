---
title: "ADR-0008 — project spec vs format spec"
parent: Architecture decisions
nav_order: 8
---
# ADR-0008 — The project's `SPEC.md` is scaffolded, and is not the format spec

- **Status**: proposed
- **Date**: 2026-11-24
- **Deciders**: story-spec maintainer
- **Related to**: ADR-0001 (modular kit), ADR-0003 (kit layout)

## Context

`SPEC.md` means two different things in the kit, and nothing says which is meant where.

- In this repository, `SPEC.md` is the **story format**.
- In a consumer project, the agents read `SPEC.md` as the **project spec**:
  `spec-guardian` checks "the architecture (layers, bounded contexts, conventions, API
  boundaries) described in `SPEC.md`"; `story-implementer` stops when "the story
  contradicts `SPEC.md`"; the `adr` module's SPEC section says "`SPEC.md` describes the
  current state". `story-author`, meanwhile, reads `SPEC.md` *and* `stories/README.md`
  as context, which reads like the format.

And in a project set up with `init.sh`, there is **no `SPEC.md` at all**: the README
says `init` composes "the SPEC", but `init.sh` only copies each module's
`SPEC.section.md` under `.story-spec/modules/` — where nothing reads it — and never
creates the file the agents are told to defer to. `stories/README.md`, which
`story-author` also reads, is not created either.

The result, met while setting up a new project: an agent told "SPEC.md wins" has no
SPEC.md to read, and a human reading the kit's docs cannot tell which of the two files
a sentence refers to.

## Decision

1. **Name the two.** StorySpec's `SPEC.md` is the *format spec*. A project's `SPEC.md`
   is the *project spec*: architecture, conventions, external contracts of that
   application. The agents and docs say "the project spec `SPEC.md`" where they mean
   the latter, and point to `stories/README.md` for the format.
2. **Scaffold it.** `init.sh` creates `SPEC.md` from `kit/templates/SPEC.project.md`
   when it does not exist, and `stories/README.md` from the existing
   `stories-README.md` template. Neither is ever overwritten.
3. **Inline the module sections.** Between `<!-- BEGIN/END story-spec:spec-sections -->`
   markers, `init.sh` writes the `SPEC.section.md` of every enabled module, on every run
   including `--sync`. Inlined rather than `@import`ed: `SPEC.md` is read by humans as
   much as by agents, and a human does not follow `@` lines. A `SPEC.md` without the
   markers is the project's own and is left untouched.

No file is renamed: renaming either `SPEC.md` would break every consumer's links for a
problem that naming and scaffolding solve.

## Consequences

**Positive**
- "SPEC.md wins" now points to a file that exists, from the first `init`.
- Module SPEC sections (`adr`, and any future module) reach the place they were written
  for.
- Existing projects are untouched: their `SPEC.md` has no markers, so `init` leaves it
  alone and says so. Adding the two marker lines opts them in.

**Costs / risks**
- `init` now writes two more files on a fresh project. Both are templates to fill, not
  content to maintain.
- The generated block in `SPEC.md` must not be edited by hand, like the one in
  `CLAUDE.md`; the opening marker says so.

## Rejected alternatives

- **Rename the kit's `SPEC.md` to `FORMAT.md`**: breaks links in every consumer and in
  published docs; the ambiguity is in the agents' wording, not in the kit's file name.
- **Rename the project file to `ARCHITECTURE.md`**: same breakage on the consumer side,
  and `SPEC.md` is the name existing projects already use.
- **`@import` the module sections**: works for agents, not for the human reader the
  project spec is also for.
