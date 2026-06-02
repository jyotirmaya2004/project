import os

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI


NVIDIA_BASE_URL = "https://integrate.api.nvidia.com/v1"
DEFAULT_MODEL = "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning"
SYSTEM_PROMPT = """
You are LeafGuard AI Assistant, a helpful agriculture and plant-health assistant.
Answer questions about plant diseases, crop care, fertilizers, pests, irrigation,
soil health, and safe treatment practices. If the user asks about something
outside agriculture or plant care, politely bring the conversation back to plants.
Keep answers practical and easy to follow.
""".strip()


def _get_float_env(name: str, default: float) -> float:
    try:
        return float(os.getenv(name, default))
    except (TypeError, ValueError):
        return default


def _get_int_env(name: str, default: int) -> int:
    try:
        return int(os.getenv(name, default))
    except (TypeError, ValueError):
        return default


def initialize_chat():
    load_dotenv()

    if "messages" not in st.session_state:
        reset_chat()


def reset_chat():
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hello! Ask me about leaf diseases, crop care, pests, fertilizers, or treatment steps.",
        }
    ]


def _build_client() -> OpenAI | None:
    api_key = os.getenv("NVIDIA_API_KEY")
    if not api_key:
        return None

    return OpenAI(
        api_key=api_key,
        base_url=NVIDIA_BASE_URL,
    )


def _chat_with_nvidia(user_prompt: str) -> str:
    client = _build_client()
    if client is None:
        return "NVIDIA_API_KEY is missing. Add it to your .env file and restart Streamlit."

    model = os.getenv("NVIDIA_MODEL", DEFAULT_MODEL)
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.extend(
        {
            "role": message["role"],
            "content": message["content"],
        }
        for message in st.session_state.messages
        if message["role"] in {"user", "assistant"}
    )
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=_get_float_env("NVIDIA_TEMPERATURE", 0.6),
        top_p=_get_float_env("NVIDIA_TOP_P", 0.95),
        max_tokens=_get_int_env("NVIDIA_MAX_TOKENS", 1200),
    )

    return response.choices[0].message.content or "I could not generate a response."


def chatbot_ui():
    initialize_chat()

    st.subheader("LeafGuard AI Assistant")

    col1, col2 = st.columns([1, 1])
    with col2:
        if st.button("Clear chat", use_container_width=True):
            reset_chat()
            st.rerun()

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    user_prompt = st.chat_input("Ask about plant diseases or crop care...")
    if not user_prompt:
        return

    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.write(user_prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = _chat_with_nvidia(user_prompt)
            except Exception as exc:
                response = f"Chat API error: {exc}"

            st.write(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
