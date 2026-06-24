---
name: release-bump
description: >-
  Synchronise CHANGELOG, application version and README in A SINGLE commit when stories
  move to done or a completed batch of fixes is wrapped up. To be used at the time of the final commit of a
  story/batch. Provided by the release-versioning module. Triggers: "bump version", "move
  the story to done", "close the batch".
---

# release-bump

Ensures release discipline is respected **in the same commit** as the `done`.

## Steps

1. **Read the scheme** from `.story-spec/manifest.yaml` (`release-versioning` module):
   - version scheme (e.g. semver `MAJOR.MINOR.PATCH`, or project variant);
   - location of the version (`.env` `APP_VERSION`, `package.json`, `composer.json`…).
2. **CHANGELOG**: convert `## [Unreleased]` into the target version (or add the entry there), classified
   `Added` / `Changed` / `Fixed`; add the comparison link at the bottom of the file.
3. **Application version**: update the declared location.
4. **README**: add/update the story line in the "User stories" table.
5. **A single commit** grouping: story `status: done` + CHANGELOG + version + README.

## Guardrails

- **Never** commit a completed batch leaving `[Unreleased]` unversioned if the project's scheme
  requires it.
- Do not invent the number: if the bump trigger (milestone/batch) is ambiguous, ask the question.
- Respect the existing CHANGELOG format (Keep a Changelog by default).
