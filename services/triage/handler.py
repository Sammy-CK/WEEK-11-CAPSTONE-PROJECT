"""Orchestration for stub MVP: route, grounded lookup, one tool surface."""
from agents.router import route
from agents.tools.logistics import lookup_shipment
from services.catalog.stub_mismatch import flag_mismatch
from services.triage.rag import ground_answer


def handle_message(payload: dict, stub: bool = True) -> dict:
    text = (payload.get("text") or payload.get("message") or "").strip()
    if not text:
        return {"status": "error", "detail": "empty message"}

    from services.triage.app import load_pin, should_use_stub, triage_for_message

    tool = route(text)
    pin = load_pin()
    use_stub = should_use_stub(stub)
    out: dict = {
        "status": "ok",
        "route": tool,
        "stub_mode": use_stub,
    }

    if tool == "logistics_lookup":
        out["tool_result"] = lookup_shipment("AFYA-STUB-001")
        return out

    if tool == "catalog_mismatch":
        out["catalog_flagged"] = flag_mismatch(
            title=text,
            tags=["sisal", "kiondo"] if "listing" in text.lower() else ["generic"],
        )
        return out

    out["grounded_snippet"] = ground_answer(text)
    county = payload.get("county") or "Nairobi"
    tri = triage_for_message(text, county, pin, force_stub=stub)
    out["stub_mode"] = tri["stub_mode"]
    out["urgency"] = tri["urgency"]
    out["advice"] = tri["advice"]
    out["model_id"] = tri["model_id"]
    out["prompt_version"] = tri["prompt_version"]
    return out
