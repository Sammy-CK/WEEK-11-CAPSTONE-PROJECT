# User guide

## Run

See `docs/deployment.md`. From repo root:

```bash
uvicorn services.triage.app:app --port 8000
```

## Health check

```bash
curl -s http://localhost:8000/health
```

## Authenticated triage

1. Obtain a token (teaching users: `nurse` / `nurse2026`):
   ```bash
   curl -s -X POST http://localhost:8000/token -H "Content-Type: application/json" -d "{\"username\":\"nurse\",\"password\":\"nurse2026\"}"
   ```
2. Call triage with `Authorization: Bearer <access_token>`:
   ```bash
   curl -s -X POST http://localhost:8000/triage -H "Authorization: Bearer <token>" -H "Content-Type: application/json" -d "{\"message\":\"child has fever\",\"county\":\"Nairobi\"}"
   ```

Response includes `stub_mode`: **true** in CI and by default locally; **false** only when `OPENAI_API_KEY` is set and `FORCE_STUB=0`.

## Fallback path

Missing or stub API key → rule-based urgency/advice, RAG snippet from markdown corpus, logistics/catalog routes return stub tool payloads. No silent pass on empty fixtures (diagnose and pytest fail loudly).

## Fixture location

`fixtures/triage_messages_sample.jsonl` — **~300** synthetic labelled rows (200–500 teaching band). Catalog data stays out of this file.
