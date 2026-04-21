from __future__ import annotations

from pydantic import BaseModel, Field

from src.config import settings


class IntentResult(BaseModel):
    intent: str = Field(description="One of greeting, pricing_inquiry, high_intent, other")
    reason: str = Field(description="Short explanation")


class IntentClassifier:
    def __init__(self) -> None:
        self._llm = None
        if settings.openai_api_key:
            from langchain_openai import ChatOpenAI

            self._llm = ChatOpenAI(
                model=settings.openai_model,
                temperature=0,
                api_key=settings.openai_api_key,
            ).with_structured_output(IntentResult)

    def classify(self, message: str) -> IntentResult:
        if self._llm:
            prompt = f"""
Classify the user's latest message into one of these intents only:
- greeting
- pricing_inquiry
- high_intent
- other

Rules:
- greeting: simple hello/hi/hey without a real product question
- pricing_inquiry: asks about product, plans, pricing, features, support, policy
- high_intent: user indicates readiness to try, buy, sign up, book demo, start, or use a plan
- other: none of the above

User message: {message}
"""
            return self._llm.invoke(prompt)

        lower = message.lower()
        if any(word in lower for word in ["hello", "hi", "hey"]):
            if not any(word in lower for word in ["price", "pricing", "plan", "feature", "refund", "support"]):
                return IntentResult(intent="greeting", reason="Detected simple greeting")
        if any(phrase in lower for phrase in [
            "i want to try",
            "i want to sign up",
            "sign me up",
            "i want pro",
            "i want the pro plan",
            "that sounds good",
            "let's start",
            "i'm ready",
            "ready to start",
            "book demo",
            "get started",
            "start with",
        ]):
            return IntentResult(intent="high_intent", reason="Detected readiness to start or buy")
        if any(word in lower for word in ["price", "pricing", "plan", "feature", "features", "refund", "support", "cost"]):
            return IntentResult(intent="pricing_inquiry", reason="Detected product or pricing inquiry")
        return IntentResult(intent="other", reason="No strong signal found")
