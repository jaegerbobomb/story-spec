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
