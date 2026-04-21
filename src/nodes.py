from __future__ import annotations

from typing import Any

from src.config import settings
from src.extractor import LeadInfoExtractor
from src.intent_classifier import IntentClassifier
from src.lead_tool import mock_lead_capture
from src.rag import LocalRAG


class NodeFactory:
    def __init__(self, rag: LocalRAG):
        self.rag = rag
        self.classifier = IntentClassifier()
        self.extractor = LeadInfoExtractor()
        self._response_llm = None
        if settings.openai_api_key:
            from langchain_openai import ChatOpenAI

            self._response_llm = ChatOpenAI(
                model=settings.openai_model,
                temperature=0.2,
                api_key=settings.openai_api_key,
            )

    def classify_intent(self, state: dict[str, Any]) -> dict[str, Any]:
        result = self.classifier.classify(state["user_message"])
        return {"intent": result.intent}

    def greeting_node(self, state: dict[str, Any]) -> dict[str, Any]:
        return {
            "response": "Hi! I can help with AutoStream pricing, features, support, and getting you started. What would you like to know?",
            "needs_followup": False,
        }

    def rag_node(self, state: dict[str, Any]) -> dict[str, Any]:
        context = self.rag.retrieve(state["user_message"])
        if self._response_llm:
            prompt = f"""
You are a sales support assistant for AutoStream.
Answer only using the provided context.
If the answer is not in the context, say you can only answer based on the current knowledge base.
Keep the answer concise and helpful.

Context:
{context}

User question:
{state['user_message']}
"""
            response = self._response_llm.invoke(prompt).content
        else:
            response = self._offline_grounded_response(state["user_message"], context)
        return {
            "retrieved_context": context,
            "response": response,
            "needs_followup": False,
        }

    def qualification_node(self, state: dict[str, Any]) -> dict[str, Any]:
        updated = self.extractor.update_state_from_message(state, state["user_message"])
        missing = self.extractor.missing_fields(updated)
        if missing:
            prompts = {
                "name": "your name",
                "email": "your email address",
                "platform": "your creator platform (YouTube, Instagram, etc.)",
            }
            if len(missing) == 1:
                ask = prompts[missing[0]]
            elif len(missing) == 2:
                ask = f"{prompts[missing[0]]} and {prompts[missing[1]]}"
            else:
                ask = "your name, email address, and creator platform"
            response = f"Great — I can help you get started with AutoStream. Please share {ask}."
            return {
                **{k: updated.get(k) for k in ["name", "email", "platform"]},
                "missing_fields": missing,
                "needs_followup": True,
                "response": response,
            }

        result = mock_lead_capture(updated["name"], updated["email"], updated["platform"])
        return {
            **{k: updated.get(k) for k in ["name", "email", "platform"]},
            "missing_fields": [],
            "lead_captured": True,
            "lead_result": result,
            "needs_followup": False,
            "response": (
                f"You're all set, {updated['name']}. I've captured your interest for AutoStream on {updated['platform']} "
                f"using {updated['email']}. Our team can follow up with the next steps."
            ),
        }

    def fallback_node(self, state: dict[str, Any]) -> dict[str, Any]:
        updated = self.extractor.update_state_from_message(state, state["user_message"])
        if state.get("needs_followup"):
            return self.qualification_node(updated)
        return {
            "response": "I can help with AutoStream pricing, features, policies, or getting you started on a plan.",
            "needs_followup": False,
        }

    @staticmethod
    def _offline_grounded_response(question: str, context: str) -> str:
        q = question.lower()
        if "pro" in q and ("price" in q or "pricing" in q or "cost" in q):
            return "The Pro plan is $79/month and includes unlimited videos, 4K resolution, AI captions, and 24/7 support."
        if "basic" in q and ("price" in q or "pricing" in q or "cost" in q):
            return "The Basic plan is $29/month and includes 10 videos per month at 720p resolution."
        if "refund" in q:
            return "AutoStream does not offer refunds after 7 days."
        if "support" in q:
            return "24/7 support is available only on the Pro plan."
        if "pricing" in q or "plan" in q or "feature" in q:
            return (
                "AutoStream offers a Basic plan at $29/month for 10 videos at 720p, and a Pro plan at $79/month with "
                "unlimited videos, 4K resolution, AI captions, and 24/7 support."
            )
        return f"Based on the current knowledge base, here is the most relevant information:\n\n{context}"
