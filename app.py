from __future__ import annotations

from copy import deepcopy

from src.config import settings
from src.graph import AutoStreamAgent


def build_initial_state() -> dict:
    return {
        "history": [],
        "lead_captured": False,
        "needs_followup": False,
        "missing_fields": [],
        "name": None,
        "email": None,
        "platform": None,
    }


def main() -> None:
    print("AutoStream Lead Agent CLI")
    print("Type 'exit' to quit.\n")

    agent = AutoStreamAgent(settings.knowledge_base_path)
    state = build_initial_state()

    while True:
        user_message = input("You: ").strip()
        if user_message.lower() in {"exit", "quit"}:
            print("Session ended.")
            break

        run_state = deepcopy(state)
        run_state["user_message"] = user_message
        run_state["history"] = state.get("history", []) + [{"role": "user", "content": user_message}]

        result = agent.invoke(run_state)
        assistant_message = result.get("response", "I wasn't able to respond.")
        print(f"Agent: {assistant_message}\n")

        state.update({
            "name": result.get("name"),
            "email": result.get("email"),
            "platform": result.get("platform"),
            "lead_captured": result.get("lead_captured", False),
            "needs_followup": result.get("needs_followup", False),
            "missing_fields": result.get("missing_fields", []),
            "history": run_state["history"] + [{"role": "assistant", "content": assistant_message}],
        })


if __name__ == "__main__":
    main()
