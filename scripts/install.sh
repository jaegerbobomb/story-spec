#!/usr/bin/env bash
# story-spec install — vendor the kit into the CURRENT repository and bootstrap it.
#
# From your project root:
#   curl -fsSL https://raw.githubusercontent.com/jaegerbobomb/story-spec/main/scripts/install.sh | bash
#
# Pin a version, or skip the initial compose:
#   curl -fsSL .../install.sh | STORY_SPEC_REF=v0.1.0 bash
#   curl -fsSL .../install.sh | STORY_SPEC_NO_INIT=1 bash
#
# What it does (idempotent):
#   1. downloads the kit tarball for $STORY_SPEC_REF
#   2. vendors the full catalog under .story-spec/dist/
#   3. copies the runtime scripts into scripts/
#   4. creates .story-spec/manifest.yaml from the example (if absent)
#   5. runs `scripts/init.sh` to compose CLAUDE.md (unless STORY_SPEC_NO_INIT=1)
set -euo pipefail

REPO="${STORY_SPEC_REPO:-jaegerbobomb/story-spec}"
REF="${STORY_SPEC_REF:-main}"
ROOT="${STORY_SPEC_ROOT:-$(pwd)}"
DIST="$ROOT/.story-spec/dist"

say()  { echo "story-spec: $*"; }
fail() { echo "story-spec: $*" >&2; exit 1; }

command -v curl >/dev/null || fail "curl is required"
command -v tar  >/dev/null || fail "tar is required"

tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT

say "downloading $REPO@$REF"
curl -fsSL "https://codeload.github.com/$REPO/tar.gz/$REF" | tar -xz -C "$tmp" \
  || fail "download failed (check the repo/ref or your network)"
src="$(find "$tmp" -mindepth 1 -maxdepth 1 -type d | head -n1)"
[ -d "$src/core" ] || fail "unexpected archive layout"

# 1) Vendor the full catalog (source of truth for init's DIST auto-detection).
say "vendoring kit into .story-spec/dist"
rm -rf "$DIST"; mkdir -p "$DIST"
cp -R "$src/core" "$src/modules" "$src/agents" "$src/skills" "$src/CLAUDE.dist.md" "$DIST/"
[ -d "$src/templates" ] && cp -R "$src/templates" "$DIST/"

# 2) Copy the scripts the project calls directly.
mkdir -p "$ROOT/scripts"
for s in extract_features.py lint_stories.py stories_status.sh generate_report.py init.sh; do
  [ -f "$src/scripts/$s" ] && cp "$src/scripts/$s" "$ROOT/scripts/$s"
done
chmod +x "$ROOT/scripts/init.sh" 2>/dev/null || true

# 3) First-run manifest.
mkdir -p "$ROOT/.story-spec"
fresh=0
if [ ! -f "$ROOT/.story-spec/manifest.yaml" ]; then
  cp "$src/.story-spec/manifest.example.yaml" "$ROOT/.story-spec/manifest.yaml"
  fresh=1
  say "created .story-spec/manifest.yaml (default selection)"
fi

command -v yq >/dev/null || say "note: install \`yq\` for full manifest parsing (module selection)."

# 4) Compose, unless opted out. init.sh auto-detects DIST=.story-spec/dist.
if [ "${STORY_SPEC_NO_INIT:-0}" = "1" ]; then
  say "skipped compose (STORY_SPEC_NO_INIT=1)."
else
  say "composing CLAUDE.md"
  ( cd "$ROOT" && bash scripts/init.sh )
fi

say "done."
if [ "$fresh" = 1 ]; then
  echo "  → edit .story-spec/manifest.yaml, then run: bash scripts/init.sh --sync"
fi
