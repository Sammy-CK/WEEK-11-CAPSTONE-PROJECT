"""AfyaPlus triage API — Week 6 boundary, Week 8 pins, Week 9 auth (stub model)."""
import hashlib
import json
import os
from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, Field

from services.triage.auth import check_password, create_token, current_user

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
        "stub_mode": os.getenv("OPENAI_API_KEY") in (None, "", "stub"),
    }


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
    result = stub_triage(request.message, request.county, pin)
    return TriageResponse(
        urgency=result["urgency"],
        advice=result["advice"],
        model_id=result["model_id"],
        prompt_version=result["prompt_version"],
        handled_for=user["sub"],
        stub_mode=result["stub_mode"],
    )
