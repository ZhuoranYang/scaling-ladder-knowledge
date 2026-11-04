# Marin released mixture experiment records

Source: https://huggingface.co/datasets/marin-community/grug-moe-mix-swarm

Revision: `7aa59d2158a6299bde95d24dd1b1b9c98f6e4d5a` (2026-11-02).

- [Audit](audit.json): 116 legacy Harrier rows (72 fresh, 44 resumed cooldown); 840 rows in the other downloaded swarm table.
- `harrier_18t75_d768.parquet`, `swarm_runs.parquet`: pinned experiment records.
- `buckets.json`, `harrier_buckets.json`: bucket metadata.
- [Original dataset card](dataset-card.md).

These are experiment records, not the prepared pretraining text. Counts from distinct exports and report snapshots must not be summed as independent runs. See `metadata.json` for provenance.
