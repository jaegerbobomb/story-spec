# ADR-0004 — sub-stories, `proposed`/`split`, and a computed story number

- **Status**: accepted
- **Date**: 2026-09-28
- **Deciders**: story-spec maintainer
- **Related to**: ADR-0001 (modular mechanics)

## Context

Three gaps surfaced from a consumer project (Didascale, 291 story files) running the
v0.2.0 kit. Each is a place where the spec asks for something it cannot express.

**1. The spec prescribes splitting into `S<NNN>a` but forbids the name.**
`kit/core/CLAUDE.core.md` and `kit/agents/story-author.md` both instruct the agent to
propose `S<NNN>a` / `S<NNN>b` when a story is too big. Yet `SPEC.md`'s naming table
says three digits and nothing else, and `lint_stories.py` enforces `^S\d{3}$`. The kit
tells you to do something its own linter rejects. Measured on that consumer: **114 of
291 files** fail, on the filename and the `id`, for doing exactly what core says.

**2. A split parent has no honest status.** Once the children carry the work, the
parent is neither `done` (nothing was implemented from it) nor `archived` (it is still
the living frame and the decision log for its children) nor `todo` (it will never be
picked up). Consumers invent a value; that consumer had 25 files on an invented one.

**3. The core rule mandates a wait the format cannot represent.** "Propose the story
and **wait for human validation**" is the first rule of core. But the only entry state
is `todo`, which also means *validated, not started*. A story awaiting a human is
indistinguishable from one cleared to start — so the gate exists in prose only. Same
consumer: 23 files on an invented `proposed`.

**4. The number is picked from the wrong place.** `story-author.md` said: "next free
`S<NNN>` in `stories/`" — the working tree. A story being authored on another branch
already owns its number and is invisible there. Two sessions working the same day pick
the same number; it happened, and was only caught by hand. The mitigation people reach
for — a "reserved ids" table in `stories/README.md` — is worse: it drifts the moment
nobody updates it (that consumer's table announced a number as free while a `done`
story already carried it), and it still cannot see branches, so it never catches the
collision it exists to prevent.

While verifying the above, three v0.1.0 drifts also turned up: the statuses went 4 → 6
in v0.1.0 but `kit/templates/stories-README.md`, `docs/reference/format.md`,
`scripts/generate_report.py` and `scripts/stories_status.sh` were never updated —
`generate_report.py` silently **excluded** `to_extend` and `deferred` stories from its
denominator, so the advertised completion percentage was wrong for any project using
the full lifecycle.

## Decision

**Sub-stories are part of the grammar.** `S<NNN>` may be followed by one lowercase
letter. The letter consumes no new number: `S006` and `S006a` are one number, one of
them decomposed. `SPEC.md`, `docs/reference/format.md` and `lint_stories.py` agree with
core. A second level (`S006a1`) parses but warns — it usually means the parent was
split too coarsely.

**Two statuses are added, taking the lifecycle to eight.**

- `proposed` — written, awaiting human validation. The state a story is **born** in;
  validation moves it to `todo`. The template and `story-author` now emit it.
- `split` — decomposed into sub-stories. The file stays as framing and decision log.

**The number is computed, not reserved.** New `scripts/next_story_id.py` reads the
story files of every git ref (`git ls-tree` over `refs/heads` and `refs/remotes`, no
network) and prints the next free number, naming which ref holds which. Core,
`story-author` and the `stories/README.md` template point at it and say, explicitly,
not to keep a hand-written reserved list. `story-author` gains the `Bash` tool so it
can run it, with a documented fallback of asking the operator.

**The drifts are fixed in the same change**, since they are the same failure mode: a
statement about the lifecycle that no longer matches the lifecycle.

## Consequences

**Additive for existing data.** No story file that was valid under v0.2.0 becomes
invalid: the id grammar is relaxed, never tightened, and the two statuses extend an
enum. Hence **0.3.0** (MINOR), not a major.

**One behavioural change to notice.** A story authored by the updated kit is born
`proposed`, not `todo`. A consumer whose own tooling switches on status, or whose CI
asserts that a new story is `todo`, must learn the value. That is the reason this is a
`Changed` entry in the changelog and not only `Added`.

**Consumers upgrade at their own pace**, but an old vendored linter rejects `proposed`
/ `split` / `S006a`. The two halves must move together: a project that adopts the new
statuses must also take the new `lint_stories.py`. The changelog's upgrade notes say
so.

**The nesting warning is a judgement, not a rule.** `S006a1` stays legal because a
consumer already had two, and breaking their files to make a point would contradict
the additive principle above. The warning states the opinion without enforcing it.

## Alternatives considered

- **Leave sub-stories out and forbid the split naming.** Rejected: core's size rule is
  one of its most-used instructions, and the split is genuinely how a large story gets
  handled. The inconsistency was in the linter, not in the practice.
- **A separate `parent`/`children` frontmatter field instead of the letter.** Rejected:
  it duplicates in metadata what the id already says, and it would make the id grammar
  a lie on the 114 files that already use the letter.
- **A `validated: true/false` flag instead of `proposed`.** Rejected: two orthogonal
  fields to express one position in a lifecycle. The lifecycle already has a name for
  that — a status.
- **Keep the reserved-ids table but generate it.** Rejected: a generated snapshot of a
  moving set is stale the moment a branch is pushed. The question "which number is
  free" has no correct answer at rest, only at the moment it is asked.
