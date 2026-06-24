---
layout: page
title: Getting started
permalink: /getting-started/
---

# Getting started

> **Using the modular kit?** The fastest path is `scripts/init.sh`: declare your
> modules in `.story-spec/manifest.yaml`, run `bash scripts/init.sh`, and it composes
> `CLAUDE.md` and scaffolds the core + modules for you — see the
> [README quick start](https://github.com/jaegerbobomb/story-spec#quick-start) and the
> [migration guide](../how-to/migrating-to-modular.md). The manual steps below still
> work for a minimal, script-only setup.

## Prerequisites

- Python 3.8+ (no pip dependencies - stdlib only)
- A BDD framework: [Behat](https://behat.org) (PHP), [Cucumber](https://cucumber.io) (JVM/JS/Ruby), [pytest-bdd](https://pytest-bdd.readthedocs.io) (Python), etc.

## 1. Set up your stories directory

```bash
mkdir stories
cp path/to/storyspec/templates/stories-README.md stories/README.md
```

Add generated feature files to your `.gitignore`:

```
tests/features/*.feature
```

## 2. Copy the scripts

```bash
mkdir -p scripts
cp path/to/storyspec/scripts/extract_features.py scripts/
cp path/to/storyspec/scripts/stories_status.sh scripts/
```

## 3. Write your first story

```bash
cp path/to/storyspec/templates/story.md stories/S001-my-first-feature.md
```

Edit the file - fill in the frontmatter, the user story, and the acceptance criteria.

## 4. Generate feature files

```bash
python3 scripts/extract_features.py
# [ok] tests/features/S001.feature
```

Options:

```bash
python3 scripts/extract_features.py --stories-dir=stories --output-dir=tests/features
python3 scripts/extract_features.py --dry-run --verbose
```

## 5. Run your BDD suite

```bash
# Behat (PHP)
vendor/bin/behat

# Cucumber (Node)
npx cucumber-js

# pytest-bdd (Python)
pytest tests/
```

## 6. Check story status

```bash
bash scripts/stories_status.sh
```

## Makefile integration

```makefile
extract-features:
	python3 scripts/extract_features.py

test-acceptance: extract-features
	vendor/bin/behat --colors

stories-status:
	@bash scripts/stories_status.sh
```

## GitHub Actions

Copy `.github/workflows/validate.yml` from the StorySpec repository into your project
to validate stories on every pull request.

For a GitHub Pages status dashboard, copy `.github/workflows/pages.yml`
and adapt the `--stories-dir` argument.
