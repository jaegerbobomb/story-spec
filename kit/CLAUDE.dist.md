# CLAUDE.md — operational conventions (composed by story-spec)

> ⚙️ **File composed** by `story-spec init` from the core + the modules declared in
> `.story-spec/manifest.yaml`. Do not edit the `@import` blocks by hand: re-run
> `story-spec init --sync` after changing the manifest. **Project-specific** content
> (stack, commands, house rules) goes under "Project-specific".

## Core

@.story-spec/core/CLAUDE.core.md

## Enabled modules

<!-- BEGIN story-spec:modules (generated) -->
@.story-spec/modules/adr/CLAUDE.md
@.story-spec/modules/github-piloting/CLAUDE.md
@.story-spec/modules/release-versioning/CLAUDE.md
@.story-spec/modules/claude-code/CLAUDE.md
<!-- END story-spec:modules -->

## Project-specific

<!-- Everything that does not come from story-spec: stack, versions, make commands, house rules. -->

- **Stack**: <to fill in>
- **Commands**: `<lint>`, `<static analysis>`, `<tests>`
- **Quality check before commit**: `<quality_check>`
