from __future__ import annotations

from src.knowledge_base import KnowledgeBase
from src.nodes import NodeFactory
from src.rag import LocalRAG
from src.state import AgentState


def route_from_intent(state: AgentState) -> str:
    intent = state.get("intent", "other")
    if intent == "greeting":
        return "greeting"
    if intent == "pricing_inquiry":
        return "rag"
    if intent == "high_intent":
        return "qualification"
    return "fallback"


class AutoStreamAgent:
    def __init__(self, knowledge_base_path: str):
        kb = KnowledgeBase(knowledge_base_path)
        rag = LocalRAG(kb)
        self.nodes = NodeFactory(rag)
        self._langgraph_app = None

        try:
            from langgraph.graph import END, START, StateGraph

            graph = StateGraph(AgentState)
            graph.add_node("classify_intent", self.nodes.classify_intent)
            graph.add_node("greeting", self.nodes.greeting_node)
            graph.add_node("rag", self.nodes.rag_node)
            graph.add_node("qualification", self.nodes.qualification_node)
            graph.add_node("fallback", self.nodes.fallback_node)

            graph.add_edge(START, "classify_intent")
            graph.add_conditional_edges(
                "classify_intent",
                route_from_intent,
                {
                    "greeting": "greeting",
                    "rag": "rag",
                    "qualification": "qualification",
                    "fallback": "fallback",
                },
            )
            graph.add_edge("greeting", END)
            graph.add_edge("rag", END)
            graph.add_edge("qualification", END)
            graph.add_edge("fallback", END)
            self._langgraph_app = graph.compile()
        except ModuleNotFoundError:
            self._langgraph_app = None

    def invoke(self, state: AgentState) -> AgentState:
        if self._langgraph_app is not None:
            return self._langgraph_app.invoke(state)

        # Fallback execution path for environments where langgraph is not installed.
        merged = dict(state)
        merged.update(self.nodes.classify_intent(merged))
        route = route_from_intent(merged)
        if route == "greeting":
            merged.update(self.nodes.greeting_node(merged))
        elif route == "rag":
            merged.update(self.nodes.rag_node(merged))
        elif route == "qualification":
            merged.update(self.nodes.qualification_node(merged))
        else:
            merged.update(self.nodes.fallback_node(merged))
        return merged
