# StorySpec — CLAUDE.md snippet

This file is a distributable template for projects using StorySpec.
Copy the relevant sections into your project's `CLAUDE.md`.

---

## User stories

See `stories/README.md` for the full story format and workflow.

**Absolute rule**: always propose a story file (`stories/S<NNN>-<slug>.md`)
and wait for human validation before starting any feature development.
The only exceptions are urgent bug fixes and minor refactors with no
functional impact.

### Story workflow (per story)

1. Read the full story file: `stories/S<NNN>-*.md`.
2. Check `depends_on` — if any listed story is not `done`, flag it before starting.
3. Propose a short plan (5–10 lines: classes to create/modify, layers affected).
4. **Tests first:**
   - If `bdd: true`: run `<extract-features-command>` to generate the `.feature` file,
     write step definitions → red.
   - If `bdd: false`: write unit/integration tests directly → red.
5. Implement (green). Refactor if needed (still green).
6. Run quality checks (linter, static analysis).
7. Single commit: `feat(S<NNN>): <short slug>`.
8. Set the story `status` to `done`.

**Stop and split** if the story exceeds one effective day or 300 lines of
production code. Propose sub-stories (e.g. `S006a`, `S006b`) and wait
for validation before continuing.

**When a story is ambiguous**: ask before coding. Never guess silently.
Add the answer to the story's `## Notes` section.

### Commands

Adapt these to your project's toolchain:

```bash
# Generate .feature files from stories with `bdd: true`
<extract-features-command>
# e.g. python3 scripts/extract_features.py
# e.g. make extract-features

# Run BDD acceptance tests (includes feature generation)
<bdd-test-command>
# e.g. make behat
# e.g. npx cucumber-js

# Print the story status dashboard
<stories-status-command>
# e.g. bash scripts/stories_status.sh
# e.g. make stories-status
```

### Commit scope

Use the story ID as the commit scope:

```
feat(S007): add program cycle prescription
fix(S012): handle missing patient in enrollment flow
test(S003): cover edge case in registration validator
```

For non-story commits, use the component name as scope:

```
fix(ci): pin Node.js version to 22
chore(deps): update prettier to 3.x
```
