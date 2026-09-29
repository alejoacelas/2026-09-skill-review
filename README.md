# Skill review

Compare two generated documents, mark passages to rewrite or remove, and choose which differences to keep. This local interface includes the Morning reader and Writing checks trials.

Run `python3 server.py`, then open http://127.0.0.1:8767 in Chrome. No account or API key is needed.

New trials use the copy of this tool in the private `alejoacelas/skill-cases` repository, which reads each trial from its case folder. This repository keeps only the prepare-to-share trial.

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

The original Markdown is frozen under [sources](sources), with provenance in the [manifest](sources/manifest.json). Version labels stay neutral in the reading interface; the manifest contains the mapping. To regenerate the rendered documents, run `uv run scripts/build_data.py`.

Browser checks covered keyboard preferences, selected-text annotation, missing notes, restoration after reload, project switching, difference placement and JSON export. Test feedback uses a separate port and ignored file.
