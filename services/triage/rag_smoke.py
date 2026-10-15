"""Ground one answer in the small doc set (stub mode). Run: python -m services.triage.rag_smoke"""
from services.triage.rag import ground_answer


def main() -> int:
    snippet = ground_answer("fever ORS rehydration")
    print("grounded:", snippet)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
