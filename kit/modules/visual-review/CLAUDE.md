# Module `visual-review` — CLAUDE fragment

> Automated visual review, kept in sync with delivered stories. Same principle as
> story ↔ `.feature`: a visual artifact stays synced to the story it documents.

## Rule

After each `done` story that touches the UI, make sure the project's screenshot
script — whatever tool it uses (Playwright, Cypress, Storybook snapshots, etc.) —
covers the views introduced or changed:

1. For each `done` story in the PR, identify the URLs / interactions involved.
2. Check that a capture call exists for each main view.
3. If not, add it to the script and commit it on the same branch before the final push.

Keeps the screenshot workflow in sync with the features and replayable for visual review.

## Frontmatter field added (optional)

`design` — the mockups or design references the story implements: URLs or repository
paths (`design: ["docs/design/timeline.png", "https://…"]`). A story that implements a
designed screen lists them; the implementer builds from the mockup, not from a
paraphrase, and the reviewer compares the screenshot against the same source.

## Acceptance criteria for UI stories

Gherkin describes behaviour, not pixels. For a UI story:

- **Name the condition that changes the layout** — window width, theme, empty state,
  error state — in the `Given`, with a number when it is a size:
  `* **Given** the window is 500 px wide`.
- **Assert what a user can observe and a test can query**: an element is visible or
  hidden, a control is enabled or disabled, a label reads a given text, a click leads
  to a given view. Not a colour, a margin or a font size.
- **Leave visual conformance to the screenshots** of this module, checked against the
  `design` references. A scenario that only a human eye can verify is not an
  acceptance criterion; say it in `## Notes` instead.

```markdown
### Scenario: The jump index hides on a narrow window

* **Given** a trip with five segments is open
* **And** the window is 500 px wide
* **Then** the jump index is not shown
* **And** the tabs are in a bar at the bottom of the window
```
