# Knowledge representation and maintenance

Read [CLAUDE.md](../CLAUDE.md) for the human-facing schema and [index.md](../index.md)
for the knowledge portal. This directory stores the control plane and small
replay inputs; the full downloaded literature remains in [references/](../references/).

| File | Role |
|---|---|
| `schemas.yaml` | Required fields, page types, confidence/reproduction levels and numerical-claim contract |
| `tags.yaml`, `aliases.yaml` | Controlled vocabulary and non-ambiguous query aliases |
| `claims.json` | Scoped statements, exact source locators, quantities/units, limits and verification |
| `version-claims.json` | Bidirectional claim/version dependencies and review dates |
| `questions.json` | Ten core decision contracts with answer pages, evidence and unresolved inputs |
| `legacy-guides.json` | The original long-form guides, retained and catalogued without automatic review promotion |
| `literature-baseline.json` | Preservation roster for 4615 original library files; immutable primary-artifact Git identities |
| `inputs/` | Small verbatim public fitting/configuration inputs and their provenance |
| `receipts/` | Seven executed CPU record/configuration/analytical checks, not training runs |
| `index.json`, `source-map.json` | Generated machine retrieval views; do not edit manually |

## Add a source

Retain the original paper/LaTeX/code/result artifact in its readable reference
folder. Add a `sources/` Markdown card with the required YAML frontmatter and
local artifact hashes. Preserve upstream version/status and source category.
`review_status: catalogued` means indexed, not semantically audited.

## Add a synthesis

Add a `wiki/` Markdown page with a stable typed ID, controlled tags and architecture
scope, confidence, reproducibility **and scope**, prerequisites, related/source
IDs and scoped claim IDs. Techniques/recipes/case studies need actual code
examples; an offline accounting example does not qualify a training stack.
Bind numerical comparisons to full claim records. Declare missing uncertainty.

## Validate and publish

```bash
python -m pip install -r scripts/requirements-kb.txt
python scripts/kb_workbench.py --all --check
python scripts/kb.py generate-indices
python scripts/kb.py validate --verify-artifacts
python -m unittest discover -s tests -p 'test_kb*.py'
quarto render
# Use the isolated PDF environment described in pdf/README.md:
PLAYWRIGHT_BROWSERS_PATH="$PWD/tmp/pdf-browser" tmp/pdf-tools/bin/python scripts/render_pdfs.py
python scripts/kb.py validate --verify-artifacts --check-generated
```

When intentionally changing replay code or input versions, regenerate the named
receipt, review its result and update the corresponding source-card hash before
validation. Do not rewrite receipts simply to silence a regression. New versions
of original literature belong alongside old ones.

Query/get/status use the committed index and standard Python. Generation and
validation require PyYAML. HF record replay additionally needs PyArrow. The CI
workflow runs only CPU checks; it neither renders GPU training configs nor
submits cluster jobs.

The final generated-artifact gate also compares every PDF with its source fingerprint and the PDF renderer version. A source or renderer edit requires refreshing the corresponding rendered collection before publication.
