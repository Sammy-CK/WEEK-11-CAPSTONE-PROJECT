"""Agent stub: route message, optional RAG + one MCP-style tool (no live key)."""
from services.triage.handler import handle_message


def run_agent(text: str) -> dict:
    return handle_message({"text": text}, stub=True)
