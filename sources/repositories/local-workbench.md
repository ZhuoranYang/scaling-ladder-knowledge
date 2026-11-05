---
id: doc-local-workbench
title: Local CPU record replays and analytical fixtures
type: source-doc
tags:
- provenance
- reproducibility
sources: []
url: https://github.com/ZhuoranYang/scaling-ladder-knowledge
source_category: local-analysis
retrieved_at: '2026-11-05'
version: sha256:37e2ff1a35530dd94d2c679b1b014290794bf7d244ac3ca0815376f9bb56d1a0
local_artifacts:
- path: scripts/kb_workbench.py
  role: code
  sha256: 37e2ff1a35530dd94d2c679b1b014290794bf7d244ac3ca0815376f9bb56d1a0
- path: knowledge/receipts/compute-ledger.json
  role: local-receipt
  sha256: 9db784c36ff2ea6fd2d7040f48b7c739cef96f5913d68f4fb88c97f4c69c7257
- path: knowledge/receipts/evaluation-denominators.json
  role: local-receipt
  sha256: b8b6dc89d545fc6b35d27f8b5af8e6af58ba97fa82c5be2d5cd8d7a4a1a927de
- path: knowledge/receipts/hf-mixture-records.json
  role: local-receipt
  sha256: 5d8c54cc5d282b5d4f09b4f21abf1338d332cb8c7f39129eb306c335c562161c
- path: knowledge/receipts/identifiability.json
  role: local-receipt
  sha256: 415b6ecc560bccfab33d29da6d423540dfd37313f06a8242045725890e1eace3
- path: knowledge/receipts/optimizer-timescale.json
  role: local-receipt
  sha256: 0648e3bbb191444b9f01bbd8ce83c872397e40b3a71dbe5c3926c80f769f5568
- path: knowledge/receipts/phase-exposure.json
  role: local-receipt
  sha256: a7b91c1ee15d395b409774ad70e3ac70bec1eb16d5da4dc44c0b0ac466cfba5c
- path: knowledge/receipts/step-law-release.json
  role: local-receipt
  sha256: 5f7860e03a3476c41547698d6488c7708ee06714bcaa877d82e990529711b8e9
review_status: artifact-inspected
architectures:
- not-specified
---

# Local CPU record replays and analytical fixtures

This is our own proposal or CPU analysis, explicitly separate from a reported training experiment. No GPU training was performed.

- [code](../../scripts/kb_workbench.py) — `37e2ff1a35530dd94d2c679b1b014290794bf7d244ac3ca0815376f9bb56d1a0`.
- [local-receipt](../../knowledge/receipts/compute-ledger.json) — `9db784c36ff2ea6fd2d7040f48b7c739cef96f5913d68f4fb88c97f4c69c7257`.
- [local-receipt](../../knowledge/receipts/evaluation-denominators.json) — `b8b6dc89d545fc6b35d27f8b5af8e6af58ba97fa82c5be2d5cd8d7a4a1a927de`.
- [local-receipt](../../knowledge/receipts/hf-mixture-records.json) — `5d8c54cc5d282b5d4f09b4f21abf1338d332cb8c7f39129eb306c335c562161c`.
- [local-receipt](../../knowledge/receipts/identifiability.json) — `415b6ecc560bccfab33d29da6d423540dfd37313f06a8242045725890e1eace3`.
- [local-receipt](../../knowledge/receipts/optimizer-timescale.json) — `0648e3bbb191444b9f01bbd8ce83c872397e40b3a71dbe5c3926c80f769f5568`.
- [local-receipt](../../knowledge/receipts/phase-exposure.json) — `a7b91c1ee15d395b409774ad70e3ac70bec1eb16d5da4dc44c0b0ac466cfba5c`.
- [local-receipt](../../knowledge/receipts/step-law-release.json) — `5f7860e03a3476c41547698d6488c7708ee06714bcaa877d82e990529711b8e9`.
