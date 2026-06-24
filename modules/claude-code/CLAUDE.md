# Module `claude-code` — CLAUDE fragment

> Claude Code integration: session bootstrap, story-spec agents and skills.

## Content installed by the module

- **`SessionStart` hook** (`.claude/hooks/session-start.sh`): prepares the environment in a
  remote session (dependency install, enabling project git hooks). Idempotent;
  only runs in a remote session (`CLAUDE_CODE_REMOTE`).
- **`.claude/settings.json`**: registers the hook + the attribution.
- **Agents**: `story-author`, `story-implementer`, `spec-guardian`.
- **Skills**: `release-bump` (+ `adr-new` if the `adr` module is active).

## Rule

Use the agents for the story-spec loop:
`story-author` (drafting + stop for validation) → `spec-guardian` (SPEC/ADR consistency) →
`story-implementer` (red→green→commit). The hook guarantees that a remote session can run
tests and linters right from startup.
