# Deployment

## Run locally

```bash
pip install -r requirements.txt
uvicorn services.triage.app:app --port 8000
```

## Env vars
- **OPENAI_API_KEY** — optional; unset or `stub` → triage uses rule-based stub
- **FORCE_STUB** — `1` (default) forces stub triage; set **`FORCE_STUB=0`** locally for optional live demo calls only
- **JWT_SECRET** — optional override for dev tokens (default dev secret in code for teaching)

Copy **`.env.example`** to **`.env`** locally; never commit `.env`.

## Health

`GET http://localhost:8000/health` should return **200** with pin/version fields.

## Fallback

Cloud deploy, Docker compose, and GPU hosts are **not executed live** for this capstone week. CI runs stub-only (`FORCE_STUB=1`, no API key). If credentials or Docker are missing locally, stub mode still demonstrates the full teaching path.
