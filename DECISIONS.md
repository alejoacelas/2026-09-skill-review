# Review design

## Core decisions

- [Ask concrete questions and collect passage-level feedback](#concrete-judgments), so the reviewer can explain a preference without inventing a grading rubric.
- [Preserve source documents and keep feedback local](#sources-and-feedback), so judgments remain traceable and separate from later edits.

## Details

### Concrete judgments

Start with which opening to keep. Offer selected-text tags for bad writing, removal and moving to a linked file. For missing information, compare actual excerpts and ask what to retain and where it belongs; allow a free-text note for omissions in both versions. Curated differences supplement the full documents rather than claiming to cover every difference. Implemented in [058e80b](https://github.com/alejoacelas/2026-09-skill-review/commit/058e80b).

### Sources and feedback

Freeze documents at exact commits and expose source links. Keep version labels neutral in the review interface, with the mapping available in the manifest. Save feedback locally and provide an explicit export containing source provenance and criteria. Preserve this separation when modifying the interface. Implemented in [058e80b](https://github.com/alejoacelas/2026-09-skill-review/commit/058e80b) and [25122a0](https://github.com/alejoacelas/2026-09-skill-review/commit/25122a0).

## Decision log

2026-09-29: Use narrow comparisons, selectable passage tags and excerpt-based retention choices, following the reviewer's preference for concrete judgments over broad scores. Keep missing-content notes available for omissions that a comparison cannot surface.
