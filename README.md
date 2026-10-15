# Module 4 Capstone: AfyaPlus integrated health operations

Integrated Week 6–10 artefacts: triage API with JWT and Week 8 pins, Week 7 logistics tool surface, Week 9 security smoke, optional Week 10 Sokoni catalog lane (`services/catalog/`, deferred).

## Week reuse


| Week | Folder / file                                                  |
| ---- | -------------------------------------------------------------- |
| 6    | `services/triage/` (API, auth pattern from triage capstone)    |
| 7    | `agents/tools/logistics.py`                                    |
| 8    | `services/triage/prompts/pin.json`                             |
| 9    | `tests/test_security_smoke.py`, JWT on `/triage`               |
| 10   | `services/catalog/` (catalog mismatch lane, separate fixtures) |


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

```bash
curl -s http://localhost:8000/health
```



## Docs

- docs/architecture.md
- docs/deployment.md
- docs/cost_analysis.md
- docs/user_guide.md
- docs/build_checkpoint.md



## Demo (Week 12)

Start service, `GET /health`, `POST /token` then authenticated `POST /triage` (stub mode without live key).

## Peer review

- review_log.md
- docs/peer_review_checklist.md

