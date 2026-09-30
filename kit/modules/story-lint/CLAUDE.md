# Module `story-lint` — CLAUDE fragment

> The story file is the spec; CI enforces it. `scripts/lint_stories.py` validates
> every story — the "third audience: CI" applied to the spec itself.

## Rule

A story must be **well-formed before it is implemented**. Run
`python3 scripts/lint_stories.py --stories-dir=stories` before moving a story to
`in_progress`, and in CI on every PR:

- filename `S<NNN>[<letter>]-<kebab-slug>.md`, with `id` matching the filename;
- required frontmatter complete (`id, title, epic, depends_on, status, bdd`);
- `estimate` **on `proposed` / `todo` / `in_progress` only** — it is a planning field,
  and reconstructing it on a delivered story would fabricate a forecast nobody made.
  It stays allowed, and validated, on every status;
- valid `status` (8-state lifecycle) and `estimate`;
- `bdd: true` ⇒ at least one scenario with steps under `## Acceptance Criteria`;
- `updated` present (warning), `depends_on` ids resolvable (warning), and a sub-story
  nested beyond one level — `S006a1` — flagged (warning).

Errors fail the run; `--strict` also fails on warnings. Fix lint errors before coding.

## Companion tool

`scripts/next_story_id.py` answers the other half of the question — *which number is
free* — across every git ref. The linter cannot catch a duplicate number living on
another branch; nothing purely local can. So the number is taken with that tool at
authoring time, not read off a hand-maintained list.
