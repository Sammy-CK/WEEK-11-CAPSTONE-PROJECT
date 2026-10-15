# Cost analysis

| Call type | Calls (n) | Unit cost | Total | Assumptions |
| --- | --- | --- | --- | --- |
| Stub tests (CI + local pytest) | 0 live | $0 | $0 | GitHub Actions has no `OPENAI_API_KEY`; `FORCE_STUB=1` |
| Local stub demo | unlimited | $0 | $0 | Default path for Week 12 rehearsal |
| Optional live triage demo | ~10 | ~$0.001–0.02 per mini call | ~$0.01–0.20 | `gpt-4o-mini`, low max_tokens; teaching cap ~$1 |
| Agent / MCP loops | 0 | — | $0 | Not enabled; no autonomous tool loops in this build |

**Budget honesty:** Soft cohort ceiling ~$5/week; live demo stays a small, capped slice if used at all.
