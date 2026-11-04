"""Generate the source housekeeping page from local reference metadata."""
from pathlib import Path
from collections import Counter
import json
ROOT=Path(__file__).resolve().parents[1];REF=ROOT/'references'
records=[]
for p in REF.rglob('metadata.json'):
 if any((p.parent/n).exists() for n in ['paper.pdf','article.md','repository.tar.gz','audit.json']):
  m=json.loads(p.read_text());m['folder']=str(p.parent.relative_to(REF));records.append(m)
counts=Counter(m.get('topic','other') for m in records)
source=Counter(m.get('latex_source',{}).get('status','unrecorded') for m in records)
code=Counter(c.get('status') for m in records for c in m.get('code',[]))
pdfs=sum((REF/m['folder']/'paper.pdf').exists() for m in records)
figures=len(list((ROOT/'doc/assets').glob('*')))
labels={'scaling-laws':'Scaling laws and fitting','architecture':'Architecture and MoE','optimization':'Optimizers and hyperparameter transfer','data':'Data construction, mixtures, and repetition','evaluation':'Evaluation and task prediction','model-reports':'Model reports: OLMo, Kimi, Nemotron, and others','marin':'Marin technical reports','methodology':'Research methodology','systems':'Training systems and source implementations'}
rows='\n'.join(f'| {labels.get(k,k)} | {v} |' for k,v in sorted(counts.items()))
key=[]
for aid in ['2203.15556','2203.03466','2412.04403','2505.13738','2503.04715','2305.16264','2602.12237','2512.20848','2604.12374','2606.15007','2412.02595','2609.01343']:
 m=next(m for m in records if m.get('id','').split('v')[0]==aid)
 key.append(f'- [{m["title"]}](../references/{m["folder"]}/paper.pdf) — `{m.get("reviewed_version",m["id"])}`.')
