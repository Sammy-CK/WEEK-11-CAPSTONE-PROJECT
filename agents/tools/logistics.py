"""Week 7 MCP logistics habit — structured dicts for agents (no raw SQL in prompts)."""

VALID_ITEMS = ["amoxicillin", "ors_sachets", "malaria_kits"]

_STUB_STOCK = {
    "amoxicillin": 42,
    "ors_sachets": 18,
    "malaria_kits": 7,
}


def lookup_shipment(tracking_id: str) -> dict:
    tid = tracking_id.strip().upper()
    return {
        "tracking_id": tid,
        "status": "in_transit",
        "eta_days": 2,
        "carrier": "AfyaPlus logistics (stub)",
    }


def check_stock(item: str) -> dict:
    if item not in VALID_ITEMS:
        return {"error": f"Unknown item '{item}'. Valid: {VALID_ITEMS}"}
    units = _STUB_STOCK[item]
    return {
        "item": item,
        "units": units,
        "reorder_needed": units < 10,
    }
