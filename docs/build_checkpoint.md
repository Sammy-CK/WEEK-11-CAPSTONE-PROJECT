# Build checkpoint

## Works now
- `python check_proposal.py` and `python check_integration_map.py` exit 0
- `fixtures/triage_messages_sample.jsonl`: 300 synthetic rows
- `uvicorn services.triage.app:app --port 8000` → `GET /health` 200, pin match true
- JWT `POST /token` + authenticated `POST /triage` (stub, no live key)

## Incident note
- (Tuesday)

## Deferred
- RAG, agent router E2E, MCP server, catalog mismatch wiring (Week 10 lane)
- pytest security smoke green in CI, golden eval score
