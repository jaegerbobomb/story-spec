#!/usr/bin/env bash
# story-spec init — scaffolds a project from the core + the manifest's modules.
#
# Usage:
#   story-spec init                 # reads .story-spec/manifest.yaml, writes the files
#   story-spec init --dry-run       # shows what would be done without writing anything
#   story-spec init --sync          # recompose only CLAUDE.md (after editing the manifest)
#   story-spec init --check         # checks module autonomy (lint only, for CI)
#
# Reference implementation in POSIX-ish bash; a Python/Node port is planned (parity with
# the extractors). Depends on `yq` to read the YAML (fallback: minimal parsing).
set -euo pipefail

ROOT="${STORY_SPEC_ROOT:-$(pwd)}"
# Source kit ("dist"). Resolution order:
#   1. $STORY_SPEC_DIST if set
#   2. a vendored kit at $ROOT/.story-spec/dist (installed projects)
#   3. the kit/ catalog in the story-spec repo this script lives in
if [ -n "${STORY_SPEC_DIST:-}" ]; then
  DIST="$STORY_SPEC_DIST"
elif [ -d "$ROOT/.story-spec/dist/core" ]; then
  DIST="$ROOT/.story-spec/dist"
else
  DIST="$(cd "$(dirname "$0")/.." && pwd)/kit"
fi
MANIFEST="$ROOT/.story-spec/manifest.yaml"
DRY=0; SYNC=0; CHECK=0
for a in "$@"; do
  case "$a" in
    --dry-run) DRY=1 ;;
    --sync)    SYNC=1 ;;
    --check)   CHECK=1 ;;
    *) echo "unknown option: $a" >&2; exit 2 ;;
  esac
done

say() { echo "story-spec: $*"; }

# Module autonomy contract (ADR-0002): a module fragment must NEVER
# import another fragment via @import — otherwise the "copy for AGENTS" path breaks.
# Only CLAUDE.dist.md aggregates the modules. We forbid any @import line in modules/ and core/.
check_module_autonomy() { # kit_root -> 0 if ok, 1 otherwise
  local base="$1" found=0 hit
  # Claude Code @import form: a line whose 1st token is @<path> (contains a /).
  hit="$(grep -rnE '^[[:space:]]*@[^[:space:]]*/' "$base/modules" "$base/core" 2>/dev/null || true)"
  if [ -n "$hit" ]; then
    echo "story-spec: ERROR — @import forbidden in a module/core fragment (ADR-0002):" >&2
    echo "$hit" >&2
    echo "story-spec: each module must stay autonomous; only CLAUDE.dist.md aggregates." >&2
    found=1
  fi
  return $found
}

if [ "$CHECK" = 1 ]; then
  check_module_autonomy "$DIST" && say "module autonomy: OK"
  exit $?
fi
do_cp() { # src dst
  if [ "$DRY" = 1 ]; then echo "  + $2"; else mkdir -p "$(dirname "$2")"; [ -e "$2" ] || cp "$1" "$2"; fi
}

[ -f "$MANIFEST" ] || { say "manifest missing: $MANIFEST (copy manifest.example.yaml to get started)"; exit 1; }

read_list() { # yaml key -> lignes
  yq -r ".$1[]? // empty" "$MANIFEST" 2>/dev/null || true
}

MODULES="$(read_list modules)"
AGENTS="$(read_list agents)"
SKILLS="$(read_list skills)"
ADAPTER="$(yq -r '.test_adapter // "none"' "$MANIFEST" 2>/dev/null || echo none)"

say "test adapter: $ADAPTER"
say "modules: $(echo "$MODULES" | tr '\n' ' ')"

# 1) Core
do_cp "$DIST/core/CLAUDE.core.md" "$ROOT/.story-spec/core/CLAUDE.core.md"
if [ "$SYNC" = 0 ]; then
  do_cp "$DIST/templates/story.md" "$ROOT/stories/_TEMPLATE.md" 2>/dev/null || true
fi

# 2) Modules (CLAUDE fragment + SPEC section + templates + module-specific skills)
for m in $MODULES; do
  do_cp "$DIST/modules/$m/CLAUDE.md" "$ROOT/.story-spec/modules/$m/CLAUDE.md"
  [ -f "$DIST/modules/$m/SPEC.section.md" ] && do_cp "$DIST/modules/$m/SPEC.section.md" "$ROOT/.story-spec/modules/$m/SPEC.section.md"
  if [ -d "$DIST/modules/$m/templates" ]; then
    for t in "$DIST/modules/$m/templates"/*; do do_cp "$t" "$ROOT/.story-spec/modules/$m/templates/$(basename "$t")"; done
  fi
  if [ -d "$DIST/modules/$m/skills" ]; then
    for s in "$DIST/modules/$m/skills"/*; do do_cp "$s/SKILL.md" "$ROOT/.claude/skills/$(basename "$s")/SKILL.md"; done
  fi
done

# 3) Agents & skills listed at project level
for a in $AGENTS; do do_cp "$DIST/agents/$a.md" "$ROOT/.claude/agents/$a.md"; done
for s in $SKILLS; do do_cp "$DIST/skills/$s/SKILL.md" "$ROOT/.claude/skills/$s/SKILL.md"; done

# 4) Composition of CLAUDE.md (@import block generated between the markers)
check_module_autonomy "$DIST" || exit 1
say "(re)generates CLAUDE.md from the manifest"
if [ "$DRY" = 0 ]; then
  BLOCK="$(for m in $MODULES; do echo "@.story-spec/modules/$m/CLAUDE.md"; done)"
  export BLOCK
  awk '
    /<!-- BEGIN story-spec:modules/ {print; print ENVIRON["BLOCK"]; skip=1; next}
    /<!-- END story-spec:modules/   {skip=0}
    skip!=1 {print}
  ' "$DIST/CLAUDE.dist.md" > "$ROOT/CLAUDE.md.tmp" && mv "$ROOT/CLAUDE.md.tmp" "$ROOT/CLAUDE.md"
fi

if [ "$DRY" = 1 ]; then say "done. (dry-run)"; else say "done."; fi
