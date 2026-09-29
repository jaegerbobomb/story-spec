#!/usr/bin/env python3
"""
StorySpec - generate_report.py

Generates a Markdown status report of all stories for GitHub Pages.

Usage:
    python3 generate_report.py [--stories-dir=stories] [--output=docs/status.md]
"""

import sys
from datetime import date
from pathlib import Path


def parse_args():
    args = sys.argv[1:]

    def get(name, default):
        for a in args:
            if a.startswith(f'--{name}='):
                return a[len(f'--{name}='):]
        return default

    return Path(get('stories-dir', 'stories')), Path(get('output', 'docs/status.md'))


def parse_frontmatter(content: str) -> dict:
    if not content.startswith('---'):
        return {}
    end = content.find('---', 3)
    if end == -1:
        return {}
    result = {}
    for line in content[3:end].splitlines():
        line = line.strip()
        if not line or ':' not in line:
            continue
        key, _, value = line.partition(':')
        result[key.strip()] = value.strip().strip('"\'')
    return result


# A story whose status is not one of these is still listed (with `❓`) and still
# counted in the total — a story the report cannot classify must not silently
# vanish from the denominator.
BADGE = {
    'proposed':    '💡',
    'todo':        '⬜',
    'in_progress': '🔄',
    'done':        '✅',
    'split':       '🔀',
    'to_extend':   '➕',
    'deferred':    '⏸️',
    'archived':    '🗄️',
}


def main() -> int:
    stories_dir, output_file = parse_args()

    files = sorted(stories_dir.glob('S*.md'))
    if not files:
        print(f'No stories found in {stories_dir}', file=sys.stderr)
        return 1

    rows   = []
    counts = {status: 0 for status in BADGE}
    unknown = 0

    for file in files:
        fm     = parse_frontmatter(file.read_text(encoding='utf-8'))
        status = fm.get('status', 'unknown')
        bdd    = '✓' if fm.get('bdd') == 'true' else ''
        badge  = BADGE.get(status, '❓')
        rows.append(
            f"| {badge} | `{fm.get('id', file.stem)}` | {fm.get('title', '')} "
            f"| {fm.get('epic', '')} | {fm.get('estimate', '')} | {bdd} |"
        )
        if status in counts:
            counts[status] += 1
        else:
            unknown += 1

    total    = sum(counts.values()) + unknown
    done     = counts['done']
    progress = round(done / total * 100) if total else 0

    header  = ' | '.join(f'{BADGE[s]} {s}' for s in BADGE)
    figures = ' | '.join(str(counts[s]) for s in BADGE)
    if unknown:
        header += ' | ❓ unknown'
        figures += f' | {unknown}'
    columns = '|---' * (len(BADGE) + 1 + bool(unknown)) + '|'

    md = f"""\
# Story Status

Generated: {date.today().isoformat()}

**{done}/{total} done ({progress}%)**

| | {header} |
{columns}
| Count | {figures} |

---

| | ID | Title | Epic | Size | BDD |
|---|---|---|---|---|---|
""" + '\n'.join(rows) + '\n'

    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(md, encoding='utf-8')
    print(f'Report written to {output_file}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
