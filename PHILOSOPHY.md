# StorySpec - Philosophy

## The core problem

In software projects, three artefacts describe the same behaviour at three levels of detail:

1. **The user story** (agile card) - *who* and *why*, but vague on *what*
2. **The use case** (specification) - *what* in detail, but disconnected from code
3. **The BDD test** (`.feature`) - *what* as executable code, but technical and redundant

Keeping the three consistent is expensive. In practice only one survives:
usually the test file, which ends up being the only real documentation -
but unreadable by a non-developer.

## The central intuition

A user story with well-written acceptance criteria *is already* a use case.
Criteria written in Given/When/Then *are already* Gherkin.

All it takes is a minimal parser to transform one into the other.

The story file then becomes:
- readable by a product owner (the markdown)
- useful to a developer (the diagram, the technical description)
- consumable by CI (the criteria extracted to `.feature`)

## Lineage

This method builds on:

- **Dan North** : ["Introducing BDD"](https://dannorth.net/introducing-bdd/) (2006):
  first to articulate explicitly that a story's acceptance criteria *are* its test
  scenarios, and to propose Given/When/Then as a shared language between
  business and engineering.

- **Gojko Adzic** : *Specification by Example* (2011): the executable specification
  as a single source of truth, living close to the code.

- **Tony Heap** : ["An Agile Functional Specification"](https://www.its-all-design.com/an-agile-functional-specification/)
  (its-all-design.com): showed how user stories, use cases, and acceptance criteria can
  be a single artefact rather than three separate documents. Heap treats acceptance criteria
  written as "when I do X, the system does Y" as both the functional specification *and*
  the basis for automated tests - the direct intuition behind StorySpec's embedded Gherkin.

## What StorySpec adds

- **YAML frontmatter** brings project management metadata (status, estimate,
  dependencies, epic) directly into the story file - machine-readable, version-controlled.
- **Mermaid diagrams** stay co-located with the story and render natively in GitHub
  without any external tooling.
- **Automatic extraction** makes `.feature` files build artifacts (gitignored),
  not files to maintain by hand.
- Everything lives in the **Git repository** alongside the code it describes,
  subject to the same review and versioning rules.
