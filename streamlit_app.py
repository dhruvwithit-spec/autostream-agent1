from __future__ import annotations

from copy import deepcopy

import streamlit as st

from src.config import settings
from src.graph import AutoStreamAgent

st.set_page_config(page_title="AutoStream Lead Agent", page_icon="🎬", layout="centered")
st.title("🎬 AutoStream Lead Agent")
st.caption("Demo app for the ServiceHive / Inflx assignment")

if "agent" not in st.session_state:
    st.session_state.agent = AutoStreamAgent(settings.knowledge_base_path)
if "state" not in st.session_state:
    st.session_state.state = {
        "history": [],
        "lead_captured": False,
        "needs_followup": False,
        "missing_fields": [],
        "name": None,
        "email": None,
        "platform": None,
    }

for message in st.session_state.state["history"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask about pricing or say you want to try the Pro plan"):
    with st.chat_message("user"):
        st.markdown(prompt)

    run_state = deepcopy(st.session_state.state)
    run_state["user_message"] = prompt
    run_state["history"] = st.session_state.state["history"] + [{"role": "user", "content": prompt}]
    result = st.session_state.agent.invoke(run_state)
    reply = result.get("response", "I wasn't able to respond.")

    st.session_state.state.update({
        "name": result.get("name"),
        "email": result.get("email"),
        "platform": result.get("platform"),
        "lead_captured": result.get("lead_captured", False),
        "needs_followup": result.get("needs_followup", False),
        "missing_fields": result.get("missing_fields", []),
        "history": run_state["history"] + [{"role": "assistant", "content": reply}],
    })

    with st.chat_message("assistant"):
        st.markdown(reply)

with st.expander("Current session state"):
    st.json({
        "name": st.session_state.state.get("name"),
        "email": st.session_state.state.get("email"),
        "platform": st.session_state.state.get("platform"),
        "lead_captured": st.session_state.state.get("lead_captured"),
        "needs_followup": st.session_state.state.get("needs_followup"),
        "missing_fields": st.session_state.state.get("missing_fields"),
    })
