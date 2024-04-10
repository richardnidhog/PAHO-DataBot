import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from openai import OpenAI

st.title('Data Visualization Chatting Bot')

# Sidebar configuration for OpenAI API Key
with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")


st.caption("Upload your CSV data and ask me to visualize it for you!")

# User uploads CSV
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("Data Preview:")
    st.dataframe(df.head(5))

# Initialize chat messages in session state if not already present
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you with your data?"}]

# Display chat history
for msg in st.session_state["messages"]:
    st.chat_message(msg["role"]).write(msg["content"])

# User inputs a request
prompt = st.chat_input()

if prompt:
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
    else:
        # Authenticate with OpenAI and send the user's request
        client = OpenAI(api_key=openai_api_key)
        st.session_state.messages.append({"role": "user", "content": prompt})
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=[
                {"role": "system", "content": "You are an expert in writing code and analyzing data. You will answer questions and provide images for data visualization based on user needs. Python is used by default."},
                {"role": "user", "content": prompt}
            ],
        )
        
        # Get the assistant's response from OpenAI
        msg = response.choices[0].message.content.strip()
        st.chat_message("assistant").write(msg)

        # Assuming the message potentially contains visualization commands, process it.
        # This is where you would parse and handle the assistant's response to generate visualizations.

# Note: You would need to add here the logic for interpreting and acting on the assistant's response.