import json
from pathlib import Path

from agents.router import route

GOLD = {
    "T-001": ("fever", "triage"),
    "T-002": ("track delivery", "logistics_lookup"),
    "T-003": ("listing photo mismatch", "catalog_mismatch"),
}


def _gold_rows():
    path = Path("fixtures/triage_messages_sample.jsonl")
    by_id = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        by_id[row["id"]] = row
    return by_id


def test_gold_rows_match_router():
    rows = _gold_rows()
    for gid, (text, label) in GOLD.items():
        row = rows[gid]
        assert row["text"] == text
        assert row["label"] == label
        assert route(row["text"]) == label


def test_route_catalog_mismatch_intent():
    assert route("listing photo mismatch") == "catalog_mismatch"
