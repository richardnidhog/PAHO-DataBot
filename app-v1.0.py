import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from openai import OpenAI

def preprocess_dataset(df):
    # Example preprocessing logic
    df.dropna(inplace=True)
    # Additional preprocessing steps here as needed (data cleaning, feature selection, etc.)
    return df

def summarize_dataset(df):
    # Create a summary of the dataset for initial insights
    summary = f"- Number of Rows: {len(df)}\n- Number of Columns: {len(df.columns)}"
    return summary

st.title('Data Visualization Chatting Bot')

# Sidebar configuration for OpenAI API Key
with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")

st.caption("Upload your CSV data and ask me to visualize it for you!")

# User uploads CSV
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    df = preprocess_dataset(df)
    dataset_summary = summarize_dataset(df) # Summarize after preprocessing
    
    if 'initiated' not in st.session_state or not st.session_state['initiated']:
        dataset_ready_message = f"The dataset has been uploaded and is ready for analysis. The summary information is {dataset_summary}.\nThe file name is {uploaded_file.name}.\nWe can proceed with data visualizations."
        st.session_state['initiated'] = True
        st.session_state["messages"].append({"role": "system", "content": dataset_ready_message})
    
    st.write("Data Preview:")
    st.dataframe(df.head(5))
else:
    st.session_state['initiated'] = False

# Initialize chat messages in session state if not already present
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you with your data?"}]

# Display chat history
for msg in st.session_state["messages"]:
    st.chat_message(msg["role"]).write(msg["content"])

# User inputs a request
prompt = st.chat_input()
system_message = f"You are an expert in writing code and analyzing data. You will answer questions and provide images for data visualization based on user needs. Python is used by default. The summary information is {dataset_summary}. The file path is {uploaded_file.name}. The code you create should use this path to read the file."
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
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
        )
        
        # Get the assistant's response from OpenAI
        msg = response.choices[0].message.content.strip()
        st.chat_message("assistant").write(msg)

        # Assuming the message potentially contains visualization commands, process it.
        # This is where you would parse and handle the assistant's response to generate visualizations.

# Note: You would need to add here the logic for interpreting and acting on the assistant's response.