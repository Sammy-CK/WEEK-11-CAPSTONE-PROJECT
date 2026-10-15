from agents.run_stub import run_agent


def test_agent_logistics_tool_stub():
    out = run_agent("track delivery")
    assert out["status"] == "ok"
    assert out["route"] == "logistics_lookup"
    assert out["tool_result"]["status"] == "in_transit"


def test_agent_triage_grounded():
    out = run_agent("fever and ORS question")
    assert out["status"] == "ok"
    assert out["route"] == "triage"
    assert "grounded_snippet" in out
