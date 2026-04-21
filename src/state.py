from __future__ import annotations

from typing import Literal, Optional, TypedDict

Intent = Literal["greeting", "pricing_inquiry", "high_intent", "other"]


class AgentState(TypedDict, total=False):
    user_message: str
    intent: Intent
    retrieved_context: str
    response: str
    name: Optional[str]
    email: Optional[str]
    platform: Optional[str]
    lead_captured: bool
    needs_followup: bool
    missing_fields: list[str]
    lead_result: Optional[dict]
    history: list[dict[str, str]]
