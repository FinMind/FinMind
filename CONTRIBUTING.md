# Contributing to FinMind

FinMind accepts bug fixes, tests, documentation updates, and new dataset
integrations. Keep each pull request focused so its behavior and data assumptions
can be reviewed independently.

## Development setup

FinMind uses [uv](https://docs.astral.sh/uv/) for dependency management. The CI
test matrix currently covers Python 3.8 through 3.12; the commands below use
Python 3.12.

```bash
uv sync --group dev --python 3.12
```

Some tests query the live FinMind API. Put the required token in the ignored
`.env` file and do not commit credentials:

```text
FINMIND_API_TOKEN=your-token
```

Run the smallest relevant test selection while developing:

```bash
uv run --env-file=.env pytest tests/path/to/test_file.py
```

Before opening a pull request, run the full checks when your API access permits:

```bash
uv run --env-file=.env pytest -n auto --dist=loadfile \
  --cov-report term-missing --cov-config=.coveragerc --cov=./ tests/
uv tool run --python 3.8 black==24.8.0 -l 80 --check FinMind tests
```

## What to include

- Add or update tests for behavior changes and bug fixes.
- Keep unrelated cleanup out of the pull request.
- Update public documentation and the files under `.claude/commands/` when a
  dataset, SDK method, parameter, or documented behavior changes.
- For new or corrected financial data, identify the source and describe the
  field, date, unit, and availability semantics. Note any access or licensing
  restriction that affects reproducibility.
- Update `uv.lock` when dependency constraints change.

Open pull requests against `master` and link the related issue when one exists.
Include the observed problem, the chosen change, and the commands used to verify
it.
