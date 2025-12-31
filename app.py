from dotenv import load_dotenv
import os
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
print("GROQ API Key:", api_key)

import requests
url = "https://api.groq.com/openai/v1/models"
headers = {
    "Authorization": f"Bearer {api_key}"
}
response = requests.get(url, headers=headers)
print(response.json())

import streamlit as st
from langchain_groq import ChatGroq
#from langchain.chains import ConversationChain
from langchain_classic.chains import ConversationChain
#from langchain.memory import ConversationBufferMemory
from langchain_classic.memory import ConversationBufferMemory
import os
from dotenv import load_dotenv

load_dotenv()

# Page configuration
st.set_page_config(page_title="Groq Chatbot", page_icon="⚡")

st.title("⚡ Groq Q&A Conversation Chatbot")

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "conversation" not in st.session_state:
    llm = ChatGroq(
        groq_api_key=os.getenv("GROQ_API_KEY"),
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
        st.markdown(f"*🧑 You:* {msg}")
    else:
        st.markdown(f"*🤖 Bot:* {msg}")