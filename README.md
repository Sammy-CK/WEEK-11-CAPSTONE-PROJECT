# Module 4 Capstone: AfyaPlus integrated health operations

Integrated Week 6–10 artefacts: triage API with JWT and Week 8 pins, Week 7 logistics tool surface, Week 9 security smoke, optional Week 10 Sokoni catalog stub lane.

## Week reuse

| Week | Folder / file |
| --- | --- |
| 6 | `services/triage/` |
| 7 | `agents/tools/logistics.py` |
| 8 | `services/triage/prompts/pin.json` |
| 9 | `tests/test_security_smoke.py` |
| 10 | `services/catalog/stub_mismatch.py` |

## Quick start

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python scripts/make_fixture.py --rows 300 --out fixtures/triage_messages_sample.jsonl
python -m services.triage.rag_smoke
pytest -q
uvicorn services.triage.app:app --port 8000
```

## Demo script (3 commands)

**1 — Start the service**

```bash
uvicorn services.triage.app:app --port 8000
```

**2 — Confirm health**

```bash
curl -s http://localhost:8000/health
```

**3 — Send one demo message** (token, then triage — teaching user `nurse` / `nurse2026`)

```bash
curl -s -X POST http://localhost:8000/token -H "Content-Type: application/json" -d "{\"username\":\"nurse\",\"password\":\"nurse2026\"}"
curl -s -X POST http://localhost:8000/triage -H "Authorization: Bearer <access_token>" -H "Content-Type: application/json" -d "{\"message\":\"child has fever\",\"county\":\"Nairobi\"}"
```

Stub mode by default. Optional live triage: set `OPENAI_API_KEY` in `.env` and `FORCE_STUB=0` (see `docs/deployment.md`).

## Docs

- docs/architecture.md
- docs/deployment.md
- docs/cost_analysis.md
- docs/user_guide.md
- docs/build_checkpoint.md

## Presentation

Fill `docs/presentation_outline_filled.md`; export **docs/presentation.pdf** before Week 12 Monday.

## Peer review

- review_log.md
- docs/peer_review_checklist.md
- docs/PR_TEMPLATE.md
