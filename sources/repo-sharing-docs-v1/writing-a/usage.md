# Usage

Run every command from the repository folder. You need Python 3.10 or later and
[uv](https://docs.astral.sh/uv/getting-started/installation/). The first
`uv run` installs the two Python dependencies.

## Check files

```sh
# Try the bundled synthetic examples (one passes, one fails on purpose).
uv run scripts/check.py

# Check your own files or folders.
uv run scripts/check.py /path/to/writing
uv run scripts/check.py /path/to/guide.md --format json
```

Exit codes: **0** no findings, **1** at least one finding, **2** invalid input
such as a missing path.

Folder scans read every `.md` file, skipping hidden paths, `node_modules`,
`__pycache__`, `AGENTS.md`, `DECISIONS.md`, `PLAN.md` and `feedback-log.md`.
Naming a file directly checks it even if a folder scan would skip it.

## Choose checks

Pass `--checks` with the rule IDs from the [rubric](RUBRIC.md). To run
everything except the two author-specific checks (6 and 17):

```sh
uv run scripts/check.py /path/to/writing --checks 1,2,4,5,7,8,9,11,12,13,16,18,19,20,21,22,23
```

- **Technical readers:** `--audience technical` skips check 2, which flags
  unexplained acronyms.
- **Comparison guides:** check 4 wants a recommendation before the first list
  of options. It runs automatically when the title or a heading contains words
  like "vs" or "comparison". Use `--options-guide` to force it on.

## Browse results

```sh
uv run scripts/explore.py /path/to/writing --open
```

This writes `scripts/explorer.local.html` and opens it in your browser. The page
works offline and always applies every check with the beginner audience.
`--output` writes it elsewhere.

The page contains the text of every document and their local file paths.
Share it only if that content can be shared. Git ignores it in this repository.

- **Filter:** document type, length and search narrow the collection. Click a
  rule to show documents that fail it, or double-click to show those that pass.
  Pass rates are computed after the type, length and search filters and before
  score or rule filters.
- **Keys:**
  - Up/Down or j/k browse documents.
  - Left/Right move between scores.
  - [ and ] step through findings, and v switches to reading view.
  - / searches, Esc resets filters and ? lists shortcuts.
- **Grouping:** add YAML frontmatter `kind: article` or `kind: primer` to group
  documents. Other files appear as Notes, or Indexes for `README.md` and
  `index.md`. Frontmatter `reference_provider` (one of `Stripe`, `Django`,
  `GOV.UK`, `Chrome`) plus `source_url` marks a document as a third-party
  reference snapshot; none are bundled.

## Development

```sh
uv run --with markdown-it-py==4.0.0 --with 'pyyaml>=6,<7' python -m unittest discover -s scripts -v
uv run scripts/explore.py
```

The checker, explorer and tests were extracted from a private writing-evaluation
project. This repository starts with fresh history and synthetic examples.
