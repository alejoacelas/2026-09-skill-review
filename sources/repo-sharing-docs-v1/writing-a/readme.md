# Writing checks

Point this at a folder of Markdown and it lists the passages most worth a second
edit: overlong sentences and paragraphs, unexplained acronyms, stacked asides,
piled-up em dashes and semicolons, and other habits that slow readers down. It
runs locally in seconds, with no AI model, account or API key.

For example, given this paragraph from the bundled examples:

> Files: copy them. Versions: keep them. Recovery: test it.

it reports line 6 under check 19: *two or more short sentence-initial labels;
separate these into items*.

## What it does for you

- **Writers get a short review list and keep control of the edits.** Each
  finding names the rule, the source line and the passage, so you decide what
  to change. Your files are never edited.
- **Editors and documentation teams see the whole collection at once.** A
  browser page ranks every document by score and lets you filter by rule,
  document type or length, then read each finding in context.
- **Teams can run it automatically.** Exit codes separate clean files, files
  with findings and bad input, so the checker can gate a review step. You can
  choose which checks to run.
- **The rules are exact and inspectable.** Every threshold is written down in
  the [rubric](RUBRIC.md), so two people running it get the same answer.

## Cost and effort

- **Money:** free. Nothing leaves your machine.
- **Setup:** Python 3.10+ and [uv](https://docs.astral.sh/uv/getting-started/installation/).
  The first run installs two small Python packages automatically.
- **Speed:** 200 documents of about 1,100 words each took 2.3 seconds to check
  and 3 seconds to build the browser page on an Apple M4 Mac.

To try it, clone this repository and, from its folder, run
`uv run scripts/check.py /path/to/your/writing`. Or ask your coding agent
(Claude Code, Codex or similar):

> Clone this repository, run its writing checks on my `docs/` folder, open the
> explorer, and summarise which rules fail most often. Don't edit my files.

## Before you rely on it

These are editing prompts, not a quality score. A document can pass every check
and still be wrong, unclear or useless, and some findings will be passages you
should keep. Two checks encode the original author's own preferences and will
rarely matter to anyone else: check 6 flags third-person references to "Alejo",
and check 17 flags coaching-call phrasing. [Usage](USAGE.md#choose-checks)
shows how to skip them.

- **Tested:** the 14 unit tests pass. Every command in [Usage](USAGE.md) was run
  on the bundled examples and on a 200-file folder on macOS.
- **Not tested:** Windows and Linux, collections much larger than 200 files,
  running inside a CI service, and non-English writing. The sentence and
  acronym rules assume English.

## How it works

`scripts/check.py` parses each Markdown file, strips frontmatter, code, quotes,
comments and source lists, then applies 19 fixed pattern and length rules to
the remaining prose. `scripts/explore.py` runs the same checks and writes a
single offline HTML page with the results and the document text embedded.

## More

- [Usage](USAGE.md): every command, options, the explorer and development.
- [Rubric](RUBRIC.md): each rule's pass condition and exact counting conventions.
- [Decisions](DECISIONS.md): what this repository keeps public and why.