body='''---
title: "Source housekeeping: what we have and where to find it"
---

## The blog, notes, and research papers have different roles

| Item | Location | Meaning |
|---|---|---|
| [Jiaxuan's saved blog](scientific-scaling-ladder.md) | `doc/scientific-scaling-ladder.md` | Secondary synthesis, retained with its original reference links and local figures |
| [Supplied notes](../scaling_ladder_notes.md) | `scaling_ladder_notes.md` | Restructuring and derivations based on the blog; some claims need qualification |
| [Annotated Quarto notes](deep-dive-notes.qmd) | `doc/deep-dive-notes.qmd` | Generated reading edition with companion links |
| [Source review](notes-review.qmd) | `doc/notes-review.qmd` | Checked claims and corrections, with primary evidence |
| [Full source catalogue](../references/SOURCES.md) | `references/SOURCES.md` | Readable names, stable identifiers, PDFs and metadata |
| [Download status](../references/README.md) | `references/README.md` | Collection scope and unresolved code availability |
| [Machine-readable manifest](../references/download-manifest.json) | `references/download-manifest.json` | Per-reference provenance and retrieval results |

The paper folders contain their own `source/` directories for LaTeX. Those are different from the saved blog in `doc/`. An empirical claim should ultimately point to a paper, report or experiment artifact, rather than relying only on the blog or notes.

## Collection at a glance

COUNTS

| Topic | Reference folders |
|---|---:|
TOPICS

Counts describe collection availability, not scientific validation. A downloaded source is not automatically a reviewed source, and a paper-linked repository may be evaluation code, data tooling, or a baseline. Current code snapshots are not automatically the revisions used in the reported experiment.

## Useful primary sources for this reading project

KEY

The [complete catalogue](../references/SOURCES.md) includes the remaining sources. Use [Marin's reading map](../references/MARIN-READING.md) to locate its implementation examples.

## Industry-practice evidence and implementation snapshots

The [conversation audit](industry-practice-audit.qmd) reviews the supplied `scaling_ladder_industry_practice.md` against Step Law v3, Farseer v3, Power Lines v2 and Marin. The [data-engineering guide](marin-data-engineering.qmd) audits actual mixture Parquet records and distinguishes the historical report from newer code. The [trainer guide](trainer-playbook.qmd) and [checkpoint-evaluation guide](checkpoint-evaluation.qmd) link the downloaded implementations. The [96-H100 plan](plan-96-h100.qmd) is the current budget interpretation.

Pinned trainer archives live in `references/systems/`; ignored checkouts are `tmp/torchtitan`, `tmp/megatron-lm` and `tmp/lm-evaluation-harness`. The [source pins](../configs/industry/source-pins.json) and [Marin record audit](../references/marin/2026-datakit-proxy-run-records/audit.json) record exactly what was inspected. Records are experiment metadata, not a prepared corpus. The Step Law fitting repository was found through its project site and added to its existing paper folder.

## Effort-level reading

The [OLMo deep dive](olmo-pretraining.qmd) connects its corpus work, mixture proxies, Task Ladder and training stages. The [Marin deep dive](marin-pretraining.qmd) connects Datakit, mixture learning, Delphi and training heuristics. The [beginning-to-end design](from-data-to-pretraining.qmd) turns those examples into a project plan starting from an available corpus.

## Inside a reference folder

```text
references/<topic>/<year-readable-title>/
  README.md              description and local entry points
  metadata.json          identifier, URL, version information, download status
  paper.pdf              paper/report, when available
  paper.txt              extracted text for searching
  arxiv-source.tar       original source download, when available
  source/                extracted LaTeX, bibliography and figures
  code/                  discovered repository archives
  article.md             web-first report snapshot, where applicable
  release-recipes/       additional official recipe snapshots, where collected
```

Not every reference has every artifact. Read `metadata.json` for actual availability. Source archives can be gzip-compressed despite the `.tar` suffix. The [notes heading map](data/notes-reading-map.json) records the section/subsection companion links. The [directory map](../references/directory-map.json) resolves the earlier arXiv-named folders into the readable topic layout.

## Focused paper and code replication guides

New focused guides explain [Step Law](papers/step-law.qmd), [Farseer](papers/farseer.qmd), and [Power Lines](papers/power-lines.qmd). The [MoE architecture comparison](architecture/moe-families.qmd) uses pinned official Qwen3/OLMoE configs and Marin model code. The [Marin optimizer-search manual](optimizers/marin-hyperparameter-search.qmd) audits Vizier and multiplier grids; the [Datakit code walkthrough](data/marin-code-walkthrough.qmd) traces artifact contracts; the [cyber-data extension](data/cyber-data.qmd) separates our domain hypothesis from the baseline reproduction.

## Routine upkeep

1. When adding evidence, record the primary title, identifier/version, URL and local artifact. Preserve an existing snapshot when a new version could change a numerical claim.
2. Record whether a statement is a reported configuration, measured optimum, mathematical derivation, or our proposed experiment. Add exact section/table/code locators where available.
3. Update the catalogue and status pages from the repository root:

```bash
python scripts/summarize_references.py
python scripts/build_reference_catalog.py
python scripts/build_source_guide.py
```

4. After editing the supplied Markdown notes, regenerate their Quarto edition and heading map:

```bash
python scripts/build_notes_quarto.py
```

5. Render the site with `quarto render`, or browse it with `quarto preview`. Generated HTML is in `_site/`; it is ignored by Git. The notes edition and this page are generated source files, so change their generator or the original inputs rather than editing their generated body.

Network collection is separate from housekeeping: the collectors in `scripts/` attempt source/code downloads and record failures. Do not rerun downloads merely to refresh navigation or counts.
'''
countline=f'The library contains **{len(records)} reference folders**, including **{pdfs} PDFs** and **{source["downloaded"]} successfully collected arXiv source packages**. Per-reference code records show **{code["downloaded"]} downloaded** and **{code["unavailable"]} unavailable** archives; the same repository may be associated with several papers.'
from doc_paths import rewrite, full_paths
page=body.replace('COUNTS',countline).replace('TOPICS',rows).replace('KEY','\n'.join(key))
(ROOT/'doc/sources/source-guide.qmd').write_text(full_paths(rewrite(page,ROOT/'doc/source-guide.qmd',ROOT/'doc/sources/source-guide.qmd')))
print('Built housekeeping guide for',len(records),'references')
