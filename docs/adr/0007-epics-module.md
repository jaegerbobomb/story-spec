---
title: "ADR-0007 — epics module"
parent: Architecture decisions
nav_order: 7
---
# ADR-0007 — An `epics` module for the layer above the stories

- **Status**: proposed
- **Date**: 2026-11-24
- **Deciders**: story-spec maintainer
- **Related to**: ADR-0001 (modular kit), ADR-0002 (module autonomy)

## Context

A story says *what* to build and *how we know it works*. Nothing in the kit says *why a
group of stories exists*, *in which order the groups come*, or *when a group is
finished*.

`epic:` is a required field, but it is only a label: a string nobody defines. The
information that should sit behind it lives elsewhere, or nowhere:

- with the `github-piloting` module, in an `[Epic]` issue — outside the repository, so
  an agent without GitHub access, an offline reader, or a fork does not see it;
- without it, in a planning document next to the repository (a doc, a wiki page), which
  drifts from `stories/` the day it is written;
- or only in the head of the person who wrote the stories.

This was met while turning a project plan into StorySpec (a desktop/mobile travel app,
eight phases). Each phase had a goal, a place in the order, and a "finished when"
condition — for example *a ticket imported on Linux shows up on Android with its PDF*.
That condition belongs to no single story: it is reached by several, and it is exactly
what tells a reader whether the phase is over. The format had nowhere to put it.

Issue #7 asks for a `## Plan` section **inside** a story (the design between the story
and the code). This ADR is about the level **above** the stories; the two do not
overlap.

## Decision

We add an opt-in module **`epics`**:

1. Every value used in `epic:` has a file `epics/<epic>.md`.
2. The file carries a small frontmatter — `id` (= file name), `title`, `order`,
   `status` (`planned | active | done | dropped`), `updated` — and two required
   sections: `## Goal` and `## Exit criteria` (a checklist). `## Out of scope` and
   `## Notes` are optional.
3. The epic file **does not list its stories**. The list is whatever `stories/` says has
   that `epic:` — a second list would drift.
4. `lint_stories.py --epics-dir=epics` checks that every story's epic has a file and
   that each epic file is well-formed. Without the flag nothing changes.
5. The module's CLAUDE fragment tells the agent to read the epic before authoring a
   story, to propose a new epic together with its first story, to pick the next story
   from the active epic with the lowest `order`, and to check the exit criteria when the
   last story of an epic is `done`.

## Consequences

**Positive**
- The roadmap lives in the repository, next to the stories, under review like them.
- An agent starting a session from the repository alone knows the order of work and
  when a group is finished, without GitHub.
- A human reader gets a short page per epic instead of reconstructing intent from a
  dozen stories.
- No impact on projects that do not enable the module: the linter flag is opt-in and
  the core is untouched.

**Costs / risks**
- One more file per epic to keep up to date. The cost is bounded: the file does not
  list stories, so it changes when the goal or the exit criteria change, not on every
  story.
- `status` of an epic is set by hand. It could be derived from its stories, but
  "every story is `done`" is not "every exit criterion is met" — the gap between the
  two is precisely the missing story the module wants to surface.

## Rejected alternatives

- **An epic table in `stories/README.md`**: one file for every epic means one file
  touched by every epic change — the same aggregate-file conflicts issue #7 measures
  on `CHANGELOG.md`. It also leaves no room for exit criteria.
- **Epic fields in each story** (`epic_goal:`…): repeats the same text in every story
  of the epic, and drifts.
- **Leave it to `github-piloting`**: keeps the information outside the repository,
  which is the problem.

## Follow-up

- [ ] `stories_status.sh` / `generate_report.py`: group by epic in `order`, show each
      epic's exit criteria progress.
