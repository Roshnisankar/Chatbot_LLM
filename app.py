import os
import streamlit as st

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("GROQ API Key not found. Please add it in Streamlit Secrets.")
    st.stop()

st.success("API Key loaded successfully")

import requests
url = "https://api.groq.com/openai/v1/models"
headers = {
    "Authorization": f"Bearer {api_key}"
}
response = requests.get(url, headers=headers)
print(response.json())

import streamlit as st
import os
from langchain_groq import ChatGroq
from langchain_classic.chains import ConversationChain
from langchain_classic.memory import ConversationBufferMemory

# Page config (mobile friendly)
st.set_page_config(page_title="Groq Chatbot", page_icon="⚡", layout="centered")

st.title("⚡ Groq Q&A Conversation Chatbot")

# Get API key from Streamlit Secrets
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "conversation" not in st.session_state:
    llm = ChatGroq(
        groq_api_key=GROQ_API_KEY,
        model_name="llama-3.1-8b-instant",
        temperature=0.4
    )

    memory = ConversationBufferMemory()

    st.session_state.conversation = ConversationChain(
        llm=llm,
        memory=memory,
        verbose=False
    )

# User input
user_input = st.text_input("Ask a question:")

if st.button("Send") and user_input:
    response = st.session_state.conversation.predict(input=user_input)

    st.session_state.chat_history.append(("You", user_input))
    st.session_state.chat_history.append(("Bot", response))

# Display conversation
for role, msg in st.session_state.chat_history:
    if role == "You":
        st.markdown(f"🧑 **You:** {msg}")
    else:
        st.markdown(f"🤖 **Bot:** {msg}")

        st.markdown(f"*🧑 You:* {msg}")
    else:

        st.markdown(f"*🤖 Bot:* {msg}")


