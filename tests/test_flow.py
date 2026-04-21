from src.graph import AutoStreamAgent


def initial_state():
    return {
        "history": [],
        "lead_captured": False,
        "needs_followup": False,
        "missing_fields": [],
        "name": None,
        "email": None,
        "platform": None,
    }


def test_pricing_response_contains_pro_price():
    agent = AutoStreamAgent("data/knowledge_base.md")
    state = initial_state()
    state["user_message"] = "Tell me about your Pro pricing"
    result = agent.invoke(state)
    assert "$79" in result["response"]


def test_lead_capture_only_after_all_fields_present():
    agent = AutoStreamAgent("data/knowledge_base.md")

    state = initial_state()
    state["user_message"] = "I want to try the Pro plan for my YouTube channel"
    result = agent.invoke(state)
    assert result["needs_followup"] is True
    assert result.get("lead_captured") is not True
    assert result.get("platform") == "Youtube"

    next_state = initial_state()
    next_state.update({
        "platform": result.get("platform"),
        "needs_followup": result.get("needs_followup"),
        "missing_fields": result.get("missing_fields"),
    })
    next_state["user_message"] = "My name is Dhruv and my email is dhruv@example.com"
    result2 = agent.invoke(next_state)
    assert result2["lead_captured"] is True
    assert result2["lead_result"]["status"] == "success"
