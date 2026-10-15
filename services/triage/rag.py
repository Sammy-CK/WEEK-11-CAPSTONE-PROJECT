"""Small-document grounded lookup (stub — keyword match, no live embeddings)."""
from pathlib import Path

KNOWLEDGE_DIR = Path(__file__).resolve().parent / "knowledge"


def ground_answer(query: str) -> str:
    if not KNOWLEDGE_DIR.is_dir() or not any(KNOWLEDGE_DIR.glob("*.md")):
        raise FileNotFoundError("knowledge doc set missing or empty")
    q = query.lower()
    tokens = [w for w in q.split() if len(w) > 2]
    for md in sorted(KNOWLEDGE_DIR.glob("*.md")):
        for line in md.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            low = line.lower()
            if any(t in low for t in tokens):
                return line
    first = next(
        (
            line.strip()
            for md in sorted(KNOWLEDGE_DIR.glob("*.md"))
            for line in md.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ),
        None,
    )
    if first is None:
        raise ValueError("no grounding match in knowledge set")
    return first
