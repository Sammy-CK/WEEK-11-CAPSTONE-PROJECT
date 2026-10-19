"""AfyaPlus triage API — Week 6 boundary, Week 8 pins, Week 9 auth (stub model)."""
import hashlib
import json
import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, Field

from services.triage.auth import check_password, create_token, current_user
from services.triage.handler import handle_message
import dotenv
dotenv.load_dotenv()

load_dotenv()

PROMPTS_DIR = Path(__file__).resolve().parent / "prompts"
PIN_PATH = PROMPTS_DIR / "pin.json"
PROMPT_VERSION = "1.2.0"
SERVICE_VERSION = "11.0.0-monday"

app = FastAPI(title="AfyaPlus Triage", version=SERVICE_VERSION)


def prompt_sha() -> str:
    path = PROMPTS_DIR / f"triage_system_v{PROMPT_VERSION}.txt"
    if path.is_file():
        return hashlib.sha256(path.read_text(encoding="utf-8").encode()).hexdigest()
    return "missing"


def load_pin() -> dict:
    if PIN_PATH.is_file():
        return json.loads(PIN_PATH.read_text(encoding="utf-8"))
    return {}


class LoginRequest(BaseModel):
    username: str
    password: str


class TriageRequest(BaseModel):
    message: str = Field(min_length=1, max_length=2000)
    county: str = Field(default="Nairobi", min_length=2, max_length=40)


class TriageResponse(BaseModel):
    urgency: str = Field(pattern="^(low|medium|high)$")
    advice: str = Field(min_length=5, max_length=500)
    model_id: str
    prompt_version: str
    handled_for: str
    stub_mode: bool
    grounded_snippet: str


def should_use_stub(force_stub: bool = False) -> bool:
    if force_stub:
        return True
    if os.getenv("FORCE_STUB", "1") == "1":
        return True
    return os.getenv("OPENAI_API_KEY", "") in ("", "stub")


def stub_triage(message: str, county: str, pin: dict) -> dict:
    low = message.lower()
    urgency = "low"
    if any(w in low for w in ("chest pain", "bleeding", "unconscious", "cannot breathe")):
        urgency = "high"
    elif any(w in low for w in ("fever", "pain", "vomit")):
        urgency = "medium"
    advice = (
        f"Monitor symptoms in {county}. Seek in-person care if they worsen. "
        "This is not a diagnosis."
    )
    model_id = pin.get("model_id") or os.getenv("TRIAGE_MODEL", "stub-triage-v1")
    return {
        "urgency": urgency,
        "advice": advice,
        "model_id": model_id,
        "prompt_version": pin.get("prompt_version", PROMPT_VERSION),
        "stub_mode": True,
    }


def live_triage(message: str, county: str, pin: dict) -> dict:
    """Optional live call when key present and FORCE_STUB=0; fail closed to stub."""
    from openai import OpenAI

    model = pin.get("model_id") or "gpt-4o-mini"
    if model == "stub-triage-v1":
        model = "gpt-4o-mini"
    prompt_path = PROMPTS_DIR / f"triage_system_v{PROMPT_VERSION}.txt"
    system = (
        prompt_path.read_text(encoding="utf-8")
        if prompt_path.is_file()
        else "Never diagnose. Classify urgency low, medium, or high."
    )
    try:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = client.chat.completions.create(
            model=model,
            temperature=0,
            max_tokens=120,
            messages=[
                {"role": "system", "content": system},
                {
                    "role": "user",
                    "content": (
                        f"County: {county}. Message: {message}. "
                        "Reply with URGENCY: low|medium|high then ADVICE: one short sentence."
                    ),
                },
            ],
        )
    except Exception:
        out = stub_triage(message, county, pin)
        out["stub_mode"] = True
        return out

    text = response.choices[0].message.content or ""
    urgency = "low"
    advice = "Seek in-person care if symptoms worsen. Not a diagnosis."
    for line in text.splitlines():
        upper = line.upper()
        if upper.startswith("URGENCY:"):
            value = line.split(":", 1)[1].strip().lower()
            if value in ("low", "medium", "high"):
                urgency = value
        if upper.startswith("ADVICE:"):
            advice = line.split(":", 1)[1].strip()
    return {
        "urgency": urgency,
        "advice": advice,
        "model_id": model,
        "prompt_version": pin.get("prompt_version", PROMPT_VERSION),
        "stub_mode": False,
    }


def triage_for_message(message: str, county: str, pin: dict, force_stub: bool) -> dict:
    if should_use_stub(force_stub):
        return stub_triage(message, county, pin)
    return live_triage(message, county, pin)


@app.get("/health")
def health():
    pin = load_pin()
    sha = prompt_sha()
    pin_sha = pin.get("prompt_sha256")
    return {
        "status": "ok",
        "service": "afyaplus-triage",
        "version": SERVICE_VERSION,
        "prompt_version": pin.get("prompt_version", PROMPT_VERSION),
        "prompt_sha256": sha,
        "prompt_pin_match": pin_sha == sha if pin_sha else None,
        "model_id": pin.get("model_id"),
    }


@app.post("/token")
def login(body: LoginRequest):
    if not check_password(body.username, body.password):
        raise HTTPException(status_code=401, detail="Wrong username or password.")
    return {"access_token": create_token(body.username), "token_type": "bearer"}


@app.post("/triage", response_model=TriageResponse)
def triage(request: TriageRequest, user: dict = Depends(current_user)):
    pin = load_pin()
    result = handle_message(
        {"text": request.message, "message": request.message, "county": request.county},
        stub=False,
    )
    if result.get("status") != "ok":
        raise HTTPException(status_code=400, detail=result.get("detail", "bad request"))
    if result["route"] == "logistics_lookup":
        tr = result["tool_result"]
        advice = f"Logistics lookup (stub): shipment {tr['tracking_id']} is {tr['status']}."
        urgency = "low"
    elif result["route"] == "catalog_mismatch":
        advice = f"Catalog lane (stub): flagged={result['catalog_flagged']}."
        urgency = "low"
    else:
        urgency = result["urgency"]
        advice = result["advice"]
    model_id = result.get("model_id") or pin.get("model_id", "stub-triage-v1")
    prompt_version = result.get("prompt_version") or pin.get("prompt_version", PROMPT_VERSION)
    return TriageResponse(
        urgency=urgency,
        advice=advice,
        model_id=model_id,
        prompt_version=prompt_version,
        handled_for=user["sub"],
        stub_mode=result["stub_mode"],
        grounded_snippet=result.get("grounded_snippet", ""),
    )
