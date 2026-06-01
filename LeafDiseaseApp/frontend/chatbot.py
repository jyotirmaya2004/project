import streamlit as st


def initialize_chat():

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "chat_open" not in st.session_state:
        st.session_state.chat_open = False


def toggle_chat():

    st.session_state.chat_open = (
        not st.session_state.chat_open
    )


def chatbot_ui():

    initialize_chat()

    # Floating Button
    st.markdown("""
    <style>

    .chat-button{
        position:fixed;
        bottom:20px;
        right:20px;
        z-index:999;
    }

    </style>
    """,
    unsafe_allow_html=True)

    col1, col2 = st.columns([8,1])

    with col2:
        if st.button("🤖"):
            toggle_chat()

    if st.session_state.chat_open:

        st.markdown("---")
        st.subheader("🌿 LeafGuard AI Assistant")

        for msg in st.session_state.messages:

            with st.chat_message(msg["role"]):
                st.write(msg["content"])

        user_prompt = st.chat_input(
            "Ask about plant diseases..."
        )

        if user_prompt:

            st.session_state.messages.append(
                {
                    "role":"user",
                    "content":user_prompt
                }
            )

            with st.chat_message("user"):
                st.write(user_prompt)

            # Temporary Response
            response = (
                "AI assistant response will appear here."
            )

            st.session_state.messages.append(
                {
                    "role":"assistant",
                    "content":response
                }
            )

            with st.chat_message("assistant"):
                st.write(response)