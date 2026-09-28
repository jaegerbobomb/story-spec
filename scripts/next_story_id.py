#!/usr/bin/env python3
"""
StorySpec - next_story_id.py

Which story number is free? A number is never reused, so the answer must account
for every git ref, not just the working tree: a story being written on another
branch owns its number already. Looking only at `stories/` is exactly how two
authors pick the same number on the same day.

This replaces the practice of keeping a hand-written "reserved ids" list, which
drifts as soon as nobody updates it and cannot see branches anyway.

Sources, in order:
  1. story files in the working tree
  2. story files in every known git ref (local branches and remotes), via
     `git ls-tree` — no network, only what the repo already has

Run `git fetch --all --prune` first so step 2 is current.

Usage:
    python3 next_story_id.py [--stories-dir=stories] [--verbose]

Stdlib only, no dependencies.
"""

import argparse
import re
import subprocess
from collections import defaultdict
from pathlib import Path

# S142, S156a, S167m… : a number, optionally followed by a sub-story suffix.
STORY_FILE_RE = re.compile(r'^S(\d+)([a-z]\d*)?-')


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--stories-dir', default='stories', type=Path)
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='list the numbers only another git ref holds',
    )
    return parser.parse_args()


def numbers_from_names(names):
    """The story numbers carried by a list of file names."""
    found = set()
    for name in names:
        match = STORY_FILE_RE.match(Path(name).name)
        if match:
            found.add(int(match.group(1)))
    return found


def git(*args):
    """Run a git command, or return an empty string if it fails."""
    try:
        result = subprocess.run(
            ['git', *args], capture_output=True, text=True, check=True
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return ''
    return result.stdout


def working_tree_ids(stories_dir):
    """The numbers carried by the story files in the working tree."""
    return numbers_from_names([p.name for p in stories_dir.glob('S*.md')])


def ids_by_ref(stories_dir):
    """number -> set of git refs whose tree carries a story with that number."""
    refs = [
        line.strip()
        for line in git(
            'for-each-ref', '--format=%(refname:short)', 'refs/heads', 'refs/remotes'
        ).splitlines()
        if line.strip()
    ]
    owners = defaultdict(set)
    for ref in refs:
        names = git('ls-tree', '-r', '--name-only', ref, f'{stories_dir}/').splitlines()
        for number in numbers_from_names(names):
            owners[number].add(ref)
    return owners


def main():
    args = parse_args()

    local = working_tree_ids(args.stories_dir)
    owners = ids_by_ref(args.stories_dir)
    taken = local | set(owners)

    if not taken:
        print('S001')
        return 0

    highest = max(taken)
    print(f'S{highest + 1:03d}')

    if args.verbose:
        elsewhere = sorted(number for number in owners if number not in local)
        if elsewhere:
            print('\nHeld by another git ref:')
            for number in elsewhere:
                print(f'  S{number:03d} — {", ".join(sorted(owners[number]))}')
        gaps = sorted(set(range(1, highest)) - taken)
        if gaps:
            joined = ', '.join(f'S{number:03d}' for number in gaps)
            print(f'\nGaps (no story carries them; prefer max+1 anyway): {joined}')

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
