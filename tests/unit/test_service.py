import json
from pathlib import Path

from services.triage.app import handle_message


def test_service_runs_in_stub_mode():
    out = handle_message({"text": "hello"}, stub=True)
    assert out["status"] == "ok"
    assert out["stub_mode"] is True


def test_pin_has_model_and_version():
    pin = json.loads(Path("services/triage/prompts/pin.json").read_text(encoding="utf-8"))
    assert pin.get("model_id") and pin.get("prompt_version")
