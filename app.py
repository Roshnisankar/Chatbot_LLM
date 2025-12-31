import os
import streamlit as st
from langchain_groq import ChatGroq

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Groq Chatbot",
    page_icon="⚡",
    layout="centered"
)

st.title("⚡ Groq Q&A Chatbot")

# ---------------- API KEY ----------------
api_key = st.secrets.get("GROQ_API_KEY")

if not api_key:
    st.error("❌ GROQ_API_KEY not found. Add it in Streamlit Secrets.")
    st.stop()

# ---------------- SESSION STATE ----------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "llm" not in st.session_state:
    st.session_state.llm = ChatGroq(
        groq_api_key=api_key,
        model_name="llama-3.1-8b-instant",
        temperature=0.4
    )

# ---------------- USER INPUT ----------------
user_input = st.text_input("Ask a question:")

if st.button("Send") and user_input.strip():
    llm = st.session_state.llm

    # Send conversation context manually
    conversation = ""
    for role, msg in st.session_state.chat_history:
        conversation += f"{role}: {msg}\n"

    conversation += f"You: {user_input}"

    response = llm.invoke(conversation).content

    st.session_state.chat_history.append(("You", user_input))
    st.session_state.chat_history.append(("Bot", response))

# ---------------- DISPLAY CHAT ----------------
for role, msg in st.session_state.chat_history:
    if role == "You":
        st.markdown(f"🧑 **You:** {msg}")
    else:
        st.markdown(f"🤖 **Bot:** {msg}")
