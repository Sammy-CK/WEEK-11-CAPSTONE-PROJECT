# Capstone proposal

## Path
AfyaPlus Module 4 Capstone: integrated AI health-operations system.

## Problem
Clinic coordinators and nurses need one intake path for symptom triage, logistics lookups, and optional Sokoni catalog checks without mixing patient and marketplace data. The system supports routing, grounded stub answers, and tool calls under JWT auth. Success this week: Monday planning and health check; Tuesday end-to-end stub flow with tests; Thursday doc packet and demo script for Week 12.

## Dataset
fixtures/triage_messages_sample.jsonl: ~300 synthetic rows (teaching only).
Do not scrape production. Do not use millions of rows.
Catalog lane (Week 10) will use separate fixtures under services/catalog when wired Tuesday.

## Milestones
- Monday: proposal, skill_matrix, integration_map, base service /health 200
- Tuesday: pytest pyramid, security smoke, CI, remaining layers, fixture diagnosis, eval score
- Thursday: docs, peer review, presentation deck
- Week 12 Monday: presentation and demo

## Out of scope
- Training a new foundation model
- Live crawl of patient or buyer PII
- Mixing clinical and marketplace fixtures
