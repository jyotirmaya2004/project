import html
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


def reset_chat():
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hello! Ask me about leaf diseases, crop care, pests, fertilizers, or treatment steps.",
        }
    ]


def initialize_chat():
    load_dotenv()

    if "messages" not in st.session_state:
        reset_chat()

    if "chat_open" not in st.session_state:
        st.session_state.chat_open = False


def _build_client() -> OpenAI | None:
    api_key = os.getenv("NVIDIA_API_KEY")
    if not api_key:
        return None

    return OpenAI(
        api_key=api_key,
        base_url=NVIDIA_BASE_URL,
    )


def _chat_with_nvidia() -> str:
    client = _build_client()
    if client is None:
        return "NVIDIA_API_KEY is missing. Add it to your .env file and restart Streamlit."

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
        model=os.getenv("NVIDIA_MODEL", DEFAULT_MODEL),
        messages=messages,
        temperature=_get_float_env("NVIDIA_TEMPERATURE", 0.6),
        top_p=_get_float_env("NVIDIA_TOP_P", 0.95),
        max_tokens=_get_int_env("NVIDIA_MAX_TOKENS", 1200),
    )

    return response.choices[0].message.content or "I could not generate a response."


def _render_message_bubbles():
    st.html('<div class="chat-log">')
    for message in st.session_state.messages:
        role = "user" if message["role"] == "user" else "assistant"
        icon = "fa-user" if role == "user" else "fa-seedling"
        content = html.escape(message["content"])
        st.html(
            f"""
            <div class="chat-bubble {role}">
                <i class="fa-solid {icon}"></i> {content}
            </div>
            """,
        )
    st.html("</div>")


def chatbot_ui():
    initialize_chat()

    st.html('<div class="chat-shell">')

    if not st.session_state.chat_open:
        st.html(
            """
            <div class="chat-card">
                <div class="chat-title">
                    <i class="fa-solid fa-comments"></i>
                    LeafGuard Assistant
                </div>
                <p class="chat-launch-copy">Ask about disease symptoms, treatment, pests, or crop care.</p>
            </div>
            """,
        )
        if st.button("Open plant chat", key="open_chat", use_container_width=True):
            st.session_state.chat_open = True
            st.rerun()

        st.html("</div>")
        return

    st.html(
        """
        <div class="chat-card">
            <div class="chat-header">
                <div class="chat-title">
                    <i class="fa-solid fa-comments"></i>
                    LeafGuard Assistant
                </div>
            </div>
        """,
    )

    col_close, col_clear = st.columns([1, 1])
    with col_close:
        if st.button("Close", key="close_chat", use_container_width=True):
            st.session_state.chat_open = False
            st.rerun()
    with col_clear:
        if st.button("Clear", key="clear_chat", use_container_width=True):
            reset_chat()
            st.rerun()

    _render_message_bubbles()

    with st.form("floating_chat_form", clear_on_submit=True):
        prompt = st.text_input(
            "Message",
            placeholder="Ask about leaf disease treatment...",
            label_visibility="collapsed",
        )
        submitted = st.form_submit_button("Send", use_container_width=True)

    if submitted and prompt.strip():
        st.session_state.messages.append({"role": "user", "content": prompt.strip()})

        with st.spinner("Thinking..."):
            try:
                response = _chat_with_nvidia()
            except Exception as exc:
                response = f"Chat API error: {exc}"

        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

    st.html("</div></div>")
