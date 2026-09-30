#!/usr/bin/env python3
"""
StorySpec - lint_stories.py  (module: story-lint)

Validates that every story file is well-formed before implementation — the
"third audience: CI" applied to the spec itself. Stdlib only, no dependencies.

Checks (ERROR fails the run, WARN is informational unless --strict):
  - filename matches  S<NNN>[<suffix>]-<kebab-slug>.md
  - frontmatter present, with required keys: id, title, epic, depends_on,
    status, estimate, bdd
  - id is S<NNN>[<suffix>] and matches the filename prefix
  - status in proposed|todo|in_progress|done|split|to_extend|deferred|archived
  - estimate in XS|S|M|L|XL ; bdd in true|false
  - bdd: true  =>  at least one scenario with steps under "## Acceptance Criteria"
  - updated present and ISO 8601 (YYYY-MM-DD)            [WARN]
  - depends_on ids resolve to a story in the same dir    [WARN]
  - adr ids (adr module) are integers                    [WARN]
  - title <= 8 words                                     [WARN]
  - sub-story nested beyond one level (S006a1)           [WARN]

Usage:
    python3 lint_stories.py [--stories-dir=stories] [--verbose] [--strict]
"""

import re
import sys
from pathlib import Path

STATUSES = {
    'proposed', 'todo', 'in_progress', 'done',
    'split', 'to_extend', 'deferred', 'archived',
}
ESTIMATES = {'XS', 'S', 'M', 'L', 'XL'}
REQUIRED = ['id', 'title', 'epic', 'depends_on', 'status', 'estimate', 'bdd']

# A sub-story carries its parent's number plus one lowercase letter (S006a), so it
# consumes no new number. A second level (S006a1) parses but is warned about — see
# SPEC.md § Sub-stories.
SUFFIX = r'(?:[a-z]\d*)?'
FILENAME_RE = re.compile(rf'^S\d{{3}}{SUFFIX}-[a-z0-9]+(?:-[a-z0-9]+)*\.md$')
ID_RE = re.compile(rf'^S\d{{3}}{SUFFIX}$')
NESTED_SUFFIX_RE = re.compile(r'^S\d{3}[a-z]\d')
DATE_RE = re.compile(r'^\d{4}-\d{2}-\d{2}$')


def parse_args():
    args = sys.argv[1:]

    def get(name, default):
        for a in args:
            if a.startswith(f'--{name}='):
                return a[len(f'--{name}='):]
        return default

    return (
        Path(get('stories-dir', 'stories')),
        '--verbose' in args,
        '--strict' in args,
    )


def parse_frontmatter(content: str):
    """Return (dict, present). Scalars are strings; list values become lists."""
    if not content.startswith('---'):
        return {}, False
    end = content.find('\n---', 3)
    if end == -1:
        return {}, False
    result = {}
    for line in content[3:end].splitlines():
        line = line.strip()
        if not line or ':' not in line or line.startswith('#'):
            continue
        key, _, value = line.partition(':')
        key = key.strip()
        value = value.strip()
        if value.startswith('[') and value.endswith(']'):
            inner = value[1:-1].strip()
            result[key] = [v.strip().strip('"\'') for v in inner.split(',') if v.strip()]
        else:
            result[key] = value.strip('"\'')
    return result, True


#: Same anchoring as the extractor: the heading counts only at the start of a line.
#: A story may mention "## Acceptance Criteria" inside a sentence or a Gherkin step,
#: and a plain substring search then cuts the section short at that mention — the
#: linter reports "no scenario" on a story that has several, and the extractor
#: silently produces nothing. Keep the two in step.
AC_HEADING_RE = re.compile(r'^## Acceptance Criteria[ \t]*$', re.M)


def has_scenarios(content: str) -> bool:
    for match in AC_HEADING_RE.finditer(content):
        rest = content[match.end():]
        end = re.search(r'^## ', rest, re.M)
        section = rest[:end.start()] if end else rest
        has_title = re.search(r'^###\s+Scenario:\s+.+$', section, re.M)
        has_step = re.search(r'^\*\s+\*\*(Given|When|Then|And|But)\*\*\s+.+$', section, re.M)
        if has_title and has_step:
            return True
    return False


def main() -> int:
    stories_dir, verbose, strict = parse_args()

    files = sorted(stories_dir.glob('S*.md'))
    if not files:
        print(f'No story files found in {stories_dir}')
        return 0

    known_ids = {f.stem.split('-')[0] for f in files}
    errors = warnings = 0

    def err(name, msg):
        nonlocal errors
        errors += 1
        print(f'[ERROR] {name}: {msg}')

    def warn(name, msg):
        nonlocal warnings
        warnings += 1
        print(f'[warn]  {name}: {msg}')

    for file in files:
        name = file.name
        content = file.read_text(encoding='utf-8')
        fm, present = parse_frontmatter(content)

        if not FILENAME_RE.match(name):
            err(name, 'filename must match S<NNN>[<suffix>]-<kebab-slug>.md')
        elif NESTED_SUFFIX_RE.match(name):
            warn(name, 'sub-story nested beyond one level — split the parent more finely')
        if not present:
            err(name, 'missing or unterminated YAML frontmatter')
            continue

        for k in REQUIRED:
            if k not in fm:
                err(name, f'missing required frontmatter key `{k}`')

        sid = fm.get('id', '')
        if sid and not ID_RE.match(sid):
            err(name, f'id `{sid}` must be S<NNN>[<suffix>]')
        elif sid and not name.startswith(sid + '-'):
            err(name, f'id `{sid}` does not match filename prefix')

        status = fm.get('status')
        if status is not None and status not in STATUSES:
            err(name, f'status `{status}` not in {sorted(STATUSES)}')

        estimate = fm.get('estimate')
        if estimate is not None and estimate not in ESTIMATES:
            err(name, f'estimate `{estimate}` not in {sorted(ESTIMATES)}')

        bdd = fm.get('bdd')
        if bdd is not None and bdd not in ('true', 'false'):
            err(name, f'bdd `{bdd}` must be true or false')
        elif bdd == 'true' and not has_scenarios(content):
            err(name, 'bdd: true but no scenario with steps under "## Acceptance Criteria"')

        updated = fm.get('updated')
        if updated is None:
            warn(name, 'no `updated` field (recommended, ISO 8601)')
        elif not DATE_RE.match(updated):
            warn(name, f'`updated: {updated}` is not ISO 8601 (YYYY-MM-DD)')

        for dep in fm.get('depends_on', []) or []:
            if dep not in known_ids:
                warn(name, f'depends_on `{dep}` not found in {stories_dir}')

        for ref in fm.get('adr', []) or []:
            if not str(ref).isdigit():
                warn(name, f'adr `{ref}` should be an ADR number (integer)')

        title = fm.get('title', '')
        if title and len(title.split()) > 8:
            warn(name, 'title longer than 8 words')

        if verbose and not errors:
            print(f'[ok]    {name}')

    print(f'\n{len(files)} story file(s): {errors} error(s), {warnings} warning(s).')
    if errors or (strict and warnings):
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
