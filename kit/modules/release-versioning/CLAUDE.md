# Module `release-versioning` — CLAUDE fragment

> Versioning discipline. The **scheme** is project-defined (SemVer, CalVer, or
> mirrored on an external milestone); the **mechanics** are universal. See the
> `release-bump` skill.

## Rule

On every `done` story (or completed batch of fixes), in the **same commit**:

1. **CHANGELOG** — `## [Unreleased]` → target version, `Added`/`Changed`/`Fixed`
   sections + a comparison link at the bottom (Keep a Changelog format).
2. **Application version** — update the location declared in the manifest
   (`VERSION` file, `APP_VERSION` in `.env`, `package.json`, etc.).
3. **README** — the story's row in the "User stories" table.

Never merge a completed batch leaving `[Unreleased]` unversioned when the scheme
requires it. Delegate to the **`release-bump`** skill.

## Frontmatter field added (optional)

`released_in` — the version (or tag) the story shipped in, so the CHANGELOG and the
story files can cross-reference each other. Any project-specific milestone fields
stay in the project layer, never in the core frontmatter.
