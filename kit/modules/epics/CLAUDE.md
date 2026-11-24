# Module `epics` — CLAUDE fragment

> Activated by `modules: [epics]`. The layer above the stories: **why** a group of
> stories exists, **in which order** the groups come, and **when** a group is finished.

## Rule

Every value used in a story's `epic:` field has a file `epics/<epic>.md` (format in the
`epics` section of the SPEC, template in
`.story-spec/modules/epics/templates/epic.md`). The epic
file holds what no single story can hold:

- the **goal** of the group, in two or three sentences;
- its **order** among the other epics (`order:` in the frontmatter);
- its **exit criteria**: the observable conditions under which the epic is finished,
  as a checklist.

The epic file never repeats the stories: the list of stories is whatever `stories/`
says has `epic: <epic>`. Duplicating it would drift.

## When you work with stories

1. **Before authoring a story**, read its epic file. A story that serves none of the
   epic's goal belongs to another epic — or to a new one, proposed like a story.
2. **New epic** = new file `epics/<epic>.md` with `status: planned`, proposed to the
   human in the same message as its first story. The validation of the story does not
   validate a new epic implicitly: say that both need a yes.
3. **Before picking the next story**, take the active epic with the lowest `order`.
4. **When the last story of an epic moves to `done`**, check the exit criteria one by
   one, tick the ones met, and report the others. Move the epic to `done` only when
   every criterion is ticked; otherwise say what is missing — usually a story nobody
   wrote yet.

## Lint

With this module, run the linter with the epics directory so that a story pointing to
an epic without a file fails:

```bash
python3 scripts/lint_stories.py --stories-dir=stories --epics-dir=epics
```
