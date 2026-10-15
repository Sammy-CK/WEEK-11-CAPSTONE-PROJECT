# Presentation outline (filled copy for Week 12 Monday)

1. **Problem and user** — Clinic coordinators and nurses need one intake channel for triage, logistics lookups, and optional catalog checks without mixing patient and marketplace data.

2. **Path chosen and why** — AfyaPlus Module 4 integrated capstone; reuses Weeks 6–10 artefacts instead of a blank notebook; finishable in one week on ~300 synthetic rows.

3. **Architecture diagram with module boundaries** — Client → `services/triage` (JWT) → `agents/router` → RAG (`knowledge/*.md`) + logistics tool + catalog stub; separate fixture boundaries.

4. **Skill coverage** — API (W6 `services/triage`), tools (W7 `logistics.py`), pins (W8 `pin.json`), security smoke (W9), optional catalog (W10 stub), tests/eval (W11).

5. **Live demo** — uvicorn :8000, `/health`, `/token` + `/triage`; stub default; optional one live triage if key + `FORCE_STUB=0`.

6. **Testing evidence** — `pytest -q` unit green; security smoke; golden eval **3/3**; GitHub Actions CI.

7. **Security and compliance choices** — JWT on `/triage`, `.env` gitignored, redaction helper tested, no secrets in repo, fail closed in CI.

8. **Cost table with assumptions** — CI $0 stub; optional ~10 live calls under ~$1 teaching cap.

9. **What works vs deferred** — Works: MVP stub E2E, RAG smoke, 300-row fixture. Deferred: full Sokoni join, production cloud deploy.

10. **Process** — Feature branch, PR with checklist review, `review_log.md`, next: Week 12 presentation PDF demo.
