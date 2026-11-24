---
title: Running the stories with pytest-bdd
nav_order: 4.5
permalink: /python-pytest-bdd/
---
# How to run the stories with pytest-bdd (Python)

StorySpec's extractor writes plain Gherkin `.feature` files. Behat and Cucumber read
them, and so does [pytest-bdd](https://pytest-bdd.readthedocs.io). This page shows the
wiring for a Python project. The manifest value for it is `test_adapter: bdd-pytest`;
today `init.sh` only records that value, it installs nothing.

## 1. Install pytest-bdd

```bash
pip install pytest pytest-bdd
```

## 2. Generate the features before pytest collects

`scenarios()` reads the `.feature` files **when the test module is imported**, so they
must exist before pytest collects. Two ways:

- run the extractor first, in your Makefile or CI:

  ```bash
  python3 scripts/extract_features.py --output-dir=tests/features && pytest
  ```

- or let pytest do it, in `tests/conftest.py`:

  ```python
  import subprocess
  import sys


  def pytest_configure(config):
      # Regenerate tests/features/*.feature from stories/ (build artifacts, gitignored).
      subprocess.run(
          [sys.executable, "scripts/extract_features.py", "--output-dir=tests/features"],
          check=True,
      )
  ```

Keep `tests/features/*.feature` in `.gitignore`: the story stays the source.

## 3. Bind the scenarios of a story

One test module per story keeps the trace obvious — `S001` in `stories/`,
`tests/features/S001.feature`, `tests/step_defs/test_S001.py`:

```python
# tests/step_defs/test_S001.py
from pytest_bdd import given, parsers, scenarios, then, when

scenarios("../features/S001.feature")


@given(parsers.parse("no account exists with email `{email}`"))
def no_account(db, email):
    db.delete_user(email)


@when(parsers.parse("`POST /api/users` is sent with `{payload}`"), target_fixture="response")
def register(client, payload):
    return client.post("/api/users", data=payload)


@then(parsers.parse("the response status is {status:d}"))
def status_is(response, status):
    assert response.status_code == status
```

Things that trip people up:

- **The step text is matched literally**, backticks included. The extractor keeps them
  as written in the story, so the pattern must contain them too.
- **`And` and `But` take the type of the step before them** (`Given`, `When` or
  `Then`): bind them with the same decorator as that step.
- **A step with no definition fails the scenario.** That is the point — but it means
  every scenario of a story moved to `done` needs all its steps bound.

## 4. Only `done` stories in CI

The extractor generates a feature for every story with `bdd: true` and at least one
scenario. In CI you usually want the suite of delivered stories only; a story still
`proposed` or `in_progress` must not break the build. Keep the step definitions of
unfinished stories out of the test paths, or mark their modules with
`pytestmark = pytest.mark.skip(reason="S00N not done")` until the story is delivered.
