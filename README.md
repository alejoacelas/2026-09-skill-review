# Skill review

Compare two generated documents, mark passages to rewrite or remove, and choose which differences to keep. This local interface includes the Morning reader and Writing checks trials.

Run `python3 server.py`, then open http://127.0.0.1:8767 in Chrome. No account or API key is needed.

Other trials open at `http://127.0.0.1:8767/?trial=NAME`. The current one is [repo-sharing-docs-v1](http://127.0.0.1:8767/?trial=repo-sharing-docs-v1): a draft repo-sharing skill against no skill on Morning reader, Writing checks and Team agent server, with the Opening and Full README steps only. Each trial saves feedback to its own `feedback.NAME.local.json`.

1. **Opening:** choose which opening you would keep.
2. **Full README:** read each document and mark passages. Each pane scrolls independently; the setup guide is available where the version includes one.
3. **Differences:** compare selected source excerpts, choose A, B, both or neither, and decide whether the material belongs in the README or a linked file. These are curated comparisons, not an exhaustive diff.

Select text to mark **Bad writing**, **Remove**, **Move to linked file** or **Really good**. Use **Add what’s missing** for information absent from both versions. Open **Feedback** to add comments, change notes, undo marks or revisit a passage.

| Key | Action |
| --- | --- |
| 1 / 2 / 3 / 4 / 0 | A / B / combine / neither / cannot judge |
| B / R / M / G | Tag selected text |
| N | Add missing information |
| F | Review feedback |
| ← / → | Previous / next question |
| ? | Show shortcuts |

Feedback saves in the browser and in the ignored `feedback.local.json` file. **Export** downloads a JSON copy with the source commits and review questions. Feedback is never published automatically. Use one review tab at a time; this prototype does not merge simultaneous edits.

The original Markdown is frozen under [sources](sources), with provenance in the [manifest](sources/manifest.json). Version labels stay neutral in the reading interface; the manifest contains the mapping. To regenerate the rendered documents, run `uv run scripts/build_data.py`. Other trials keep their frozen Markdown and manifest in `sources/NAME/` and are built with `uv run scripts/build_trial.py NAME`.

Browser checks covered keyboard preferences, selected-text annotation, missing notes, restoration after reload, project switching, difference placement and JSON export. Test feedback uses a separate port and ignored file.
