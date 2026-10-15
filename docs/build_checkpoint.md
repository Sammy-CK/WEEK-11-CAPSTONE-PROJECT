# Build checkpoint

## Works now
- **Path:** AfyaPlus Module 4 Capstone (`proposal.md`)
- **skill_matrix.md** and **integration_map.json** complete; map paths exist on disk
- **pytest -q** unit layer green; **tests/test_security_smoke.py** present; **eval** golden-set **3/3 = 1.00**
- **Minimum Working Product** end-to-end in **stub mode** (CI); optional **live triage** locally when `OPENAI_API_KEY` set and `FORCE_STUB=0`
- **fixtures/triage_messages_sample.jsonl:** ~300 synthetic triage rows (no production scrape)
- **RAG:** `python -m services.triage.rag_smoke` over `services/triage/knowledge/`
- **Agent stub:** `agents/run_stub.py` — route, grounded snippet, logistics tool
- **GitHub Actions:** ruff, pytest, smoke, eval

## Incident note (Tuesday diagnosis drill)
- Broke gold row **T-002** label to `triage` while text stayed `track delivery`.
- **pytest** `tests/unit/test_fixture_routes.py` failed; restored `logistics_lookup`.
- **diagnose_fixture.py** green after fix.

## Deferred
- Full Week 10 Sokoni **mismatch.py** join and dedicated catalog fixtures under `services/catalog/fixtures/`
- **Live cloud deploy** (steps documented only in `docs/deployment.md`)
- **Live LLM agent loops** beyond a capped Thursday demo (~$1 teaching budget)
- Running MCP server process (logistics returns structured dicts; no long-lived MCP in CI)
