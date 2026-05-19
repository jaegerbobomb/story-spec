#!/usr/bin/env python3
"""
StorySpec - extract_features.py

Reads story files (stories/S*.md) and generates Behat/Cucumber .feature
files from the "## Acceptance Criteria" section of stories with `bdd: true`.

Usage:
    python3 extract_features.py [options]

Options:
    --stories-dir=<path>   Source directory (default: stories)
    --output-dir=<path>    Output directory (default: tests/features)
    --dry-run              Print what would be generated, write nothing
    --verbose              Print skipped files too
"""

import re
import sys
from pathlib import Path


def parse_args():
    args = sys.argv[1:]

    def get(name, default):
        for a in args:
            if a.startswith(f'--{name}='):
                return a[len(f'--{name}='):]
        return default

    return (
        Path(get('stories-dir', 'stories')),
        Path(get('output-dir', 'tests/features')),
        '--dry-run' in args,
        '--verbose' in args,
    )


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
        value = value.strip().strip('"\'')
        if not value.startswith('['):
            result[key.strip()] = value
    return result


def extract_scenarios(content: str) -> list:
    start = content.find('## Acceptance Criteria')
    if start == -1:
        return []

    rest = content[start + len('## Acceptance Criteria'):]
    m = re.search(r'\n## ', rest)
    section = rest[:m.start()] if m else rest

    scenarios, current = [], None
    step_re = re.compile(r'^\*\s+\*\*(Given|When|Then|And|But)\*\*\s+(.+)$')

    for line in section.splitlines():
        m = re.match(r'^###\s+Scenario:\s+(.+)$', line)
        if m:
            if current:
                scenarios.append(current)
            current = {'title': m.group(1).strip(), 'steps': []}
            continue
        if current is None:
            continue
        m = step_re.match(line)
        if m:
            current['steps'].append({'keyword': m.group(1), 'text': m.group(2).strip()})

    if current and current['steps']:
        scenarios.append(current)
    return scenarios


def build_feature(story_id: str, title: str, scenarios: list) -> str:
    lines = [f'Feature: [{story_id}] {title}', '']
    for s in scenarios:
        lines.append(f"  Scenario: {s['title']}")
        for step in s['steps']:
            lines.append(f"    {step['keyword']} {step['text']}")
        lines.append('')
    return '\n'.join(lines)


def main() -> int:
    stories_dir, output_dir, dry_run, verbose = parse_args()

    files = sorted(stories_dir.glob('S*.md'))
    if not files:
        print(f'No story files found in {stories_dir}')
        return 0

    generated = skipped = 0

    for file in files:
        content = file.read_text(encoding='utf-8')
        fm = parse_frontmatter(content)

        if fm.get('bdd') != 'true':
            if verbose:
                print(f'[skip] {file.name} (bdd: false)')
            skipped += 1
            continue

        story_id  = fm.get('id', file.stem)
        scenarios = extract_scenarios(content)

        if not scenarios:
            if verbose:
                print(f'[skip] {file.name} (no scenarios found)')
            skipped += 1
            continue

        out     = output_dir / f'{story_id}.feature'
        feature = build_feature(story_id, fm.get('title', story_id), scenarios)

        if dry_run:
            print(f'[dry-run] Would generate: {out}')
            if verbose:
                print(feature)
        else:
            output_dir.mkdir(parents=True, exist_ok=True)
            out.write_text(feature, encoding='utf-8')
            print(f'[ok] {out}')

        generated += 1

    print(f'\n{generated} file(s) generated, {skipped} skipped.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
