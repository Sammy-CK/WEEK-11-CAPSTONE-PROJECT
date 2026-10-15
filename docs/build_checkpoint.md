# Build checkpoint

## Works now
- `pytest -q` green (unit layer); `pytest tests/test_security_smoke.py -q` green
- `python evals/run_eval.py evals/golden.jsonl` prints golden-set score
- `python scripts/diagnose_fixture.py fixtures/triage_messages_sample.jsonl` OK
- `python -m services.triage.rag_smoke` grounds one answer from `services/triage/knowledge/`
- Stub MVP: `handle_message` / `agents/run_stub.py` — route, RAG snippet, logistics tool
- `uvicorn services.triage.app:app --port 8000` → `GET /health` 200
- `perf_stub.json` from `scripts/measure_perf.py` (teaching p95, not SLA)

## Incident note
- Broke gold row T-002 by setting `label` to `triage` while text stayed `track delivery`.
- `pytest tests/unit/test_fixture_routes.py` failed on assert `route(...) == label`.
- Restored `label` to `logistics_lookup`; diagnose script and unit tests green again.

## Deferred
- Full Week 10 Sokoni `mismatch.py` join and catalog fixtures under `services/catalog/fixtures/`
- Live LLM calls; MCP server process (tool surface is stub dict today)
- Thursday doc pack, peer review deck, presentation PDF
